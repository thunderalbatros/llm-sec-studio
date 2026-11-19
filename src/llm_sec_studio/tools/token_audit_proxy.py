#!/usr/bin/env python3
"""
llm_sec_studio.tools.token_audit_proxy — Opt-in local OpenAI telemetry & reversible CCR proxy (127.0.0.1:8001 -> :8000).
Preserves static system prefixes byte-identically for llama-server prefix cache hits,
logs per-turn token usage/cache hits to .cache/token_telemetry.jsonl, and compacts only huge repetitive logs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE_DIR = ROOT / ".cache"
TELEMETRY_LOG = CACHE_DIR / "token_telemetry.jsonl"
CCR_DB = CACHE_DIR / "ccr_blobs.sqlite"


def _init_ccr_db() -> sqlite3.Connection:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(CCR_DB))
    conn.execute("CREATE TABLE IF NOT EXISTS blobs (id TEXT PRIMARY KEY, created_at REAL, content TEXT)")
    conn.commit()
    return conn


def compact_oversized_tool_text(text: str, threshold: int = 8000) -> str:
    """Reversibly compress huge repetitive terminal/tool outputs (CCR) without touching short/code/JSON text."""
    if len(text) <= threshold:
        return text
    stripped = text.lstrip()
    if stripped.startswith(("{", "[", "def ", "class ", "import ", "from ", "function ", "export ")):
        return text
    blob_id = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:12]
    conn = _init_ccr_db()
    try:
        conn.execute("INSERT OR REPLACE INTO blobs VALUES (?, ?, ?)", (blob_id, time.time(), text))
        conn.commit()
    finally:
        conn.close()
    lines = text.splitlines()
    head = "\n".join(lines[:40])
    tail = "\n".join(lines[-30:]) if len(lines) > 70 else ""
    omitted = max(0, len(lines) - 70)
    return f"{head}\n... [CCR_COMPACTED {omitted} lines | full blob id={blob_id} in .cache/ccr_blobs.sqlite] ...\n{tail}"


def _log_telemetry(record: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with TELEMETRY_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def make_handler(upstream: str, compact_threshold: int):
    class ProxyHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args) -> None:
            return

        def _forward(self, method: str) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length) if length > 0 else None
            t0 = time.perf_counter()
            if raw_body and self.path.startswith("/v1/chat/completions"):
                try:
                    payload = json.loads(raw_body.decode("utf-8"))
                    msgs = payload.get("messages")
                    if isinstance(msgs, list) and len(msgs) > 2:
                        # Never touch system prompt (index 0) or the latest user turn; only compact old huge tool messages
                        for m in msgs[1:-1]:
                            if m.get("role") == "tool" and isinstance(m.get("content"), str):
                                m["content"] = compact_oversized_tool_text(m["content"], compact_threshold)
                    raw_body = json.dumps(payload).encode("utf-8")
                except (ValueError, KeyError):
                    pass

            headers = {k: v for k, v in self.headers.items() if k.lower() not in {"host", "content-length"}}
            req = urllib.request.Request(f"{upstream.rstrip('/')}{self.path}", data=raw_body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    self.send_response(resp.status)
                    for k, v in resp.getheaders():
                        if k.lower() not in {"transfer-encoding", "connection"}:
                            self.send_header(k, v)
                    self.end_headers()
                    usage_last: dict = {}
                    while True:
                        chunk = resp.read(4096)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        self.wfile.flush()
                        if b'"usage"' in chunk:
                            for ln in chunk.decode("utf-8", errors="ignore").splitlines():
                                if ln.startswith("data:") and '"usage"' in ln:
                                    try:
                                        usage_last = json.loads(ln[5:]).get("usage") or usage_last
                                    except ValueError:
                                        pass
                    if self.path.startswith("/v1/chat/completions"):
                        _log_telemetry({"ts": round(time.time(), 1), "ms": round((time.perf_counter() - t0) * 1000, 1), "usage": usage_last})
            except urllib.error.HTTPError as err:
                self.send_response(err.code)
                self.end_headers()
                self.wfile.write(err.read())

        def do_GET(self) -> None:
            self._forward("GET")

        def do_POST(self) -> None:
            self._forward("POST")

    return ProxyHandler


def main() -> int:
    ap = argparse.ArgumentParser(description="Opt-in local OpenAI telemetry & CCR proxy.")
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--upstream", default="http://127.0.0.1:8000")
    ap.add_argument("--compact-threshold", type=int, default=8000)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(args.upstream, args.compact_threshold))
    print(f"token_audit_proxy listening on http://127.0.0.1:{args.port}/v1 -> {args.upstream}")
    srv.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
