---
name: threat_modeling_stride
description: Pre-code threat modeling using STRIDE, Attack Trees, and Trust Boundaries to catch architectural flaws before implementation or major refactors.
domain: cybersec_audit
provenance: curated from trailofbits/audit-context-building and Adam Shostack Threat Modeling
---
# Threat Modeling (STRIDE + Attack Trees)

## When to Use
Run before writing new features, auth flows, webhooks, multi-tenant APIs, or agent tool integrations. Build system understanding first; do not skip straight to line-by-line nitpicks.

## 1. Decompose & Map Trust Boundaries
List in <= 15 lines:
- **Assets:** credentials, PII, tenant data, billing/credits, tool execution capability.
- **Entry Points:** HTTP endpoints, webhooks, CLI args, MCP tools, fetched external HTML/Markdown.
- **Trust Boundaries:** Browser <-> Edge Worker, Local CLI <-> IAP Tunnel <-> VM, Trusted Prompt <-> Untrusted External Data.
- **Assumptions & Guarantees:** what each component assumes its caller checked vs. what it enforces itself.

## 2. STRIDE Matrix (Evaluate Every Boundary Crossing)
- **S (Spoofing):** Can identity/origin/webhook signature be forged? -> Require HMAC-SHA256 + timestamp replay window (`<= 300s`) or asymmetric JWT/OIDC.
- **T (Tampering):** Can payload, params, or prompt context be modified? -> Strict schema validation + integrity checks + `<untrusted_data>` isolation.
- **R (Repudiation):** Are sensitive state changes auditable? -> Structured append-only logs (zero secret values).
- **I (Information Disclosure):** Can errors, stack traces, IDs, or side-channels leak cross-tenant data? -> Generic errors, opaque UUIDs, RLS.
- **D (Denial of Service):** Unbounded loops, large payloads, ReDoS, or LLM token/credit exhaustion? -> Strict timeouts, size caps, rate limits, reasoning/idle watchdogs.
- **E (Elevation of Privilege):** Broken object/function auth, SSRF to metadata (`169.254.169.254`), or shell injection? -> Deny-by-default authz, allowlists, parameterized APIs.

## 3. Compact Attack Tree & Mitigations
For each high-risk asset, write a 3-level AND/OR tree:
`Goal -> [OR] Path A / Path B -> Control verifying mitigation + automated test`.
Record accepted risks vs. blocking fixes before coding starts.
