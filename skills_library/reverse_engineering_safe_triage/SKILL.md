---
name: reverse_engineering_safe_triage
description: Safe read-only binary and artifact triage using REA MCP (compact), Ghidra Headless metadata, and Radare2 JSON commands for defensive forensics, SBOM verification, and protocol analysis.
domain: cybersec_audit
provenance: curated from morluto/rea, Ghidra Headless docs, and Radare2 JSON reference
---
# Safe Read-Only Binary & Artifact Triage

## When to Use
Use strictly for defensive malware/artifact triage, SBOM & binary dependency inspection, crash root-cause analysis, or documenting proprietary protocols in isolated local sandboxes. Never generate weaponized payloads or exploit chains.

## 1. Isolation First
- Inspect untrusted binaries ONLY inside isolated sandboxes (`--runtime=runsc --network=none --read-only`) — never execute untrusted binaries directly on the host laptop.
- Hash artifacts first (`sha256sum`) and record provenance metadata.

## 2. Structured JSON Triage (Token-Efficient)
- **Radare2 (JSON mode, non-interactive):**
  - `r2 -q -c 'ij' <bin>` — binary format, arch, mitigations (`canary`, `nx`, `pic`, `relro`).
  - `r2 -q -c 'iij' <bin>` — imported symbols/APIs (crypto, network, process APIs).
  - `r2 -q -c 'izj' <bin>` — strings in data sections (cap output with `jq '.[0:40]'`).
  - `r2 -q -c 'aaa; aflj' <bin>` — function table summary before selective disassembly.
- **Ghidra Headless (`analyzeHeadless`):**
  - Run `-readOnly -noanalysis` or targeted post-scripts emitting concise JSON summaries (`<= 1,200` tokens) rather than raw full-binary dumps.
- **REA MCP (`compact` profile):**
  - Query targeted functions/xrefs only; pass bulky outputs through `tools/prompt_sanitizer.py --compress` before LLM analysis.

## 3. Defensive Deliverable
Produce a structured triage brief: binary hardening flags, suspicious APIs/URLs/IOCs, root cause of defect/behavior, and YARA/Sigma detection signatures.
