"""Ensure sec-agent-squad is first on sys.path for isolated test execution."""
import sys
from pathlib import Path

SQUAD_ROOT = Path(__file__).resolve().parents[1]
if str(SQUAD_ROOT) not in sys.path:
    sys.path.insert(0, str(SQUAD_ROOT))
