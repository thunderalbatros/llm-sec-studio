# llm-sec-studio

Standalone Zero-Trust GCP LLM Runtime (`Qwen 3.8 27B` at `131K` context on NVIDIA L4), Anti-Prompt-Injection Guardrails, Curated `SKILL.md` Library, and Isolated Agent Sandbox Workspace.

Separated cleanly from `C:\Users\tomas\Desktop\web-software-factory` (`Academia IA`) with `0 MB` duplicate RAG storage (reads `.cache/rag_*.sqlite` strictly `?mode=ro`).

## Daily GCP Lifecycle (2-command workflow via `~/scripts-gcp-llm/`)
- Open session (Preflight `$0/h` + VM + IAP `:8000` + Headroom `--lossless` `:8787`): `~\scripts-gcp-llm\abrir_sesion.ps1` *(supports `-OfflineOnly`, `-NoHeadroom`, `-SmokeTest`)*
- Close session (optional live evals + immediate `$0.00/h` stop + full QA + index): `~\scripts-gcp-llm\cerrar_sesion.ps1` *(supports `-RunLiveEvals`, `-Milestone "..."`)*
- Low-level scripts: `iniciar_llm.ps1`, `estado_llm.ps1`, `iniciar_headroom.ps1 -Background`, `detener_llm.ps1`

## Core Studio CLIs (from `llm-sec-studio` root)
- Fast quality & security gates (`< 2s`): `uv run run-gates` (or `--full`)
- Curated RAG + Skills router (`< 1,500` tok): `uv run query-arsenal --query "<q>" --domain <domain> --json`
- Symbol slicer (`0` MCP tokens): `uv run code-slice --outline <file>` or `toktoken search:symbols <q> -p src -c -l 10`
- Anti-Prompt-Injection Spotlighting: `uv run input-sanitizer --source "<origin>" --json`
- Live E2E LLM benchmark: `uv run llm-bench`
- Offline evals: `uv run pytest tests/evals/ -m "not live" -v`
- Live evals (VM running): `uv run pytest tests/evals/test_llm_live_evals.py -m live -v`
