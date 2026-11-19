#!/usr/bin/env python3
"""
llm_sec_studio.tools.code_slice — Zero-MCP-overhead symbol-level code navigator for Cline & local agents.
Extracts compact outlines, exact symbol bodies (Python AST / JS-TS regex), and bounded ast-grep refs.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
from pathlib import Path

JS_SYM_RE = re.compile(
    r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function|class)\s+([A-Za-z_$][\w$]*)"
    r"|^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\("
)


def _py_outline(src: str) -> list[dict]:
    tree = ast.parse(src)
    items: list[dict] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = ast.unparse(node.args)
            ret = f" -> {ast.unparse(node.returns)}" if node.returns else ""
            items.append({"kind": "func", "name": node.name, "sig": f"def {node.name}({args}){ret}", "start": node.lineno, "end": node.end_lineno})
        elif isinstance(node, ast.ClassDef):
            methods = [
                {"name": m.name, "start": m.lineno, "end": m.end_lineno}
                for m in node.body
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            items.append({"kind": "class", "name": node.name, "start": node.lineno, "end": node.end_lineno, "methods": methods})
    return items


def _generic_outline(lines: list[str]) -> list[dict]:
    items: list[dict] = []
    for idx, ln in enumerate(lines, 1):
        m = JS_SYM_RE.match(ln)
        if m:
            name = m.group(1) or m.group(2)
            items.append({"kind": "symbol", "name": name, "sig": ln.strip()[:100], "start": idx, "end": idx})
    return items


def get_outline(path: Path) -> list[dict]:
    src = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".py":
        return _py_outline(src)
    return _generic_outline(src.splitlines())


def extract_symbol(path: Path, symbol: str) -> dict:
    src = path.read_text(encoding="utf-8", errors="replace")
    lines = src.splitlines()
    if path.suffix.lower() == ".py":
        tree = ast.parse(src)
        parts = symbol.split(".")
        target: ast.AST | None = None
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == parts[0]:
                target = node
                break
            if isinstance(node, ast.ClassDef) and node.name == parts[0]:
                if len(parts) == 1:
                    target = node
                    break
                for m in node.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.name == parts[1]:
                        target = m
                        break
        if target is None or not hasattr(target, "lineno") or not hasattr(target, "end_lineno"):
            raise KeyError(f"Symbol {symbol!r} not found in {path}")
        start, end = int(target.lineno), int(target.end_lineno or target.lineno)
        numbered = [f"{i}: {lines[i - 1]}" for i in range(start, end + 1)]
        return {"file": str(path), "symbol": symbol, "start": start, "end": end, "code": "\n".join(numbered)}

    for idx, ln in enumerate(lines, 1):
        m = JS_SYM_RE.match(ln)
        if m and (m.group(1) == symbol or m.group(2) == symbol):
            end = min(len(lines), idx + 60)
            numbered = [f"{i}: {lines[i - 1]}" for i in range(idx, end + 1)]
            return {"file": str(path), "symbol": symbol, "start": idx, "end": end, "code": "\n".join(numbered)}
    raise KeyError(f"Symbol {symbol!r} not found in {path}")


def find_refs(symbol: str, directory: Path, limit: int = 30) -> list[str]:
    sg = shutil.which("ast-grep") or str(Path.home() / "AppData" / "Roaming" / "npm" / "ast-grep.cmd")
    proc = subprocess.run([sg, "run", "-p", symbol, str(directory)], capture_output=True, text=True, timeout=15, check=False)
    hits = [ln for ln in proc.stdout.splitlines() if ln.strip()][:limit]
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Surgical symbol-level code slicer (0 MCP token overhead).")
    ap.add_argument("--outline", type=Path, help="Print compact symbol outline with line ranges")
    ap.add_argument("--symbol", nargs=2, metavar=("FILE", "SYMBOL"), help="Extract exact symbol (e.g. File.py Class.method)")
    ap.add_argument("--refs", nargs="+", metavar="ARG", help="Find bounded ast-grep references: --refs <Symbol> [dir]")
    ap.add_argument("--json", action="store_true", help="Emit JSON output")
    args = ap.parse_args()

    if args.outline:
        data = get_outline(args.outline)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            for it in data:
                if it["kind"] == "class":
                    meths = ", ".join(f"{m['name']}(L{m['start']}-{m['end']})" for m in it["methods"])
                    print(f"class {it['name']} [L{it['start']}-{it['end']}]: {meths}")
                else:
                    print(f"{it['sig']} [L{it['start']}-{it['end']}]")
        return 0

    if args.symbol:
        res = extract_symbol(Path(args.symbol[0]), args.symbol[1])
        print(json.dumps(res, indent=2) if args.json else f"# {res['file']}::{res['symbol']} (L{res['start']}-L{res['end']})\n{res['code']}")
        return 0

    if args.refs:
        sym = args.refs[0]
        target_dir = Path(args.refs[1]) if len(args.refs) > 1 else Path(".")
        hits = find_refs(sym, target_dir)
        print(json.dumps({"symbol": sym, "hits": hits}, indent=2) if args.json else "\n".join(hits))
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
