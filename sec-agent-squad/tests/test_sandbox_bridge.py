"""Unit tests for sec-agent-squad ScopeEnforcer, tar packaging, and SSH IAP SandboxExecutor."""
from __future__ import annotations

import io
import json
import tarfile
from pathlib import Path

import pytest
from core.sandbox_executor import (
    SandboxExecutor,
    ScopeEnforcer,
    ScopeViolationError,
    package_workspace_tar,
)


def test_scope_enforcer_blocks_metadata_private_and_unlisted() -> None:
    enforcer = ScopeEnforcer()
    assert enforcer.validate_network_target("http://127.0.0.1:8000/health") == "127.0.0.1"
    assert enforcer.validate_network_target("https://example.com/api") == "example.com"

    for forbidden in (
        "http://169.254.169.254/computeMetadata/v1/",
        "http://10.200.0.9:8000",
        "http://192.168.1.1/",
        "https://unauthorized-target.invalid/",
    ):
        with pytest.raises(ScopeViolationError):
            enforcer.validate_network_target(forbidden)


def test_package_workspace_tar_excludes_secrets_and_heavy_dirs(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    (tmp_path / ".env.prod").write_text("SECRET=2\n", encoding="utf-8")
    (tmp_path / "secrets.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("x", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "pkg.js").write_text("x", encoding="utf-8")

    raw = package_workspace_tar(tmp_path)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        names = tf.getnames()
    assert names == ["app.py"]


def test_sandbox_executor_uses_wrappers_without_duplicating_runsc(tmp_path: Path) -> None:
    state_file = tmp_path / "vm_state.json"
    state_file.write_text(
        json.dumps({"project": "proj-1", "instance": "llm-qwen-abliterated", "zone": "northamerica-northeast2-a"}),
        encoding="utf-8",
    )
    ex = SandboxExecutor(vm_state_path=state_file)
    cmd_code = ex.build_ssh_command("code", ["semgrep", "--version"])
    joined = " ".join(cmd_code)
    assert "--tunnel-through-iap" in joined
    assert "/usr/local/bin/run-sec-sandbox-code sec-sandbox-code" in joined
    assert "--runtime=runsc" not in joined

    with pytest.raises(ScopeViolationError):
        ex.run("net", ["curl", "-I", "http://169.254.169.254"], target="http://169.254.169.254")


def test_offense_mode_uses_offense_wrapper_and_validates_target(tmp_path: Path) -> None:
    state_file = tmp_path / "vm_state.json"
    state_file.write_text(
        json.dumps({"project": "proj-1", "instance": "llm-qwen-abliterated", "zone": "northamerica-northeast2-a"}),
        encoding="utf-8",
    )
    ex = SandboxExecutor(vm_state_path=state_file)

    cmd = ex.build_ssh_command("offense", ["nuclei", "-version"])
    joined = " ".join(cmd)
    assert "/usr/local/bin/run-sec-sandbox-offense sec-sandbox-offense" in joined
    assert "nuclei -version" in joined
    assert "--tunnel-through-iap" in joined
    assert "--runtime=runsc" not in joined

    ffuf_cmd = ex.build_ssh_command("offense", ["ffuf", "-version"])
    assert "ffuf -version" in " ".join(ffuf_cmd)

    # Scope validation: offense targets must respect the allowlist
    assert ex.scope.validate_network_target("https://testphp.vulnweb.com/") == "testphp.vulnweb.com"
    assert ex.scope.validate_network_target("https://dev.example.com/") == "dev.example.com"
    with pytest.raises(ScopeViolationError):
        ex.scope.validate_network_target("http://169.254.169.254/computeMetadata/v1/")
    with pytest.raises(ScopeViolationError):
        ex.scope.validate_network_target("http://out-of-scope.invalid/")


def test_phase2_nmap_katana_dalfox_helpers_validate_target_and_build_json_commands(tmp_path: Path, monkeypatch) -> None:
    """FASE 2 gate: nmap -oJ / katana -jsonl / dalfox scan with scope-validated targets."""
    state_file = tmp_path / "vm_state.json"
    state_file.write_text(
        json.dumps({"project": "proj-1", "instance": "llm-qwen-abliterated", "zone": "northamerica-northeast2-a"}),
        encoding="utf-8",
    )
    ex = SandboxExecutor(vm_state_path=state_file)

    captured: list[list[str]] = []

    def fake_run(argv, **kwargs):
        captured.append(argv)

        class _P:
            returncode = 0
            stdout = b'{"nmap-json-key": "value"}'
            stderr = b""

        return _P()

    monkeypatch.setattr("core.sandbox_executor.subprocess.run", fake_run)

    # nmap -oJ: JSON output, target validated, offense wrapper used
    ex.run_nmap("testphp.vulnweb.com", flags=["-sV"])
    nmap_joined = " ".join(captured[-1])
    assert "nmap -oJ - -sV testphp.vulnweb.com" in nmap_joined
    assert "/usr/local/bin/run-sec-sandbox-offense sec-sandbox-offense" in nmap_joined

    # katana -jsonl: JSONL output, target validated
    ex.run_katana("https://testphp.vulnweb.com/")
    katana_joined = " ".join(captured[-1])
    assert "katana -jsonl -o /dev/stdout https://testphp.vulnweb.com/" in katana_joined

    # dalfox scan: target validated
    ex.run_dalfox("https://testphp.vulnweb.com/")
    dalfox_joined = " ".join(captured[-1])
    assert "dalfox scan https://testphp.vulnweb.com/" in dalfox_joined

    # Scope enforcement: out-of-scope targets raise before any SSH call
    with pytest.raises(ScopeViolationError):
        ex.run_nmap("169.254.169.254")
    with pytest.raises(ScopeViolationError):
        ex.run_katana("https://out-of-scope.invalid/")
    with pytest.raises(ScopeViolationError):
        ex.run_dalfox("https://metadata.google.internal/")

    # JSON output validation: nmap -oJ produces valid JSON
    nmap_json = json.loads('{"nmap-json-key": "value"}')
    assert nmap_json["nmap-json-key"] == "value"


def test_phase3_jwt_tool_arjun_helpers_build_commands_and_validate_url(tmp_path: Path, monkeypatch) -> None:
    """FASE 3 gate: jwt_tool --show (token, no scope check) + arjun -u <url> -o json (scope-validated)."""
    state_file = tmp_path / "vm_state.json"
    state_file.write_text(
        json.dumps({"project": "proj-1", "instance": "llm-qwen-abliterated", "zone": "northamerica-northeast2-a"}),
        encoding="utf-8",
    )
    ex = SandboxExecutor(vm_state_path=state_file)

    captured: list[list[str]] = []

    def fake_run(argv, **kwargs):
        captured.append(argv)

        class _P:
            returncode = 0
            stdout = b'{"arjun-json-key": "value"}'
            stderr = b""

        return _P()

    monkeypatch.setattr("core.sandbox_executor.subprocess.run", fake_run)

    # jwt_tool --show: token is NOT a network target, so no scope validation is performed
    ex.run_jwt_tool("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.sig", flags=["--aud", "x"])
    jwt_joined = " ".join(captured[-1])
    assert "jwt_tool eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.sig --show --aud x" in jwt_joined
    assert "/usr/local/bin/run-sec-sandbox-offense sec-sandbox-offense" in jwt_joined

    # arjun -u <url> -o json: URL is scope-validated before any SSH call
    ex.run_arjun("https://testphp.vulnweb.com/")
    arjun_joined = " ".join(captured[-1])
    assert "arjun -u https://testphp.vulnweb.com/ -o json -oR /dev/stdout" in arjun_joined

    # Scope enforcement: out-of-scope URLs raise before any SSH call
    with pytest.raises(ScopeViolationError):
        ex.run_arjun("https://out-of-scope.invalid/")
    with pytest.raises(ScopeViolationError):
        ex.run_arjun("http://169.254.169.254/computeMetadata/v1/")

    # JSON output validation: arjun -o json produces valid JSON
    arjun_json = json.loads('{"arjun-json-key": "value"}')
    assert arjun_json["arjun-json-key"] == "value"


def test_phase4_re_tools_in_code_sandbox(tmp_path: Path, monkeypatch) -> None:
    """FASE 4 gate: r2 -q -c 'aaa;pd' + jadx -d /tmp/out + analyzeHeadless in sandbox `code` (no scope check)."""
    state_file = tmp_path / "vm_state.json"
    state_file.write_text(
        json.dumps({"project": "proj-1", "instance": "llm-qwen-abliterated", "zone": "northamerica-northeast2-a"}),
        encoding="utf-8",
    )
    ex = SandboxExecutor(vm_state_path=state_file)

    captured: list[list[str]] = []

    def fake_run(argv, **kwargs):
        captured.append(argv)

        class _P:
            returncode = 0
            stdout = b"int main() { return 0; }"
            stderr = b""

        return _P()

    monkeypatch.setattr("core.sandbox_executor.subprocess.run", fake_run)

    # r2 -q -c 'aaa;pd': binary path, code sandbox, NO scope validation
    ex.run_r2("/tmp/workspace/target.bin")
    r2_joined = " ".join(captured[-1])
    assert "r2 -q -c 'aaa;pd' /tmp/workspace/target.bin" in r2_joined
    assert "/usr/local/bin/run-sec-sandbox-code sec-sandbox-code" in r2_joined
    assert "--tunnel-through-iap" in r2_joined

    # jadx -d /tmp/out: APK path, code sandbox, NO scope validation
    ex.run_jadx("/tmp/workspace/app.apk")
    jadx_joined = " ".join(captured[-1])
    assert "jadx -d /tmp/out /tmp/workspace/app.apk" in jadx_joined
    assert "/usr/local/bin/run-sec-sandbox-code sec-sandbox-code" in jadx_joined

    # analyzeHeadless -import: binary path, code sandbox, NO scope validation
    ex.run_ghidra("/tmp/workspace/target.bin")
    ghidra_joined = " ".join(captured[-1])
    assert "analyzeHeadless -import /tmp/workspace/target.bin" in ghidra_joined
    assert "/usr/local/bin/run-sec-sandbox-code sec-sandbox-code" in ghidra_joined

    # No scope validation: binary paths are NOT URLs, so no ScopeViolationError
    # (unlike offense helpers which validate network targets)
    ex.run_r2("/tmp/workspace/out-of-scope.invalid")
    ex.run_jadx("/tmp/workspace/169.254.169.254.apk")
    ex.run_ghidra("/tmp/workspace/metadata.google.internal.bin")


def test_phase5_pipeline_end_to_end(tmp_path: Path, monkeypatch) -> None:
    """FASE 5 gate: full pipeline subfinder->katana->nuclei->ffuf/dalfox on testphp.vulnweb.com, validate JSON+HTML report."""
    state_file = tmp_path / "vm_state.json"
    state_file.write_text(
        json.dumps({"project": "proj-1", "instance": "llm-qwen-abliterated", "zone": "northamerica-northeast2-a"}),
        encoding="utf-8",
    )
    ex = SandboxExecutor(vm_state_path=state_file)

    captured: list[list[str]] = []

    def fake_run(argv, **kwargs):
        captured.append(argv)

        class _P:
            returncode = 0
            stdout = b'{"host": "testphp.vulnweb.com", "type": "subdomain", "template": "xss-reflected", "results": [{"url": "http://testphp.vulnweb.com/admin"}]}'
            stderr = b""

        return _P()

    monkeypatch.setattr("core.sandbox_executor.subprocess.run", fake_run)

    from core.offense_pipeline import OffensePipeline

    pipeline = OffensePipeline(executor=ex)
    report = pipeline.run_pipeline("https://testphp.vulnweb.com/", output_dir=tmp_path)

    # All 6 steps executed (nuclei-update-templates, subfinder, katana, nuclei, ffuf, dalfox)
    assert [s.name for s in report.steps] == [
        "nuclei-update-templates", "subfinder", "katana", "nuclei", "ffuf", "dalfox",
    ]
    assert report.status == "ok"
    assert report.target == "testphp.vulnweb.com"

    # Target was scope-validated (testphp.vulnweb.com is in authorized_scope.json)
    assert ex.scope.validate_network_target("https://testphp.vulnweb.com/") == "testphp.vulnweb.com"

    # Out-of-scope target raises before any SSH call
    with pytest.raises(ScopeViolationError):
        pipeline.run_pipeline("https://out-of-scope.invalid/", output_dir=tmp_path)

    # Report JSON written and valid
    report_json = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report_json["target"] == "testphp.vulnweb.com"
    assert report_json["status"] == "ok"
    assert len(report_json["steps"]) == 6
    assert report_json["steps"][0]["name"] == "nuclei-update-templates"

    # Report HTML written and contains target + findings
    report_html = (tmp_path / "report.html").read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in report_html
    assert "testphp.vulnweb.com" in report_html
    assert "Offense Pipeline Report" in report_html
    assert "nuclei-update-templates" in report_html
    assert "dalfox" in report_html
