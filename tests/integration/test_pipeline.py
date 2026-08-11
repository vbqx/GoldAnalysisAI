"""Live integration checks for the Advice V2 pipeline."""

from __future__ import annotations

import time

import pytest

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.pipeline import run_analysis

EXPECTED_TFS = ("5m", "15m", "1h", "4h", "1d")


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_returns_human_review_advice(env_pipeline_result) -> None:
    report, _data, _analyses = env_pipeline_result
    assert report["artifact_kind"] == "human_review_advice"
    assert report["artifact_version"] == 2
    assert report["advice"]["decision"] in {"WAIT", "WATCH_LONG", "WATCH_SHORT", "AVOID"}
    assert report["meta"]["observation_mode"] is True
    assert report["advice"]["audit"]["passed"] is True
    for legacy_key in ("signals", "agent_trace", "validated_plans", "projections"):
        assert legacy_key not in report


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_multi_timeframe_data(env_pipeline_result) -> None:
    _report, data, analyses = env_pipeline_result
    for timeframe in EXPECTED_TFS:
        assert timeframe in data and len(data[timeframe]) > 50
        assert timeframe in analyses and analyses[timeframe].trend is not None


@pytest.mark.slow
@pytest.mark.integration
def test_report_price_matches_5m_close(env_pipeline_result) -> None:
    report, data, _analyses = env_pipeline_result
    price = float(report["metrics"]["current_price"])
    close_5m = float(data["5m"]["Close"].iloc[-1])
    tolerance = max(0.5, close_5m * 0.0002)
    assert abs(price - close_5m) <= tolerance


@pytest.mark.slow
@pytest.mark.integration
def test_watch_setup_has_reviewable_geometry(env_pipeline_result) -> None:
    report, _data, _analyses = env_pipeline_result
    advice = report["advice"]
    setup = advice.get("primary_setup")
    if advice["decision"] in {"WAIT", "AVOID"}:
        assert setup is None
        return
    assert setup is not None
    assert setup["confirmation_checklist"]
    assert setup["evidence_ids"]
    assert 1 <= len(setup["targets"]) <= 2


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_duration_within_limit() -> None:
    reporter = ProgressReporter()
    token = set_progress(reporter)
    started = time.perf_counter()
    try:
        run_analysis()
    finally:
        reset_progress(token)
    assert time.perf_counter() - started <= 240
