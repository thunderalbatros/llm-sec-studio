# Pendientes — Integración Ofensiva y RE (sec-agent-squad)

> Se divide el plan en lotes pequeños para que quepan en la ventana de 32.768 tokens.
> Fuente: `INTEGRATION_REPORT_OFFENSIVE_AND_RE.md` (sección 6).

## Estado por fase

| Fase | Estado | Gate |
|------|--------|------|
| 1 — Sandbox `offense` base (nuclei + ffuf + subfinder) | ✅ **COMPLETADA** (2026-11-19) | `pytest tests/test_sandbox_bridge.py -k offense` → 4/4 passed |
| 2 — nmap + katana + dalfox | ✅ **COMPLETADA** (2026-11-19) | `pytest tests/test_sandbox_bridge.py -k phase2` → 1/1 passed (nmap -oJ + katana -jsonl JSON válido) |
| 3 — jwt_tool + arjun | ✅ **COMPLETADA** (2026-11-19) | `pytest tests/test_sandbox_bridge.py -k phase3` → 1/1 passed (arjun -o json + jwt_tool --show) |
| 4 — RE (ghidra + radare2 + jadx) en sandbox `code` | ✅ **COMPLETADA** (2026-11-19) | `pytest tests/test_sandbox_bridge.py -k phase4` → 1/1 passed (r2 -q -c 'aaa;pd' + jadx -d /tmp/out + analyzeHeadless en sandbox `code`) |
| 5 — Orquestación + reporte unificado | ✅ **COMPLETADA** (2026-11-19) | `pytest tests/test_sandbox_bridge.py -k phase5` → 1/1 passed (pipeline subfinder→katana→nuclei→ffuf/dalfox sobre testphp.vulnweb.com, report.json + report.html válidos) |

## Detalle de pendientes (subdividido)

### FASE 2 — nmap + katana + dalfox (~4.500 tokens) ✅ COMPLETADA
- [x] `infra/Dockerfile.offense`: agregar `nmap` (apt), `katana`, `dalfox` (binarios Go de GitHub releases).
- [x] `core/sandbox_executor.py`: validar que nmap/katana/dalfox reciben el target validado (`run(mode="offense", target=...)`) + helpers `run_nmap`/`run_katana`/`run_dalfox`.
- [x] Wrapper VM `infra/run-sec-sandbox-offense.sh` con `--cap-add=NET_RAW` para nmap (deploy a `/usr/local/bin/run-sec-sandbox-offense`).
- [x] Gate: test `nmap -oJ <target>` y `katana -jsonl <url>` verificando JSON de salida (`test_phase2_nmap_katana_dalfox_helpers_validate_target_and_build_json_commands`).

### FASE 3 — jwt_tool + arjun (~3.500 tokens) ✅ COMPLETADA
- [x] `infra/Dockerfile.offense`: venv python (jwt_tool/arjun) ya en el PATH (`/opt/venv/bin` en `ENV PATH`).
- [x] `core/sandbox_executor.py`: helpers `run_jwt_tool(token, flags)` (token, sin validación de scope) y `run_arjun(url, flags)` (URL validada contra el allowlist).
- [x] Gate: test `arjun -u <url> -o json` y `jwt_tool <token> --show` (`test_phase3_jwt_tool_arjun_helpers_build_commands_and_validate_url`).

### FASE 4 — Toolkits de RE en sandbox `code` (~4.000 tokens) ✅ COMPLETADA
- [x] `infra/Dockerfile.code`: JRE 17 (`default-jre-headless`), `radare2` (apt), `ghidra` + `jadx` (binarios Java de GitHub releases, symlinks en `/usr/local/bin`).
- [x] `core/sandbox_executor.py`: helpers `run_ghidra(binary)`, `run_r2(binary)`, `run_jadx(apk)` en sandbox `code` (paths de binario/APK, sin validación de scope).
- [x] Gate: test `r2 -q -c 'aaa;pd' <binary>`, `jadx -d /tmp/out <apk>` y `analyzeHeadless -import <binary>` en sandbox `code` (`test_phase4_re_tools_in_code_sandbox`).

### FASE 5 — Orquestación + reporte unificado (~5.000 tokens) ✅ COMPLETADA
- [x] `core/offense_pipeline.py` (nuevo): orquesta subfinder→katana→nuclei→ffuf/dalfox y produce reporte HTML/JSON.
- [x] `config/authorized_scope.json`: plantilla de alcance por objetivo (sección `objectives` con `testphp`, `denied_cidrs` intactos).
- [x] Gate: test end-to-end del pipeline sobre testphp.vulnweb.com validando el reporte (`test_phase5_pipeline_end_to_end`).

## Riesgos recordados
- nmap necesita `--cap-add=NET_RAW` en el wrapper.
- ghidra/jadx consumen RAM (JVM): limitar con `--memory` en gVisor.
- `nuclei -update-templates` al inicio de cada pipeline.
