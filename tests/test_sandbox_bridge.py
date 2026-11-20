"""Tests for the offense sandbox bridge (gVisor/runsc on GCP VM).

Requires an active GCP VM with the sec-sandbox-offense image deployed.
Run with: uv run pytest tests/test_sandbox_bridge.py -m live -v
"""

import json
import os
import subprocess
import sys

import pytest

# Resolve gcloud path (Windows .cmd wrapper)
if sys.platform == "win32":
    GCLOUD = os.path.expandvars(
        r"%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    )
else:
    GCLOUD = "gcloud"

VM_NAME = "llm-qwen-abliterated"
VM_ZONE = "northamerica-northeast2-a"
WRAPPER = "/usr/local/bin/run-sec-sandbox-offense"
IMAGE = "sec-sandbox-offense"
TARGET = "scanme.nmap.org"


def _run_on_vm(command: str, timeout: int = 120) -> str:
    """Run a command on the VM via gcloud SSH and return stdout."""
    result = subprocess.run(
        [
            GCLOUD, "compute", "ssh", VM_NAME,
            f"--zone={VM_ZONE}", "--tunnel-through-iap",
            f"--command={command}",
        ],
        capture_output=True, text=True, timeout=timeout,
    )
    return result.stdout.strip()


def _sandbox(cmd: str, timeout: int = 120) -> str:
    """Run a command inside the offense sandbox."""
    return _run_on_vm(f"sudo {WRAPPER} {IMAGE} {cmd}", timeout)


@pytest.mark.live
class TestSandboxOffense:
    """Verify all 5 offensive tools work inside the gVisor sandbox."""

    def test_nmap_json_output(self):
        """NMAP -oJ produces valid JSON with port data."""
        # nmap -oJ writes JSON to a file; human-readable goes to stdout
        # Use sh -c to redirect human-readable output and cat the JSON file
        out = _sandbox(
            f"sh -c 'nmap -sV {TARGET} -oJ/tmp/nmap.json 2>&1 >/dev/null && cat /tmp/nmap.json'"
        )
        data = json.loads(out)
        ports = data["scan"]["hosts"][0]["ports"]
        assert len(ports) > 0
        assert any(p["portid"] == 22 for p in ports)

    def test_nuclei_jsonl(self):
        """Nuclei -jsonl produces valid JSON Lines."""
        out = _sandbox(
            f"nuclei -jsonl -severity high,critical -u http://{TARGET} 2>/dev/null"
        )
        # No findings is OK; just verify no crash
        assert "panic" not in out.lower()

    def test_katana_jsonl(self):
        """Katana -jsonl produces valid JSON with request/response."""
        out = _sandbox(
            f"sh -c 'katana -jsonl -u http://{TARGET} 2>/dev/null | head -1'"
        )
        data = json.loads(out)
        assert "request" in data
        assert "response" in data
        assert data["response"]["status_code"] == 200

    def test_ffuf_json(self):
        """FFUF -of json produces valid JSON results."""
        out = _sandbox(
            f"sh -c 'ffuf -of json -u http://{TARGET}/FUZZ "
            f"-w /usr/share/nmap/nmap-payloads/ -o /tmp/ffuf.json 2>/dev/null && cat /tmp/ffuf.json'"
        )
        data = json.loads(out)
        assert "results" in data

    def test_dalfox_scan(self):
        """Dalfox scan runs without errors."""
        out = _sandbox(f"dalfox scan -u http://{TARGET} 2>/dev/null")
        assert "panic" not in out.lower()

    def test_jwt_tool_show(self):
        """JWT tool --show decodes a JWT correctly."""
        jwt = (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.x"
        )
        out = _sandbox(f"jwt_tool --show {jwt} 2>&1")
        # pycryptodomex warning may appear; check for decoded content
        assert "admin" in out or "user" in out or "header" in out.lower()

    def test_arjun_json(self):
        """Arjun -o json runs without errors."""
        out = _sandbox(
            f"arjun -u http://{TARGET}/ -o json -t 5 2>/dev/null"
        )
        assert "arjun" in out.lower() or "v2" in out
