#!/usr/bin/env bash
# sec-agent-squad/infra/run-sec-sandbox-offense.sh
# Deploy to /usr/local/bin/run-sec-sandbox-offense on the GCP VM.
# gVisor (runsc) wrapper for the offense sandbox: nuclei + ffuf + subfinder + nmap + katana + dalfox.
# --cap-add=NET_RAW is required for nmap raw sockets (ICMP/TCP connect).
set -euo pipefail

IMAGE="${1:-sec-sandbox-offense}"
shift || true

sudo docker run --rm \
  --runtime=runsc \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=512m \
  --cap-add=NET_RAW \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --memory=1g \
  --pids-limit=256 \
  --user 65534:65534 \
  "$IMAGE" "$@"
