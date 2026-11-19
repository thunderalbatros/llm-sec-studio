---
name: secure_system_architecture
description: Design and audit Zero-Trust architectures, OAuth2.1/OIDC auth, RBAC/ABAC, applied cryptography (AEAD, Argon2id), and OWASP ASVS v5.0 controls before shipping code.
domain: cybersec_audit
provenance: curated from trailofbits/skills, zebbern/authentication-patterns, and OWASP ASVS v5.0
---
# Secure System Architecture (OWASP ASVS v5.0)

## When to Use
Use when designing new APIs/services, implementing auth/sessions/crypto, or hardening trust boundaries.

## 1. Authentication & Sessions
- Prefer Passkeys/WebAuthn or OAuth 2.1 + PKCE (`S256`) + exact `redirect_uri` match.
- Password hashing: `Argon2id` (`m >= 19456`, `t >= 2`, `p = 1`) with CSPRNG salts; block breached/top-10k passwords.
- Cookies: `Secure; HttpOnly; SameSite=Strict` (or `Lax`), `__Host-` prefix, rotate session ID on privilege change.
- JWTs: pin explicit asymmetric algorithm (`ES256`/`EdDSA`), reject `alg=none`, short access TTL (`15-60m`), single-use rotating refresh tokens with reuse revocation.

## 2. Authorization (Zero-Trust)
- Deny-by-default middleware on every route; enforce object-level ownership (`BOLA`/`IDOR`) in the data layer (e.g. Postgres RLS / Zanzibar / parameterized tenant `WHERE user_id = ?`).
- Separate RBAC/ABAC policy checks from handlers; never trust client-supplied role/tenant fields or `X-Forwarded-*` without trusted proxy validation.

## 3. Applied Cryptography & Secrets
- Authenticated encryption only (`AES-256-GCM` or `XChaCha20-Poly1305`) with CSPRNG nonces (`crypto.getRandomValues`); never ECB or unauthenticated CBC.
- Constant-time MAC/token comparison (`crypto.timingSafeEqual`).
- Zero secrets in source/logs/prompts; load from protected `.env` or KMS with rotation metadata.

## 4. Executable ASVS v5.0 Checklist
- [ ] Strict schema validation (`Valibot`/`Zod`) rejecting unknown fields (`additionalProperties: false`).
- [ ] Parameterized queries everywhere; zero string concatenation in SQL/shell.
- [ ] Bounded rate limits, body size caps, and outbound SSRF allowlists (block `169.254.169.254`, RFC1918, `::1`).
- [ ] Run `uv run run-gates` before sign-off.
