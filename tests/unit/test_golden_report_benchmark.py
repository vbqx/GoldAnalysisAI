"""Deterministic zero-token golden report benchmark (#32)."""

from __future__ import annotations

import json
from pathlib import Path

from src.analysis.fact_registry import build_fact_registry
from src.analysis.report_invariants import validate_report_invariants
from src.analysis.report_reliability import compute_report_reliability

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"

# Frozen expectations — update only when invariant rules intentionally change.
GOLDEN = {
    "wait_observation.json": {
        "passed": True,
        "min_facts": 12,
        "overall_reliability": 0.649,
    },
    "bad_geometry.json": {
        "passed": False,
        "codes": ["INV-GEO-003"],
        "overall_reliability": 0.275,
    },
    "stale_urgent_narrative.json": {
        "passed": False,
        "codes": ["INV-FRESH-001"],
    },
}


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _run_benchmark(report: dict) -> dict:
    registry = build_fact_registry(report)
    report.setdefault("meta", {})["fact_registry"] = registry
    inv = validate_report_invariants(report, registry=registry)
    report["meta"]["report_invariants"] = inv
    rel = compute_report_reliability(report)
    return {
        "passed": inv["passed"],
        "codes": [v["code"] for v in inv["violations"]],
        "fact_count": registry["fact_count"],
        "overall_reliability": rel["overall_reliability"],
    }


def test_golden_report_benchmark_snapshots() -> None:
    for filename, expected in GOLDEN.items():
        result = _run_benchmark(_load(filename))
        assert result["passed"] == expected["passed"], filename
        if "min_facts" in expected:
            assert result["fact_count"] >= expected["min_facts"], filename
        if "codes" in expected:
            for code in expected["codes"]:
                assert code in result["codes"], f"{filename}: missing {code}"
        if "overall_reliability" in expected:
            assert abs(result["overall_reliability"] - expected["overall_reliability"]) < 0.06, filename
