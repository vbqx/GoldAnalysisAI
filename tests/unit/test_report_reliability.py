from __future__ import annotations

import json
from pathlib import Path

from src.analysis.fact_registry import build_fact_registry
from src.analysis.report_invariants import validate_report_invariants
from src.analysis.report_reliability import compute_report_reliability

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_reliability_components_bounded() -> None:
    report = _load("wait_observation.json")
    registry = build_fact_registry(report)
    report["meta"]["fact_registry"] = registry
    report["meta"]["report_invariants"] = validate_report_invariants(report, registry=registry)
    rel = compute_report_reliability(report)
    assert 0.0 <= rel["overall_reliability"] <= 1.0
    assert rel["model_self_reported_confidence"] == 0.72
    assert rel["schema_quality"] == 1.0
    assert rel["freshness_quality"] < rel["data_quality"] or report["meta"]["observation_mode"]


def test_source_diversity_ignores_agent_prefix() -> None:
    report = {
        "agent_trace": {
            "debate": {
                "bullish": {
                    "items": [
                        {"evidence_id": "technical_analyst:0", "refs": {"source": "same"}},
                        {"evidence_id": "technical_analyst:1", "refs": {"source": "same"}},
                    ]
                },
                "bearish": {"items": []},
            },
            "analyst_team": {},
        },
        "meta": {"report_invariants": {"passed": True}},
    }
    rel = compute_report_reliability(report)
    assert rel["source_diversity"] < 0.34
    assert rel["calibration_status"] == "heuristic"


def test_reliability_drops_on_invariant_failures() -> None:
    good = _load("wait_observation.json")
    registry = build_fact_registry(good)
    good["meta"]["fact_registry"] = registry
    good["meta"]["report_invariants"] = validate_report_invariants(good, registry=registry)
    good_score = compute_report_reliability(good)["overall_reliability"]

    bad = _load("bad_geometry.json")
    bad["meta"]["report_invariants"] = validate_report_invariants(bad)
    bad_score = compute_report_reliability(bad)["overall_reliability"]
    assert bad_score < good_score
