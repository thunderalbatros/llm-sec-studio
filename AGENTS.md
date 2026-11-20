# AGENTS.md — llm-sec-studio

## 1. Rol, Frontera y Reglas Zero-Trust
- Repo standalone para runtime LLM GCP (`Qwen 3.8 27B`, `131K`), guardrails anti-prompt-injection, skills curadas y sandboxes aislados.
- **Frontera:** aislado de `web-software-factory` (prohibido escribir/modificar). El RAG compartido (`.cache/rag_*.sqlite`) se lee solo `?mode=ro` vía `uv run query-arsenal`.
- **Secretos:** prohibido leer, imprimir o exponer `.env`, `.env.*`, `secrets.json`, `.qwen_api_key` o credenciales.
- **PowerShell 5.1 y Plan Mode:** prohibido `&&` (usar `;`), `2>nul` y cualquier redirección `>` en Plan Mode (usar `-ErrorAction SilentlyContinue`). Usar siempre `icm.exe` (con `.exe`). Si un comando o MCP falla 2 veces igual, detenerse e informar.

## 2. Topología VM GCP y Sandboxes gVisor
- **Fuente de verdad VM:** `~\scripts-gcp-llm\vm_state.json` (proyecto, instancia `llm-qwen-abliterated`, zona activa). No hardcodear zona ni apagar/reiniciar/recrear sin orden.
- **Scripts:** `~\scripts-gcp-llm\{abrir,cerrar}_sesion.ps1` (flujo 2 comandos) sobre `{iniciar,estado,detener}_llm.ps1` e `iniciar_headroom.ps1` (`--lossless` `:8787/v1` → IAP `:8000/v1`).
- **Sandboxes gVisor (`runsc`):** `/usr/local/bin/run-sec-sandbox-{code,net}` vía SSH IAP; alcance estricto en `sec-agent-squad/config/authorized_scope.json`.

## 3. Comandos Nativos Verificados
- `uv run run-gates` (gates `< 2s`; `--full` gitleaks completo)
- `uv run query-arsenal --query "<q>" --domain <cybersec_audit|agent_harness|web_engineering|browser_automation> --json` (`--list-domains`)
- `uv run code-slice --outline <file>` | `toktoken search:symbols <q> -p src -c -l 10` | `toktoken index:update src`
- `uv run input-sanitizer --source "<origin>" --json`
- `uv run llm-bench` (E2E con VM activa)
- `uv run pytest tests/evals/ -m "not live" -v` (evals offline)
- `icm.exe facts list llm-sec-studio` (memoria sin costo LLM)

## 4. Disciplina de Contexto (`131K`)
- **Progressive disclosure:** `11` skills en `skills_library/<skill>/SKILL.md` (`0` tokens fijos en prompt; cargar solo bajo demanda).
- **MCP:** solo `context-mode` habilitado; mantener MCPs pesados desactivados.
- **Handoff:** actualizar `memory/session_handoff.md` (`< 400` tok) al cerrar subfase o superar `60%` de contexto, antes de `/newtask`.
