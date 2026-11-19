# Walkthrough — Misión de Blindaje Pre-Maestra (`100% PASS`)

> **Verificado:** `2026-11-19` (ART) | **Estado VM GCP (`llm-qwen-abliterated`, `us-central1-b`):** `TERMINATED` (`$0.00/h` cómputo, `PORT_8000_LISTENERS=0`) *(posteriormente migrada a `northamerica-northeast2-a` en el polyrepo `llm-sec-studio`)*

---

## 1. Librería Curada de Skills + Defensa Anti-Indirect Prompt Injection (`$0` GCP)

- **10 `SKILL.md` defensivas y auditadas** (`<= 600` tokens c/u, cero payloads ofensivos/webshells, cero patrones de prompt injection) en `skills_library/`:
  - [secure_system_architecture/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/secure_system_architecture/SKILL.md)
  - [threat_modeling_stride/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/threat_modeling_stride/SKILL.md)
  - [variant_analysis_audit/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/variant_analysis_audit/SKILL.md)
  - [detection_and_hardening/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/detection_and_hardening/SKILL.md)
  - [differential_pr_security_review/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/differential_pr_security_review/SKILL.md)
  - [web_api_security_audit/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/web_api_security_audit/SKILL.md)
  - [sast_ast_refactoring/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/sast_ast_refactoring/SKILL.md)
  - [reverse_engineering_safe_triage/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/reverse_engineering_safe_triage/SKILL.md)
  - [indirect_prompt_injection_defense/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/indirect_prompt_injection_defense/SKILL.md)
  - [agent_harness_and_web_engineering/SKILL.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/skills_library/agent_harness_and_web_engineering/SKILL.md)
- **Integración en el Arsenal existente (sin duplicar RAG):** [arsenal_registry.json](file:///C:/Users/tomas/Desktop/llm-sec-studio/config/arsenal_registry.json) (`< 800` tokens) + [query_arsenal.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/src/llm_sec_studio/tools/query_arsenal.py) + [.clinerules](file:///C:/Users/tomas/Desktop/llm-sec-studio/.clinerules).
- **Sanitizador determinista + compresor de trazas (`< 2 ms`, `0 MB` RAM extra):** [prompt_sanitizer.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/src/llm_sec_studio/guardrails/prompt_sanitizer.py) con normalización NFKC, strip de caracteres zero-width/bidi, comentarios HTML/scripts/control tokens, detección bilingüe EN/ES y aislamiento `<untrusted_data source="...">`.

---

## 2. Gates Deterministas Unificados y Evals Reproducibles (`$0` GCP)

- **Herramientas y reglas:** `gitleaks 8.30.1` instalado con allowlist verificada en [gitleaks.toml](file:///C:/Users/tomas/Desktop/llm-sec-studio/config/gitleaks.toml) y 5 reglas SAST AST en [security_baseline.yml](file:///C:/Users/tomas/Desktop/llm-sec-studio/config/ast_rules/security_baseline.yml) (`5/5` verificadas con snippets vulnerables sintéticos: `py-subprocess-shell-true`, `py-unsafe-eval-exec`, `py-unsafe-yaml-load`, `js-unsafe-eval`, `js-sql-string-concat`).
- **Gate Unificado Rápido ([run_gates.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/src/llm_sec_studio/tools/run_gates.py)):**
  - Modo rápido (`uv run run-gates`): **`PASS=True` en `1,138.1 ms`** (`< 3s`): `ruff` (`67.7 ms`), `ty` (`379.5 ms`), `oxlint` (`313.8 ms`), `ast_grep` (`342.8 ms`), `gitleaks` (`1,096.9 ms`, `23` archivos limpios), `supply_chain_fast` (`1.0 ms`).
  - Modo completo (`--full`): `supply_chain_guard.mjs` `PASS` (`64` pkgs, SBOM `38` componentes) + `gitleaks` limpio en `4` directorios.
- **Evals Offline (`uv run pytest tests/evals/ -m "not live" -v`):** **`6 passed, 3 deselected in 0.61s`** (cero warnings, marcador `live` registrado en [conftest.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/tests/conftest.py)):
  - [test_prompt_sanitizer.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/tests/evals/test_prompt_sanitizer.py) (`3/3 PASS`)
  - [test_skills_and_registry.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/tests/evals/test_skills_and_registry.py) (`3/3 PASS`)

---

## 3. Hardening en VM GCP (`us-central1-b`), Validación Live y Apagado FinOps

| Verificación en VM / Túnel IAP | Resultado | Evidencia Verificada (`[VERIFICADO: 2026-11-19]`) |
| :--- | :---: | :--- |
| **Google gVisor (`runsc`) + NVIDIA runtime** | **PASS** | `runsc release-20261116.0` (`spec 1.2.1`) instalado. `/etc/docker/daemon.json` conserva simultáneamente `nvidia` y `runsc`. `docker run --rm --runtime=runsc alpine dmesg` → `[0.000000] Starting gVisor...`. VRAM `qwen-server`: **`18,196 MiB / 23,034 MiB`**. |
| **Techo duro de razonamiento** | **PASS** | En el primer intento con `--reasoning-budget 1536`, `bench_streaming` (`max_tokens: 900`) agotaba los 900 tokens antes del techo (`900 < 1536`). Ajustado a **`--reasoning-budget 512 --reasoning-budget-message "Thinking budget reached. Provide final answer:" --presence-penalty 0.0`** en `qwen-server` y [iniciar_llm.ps1](file:///C:/Users/tomas/scripts-gcp-llm/iniciar_llm.ps1) (`PS1_PARSE_ERRORS=0`). |
| **Watchdog de Inactividad (35 min)** | **PASS** | `qwen-idle-watchdog.timer` (`systemd`, `60s`, gracia `300s`, límite `2100s` → `/sbin/poweroff`) + `/usr/local/bin/qwen-idle-watchdog.sh` monitoreando `/v1/`, `/slots` y GPU util > `2%`. `WATCHDOG_TIMER_STATE=active`, `--dry-run` verificado. |
| **Micro-Benchmark ([llm_health_benchmark.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/src/llm_sec_studio/tools/llm_health_benchmark.py))** | **PASS** | **`overall_pass: true`** (`BENCH_EXIT=0`): `streaming` **`PASS`** (`TTFT 927.0 ms`, `gen 17.21 tok/s`, **`content_chars: 535`**, `reasoning_chars: 1,790`, `ratio: 3.346`, `679 / 900` tokens), `nested_tool_calling` **`PASS`** (`15.8 s`, `2` hits reales), `security_patch` **`PASS`** (`10.7 s`). |
| **Evals Live ([test_llm_live_evals.py](file:///C:/Users/tomas/Desktop/llm-sec-studio/tests/evals/test_llm_live_evals.py))** | **PASS** | `pytest -m live -v`: **`3 passed in 57.55s`** (`streaming`, `nested_tool_calling + patch`, `indirect_prompt_injection_resistance` con HTML hostil sanitizado). |
| **Apagado FinOps (`detener_llm.ps1`)** | **PASS** | `FINAL_VM_STATUS=TERMINATED`, `PORT_8000_LISTENERS=0` (`$0.00/h` de cómputo). |

Reporte maestro actualizado en [PREFLIGHT_REPORT.md](file:///C:/Users/tomas/Desktop/llm-sec-studio/docs/PREFLIGHT_REPORT.md).
