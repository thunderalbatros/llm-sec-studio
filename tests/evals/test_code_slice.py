"""Deterministic evals for tools/code_slice.py and tools/token_audit_proxy.py."""
from pathlib import Path

from llm_sec_studio.tools.code_slice import extract_symbol, get_outline
from llm_sec_studio.tools.token_audit_proxy import compact_oversized_tool_text

ROOT = Path(__file__).resolve().parents[2]


def test_code_slice_outline_reduces_tokens_dramatically() -> None:
    for rel in (
        "src/llm_sec_studio/tools/run_gates.py",
        "src/llm_sec_studio/guardrails/input_sanitizer.py",
    ):
        path = ROOT / rel
        full_text = path.read_text(encoding="utf-8")
        outline = get_outline(path)
        assert len(outline) >= 3
        outline_text = "\n".join(str(item) for item in outline)
        savings = 1.0 - (len(outline_text) / len(full_text))
        assert savings >= 0.70, f"Expected >=70% reduction on {rel}, got {savings:.2%}"


def test_code_slice_extracts_exact_symbol_and_method() -> None:
    res_fn = extract_symbol(ROOT / "src" / "llm_sec_studio" / "tools" / "run_gates.py", "fast_hygiene_check")
    assert "def fast_hygiene_check" in res_fn["code"]
    assert res_fn["start"] < res_fn["end"]

    res_meth = extract_symbol(
        ROOT / "src" / "llm_sec_studio" / "guardrails" / "input_sanitizer.py",
        "SpotlightingSession.wrap",
    )
    assert "def wrap(" in res_meth["code"]
    assert "ESCAPED_BOUNDARY_TAG" in res_meth["code"]


def test_ccr_proxy_preserves_json_and_code_but_compacts_huge_logs() -> None:
    big_json = '{"items": [' + ",".join(['"a"'] * 4000) + "]}"
    assert compact_oversized_tool_text(big_json, threshold=1000) == big_json

    big_log = "\n".join(f"2026-11-19 INFO step={i} status=ok" for i in range(400))
    compacted = compact_oversized_tool_text(big_log, threshold=1000)
    assert "CCR_COMPACTED" in compacted
    assert len(compacted) < len(big_log) * 0.4
