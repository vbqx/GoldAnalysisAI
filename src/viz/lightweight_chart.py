"""TradingView Lightweight Charts renderer with SMC overlays."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis

LINE_COLORS = {
    "EMA20": "#a855f7",
    "EMA50": "#eab308",
    "EMA610": "#ef4444",
    "VWAP": "#3b82f6",
}

MAX_FVG_ZONES = 2
MAX_OB_ZONES = 2

TF_LABELS = {
    "5m": "5min周期 (执行结构)",
    "15m": "15min周期 (中间结构)",
    "1h": "1H周期 (宏观结构)",
    "4h": "4H周期 (宏观结构)",
}


def _zone_title(kind: str, direction: str, low: float, high: float, *, strong: bool = False) -> str:
    lo, hi = int(round(low)), int(round(high))
    if kind == "demand":
        return f"需求/流动性区 {hi}-{lo}"
    if kind == "fvg":
        prefix = "反抽卖区" if direction == "bearish" else "回调买区"
        return f"{prefix} (FVG) {lo}-{hi}"
    prefix = "强势反抽卖区" if direction == "bearish" and strong else (
        "强势回调买区" if direction == "bullish" and strong else (
            "反抽卖区" if direction == "bearish" else "回调买区"
        )
    )
    return f"{prefix} (订单块) {lo}-{hi}"


def _to_unix(ts: pd.Timestamp) -> int:
    return int(pd.Timestamp(ts).timestamp())


def _ranges_overlap(a_low: float, a_high: float, b_low: float, b_high: float, *, gap: float = 4.0) -> bool:
    return not (a_high + gap < b_low or b_high + gap < a_low)


def _merge_fvg_cluster(fvgs: list) -> tuple[float, float, pd.Timestamp, str]:
    low = min(f.low for f in fvgs)
    high = max(f.high for f in fvgs)
    time = min(f.time for f in fvgs)
    direction = fvgs[0].direction
    return low, high, time, direction


def _pick_chart_fvgs(analysis: TimeframeAnalysis, price: float, *, max_zones: int = 1) -> list[tuple[float, float, pd.Timestamp, str]]:
    """Nearest active bearish FVG above price; merge overlapping gaps."""
    active = [f for f in analysis.active_fvgs if f.direction == "bearish"]
    if not active:
        return []

    above = sorted([f for f in active if f.high >= price * 0.998], key=lambda f: f.low)
    if not above:
        active.sort(key=lambda f: abs((f.low + f.high) / 2 - price))
        above = active[:1]

    clusters: list[list] = []
    for fvg in above:
        placed = False
        for cluster in clusters:
            if _ranges_overlap(cluster[0].low, cluster[0].high, fvg.low, fvg.high):
                cluster.append(fvg)
                placed = True
                break
        if not placed:
            clusters.append([fvg])

    picked: list[tuple[float, float, pd.Timestamp, str]] = []
    for cluster in sorted(clusters, key=lambda c: c[0].low):
        picked.append(_merge_fvg_cluster(cluster))
        if len(picked) >= max_zones:
            break
    return picked


def _pick_chart_obs(
    analysis: TimeframeAnalysis,
    macro: TimeframeAnalysis | None,
    price: float,
    *,
    max_zones: int = 2,
) -> list[tuple[Any, bool]]:
    """Pick bearish OBs: strong zone from macro TF, tactical zone from execution TF."""
    exec_obs = [o for o in analysis.order_blocks if o.direction == "bearish"]
    macro_obs = [o for o in (macro.order_blocks if macro else []) if o.direction == "bearish"]

    result: list[tuple[Any, bool]] = []
    seen: set[tuple[float, float]] = set()

    def add(ob: Any, strong: bool) -> None:
        key = (round(ob.low, 2), round(ob.high, 2))
        if key in seen:
            return
        seen.add(key)
        result.append((ob, strong))

    if macro_obs:
        strong = max(macro_obs, key=lambda o: (o.high - o.low, o.high))
        add(strong, True)

    near = sorted([o for o in exec_obs if o.high >= price * 0.995], key=lambda o: o.low)
    if near:
        add(near[0], not result)

    if not result and exec_obs:
        add(max(exec_obs, key=lambda o: (o.high - o.low, o.high)), True)

    return result[:max_zones]


def _zone_area_data(plot_df: pd.DataFrame, start_time: pd.Timestamp, high: float) -> list[dict[str, float | int]]:
    """Area series points: value=high from start_time to end of visible range."""
    subset = plot_df[plot_df.index >= start_time]
    if subset.empty:
        subset = plot_df
    return [{"time": _to_unix(idx), "value": round(high, 2)} for idx in subset.index]


def _append_zone(
    zones: list[dict[str, Any]],
    *,
    kind: str,
    direction: str,
    low: float,
    high: float,
    start_time: pd.Timestamp,
    plot_df: pd.DataFrame,
    strong: bool = False,
) -> None:
    bear = direction == "bearish"
    if kind == "demand":
        fill, border, label_color = "rgba(34,197,94,0.28)", "rgba(34,197,94,0.70)", "#16a34a"
    elif kind == "fvg":
        fill = "rgba(244,63,94,0.32)" if bear else "rgba(34,197,94,0.32)"
        border = "rgba(244,63,94,0.75)" if bear else "rgba(34,197,94,0.75)"
        label_color = "#e11d48" if bear else "#16a34a"
    else:
        fill = "rgba(249,115,22,0.30)" if bear else "rgba(59,130,246,0.30)"
        border = "rgba(249,115,22,0.80)" if bear else "rgba(59,130,246,0.80)"
        label_color = "#ea580c" if bear else "#2563eb"

    zones.append(
        {
            "kind": kind,
            "title": _zone_title(kind, direction, low, high, strong=strong),
            "low": round(low, 2),
            "high": round(high, 2),
            "fill": fill,
            "border": border,
            "labelColor": label_color,
            "data": _zone_area_data(plot_df, start_time, high),
        }
    )


def _serialize_overlays(
    analysis: TimeframeAnalysis,
    report: dict[str, Any],
    plot_df: pd.DataFrame,
    *,
    timeframe: str = "1h",
    macro_analysis: TimeframeAnalysis | None = None,
) -> dict[str, Any]:
    """Build zones (filled blocks), minimal reference lines, and structure markers."""
    t_min = plot_df.index.min()
    t_max = plot_df.index.max()
    price = float(plot_df["Close"].iloc[-1])

    price_lines: list[dict[str, Any]] = []
    zones: list[dict[str, Any]] = []
    markers: list[dict[str, Any]] = []

    # EQ reference — macro timeframes only (5m execution chart matches reference layout)
    if timeframe != "5m" and analysis.equilibrium is not None:
        price_lines.append(
            {
                "price": round(analysis.equilibrium, 2),
                "color": "#6366f1",
                "title": "EQ 50%",
                "style": 2,
                "label": True,
            }
        )

    swing_low = report["chart"].get("swing_low")
    if swing_low:
        sl = float(swing_low)
        _append_zone(
            zones,
            kind="demand",
            direction="bullish",
            low=sl - 5,
            high=sl,
            start_time=t_min,
            plot_df=plot_df,
        )

    if analysis.trend != "bullish":
        for low, high, start, direction in _pick_chart_fvgs(analysis, price, max_zones=1):
            _append_zone(
                zones,
                kind="fvg",
                direction=direction,
                low=low,
                high=high,
                start_time=start,
                plot_df=plot_df,
            )
        for ob, strong in _pick_chart_obs(analysis, macro_analysis, price, max_zones=MAX_OB_ZONES):
            _append_zone(
                zones,
                kind="ob",
                direction=ob.direction,
                low=ob.low,
                high=ob.high,
                start_time=ob.time,
                plot_df=plot_df,
                strong=strong,
            )
    else:
        bull_fvgs = [f for f in analysis.active_fvgs if f.direction == "bullish"]
        if bull_fvgs:
            fvg = min(bull_fvgs, key=lambda f: abs((f.low + f.high) / 2 - price))
            _append_zone(
                zones, kind="fvg", direction="bullish", low=fvg.low, high=fvg.high,
                start_time=fvg.time, plot_df=plot_df,
            )
        bull_obs = [o for o in analysis.order_blocks if o.direction == "bullish"]
        if bull_obs:
            ob = max(bull_obs, key=lambda o: (o.high - o.low, o.high))
            _append_zone(
                zones, kind="ob", direction="bullish", low=ob.low, high=ob.high,
                start_time=ob.time, plot_df=plot_df, strong=True,
            )

    # BOS / CHoCH markers — execution TF + macro TF events
    event_sources = [analysis]
    if macro_analysis is not None:
        event_sources.append(macro_analysis)
    seen_events: set[tuple[str, int]] = set()
    for src in event_sources:
        for ev in src.events[-3:]:
            if ev.time < t_min or ev.time > t_max:
                continue
            key = (ev.kind, _to_unix(ev.time))
            if key in seen_events:
                continue
            seen_events.add(key)
            is_bull = ev.direction == "bullish"
            markers.append(
                {
                    "time": _to_unix(ev.time),
                    "position": "belowBar" if is_bull else "aboveBar",
                    "color": "#22c55e" if is_bull else "#ef4444",
                    "shape": "arrowUp" if is_bull else "arrowDown",
                    "text": ev.kind,
                }
            )

    return {"priceLines": price_lines, "zones": zones, "markers": markers}


def build_lightweight_chart_html(
    df: pd.DataFrame,
    analysis: TimeframeAnalysis | None = None,
    report: dict[str, Any] | None = None,
    *,
    macro_analysis: TimeframeAnalysis | None = None,
    timeframe: str = "1h",
    symbol: str = "XAUUSD",
    symbol_name: str = "黄金/美元",
    exchange: str = "OANDA",
    height: int = 520,
    bars: int = 120,
) -> str:
    """Build HTML/JS for TradingView Lightweight Charts with volume + SMC zones."""
    plot_df = df.tail(bars).copy()
    last = plot_df.iloc[-1]
    prev = plot_df.iloc[-2] if len(plot_df) > 1 else last
    o, h, l, c = float(last["Open"]), float(last["High"]), float(last["Low"]), float(last["Close"])
    chg = c - float(prev["Close"])
    chg_pct = (chg / float(prev["Close"]) * 100) if float(prev["Close"]) else 0.0
    chg_sign = "+" if chg >= 0 else ""
    chg_cls = "up" if chg >= 0 else "down"

    tf_label = TF_LABELS.get(timeframe, f"{timeframe}周期")
    tf_num = {"5m": "5", "15m": "15", "1h": "60", "4h": "240"}.get(timeframe, timeframe)

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
            analysis, report, plot_df, timeframe=timeframe, macro_analysis=macro_analysis,
        )
        if analysis is not None and report is not None
        else {"priceLines": [], "zones": [], "markers": []}
    )

    candles_json = json.dumps(candles)
    volumes_json = json.dumps(volumes)
    lines_json = json.dumps(line_series)
    overlays_json = json.dumps(overlays)
    candle_times_json = json.dumps([c["time"] for c in candles])
    candle_map_json = json.dumps({c["time"]: c for c in candles})
    last_bar = candles[-1] if candles else {"open": 0, "high": 0, "low": 0, "close": 0}
    last_o, last_h, last_l, last_c = last_bar["open"], last_bar["high"], last_bar["low"], last_bar["close"]
    default_ohlc_html = (
        f"【{tf_label}】 {symbol} {symbol_name} · {tf_num} · {exchange} "
        f"开={last_o:.2f} 高={last_h:.2f} 低={last_l:.2f} 收={last_c:.2f} "
        f"<span class=\"{chg_cls}\" style=\"font-weight:700;\">{chg_sign}{chg:.2f} ({chg_sign}{chg_pct:.2f}%)</span>"
    )

    return f"""
<div class="tv-chart-wrap" style="position:relative;width:100%;font-family:system-ui,-apple-system,sans-serif;">
  <div id="tv-chart-header" style="position:absolute;top:6px;left:10px;z-index:20;pointer-events:none;line-height:1.45;">
    <div id="tv-ohlc-line" style="font-size:12px;color:#334155;font-weight:600;">{default_ohlc_html}</div>
    <div style="font-size:11px;color:#64748b;margin-top:1px;">
      <span style="color:#a855f7;">EMA20(紫)</span>
      <span style="margin-left:8px;color:#eab308;">EMA50(黄)</span>
      <span style="margin-left:8px;color:#3b82f6;">VWAP(蓝)</span>
      <span style="margin-left:8px;color:#ef4444;">EMA610(红)</span>
    </div>
    <div style="font-size:11px;color:#94a3b8;margin-top:1px;">{smc_note}</div>
  </div>
  <div id="zone-labels" style="position:absolute;inset:0;pointer-events:none;z-index:15;overflow:hidden;"></div>
  <div id="tv-chart-container" style="width:100%;height:{height}px;"></div>
</div>
<style>
  .tv-chart-wrap .up {{ color:#16a34a; }}
  .tv-chart-wrap .down {{ color:#dc2626; }}
  .zone-label {{
    position:absolute;
    right:78px;
    transform:translateY(-50%);
    font-size:11px;
    font-weight:600;
    color:#334155;
    background:rgba(255,255,255,0.92);
    padding:2px 7px 2px 5px;
    border-left:3px solid var(--zone-color, #94a3b8);
    white-space:nowrap;
    box-shadow:0 1px 2px rgba(15,23,42,0.06);
  }}
</style>
<script src="https://unpkg.com/lightweight-charts@4.2.0/dist/lightweight-charts.standalone.production.js"></script>
<script>
(function() {{
  const container = document.getElementById('tv-chart-container');
  const labelsEl = document.getElementById('zone-labels');
  const ohlcEl = document.getElementById('tv-ohlc-line');
  const candleMap = {candle_map_json};
  const candleTimes = {candle_times_json};
  const headerPrefix = '【{tf_label}】 {symbol} {symbol_name} · {tf_num} · {exchange}';

  const chart = LightweightCharts.createChart(container, {{
    width: container.clientWidth,
    height: {height},
    layout: {{ background: {{ color: '#ffffff' }}, textColor: '#334155' }},
    grid: {{ vertLines: {{ color: '#f1f5f9' }}, horzLines: {{ color: '#f1f5f9' }} }},
    rightPriceScale: {{ borderColor: '#e2e8f0', minimumWidth: 72 }},
    timeScale: {{ borderColor: '#e2e8f0', timeVisible: true, secondsVisible: false }},
  }});

  const overlays = {overlays_json};

  function formatOhlc(c, time) {{
    const idx = candleTimes.indexOf(time);
    const prevClose = idx > 0 ? candleMap[candleTimes[idx - 1]].close : c.open;
    const chg = c.close - prevClose;
    const pct = prevClose ? (chg / prevClose * 100) : 0;
    const sign = chg >= 0 ? '+' : '';
    const cls = chg >= 0 ? 'up' : 'down';
    return `${{headerPrefix}} 开=${{c.open.toFixed(2)}} 高=${{c.high.toFixed(2)}} 低=${{c.low.toFixed(2)}} 收=${{c.close.toFixed(2)}} `
      + `<span class="${{cls}}" style="font-weight:700;">${{sign}}${{chg.toFixed(2)}} (${{sign}}${{pct.toFixed(2)}}%)</span>`;
  }}

  const defaultOhlcHtml = {json.dumps(default_ohlc_html)};

  function positionZoneLabels(candleSeries) {{
    labelsEl.innerHTML = '';
    const placed = [];
    const sorted = [...overlays.zones].sort((a, b) => (a.high + a.low) / 2 - (b.high + b.low) / 2);
    for (const zone of sorted) {{
      const mid = (zone.low + zone.high) / 2;
      let y = candleSeries.priceToCoordinate(mid);
      if (y == null || y < 48 || y > {height} - 36) continue;
      for (const py of placed) {{
        if (Math.abs(py - y) < 22) y = py - 24;
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

  // 1) SMC zones first (background layers) — BaselineSeries fills between low & high
  for (const zone of overlays.zones) {{
    if (!zone.data || !zone.data.length) continue;
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

  // 2) Candles on top of zones
  const candleSeries = chart.addCandlestickSeries({{
    upColor: '#22c55e', downColor: '#ef4444', borderVisible: false,
    wickUpColor: '#22c55e', wickDownColor: '#ef4444',
    priceLineVisible: true, lastValueVisible: true,
  }});
  candleSeries.setData({candles_json});
  candleSeries.priceScale().applyOptions({{ scaleMargins: {{ top: 0.10, bottom: 0.28 }} }});

  const volSeries = chart.addHistogramSeries({{
    priceFormat: {{ type: 'volume' }},
    priceScaleId: 'volume',
  }});
  volSeries.setData({volumes_json});
  chart.priceScale('volume').applyOptions({{ scaleMargins: {{ top: 0.78, bottom: 0 }} }});

  // 3) EMA / VWAP — all show colored last-value labels on the right (like reference)
  const lines = {lines_json};
  for (const [name, cfg] of Object.entries(lines)) {{
    const s = chart.addLineSeries({{
      color: cfg.color, lineWidth: 2, title: name,
      priceLineVisible: false,
      lastValueVisible: true,
    }});
    s.setData(cfg.data);
  }}

  // Minimal reference lines (EQ only)
  for (const pl of overlays.priceLines) {{
    candleSeries.createPriceLine({{
      price: pl.price, color: pl.color, lineWidth: 1,
      lineStyle: pl.style || 0,
      axisLabelVisible: !!pl.label,
      title: pl.title || '',
    }});
  }}

  if (overlays.markers.length) {{
    candleSeries.setMarkers(overlays.markers);
  }}

  chart.timeScale().fitContent();
  positionZoneLabels(candleSeries);

  chart.subscribeCrosshairMove(param => {{
    if (!param.time || !param.point) {{
      ohlcEl.innerHTML = defaultOhlcHtml;
      return;
    }}
    const c = candleMap[param.time];
    if (c) ohlcEl.innerHTML = formatOhlc(c, param.time);
  }});

  new ResizeObserver(() => {{
    chart.applyOptions({{ width: container.clientWidth }});
    positionZoneLabels(candleSeries);
  }}).observe(container);
}})();
</script>
"""
