---
name: detection_and_hardening
description: Active Blue Team Detection-as-Code (Semgrep, YARA, Sigma), strict HTTP security headers (CSP/HSTS), WAF virtual patching, and CIS Docker/gVisor hardening.
domain: cybersec_audit
provenance: curated from mukul975/Anthropic-Cybersecurity-Skills (Apache-2.0) and trailofbits/skills
---
# Detection-as-Code & System Hardening

## When to Use
Use when hardening web apps, edge workers, Docker containers, or writing automated detection rules after an audit or incident.

## 1. Detection-as-Code Patterns
- **Semgrep (SAST):** encode banned sinks + taint rules with `test:` positive/negative fixtures (`# ruleid:` / `# ok:`) to keep false positives near zero.
- **YARA (Artifact/Supply-Chain):** match suspicious obfuscated payloads, unauthorized postinstall droppers, or credential-harvesting strings in static artifacts; require >= 2 independent indicators.
- **Sigma (Runtime Logs):** express log detections vendor-agnostically (`logsource`, `selection`, `filter`, `condition`) for auth brute force, metadata IP probing (`169.254.169.254`), or unexpected outbound shells.

## 2. Web & Edge HTTP Hardening
Enforce via Cloudflare `_headers` or reverse proxy:
- `Content-Security-Policy`: strict nonce/hash `script-src`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`.
- `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Cross-Origin-Resource-Policy: same-origin`.
- Validate `Sec-Fetch-Site` + `Origin` on state-changing routes; apply WAF virtual rules (rate-limit + payload regex) as defense-in-depth while patching root cause.

## 3. CIS Docker & gVisor Hardening
- Bind local-only services strictly to `127.0.0.1:<port>:<port>`, never `0.0.0.0`.
- Run untrusted workloads with `--runtime=runsc` (gVisor), `--read-only`, `--cap-drop=ALL`, `--security-opt=no-new-privileges:true`, `--pids-limit=128`, `--memory`, and `--network=none` when offline.
- Enforce `iptables` `DOCKER-USER` egress drop for `169.254.169.254/32` and private RFC1918 ranges on networked sandboxes.
