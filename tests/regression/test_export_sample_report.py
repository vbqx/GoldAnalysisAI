"""Regression: offline sample report export stays compatible with AgentTrace schema."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "docs" / "reference" / "examples" / "sample-report.json"


def test_export_sample_report_script() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "export_sample_report.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert SAMPLE.is_file(), "sample-report.json was not written"

    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    assert sample["meta"]["sample"] is True
    trace = sample["agent_trace"]
    assert "llm_levels" in trace
    assert "validated_plans" in trace

    price = sample["metrics"]["current_price"]
    assert price is not None and not math.isnan(float(price))
