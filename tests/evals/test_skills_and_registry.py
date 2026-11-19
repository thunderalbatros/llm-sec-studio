"""Deterministic evals verifying skills_library budgets, prompt-injection hygiene, and query_arsenal bounds."""
import json
import os
import subprocess
import sys
from pathlib import Path

from llm_sec_studio.guardrails.prompt_sanitizer import sanitize_text

ROOT = Path(__file__).resolve().parents[2]


def est_tokens(text: str) -> int:
    return (len(text) + 3) // 4


def test_skills_library_count_budget_and_hygiene() -> None:
    skills = sorted((ROOT / "skills_library").glob("*/SKILL.md"))
    assert len(skills) >= 8, f"Expected >= 8 curated skills, found {len(skills)}"
    required = {
        "secure_system_architecture",
        "threat_modeling_stride",
        "variant_analysis_audit",
        "detection_and_hardening",
    }
    found_names = {p.parent.name for p in skills}
    assert required.issubset(found_names), f"Missing required skills: {required - found_names}"

    for skill_path in skills:
        txt = skill_path.read_text(encoding="utf-8")
        tok = est_tokens(txt)
        assert tok <= 600, f"{skill_path.parent.name} exceeds 600-token budget ({tok} tokens)"
        assert txt.startswith("---\n"), f"{skill_path} missing YAML frontmatter"
        scan = sanitize_text(txt, source=skill_path.parent.name)
        assert "instruction_override_en" not in scan["findings"], f"Injection pattern in {skill_path}"
        assert "instruction_override_es" not in scan["findings"], f"Injection pattern in {skill_path}"
        assert "role_hijack" not in scan["findings"], f"Role hijack pattern in {skill_path}"


def test_arsenal_registry_under_800_tokens() -> None:
    reg_path = ROOT / "config" / "arsenal_registry.json"
    raw = reg_path.read_text(encoding="utf-8")
    tok = est_tokens(raw)
    assert tok < 800, f"arsenal_registry.json exceeded 800 tokens ({tok})"
    reg = json.loads(raw)
    assert reg.get("skills_library") == "skills_library"
    for dom in ("cybersec_audit", "agent_harness", "web_engineering", "browser_automation"):
        assert dom in reg["domains"]


def test_query_arsenal_discovers_skills_and_respects_budget() -> None:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "llm_sec_studio.tools.query_arsenal",
            "--query",
            "STRIDE threat modeling variant analysis ast-grep",
            "--domain",
            "cybersec_audit",
            "--top-k",
            "3",
            "--json",
        ],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["returned"] > 0
    assert data["total_tokens_est"] <= 1500
    assert any(r["source"] == "skills_library" for r in data["results"])


def test_query_arsenal_reads_shared_wsf_sqlite_readonly() -> None:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "llm_sec_studio.tools.query_arsenal",
            "--query",
            "OWASP ASVS JWT authentication",
            "--domain",
            "cybersec_audit",
            "--top-k",
            "3",
            "--json",
        ],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["returned"] > 0
    assert data["total_tokens_est"] <= 1500
    assert any(r["source"] in {"wsf_hot_sqlite", "wsf_library_sqlite", "curated_catalog"} for r in data["results"])
