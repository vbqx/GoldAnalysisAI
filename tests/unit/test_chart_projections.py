"""Chart projection overlay tests."""

from __future__ import annotations

import pandas as pd

from src.analysis.report_engine import trend_projections
from src.viz.lightweight_chart import _build_projections, build_lightweight_chart_html


def test_projection_step_gap_on_5m() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=100, freq="5min")
    df = pd.DataFrame(
        {
            "Open": [4150.0] * 100,
            "High": [4160.0] * 100,
            "Low": [4140.0] * 100,
            "Close": [4155.4] * 100,
            "Volume": [100] * 100,
        },
        index=idx,
    )
    report = {
        "projections": trend_projections(
            4155.4, 4210.69, 4121.95, {"bearish": 45, "bullish": 25, "ranging": 30}
        )
    }
    lines = _build_projections(df, report, timeframe="5m")
    assert len(lines) == 3
    pts = lines[0]["data"]
    assert pts[0]["value"] == 4155.4
    assert pts[1]["time"] - pts[0]["time"] == 3 * 3600


def test_projection_lines_share_candle_price_scale() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=50, freq="5min")
    df = pd.DataFrame(
        {
            "Open": [4150.0] * 50,
            "High": [4160.0] * 50,
            "Low": [4140.0] * 50,
            "Close": [4155.4] * 50,
            "Volume": [100] * 50,
        },
        index=idx,
    )
    report = {
        "projections": trend_projections(
            4155.4, 4210.69, 4121.95, {"bearish": 45, "bullish": 25, "ranging": 30}
        )
    }
    html = build_lightweight_chart_html(df, report=report, timeframe="5m", variant="main")
    assert "priceScaleId: 'proj'" not in html
    assert "priceScale('proj')" not in html


def test_main_variant_hides_ema_macd_overlays() -> None:
    """IND-30: 5m 主图不绘制 EMA/MACD/RSI 副图线."""
    idx = pd.date_range("2026-06-20 08:00", periods=50, freq="5min")
    close = pd.Series(4155.4, index=idx)
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": 100,
            "EMA20": close * 0.99,
            "EMA50": close * 0.98,
            "EMA610": close * 0.97,
            "VWAP": close * 1.01,
        },
        index=idx,
    )
    html = build_lightweight_chart_html(df, timeframe="5m", variant="main")
    assert "const showIndicators = false" in html
    assert "let bodyHeight = 420" in html


def test_main_variant_includes_volume() -> None:
    """IND-30: 5m 主图保留成交量柱."""
    idx = pd.date_range("2026-06-20 08:00", periods=20, freq="5min")
    df = pd.DataFrame(
        {
            "Open": [4150.0] * 20,
            "High": [4160.0] * 20,
            "Low": [4140.0] * 20,
            "Close": [4155.4] * 20,
            "Volume": [100] * 20,
        },
        index=idx,
    )
    html = build_lightweight_chart_html(df, timeframe="5m", variant="main")
    assert "const showVolume = true" in html
