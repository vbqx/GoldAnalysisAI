"""Integration tests — full pipeline (IT-01 ~ IT-04, IND-01, IND-33)."""
from __future__ import annotations

import time

import pytest

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.pipeline import run_analysis

EXPECTED_TFS = ("5m", "15m", "1h", "4h", "1d")
PIPELINE_MAX_SECONDS = 240


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_returns_valid_report() -> None:
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        report, data, analyses = run_analysis()
    finally:
        reset_progress(token)

    price = report["metrics"]["current_price"]
    assert 1800 < price < 5000, f"price out of range: {price}"

    steps = report.get("meta", {}).get("generation_steps", [])
    assert len(steps) >= 8
    assert all(s.get("status") == "done" for s in steps), steps

    for key in ("meta", "metrics", "signals", "conclusion", "sentiment"):
        assert key in report


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_multi_timeframe_data() -> None:
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        _, data, analyses = run_analysis()
    finally:
        reset_progress(token)

    for tf in EXPECTED_TFS:
        assert tf in data and len(data[tf]) > 50, tf
        assert tf in analyses and analyses[tf].trend is not None, tf


@pytest.mark.slow
@pytest.mark.integration
def test_report_price_matches_5m_close() -> None:
    """IND-01: metrics.current_price 与 5m 最新 Close 一致."""
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        report, data, _ = run_analysis()
    finally:
        reset_progress(token)

    price = report["metrics"]["current_price"]
    close_5m = float(data["5m"]["Close"].iloc[-1])
    assert abs(price - close_5m) <= 0.01, f"metrics {price} vs 5m close {close_5m}"


@pytest.mark.slow
@pytest.mark.integration
def test_report_signals_complete() -> None:
    """IT-03 / IND-33: signals 含 entry/stop/take_profits."""
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        report, _, _ = run_analysis()
    finally:
        reset_progress(token)

    signals = report.get("signals", [])
    assert signals, "expected at least one trading signal"
    for sig in signals:
        for key in ("entry_low", "entry_high", "stop_loss", "take_profits", "direction"):
            assert key in sig, sig


@pytest.mark.slow
@pytest.mark.integration
def test_pipeline_duration_within_limit() -> None:
    """IT-04 / PERF-01: 首次流水线耗时 ≤ 240s."""
    reporter = ProgressReporter()
    token = set_progress(reporter)
    t0 = time.perf_counter()
    try:
        run_analysis()
    finally:
        reset_progress(token)
    elapsed = time.perf_counter() - t0
    assert elapsed <= PIPELINE_MAX_SECONDS, f"pipeline took {elapsed:.1f}s"
