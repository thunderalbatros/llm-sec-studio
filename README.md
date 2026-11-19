# llm-sec-studio

Standalone Zero-Trust GCP LLM Runtime (`Qwen 3.8 27B` at `131K` context on NVIDIA L4), Anti-Prompt-Injection Guardrails, Curated `SKILL.md` Library, and Isolated Agent Sandbox Workspace.

Separated cleanly from `C:\Users\tomas\Desktop\web-software-factory` (`Academia IA`) with `0 MB` duplicate RAG storage (reads `.cache/rag_*.sqlite` strictly `?mode=ro`).

## Daily GCP Lifecycle (compatible via `~/scripts-gcp-llm/`)
- Start VM + IAP tunnel (`127.0.0.1:8000/v1`): `~\scripts-gcp-llm\iniciar_llm.ps1`
- Inspect status & FinOps estimate: `~\scripts-gcp-llm\estado_llm.ps1`
- Optional Headroom CCR Proxy (`127.0.0.1:8787/v1`): `~\scripts-gcp-llm\iniciar_headroom.ps1 -Background`
- Stop tunnel + proxy + VM (`$0.00/h` compute): `~\scripts-gcp-llm\detener_llm.ps1`

## Core Studio CLIs (from `llm-sec-studio` root)
- Fast quality & security gates (`< 2s`): `python -m llm_sec_studio.tools.run_gates` (with `PYTHONPATH=src` or `uv run`)
- Curated RAG + Skills router (`< 1,500` tok): `python -m llm_sec_studio.tools.query_arsenal --query "<q>" --domain <domain> --json`
- Symbol slicer (`0` MCP tokens): `python -m llm_sec_studio.tools.code_slice --outline <file>` or `toktoken search:symbols <q> -p src -c -l 10`
- Anti-Prompt-Injection Spotlighting: `python -m llm_sec_studio.guardrails.input_sanitizer --source "<origin>" --json`
- Offline evals: `uv run --with pytest pytest tests/evals/ -m "not live" -v`
- Live evals (VM running): `uv run --with pytest pytest tests/evals/test_llm_live_evals.py -m live -v`
