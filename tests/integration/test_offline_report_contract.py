"""Deterministic cross-component verification for the Advice V2 report contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from src.advice.audit import audit_advice
from src.advice.engine import build_advice_packet
from src.advice.report import build_advice_report
from src.run.archive.compat import normalize_report
from src.run.archive.schema import REPORT_CONTRACT_VERSION

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "docs/aspice/SWE.3-detailed-design/reference/examples/sample-report.json"
LEGACY_KEYS = frozenset(
    {"signals", "agent_trace", "validated_plans", "projections", "path_summary"}
)
VALID_DECISIONS = frozenset({"WAIT", "WATCH_LONG", "WATCH_SHORT", "AVOID"})


def _load_sample() -> dict[str, Any]:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def _assert_offline_report_contract(report: dict[str, Any]) -> None:
    assert report.get("artifact_kind") == "human_review_advice"
    assert report.get("artifact_version") == REPORT_CONTRACT_VERSION
    assert not (LEGACY_KEYS & report.keys())

    meta = report.get("meta")
    assert isinstance(meta, dict)
    assert meta.get("observation_mode") is True

    advice = report.get("advice")
    assert isinstance(advice, dict)
    assert advice.get("decision") in VALID_DECISIONS
    assert advice.get("audit", {}).get("passed") is True

    setup = advice.get("primary_setup")
    decision = advice["decision"]
    if decision in {"WAIT", "AVOID"}:
        assert setup is None
    if decision in {"WATCH_LONG", "WATCH_SHORT"}:
        assert setup is not None
        assert setup.get("confirmation_checklist")
        assert setup.get("evidence_ids")

    metrics = report.get("metrics")
    assert isinstance(metrics, dict)
    assert metrics.get("current_price") is not None


@pytest.mark.integration
def test_sample_report_offline_contract() -> None:
    _assert_offline_report_contract(_load_sample())


@pytest.mark.integration
def test_normalize_report_preserves_advice_v2_contract() -> None:
    report = _load_sample()
    normalized, warnings = normalize_report(report)
    assert not warnings
    assert normalized["advice"] == report["advice"]
    _assert_offline_report_contract(normalized)
    assert normalized["meta"].get("archive_report_contract_version") == REPORT_CONTRACT_VERSION


@pytest.mark.integration
def test_build_advice_report_offline_contract() -> None:
    from tests.unit.test_advice_v2 import _context

    ctx = _context()
    packet = build_advice_packet(ctx)
    audit = audit_advice(packet)
    assert audit.passed

    report = build_advice_report(
        ctx,
        packet,
        run_id="offline-contract",
        run_config={"generation_mode": "rule"},
    )
    _assert_offline_report_contract(report)
