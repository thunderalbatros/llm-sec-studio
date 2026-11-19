---
name: modern_web_leaks_audit
description: Detect modern web information leaks — source maps, SSR state, exposed GraphQL/OpenAPI schemas, CORS/CSP misconfig, RLS/buckets, and CMS fingerprinting — in authorized scopes.
domain: cybersec_audit
provenance: curated from WSTG v4.2, OWASP API Top 10, and delta_docs_2026 (httpx, katana, nuclei)
---
# Modern Web Leaks Audit (Authorized Scope)

## When to Use
Use when auditing a live web app or API in an authorized scope to find information-disclosure leaks that classic SAST misses.

## 1. Source Maps (`.js.map`)
- Enumerate `*.js.map` with `httpx -json` / `katana -json`.
- If any `.js.map` is served, the full original source (variable names, inline secrets, file paths) is exposed. Flag `HIGH`.

## 2. SSR State Leaks
- Extract `<script id="__NEXT_DATA__">` (Next.js) or `window.__NUXT__` (Nuxt) from the HTML.
- Reveals props, GraphQL queries, auth tokens, and user objects. Flag if it contains `token`, `password`, or `email`.

## 3. Exposed Schemas (GraphQL / OpenAPI)
- Probe `/graphql` (introspection query), `/openapi.json`, `/swagger.json`, `/api/schema`.
- If introspection returns `__schema`, the full API surface is exposed. Flag `MEDIUM`.

## 4. CORS / CSP Misconfiguration
- **CORS:** `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true` = `HIGH` (any origin can read authenticated responses).
- **CSP:** Missing or weak CSP (no `script-src`, no `frame-ancestors`) = `MEDIUM` (enables XSS and clickjacking).

## 5. RLS / Bucket Misconfiguration
- **Supabase/Cloudflare RLS:** Check if Row Level Security policies exist on every table. If `auth.uid() = user_id` is missing, any user can read/write all rows. Flag `CRITICAL`.
- **Buckets:** A public-read bucket that should be private, or a bucket allowing anonymous writes, is `HIGH`.

## 6. CMS Fingerprinting
- Use `httpx -json` + `nuclei` to detect the CMS (WordPress, Drupal, Joomla, Next.js) via headers (`X-Powered-By`), canonical paths (`/wp-login.php`, `/drupal/`), and generator meta.
- Fingerprinting reveals known CVEs. Flag the CMS version and check against recent CVEs.

## 7. Evidence-Based Reporting
Each finding: `file:line` or `URL`, `leak type`, `impact`, `minimal safe patch`.
