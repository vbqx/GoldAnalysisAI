"""Report assembly: trading plans, conclusions, projections."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.data.fetcher import daily_metrics, utc8_now
from src.indicators.technical import ema_relation, fibonacci_levels


@dataclass
class TradingSignal:
    name: str
    direction: str
    entry_low: float
    entry_high: float
    stop_loss: float
    take_profits: list[float]
    risk_reward: str
    note: str


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


def generate_trading_signals(
    price: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
    swing_high: float,
    swing_low: float,
) -> list[TradingSignal]:
    signals: list[TradingSignal] = []

    bear_fvgs = analysis_5m.fvgs + analysis_15m.fvgs
    bear_obs = [ob for ob in analysis_5m.order_blocks + analysis_15m.order_blocks if ob.direction == "bearish"]
    bull_obs = [ob for ob in analysis_5m.order_blocks + analysis_15m.order_blocks if ob.direction == "bullish"]

    # Aggressive sell near nearest bearish FVG / rally zone
    fvg_zone = _nearest_zone(price, bear_fvgs, "bearish")
    if fvg_zone:
        entry_low, entry_high = fvg_zone[0], fvg_zone[1]
        sl = entry_high + (entry_high - entry_low) * 0.5
        tp1 = price - (entry_high - price) * 1.5
        tp2 = swing_low
        signals.append(
            TradingSignal(
                name="激进做空",
                direction="SELL",
                entry_low=round(entry_low, 2),
                entry_high=round(entry_high, 2),
                stop_loss=round(sl, 2),
                take_profits=[round(tp1, 2), round(tp2, 2)],
                risk_reward="1:2.5 ~ 1:4",
                note="反弹至 FVG / 流动性回补后做空",
            )
        )

    # Conservative sell at higher OB
    if bear_obs:
        ob = sorted(bear_obs, key=lambda o: o.low)[-1]
        signals.append(
            TradingSignal(
                name="保守做空",
                direction="SELL",
                entry_low=round(ob.low, 2),
                entry_high=round(ob.high, 2),
                stop_loss=round(ob.high + (ob.high - ob.low), 2),
                take_profits=[round(swing_low, 2)],
                risk_reward="1:2 ~ 1:3",
                note="更高时间框架 Order Block 反弹做空",
            )
        )

    # Counter-trend long after liquidity sweep
    if bull_obs or swing_low:
        sweep_low = swing_low - 3
        signals.append(
            TradingSignal(
                name="扫低反弹做多 (逆势)",
                direction="BUY",
                entry_low=round(sweep_low, 2),
                entry_high=round(swing_low, 2),
                stop_loss=round(swing_low - 8, 2),
                take_profits=[round(price, 2), round(swing_high * 0.5 + price * 0.5, 2)],
                risk_reward="1:1.5 ~ 1:2",
                note="流动性扫低后短多，严格止损",
            )
        )

    return signals


def trend_projections(
    price: float,
    swing_high: float,
    swing_low: float,
    sentiment: dict[str, float],
) -> list[dict[str, Any]]:
    mid_rally = swing_low + (swing_high - swing_low) * 0.382
    deep_rally = swing_low + (swing_high - swing_low) * 0.618

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
    if sentiment["bearish"] >= sentiment["bullish"]:
        mood = "偏弱 / 偏空"
        direction = "主方向偏空，当前可能处于逆势反弹阶段"
        action = "不追多，优先等待反弹至阻力区做空"
    else:
        mood = "偏强 / 偏多"
        direction = "主方向偏多，关注回调支撑"
        action = "不追空，优先等待回调至需求区做多"

    if signals:
        first = signals[0]
        zone = f"{first.entry_low}-{first.entry_high}"
        action += f"；关注 {zone} 区域"

    return {
        "market_sentiment": mood,
        "direction_summary": direction,
        "action": action,
        "must_do": [
            "严格设置止损，不扛单",
            "关注 DXY 与美盘数据波动",
            "15min 结构破坏时立即重新评估",
        ],
    }


def invalidation_rules(analysis_15m: TimeframeAnalysis, swing_high: float) -> list[str]:
    rules = [
        f"15min 收盘价站稳 {round(swing_high, 2)} 上方 → 空头失效",
        "出现 Higher High + Higher Low 结构 → 趋势转多",
        "价格有效填补所有 bearish FVG 并延续 → 降低做空优先级",
    ]
    if analysis_15m.events:
        for e in analysis_15m.events:
            if e.kind == "CHoCH" and e.direction == "bullish":
                rules.insert(0, f"已出现 15min Bullish CHoCH @ {e.price:.2f}")
    return rules


def build_report(
    data: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
) -> dict[str, Any]:
    df_1d = data["1d"]
    df_5m = data["5m"]
    metrics = daily_metrics(df_1d)
    price = metrics["current_price"]

    sentiment = sentiment_score(analyses)
    primary = analyses.get("4h") or analyses.get("1h")
    swing_high = primary.swing_high if primary and primary.swing_high else metrics["daily_high"]
    swing_low = primary.swing_low if primary and primary.swing_low else metrics["daily_low"]

    fib = fibonacci_levels(swing_high, swing_low)
    signals = generate_trading_signals(price, analyses["5m"], analyses["15m"], swing_high, swing_low)
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

    return {
        "meta": {
            "symbol": "XAUUSD",
            "title": "XAUUSD Gold/USD Institutional Grade Analysis Report (PA + ICT)",
            "updated_at": utc8_now().strftime("%Y-%m-%d %H:%M (UTC+8)"),
            "methodology": "Price Action + ICT (MVP rules)",
        },
        "metrics": metrics,
        "sentiment": sentiment,
        "conclusion": conclusion,
        "timeframes": tf_summary,
        "liquidity": liquidity[:8],
        "fibonacci": fib,
        "signals": [asdict(s) for s in signals],
        "projections": trend_projections(price, swing_high, swing_low, sentiment),
        "invalidation": invalidation_rules(analyses["15m"], swing_high),
        "chart": {
            "timeframe": "1h",
            "swing_high": swing_high,
            "swing_low": swing_low,
        },
    }
