# PREFLIGHT_REPORT.md — Blindaje Integral Zero-Trust, Pre-Vuelo y Arsenal RAG (Qwen 3.8 27B + Cline)

> **Fecha de verificación final:** `2026-11-19` (ART)  
> **Workspace:** `C:\Users\tomas\Desktop\web-software-factory`  
> **Estado actual de VM GCP:** `TERMINATED` (`$0.00/h` de cómputo; solo disco `100 GB pd-balanced` ~`$0.33/día`, `PORT_8000_LISTENERS=0`)

---

## 1. Tabla Healthcheck Zero-Trust & Pre-Vuelo (`100% PASS`)

| Capa / Componente | Estado | Evidencia Verificada en Vivo (`[VERIFICADO: 2026-11-19]`) |
| :--- | :---: | :--- |
| **1. Identidad IAM Mínimo Privilegio (GCP)** | **PASS** | Service Account dedicada **`sa-llm-zero-priv@project-6565e6dc-f33c-49ff-b22.iam.gserviceaccount.com`** asignada con **`--no-scopes`** y **`0` roles IAM de proyecto** (reemplazó a la cuenta default de Compute Engine). |
| **2. Perímetro VPC, IP Efímera vs Cloud NAT y Shielded VM** | **PASS** | VPC `llm-vpc` con únicamente `llm-allow-iap-ssh` (`prio 1000`, `35.235.240.0/20`, `tcp:22`) + **`llm-deny-all-ingress`** (`prio 65534`, `0.0.0.0/0`, `DENY all`, logging activo). **Evaluación FinOps:** se conservó IP efímera (`$0.005/h` solo encendida; `$0/h` apagada) blindada con `DROP` total de entrada en VPC y host (`ZT-HOST-INPUT`), evitando Cloud NAT (`~$7.30–$10/mes` fijos 24/7). **Shielded VM:** `enableSecureBoot: true`, `enableVtpm: true`, `enableIntegrityMonitoring: true` verificados en vivo junto con driver NVIDIA firmado `580.178.04` (`PKCS#7`, `Canonical Ltd. Kernel Module Signing`, `NVIDIA L4 23034 MiB`). |
| **3. Hardening Linux (`sysctl` + `sshd` + `DOCKER-USER`)** | **PASS** | `/etc/sysctl.d/99-zero-trust-hardening.conf`: `kptr_restrict=2`, `dmesg_restrict=1`, `yama.ptrace_scope=2`, `rp_filter=1`, `tcp_syncookies=1`. `/etc/ssh/sshd_config.d/99-zero-trust.conf` (`sshd -t` OK): `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `PermitRootLogin no`, `X11Forwarding no`, `AllowAgentForwarding no`, `GatewayPorts no`, **`AllowTcpForwarding local`**. Firewall persistente `zero-trust-firewall.service=enabled` (`/usr/local/sbin/apply-zt-firewall.sh` en `DOCKER-USER` + `INPUT`). |
| **4. Contenedor `qwen-server` Endurecido + 131K Contexto + Prefix Cache** | **PASS** | `User=65534:65534`, `CapDrop=[ALL]`, `SecurityOpt=[no-new-privileges:true]`, `ReadonlyRootfs=true`, `/tmp:rw,noexec,nosuid,size=256m`, `Mounts=/modelos:rw=false`, red `llm-noegress`. Modelo `Coder390-EfficientThink-abliterated.i1-Q4_K_M.gguf` (Gated DeltaNet híbrido) en **`-np 1 -c 131072`** (4x vs `32K` previo; fallback `131072→98304→65536`), `-fa on --cache-type-k/v q8_0 --cache-reuse 256 --presence-penalty 0.0 --reasoning-budget 512 --spec-type ngram-cache --spec-draft-n-max 3`. VRAM estable: **`20,576 MiB / 23,034 MiB`** (`~2.4 GiB` libres), `SLOTS: [(0, 131072)]`. **Prefix Cache Hit en vivo (6K tok):** Turno 1 `13.06 s` (`0` cached) → Turno 2 **`3.38 s` (`5,983/6,001` = `99.7%` cached, `3.86x` más rápido)**. |
| **5. Sandboxes gVisor (`runsc`) y Cero `docker.sock`** | **PASS** | `runsc release-20261116.0` preservando `nvidia` runtime + `"dns": ["1.1.1.1", "8.8.8.8"]` en `/etc/docker/daemon.json`. Redes dedicadas `sec-sandbox-code` (`internal=true`) y `sec-sandbox-net`, imágenes defensivas `sec-sandbox-code:latest` y `sec-sandbox-net:latest` verificadas bajo `runsc`. **`PENTEST_DOCKER_SOCK_MOUNTS=0`**. |
| **6. Detección Activa (`auditd` + Logs Firewall) y Watchdog 35 min** | **PASS** | `auditd=active` con **`8` reglas Zero-Trust** (`/etc/audit/rules.d/99-zero-trust.rules`). Alertas kernel `[ZT-DROP-HOST8000]`, `[ZT-DROP-DOCKER-IN]`, `[ZT-DROP-LLM-EGRESS]` verificadas en `journalctl -k`. Watchdog `qwen-idle-watchdog.timer=active` (`35 min` inactividad → `/sbin/poweroff`). |
| **7. Optimización de Contexto Cline + Slicer AST + Escudo Prompt Injection** | **PASS** | Cline (`globalState.json`, `providers.json`, `models.json`): **`contextWindow: 131072`**, **`useAutoCondense: true`**, `reasoningEffort: "low"`, `terminalOutputLineLimit: 80`, `maxTokens: 4096`. Nuevo `tools/code_slice.py` (`0` tokens MCP, `>= 70%` ahorro vs lectura completa), `tools/token_audit_proxy.py` (proxy CCR + telemetría opt-in), `.agents/memory/session_handoff.md`, `.clineignore` podado, `guardrails/input_sanitizer.py`, `10` skills (`<= 600` tok) y `tools/run_gates.py` (`PASS`, `< 2 s`). |
| **8. Batería de Pentest Interno (`11/11 PASS`)** | **PASS** | Desde `runsc`: `169.254.169.254` bloqueado (`PASS`), `172.30.0.1:8000` / `10.200.0.9:8000` / `127.0.0.1:8000` / `172.30.0.1:22` aislados (`4/4 PASS`), rootfs sandbox `:ro` y `sec-sandbox-code` sin red (`2/2 PASS`); en `qwen-server`: `/modelos` inmutable (`PASS`), rootfs `:ro` (`PASS`), cero egreso `1.1.1.1:443` (`PASS`), cero `docker.sock` (`PASS`). |
| **9. Validación Live a 131K (`llm_health_benchmark.py` + `pytest` 16/16)** | **PASS** | `iniciar_llm.ps1` (`0` parse errors, `0` unapproved verbs, Auto-Failover multi-región en `vm_state.json`), **`llm_health_benchmark.py --json` (`overall_pass: true`)**: Streaming `TTFT 957.0 ms` / `17.02 tok/s` / `content_chars: 495`, Tool Calling Anidado `10.9 s` (`2` hits `query_arsenal.py`), Security Patch `6.9 s`. **`pytest tests/evals/`:** **`16/16 PASS`** (`54.39 s`, `0` warnings). |

---

## 2. Evidencia de Batería de Pentest Interno (VM `us-central1-b`)

- `PENTEST_DOCKER_SOCK_MOUNTS=0`
- `PENTEST_METADATA_BLOCK=PASS` (`wget http://169.254.169.254/computeMetadata/v1/` bloqueado desde `run-sec-sandbox-net`)
- `PENTEST_HOST_ISOLATION_172.30.0.1:8000=PASS` (kernel log `[ZT-DROP-HOST8000]`)
- `PENTEST_HOST_ISOLATION_10.200.0.9:8000=PASS` (kernel log `[ZT-DROP-HOST8000]`)
- `PENTEST_HOST_ISOLATION_127.0.0.1:8000=PASS`
- `PENTEST_HOST_ISOLATION_172.30.0.1:22=PASS` (kernel log `[ZT-DROP-DOCKER-IN]`)
- `PENTEST_SANDBOX_RO_ROOTFS=PASS` y `PENTEST_SANDBOX_CODE_NO_NET=PASS`
- `PENTEST_MODELOS_IMMUTABLE=PASS`, `PENTEST_QWEN_RO_ROOTFS=PASS`, `PENTEST_QWEN_NO_EGRESS=PASS` (kernel log `[ZT-DROP-LLM-EGRESS]`)

---

## 3. Comandos Operativos Diarios
- **Encender VM + Túnel IAP:** `~\scripts-gcp-llm\iniciar_llm.ps1`
- **Estado + FinOps:** `~\scripts-gcp-llm\estado_llm.ps1`
- **Detener VM (`$0.00/h` cómputo):** `~\scripts-gcp-llm\detener_llm.ps1`
- **Escudo Anti-Prompt-Injection (Spotlighting):** `python guardrails/input_sanitizer.py --source "<origen>" --json`
- **Gate Unificado (< 3s):** `python tools/run_gates.py` (o `--full` para SBOM/SRI + gitleaks completo)
- **Router RAG + Skills:** `python tools/query_arsenal.py --query "<consulta>" --domain <cybersec_audit|agent_harness|web_engineering|browser_automation> --json`
- **Evals Offline / Live:** `uv run --with pytest pytest tests/evals/ -m "not live" -v` / `uv run --with pytest pytest tests/evals/test_llm_live_evals.py -m live -v`
- **Sandboxes gVisor en VM:** `sudo run-sec-sandbox-code <imagen> <cmd>` / `sudo run-sec-sandbox-net <imagen> <cmd>`
