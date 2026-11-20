"""Token-bounded CLI and JSON output compressor wrapped with anti-prompt-injection Spotlighting."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

_SRC_DIR = Path(__file__).resolve().parents[2] / "src"


def _ensure_src_on_path() -> None:
    if _SRC_DIR.is_dir() and str(_SRC_DIR) not in sys.path:
        sys.path.insert(0, str(_SRC_DIR))


def est_tokens(text: str) -> int:
    """Estimate token count using the studio's conservative 4-chars/token rule."""
    return (len(text) + 3) // 4


def _write_raw_artifact(
    raw: str,
    source: str,
    spotlight_tag: str,
    artifact_dir: Path | str | None,
) -> str | None:
    if artifact_dir is None:
        return None
    target_dir = Path(artifact_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_source = re.sub(r"[^a-zA-Z0-9._-]+", "_", source).strip("_") or "cli"
    artifact_path = target_dir / f"{safe_source}_{spotlight_tag}.raw.txt"
    artifact_path.write_text(raw, encoding="utf-8")
    return str(artifact_path)


def _build_payload(
    sanitized: dict[str, Any],
    returncode: int,
    orig_chars: int,
    raw_artifact_path: str | None = None,
) -> dict[str, Any]:
    clean_text = str(sanitized["clean_text"])
    was_compacted = bool(
        sanitized["truncated"]
        or "omitted by input_sanitizer]" in clean_text
        or "more times]" in clean_text
    )
    payload: dict[str, Any] = {
        "source": sanitized["source"],
        "returncode": returncode,
        "risk_level": sanitized["risk_level"],
        "findings": sanitized["findings"],
        "truncated": was_compacted,
        "est_tokens": 999999,
        "orig_chars": orig_chars,
        "raw_artifact_path": raw_artifact_path,
        "spotlight_tag": sanitized["spotlight_tag"],
        "system_instruction": sanitized["system_instruction"],
        "spotlighted_text": sanitized["spotlighted_text"],
    }
    payload["est_tokens"] = est_tokens(json.dumps(payload, ensure_ascii=False))
    payload["est_tokens"] = est_tokens(json.dumps(payload, ensure_ascii=False))
    return payload


def compress_cli_output(
    raw: str,
    source: str,
    max_tokens: int = 1500,
    session_nonce: str | None = None,
    returncode: int = 0,
    artifact_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Sanitize, deduplicate, and bound raw CLI output strictly to <= max_tokens when JSON-serialized."""
    if max_tokens < 160:
        raise ValueError("max_tokens must be >= 160 to preserve spotlighting metadata")

    _ensure_src_on_path()
    from llm_sec_studio.guardrails.input_sanitizer import sanitize_untrusted_input

    orig_chars = len(raw)
    char_budget = max(200, max_tokens * 4 - 900)
    payload: dict[str, Any] = {}
    raw_artifact_path: str | None = None

    for _ in range(8):
        res = sanitize_untrusted_input(
            raw=raw,
            source=source,
            session_nonce=session_nonce,
            compress=True,
            max_chars=char_budget,
        )
        if raw_artifact_path is None and artifact_dir is not None:
            raw_artifact_path = _write_raw_artifact(raw, source, res["spotlight_tag"], artifact_dir)
        payload = _build_payload(
            res,
            returncode=returncode,
            orig_chars=orig_chars,
            raw_artifact_path=raw_artifact_path,
        )
        serialized_tokens = est_tokens(json.dumps(payload, ensure_ascii=False))
        payload["est_tokens"] = serialized_tokens
        if serialized_tokens <= max_tokens or char_budget <= 120:
            return payload
        overshoot_chars = max(80, (serialized_tokens - max_tokens) * 4 + 64)
        char_budget = max(120, char_budget - overshoot_chars)

    return payload


def compress_json_records(
    records: list[dict[str, Any]],
    source: str,
    max_tokens: int = 1500,
    max_items: int = 25,
    session_nonce: str | None = None,
    artifact_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Cap structured finding records and apply Spotlighting strictly within max_tokens."""
    if max_items < 1:
        raise ValueError("max_items must be >= 1")

    bounded = records[:max_items]
    summary = {
        "total_records": len(records),
        "included_records": len(bounded),
        "records": bounded,
    }
    # Multi-line JSON ensures line-level injection quarantine never wipes safe sibling fields/records.
    raw_json = json.dumps(summary, indent=2, ensure_ascii=False)
    payload = compress_cli_output(
        raw=raw_json,
        source=source,
        max_tokens=max_tokens,
        session_nonce=session_nonce,
        returncode=0,
        artifact_dir=artifact_dir,
    )
    if len(records) > len(bounded):
        payload["truncated"] = True
    return payload
