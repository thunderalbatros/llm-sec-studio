#!/usr/bin/env python3
"""
llm_sec_studio.tools.run_gates — Fast (<2s) pre-execution security and quality gate pipeline for llm-sec-studio.
Chains: ruff, ty, ast-grep, gitleaks, and repo hygiene check (zero WSF JS coupling).
"""
import argparse
import concurrent.futures
import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PY_TOOLS = [
    "src/llm_sec_studio",
]
DEFAULT_PY_TARGETS = [
    "src",
    "tests",
    "sec-agent-squad/guardrails/scope_enforcer.py",
    "sec-agent-squad/core/sandbox_executor.py",
    "sec-agent-squad/tests",
]


def resolve_bin(name: str, extra_globs: list[Path] | None = None) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    home = Path.home()
    candidates = [
        home / ".local" / "bin" / f"{name}.exe",
        home / ".local" / "bin" / name,
        home / "AppData" / "Roaming" / "npm" / f"{name}.cmd",
        home / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / f"{name}.exe",
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    if extra_globs:
        for base in extra_globs:
            if base.is_dir():
                for hit in base.rglob(f"{name}.exe"):
                    return str(hit)
    return None


def run_cmd(name: str, cmd: list[str], timeout: int = 30) -> dict:
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        ms = round((time.perf_counter() - t0) * 1000.0, 1)
        out = (proc.stdout + "\n" + proc.stderr).strip()
        return {
            "gate": name,
            "pass": proc.returncode == 0,
            "returncode": proc.returncode,
            "ms": ms,
            "detail": out[:400],
        }
    except (OSError, subprocess.SubprocessError) as err:
        ms = round((time.perf_counter() - t0) * 1000.0, 1)
        return {
            "gate": name,
            "pass": False,
            "returncode": 127,
            "ms": ms,
            "detail": str(err)[:300],
        }


def fast_hygiene_check() -> dict:
    t0 = time.perf_counter()
    pyproject = ROOT / "pyproject.toml"
    gitignore = ROOT / ".gitignore"
    gi_txt = gitignore.read_text(encoding="utf-8", errors="ignore") if gitignore.is_file() else ""
    env_ignored = ".env" in gi_txt and ".env.*" in gi_txt
    passed = bool(pyproject.is_file() and env_ignored)
    ms = round((time.perf_counter() - t0) * 1000.0, 1)
    return {
        "gate": "hygiene_fast",
        "pass": passed,
        "returncode": 0 if passed else 1,
        "ms": ms,
        "detail": f"pyproject={pyproject.is_file()} env_ignored={env_ignored}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run unified fast local security & quality gates for llm-sec-studio.")
    parser.add_argument("--full", action="store_true", help="Scan directories recursively with gitleaks dir")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON summary")
    args = parser.parse_args()

    t_start = time.perf_counter()
    winget_pkgs = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
    ruff_bin = resolve_bin("ruff") or "ruff"
    ty_bin = resolve_bin("ty") or "ty"
    sg_bin = resolve_bin("ast-grep") or "ast-grep"
    gitleaks_bin = resolve_bin("gitleaks", [winget_pkgs]) or "gitleaks"

    py_tool_targets = [p for p in DEFAULT_PY_TOOLS if (ROOT / p).exists()]
    py_targets = [p for p in DEFAULT_PY_TARGETS if (ROOT / p).exists()]

    gitleaks_cfg = ["--config", "config/gitleaks.toml"] if (ROOT / "config" / "gitleaks.toml").is_file() else []
    gitleaks_scopes = ["config", "skills_library", "tests", "infra", "src", "sec-agent-squad/config", "sec-agent-squad/guardrails", "sec-agent-squad/core"]
    if args.full:
        gitleaks_scopes = ["src", "config", "skills_library", "tests", "infra", "sec-agent-squad"]

    def run_gitleaks_gate() -> dict:
        t0 = time.perf_counter()
        if not args.full:
            files: list[Path] = []
            for scope in gitleaks_scopes:
                p = ROOT / scope
                if p.is_file():
                    files.append(p)
                elif p.is_dir():
                    files.extend(
                        f
                        for f in sorted(p.rglob("*"))
                        if f.is_file()
                        and "__pycache__" not in f.parts
                        and ".pytest_cache" not in f.parts
                        and f.suffix.lower() not in {".pyc", ".sqlite", ".db"}
                        and f.stat().st_size <= 512_000
                    )
            chunks: list[str] = []
            for f in files:
                rel = f.relative_to(ROOT).as_posix()
                chunks.append(f"\n# --- {rel} ---\n" + f.read_text(encoding="utf-8", errors="ignore"))
            payload = "\n".join(chunks)
            try:
                proc = subprocess.run(
                    [gitleaks_bin, "stdin", *gitleaks_cfg, "--no-banner", "--redact"],
                    cwd=str(ROOT),
                    input=payload,
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
                ms = round((time.perf_counter() - t0) * 1000.0, 1)
                out = (proc.stdout + "\n" + proc.stderr).strip()
                return {
                    "gate": "gitleaks",
                    "pass": proc.returncode == 0,
                    "returncode": proc.returncode,
                    "ms": ms,
                    "detail": f"clean ({len(files)} files)" if proc.returncode == 0 else out[:240],
                }
            except (OSError, subprocess.SubprocessError) as err:
                ms = round((time.perf_counter() - t0) * 1000.0, 1)
                return {"gate": "gitleaks", "pass": False, "returncode": 127, "ms": ms, "detail": str(err)[:240]}

        details: list[str] = []
        failed_rc = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(gitleaks_scopes))) as gex:
            gfuts = {
                gex.submit(
                    run_cmd,
                    f"gitleaks:{scope}",
                    [
                        gitleaks_bin,
                        "dir",
                        scope,
                        *gitleaks_cfg,
                        "--no-banner",
                        "--redact",
                        "--max-target-megabytes",
                        "2",
                    ],
                    30,
                ): scope
                for scope in gitleaks_scopes
                if (ROOT / scope).exists()
            }
            for gf in concurrent.futures.as_completed(gfuts):
                res = gf.result()
                if not res["pass"]:
                    failed_rc = res["returncode"] or 1
                    details.append(f"{gfuts[gf]}: {res['detail'][:120]}")
        ms = round((time.perf_counter() - t0) * 1000.0, 1)
        return {
            "gate": "gitleaks",
            "pass": failed_rc == 0,
            "returncode": failed_rc,
            "ms": ms,
            "detail": "; ".join(details) if details else f"clean ({len(gitleaks_scopes)} dirs)",
        }

    jobs: list[tuple[str, list[str], int]] = [
        ("ruff", [ruff_bin, "check", *py_targets], 20),
        ("ty", [ty_bin, "check", "--extra-search-path", "src", *py_tool_targets], 20),
        ("ast_grep", [sg_bin, "scan", "--rule", "config/ast_rules/security_baseline.yml", *py_targets], 20),
    ]

    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs) + 1) as ex:
        futs = [ex.submit(run_cmd, name, cmd, timeout) for name, cmd, timeout in jobs]
        futs.append(ex.submit(run_gitleaks_gate))
        results.append(fast_hygiene_check())
        for f in concurrent.futures.as_completed(futs):
            results.append(f.result())

    results.sort(key=lambda x: x["gate"])
    total_ms = round((time.perf_counter() - t_start) * 1000.0, 1)
    overall = all(r["pass"] for r in results)

    summary = {
        "overall_pass": overall,
        "total_ms": total_ms,
        "mode": "full" if args.full else "fast",
        "gates": results,
    }

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"=== RUN_GATES ({summary['mode'].upper()}) | PASS={overall} | {total_ms}ms ===")
        for r in results:
            tag = "PASS" if r["pass"] else "FAIL"
            print(f"  [{tag}] {r['gate']:<20} {r['ms']:>7.1f}ms | {r['detail'][:110]}")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
