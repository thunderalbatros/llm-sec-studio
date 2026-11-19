"""FASE 5: Offensive pipeline orchestration (subfinder -> katana -> nuclei -> ffuf/dalfox) with unified JSON+HTML report."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.sandbox_executor import SandboxExecutor, SandboxResult
from guardrails.scope_enforcer import ScopeEnforcer


@dataclass
class PipelineStep:
    """Result of one pipeline stage."""
    name: str
    returncode: int
    stdout: str
    stderr: str
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PipelineReport:
    """Unified report across all pipeline stages."""
    target: str
    started_at: str
    finished_at: str
    steps: list[PipelineStep] = field(default_factory=list)
    status: str = "ok"

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "status": self.status,
            "steps": [
                {
                    "name": s.name,
                    "returncode": s.returncode,
                    "findings": s.findings,
                    "stdout": s.stdout,
                    "stderr": s.stderr,
                }
                for s in self.steps
            ],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def to_html(self) -> str:
        rows = []
        for s in self.steps:
            findings_html = "".join(f"<li>{json.dumps(f, ensure_ascii=False)}</li>" for f in s.findings)
            findings_block = f"<ul>{findings_html}</ul>" if findings_html else "<p><em>sin hallazgos</em></p>"
            rows.append(f"<tr><td>{s.name}</td><td>{s.returncode}</td><td>{findings_block}</td></tr>")
        return (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>Offense Pipeline Report - {self.target}</title></head><body>"
            f"<h1>Offense Pipeline Report</h1>"
            f"<p>Target: <code>{self.target}</code></p>"
            f"<p>Started: {self.started_at} | Finished: {self.finished_at} | Status: <strong>{self.status}</strong></p>"
            "<table border='1'><tr><th>Paso</th><th>Returncode</th><th>Hallazgos</th></tr>"
            + "".join(rows)
            + "</table></body></html>"
        )


class OffensePipeline:
    """Orchestrates subfinder -> katana -> nuclei -> ffuf/dalfox against a scope-validated target.

    Produces a unified JSON + HTML report. `nuclei -update-templates` runs at pipeline start.
    """

    def __init__(self, executor: SandboxExecutor | None = None, scope_enforcer: ScopeEnforcer | None = None) -> None:
        self.executor = executor or SandboxExecutor()
        self.scope = scope_enforcer or self.executor.scope

    def validate_target(self, target: str) -> str:
        return self.scope.validate_network_target(target)

    def run_pipeline(self, target: str, output_dir: Path | str | None = None) -> PipelineReport:
        """Run the full pipeline and write report.json + report.html to output_dir."""
        validated = self.validate_target(target)
        started_at = datetime.now(timezone.utc).isoformat()
        report = PipelineReport(target=validated, started_at=started_at, finished_at="")

        # nuclei -update-templates at pipeline start (recorded risk)
        report.steps.append(self._run_step("nuclei-update-templates", self.executor.run("offense", ["nuclei", "-update-templates"], target=target)))

        # subfinder: subdomain discovery
        report.steps.append(self._run_step("subfinder", self.executor.run("offense", ["subfinder", "-d", self.scope._extract_host(target), "-json"], target=target)))

        # katana: web crawling (JSONL)
        report.steps.append(self._run_step("katana", self.executor.run_katana(target)))

        # nuclei: vulnerability scanning (JSONL)
        report.steps.append(self._run_step("nuclei", self.executor.run("offense", ["nuclei", "-jsonl", "-o", "/dev/stdout", target], target=target)))

        # ffuf: HTTP path fuzzing (JSON)
        report.steps.append(self._run_step("ffuf", self.executor.run("offense", ["ffuf", "-u", target + "/{wordlist}", "-w", "/usr/share/wordlists/common.txt", "-of", "json"], target=target)))

        # dalfox: XSS fuzzing (JSON)
        report.steps.append(self._run_step("dalfox", self.executor.run_dalfox(target)))

        report.finished_at = datetime.now(timezone.utc).isoformat()
        report.status = "ok" if all(s.returncode == 0 for s in report.steps) else "partial"

        out = Path(output_dir) if output_dir else Path(__file__).resolve().parents[1] / "reports"
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.json").write_text(report.to_json(), encoding="utf-8")
        (out / "report.html").write_text(report.to_html(), encoding="utf-8")
        return report

    def _run_step(self, name: str, result: SandboxResult) -> PipelineStep:
        step = PipelineStep(name=name, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        step.findings = self._parse_findings(name, result.stdout)
        return step

    def _parse_findings(self, step_name: str, stdout: str) -> list[dict[str, Any]]:
        """Parse JSON/JSONL output into findings list."""
        findings: list[dict[str, Any]] = []
        for line in stdout.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if step_name == "nuclei" and isinstance(data, dict) and "template" in data:
                findings.append(data)
            elif step_name == "katana" and isinstance(data, dict) and "type" in data:
                findings.append(data)
            elif step_name == "subfinder" and isinstance(data, dict) and "host" in data:
                findings.append(data)
            elif step_name == "ffuf" and isinstance(data, dict) and "results" in data:
                findings.extend(data["results"])
            elif step_name == "dalfox" and isinstance(data, dict):
                findings.append(data)
        return findings