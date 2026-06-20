"""Report assembly: trading plans, conclusions, projections."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.core.types import MarketContext
from src.config import RISK_REWARD_DISPLAY_CAP, SIGNAL_SL_BELOW_SWING, SIGNAL_SWEEP_OFFSET
from src.data.fetcher import daily_metrics, utc8_now
from src.indicators.technical import ema_relation, fibonacci_levels
from src.indicators.verify import indicator_snapshot
from src.log import get_logger

log = get_logger(__name__)

_CAL_EVENT_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{1,2}:\d{2}\s+[AP]M)\s+(?P<body>.+)$",
    re.I,
)


@dataclass
class TradingSignal:
    name: str
    direction: str
    direction_cn: str
    entry_low: float
    entry_high: float
    stop_loss: float
    take_profits: list[float]
    risk_reward: str
    sentiment_bias_pct: str
    position_size: str
    note: str
    theme: str  # "short" | "long"
    signal_role: str = "primary"  # "primary" | "alternate"


def _nearest_zone(price: float, zones: list, direction: str) -> tuple[float, float] | None:
    candidates = []
    for z in zones:
        if direction == "bearish" and z.direction == "bearish" and z.low >= price * 0.998:
            candidates.append((z.low, z.high))
        if direction == "bullish" and z.direction == "bullish" and z.high <= price * 1.002:
            candidates.append((z.low, z.high))
    if not candidates:
        return None
    if direction == "bearish":
        candidates.sort(key=lambda x: x[0])
        return candidates[0]
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0]


def _sell_fvg_targets(
    entry_low: float,
    entry_high: float,
    swing_low: float,
) -> tuple[float, float, float, float] | None:
    """SELL FVG: SL above entry, TP1 below entry_mid. Returns None if geometry invalid."""
    entry_mid = (entry_low + entry_high) / 2
    zone_width = max(entry_high - entry_low, 0.01)
    min_sl_dist = max(zone_width * 0.25, 0.5)
    sl = max(entry_high + zone_width * 0.5, entry_mid + min_sl_dist)
    tp1 = entry_mid - max(zone_width * 1.5, entry_mid * 0.003)
    tp2 = swing_low + (entry_mid - swing_low) * 0.3
    tp3 = swing_low
    if sl <= entry_mid or tp1 >= entry_mid:
        return None
    return round(sl, 2), round(tp1, 2), round(tp2, 2), round(tp3, 2)


def _compute_risk_reward(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    stop_loss: float,
    take_profits: list[float],
) -> str:
    if not take_profits:
        return "N/A"
    entry_mid = (entry_low + entry_high) / 2
    tp1 = take_profits[0]
    if direction == "SELL":
        risk = stop_loss - entry_mid
        reward = entry_mid - tp1
    else:
        risk = entry_mid - stop_loss
        reward = tp1 - entry_mid
    if risk <= 0 or reward <= 0:
        return "N/A"
    ratio = reward / risk
    if ratio > RISK_REWARD_DISPLAY_CAP:
        return f"1:{RISK_REWARD_DISPLAY_CAP:.0f}+（远端限价）"
    return f"1:{ratio:.1f}"


def compute_trading_signals(ctx: MarketContext) -> list[TradingSignal]:
    """Single entry point for pipeline signal generation (trader + report share this)."""
    analyses = ctx.analyses
    sentiment = sentiment_score(analyses)
    primary = analyses.get("4h") or analyses.get("1h")
    swing_high = (
        primary.swing_high if primary and primary.swing_high else ctx.metrics["daily_high"]
    )
    swing_low = (
        primary.swing_low if primary and primary.swing_low else ctx.metrics["daily_low"]
    )
    return generate_trading_signals(
        ctx.price,
        analyses["5m"],
        analyses["15m"],
        swing_high,
        swing_low,
        sentiment,
    )


def generate_trading_signals(
    price: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
    swing_high: float,
    swing_low: float,
    sentiment: dict[str, float],
) -> list[TradingSignal]:
    signals: list[TradingSignal] = []
    bear_pct = int(sentiment.get("bearish", 62))
    bull_pct = int(sentiment.get("bullish", 28))

    bear_fvgs = analysis_5m.fvgs + analysis_15m.fvgs
    bear_obs = [ob for ob in analysis_5m.order_blocks + analysis_15m.order_blocks if ob.direction == "bearish"]
    bull_obs = [ob for ob in analysis_5m.order_blocks + analysis_15m.order_blocks if ob.direction == "bullish"]

    fvg_zone = _nearest_zone(price, bear_fvgs, "bearish")
    if fvg_zone:
        entry_low, entry_high = fvg_zone[0], fvg_zone[1]
        targets = _sell_fvg_targets(entry_low, entry_high, swing_low)
        if targets:
            sl, tp1, tp2, tp3 = targets
            el, eh = round(entry_low, 2), round(entry_high, 2)
            tps = [tp1, tp2, tp3]
            rr = _compute_risk_reward(
                direction="SELL",
                entry_low=el,
                entry_high=eh,
                stop_loss=sl,
                take_profits=tps,
            )
            if rr != "N/A":
                signals.append(
                    TradingSignal(
                        name="激进反抽做空",
                        direction="SELL",
                        direction_cn="卖出",
                        entry_low=el,
                        entry_high=eh,
                        stop_loss=sl,
                        take_profits=tps,
                        risk_reward=rr,
                        sentiment_bias_pct=f"{bear_pct}%",
                        position_size="30% 试探仓",
                        note="反弹至 FVG / 流动性回补后做空",
                        theme="short",
                    )
                )

    if bear_obs:
        ob = sorted(bear_obs, key=lambda o: o.low)[-1]
        entry_low, entry_high = round(ob.low, 2), round(ob.high, 2)
        mid = (entry_low + entry_high) / 2
        zone_width = max(entry_high - entry_low, 0.01)
        sl = round(entry_high + zone_width, 2)
        tp1 = round(mid - zone_width * 2, 2)
        tp2 = round(swing_low + (mid - swing_low) * 0.5, 2)
        tp3 = round(swing_low, 2)
        tps = [tp1, tp2, tp3]
        rr = _compute_risk_reward(
            direction="SELL",
            entry_low=entry_low,
            entry_high=entry_high,
            stop_loss=sl,
            take_profits=tps,
        )
        if sl > mid > tp1 and rr != "N/A":
            signals.append(
                TradingSignal(
                    name="保守反抽做空",
                    direction="SELL",
                    direction_cn="卖出",
                    entry_low=entry_low,
                    entry_high=entry_high,
                    stop_loss=sl,
                    take_profits=tps,
                    risk_reward=rr,
                    sentiment_bias_pct=f"{max(bear_pct - 5, 45)}%",
                    position_size="20% 标准仓",
                    note="更高时间框架 Order Block 反弹做空",
                    theme="short",
                )
            )

    if bull_obs or swing_low:
        sweep_low = swing_low - SIGNAL_SWEEP_OFFSET
        tp1 = price
        tp2 = swing_low + (swing_high - swing_low) * 0.382
        tp3 = swing_low + (swing_high - swing_low) * 0.5
        entry_low_r = round(sweep_low, 2)
        entry_high_r = round(swing_low, 2)
        sl_r = round(swing_low - SIGNAL_SL_BELOW_SWING, 2)
        tps = [round(tp1, 2), round(tp2, 2), round(tp3, 2)]
        signals.append(
            TradingSignal(
                name="右侧扫低做多",
                direction="BUY",
                direction_cn="买入",
                entry_low=entry_low_r,
                entry_high=entry_high_r,
                stop_loss=sl_r,
                take_profits=tps,
                risk_reward=_compute_risk_reward(
                    direction="BUY",
                    entry_low=entry_low_r,
                    entry_high=entry_high_r,
                    stop_loss=sl_r,
                    take_profits=tps,
                ),
                sentiment_bias_pct=f"{bull_pct}%",
                position_size="15% 逆势轻仓",
                note="流动性扫低后短多，严格止损",
                theme="long",
            )
        )

    return signals


def trend_projections(
    price: float,
    swing_high: float,
    swing_low: float,
    sentiment: dict[str, float],
) -> list[dict[str, Any]]:
    range_size = max(swing_high - swing_low, 1e-9)
    pullback_shallow = swing_high - range_size * 0.382
    pullback_deep = swing_high - range_size * 0.618
    mid_rally = swing_low + range_size * 0.382
    deep_rally = swing_low + range_size * 0.618

    bull = sentiment.get("bullish", 0)
    bear = sentiment.get("bearish", 0)
    ranging = sentiment.get("ranging", 0)

    if bull > bear and bull >= ranging:
        return [
            {
                "name": "主路径 (回调后上行)",
                "probability": bull,
                "color": "#22c55e",
                "steps": [
                    {"label": "当前", "price": price},
                    {"label": "回踩支撑", "price": round(pullback_shallow, 2)},
                    {"label": "上破前高", "price": round(swing_high + range_size * 0.1, 2)},
                ],
            },
            {
                "name": "次路径 (深回调后修复)",
                "probability": ranging,
                "color": "#64748b",
                "steps": [
                    {"label": "当前", "price": price},
                    {"label": "测试深支撑", "price": round(pullback_deep, 2)},
                    {"label": "回到中枢", "price": round((swing_high + swing_low) / 2, 2)},
                ],
            },
            {
                "name": "风险路径 (跌破支撑)",
                "probability": bear,
                "color": "#ef4444",
                "steps": [
                    {"label": "当前", "price": price},
                    {"label": "跌破支撑", "price": round(swing_low - range_size * 0.1, 2)},
                ],
            },
        ]

    if ranging >= max(bull, bear):
        return [
            {
                "name": "主路径 (区间震荡)",
                "probability": ranging,
                "color": "#64748b",
                "steps": [
                    {"label": "当前", "price": price},
                    {"label": "回归中枢", "price": round((swing_high + swing_low) / 2, 2)},
                    {
                        "label": "测试区间边界",
                        "price": round(
                            swing_high if price < (swing_high + swing_low) / 2 else swing_low,
                            2,
                        ),
                    },
                ],
            },
            {
                "name": "上破路径",
                "probability": bull,
                "color": "#22c55e",
                "steps": [
                    {"label": "当前", "price": price},
                    {"label": "上破前高", "price": round(swing_high + range_size * 0.1, 2)},
                ],
            },
            {
                "name": "下破路径",
                "probability": bear,
                "color": "#ef4444",
                "steps": [
                    {"label": "当前", "price": price},
                    {"label": "跌破前低", "price": round(swing_low - range_size * 0.1, 2)},
                ],
            },
        ]

    return [
        {
            "name": "主路径 (反弹后回落)",
            "probability": sentiment.get("bearish", 60),
            "color": "#ef4444",
            "steps": [
                {"label": "当前", "price": price},
                {"label": "反弹 FVG", "price": round(mid_rally, 2)},
                {"label": "新低", "price": round(swing_low - (swing_high - swing_low) * 0.1, 2)},
            ],
        },
        {
            "name": "次路径 (更深反弹)",
            "probability": sentiment.get("bullish", 28),
            "color": "#22c55e",
            "steps": [
                {"label": "当前", "price": price},
                {"label": "测试 OB", "price": round(deep_rally, 2)},
                {"label": "回落", "price": round(swing_low, 2)},
            ],
        },
        {
            "name": "极端路径 (直接破位)",
            "probability": sentiment.get("ranging", 12),
            "color": "#64748b",
            "steps": [
                {"label": "当前", "price": price},
                {"label": "直接下破", "price": round(swing_low - 15, 2)},
            ],
        },
    ]


def build_conclusion(
    sentiment: dict[str, float],
    primary_trend: str,
    signals: list[TradingSignal],
) -> dict[str, Any]:
    bearish = sentiment["bearish"]
    bullish = sentiment["bullish"]
    ranging = sentiment.get("ranging", 0)
    if ranging >= max(bearish, bullish):
        mood = "震荡中性 ↔"
        direction = "多空优势不明显，优先等待区间边界确认"
        action = "不追涨杀跌，等待支撑/阻力区的确认信号"
        dominant_theme = "neutral"
    elif bearish >= bullish:
        mood = "弱势偏空 ↓"
        direction = "主方向偏空，当前处于逆势反弹阶段"
        action = "不追多，优先等待反弹至阻力区做空"
        dominant_theme = "short"
    else:
        mood = "偏强偏多 ↑"
        direction = "主方向偏多，关注回调支撑"
        action = "不追空，优先等待回调至需求区做多"
        dominant_theme = "long"

    primary_signal = None
    if dominant_theme != "neutral":
        primary_signal = next((s for s in signals if s.theme == dominant_theme), None)
    if primary_signal is None and signals:
        primary_signal = signals[0]

    if primary_signal:
        first = primary_signal
        zone = f"{first.entry_low:.0f}-{first.entry_high:.0f}"
        if dominant_theme == "short":
            action = f"不追多，优先等待 {zone} 反弹至阻力区做空"
        elif dominant_theme == "long":
            action = f"不追空，优先等待 {zone} 附近回调做多"
        else:
            action = f"等待 {zone} 区域确认方向后再参与"

    short_sig = next((s for s in signals if s.theme == "short"), None)
    long_sig = next((s for s in signals if s.theme == "long"), None)
    if dominant_theme == "long":
        must_do = [
            "★ 主策略：回调至需求/支撑区分批做多",
            "★ 次策略：冲高至阻力区后只做轻仓逆势短空",
            "★ 风控：单笔风险 ≤ 2%，跌破结构支撑减仓或退出",
        ]
    elif dominant_theme == "neutral":
        must_do = [
            "★ 主策略：等待区间边界确认，不在中枢追单",
            "★ 次策略：突破后回踩/反抽确认再跟随",
            "★ 风控：单笔风险 ≤ 2%，事件前降低仓位",
        ]
    else:
        must_do = [
            "★ 主策略：反弹至 FVG/OB 阻力区分批做空",
            "★ 次策略：扫低流动性后短多（逆势轻仓）",
            "★ 风控：单笔风险 ≤ 2%，止损必执行",
        ]

    return {
        "market_sentiment": mood,
        "direction_summary": direction,
        "action": action,
        "header_conclusion": f"{direction}。{action}",
        "must_do": must_do,
        "starred": [
            f"最佳做空区：{short_sig.entry_low:.0f}-{short_sig.entry_high:.0f}" if short_sig else "暂不建议追空",
            f"最佳做多区：{long_sig.entry_low:.0f}-{long_sig.entry_high:.0f}" if long_sig else "暂不建议追多",
            "失效条件见下方「失效条件」模块",
        ],
    }


def invalidation_rules(
    analysis_15m: TimeframeAnalysis,
    swing_high: float,
    signals: list[TradingSignal],
) -> list[str]:
    # Use conservative OB top or 15m swing high, whichever is closer to price action
    invalid_level = swing_high
    if signals:
        short_sigs = [s for s in signals if s.theme == "short"]
        if short_sigs:
            invalid_level = max(s.stop_loss for s in short_sigs)

    rules = [
        f"15min 收盘价站稳 {round(invalid_level, 2)} 上方 → 空头 thesis 失效",
        "出现 Higher High + Higher Low 结构 → 趋势转多",
        "价格有效填补所有 bearish FVG 并延续上行 → 降低做空优先级",
    ]
    if analysis_15m.events:
        for e in analysis_15m.events:
            if e.kind == "CHoCH" and e.direction == "bullish":
                rules.insert(0, f"已出现 15min Bullish CHoCH @ {e.price:.2f}")
    return rules


def parse_risk_events_calendar(risk_events: str) -> list[dict[str, str]]:
    """Turn scraped calendar text into sidebar calendar rows."""
    if not risk_events or risk_events == "—" or "占位" in risk_events:
        return []
    events: list[dict[str, str]] = []
    for part in risk_events.split("；"):
        chunk = part.strip()
        if not chunk:
            continue
        m = _CAL_EVENT_RE.match(chunk)
        if m:
            body = m.group("body").strip()
            flag = "🇺🇸" if "united states" in body.lower() or body.upper().startswith("US ") else "🌍"
            events.append(
                {
                    "time": f"{m.group('date')} {m.group('time')}",
                    "flag": flag,
                    "event": body,
                }
            )
        else:
            events.append({"time": "—", "flag": "📅", "event": chunk})
    return events


def build_calendar_events() -> list[dict[str, str]]:
    """Fallback placeholders when live calendar is unavailable."""
    return [
        {"time": "20:15", "flag": "🇺🇸", "event": "ADP 就业 / 制造业数据"},
        {"time": "22:30", "flag": "🇺🇸", "event": "EIA 原油库存"},
        {"time": "22:45", "flag": "🇺🇸", "event": "美联储官员讲话 (关注)"},
    ]


def build_key_levels(
    price: float,
    metrics: dict,
    swing_high: float,
    swing_low: float,
    fib: list[dict],
    signals: list[TradingSignal],
) -> list[dict[str, Any]]:
    levels: list[dict[str, Any]] = []
    daily_open = metrics.get("prev_close", price)

    levels.append({"price": metrics["daily_high"], "label": "上方强压", "kind": "resistance"})
    levels.append({"price_low": daily_open - 1, "price_high": daily_open + 1, "label": "Daily Open", "kind": "neutral"})
    eq = fib[1]["price"] if len(fib) > 1 else (swing_high + swing_low) / 2
    levels.append({"price": eq, "label": "前段中枢 / 均衡", "kind": "neutral"})

    if signals:
        s0 = signals[0]
        levels.append({
            "price_low": s0.entry_low, "price_high": s0.entry_high,
            "label": "反抽压力", "kind": "resistance",
        })
    mid = (swing_high + swing_low) / 2
    levels.append({"price_low": mid - 2, "price_high": mid + 2, "label": "当前分界", "kind": "neutral"})
    levels.append({"price_low": swing_low, "price_high": swing_low + 12, "label": "下方支撑", "kind": "support"})

    return sorted(levels, key=lambda x: -(x.get("price") or x.get("price_high", 0)))


def build_market_overview(
    analyses: dict[str, TimeframeAnalysis],
    metrics: dict,
    conclusion: dict,
) -> list[str]:
    items = []
    for tf, label in (("4h", "4H"), ("1h", "1H"), ("15m", "15m")):
        a = analyses[tf]
        trend = {"bearish": "偏空", "bullish": "偏多", "ranging": "震荡"}.get(a.trend, "—")
        items.append(f"{label} 结构：{trend} | BOS {a.bos} | CHoCH {a.choch}")
    items.append(f"现价 {metrics['current_price']:.2f}，日幅 {metrics['daily_low']:.0f}-{metrics['daily_high']:.0f}")
    items.append(conclusion["direction_summary"])
    return items[:5]


def build_resistance_support(
    key_levels: list[dict],
    liquidity: list[dict],
) -> tuple[list[str], list[str]]:
    resist, support = [], []
    for lv in key_levels:
        txt = lv.get("label", "")
        if "price_low" in lv:
            val = f"{lv['price_low']:.0f}-{lv['price_high']:.0f}"
        else:
            val = f"{lv['price']:.0f}"
        line = f"{val}：{txt}"
        if lv.get("kind") == "resistance":
            resist.append(line)
        elif lv.get("kind") == "support":
            support.append(line)
    for item in liquidity[:3]:
        if "Low" in item["label"] or "Buy" in item["label"]:
            support.append(f"{item['price']:.0f}：{item['label']}")
        else:
            resist.append(f"{item['price']:.0f}：{item['label']}")
    return resist[:5], support[:5]


def build_strategy_plans(signals: list[TradingSignal]) -> list[dict[str, Any]]:
    labels = ["方案 A（主策略）", "方案 B（备选）", "方案 C（逆势）"]
    plans = []
    for i, sig in enumerate(signals[:3]):
        tps = sig.take_profits
        plans.append({
            "name": labels[i] if i < len(labels) else sig.name,
            "logic": sig.note,
            "entry": f"{sig.entry_low} ~ {sig.entry_high}",
            "stop_loss": sig.stop_loss,
            "targets": " / ".join(str(t) for t in tps),
            "theme": sig.theme,
        })
    return plans


def build_path_summary(projections: list[dict]) -> list[dict[str, Any]]:
    labels = ["路径 A", "路径 B", "路径 C"]
    colors = ["#ef4444", "#22c55e", "#3b82f6"]
    out = []
    for i, p in enumerate(projections[:3]):
        steps = p.get("steps", [])
        desc = " → ".join(f"{s['label']}({s['price']})" for s in steps)
        out.append({
            "id": labels[i],
            "name": p["name"],
            "probability": p["probability"],
            "color": colors[i] if i < len(colors) else p.get("color", "#64748b"),
            "summary": desc,
        })
    return out


def build_report(
    data: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
    *,
    signals: list[TradingSignal] | None = None,
) -> dict[str, Any]:
    df_1d = data["1d"]
    metrics = daily_metrics(df_1d)
    price = metrics["current_price"]

    sentiment = sentiment_score(analyses)
    primary = analyses.get("4h") or analyses.get("1h")
    swing_high = primary.swing_high if primary and primary.swing_high else metrics["daily_high"]
    swing_low = primary.swing_low if primary and primary.swing_low else metrics["daily_low"]

    fib = fibonacci_levels(swing_high, swing_low)
    if signals is None:
        signals = generate_trading_signals(
            price, analyses["5m"], analyses["15m"], swing_high, swing_low, sentiment,
        )
    conclusion = build_conclusion(sentiment, primary.trend if primary else "ranging", signals)

    # EMA relations for each TF
    tf_summary = {}
    for tf in ("1h", "4h", "15m"):
        df = data[tf]
        last = df.iloc[-1]
        tf_summary[tf] = {
            "trend": analyses[tf].trend,
            "bos": analyses[tf].bos,
            "choch": analyses[tf].choch,
            "premium_discount": analyses[tf].premium_discount,
            "equilibrium": analyses[tf].equilibrium,
            "volume_signal": analyses[tf].volume_signal,
            "active_fvg_count": len(analyses[tf].active_fvgs),
            "ema_relation": ema_relation(price, last),
            "order_blocks": [
                {"low": ob.low, "high": ob.high, "direction": ob.direction}
                for ob in analyses[tf].order_blocks[-2:]
            ],
            "fvgs": [
                {"low": fvg.low, "high": fvg.high, "direction": fvg.direction}
                for fvg in analyses[tf].active_fvgs[-3:] or analyses[tf].fvgs[-2:]
            ],
        }

    liquidity = []
    for tf in ("1h", "15m", "5m"):
        for lz in analyses[tf].liquidity:
            liquidity.append({"timeframe": tf, "price": lz.price, "label": lz.label})

    risk_zone = "—"
    short_sigs = [s for s in signals if s.theme == "short"]
    if short_sigs:
        top = max(s.entry_high for s in short_sigs)
        risk_zone = f"{top:.0f}-{top + 18:.0f}"

    projections = trend_projections(price, swing_high, swing_low, sentiment)
    path_summary = build_path_summary(projections)
    key_levels = build_key_levels(price, metrics, swing_high, swing_low, fib, signals)
    resist, support = build_resistance_support(key_levels, liquidity)

    log.info(
        "report built price=%.2f signals=%d sentiment=%s/%s/%s",
        price,
        len(signals),
        sentiment.get("bullish"),
        sentiment.get("bearish"),
        sentiment.get("ranging"),
    )

    indicator_notes: list[str] = []
    for tf in ("5m", "15m"):
        snap = indicator_snapshot(data[tf], tf)
        for note in snap.get("notes", []):
            if note not in indicator_notes:
                indicator_notes.append(note)

    meta_warnings: list[str] = []
    if indicator_notes:
        meta_warnings.extend(indicator_notes)

    return {
        "meta": {
            "symbol": "XAUUSD",
            "title": "XAUUSD 黄金/美元 机构级交易分析报告 (PA + ICT + SMC)",
            "strategy_title": "XAUUSD 黄金 短线交易策略图",
            "strategy_subtitle": "PA + ICT + SMC | 5min / 15min 简版执行策略",
            "updated_at": utc8_now().strftime("%Y-%m-%d %H:%M (UTC+8)"),
            "methodology": "Price Action + ICT + SMC",
            "indicator_notes": indicator_notes,
            "warnings": meta_warnings,
        },
        "metrics": metrics,
        "sentiment": sentiment,
        "conclusion": conclusion,
        "market_overview": build_market_overview(analyses, metrics, conclusion),
        "key_levels": key_levels,
        "resistance_levels": resist,
        "support_levels": support,
        "strategy_plans": build_strategy_plans(signals),
        "path_summary": path_summary,
        "calendar_events": build_calendar_events(),
        "external": {
            "dxy_impact": "偏强 → 利空黄金",
            "risk_events": "美盘数据/讲话 → 波动放大",
        },
        "risk_control": [
            f"最大风险区：{risk_zone} 上方不做空",
            "止损必执行，不扛单、不补仓",
            "分批止盈：TP1 减仓50%，TP2 减仓30%",
        ],
        "footer_reminders": [
            "今日美盘流动性释放时段注意滑点",
            "重要数据/讲话前后缩小仓位或观望",
        ],
        "timeframes": tf_summary,
        "liquidity": liquidity[:8],
        "fibonacci": fib,
        "signals": [asdict(s) for s in signals],
        "projections": projections,
        "invalidation": invalidation_rules(analyses["15m"], swing_high, signals),
        "chart": {
            "timeframe": "1d",
            "swing_high": swing_high,
            "swing_low": swing_low,
        },
    }
