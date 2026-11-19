# PLAN_ARQUITECTURA — sec-agent-squad

> Sistema multi-agente en LangGraph para auditoria AppSec, deteccion de fugas web, ingenieria inversa y remediacion sobre infraestructura Zero-Trust en GCP.
> Runtime local: Python 3.11+ + SqliteSaver + SSH IAP persistente hacia sandboxes gVisor (runsc) en VM GCP.

---

## 1. Arbol del Proyecto

sec-agent-squad/
├── config/
│   ├── settings.py               # Endpoint 127.0.0.1:8000/v1, limites de tokens y timeouts
│   └── authorized_scope.json     # Lista blanca estricta de dominios, IPs y rutas locales
├── infra/
│   ├── Dockerfile.net            # Debian/Kali slim: nmap, subfinder, httpx, katana, nuclei, ffuf, dalfox, jwt_tool, arjun, Playwright
│   └── Dockerfile.code           # Sin red: Node 22+, rea-agents (MCP), ghidra headless, jadx, radare2, semgrep, ast-grep, gitleaks, trivy, tree-sitter, cli-anything-hub
├── core/
│   ├── sandbox_executor.py       # Sesion SSH IAP reutilizable + ejecucion en /usr/local/bin/run-sec-sandbox-{net,code} + sync tar sin .env
│   ├── output_compressor.py      # Comprime salidas CLI largas a JSON < 1500 tokens + pasa guardrails/input_sanitizer.py
│   ├── skill_loader.py           # Carga bajo demanda desde skills_library/ (< 600 tokens) y consulta tools/query_arsenal.py
│   └── squad_graph.py            # StateGraph + SqliteSaver + State Handoff Compression (< 800 tokens JSON entre nodos)
├── guardrails/
│   └── scope_enforcer.py         # Bloquea cualquier ejecucion fuera de authorized_scope.json
├── agents/
│   ├── commander_lead.py         # Orquestador, valida alcance, enruta y consolida reporte
│   ├── recon_surface.py          # Superficie web/API, fingerprinting CMS, CORS/CSP, Source Maps (.js.map) y SSR (__NEXT_DATA__)
│   ├── appsec_validation.py      # Validacion controlada de brechas/exposiciones (OWASP Top 10, GraphQL/OpenAPI, BOLA/IDOR, RLS/buckets)
│   ├── reverse_sast.py           # morluto/rea (MCP perfil compacto / --json) + semgrep + ast-grep + variant analysis
│   ├── automation_cli.py         # Generador de PoCs limpias y wrappers CLI bajo estandar HKUDS/CLI-Anything (--json + SKILL.md)
│   └── blueteam_remediation.py   # Evaluador independiente (Gatekeeper), parches seguros, Detection-as-Code y tools/run_gates.py
├── tests/
│   ├── test_scope_and_handoff.py
│   └── test_graph_flow.py
├── main.py                       # CLI principal con aprobacion humana antes de acciones activas o parches
└── requirements.txt

---

## 2. Estado y Compresion en LangGraph (State Handoff Compression)

- Checkpointer: SqliteSaver sobre sec-agent-squad/checkpoints.db (thread_id por mision).
- Cada especialista corre con contexto aislado y devuelve unicamente un artefacto handoff (< 800 tokens JSON):
  {"agent": "...", "verified_findings": [...], "evidence_paths": [...], "next_step": "..."}
- Toda entrada externa (HTML, JS, cabeceras, binarios) pasa obligatoriamente por guardrails/input_sanitizer.py (Spotlighting) antes de entrar al LLM.

---

## 3. Plomeria Hibrida Local (HP 250 G8) <-> VM GCP (gVisor runsc)

1. Ejecucion remota: sandbox_executor.py invoca /usr/local/bin/run-sec-sandbox-net y /usr/local/bin/run-sec-sandbox-code (que ya imponen --runtime=runsc, --read-only, --cap-drop=ALL y /tmp escribible) reutilizando conexion SSH IAP activa.
2. Copia limpia de codigo (Windows -> VM): empaquetado con tar nativo excluyendo .env, .env.*, .git, node_modules y secretos hacia /tmp/workspace dentro del sandbox efimero.
3. Validacion final de calidad: todo parche o cambio debe aprobar python tools/run_gates.py antes de finalizar el grafo.
