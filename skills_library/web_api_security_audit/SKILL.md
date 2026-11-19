---
name: web_api_security_audit
description: Authorized source and endpoint security review aligned with OWASP API Security Top 10 and WSTG v4.2, focusing on authz, input validation, rate limits, and safe remediation.
domain: cybersec_audit
provenance: curated from zebbern/code-vuln-audit (MIT) and OWASP API Top 10 / WSTG v4.2
---
# Web & API Security Audit (Authorized Scope)

## When to Use
Use when auditing web apps, REST/GraphQL APIs, or Cloudflare Workers in local sandboxes or explicitly authorized repositories/scopes.

## 1. Pre-Flight Scope & Inventory
- Confirm authorization scope before inspecting any live endpoint; prefer source-code + local test harness review first.
- Enumerate all routes, HTTP methods, auth middleware, request schemas, and outbound HTTP calls.

## 2. OWASP API Top 10 / WSTG Source Checks
- **API1/API5 (BOLA/BFLA):** Every resource fetch/mutation verifies `owner_id == session.user_id` or explicit RBAC permission at the query layer.
- **API2 (Broken Auth):** No default/hardcoded secrets, timing-safe token comparison, brute-force throttling, strict JWT issuer/audience/algorithm checks.
- **API3 (Mass Assignment / Excessive Data):** Whitelist response DTO fields explicitly; reject unexpected body properties (`additionalProperties: false`).
- **API4 (Resource Consumption):** Enforce request body byte limits, pagination caps (`limit <= 100`), query timeouts, and per-IP/user rate limits.
- **API7 (SSRF):** Restrict outbound URLs to allowlisted hosts/schemes (`https:`); block loopback, link-local (`169.254.169.254`), and private ranges.
- **Injection & XSS:** Parameterized SQL only, strict template auto-escaping, safe DOM APIs (`textContent` over `innerHTML`), and strict CSP.

## 3. Evidence-Based Reporting
Report each confirmed finding with: `file:line`, `OWASP ID`, `impact`, `minimal safe patch`, and a unit test verifying the fix.
