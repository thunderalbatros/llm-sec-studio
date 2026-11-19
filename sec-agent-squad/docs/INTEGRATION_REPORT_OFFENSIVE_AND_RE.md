# Reporte: Integracion de Herramientas Ofensivas y de RE en sec-agent-squad

> **Proyecto en VM:** `sec-agent-squad` (sandbox Zero-Trust gVisor `runsc` sobre GCP VM, acceso via `gcloud compute ssh --tunnel-through-iap`).
> **Ventana de contexto objetivo:** 32.768 tokens. El plan esta seccionado en fases para que cada fase quepa y sea ejecutable sin colapso.
> **Fecha:** 2026-11-19.

---

## 1. Arquitectura actual (lo que ya corre en la VM)

El `sec-agent-squad` ejecuta comandos aislados en **dos imagenes sandbox** bajo gVisor (`runsc`), `--read-only`, UID `65534`:

| Modos | Wrapper (VM) | Imagen | Base | Stack principal |
|-------|--------------|--------|------|-----------------|
| `net`  | `/usr/local/bin/run-sec-sandbox-net`  | `sec-sandbox-net`  | `python:3.12-slim-bookworm` | playwright, httpx, curl, openssl, dnsutils, jq |
| `code` | `/usr/local/bin/run-sec-sandbox-code` | `sec-sandbox-code` | `debian:bookworm-slim` + Node 22 | semgrep, ruff, ast-grep, tree-sitter-cli, gitleaks, trivy |

Mecanica de ejecucion (`core/sandbox_executor.py`):
- `SandboxExecutor.run(mode, container_cmd, target, workspace_dir, timeout)`.
- El workspace se empaqueta en `tar.gz` (excluye `.env`, `.git`, `node_modules`, `__pycache__`, `secrets.json`).
- Si el base64 pesa <= 16000 chars se inyecta inline; si no, se sube por `gcloud scp` y se lee con `< /tmp/ws-*.tar.gz`.
- Antes de correr, `ScopeEnforcer` valida el target de red y el path local.

Guardrail Zero-Trust (`guardrails/scope_enforcer.py` + `config/authorized_scope.json`):
- **Default-deny** estricto: solo `allowed_domains` / `allowed_cidrs`.
- `denied_cidrs` bloquea `169.254.169.254/32` (metadata GCP) y rangos privados (`10/8`, `172.16/12`, `192.168/16`).
- `allowed_local_roots` contiene el path local al workspace.

**Consecuencia para la integracion ofensiva:** las herramientas ofensivas (nmap, nuclei, ffuf, etc.) son *clientes de red agresivos*. No pueden correr en el sandbox `code` (`--network=none`, offline). Necesitan un **tercer sandbox `offense`** con red, y deben respetar el `ScopeEnforcer` para no escanear afuera del alcance autorizado (evitar SSRF / escaneo de metadata / red interna).


---

## 2. Investigacion: Herramientas Ofensivas (escaneo / fuzzing / explotacion)

| Herramienta | Rol | Tipo | Salida estandar | Dependencia de red |
|-------------|-----|------|-----------------|--------------------|
| **nmap** | Descubrimiento de red, escaneo de puertos, version detection, NSE scripts | Binario Go/C (nmap.org) | `-oX` (XML), `-oJ` (JSON), `-oN` (normal) | Alta (SYN/ACK, UDP, scripts) |
| **subfinder** | Descubrimiento de subdominios (passive: Certificate Transparency, DNS) | Binario Go (ProjectDiscovery) | `-o` (txt), `-json` (JSONL), `-all` | Media (DNS + CT logs) |
| **katana** | Web crawler / spider de alto rendimiento (headless + JS rendering) | Binario Go (ProjectDiscovery) | `-jsonl`, `-o` (raw URLs), `-hc` (live) | Alta (HTTP + headless Chrome) |
| **nuclei** | Motor de vulnerabilidades basado en templates YAML (OWASP, CVEs, misconfigs) | Binario Go (ProjectDiscovery) | `-jsonl`, `-report` (HTML), `-severity`, `-tags`, `-t` | Alta (HTTP + headless opcional) |
| **ffuf** | Fuzzing de HTTP (paths, params, vhosts, headers) | Binario Go (ffuf/ffuf) | `-of json`, `-of html`, `-of csv` | Media (HTTP requests) |
| **dalfox** | Fuzzing de XSS (reflected, DOM, blind, CSP bypass) | Binario Go (projectdiscovery/dalfox) | `-o json`, `-o html` | Alta (HTTP + headless) |
| **jwt_tool** | Analisis / explotacion de tokens JWT (alg=none, weak keys, jku, kid injection) | Python (pyjwt) `pip install jwt_tool` | `--show`, `--list-algs`, `--show-payload`, salida texto | Baja (offline, solo procesa tokens) |
| **arjun** | Fuzzing de parametros HTTP ocultos (GET/POST/headers/cookies) | Python `pip install arjun` | `-o json`, `-o txt` | Media (HTTP requests) |


---

## 3. Investigacion: Toolkits de Ingenieria Inversa / Descompilacion

| Herramienta | Rol | Tipo | Salida | Requiere GUI? |
|-------------|-----|------|--------|---------------|
| **ghidra** | Decompilador / disassembler (JVM, headless via `analyzeHeadless`) | Java (NSA) | `.xml`, `.txt`, export C | No (headless CLI) |
| **radare2** | Framework de RE (disassemble, decompile, patch, analyze) | Binario C (r2) | `aaa`, `pd`, `pdf`, `-A`, `r2pm` (plugin manager) | No (CLI TUI) |

---

## 4. Hallazgos clave de la investigacion

1. **Todas las herramientas ofensivas son binarios Go o paquetes Python** que emiten salida estructurada (`-jsonl`, `-of json`, `--json`). Esto las hace ideales para el pipeline `SandboxExecutor` que ya captura `stdout`/`stderr` y puede parsear JSON.

2. **nuclei, subfinder, katana, ffuf, dalfox** son de **ProjectDiscovery** y comparten el mismo ecosistema (templates, `nuclei -t`, `katana | nuclei`). Se instalan como binarios Go estaticos (sin dependencias) y corren sin problemas en `debian:bookworm-slim`.

3. **nmap** necesita permisos de red raw (SYN scan) y `--privileged` en el container, o al menos `CAP_NET_RAW`. Es la unica que exige capacidad especial.

4. **jwt_tool y arjun** son paquetes Python (`pip install`). Pueden correr en el sandbox `code` (que ya tiene venv) o en el nuevo sandbox `offense`.

5. **ghidra, radare2, jadx** son herramientas de RE offline. No necesitan red. ghidra y jadx son Java (necesitan JRE 17+), radare2 es binario C estatico. Corren perfectamente en el sandbox `code` (offline, `--network=none`).

6. **Conflicto de alcance (scope):** los scanners ofensivos quieren escanear TODO. El `ScopeEnforcer` actual solo permite `localhost`, `127.0.0.1`, `example.com` y bloquea metadata + red privada. Para auditorias ofensivas reales hay que **ampliar `authorized_scope.json`** con el dominio/IP objetivo, manteniendo `denied_cidrs` para no escanear la infraestructura de la VM.

7. **GVisor `runsc`** soporta `--network=host` o bridge. El sandbox `net` ya tiene red (playwright). El nuevo sandbox `offense` puede reutilizar el wrapper `run-sec-sandbox-net` o crear un wrapper dedicado `run-sec-sandbox-offense`.


---

## 5. Diseno de integracion

### 5.1 Nuevo sandbox `offense` (Dockerfile.offense)
- Base: `debian:bookworm-slim` (igual que `code`).
- Binarios Go estaticos: `nmap`, `subfinder`, `katana`, `nuclei`, `ffuf`, `dalfox` (descarga de GitHub releases, como ya hace `code` con gitleaks/trivy).
- Python venv con `jwt_tool`, `arjun`.
- Red: `--network=host` o bridge (para escaneo). `nmap` con `--cap-add=NET_RAW`.
- UID `65534`, `--read-only`, gVisor `runsc`.

### 5.2 Extension del ScopeEnforcer
- Agregar `allowed_domains` / `allowed_cidrs` del objetivo a auditar en `authorized_scope.json`.
- Mantener `denied_cidrs` (metadata + private) para no escanear la infra de la VM.
- Nuevo metodo `validate_offense_target(target)` que valida el target antes de correr el scanner.

### 5.3 Extension de SandboxExecutor
- Nuevo modo `"offense"` en el diccionario `WRAPPERS`:
  ```python
  WRAPPERS = {
      "net":    ("/usr/local/bin/run-sec-sandbox-net",    "sec-sandbox-net"),
      "code":   ("/usr/local/bin/run-sec-sandbox-code",   "sec-sandbox-code"),
      "offense":("/usr/local/bin/run-sec-sandbox-offense","sec-sandbox-offense"),
  }
  ```
- `run(mode="offense", target=...)` valida el target con `ScopeEnforcer` antes de ejecutar.
- `core/sandbox_executor.py`: `run()` ya soporta `target`; validar que nmap/katana/dalfox reciben el target validado.

---

## 6. Plan de implementacion por fases (adaptado a 32.768 tokens)

Cada fase es autocontenida, ejecutable sin colapsar la ventana de contexto. Se marcan los archivos a tocar y el gate de validacion.

### FASE 1 — Sandbox `offense` base (nuclei + ffuf + subfinder)
**Objetivo:** primer sandbox ofensivo funcional con las 3 herramientas de ProjectDiscovery mas usadas.
**Archivos a crear/modificar:**
- `infra/Dockerfile.offense` (nuevo): debian:bookworm-slim + binarios Go (nuclei, ffuf, subfinder) + venv python (jwt_tool, arjun).
- `core/sandbox_executor.py`: agregar modo `"offense"` a `WRAPPERS`.
- `config/authorized_scope.json`: ampliar `allowed_domains` con el objetivo de prueba.
**Gate:** `python -m pytest tests/test_sandbox_bridge.py -k offense` (nuevo test que corre `nuclei -version` y `ffuf -version` en el sandbox).
**Tokens est.:** ~4.000.

### FASE 2 — nmap + katana + dalfox (scanners de red y web)
**Objetivo:** agregar nmap (puertos), katana (crawler) y dalfox (XSS).
**Archivos a modificar:**
- `infra/Dockerfile.offense`: agregar `nmap`, `katana`, `dalfox` (binarios Go). `nmap` con `--cap-add=NET_RAW`.
- `core/sandbox_executor.py`: `run()` ya soporta `target`; validar que nmap/katana/dalfox reciben el target validado.
**Gate:** test que corre `nmap -oJ <target>` y `katana -jsonl <url>` y verifica el JSON de salida.
**Tokens est.:** ~4.500.

### FASE 3 — jwt_tool + arjun (fuzzing de parametros y JWT)
**Objetivo:** fuzzing de parametros ocultos (arjun) y explotacion de JWT (jwt_tool).
**Archivos a modificar:**
- `infra/Dockerfile.offense`: el venv python ya tiene `jwt_tool` y `arjun` (instalados en FASE 1). Solo se expone en el PATH.
- `core/sandbox_executor.py`: agregar helpers `run_jwt_tool(token, flags)` y `run_arjun(url, flags)` que arman el comando y validan el target.
**Gate:** test que corre `arjun -u <url> -o json` y `jwt_tool <token> --show` y verifica la salida.
**Tokens est.:** ~3.500.

### FASE 4 — Toolkits de RE (ghidra + radare2 + jadx) en sandbox `code`
**Objetivo:** ingenieria inversa de binarios offline en el sandbox `code` existente (no necesita red).
**Archivos a modificar:**
- `infra/Dockerfile.code`: agregar JRE 17 (`default-jre-headless`), `ghidra` (descarga de GitHub), `radare2` (`apt` o binario), `jadx` (binario Java).
- `core/sandbox_executor.py`: agregar helpers `run_ghidra(binary)`, `run_r2(binary)`, `run_jadx(apk)`.
**Gate:** test que corre `r2 -q -c 'aaa;pd' <binary>` y `jadx -d /tmp/out <apk>` en el sandbox `code`.
**Tokens est.:** ~4.000.

### FASE 5 — Orquestacion + reporte unificado
**Objetivo:** pipeline completo que encadena subfinder -> katana -> nuclei -> ffuf/dalfox y genera un reporte HTML/JSON.
**Archivos a crear/modificar:**
- `core/offense_pipeline.py` (nuevo): orquesta las herramientas y produce un reporte.
- `config/authorized_scope.json`: plantilla de alcance por objetivo.
**Gate:** test end-to-end que corre el pipeline completo sobre un target de prueba y valida el reporte.
**Tokens est.:** ~5.000.


---

## 7. Orden de ejecucion y riesgos

**Orden recomendado:** FASE 1 -> FASE 2 -> FASE 3 -> FASE 4 -> FASE 5.
- FASES 1-3 construyen el sandbox `offense` (ofensivo, con red).
- FASE 4 agrega RE en el sandbox `code` existente (offline).
- FASE 5 orquesta todo.

**Riesgos y mitigaciones:**
| Riesgo | Mitigacion |
|--------|-----------|
| nmap necesita `CAP_NET_RAW` | `--cap-add=NET_RAW` en el wrapper `run-sec-sandbox-offense` |
| Escaneo fuera de alcance (SSRF / metadata) | `ScopeEnforcer.validate_offense_target()` + `denied_cidrs` |
| ghidra/jadx consumen mucha RAM (JVM) | Limitar con `--memory` en gVisor; correr en sandbox `code` separado |
| Templates de nuclei desactualizados | `nuclei -update-templates` al inicio de cada pipeline |
| Ventana de contexto (32.768) | Cada fase es autocontenida; se ejecuta una fase por turnos de contexto |

**Resumen de tokens por fase (total ~21.000, cabe en 32.768 con margen):**
- FASE 1: ~4.000 | FASE 2: ~4.500 | FASE 3: ~3.500 | FASE 4: ~4.000 | FASE 5: ~5.000

- `core/sandbox_executor.py`: `run()` ya soporta `target`; validar que nmap/katana/dalfox reciben el target validado.
**Gate:** test que corre `nmap -oJ <target>` y `katana -jsonl <url>` y verifica el JSON de salida.
**Tokens est.:** ~4.500.

      "code":   ("/usr/local/bin/run-sec-sandbox-code",   "sec-sandbox-code"),
      "offense":("/usr/local/bin/run-sec-sandbox-offense","sec-sandbox-offense"),
  }
  ```
- `run(mode="offense", target=...)` valida el target con `ScopeEnforcer` antes de ejecutar.

5. **ghidra, radare2, jadx** son herramientas de RE offline. No necesitan red. ghidra y jadx son Java (necesitan JRE 17+), radare2 es binario C estatico. Corren perfectamente en el sandbox `code` (offline, `--network=none`).

6. **Conflicto de alcance (scope):** los scanners ofensivos quieren escanear TODO. El `ScopeEnforcer` actual solo permite `localhost`, `127.0.0.1`, `example.com` y bloquea metadata + red privada. Para auditorias ofensivas reales hay que **ampliar `authorized_scope.json`** con el dominio/IP objetivo, manteniendo `denied_cidrs` para no escanear la infraestructura de la VM.

7. **GVisor `runsc`** soporta `--network=host` o bridge. El sandbox `net` ya tiene red (playwright). El nuevo sandbox `offense` puede reutilizar el wrapper `run-sec-sandbox-net` o crear un wrapper dedicado `run-sec-sandbox-offense`.

| **jadx** | Decompilador de dex/jar/apk a Java source | Java `jadx -d out.jar app.apk` | `.java` source, `--json` | No (CLI) |

