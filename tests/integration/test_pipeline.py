"""Integration tests — full pipeline (IT-01 ~ IT-04, IND-01, IND-33)."""
from __future__ import annotations

import time

import pytest

from src import config as app_config
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.pipeline import run_analysis

EXPECTED_TFS = ("5m", "15m", "1h", "4h", "1d")
PIPELINE_MAX_SECONDS_RULE = 240
PIPELINE_MAX_SECONDS_LLM = 320
REALTIME_PRICE_ABS_TOLERANCE = 0.5
REALTIME_PRICE_PCT_TOLERANCE = 0.0002


def _pipeline_max_seconds() -> int:
    if app_config.AGENT_MODE in ("llm", "hybrid") and (
        app_config.LLM_ENABLED
        or app_config.LLM_STAGE_ANALYSTS
        or app_config.LLM_STAGE_BULLISH
        or app_config.LLM_STAGE_BEARISH
        or app_config.LLM_STAGE_DEBATE
    ):
        return PIPELINE_MAX_SECONDS_LLM
    return PIPELINE_MAX_SECONDS_RULE


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_returns_valid_report(env_pipeline_result) -> None:
    report, _data, _analyses = env_pipeline_result

    price = report["metrics"]["current_price"]
    assert 1800 < price < 5000, f"price out of range: {price}"

    steps = report.get("meta", {}).get("generation_steps", [])
    assert len(steps) >= 8
    assert all(s.get("status") in ("done", "skipped") for s in steps), steps

    for key in ("meta", "metrics", "signals", "conclusion", "sentiment"):
        assert key in report


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_multi_timeframe_data(env_pipeline_result) -> None:
    _report, data, analyses = env_pipeline_result

    for tf in EXPECTED_TFS:
        assert tf in data and len(data[tf]) > 50, tf
        assert tf in analyses and analyses[tf].trend is not None, tf


@pytest.mark.slow
@pytest.mark.integration
def test_report_price_matches_5m_close(env_pipeline_result) -> None:
    """IND-01: metrics.current_price 与 5m 最新 Close 近似一致."""
    report, data, _ = env_pipeline_result

    price = report["metrics"]["current_price"]
    close_5m = float(data["5m"]["Close"].iloc[-1])
    tolerance = max(REALTIME_PRICE_ABS_TOLERANCE, close_5m * REALTIME_PRICE_PCT_TOLERANCE)
    diff = abs(price - close_5m)
    assert diff <= tolerance, (
        f"metrics {price} vs 5m close {close_5m} "
        f"(diff {diff:.4f}, tolerance {tolerance:.4f})"
    )


@pytest.mark.slow
@pytest.mark.integration
def test_report_signals_complete(env_pipeline_result) -> None:
    """IT-03 / IND-33: signals 含 entry/stop/take_profits."""
    report, _, _ = env_pipeline_result

    signals = report.get("signals", [])
    assert signals, "expected at least one trading signal"
    for sig in signals:
        for key in ("entry_low", "entry_high", "stop_loss", "take_profits", "direction"):
            assert key in sig, sig


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_duration_within_limit() -> None:
    """IT-04 / PERF-01: 首次流水线耗时 ≤ 320s（hybrid+LLM 实测 260–310s）."""
    reporter = ProgressReporter()
    token = set_progress(reporter)
    t0 = time.perf_counter()
    try:
        run_analysis()
    finally:
        reset_progress(token)
    elapsed = time.perf_counter() - t0
    limit = _pipeline_max_seconds()
    assert elapsed <= limit, f"pipeline took {elapsed:.1f}s (limit {limit}s)"
