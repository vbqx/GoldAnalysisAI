"""FIN-INT-03: rule-mode pipeline coherence (debate / signals / indicators)."""

from __future__ import annotations

import json

import pytest

from tests._bootstrap import ROOT
from tests.tools.coherence_validate import validate_pipeline_coherence


@pytest.mark.slow
@pytest.mark.integration
def test_rule_mode_coherence_zero_issues(rule_pipeline_result) -> None:
    """FIN-INT-03: rule 模式 debate / 信号几何 / 指标校验无 issue."""
    report, data, analyses = rule_pipeline_result
    issues, _notes, summary = validate_pipeline_coherence(report, data, analyses)

    out = ROOT / "tests" / "reports" / "coherence_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    assert not issues, "\n".join(issues)


@pytest.mark.slow
@pytest.mark.integration
def test_rule_mode_trader_aligns_with_bearish_structure(rule_pipeline_result) -> None:
    """FIN-14: 结构偏空时交易员主方向应为 short."""
    report, _data, _analyses = rule_pipeline_result
    sentiment = report["sentiment"]
    if sentiment["bearish"] < sentiment["bullish"]:
        pytest.skip("current snapshot is not bearish-dominant")

    proposal = report.get("agent_trace", {}).get("proposal", {})
    assert proposal.get("primary_direction") == "short"
