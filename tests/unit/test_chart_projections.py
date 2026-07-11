"""Chart projection overlay tests."""

from __future__ import annotations

import pandas as pd

from src.analysis.chart_zone_filters import visible_active_fvgs, visible_order_blocks
from src.analysis.ict_pa import FairValueGap, OrderBlock, StructureEvent, TimeframeAnalysis
from src.analysis.report_engine import trend_projections
from src.analysis.technical_context import structure_narrative
from src.viz.lightweight_chart import (
    _build_projections,
    _ob_display_end_time,
    _serialize_overlays,
    _zone_box_data,
    _zone_future_end,
    _zone_title,
    build_lightweight_chart_html,
)


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
    html = build_lightweight_chart_html(
        df, report=report, timeframe="5m", variant="main", show_projections=True
    )
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


def test_main_variant_hides_projection_lines() -> None:
    """5m main chart: structure/S&R only — no dashed path overlays."""
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
        ),
        "chart": {"swing_low": 4121.95, "swing_high": 4210.69},
    }
    analysis = TimeframeAnalysis(
        "5m", "bearish", "—", "—", swing_high=4210.69, swing_low=4121.95
    )
    html = build_lightweight_chart_html(
        df, analysis=analysis, report=report, timeframe="5m", variant="main"
    )
    assert '"projections": []' in html


def test_explicit_projection_flag_overrides_main_variant_default() -> None:
    """Callers can opt the main chart back into dashed path overlays."""
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
        ),
        "chart": {"swing_low": 4121.95, "swing_high": 4210.69},
    }
    analysis = TimeframeAnalysis(
        "5m", "bearish", "—", "—", swing_high=4210.69, swing_low=4121.95
    )
    html = build_lightweight_chart_html(
        df,
        analysis=analysis,
        report=report,
        timeframe="5m",
        variant="main",
        show_projections=True,
    )
    assert '"projections": [{"color":' in html


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


def test_zone_titles_same_timeframe_only() -> None:
    """Chart overlays use the chart TF only — no 4H demand or 15M markers on 5m."""
    idx = pd.date_range("2026-06-20 08:00", periods=80, freq="5min")
    plot_df = pd.DataFrame(
        {
            "Open": [4150.0] * 80,
            "High": [4162.0] * 80,
            "Low": [4140.0] * 80,
            "Close": [4155.0] * 80,
            "Volume": [100] * 80,
        },
        index=idx,
    )
    report = {
        "chart": {
            "swing_low": 4148.0,
            "swing_high": 4210.69,
            "swing_tf": "4h",
            "swing_atr": 18.0,
            "exec_atr": 4.0,
            "macro_atr": 8.0,
        }
    }
    analysis_5m = TimeframeAnalysis(
        "5m",
        "bearish",
        "—",
        "—",
        order_blocks=[OrderBlock(4168.0, 4160.0, "bearish", idx[40])],
        active_fvgs=[FairValueGap(4165.0, 4158.0, "bearish", idx[35])],
        atr=4.0,
    )
    overlays = _serialize_overlays(
        analysis_5m,
        report,
        plot_df,
        timeframe="5m",
        include_projections=False,
        variant="main",
    )
    titles = [z["title"] for z in overlays["zones"] if z.get("title")]
    assert all(t.startswith("[5M]") for t in titles)
    assert not any("需求/流动性区" in t for t in titles)
    assert "markers" not in overlays
    assert "structureLines" not in overlays
    assert any("看跌 FVG" in t for t in titles)
    assert any("看跌 OB" in t for t in titles)


def test_zone_box_extends_beyond_last_candle() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=80, freq="5min")
    plot_df = pd.DataFrame(
        {
            "Open": [4150.0] * 80,
            "High": [4162.0] * 80,
            "Low": [4140.0] * 80,
            "Close": [4155.0] * 80,
            "Volume": [100] * 80,
        },
        index=idx,
    )
    start = idx[35]
    end = _zone_future_end(plot_df, start)
    data = _zone_box_data(plot_df, start, 4165.0, end_time=end)

    assert len(data) == 2
    assert data[-1]["time"] > int(idx[-1].timestamp())


def test_ob_zone_extends_to_future_like_lux() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=100, freq="5min")
    plot_df = pd.DataFrame(
        {
            "Open": [4150.0] * 100,
            "High": [4162.0] * 100,
            "Low": [4140.0] * 100,
            "Close": [4155.0] * 100,
            "Volume": [100] * 100,
        },
        index=idx,
    )
    end = _ob_display_end_time(plot_df)

    assert end > idx[-1]


def test_structure_narrative_prefers_internal_scope() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=80, freq="5min")
    analysis = TimeframeAnalysis(
        "1h",
        "bullish",
        "bullish @ 4096",
        "无",
        swing_high=4203.0,
        swing_low=4022.0,
        premium_discount="premium",
        events=[
            StructureEvent("CHoCH", "bullish", 4095.99, idx[50], scope="internal"),
            StructureEvent("BOS", "bearish", 4140.0, idx[40], scope="swing"),
        ],
    )
    text = structure_narrative(analysis)
    assert "内结构 BOS 未见" in text or "内结构 BOS 无" in text
    assert "CHoCH bullish @ 4095.99" in text or "CHoCH 内结构看涨 @ 4095" in text
    assert "摆结构" in text


def test_visible_zone_snapshots_filter_obs_and_fvgs_by_chart_price_range() -> None:
    from src.viz.lightweight_chart import CHART_VARIANTS

    from src.analysis.chart_zone_filters import visible_zones_for_chart

    strip_bars = int(CHART_VARIANTS["strip"]["bars"])
    idx = pd.date_range("2026-06-20 08:00", periods=80, freq="1h")
    lows = [4140.0 + (i % 5) for i in range(80)]
    highs = [low + 20 for low in lows]
    df = pd.DataFrame(
        {
            "Open": lows,
            "High": highs,
            "Low": lows,
            "Close": [low + 10 for low in lows],
            "Volume": [100] * 80,
        },
        index=idx,
    )
    analysis = TimeframeAnalysis(
        "1h",
        "bullish",
        "无",
        "无",
        order_blocks=[
            OrderBlock(4330.0, 4310.0, "bearish", idx[70]),
            OrderBlock(4160.0, 4145.0, "bullish", idx[60]),
        ],
        active_fvgs=[
            FairValueGap(4355.0, 4296.0, "bearish", idx[50]),
            FairValueGap(4165.0, 4155.0, "bullish", idx[40]),
        ],
        atr=8.0,
    )
    obs, fvgs = visible_zones_for_chart(analysis, df, bars=strip_bars)
    assert len(obs) == 1
    assert obs[0]["direction"] == "bullish"
    assert len(fvgs) == 1
    assert fvgs[0]["direction"] == "bullish"


def test_zone_title_prefix_helper() -> None:
    title = _zone_title("fvg", "bearish", 4158.0, 4165.0, source_tf="5m")
    assert title.startswith("[5M]")
    assert "看跌 FVG" in title


def test_visible_zones_filter_by_chart_price_range() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=80, freq="5min")
    plot_df = pd.DataFrame(
        {
            "Open": [4150.0] * 80,
            "High": [4162.0] * 80,
            "Low": [4140.0] * 80,
            "Close": [4155.0] * 80,
            "Volume": [100] * 80,
        },
        index=idx,
    )
    analysis = TimeframeAnalysis(
        "5m",
        "bearish",
        "—",
        "—",
        order_blocks=[
            OrderBlock(4160.0, 4156.0, "bearish", idx[70]),
            OrderBlock(4198.0, 4190.0, "bullish", idx[60]),
            OrderBlock(3975.0, 3971.0, "bullish", idx[50]),
            OrderBlock(4172.0, 4168.0, "bearish", idx[45]),
            OrderBlock(4148.0, 4144.0, "bullish", idx[40]),
            OrderBlock(4208.0, 4200.0, "bearish", idx[35]),
        ],
        active_fvgs=[
            FairValueGap(4165.0, 4158.0, "bearish", idx[35]),
            FairValueGap(4500.0, 4490.0, "bullish", idx[30]),
        ],
    )

    fvgs = visible_active_fvgs(analysis, plot_df)
    obs = visible_order_blocks(analysis, plot_df)

    assert len(fvgs) == 1
    assert fvgs[0].low == 4158.0
    assert len(obs) == 2
    assert {o.low for o in obs} == {4156.0, 4144.0}


def test_chart_order_blocks_limit_five_newest_mixed_directions() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=100, freq="5min")
    plot_df = pd.DataFrame(
        {
            "Open": [4150.0] * 100,
            "High": [4162.0] * 100,
            "Low": [4140.0] * 100,
            "Close": [4155.0] * 100,
            "Volume": [100] * 100,
        },
        index=idx,
    )
    analysis = TimeframeAnalysis(
        "5m",
        "bearish",
        "—",
        "—",
        order_blocks=[
            OrderBlock(4160.0, 4156.0, "bearish", idx[90]),
            OrderBlock(4158.0, 4154.0, "bearish", idx[80]),
            OrderBlock(4156.0, 4152.0, "bearish", idx[70]),
            OrderBlock(4154.0, 4150.0, "bullish", idx[60]),
            OrderBlock(4152.0, 4148.0, "bullish", idx[50]),
            OrderBlock(4150.0, 4146.0, "bullish", idx[40]),
        ],
    )

    obs = visible_order_blocks(analysis, plot_df)

    assert len(obs) == 5
    assert [o.time for o in obs] == [idx[90], idx[80], idx[70], idx[60], idx[50]]
