from __future__ import annotations

import json
from pathlib import Path

from src.analysis.fact_registry import build_fact_registry
from src.analysis.report_invariants import validate_report_invariants

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_wait_observation_passes_invariants() -> None:
    report = _load("wait_observation.json")
    registry = build_fact_registry(report)
    report["meta"]["fact_registry"] = registry
    result = validate_report_invariants(report, registry=registry)
    assert result["passed"] is True
    assert result["violation_count"] == 0


def test_bad_geometry_flags_sell_below_price() -> None:
    report = _load("bad_geometry.json")
    result = validate_report_invariants(report)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-GEO-003" in codes
    assert result["passed"] is False


def test_stale_data_flags_urgent_language() -> None:
    report = _load("stale_urgent_narrative.json")
    result = validate_report_invariants(report)
    codes = {v["code"] for v in result["violations"]}
    assert "INV-FRESH-001" in codes
