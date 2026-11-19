"""SSH IAP remote sandbox bridge invoking Zero-Trust gVisor (runsc) wrappers on GCP VM."""
from __future__ import annotations

import base64
import fnmatch
import importlib.util
import io
import json
import secrets
import shlex
import shutil
import subprocess
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "sec_squad_scope_enforcer", Path(__file__).resolve().parents[1] / "guardrails" / "scope_enforcer.py"
)
assert _SPEC is not None and _SPEC.loader is not None
_MOD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MOD)
ScopeEnforcer, ScopeViolationError = _MOD.ScopeEnforcer, _MOD.ScopeViolationError

DEFAULT_VM_STATE = Path.home() / "scripts-gcp-llm" / "vm_state.json"
WRAPPERS = {
    "net": ("/usr/local/bin/run-sec-sandbox-net", "sec-sandbox-net"),
    "code": ("/usr/local/bin/run-sec-sandbox-code", "sec-sandbox-code"),
    "offense": ("/usr/local/bin/run-sec-sandbox-offense", "sec-sandbox-offense"),
}


@dataclass(frozen=True)
class SandboxResult:
    returncode: int
    stdout: str
    stderr: str
    mode: str
    zone: str


def load_vm_coords(state_path: Path | str | None = None) -> dict[str, str]:
    data = json.loads((Path(state_path) if state_path else DEFAULT_VM_STATE).read_text(encoding="utf-8-sig"))
    return {"project": str(data["project"]), "instance": str(data["instance"]), "zone": str(data["zone"])}


def _is_excluded(rel_posix: str, name: str, patterns: list[str]) -> bool:
    parts = rel_posix.split("/")
    return any(fnmatch.fnmatch(name, p) or any(fnmatch.fnmatch(part, p) for part in parts) for p in patterns)


def package_workspace_tar(source_dir: Path | str, excluded_patterns: list[str] | None = None) -> bytes:
    """Create a clean gzipped tar archive excluding .env, .git, node_modules, and secrets."""
    root = Path(source_dir).resolve()
    patterns = excluded_patterns or [".env", ".env.*", ".git", "node_modules", "__pycache__", "secrets.json"]
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for item in sorted(root.rglob("*")):
            if item.is_file() and not _is_excluded(item.relative_to(root).as_posix(), item.name, patterns):
                tf.add(item, arcname=item.relative_to(root).as_posix(), recursive=False)
    return buf.getvalue()


class SandboxExecutor:
    """Executes isolated commands in gVisor sandboxes via gcloud SSH IAP (never duplicates --runtime=runsc)."""

    def __init__(self, scope_enforcer: ScopeEnforcer | None = None, vm_state_path: Path | str | None = None) -> None:
        self.scope = scope_enforcer or ScopeEnforcer()
        self.vm = load_vm_coords(vm_state_path)
        self.gcloud = shutil.which("gcloud.cmd") or shutil.which("gcloud") or "gcloud"

    def build_ssh_command(self, mode: str, container_cmd: list[str], inline_b64: str | None = None, remote_tar: str | None = None) -> list[str]:
        if mode not in WRAPPERS:
            raise ValueError(f"Unsupported sandbox mode: {mode!r}")
        wrapper, image = WRAPPERS[mode]
        quoted = " ".join(shlex.quote(arg) for arg in container_cmd)
        if inline_b64:
            remote_cmd = f"printf '%s' {shlex.quote(inline_b64)} | base64 -d | sudo {wrapper} {image} {quoted}"
        elif remote_tar:
            rt = shlex.quote(remote_tar)
            remote_cmd = f"trap 'rm -f {rt}' EXIT; sudo {wrapper} {image} {quoted} < {rt}"
        else:
            remote_cmd = f"sudo {wrapper} {image} {quoted}"
        return [
            self.gcloud, "compute", "ssh", self.vm["instance"], f"--zone={self.vm['zone']}",
            f"--project={self.vm['project']}", "--tunnel-through-iap", "--quiet", f"--command={remote_cmd}",
        ]

    def _upload_tar(self, tar_bytes: bytes, timeout: int) -> str:
        remote_tar = f"/tmp/ws-{secrets.token_hex(6)}.tar.gz"
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
            tmp.write(tar_bytes)
            local_path = Path(tmp.name)
        try:
            scp = [self.gcloud, "compute", "scp", str(local_path), f"{self.vm['instance']}:{remote_tar}", f"--zone={self.vm['zone']}", f"--project={self.vm['project']}", "--tunnel-through-iap", "--quiet"]
            for _ in range(2):
                res = subprocess.run(scp, capture_output=True, timeout=timeout, check=False)
                if res.returncode == 0:
                    return remote_tar
            raise RuntimeError(f"gcloud scp failed: {res.stderr.decode('utf-8', errors='replace')[:250]}")
        finally:
            local_path.unlink(missing_ok=True)

    def run(self, mode: str, container_cmd: list[str], target: str | None = None, workspace_dir: Path | str | None = None, timeout: int = 120) -> SandboxResult:
        if mode in ("net", "offense") and target:
            self.scope.validate_network_target(target)
        inline_b64, remote_tar = None, None
        final_cmd = list(container_cmd)
        if workspace_dir is not None:
            tar_bytes = package_workspace_tar(self.scope.validate_local_path(workspace_dir), self.scope.excluded_tar_patterns)
            b64 = base64.b64encode(tar_bytes).decode("ascii")
            if len(b64) <= 16000:
                inline_b64 = b64
            else:
                remote_tar = self._upload_tar(tar_bytes, timeout)
            inner = " ".join(shlex.quote(c) for c in container_cmd)
            final_cmd = ["sh", "-c", f"mkdir -p /tmp/workspace && tar -xzf - -C /tmp/workspace && cd /tmp/workspace && {inner}"]
        argv = self.build_ssh_command(mode, final_cmd, inline_b64=inline_b64, remote_tar=remote_tar)
        proc = subprocess.run(argv, capture_output=True, timeout=timeout, check=False)
        return SandboxResult(proc.returncode, proc.stdout.decode("utf-8", errors="replace"), proc.stderr.decode("utf-8", errors="replace"), mode, self.vm["zone"])

    # --- Phase 2 helpers: nmap + katana + dalfox (target validated against allowlist) ---

    def run_nmap(self, target: str, flags: list[str] | None = None, timeout: int = 180) -> SandboxResult:
        """Run nmap with -oJ JSON output against a scope-validated target (requires NET_RAW)."""
        self.scope.validate_network_target(target)
        cmd = ["nmap", "-oJ", "-"]
        if flags:
            cmd.extend(flags)
        cmd.append(target)
        return self.run("offense", cmd, target=target, timeout=timeout)

    def run_katana(self, url: str, flags: list[str] | None = None, timeout: int = 180) -> SandboxResult:
        """Run katana with -jsonl output against a scope-validated URL."""
        self.scope.validate_network_target(url)
        cmd = ["katana", "-jsonl", "-o", "/dev/stdout"]
        if flags:
            cmd.extend(flags)
        cmd.append(url)
        return self.run("offense", cmd, target=url, timeout=timeout)

    def run_dalfox(self, url: str, flags: list[str] | None = None, timeout: int = 180) -> SandboxResult:
        """Run dalfox scan against a scope-validated URL."""
        self.scope.validate_network_target(url)
        cmd = ["dalfox", "scan"]
        if flags:
            cmd.extend(flags)
        cmd.append(url)
        return self.run("offense", cmd, target=url, timeout=timeout)

    # --- Phase 3 helpers: jwt_tool + arjun (venv python already in PATH) ---

    def run_jwt_tool(self, token: str, flags: list[str] | None = None, timeout: int = 60) -> SandboxResult:
        """Run jwt_tool --show against a JWT token (token is not a network target, no scope check)."""
        cmd = ["jwt_tool", token, "--show"]
        if flags:
            cmd.extend(flags)
        return self.run("offense", cmd, timeout=timeout)

    def run_arjun(self, url: str, flags: list[str] | None = None, timeout: int = 180) -> SandboxResult:
        """Run arjun with -o json output against a scope-validated URL."""
        self.scope.validate_network_target(url)
        cmd = ["arjun", "-u", url, "-o", "json", "-oR", "/dev/stdout"]
        if flags:
            cmd.extend(flags)
        return self.run("offense", cmd, target=url, timeout=timeout)

    # --- Phase 4 helpers: RE toolkits in sandbox `code` (binary/apk path, no scope check) ---

    def run_ghidra(self, binary: str, flags: list[str] | None = None, timeout: int = 300) -> SandboxResult:
        """Run Ghidra analyzeHeadless on a binary (code sandbox, no scope validation)."""
        cmd = ["analyzeHeadless", "-import", binary]
        if flags:
            cmd.extend(flags)
        return self.run("code", cmd, timeout=timeout)

    def run_r2(self, binary: str, flags: list[str] | None = None, timeout: int = 180) -> SandboxResult:
        """Run radare2 disassembly (r2 -q -c 'aaa;pd') on a binary (code sandbox)."""
        cmd = ["r2", "-q", "-c", "aaa;pd", binary]
        if flags:
            cmd.extend(flags)
        return self.run("code", cmd, timeout=timeout)

    def run_jadx(self, apk: str, flags: list[str] | None = None, timeout: int = 300) -> SandboxResult:
        """Run jadx decompilation (jadx -d /tmp/out) on an APK (code sandbox)."""
        cmd = ["jadx", "-d", "/tmp/out", apk]
        if flags:
            cmd.extend(flags)
        return self.run("code", cmd, timeout=timeout)
