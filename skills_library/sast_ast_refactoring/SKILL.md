---
name: sast_ast_refactoring
description: Deterministic static analysis and structural code refactoring using ast-grep, oxlint, ruff, ty, and rtk for fast surgical edits with zero regressions.
domain: agent_harness
provenance: curated from ast-grep official docs and zebbern/deep-module-refactor (MIT)
---
# SAST & Structural AST Refactoring

## When to Use
Use when refactoring repeated code patterns, migrating deprecated APIs, or enforcing static security/style invariants across JS/TS and Python codebases.

## 1. Choose the Right Deterministic Tool
- **Structural search/rewrite:** `ast-grep --pattern '<pattern>' --lang <ts|js|py> <path>` (matches AST syntax, ignores whitespace/formatting noise).
- **Rule-based SAST scan:** `ast-grep scan --rule config/ast_rules/security_baseline.yml <path>`.
- **JS/TS fast lint:** `rtk npx oxlint --quiet <files>` (Rust Oxc, `< 200ms`).
- **Python lint & types:** `ruff check <files>` + `ty check <files>` (Astral Rust toolchain).
- **Secret scanning:** `gitleaks detect --no-git --source <path>` or `python tools/run_gates.py`.

## 2. Safe Surgical Refactoring Protocol
1. Capture baseline test/lint status before editing.
2. Preview matches first (`ast-grep --pattern ...` without `--update-all`) to confirm zero unintended edits.
3. Apply minimal contiguous edits; avoid drive-by reformatting of unrelated lines.
4. Run `python tools/run_gates.py` + unit tests immediately after editing; never declare done without observing exit code `0`.

## 3. Anti-Bloat Discipline
- Reuse existing project primitives and stdlib before adding external packages.
- Delete dead code/imports and keep functions cohesive (`<= 50` lines when practical).
