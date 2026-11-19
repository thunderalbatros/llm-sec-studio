"""Zero-Trust scope enforcement guardrail for sec-agent-squad."""
from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_SCOPE_PATH = Path(__file__).resolve().parents[1] / "config" / "authorized_scope.json"


class ScopeViolationError(PermissionError):
    """Raised when a target domain, IP, URL, or local path falls outside authorized_scope.json."""


class ScopeEnforcer:
    """Strict default-deny allowlist validator for network targets and local directories."""

    def __init__(self, scope_path: Path | str | None = None) -> None:
        path = Path(scope_path) if scope_path else DEFAULT_SCOPE_PATH
        data = json.loads(path.read_text(encoding="utf-8"))
        self.allowed_domains = {d.lower().strip() for d in data.get("allowed_domains", [])}
        self.allowed_nets = [ipaddress.ip_network(c, strict=False) for c in data.get("allowed_cidrs", [])]
        self.denied_nets = [ipaddress.ip_network(c, strict=False) for c in data.get("denied_cidrs", [])]
        self.allowed_roots = [Path(r).resolve() for r in data.get("allowed_local_roots", [])]
        self.excluded_tar_patterns = list(data.get("excluded_tar_patterns", []))

    def _extract_host(self, target: str) -> str:
        raw = target.strip()
        if not raw:
            raise ScopeViolationError("Empty target is not allowed.")
        parsed = urlparse(raw if "://" in raw else f"https://{raw}")
        host = (parsed.hostname or "").lower().strip(".")
        if not host:
            raise ScopeViolationError(f"Could not parse valid hostname from target: {target!r}")
        return host

    def validate_network_target(self, target: str) -> str:
        """Validate a URL, hostname, or IP against denied_cidrs first, then strict allowlist."""
        host = self._extract_host(target)
        try:
            ip_obj = ipaddress.ip_address(host)
        except ValueError:
            ip_obj = None

        if ip_obj is not None:
            for denied in self.denied_nets:
                if ip_obj in denied:
                    raise ScopeViolationError(f"Blocked forbidden IP/metadata target: {host}")
            for allowed in self.allowed_nets:
                if ip_obj in allowed:
                    return host
            if host in self.allowed_domains:
                return host
            raise ScopeViolationError(f"IP target {host} is not in authorized_scope.json")

        for dom in self.allowed_domains:
            if host == dom or (dom.startswith("*.") and host.endswith(dom[1:])):
                return host
        raise ScopeViolationError(f"Domain target {host} is not in authorized_scope.json")

    def validate_local_path(self, local_path: Path | str) -> Path:
        """Ensure a local workspace path stays strictly inside allowed_local_roots."""
        resolved = Path(local_path).resolve()
        for root in self.allowed_roots:
            try:
                resolved.relative_to(root)
                return resolved
            except ValueError:
                continue
        raise ScopeViolationError(f"Local path {resolved} escapes authorized_local_roots")
