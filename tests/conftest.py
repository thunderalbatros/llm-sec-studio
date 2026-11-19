"""Pytest configuration ensuring llm-sec-studio/src is on sys.path and live markers are registered."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_configure(config) -> None:
    config.addinivalue_line(
        "markers",
        "live: live end-to-end tests requiring the GCP Qwen 3.8 27B IAP tunnel at 127.0.0.1:8000",
    )
