"""Unit tests for DGT price action detection."""

from __future__ import annotations

import pandas as pd

from src.analysis.chart_sr_filters import visible_sr_price_lines
from src.analysis.dgt_price_action import (
    DEFAULT_LOOKBACK,
    PROFILE_LOOKBACK_MODE,
    analyze_dgt_price_action,
    build_volume_profile,
)
from src.analysis.price_action_facts import build_price_action_summaries, chart_sr_levels


def _make_bars(n: int = 120, *, base: float = 4200.0) -> pd.DataFrame:
    idx = pd.date_range("2026-01-01", periods=n, freq="5min")
    rows = []
    price = base
    for i in range(n):
        o = price
        c = price + (1 if i % 5 < 3 else -1)
        h = max(o, c) + 0.5
        l = min(o, c) - 0.5
        vol = 100 + (50 if i % 10 == 0 else 0)
        rows.append({"Open": o, "High": h, "Low": l, "Close": c, "Volume": vol})
        price = c
    return pd.DataFrame(rows, index=idx)


def test_volume_profile_finds_poc_in_range() -> None:
    df = _make_bars(200)
    profile = build_volume_profile(df)
    assert profile.poc is not None
    assert profile.vah is not None
    assert profile.val is not None
    assert profile.val <= profile.poc <= profile.vah


def test_consecutive_sr_detects_levels() -> None:
    df = _make_bars(150)
    result = analyze_dgt_price_action(df, "5m", lookback=150)
    assert result.volume_profile is not None
    assert isinstance(result.sr_levels, list)


def test_build_price_action_summaries_multi_tf() -> None:
    bars_5m = _make_bars(288)
    daily = pd.DataFrame(
        {
            "Open": [float(bars_5m["Open"].iloc[0])],
            "High": [float(bars_5m["High"].max())],
            "Low": [float(bars_5m["Low"].min())],
            "Close": [float(bars_5m["Close"].iloc[-1])],
            "Volume": [int(bars_5m["Volume"].sum())],
        },
        index=pd.DatetimeIndex([bars_5m.index[0]]),
    )
    data = {
        "5m": bars_5m,
        "15m": bars_5m.iloc[::3],
        "1h": bars_5m.iloc[::12],
        "4h": bars_5m.iloc[::48],
        "1d": daily,
    }
    summaries = build_price_action_summaries(data, lookback=120)
    assert "5m" in summaries
    assert "volume_profile" in summaries["5m"]
    assert "session" in summaries
    assert summaries["session"]["volume_profile"]["poc"] is not None
    assert isinstance(summaries["session"].get("sr_levels"), list)
    # Fixed-range contract (Pine VP), not chart Visible Range.
    assert summaries["5m"]["lookback_mode"] == PROFILE_LOOKBACK_MODE == "fixed"
    assert summaries["5m"]["lookback_requested"] == 120
    assert summaries["5m"]["lookback_bars"] <= 120
    defaulted = build_price_action_summaries(data)
    assert defaulted["15m"]["lookback_requested"] == DEFAULT_LOOKBACK
    assert defaulted["15m"]["lookback_mode"] == "fixed"


def test_htf_falls_back_to_native_tf_when_5m_coverage_short() -> None:
    """360×4h spans longer than available 5m → Fixed window still uses native 4h OHLC."""
    idx_4h = pd.date_range("2025-01-01", periods=360, freq="4h")
    rows_4h = []
    for i, _ in enumerate(idx_4h):
        # Early cluster 3900, late cluster 4100 — native 4h POC should include early weight.
        px = 3900.0 if i < 200 else 4100.0
        vol = 800 if i < 200 else 200
        rows_4h.append({"Open": px, "High": px + 1, "Low": px - 1, "Close": px, "Volume": vol})
    df_4h = pd.DataFrame(rows_4h, index=idx_4h)
    # Only last ~2 days of 5m — far short of 360×4h clock span.
    idx_5m = pd.date_range(idx_4h[-1] - pd.Timedelta(days=2), periods=400, freq="5min")
    df_5m = pd.DataFrame(
        {"Open": 4100.0, "High": 4101.0, "Low": 4099.0, "Close": 4100.0, "Volume": 50},
        index=idx_5m,
    )
    data = {"5m": df_5m, "15m": df_5m.iloc[::3], "1h": df_5m.iloc[::12], "4h": df_4h}
    summaries = build_price_action_summaries(data, lookback=360)
    assert summaries["4h"]["lookback_mode"] == "fixed"
    assert summaries["4h"]["lookback_requested"] == 360
    assert summaries["4h"]["lookback_bars"] == 360
    assert summaries["4h"]["profile_source"] == "native_tf"
    poc = summaries["4h"]["volume_profile"]["poc"]
    assert poc is not None
    assert abs(poc - 3900.0) < 30.0


def test_htf_volume_profile_uses_full_window_not_last_n_5m() -> None:
    """Higher-TF POC must span the HTF lookback clock range, not collapse to 5m lookback."""
    idx = pd.date_range("2026-01-01", periods=480, freq="5min")  # 40h
    rows = []
    for i in range(len(idx)):
        # Early heavy volume near 4000; recent heavy volume near 4100.
        if i < 240:
            o = c = 4000.0
            vol = 5000
        else:
            o = c = 4100.0
            vol = 5000
        rows.append({"Open": o, "High": o + 0.5, "Low": o - 0.5, "Close": c, "Volume": vol})
    bars_5m = pd.DataFrame(rows, index=idx)
    data = {
        "5m": bars_5m,
        "15m": bars_5m.iloc[::3],
        "1h": bars_5m.iloc[::12],
        "4h": bars_5m.iloc[::48],
    }
    # 5m lookback 120 bars (~10h) sees only the 4100 cluster.
    # 4h lookback covering all ~40h should still include the early 4000 cluster via 5m profile_bars.
    summaries = build_price_action_summaries(data, lookback=120)
    poc_5m = summaries["5m"]["volume_profile"]["poc"]
    poc_4h = summaries["4h"]["volume_profile"]["poc"]
    assert poc_5m is not None and poc_4h is not None
    assert abs(poc_5m - 4100.0) < 5.0
    assert abs(poc_4h - 4000.0) < 5.0 or abs(poc_4h - poc_5m) > 20.0


def test_session_pa_anchors_to_daily_open_not_utc_midnight() -> None:
    idx_5m = pd.date_range("2026-07-09 21:00", periods=240, freq="5min", tz="UTC")
    df_5m = pd.DataFrame(
        {
            "Open": 4100.0,
            "High": 4134.92,
            "Low": 4072.8,
            "Close": 4120.67,
            "Volume": 100,
        },
        index=idx_5m,
    )

    idx_1d = pd.DatetimeIndex([pd.Timestamp("2026-07-09 21:00", tz="UTC")])
    df_1d = pd.DataFrame(
        {"Open": [4054.4], "High": [4134.92], "Low": [4072.8], "Close": [4120.67], "Volume": [50000]},
        index=idx_1d,
    )
    from src.analysis.price_action_facts import _bars_for_latest_session_day, build_session_price_action_block

    session_bars = _bars_for_latest_session_day(df_5m, df_1d)
    assert session_bars.index[0] == pd.Timestamp("2026-07-09 21:00", tz="UTC")
    assert len(session_bars) == 240
    session = build_session_price_action_block(df_5m, df_1d)
    assert session is not None


def test_session_pa_skips_non_datetime_index() -> None:
    from src.analysis.price_action_facts import build_session_price_action_block

    df = pd.DataFrame({"Open": [1], "High": [2], "Low": [0.5], "Close": [1.5], "Volume": [1]})
    assert build_session_price_action_block(df, df) is None


def test_visible_sr_filters_to_plot_range() -> None:
    idx = pd.date_range("2026-01-01", periods=20, freq="5min")
    plot_df = pd.DataFrame(
        {"Open": 4200, "High": 4210, "Low": 4195, "Close": 4205, "Volume": 100},
        index=idx,
    )
    levels = [
        {
            "price": 4208.0,
            "kind": "consecutive_sr",
            "direction": "resistance",
            "time": idx[-1].isoformat(),
            "label": "量价连续阻力",
        },
        {
            "price": 4300.0,
            "kind": "consecutive_sr",
            "direction": "resistance",
            "time": idx[-1].isoformat(),
            "label": "远位阻力",
        },
    ]
    lines = visible_sr_price_lines(levels, plot_df)
    prices = {line["price"] for line in lines}
    assert 4208.0 in prices
    assert 4300.0 not in prices
    assert len(lines) <= 5
    assert lines
    assert all(line.get("title") for line in lines)
    assert all(line.get("hint") for line in lines)
    assert " " not in lines[0]["title"]


def test_chart_sr_levels_per_timeframe() -> None:
    report = {
        "price_action": {
            "5m": {"sr_levels": [{"price": 4200.0, "label": "支撑"}]},
            "4h": {"sr_levels": [{"price": 4300.0, "label": "阻力"}]},
        }
    }
    assert chart_sr_levels(report, "5m")[0]["price"] == 4200.0
    assert chart_sr_levels(report, "4h")[0]["price"] == 4300.0
    assert chart_sr_levels(report, "1h") == []
