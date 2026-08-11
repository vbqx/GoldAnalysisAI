"""Regression: the offline sample stays aligned with Advice V2."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.regression

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "docs/aspice/SWE.3-detailed-design/reference/examples/sample-report.json"


def test_export_sample_report_script() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/export_sample_report.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    assert sample["artifact_kind"] == "human_review_advice"
    assert sample["artifact_version"] == 2
    assert sample["meta"]["sample"] is True
    assert sample["advice"]["audit"]["passed"] is True
    assert sample["advice"]["decision"] in {"WAIT", "WATCH_LONG", "WATCH_SHORT", "AVOID"}
    assert not ({"signals", "agent_trace", "validated_plans", "projections"} & sample.keys())
    price = sample["metrics"]["current_price"]
    assert price is not None and not math.isnan(float(price))
