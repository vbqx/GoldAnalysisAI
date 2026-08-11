"""Advice V2 end-to-end coherence checks."""

from __future__ import annotations

import json

import pytest

from tests._bootstrap import ROOT
from tests.tools.coherence_validate import validate_pipeline_coherence


@pytest.mark.slow
@pytest.mark.integration
def test_rule_mode_coherence_zero_issues(rule_pipeline_result) -> None:
    report, data, analyses = rule_pipeline_result
    issues, _notes, summary = validate_pipeline_coherence(report, data, analyses)
    output = ROOT / "tests" / "reports" / "coherence_check.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    assert not issues, "\n".join(issues)


@pytest.mark.slow
@pytest.mark.integration
def test_rule_mode_never_claims_execution_authority(rule_pipeline_result) -> None:
    report, _data, _analyses = rule_pipeline_result
    assert report["meta"]["observation_mode"] is True
    assert report["artifact_kind"] == "human_review_advice"
    assert "execute" not in json.dumps(report["advice"], ensure_ascii=False).lower()
