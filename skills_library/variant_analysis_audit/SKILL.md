---
name: variant_analysis_audit
description: Trail of Bits style Variant Analysis: generalize one confirmed bug or security flaw into custom ast-grep or semgrep rules to hunt all sibling variants across a codebase.
domain: cybersec_audit
provenance: curated from trailofbits/variant-analysis and trailofbits/semgrep-rule-creator (CC-BY-SA-4.0)
---
# Variant Analysis Audit (ast-grep & Semgrep)

## When to Use
Trigger immediately AFTER confirming a vulnerability, logic bug, or insecure pattern in one file ("are there others like this?"). Not for blind initial discovery.

## 1. Abstract the Root Cause
Before writing any rule, separate:
- **Specific manifestation:** exact variable names/file where bug #1 occurred.
- **Structural invariant:** the root anti-pattern (missing auth check, TOCTOU check-then-act outside transaction, unvalidated redirect/SSRF sink, unsafe deserialization, raw SQL concat).
- **False-positive guards:** what distinguishes safe call sites (e.g., constant literals, validated allowlist, atomic SQL transaction).

## 2. Author Targeted Rule (`ast-grep` First, `semgrep` for Taint)
- Use `ast-grep` (`ast-grep scan --rule <rule.yml>`) for fast structural syntax matching (`< 1s` locally):
  - Example patterns: `db.prepare($SQL + $VAR)`, `fetch($URL)` without allowlist, `fs.existsSync($P)` followed by `fs.writeFileSync($P, ...)` (TOCTOU).
- Use `semgrep` (`mode: taint`) when tracking untrusted sources (`req.query`, `req.body`, external HTML) across assignments into dangerous sinks (`eval`, `exec`, `innerHTML`, SQL, outbound `fetch`).

## 3. High-Risk Variant Families to Check
- **Race Conditions / TOCTOU:** balance/quota check outside atomic `BEGIN IMMEDIATE` / `UPDATE ... WHERE balance >= ?`.
- **SSRF & Open Redirect:** user-controlled URLs reaching `fetch`/`urllib`/`axios` without DNS/IP blocklist (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.169.254`, IPv6 `::1`/`fc00::/7`).
- **Deserialization & Prototype Pollution:** `JSON.parse` merged recursively into objects (`__proto__`/`constructor`), `yaml.load` without `SafeLoader`, `pickle.loads`.

## 4. Triage & Lock In Regression Prevention
- Inspect every match; classify `TRUE_POSITIVE` / `FALSE_POSITIVE` with file:line evidence.
- Patch all confirmed variants together and commit the rule to `config/ast_rules/` so `tools/run_gates.py` prevents re-introduction permanently.
