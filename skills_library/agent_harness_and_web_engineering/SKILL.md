---
name: agent_harness_and_web_engineering
description: Progressive-disclosure agent harness patterns (query_arsenal.py, rtk, Jina Reader) combined with clean Astro/Cloudflare Edge web engineering (tools/factory.mjs).
domain: web_engineering
provenance: curated from sickn33/antigravity-awesome-skills (MIT), VoltAgent/awesome-agent-skills (MIT), and WSF Studio
---
# Agent Harness & Clean Web Engineering

## When to Use
Use when orchestrating multi-step coding tasks under a 131K context window or scaffolding/optimizing websites in Web Software Factory.

## 1. Context Budget & Progressive Disclosure
- Never preload full docs or heavy MCP schemas (> 1,000 fixed tokens/turn).
- Discover knowledge on demand:
  1. Inspect `@config/arsenal_registry.json` (`< 800` tokens).
  2. Query `uv run query-arsenal --query "<topic>" --domain <domain> --json` (`<= 1,500` tokens).
  3. Load ONLY the single relevant `skills_library/<skill>/SKILL.md` (`< 600` tokens).
- Prefix noisy shell commands with `rtk` (`rtk git status`, `rtk npm run build`) and web fetches with `https://r.jina.ai/` (max 2 URLs/turn).

## 2. Clean Web Engineering (WSF Pipeline)
- Scaffold & audit via `node tools/factory.mjs [status|styles|new|spec|build|gate|visual-gate]`.
- Enforce zero-bloat CSS (`LightningCSS`, OKLCH tokens, APCA contrast, `@starting-style`, compositor-only animations) and hardened Cloudflare `_headers` (`CSP`, `HSTS`, `CORP`).
- Keep reads surgical (`StartLine`/`EndLine <= 160` lines) and validate every change with `uv run run-gates`.
