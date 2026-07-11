"""Filter FVG/OB by the same visible candle range used on charts."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import FairValueGap, OrderBlock, TimeframeAnalysis

# Keep in sync with CHART_VARIANTS in lightweight_chart.py
STRIP_CHART_BARS = 32
MAIN_CHART_BARS = 360
STRATEGY_CHART_BARS = 52

MAX_OB_ZONES = 5
MAX_FVG_ZONES = 8


def chart_plot_df(df: pd.DataFrame, bars: int) -> pd.DataFrame:
    return df.tail(max(1, bars)).copy()


def chart_price_bounds(plot_df: pd.DataFrame) -> tuple[float, float]:
    return float(plot_df["Low"].min()), float(plot_df["High"].max())


def zone_overlaps_chart_range(low: float, high: float, plot_df: pd.DataFrame) -> bool:
    """True when zone overlaps the high/low span of visible candles."""
    lo, hi = (low, high) if low <= high else (high, low)
    ymin, ymax = chart_price_bounds(plot_df)
    return lo <= ymax and hi >= ymin


def _align_ts(ts: pd.Timestamp, ref_index: pd.DatetimeIndex) -> pd.Timestamp:
    t = pd.Timestamp(ts)
    if ref_index.tz is not None:
        if t.tzinfo is None:
            return t.tz_localize(ref_index.tz)
        return t.tz_convert(ref_index.tz)
    if t.tzinfo is not None:
        return t.tz_convert(None)
    return t


def visible_order_blocks(
    analysis: TimeframeAnalysis,
    plot_df: pd.DataFrame,
    *,
    max_zones: int = MAX_OB_ZONES,
) -> list[OrderBlock]:
    t_max = plot_df.index.max()
    visible = [
        o
        for o in analysis.order_blocks
        if _align_ts(o.time, plot_df.index) <= t_max
        and zone_overlaps_chart_range(float(o.low), float(o.high), plot_df)
    ]
    visible.sort(key=lambda o: o.time, reverse=True)
    return visible[:max_zones]


def visible_active_fvgs(
    analysis: TimeframeAnalysis,
    plot_df: pd.DataFrame,
    *,
    max_zones: int = MAX_FVG_ZONES,
) -> list[FairValueGap]:
    t_max = plot_df.index.max()
    visible = [
        f
        for f in analysis.active_fvgs
        if _align_ts(f.time, plot_df.index) <= t_max
        and zone_overlaps_chart_range(float(f.low), float(f.high), plot_df)
    ]
    visible.sort(key=lambda f: f.time, reverse=True)
    return visible[:max_zones]


def visible_zone_snapshots(
    analysis: TimeframeAnalysis,
    plot_df: pd.DataFrame,
    *,
    ob_limit: int = MAX_OB_ZONES,
    fvg_limit: int = MAX_FVG_ZONES,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Dict snapshots for report text — same rules as chart overlays."""
    order_blocks = [
        {"low": ob.low, "high": ob.high, "direction": ob.direction}
        for ob in visible_order_blocks(analysis, plot_df, max_zones=ob_limit)
    ]
    fvgs = [
        {"low": fvg.low, "high": fvg.high, "direction": fvg.direction}
        for fvg in visible_active_fvgs(analysis, plot_df, max_zones=fvg_limit)
    ]
    return order_blocks, fvgs


def visible_zones_for_chart(
    analysis: TimeframeAnalysis,
    df: pd.DataFrame,
    *,
    bars: int,
    ob_limit: int = MAX_OB_ZONES,
    fvg_limit: int = MAX_FVG_ZONES,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    plot_df = chart_plot_df(df, bars)
    return visible_zone_snapshots(analysis, plot_df, ob_limit=ob_limit, fvg_limit=fvg_limit)
