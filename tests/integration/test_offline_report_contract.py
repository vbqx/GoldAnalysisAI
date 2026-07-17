"""Deterministic cross-component verification for the report trust chain."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.analysis.fact_registry import build_fact_registry
from src.analysis.report_invariant_gate import apply_report_invariant_gate
from src.analysis.report_invariants import validate_report_invariants
from src.analysis.report_reliability import compute_report_reliability


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.mark.integration
@pytest.mark.parametrize(
    ("fixture", "expected_passed"),
    [("wait_observation.json", True), ("bad_geometry.json", False)],
)
def test_report_trust_chain_offline_contract(
    fixture: str,
    expected_passed: bool,
) -> None:
    """Integrate registry, invariants, gate, and reliability without suppliers."""
    report = _load(fixture)
    registry = build_fact_registry(report)
    report.setdefault("meta", {})["fact_registry"] = registry

    invariants = validate_report_invariants(report, registry=registry)
    report["meta"]["report_invariants"] = invariants
    gated = apply_report_invariant_gate(report, invariants)
    reliability = compute_report_reliability(report)

    assert registry["fact_count"] > 0
    assert gated["passed"] is expected_passed
    assert report["meta"]["invariant_gate"]["status"] in {"passed", "degraded"}
    assert 0.0 <= reliability["overall_reliability"] <= 1.0
    if not expected_passed:
        assert gated["remediated"] is True
        assert report["meta"]["pipeline_status"] == "degraded"
