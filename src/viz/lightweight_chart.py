"""TradingView Lightweight Charts renderer with SMC overlays."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from src.analysis.chart_sr_filters import _SR_CHART_TIMEFRAMES, visible_sr_price_lines
from src.analysis.chart_zone_filters import (
    MAX_FVG_ZONES,
    MAX_OB_ZONES,
    visible_active_fvgs,
    visible_order_blocks,
)
from src.analysis.ict_pa import TimeframeAnalysis
from src.analysis.price_action_facts import chart_sr_levels

LINE_COLORS = {
    "EMA20": "#a855f7",
    "EMA50": "#eab308",
    "EMA610": "#ef4444",
    "VWAP": "#3b82f6",
}
# LuxAlgo SMC default colors (Pine: fairValueGaps / internal OB)
LUX_FVG_BULL = {"fill": "rgba(0,255,104,0.30)", "border": "rgba(0,255,104,0.55)", "label": "#00a85c"}
LUX_FVG_BEAR = {"fill": "rgba(255,0,8,0.30)", "border": "rgba(255,0,8,0.55)", "label": "#cc0006"}
LUX_OB_BULL = {"fill": "rgba(49,121,245,0.22)", "border": "rgba(49,121,245,0.50)", "label": "#2563eb"}
LUX_OB_BEAR = {"fill": "rgba(247,124,128,0.22)", "border": "rgba(247,124,128,0.50)", "label": "#e11d48"}

_PROJECTION_STEP_GAP: dict[str, pd.Timedelta] = {
    "5m": pd.Timedelta(hours=3),
    "15m": pd.Timedelta(hours=6),
    "1h": pd.Timedelta(hours=12),
    "4h": pd.Timedelta(days=1),
    "1d": pd.Timedelta(days=5),
}

TF_LABELS = {
    "5m": "5min周期 (执行结构)",
    "15m": "15min周期 (中间结构)",
    "1h": "1H周期 (宏观结构)",
    "4h": "4H周期 (宏观结构)",
    "1d": "日线周期 (主结构)",
}

TF_SHORT = {
    "5m": "5M",
    "15m": "15M",
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}

CHART_VARIANTS: dict[str, dict[str, Any]] = {
    "main": {
        "height": 420,
        "bars": 360,
        "volume": True,
        "overlay_header": True,
        "line_labels": False,
        "zone_labels": True,
        "show_indicators": False,
        "show_projections": False,
        "top_margin": 0.08,
        "bottom_margin": 0.22,
        "header_lines": 3,
    },
    "mini": {
        "height": 172,
        "bars": 40,
        "volume": False,
        "overlay_header": False,
        "line_labels": False,
        "zone_labels": False,
        "show_indicators": False,
        "show_overlays": False,
        "top_margin": 0.06,
        "bottom_margin": 0.05,
        "header_lines": 1,
    },
    "strip": {
        "height": 120,
        "bars": 32,
        "volume": False,
        "overlay_header": False,
        "line_labels": False,
        "zone_labels": False,
        "show_indicators": False,
        "show_overlays": False,
        "top_margin": 0.02,
        "bottom_margin": 0.02,
        "header_lines": 0,
        "aspect_ratio": 3.75,
        "min_height": 108,
        "max_height": 138,
    },
    "strategy": {
        "height": 292,
        "bars": 52,
        "volume": False,
        "overlay_header": False,
        "line_labels": False,
        "zone_labels": True,
        "show_indicators": False,
        "show_overlays": True,
        "top_margin": 0.07,
        "bottom_margin": 0.06,
        "header_lines": 1,
    },
}


def _tf_short(timeframe: str) -> str:
    return TF_SHORT.get(timeframe, timeframe.upper())


def _zone_title(
    kind: str,
    direction: str,
    low: float,
    high: float,
    *,
    half: str | None = None,
    source_tf: str | None = None,
) -> str:
    lo, hi = int(round(low)), int(round(high))
    if kind == "fvg":
        tag = "看涨 FVG" if direction == "bullish" else "看跌 FVG"
        base = f"{tag} {lo}-{hi}"
    else:
        tag = "看涨 OB" if direction == "bullish" else "看跌 OB"
        base = f"{tag} {lo}-{hi}"
    if half:
        base = f"{base} ({half})"
    if source_tf:
        return f"[{_tf_short(source_tf)}] {base}"
    return base


def _align_ts(ts: pd.Timestamp, ref_index: pd.DatetimeIndex) -> pd.Timestamp:
    t = pd.Timestamp(ts)
    if ref_index.tz is not None:
        if t.tzinfo is None:
            return t.tz_localize(ref_index.tz)
        return t.tz_convert(ref_index.tz)
    if t.tzinfo is not None:
        return t.tz_convert(None)
    return t


def _to_unix(ts: pd.Timestamp) -> int:
    return int(pd.Timestamp(ts).timestamp())


def _bar_delta(plot_df: pd.DataFrame) -> pd.Timedelta:
    if len(plot_df) < 2:
        return pd.Timedelta(hours=1)
    return plot_df.index[-1] - plot_df.index[-2]


def _zone_future_end(plot_df: pd.DataFrame, start_time: pd.Timestamp) -> pd.Timestamp:
    """Extend Lux zones/lines far to the right so panning does not clip them."""
    delta = _bar_delta(plot_df)
    extend_bars = max(len(plot_df) * 2, 240)
    return _align_ts(start_time, plot_df.index) + delta * extend_bars


def _zone_box_data(
    plot_df: pd.DataFrame,
    start_time: pd.Timestamp,
    high: float,
    *,
    end_time: pd.Timestamp | None = None,
) -> list[dict[str, float | int]]:
    """Lux-style band top line from start_time through end_time (may extend past last candle)."""
    t0 = _align_ts(start_time, plot_df.index)
    t1 = _align_ts(end_time or _zone_future_end(plot_df, t0), plot_df.index)
    if t0 > t1:
        t0 = t1
    val = round(high, 2)
    t_start_unix = _to_unix(t0)
    t_end_unix = _to_unix(t1)
    if t_start_unix == t_end_unix:
        return [{"time": t_start_unix, "value": val}]
    return [
        {"time": t_start_unix, "value": val},
        {"time": t_end_unix, "value": val},
    ]


def _ob_display_end_time(plot_df: pd.DataFrame) -> pd.Timestamp:
    """Lux draws each OB box to last_bar_time with extend.right."""
    return _zone_future_end(plot_df, plot_df.index[-1])


def _append_zone_box(
    zones: list[dict[str, Any]],
    *,
    kind: str,
    direction: str,
    low: float,
    high: float,
    start_time: pd.Timestamp,
    plot_df: pd.DataFrame,
    source_tf: str,
    colors: dict[str, str],
    title: str | None = None,
    show_label: bool = True,
    end_time: pd.Timestamp | None = None,
) -> None:
    if high < low:
        low, high = high, low
    zones.append(
        {
            "kind": kind,
            "title": title if show_label else "",
            "low": round(low, 2),
            "high": round(high, 2),
            "fill": colors["fill"],
            "border": colors["border"],
            "labelColor": colors["label"],
            "data": _zone_box_data(plot_df, start_time, high, end_time=end_time),
        }
    )


def _append_lux_fvg(
    zones: list[dict[str, Any]],
    fvg,
    plot_df: pd.DataFrame,
    source_tf: str,
) -> None:
    """Lux FVG: two stacked boxes split at midpoint, extending right until mitigated."""
    colors = LUX_FVG_BULL if fvg.direction == "bullish" else LUX_FVG_BEAR
    lo, hi = float(fvg.low), float(fvg.high)
    mid = (lo + hi) / 2
    end_time = _zone_future_end(plot_df, fvg.time)
    base_title = _zone_title("fvg", fvg.direction, lo, hi, source_tf=source_tf)
    _append_zone_box(
        zones,
        kind="fvg",
        direction=fvg.direction,
        low=mid,
        high=hi,
        start_time=fvg.time,
        plot_df=plot_df,
        source_tf=source_tf,
        colors=colors,
        title=f"{base_title} (上)",
        show_label=True,
        end_time=end_time,
    )
    _append_zone_box(
        zones,
        kind="fvg",
        direction=fvg.direction,
        low=lo,
        high=mid,
        start_time=fvg.time,
        plot_df=plot_df,
        source_tf=source_tf,
        colors=colors,
        title=f"{base_title} (下)",
        show_label=False,
        end_time=end_time,
    )


def _append_lux_ob(
    zones: list[dict[str, Any]],
    ob,
    plot_df: pd.DataFrame,
    source_tf: str,
    *,
    end_time: pd.Timestamp,
) -> None:
    colors = LUX_OB_BULL if ob.direction == "bullish" else LUX_OB_BEAR
    _append_zone_box(
        zones,
        kind="ob",
        direction=ob.direction,
        low=ob.low,
        high=ob.high,
        start_time=ob.time,
        plot_df=plot_df,
        source_tf=source_tf,
        colors=colors,
        title=_zone_title("ob", ob.direction, ob.low, ob.high, source_tf=source_tf),
        end_time=end_time,
    )


def _serialize_overlays(
    analysis: TimeframeAnalysis,
    report: dict[str, Any],
    plot_df: pd.DataFrame,
    *,
    timeframe: str = "1h",
    include_projections: bool = True,
    variant: str = "main",
) -> dict[str, Any]:
    """Build Lux-style zones for the chart's own timeframe only (no BOS/CHoCH overlays)."""
    chart_tf = analysis.timeframe
    if chart_tf != timeframe:
        timeframe = chart_tf

    price_lines: list[dict[str, Any]] = []
    zones: list[dict[str, Any]] = []

    for fvg in visible_active_fvgs(analysis, plot_df):
        _append_lux_fvg(zones, fvg, plot_df, chart_tf)

    visible_obs = visible_order_blocks(analysis, plot_df)
    ob_end = _ob_display_end_time(plot_df)
    for ob in visible_obs:
        _append_lux_ob(zones, ob, plot_df, chart_tf, end_time=ob_end)

    if report and chart_tf in _SR_CHART_TIMEFRAMES:
        levels = chart_sr_levels(report, chart_tf)
        if levels:
            price_lines.extend(
                visible_sr_price_lines(
                    levels,
                    plot_df,
                    current_price=float(plot_df["Close"].iloc[-1]),
                )
            )

    projections = (
        _build_projections(plot_df, report, timeframe=timeframe)
        if include_projections
        else []
    )
    return {
        "priceLines": price_lines,
        "zones": zones,
        "projections": projections,
    }


def _build_projections(
    plot_df: pd.DataFrame,
    report: dict[str, Any] | None,
    *,
    timeframe: str = "5m",
) -> list[dict[str, Any]]:
    """Future dashed path overlays — no probability labels (shown in path cards / Plotly only)."""
    if not report or "projections" not in report:
        return []

    last_ts = plot_df.index[-1]
    point_gap = _PROJECTION_STEP_GAP.get(timeframe, pd.Timedelta(hours=4))
    lines: list[dict[str, Any]] = []

    for proj in report["projections"]:
        points: list[dict[str, float | int]] = []
        t = last_ts
        for i, step_info in enumerate(proj["steps"]):
            if i > 0:
                t = t + point_gap
            points.append({"time": _to_unix(t), "value": round(float(step_info["price"]), 2)})
        if len(points) >= 2:
            lines.append({
                "color": proj["color"],
                "data": points,
            })
    return lines


def build_lightweight_chart_html(
    df: pd.DataFrame,
    analysis: TimeframeAnalysis | None = None,
    report: dict[str, Any] | None = None,
    *,
    timeframe: str = "1h",
    symbol: str = "XAUUSD",
    symbol_name: str = "黄金/美元",
    exchange: str = "OANDA",
    height: int | None = None,
    bars: int | None = None,
    variant: str = "main",
    watermark: str | None = None,
    show_projections: bool | None = None,
) -> str:
    """Build HTML/JS for TradingView Lightweight Charts with volume + SMC zones."""
    preset = CHART_VARIANTS.get(variant, CHART_VARIANTS["main"])
    height = height if height is not None else int(preset["height"])
    bars = bars if bars is not None else int(preset["bars"])
    show_volume = bool(preset["volume"])
    overlay_header = bool(preset["overlay_header"])
    show_line_labels = bool(preset["line_labels"])
    show_zone_labels = bool(preset["zone_labels"])
    show_indicators = bool(preset.get("show_indicators", True))
    if show_projections is None:
        show_projections = bool(preset.get("show_projections", True))
    show_overlays = bool(preset.get("show_overlays", True))
    top_margin = float(preset["top_margin"])
    bottom_margin = float(preset["bottom_margin"])
    header_lines = int(preset["header_lines"])
    strip_max_h = int(preset.get("max_height", height)) if variant == "strip" else height
    strip_min_h = int(preset.get("min_height", height)) if variant == "strip" else height
    strip_aspect = float(preset.get("aspect_ratio", 3.75)) if variant == "strip" else 0.0

    plot_df = df.tail(bars).copy()
    last = plot_df.iloc[-1]
    prev = plot_df.iloc[-2] if len(plot_df) > 1 else last
    o, h, l, c = float(last["Open"]), float(last["High"]), float(last["Low"]), float(last["Close"])
    chg = c - float(prev["Close"])
    chg_pct = (chg / float(prev["Close"]) * 100) if float(prev["Close"]) else 0.0
    chg_sign = "+" if chg >= 0 else ""
    chg_cls = "up" if chg >= 0 else "down"

    tf_label = TF_LABELS.get(timeframe, f"{timeframe}周期")
    if variant == "main" and timeframe == "5m":
        tf_label = "5min周期 (主图)"
    tf_num = {"5m": "5", "15m": "15", "1h": "60", "4h": "240", "1d": "D"}.get(timeframe, timeframe)

    smc_note = ""
    if analysis is not None:
        pd_label = {"premium": "溢价区", "discount": "折价区", "equilibrium": "均衡", "unknown": "—"}.get(
            analysis.premium_discount, "—"
        )
        smc_note = f"聪明钱: {pd_label} | 成交量: {analysis.volume_signal}"

    candles: list[dict[str, float | int]] = []
    volumes: list[dict[str, float | int]] = []
    for idx, row in plot_df.iterrows():
        ts = _to_unix(idx)
        o, h, l, c = float(row["Open"]), float(row["High"]), float(row["Low"]), float(row["Close"])
        candles.append({"time": ts, "open": round(o, 2), "high": round(h, 2), "low": round(l, 2), "close": round(c, 2)})
        vol = float(row.get("Volume", 0) or 0)
        volumes.append({"time": ts, "value": vol, "color": "rgba(34,197,94,0.5)" if c >= o else "rgba(239,68,68,0.5)"})

    line_series: dict[str, dict[str, Any]] = {}
    if show_indicators:
        for col, color in LINE_COLORS.items():
            if col not in plot_df.columns:
                continue
            points: list[dict[str, float | int]] = []
            for idx, row in plot_df.iterrows():
                val = row[col]
                if pd.notna(val):
                    points.append({"time": _to_unix(idx), "value": round(float(val), 2)})
            if points:
                line_series[col] = {"color": color, "data": points}

    overlays = (
        _serialize_overlays(
            analysis, report, plot_df, timeframe=timeframe,
            include_projections=show_projections, variant=variant,
        )
        if analysis is not None and report is not None and show_overlays
        else {"priceLines": [], "zones": [], "projections": []}
    )

    last_bar = candles[-1] if candles else {"open": 0, "high": 0, "low": 0, "close": 0}
    last_o, last_h, last_l, last_c = last_bar["open"], last_bar["high"], last_bar["low"], last_bar["close"]
    if header_lines == 1:
        default_ohlc_html = (
            f"{tf_label} · {symbol} 收={last_c:.2f} "
            f"<span class=\"{chg_cls}\" style=\"font-weight:700;\">{chg_sign}{chg:.2f} ({chg_sign}{chg_pct:.2f}%)</span>"
        )
    else:
        default_ohlc_html = (
            f"【{tf_label}】 {symbol} {symbol_name} · {tf_num} · {exchange} "
            f"开={last_o:.2f} 高={last_h:.2f} 低={last_l:.2f} 收={last_c:.2f} "
            f"<span class=\"{chg_cls}\" style=\"font-weight:700;\">{chg_sign}{chg:.2f} ({chg_sign}{chg_pct:.2f}%)</span>"
        )

    legend_html = ""
    if header_lines >= 3:
        price_legend = ""
        if show_indicators:
            price_legend = """
    <div style="font-size:11px;color:#64748b;margin-top:1px;">
      <span style="color:#a855f7;">EMA20(紫)</span>
      <span style="margin-left:8px;color:#eab308;">EMA50(黄)</span>
      <span style="margin-left:8px;color:#3b82f6;">VWAP(蓝)</span>
      <span style="margin-left:8px;color:#ef4444;">EMA610(红)</span>
    </div>"""
        elif show_zone_labels and variant == "main":
            price_legend = """
    <div style="font-size:11px;color:#64748b;margin-top:1px;">
      5m 主图仅绘制 FVG/OB 色块；BOS/CHoCH/EQH/EQL/H/L 见多周期条带下方文字
    </div>"""
        legend_html = f"""{price_legend}
    <div style="font-size:11px;color:#94a3b8;margin-top:1px;">{smc_note}</div>"""

    header_inner = f'<div id="tv-ohlc-line" class="tv-ohlc-line">{default_ohlc_html}</div>{legend_html}'
    overlay_cls = " overlay" if overlay_header else ""
    show_header = overlay_header or header_lines >= 3
    header_html = f'<div id="tv-chart-header" class="tv-chart-header{overlay_cls}">{header_inner}</div>' if show_header else ""

    wm = watermark or ""
    wm_size = "28px" if variant == "main" else ("14px" if variant == "strip" else "18px")
    wm_html = (
        f'<div style="position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);'
        f'font-size:{wm_size};font-weight:700;color:rgba(148,163,184,0.22);pointer-events:none;'
        f'z-index:12;white-space:nowrap;letter-spacing:2px;">{wm}</div>'
        if wm else ""
    )

    candles_json = json.dumps(candles)
    volumes_json = json.dumps(volumes)
    lines_json = json.dumps(line_series)
    overlays_json = json.dumps(overlays)
    volume_margins_json = json.dumps({"top": 0.78, "bottom": 0})
    seconds_visible = timeframe == "5m"
    candle_times_json = json.dumps([c["time"] for c in candles])
    candle_map_json = json.dumps({c["time"]: c for c in candles})
    zone_font = "11px" if variant == "main" else ("9px" if variant == "strip" else "10px")
    zone_right = "78px" if variant == "main" else ("48px" if variant == "strip" else "62px")
    scale_min_width = 72 if variant == "main" else (44 if variant == "strip" else 56)

    body_parts = [header_html] if overlay_header else []
    body_parts.extend([
        f'<div id="zone-labels" style="position:absolute;left:0;top:0;bottom:0;right:{scale_min_width}px;pointer-events:none;z-index:15;overflow:hidden;"></div>',
        f'<div id="sr-hover-tip" style="position:absolute;pointer-events:none;z-index:25;display:none;"></div>',
        wm_html,
        f'<div id="tv-chart-container" style="width:100%;height:{height}px;touch-action:none;"></div>',
    ])
    body_html = "\n  ".join(body_parts)

    outer_header = header_html if not overlay_header else ""

    return f"""
<div class="tv-chart-wrap tv-{variant}" style="position:relative;width:100%;font-family:system-ui,-apple-system,sans-serif;">
  {outer_header}
  <div class="tv-chart-body" style="position:relative;">
  {body_html}
  </div>
</div>
<style>
  .tv-chart-wrap .up {{ color:#16a34a; }}
  .tv-chart-wrap .down {{ color:#dc2626; }}
  .tv-chart-header {{ padding:6px 10px 4px; line-height:1.4; pointer-events:none; background:#fff; }}
  .tv-chart-header.overlay {{ position:absolute; top:0; left:0; right:0; z-index:20; }}
  .tv-chart-wrap.tv-mini .tv-chart-header,
  .tv-chart-wrap.tv-strategy .tv-chart-header {{ border:none; border-radius:0; background:transparent; padding:4px 10px 2px; }}
  .tv-chart-wrap.tv-strip {{ margin:0; padding:0; line-height:0; }}
  .tv-chart-wrap.tv-strip .tv-chart-header {{ border:none; border-radius:0; background:transparent; padding:0; margin:0; height:0; overflow:hidden; }}
  .tv-chart-wrap.tv-mini .tv-ohlc-line,
  .tv-chart-wrap.tv-strategy .tv-ohlc-line {{ font-size:11px; color:#334155; font-weight:600; }}
  .tv-chart-wrap.tv-strip .tv-ohlc-line {{ font-size:9px; color:#64748b; font-weight:600; line-height:1.15; }}
  .tv-chart-wrap.tv-main .tv-ohlc-line {{ font-size:12px; color:#334155; font-weight:600; }}
  .tv-chart-wrap.tv-mini .tv-chart-body,
  .tv-chart-wrap.tv-strategy .tv-chart-body {{ border:1px solid #e2e8f0; border-radius:0 0 6px 6px; overflow:hidden; }}
  .tv-chart-wrap.tv-strip .tv-chart-body {{ border:none; border-radius:0; overflow:hidden; padding:0; margin:0; }}
  .zone-label {{
    position:absolute;
    right:{zone_right};
    transform:translateY(-50%);
    font-size:{zone_font};
    font-weight:600;
    color:#334155;
    background:rgba(255,255,255,0.92);
    padding:2px 6px 2px 4px;
    border-left:3px solid var(--zone-color, #94a3b8);
    white-space:nowrap;
    box-shadow:0 1px 2px rgba(15,23,42,0.06);
  }}
  .sr-hover-tip {{
    padding:2px 7px 2px 5px;
    font-size:{"10px" if variant == "strip" else "11px"};
    font-weight:600;
    color:#334155;
    background:rgba(255,255,255,0.96);
    border-left:3px solid var(--sr-color, #64748b);
    white-space:nowrap;
    box-shadow:0 1px 3px rgba(15,23,42,0.12);
    transform:translateY(-50%);
  }}
</style>
<script src="https://unpkg.com/lightweight-charts@4.2.0/dist/lightweight-charts.standalone.production.js"></script>
<script>
(function() {{
  const container = document.getElementById('tv-chart-container');
  const labelsEl = document.getElementById('zone-labels');
  const srTipEl = document.getElementById('sr-hover-tip');
  const ohlcEl = document.getElementById('tv-ohlc-line');
  const candleMap = {candle_map_json};
  const candleTimes = {candle_times_json};
  const headerPrefix = '{tf_label} · {symbol}';
  const headerPrefixFull = '【{tf_label}】 {symbol} {symbol_name} · {tf_num} · {exchange}';
  const showIndicators = {json.dumps(show_indicators)};
  const showVolume = {json.dumps(show_volume)};
  const showLineLabels = {json.dumps(show_line_labels)};
  const showZoneLabels = {json.dumps(show_zone_labels)};
  const showOverlays = {json.dumps(show_overlays)};
  const compactHeader = {json.dumps(header_lines == 1)};
  const enablePriceScaleDrag = {json.dumps(variant == "main")};
  const useStripAspect = {json.dumps(variant == "strip")};
  const stripAspect = {strip_aspect if strip_aspect else 3.75};
  const stripMinH = {strip_min_h};
  const stripMaxH = {strip_max_h};
  const srHoverPx = {8 if variant == "strip" else 12};
  let bodyHeight = {height};

  const chart = LightweightCharts.createChart(container, {{
    width: container.clientWidth,
    height: bodyHeight,
    layout: {{ background: {{ color: '#ffffff' }}, textColor: '#334155' }},
    grid: {{ vertLines: {{ color: '#f1f5f9' }}, horzLines: {{ color: '#f1f5f9' }} }},
    rightPriceScale: {{
      borderColor: '#e2e8f0',
      minimumWidth: {scale_min_width},
      autoScale: true,
      alignLabels: true,
    }},
    timeScale: {{ borderColor: '#e2e8f0', timeVisible: true, secondsVisible: {json.dumps(seconds_visible)} }},
    handleScale: {{
      mouseWheel: true,
      pinch: true,
      axisPressedMouseMove: {{ time: true, price: enablePriceScaleDrag }},
      axisDoubleClickReset: {{ time: true, price: enablePriceScaleDrag }},
    }},
    handleScroll: {{
      mouseWheel: true,
      pressedMouseMove: true,
      horzTouchDrag: true,
      vertTouchDrag: true,
    }},
  }});

  const overlays = {overlays_json};
  const volumeMargins = {volume_margins_json};

  function applyScaleMargins(scaleId, margins) {{
    chart.priceScale(scaleId).applyOptions({{
      scaleMargins: {{ top: margins.top, bottom: margins.bottom }},
      autoScale: true,
    }});
  }}

  function formatOhlc(c, time) {{
    const idx = candleTimes.indexOf(time);
    const prevClose = idx > 0 ? candleMap[candleTimes[idx - 1]].close : c.open;
    const chg = c.close - prevClose;
    const pct = prevClose ? (chg / prevClose * 100) : 0;
    const sign = chg >= 0 ? '+' : '';
    const cls = chg >= 0 ? 'up' : 'down';
    if (compactHeader) {{
      return `${{headerPrefix}} 收=${{c.close.toFixed(2)}} `
        + `<span class="${{cls}}" style="font-weight:700;">${{sign}}${{chg.toFixed(2)}} (${{sign}}${{pct.toFixed(2)}}%)</span>`;
    }}
    return `${{headerPrefixFull}} 开=${{c.open.toFixed(2)}} 高=${{c.high.toFixed(2)}} 低=${{c.low.toFixed(2)}} 收=${{c.close.toFixed(2)}} `
      + `<span class="${{cls}}" style="font-weight:700;">${{sign}}${{chg.toFixed(2)}} (${{sign}}${{pct.toFixed(2)}}%)</span>`;
  }}

  const defaultOhlcHtml = {json.dumps(default_ohlc_html)};

  function positionZoneLabels(candleSeries) {{
    labelsEl.innerHTML = '';
    if (!showZoneLabels) return;
    const placed = [];
    const sorted = [...overlays.zones].sort((a, b) => (a.high + a.low) / 2 - (b.high + b.low) / 2);
    for (const zone of sorted) {{
      if (!zone.title) continue;
      const mid = (zone.low + zone.high) / 2;
      let y = candleSeries.priceToCoordinate(mid);
      if (y == null || y < 24 || y > bodyHeight - 16) continue;
      for (const py of placed) {{
        if (Math.abs(py - y) < 18) y = py - 20;
      }}
      placed.push(y);
      const el = document.createElement('div');
      el.className = 'zone-label';
      el.style.setProperty('--zone-color', zone.labelColor || '#94a3b8');
      el.style.top = `${{y}}px`;
      el.textContent = zone.title || '';
      labelsEl.appendChild(el);
    }}
  }}

  for (const zone of overlays.zones) {{
    if (!showOverlays || !zone.data || !zone.data.length) continue;
    const band = chart.addBaselineSeries({{
      baseValue: {{ type: 'price', price: zone.low }},
      relativeGradient: false,
      baseVisible: false,
      topFillColor1: zone.fill,
      topFillColor2: zone.fill,
      topLineColor: zone.border,
      bottomFillColor1: 'transparent',
      bottomFillColor2: 'transparent',
      bottomLineColor: 'transparent',
      lineWidth: 1,
      priceLineVisible: false,
      lastValueVisible: false,
      crosshairMarkerVisible: false,
    }});
    band.setData(zone.data);
  }}

  const candleSeries = chart.addCandlestickSeries({{
    upColor: '#22c55e', downColor: '#ef4444', borderVisible: false,
    wickUpColor: '#22c55e', wickDownColor: '#ef4444',
    priceLineVisible: {json.dumps(variant == "main")},
    lastValueVisible: true,
  }});
  candleSeries.setData({candles_json});
  candleSeries.priceScale().applyOptions({{ scaleMargins: {{ top: {top_margin}, bottom: {bottom_margin} }} }});

  if (showVolume) {{
    const volSeries = chart.addHistogramSeries({{
      priceFormat: {{ type: 'volume' }},
      priceScaleId: 'volume',
    }});
    volSeries.setData({volumes_json});
    applyScaleMargins('volume', volumeMargins);
  }}

  const lines = {lines_json};
  const lineWidth = showLineLabels ? 2 : 1;
  if (showIndicators) {{
    for (const [name, cfg] of Object.entries(lines)) {{
      const s = chart.addLineSeries({{
        color: cfg.color, lineWidth: lineWidth, title: name,
        priceLineVisible: false,
        lastValueVisible: showLineLabels,
      }});
      s.setData(cfg.data);
    }}
  }}

  if (showOverlays) {{
    for (const proj of overlays.projections || []) {{
      const s = chart.addLineSeries({{
        color: proj.color,
        lineWidth: 2,
        lineStyle: LightweightCharts.LineStyle.Dashed,
        priceLineVisible: false,
        lastValueVisible: false,
        title: '',
        crosshairMarkerVisible: false,
      }});
      s.setData(proj.data);
    }}
  }}

  const srLines = overlays.priceLines || [];
  for (const pl of srLines) {{
    candleSeries.createPriceLine({{
      price: pl.price, color: pl.color, lineWidth: 1,
      lineStyle: pl.style || 0,
      axisLabelVisible: true,
      title: pl.title || String(pl.price),
    }});
  }}

  function hideSrTip() {{
    if (srTipEl) srTipEl.style.display = 'none';
  }}

  function updateSrHover(param) {{
    if (!srTipEl || !srLines.length || !param.point) {{
      hideSrTip();
      return;
    }}
    let best = null;
    let bestDist = srHoverPx + 1;
    for (const pl of srLines) {{
      const y = candleSeries.priceToCoordinate(pl.price);
      if (y == null) continue;
      const px = Math.abs(param.point.y - y);
      if (px <= srHoverPx && px < bestDist) {{
        bestDist = px;
        best = pl;
      }}
    }}
    if (!best) {{
      hideSrTip();
      return;
    }}
    const lineY = candleSeries.priceToCoordinate(best.price);
    if (lineY == null) {{
      hideSrTip();
      return;
    }}
    const chartBody = container.parentElement;
    const bodyRect = chartBody ? chartBody.getBoundingClientRect() : container.getBoundingClientRect();
    const chartRect = container.getBoundingClientRect();
    const tipTop = (chartRect.top - bodyRect.top) + lineY;
    const tipLeft = (chartRect.left - bodyRect.left) + Math.min(Math.max(param.point.x + 10, 4), container.clientWidth - 120);
    srTipEl.style.display = 'block';
    srTipEl.style.top = `${{tipTop}}px`;
    srTipEl.style.left = `${{tipLeft}}px`;
    srTipEl.style.setProperty('--sr-color', best.color || '#64748b');
    const hint = best.hint || '';
    srTipEl.textContent = hint ? `${{best.title}} · ${{hint}}` : String(best.title || best.price);
  }}

  chart.timeScale().fitContent();
  if ({json.dumps(variant == "main")} && overlays.projections && overlays.projections.length && candleTimes.length) {{
    chart.timeScale().setVisibleLogicalRange({{
      from: 0,
      to: candleTimes.length - 1 + 20,
    }});
  }}
  positionZoneLabels(candleSeries);

  if (ohlcEl) {{
    chart.subscribeCrosshairMove(param => {{
      if (!param.time || !param.point) {{
        ohlcEl.innerHTML = defaultOhlcHtml;
        hideSrTip();
        return;
      }}
      const c = candleMap[param.time];
      if (c) ohlcEl.innerHTML = formatOhlc(c, param.time);
      updateSrHover(param);
    }});
  }} else {{
    chart.subscribeCrosshairMove(param => updateSrHover(param));
  }}

  new ResizeObserver(() => layoutChart()).observe(container);
  layoutChart();

  function layoutChart() {{
    const w = container.clientWidth;
    let h = bodyHeight;
    if (useStripAspect) {{
      h = Math.round(w / stripAspect);
      h = Math.max(stripMinH, Math.min(stripMaxH, h));
      bodyHeight = h;
    }}
    chart.applyOptions({{ width: w, height: h }});
    positionZoneLabels(candleSeries);
    hideSrTip();
    if (useStripAspect) {{
      const total = h + 1;
      try {{
        if (window.frameElement) {{
          window.frameElement.style.height = total + 'px';
          window.frameElement.style.overflow = 'hidden';
        }}
      }} catch (e) {{}}
      document.documentElement.style.overflow = 'hidden';
      document.body.style.margin = '0';
      document.body.style.padding = '0';
      document.body.style.overflow = 'hidden';
    }}
  }}
}})();
</script>
"""


def chart_iframe_height(variant: str = "main", height: int | None = None) -> int:
    preset = CHART_VARIANTS.get(variant, CHART_VARIANTS["main"])
    height = height if height is not None else int(preset["height"])
    if variant == "main":
        return height + 20
    if variant == "strip":
        min_h = int(preset.get("min_height", height))
        return min_h + 2
    return height + 4
