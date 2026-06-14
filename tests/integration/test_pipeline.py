"""Integration tests — full pipeline (IT-01, IT-02)."""
from __future__ import annotations

import pytest

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.pipeline import run_analysis

EXPECTED_TFS = ("5m", "15m", "1h", "4h", "1d")


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
