"""Unit tests for LuxAlgo SMC port (FVG, mitigation, structure)."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import analyze_timeframe
from src.analysis.luxalgo_smc import (
    INTERNAL_FILTER_CONFLUENCE,
    _internal_confluence_bars,
    _store_order_block,
    analyze_luxalgo,
)


def _make_df(rows: list[dict], *, freq: str = "5min") -> pd.DataFrame:
    idx = pd.date_range("2026-06-01", periods=len(rows), freq=freq)
    return pd.DataFrame(rows, index=idx)


def test_luxalgo_bullish_fvg_requires_close_confirmation() -> None:
    """Gap without close[1] > high[2] must not register as bullish FVG."""
    rows = [
        {"Open": 100.0, "High": 100.0, "Low": 99.0, "Close": 99.5, "Volume": 1},
        {"Open": 99.5, "High": 100.0, "Low": 99.0, "Close": 99.8, "Volume": 1},
        {"Open": 99.8, "High": 100.0, "Low": 99.0, "Close": 99.7, "Volume": 1},
        {"Open": 99.7, "High": 100.0, "Low": 99.0, "Close": 99.6, "Volume": 1},
        {"Open": 99.6, "High": 100.0, "Low": 99.0, "Close": 99.5, "Volume": 1},
        {"Open": 99.5, "High": 100.0, "Low": 99.0, "Close": 99.4, "Volume": 1},
        {"Open": 99.4, "High": 100.0, "Low": 99.0, "Close": 99.3, "Volume": 1},
        {"Open": 99.3, "High": 100.0, "Low": 99.0, "Close": 99.2, "Volume": 1},
        {"Open": 99.2, "High": 99.5, "Low": 98.5, "Close": 99.0, "Volume": 1},
        {"Open": 99.0, "High": 105.0, "Low": 104.0, "Close": 104.5, "Volume": 1},
    ]
    df = _make_df(rows)
    lux = analyze_luxalgo(df)
    assert not any(f.direction == "bullish" for f in lux.fvgs)


def test_luxalgo_bullish_fvg_mitigation_below_bottom() -> None:
    """Bullish FVG stays active until low < bottom (not top touch)."""
    rows = []
    for i in range(12):
        rows.append({"Open": 100.0, "High": 101.0, "Low": 99.5, "Close": 100.0, "Volume": 1})
    rows[5] = {"Open": 100.0, "High": 100.5, "Low": 99.0, "Close": 99.2, "Volume": 1}
    rows[6] = {"Open": 99.2, "High": 99.4, "Low": 98.8, "Close": 99.0, "Volume": 1}
    rows[7] = {"Open": 99.0, "High": 105.0, "Low": 104.0, "Close": 104.5, "Volume": 1}
    rows[8] = {"Open": 104.5, "High": 106.0, "Low": 105.5, "Close": 105.8, "Volume": 1}
    rows[9] = {"Open": 105.8, "High": 106.2, "Low": 105.0, "Close": 105.5, "Volume": 1}
    rows[10] = {"Open": 105.5, "High": 105.8, "Low": 104.8, "Close": 105.0, "Volume": 1}
    rows[11] = {"Open": 105.0, "High": 105.2, "Low": 103.5, "Close": 104.0, "Volume": 1}
    df = _make_df(rows)
    lux = analyze_luxalgo(df)
    bull = [f for f in lux.active_fvgs if f.direction == "bullish"]
    assert bull, "expected at least one active bullish FVG before full mitigation"


def test_analyze_timeframe_uses_luxalgo_swings_not_global_min() -> None:
    idx = pd.date_range("2026-06-01", periods=36, freq="5min")
    high = [
        100, 103, 106, 110, 105, 102, 99, 96, 94, 97, 101, 104,
        108, 112, 109, 106, 103, 101, 99, 98, 101, 104, 107, 109,
        106, 103, 100, 98, 96, 95, 97, 100, 103, 105, 104, 103,
    ]
    low = [x - 2 for x in high]
    low[8] = 70
    df = pd.DataFrame(
        {
            "Open": high,
            "High": high,
            "Low": low,
            "Close": [(h + l) / 2 for h, l in zip(high, low)],
            "Volume": [100] * len(high),
        },
        index=idx,
    )
    analysis = analyze_timeframe(df, "5m")
    assert analysis.swing_low is None or analysis.swing_low != 70


def test_internal_structure_default_skips_confluence_filter() -> None:
    """Lux default has Confluence Filter off — wick-only bars can still break internal structure."""
    from src.analysis.luxalgo_smc import INTERNAL_FILTER_CONFLUENCE

    assert INTERNAL_FILTER_CONFLUENCE is False


def test_analyze_timeframe_exposes_events_and_obs() -> None:
    idx = pd.date_range("2026-01-01", periods=120, freq="5min")
    base = 2000.0
    highs, lows, opens, closes = [], [], [], []
    for i in range(120):
        wave = 5 * (i % 7 - 3)
        o = base + wave
        c = o + (1 if i % 2 == 0 else -1)
        h = max(o, c) + 2
        l = min(o, c) - 2
        opens.append(o)
        closes.append(c)
        highs.append(h)
        lows.append(l)
        base += 0.05
    df = pd.DataFrame(
        {"Open": opens, "High": highs, "Low": lows, "Close": closes, "Volume": [10] * 120},
        index=idx,
    )
    analysis = analyze_timeframe(df, "5m")
    assert analysis.trend in ("bullish", "bearish", "ranging")
    assert isinstance(analysis.order_blocks, list)
    assert isinstance(analysis.active_fvgs, list)


def test_store_order_block_matches_pine_slice_excluding_breakout_bar() -> None:
    idx = pd.date_range("2026-06-01", periods=5, freq="5min")
    ob = _store_order_block(
        parsed_highs=[101.0, 103.0, 102.0, 110.0, 104.0],
        parsed_lows=[99.0, 98.0, 97.0, 96.0, 95.0],
        times=list(idx),
        pivot_index=1,
        current_index=3,
        bias="bearish",
    )

    assert ob is not None
    assert ob.high == 103.0
    assert ob.time == idx[1]
