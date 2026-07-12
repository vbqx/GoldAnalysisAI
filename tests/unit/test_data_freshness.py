"""Data freshness contract tests."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from src.analysis.data_freshness import build_data_as_of


def test_weekend_marks_closed_snapshot() -> None:
    idx = pd.date_range("2026-07-10 20:00", periods=10, freq="5min", tz="UTC")
    df = pd.DataFrame({"Close": [4200.0] * 10}, index=idx)
    now = datetime(2026, 7, 12, 6, 0, tzinfo=timezone.utc)  # Sunday
    meta = build_data_as_of({"5m": df}, now=now)
    assert meta["market_status"] == "closed_snapshot"
    assert meta["executable"] is False
    assert meta["warnings"]
