#!/usr/bin/env python3
"""
tools/llm_health_benchmark.py — Real End-to-End Micro-Benchmark for local IAP-tunneled llama.cpp server.
Measures:
  1. Streaming TTFT (ms), generation tok/s, prompt tok/s, and reasoning (<think>) vs content ratio.
  2. Nested JSON Tool Calling accuracy + live round-trip execution of tools/query_arsenal.py.
  3. Defensive vulnerability patching on a vulnerable SQL snippet.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def load_api_key() -> str:
    env_key = os.environ.get("OPENAI_COMPAT_API_KEY", "").strip()
    if env_key:
        return env_key
    sec_path = Path.home() / ".cline" / "data" / "secrets.json"
    if sec_path.is_file():
        data = json.loads(sec_path.read_text(encoding="utf-8"))
        if data.get("openAiApiKey"):
            return str(data["openAiApiKey"]).strip()
    env_path = ROOT / ".env"
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"^\s*OPENAI_COMPAT_API_KEY\s*=(.*)$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return ""


def post_json(url: str, payload: dict, api_key: str, timeout: int = 120) -> tuple[dict, float]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return data, elapsed_ms


def bench_streaming(base_url: str, model: str, api_key: str) -> dict:
    payload = {
        "model": model,
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": 0.7,
        "top_p": 0.80,
        "top_k": 20,
        "min_p": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 900,
        "messages": [
            {"role": "system", "content": "You are a concise senior TypeScript engineer."},
            {
                "role": "user",
                "content": "Write a 15-line TypeScript LRU cache class with get/set methods and O(1) operations using Map.",
            },
        ],
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    ttft_ms = None
    first_content_ms = None
    reasoning_parts: list[str] = []
    content_parts: list[str] = []
    timings = {}
    usage = {}

    with urllib.request.urlopen(req, timeout=120) as resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8", errors="ignore").strip()
            if not line.startswith("data:"):
                continue
            body = line[5:].strip()
            if body == "[DONE]":
                break
            try:
                evt = json.loads(body)
            except json.JSONDecodeError:
                continue
            if evt.get("timings"):
                timings = evt["timings"]
            if evt.get("usage"):
                usage = evt["usage"]
            choices = evt.get("choices") or []
            if not choices:
                continue
            delta = choices[0].get("delta") or {}
            rc = delta.get("reasoning_content")
            ct = delta.get("content")
            now_ms = (time.perf_counter() - t0) * 1000.0
            if (rc or ct) and ttft_ms is None:
                ttft_ms = now_ms
            if ct and first_content_ms is None:
                first_content_ms = now_ms
            if rc:
                reasoning_parts.append(rc)
            if ct:
                content_parts.append(ct)

    total_ms = (time.perf_counter() - t0) * 1000.0
    reasoning_txt = "".join(reasoning_parts)
    content_txt = "".join(content_parts)
    # Handle inline <think>...</think> if reasoning_content wasn't split
    if not reasoning_txt and "<think>" in content_txt:
        m = re.search(r"<think>([\s\S]*?)</think>", content_txt)
        if m:
            reasoning_txt = m.group(1)
            content_txt = re.sub(r"<think>[\s\S]*?</think>", "", content_txt).strip()

    r_chars = len(reasoning_txt)
    c_chars = len(content_txt)
    ratio = round(r_chars / max(1, c_chars), 3)
    pred_tps = round(float(timings.get("predicted_per_second", 0.0)), 2)
    prompt_tps = round(float(timings.get("prompt_per_second", 0.0)), 2)
    if pred_tps == 0.0 and usage.get("completion_tokens") and total_ms > 0:
        pred_tps = round(usage["completion_tokens"] / (total_ms / 1000.0), 2)

    return {
        "pass": bool(content_txt.strip() and ttft_ms is not None),
        "ttft_ms": round(ttft_ms or 0.0, 1),
        "first_content_ms": round(first_content_ms or 0.0, 1),
        "total_ms": round(total_ms, 1),
        "prompt_tok_s": prompt_tps,
        "gen_tok_s": pred_tps,
        "reasoning_chars": r_chars,
        "content_chars": c_chars,
        "think_to_answer_ratio": ratio,
        "usage": usage,
    }


def bench_nested_tool_calling(base_url: str, model: str, api_key: str) -> dict:
    payload = {
        "model": model,
        "temperature": 0.2,
        "top_p": 0.80,
        "top_k": 20,
        "min_p": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 900,
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "query_arsenal",
                    "description": "Search curated RAG knowledge via tools/query_arsenal.py.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search terms"},
                            "filters": {
                                "type": "object",
                                "properties": {
                                    "domain": {
                                        "type": "string",
                                        "enum": [
                                            "cybersec_audit",
                                            "agent_harness",
                                            "web_engineering",
                                            "browser_automation",
                                        ],
                                    },
                                    "top_k": {"type": "integer", "minimum": 1, "maximum": 3},
                                    "max_tokens": {"type": "integer", "minimum": 300, "maximum": 1500},
                                },
                                "required": ["domain", "top_k", "max_tokens"],
                            },
                        },
                        "required": ["query", "filters"],
                    },
                },
            }
        ],
        "tool_choice": "auto",
        "messages": [
            {
                "role": "system",
                "content": "Always invoke query_arsenal with exact nested filters when asked to query internal docs.",
            },
            {
                "role": "user",
                "content": "Query our curated RAG for Ghidra Headless and Radare2 JSON commands in domain cybersec_audit with top_k=2 and max_tokens=900.",
            },
        ],
    }
    resp, elapsed_ms = post_json(f"{base_url.rstrip('/')}/chat/completions", payload, api_key)
    choice = (resp.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    tcalls = msg.get("tool_calls") or []
    schema_ok = False
    cli_ok = False
    parsed_args = {}
    cli_returned = 0

    if tcalls:
        fn = tcalls[0].get("function") or {}
        if fn.get("name") == "query_arsenal":
            try:
                parsed_args = json.loads(fn.get("arguments") or "{}")
                flt = parsed_args.get("filters") or {}
                if (
                    isinstance(parsed_args.get("query"), str)
                    and flt.get("domain") == "cybersec_audit"
                    and isinstance(flt.get("top_k"), int)
                    and isinstance(flt.get("max_tokens"), int)
                ):
                    schema_ok = True
                    cmd = [
                        sys.executable,
                        "-m",
                        "llm_sec_studio.tools.query_arsenal",
                        "--query",
                        parsed_args["query"],
                        "--domain",
                        flt["domain"],
                        "--top-k",
                        str(flt["top_k"]),
                        "--max-tokens",
                        str(flt["max_tokens"]),
                        "--json",
                    ]
                    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
                    proc = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=20, check=False)
                    if proc.returncode == 0:
                        res_json = json.loads(proc.stdout)
                        cli_returned = int(res_json.get("returned", 0))
                        cli_ok = cli_returned > 0 and int(res_json.get("total_tokens_est", 9999)) <= 1500
            except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError):
                schema_ok = False

    return {
        "pass": bool(schema_ok and cli_ok),
        "latency_ms": round(elapsed_ms, 1),
        "finish_reason": choice.get("finish_reason"),
        "nested_schema_valid": schema_ok,
        "query_arsenal_roundtrip_ok": cli_ok,
        "query_arsenal_hits": cli_returned,
        "parsed_args": parsed_args,
    }


def bench_security_patch(base_url: str, model: str, api_key: str) -> dict:
    vulnerable_snippet = (
        "function getUserByEmail(db, email) {\n"
        '  const sql = "SELECT id, role FROM users WHERE email = \'" + email + "\'";\n'
        "  return db.prepare(sql).get();\n"
        "}\n"
    )
    payload = {
        "model": model,
        "temperature": 0.2,
        "top_p": 0.80,
        "top_k": 20,
        "min_p": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 900,
        "messages": [
            {
                "role": "system",
                "content": "You are a defensive AppSec engineer. Return ONLY the fixed JavaScript function using parameterized queries.",
            },
            {
                "role": "user",
                "content": f"Patch the SQL injection vulnerability in this Node SQLite function:\n```js\n{vulnerable_snippet}```",
            },
        ],
    }
    resp, elapsed_ms = post_json(f"{base_url.rstrip('/')}/chat/completions", payload, api_key)
    choice = (resp.get("choices") or [{}])[0]
    content = str((choice.get("message") or {}).get("content") or "")
    has_placeholder = ("WHERE email = ?" in content) or ("WHERE email = @" in content) or ("WHERE email = :" in content)
    passes_param = bool(re.search(r"\.get\s*\(\s*.*email", content))
    no_concat = ("'\" + email" not in content) and ("+ email +" not in content)
    patched_ok = bool(has_placeholder and passes_param and no_concat)

    return {
        "pass": patched_ok,
        "latency_ms": round(elapsed_ms, 1),
        "has_placeholder": has_placeholder,
        "passes_param": passes_param,
        "no_string_concat": no_concat,
        "preview": content.strip()[:260],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Real E2E micro-benchmark for Qwen3.8 llama-server.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model", default="huihui-qwen3.8-27b-abliterated")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("ERROR: API key not found in env, ~/.cline/data/secrets.json, or .env", file=sys.stderr)
        return 1

    # Health check first
    health_url = args.base_url.rstrip("/").replace("/v1", "") + "/health"
    with urllib.request.urlopen(health_url, timeout=5) as hr:
        health_status = hr.status
        health_body = json.loads(hr.read().decode("utf-8"))

    stream_res = bench_streaming(args.base_url, args.model, api_key)
    tool_res = bench_nested_tool_calling(args.base_url, args.model, api_key)
    patch_res = bench_security_patch(args.base_url, args.model, api_key)

    overall_pass = bool(health_status == 200 and stream_res["pass"] and tool_res["pass"] and patch_res["pass"])
    report = {
        "overall_pass": overall_pass,
        "base_url": args.base_url,
        "model": args.model,
        "health": {"http_status": health_status, "body": health_body},
        "streaming": stream_res,
        "nested_tool_calling": tool_res,
        "security_patch": patch_res,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"OVERALL_PASS={overall_pass}")
        print(f"STREAMING: ttft={stream_res['ttft_ms']}ms gen={stream_res['gen_tok_s']}tok/s prompt={stream_res['prompt_tok_s']}tok/s think/ans={stream_res['think_to_answer_ratio']}")
        print(f"TOOL_CALL: pass={tool_res['pass']} latency={tool_res['latency_ms']}ms hits={tool_res['query_arsenal_hits']}")
        print(f"SEC_PATCH: pass={patch_res['pass']} latency={patch_res['latency_ms']}ms")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
