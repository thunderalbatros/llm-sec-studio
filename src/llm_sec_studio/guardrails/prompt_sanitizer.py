#!/usr/bin/env python3
"""
tools/prompt_sanitizer.py — Lightweight local defense against Indirect Prompt Injection
and verbose trace bloat before feeding external HTML/Markdown/tool outputs to Qwen 3.8 27B.
Zero external dependencies by default (<2 ms, ~0 MB extra RAM on HP 250 G8).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

INVISIBLE_CHARS_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u2069\ufeff]")
HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")
HIDDEN_BLOCK_RE = re.compile(
    r"<(script|style|noscript|template)[^>]*>[\s\S]*?</\1>",
    flags=re.IGNORECASE,
)
HIDDEN_STYLE_ELEM_RE = re.compile(
    r"<([a-z0-9]+)[^>]*(?:display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\D|$)|font-size\s*:\s*0)[^>]*>[\s\S]*?</\1>",
    flags=re.IGNORECASE,
)
CONTROL_TOKENS_RE = re.compile(
    r"<\|(?:im_start|im_end|endoftext|system|user|assistant|tool_call|tool_response)\|>"
    r"|</?(?:tool_call|tool_response|system_prompt|instructions?)>",
    flags=re.IGNORECASE,
)

INJECTION_RULES: list[tuple[str, re.Pattern[str]]] = [
    (
        "instruction_override_en",
        re.compile(
            r"\b(?:ignore|disregard|forget|override|bypass)\b.{0,40}\b(?:previous|prior|above|system|all)\b.{0,30}\b(?:instructions?|rules?|prompts?|directives?)\b",
            flags=re.IGNORECASE,
        ),
    ),
    (
        "instruction_override_es",
        re.compile(
            r"\b(?:ignora|olvida|anula|descarta|omite)\b.{0,40}\b(?:anteriores?|previas?|del sistema|todas)\b.{0,30}\b(?:instrucciones?|reglas?|directivas?)\b",
            flags=re.IGNORECASE,
        ),
    ),
    (
        "role_hijack",
        re.compile(
            r"\b(?:you are now|act as an unrestricted|new system prompt|developer mode enabled|ahora eres un asistente sin restricciones)\b",
            flags=re.IGNORECASE,
        ),
    ),
    (
        "secret_exfiltration",
        re.compile(
            r"\b(?:read|cat|print|dump|send|exfiltrate|curl|post|leer|imprimir|enviar)\b.{0,60}(?:\.env\b|secrets\.json|qwen_api_key|id_rsa|api[_-]?key)",
            flags=re.IGNORECASE,
        ),
    ),
    (
        "markdown_image_exfil",
        re.compile(
            r"!\[[^\]]*\]\(https?://[^)\s]*(?:secret|token|key|env|exfil|leak|data=)[^)\s]*\)",
            flags=re.IGNORECASE,
        ),
    ),
    (
        "tool_call_smuggling",
        re.compile(
            r"<\|\s*(?:im_start|tool_call)\s*\|>|<(?:tool_call|function)\s*[^>]*>",
            flags=re.IGNORECASE,
        ),
    ),
]


def compress_trace(text: str, max_lines: int = 80) -> str:
    lines = text.splitlines()
    out: list[str] = []
    prev = None
    repeat_count = 0
    for line in lines:
        stripped = line.rstrip()
        if stripped == prev and stripped != "":
            repeat_count += 1
            continue
        if repeat_count > 0:
            out.append(f"... [repeated {repeat_count} more times]")
            repeat_count = 0
        out.append(stripped)
        prev = stripped
    if repeat_count > 0:
        out.append(f"... [repeated {repeat_count} more times]")
    if len(out) > max_lines:
        head = out[: max_lines // 2]
        tail = out[-(max_lines - len(head) - 1) :]
        omitted = len(out) - len(head) - len(tail)
        out = [*head, f"... [{omitted} lines omitted by prompt_sanitizer]", *tail]
    return "\n".join(out)


def sanitize_text(
    raw: str,
    source: str = "external",
    wrap: bool = False,
    compress: bool = False,
    max_chars: int = 12000,
) -> dict:
    findings: list[str] = []

    if INVISIBLE_CHARS_RE.search(raw):
        findings.append("invisible_unicode_stripped")
    normalized = unicodedata.normalize("NFKC", raw)
    cleaned = INVISIBLE_CHARS_RE.sub("", normalized)

    if HTML_COMMENT_RE.search(cleaned):
        findings.append("html_comments_stripped")
        cleaned = HTML_COMMENT_RE.sub(" ", cleaned)

    if HIDDEN_BLOCK_RE.search(cleaned):
        findings.append("script_style_blocks_stripped")
        cleaned = HIDDEN_BLOCK_RE.sub(" ", cleaned)

    if HIDDEN_STYLE_ELEM_RE.search(cleaned):
        findings.append("hidden_css_elements_stripped")
        cleaned = HIDDEN_STYLE_ELEM_RE.sub(" ", cleaned)

    # Detect semantic injection patterns BEFORE neutralizing control tokens
    for rule_id, pattern in INJECTION_RULES:
        if pattern.search(cleaned) or pattern.search(raw):
            findings.append(rule_id)

    if CONTROL_TOKENS_RE.search(cleaned):
        findings.append("control_tokens_neutralized")
        cleaned = CONTROL_TOKENS_RE.sub("[NEUTRALIZED_TOKEN]", cleaned)

    # Neutralize suspicious injection lines while preserving surrounding benign context
    safe_lines: list[str] = []
    for line in cleaned.splitlines():
        flagged = any(pat.search(line) for _, pat in INJECTION_RULES)
        if flagged:
            safe_lines.append("[QUARANTINED_INJECTION_LINE]")
        else:
            safe_lines.append(line)
    cleaned = "\n".join(safe_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    if compress:
        cleaned = compress_trace(cleaned)

    truncated = False
    if len(cleaned) > max_chars:
        cleaned = cleaned[: max_chars - 32] + "\n...[TRUNCATED_BY_SANITIZER]"
        truncated = True

    dedup_findings = list(dict.fromkeys(findings))
    risk_signals = [
        f
        for f in dedup_findings
        if f
        in {
            "instruction_override_en",
            "instruction_override_es",
            "role_hijack",
            "secret_exfiltration",
            "markdown_image_exfil",
            "tool_call_smuggling",
            "control_tokens_neutralized",
            "hidden_css_elements_stripped",
        }
    ]
    is_suspicious = len(risk_signals) > 0

    output_text = cleaned
    if wrap:
        safe_source = re.sub(r'[^A-Za-z0-9_.:/-]', "_", source)[:80]
        output_text = (
            f'<untrusted_data source="{safe_source}" suspicious="{str(is_suspicious).lower()}">\n'
            f"{cleaned}\n"
            "</untrusted_data>"
        )

    return {
        "suspicious": is_suspicious,
        "findings": dedup_findings,
        "risk_signals": risk_signals,
        "truncated": truncated,
        "orig_chars": len(raw),
        "clean_chars": len(output_text),
        "sanitized_text": output_text,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sanitize untrusted text against Indirect Prompt Injection.")
    parser.add_argument("--file", default="", help="Input file path (reads stdin if omitted)")
    parser.add_argument("--source", default="external", help="Origin label for <untrusted_data> wrapper")
    parser.add_argument("--wrap", action="store_true", help="Wrap sanitized output in <untrusted_data> tags")
    parser.add_argument("--compress", action="store_true", help="Deduplicate and cap long CLI/log traces")
    parser.add_argument("--max-chars", type=int, default=12000, help="Hard character cap")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()

    raw = Path(args.file).read_text(encoding="utf-8", errors="ignore") if args.file else sys.stdin.read()
    res = sanitize_text(
        raw,
        source=args.source,
        wrap=args.wrap,
        compress=args.compress,
        max_chars=args.max_chars,
    )
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(res["sanitized_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
