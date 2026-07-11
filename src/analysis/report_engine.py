"""Report assembly: trading plans, conclusions, projections."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.analysis.proximity import (
    EXEC_ATR_MULT,
    SWING_ATR_MULT,
    level_near_price,
    zone_near_price,
)
from src.core.types import MarketContext
from src.config import RISK_REWARD_DISPLAY_CAP, SIGNAL_SL_BELOW_SWING, SIGNAL_SWEEP_OFFSET
from src.analysis.narrative_sections import build_rule_narrative_sections, overview_bullets_from_sections
from src.analysis.plan_signals import (
    build_pa_long_sweep,
    build_pa_short_aggressive,
    build_pa_short_conservative,
    build_rule_pa_block,
    pa_usable,
    smc_filter_adjustment,
)
from src.analysis.price_action_facts import build_price_action_summaries
from src.analysis.report_facts import build_liquidity_entries, build_tf_summaries
from src.data.fetcher import daily_metrics, utc8_now
from src.indicators.technical import fibonacci_levels
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
    setup_type: str = ""
    status: str = "candidate"  # candidate | watch | active | invalid
    trigger_confirmed: bool = False
    trigger_note: str = "等待触发确认"
    score_total: float = 0.0
    score_grade: str = "C"
    score_reasons: list[str] = field(default_factory=list)


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


def _risk_reward_ratio(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    stop_loss: float,
    take_profits: list[float],
) -> float:
    if not take_profits:
        return 0.0
    entry_mid = (entry_low + entry_high) / 2
    tp1 = take_profits[0]
    if direction == "SELL":
        risk = stop_loss - entry_mid
        reward = entry_mid - tp1
    else:
        risk = entry_mid - stop_loss
        reward = tp1 - entry_mid
    if risk <= 0 or reward <= 0:
        return 0.0
    return reward / risk


def _grade(score: float) -> str:
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def _zone_relation(
    *,
    price: float,
    direction: str,
    entry_low: float,
    entry_high: float,
) -> tuple[str, float]:
    if direction == "SELL":
        if entry_high < price:
            return "passed", (entry_high - price) / price * 100
        if entry_low <= price <= entry_high:
            return "inside", 0.0
        return "ahead", (entry_low - price) / price * 100
    if entry_low > price:
        return "passed", (price - entry_low) / price * 100
    if entry_low <= price <= entry_high:
        return "inside", 0.0
    return "ahead", (price - entry_high) / price * 100


def _stop_breached(*, price: float, direction: str, stop_loss: float) -> bool:
    """True when the current price has already crossed the plan invalidation stop."""
    if direction == "SELL":
        return price >= stop_loss
    return price <= stop_loss


def _setup_status_and_score(
    *,
    name: str,
    direction: str,
    theme: str,
    setup_type: str,
    price: float,
    entry_low: float,
    entry_high: float,
    stop_loss: float,
    take_profits: list[float],
    sentiment: dict[str, float],
    trigger_confirmed: bool = False,
) -> tuple[str, bool, str, float, str, list[str]]:
    relation, distance_pct = _zone_relation(
        price=price,
        direction=direction,
        entry_low=entry_low,
        entry_high=entry_high,
    )
    rr = _risk_reward_ratio(
        direction=direction,
        entry_low=entry_low,
        entry_high=entry_high,
        stop_loss=stop_loss,
        take_profits=take_profits,
    )
    stop_breached = _stop_breached(price=price, direction=direction, stop_loss=stop_loss)

    reasons: list[str] = []
    aligned_pct = sentiment.get("bearish" if theme == "short" else "bullish", 0.0)
    opposite_pct = sentiment.get("bullish" if theme == "short" else "bearish", 0.0)

    structure_score = min(aligned_pct / 100 * 35, 35)
    if aligned_pct >= opposite_pct:
        reasons.append(f"结构方向支持 {aligned_pct:.0f}%")
    else:
        reasons.append(f"逆主结构，结构支持仅 {aligned_pct:.0f}%")

    if relation == "passed":
        location_score = 6
        reasons.append("候选区已被现价越过，等待重新确认")
    elif relation == "inside":
        location_score = 18
        reasons.append("价格正在候选区内，等待触发信号")
    elif 0 <= distance_pct <= 1.2:
        location_score = 20
        reasons.append(f"候选区距现价 {distance_pct:.2f}%")
    else:
        location_score = 12
        reasons.append(f"候选区距现价较远 {distance_pct:.2f}%")

    rr_score = 20 if rr >= 1.5 else 12 if rr >= 1.0 else 4
    reasons.append(f"几何盈亏比约 1:{rr:.1f}" if rr else "几何盈亏比无效")

    trigger_score = 20 if trigger_confirmed else 6
    if trigger_confirmed:
        trigger_note = "触发确认已满足"
        reasons.append("已有触发确认")
    elif "liquidity_sweep" in setup_type or "pa_val_sweep" in setup_type:
        trigger_note = "等待扫低流动性后收回 + 5m 结构转强"
        reasons.append("尚未确认 sweep + reclaim")
    elif direction == "SELL":
        trigger_note = "等待反抽失败 + 5m 收盘重新走弱"
        reasons.append("尚未确认反抽失败")
    else:
        trigger_note = "等待回踩支撑后转强"
        reasons.append("尚未确认回踩转强")

    score = round(structure_score + location_score + rr_score + trigger_score, 1)

    if stop_breached:
        status = "invalid"
        trigger_confirmed = False
        trigger_note = "现价已突破止损/失效价，等待重新生成计划"
        reasons.append(f"现价 {price:.2f} 已越过止损 {stop_loss:.2f}")
        score = min(score, 35)
    elif rr <= 0:
        status = "invalid"
        score = min(score, 35)
    elif trigger_confirmed:
        status = "active"
    elif relation == "inside":
        status = "watch"
    else:
        status = "candidate"

    if name == "右侧扫低做多" and not trigger_confirmed:
        status = "candidate"

    return status, trigger_confirmed, trigger_note, score, _grade(score), reasons


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
    price_action = build_price_action_summaries(ctx.enriched)
    return generate_trading_signals(
        ctx.price,
        analyses["5m"],
        analyses["15m"],
        swing_high,
        swing_low,
        sentiment,
        price_action=price_action,
        metrics=ctx.metrics,
    )


def _apply_smc_filter_score(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
    score: float,
    reasons: list[str],
) -> tuple[float, str, list[str]]:
    filt = smc_filter_adjustment(
        direction=direction,
        entry_low=entry_low,
        entry_high=entry_high,
        analysis_5m=analysis_5m,
        analysis_15m=analysis_15m,
    )
    score = max(0.0, min(100.0, round(score + filt.bonus, 1)))
    reasons.extend(filt.reasons)
    return score, _grade(score), reasons


def _finalize_pa_plan_meta(
    *,
    rule_fallback: bool,
    setup_type: str,
    zone_label: str,
    score: float,
    grade: str,
    reasons: list[str],
    short_note: str | None = None,
) -> tuple[str, str, float, str, list[str]]:
    if rule_fallback:
        setup_type = f"rule_{setup_type}"
        note = short_note or f"规则 PA：{zone_label}（DGT 不足，价位锚点回退；SMC 仅过滤）"
        score = max(0.0, round(score - 8.0, 1))
        reasons = [*reasons, "DGT 量价不足，规则 PA 回退 (-8)"]
        grade = _grade(score)
        return setup_type, note, score, grade, reasons
    if short_note:
        return setup_type, short_note, score, grade, reasons
    return setup_type, f"PA 主：{zone_label}（SMC 仅过滤）", score, grade, reasons


def generate_trading_signals(
    price: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
    swing_high: float,
    swing_low: float,
    sentiment: dict[str, float],
    *,
    price_action: dict[str, Any] | None = None,
    metrics: dict[str, Any] | None = None,
) -> list[TradingSignal]:
    if pa_usable(price_action):
        pa_signals = _generate_pa_signals(
            price,
            analysis_5m,
            analysis_15m,
            swing_high,
            swing_low,
            sentiment,
            price_action=price_action or {},
        )
        if pa_signals:
            return pa_signals

    rule_pa = {
        "5m": build_rule_pa_block(
            price=price,
            swing_high=swing_high,
            swing_low=swing_low,
            analysis_5m=analysis_5m,
            price_action=price_action,
            metrics=metrics,
        )
    }
    return _generate_pa_signals(
        price,
        analysis_5m,
        analysis_15m,
        swing_high,
        swing_low,
        sentiment,
        price_action=rule_pa,
        rule_fallback=True,
    )


def _generate_pa_signals(
    price: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
    swing_high: float,
    swing_low: float,
    sentiment: dict[str, float],
    *,
    price_action: dict[str, Any],
    rule_fallback: bool = False,
) -> list[TradingSignal]:
    signals: list[TradingSignal] = []
    bear_pct = int(sentiment.get("bearish", 62))
    bull_pct = int(sentiment.get("bullish", 28))
    pa5 = price_action.get("5m") or {}
    atr = analysis_5m.atr or analysis_15m.atr or 5.0

    agg = build_pa_short_aggressive(
        price=price,
        pa_block=pa5,
        swing_low=swing_low,
        atr=atr,
    )
    if agg:
        zone, sl, tps = agg
        el, eh = zone.entry_low, zone.entry_high
        rr = _compute_risk_reward(
            direction="SELL",
            entry_low=el,
            entry_high=eh,
            stop_loss=sl,
            take_profits=tps,
        )
        if rr != "N/A":
            status, trigger_ok, trigger_note, score, grade, reasons = _setup_status_and_score(
                name="激进反抽做空",
                direction="SELL",
                theme="short",
                setup_type="pa_resistance_short",
                price=price,
                entry_low=el,
                entry_high=eh,
                stop_loss=sl,
                take_profits=tps,
                sentiment=sentiment,
            )
            score, grade, reasons = _apply_smc_filter_score(
                direction="SELL",
                entry_low=el,
                entry_high=eh,
                analysis_5m=analysis_5m,
                analysis_15m=analysis_15m,
                score=score,
                reasons=reasons,
            )
            setup_type, note, score, grade, reasons = _finalize_pa_plan_meta(
                rule_fallback=rule_fallback,
                setup_type="pa_resistance_short",
                zone_label=zone.label,
                score=score,
                grade=grade,
                reasons=reasons,
                short_note=f"规则 PA：反弹至{zone.label}做空（SMC 仅过滤）" if rule_fallback else f"PA 主：反弹至{zone.label}做空（SMC 仅过滤）",
            )
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
                    note=note,
                    theme="short",
                    setup_type=setup_type,
                    status=status,
                    trigger_confirmed=trigger_ok,
                    trigger_note=trigger_note,
                    score_total=score,
                    score_grade=grade,
                    score_reasons=reasons,
                )
            )

    cons = build_pa_short_conservative(
        price=price,
        pa_block=pa5,
        swing_low=swing_low,
        atr=atr,
    )
    if cons:
        zone, sl, tps = cons
        el, eh = zone.entry_low, zone.entry_high
        rr = _compute_risk_reward(
            direction="SELL",
            entry_low=el,
            entry_high=eh,
            stop_loss=sl,
            take_profits=tps,
        )
        if rr != "N/A":
            status, trigger_ok, trigger_note, score, grade, reasons = _setup_status_and_score(
                name="保守反抽做空",
                direction="SELL",
                theme="short",
                setup_type="pa_vah_short",
                price=price,
                entry_low=el,
                entry_high=eh,
                stop_loss=sl,
                take_profits=tps,
                sentiment=sentiment,
            )
            score, grade, reasons = _apply_smc_filter_score(
                direction="SELL",
                entry_low=el,
                entry_high=eh,
                analysis_5m=analysis_5m,
                analysis_15m=analysis_15m,
                score=score,
                reasons=reasons,
            )
            setup_type, note, score, grade, reasons = _finalize_pa_plan_meta(
                rule_fallback=rule_fallback,
                setup_type="pa_vah_short",
                zone_label=zone.label,
                score=score,
                grade=grade,
                reasons=reasons,
                short_note=f"规则 PA：{zone.label}做空（SMC 仅过滤）" if rule_fallback else f"PA 主：{zone.label}做空（SMC OB/CHoCH 仅过滤）",
            )
            signals.append(
                TradingSignal(
                    name="保守反抽做空",
                    direction="SELL",
                    direction_cn="卖出",
                    entry_low=el,
                    entry_high=eh,
                    stop_loss=sl,
                    take_profits=tps,
                    risk_reward=rr,
                    sentiment_bias_pct=f"{max(bear_pct - 5, 45)}%",
                    position_size="20% 标准仓",
                    note=note,
                    theme="short",
                    setup_type=setup_type,
                    status=status,
                    trigger_confirmed=trigger_ok,
                    trigger_note=trigger_note,
                    score_total=score,
                    score_grade=grade,
                    score_reasons=reasons,
                )
            )

    long_setup = build_pa_long_sweep(
        price=price,
        pa_block=pa5,
        swing_high=swing_high,
        swing_low=swing_low,
        analysis_5m=analysis_5m,
        analysis_15m=analysis_15m,
    )
    if long_setup:
        zone, sl, tps, sweep_confirmed, sweep_reasons = long_setup
        el, eh = zone.entry_low, zone.entry_high
        rr = _compute_risk_reward(
            direction="BUY",
            entry_low=el,
            entry_high=eh,
            stop_loss=sl,
            take_profits=tps,
        )
        status, trigger_ok, trigger_note, score, grade, reasons = _setup_status_and_score(
            name="右侧扫低做多",
            direction="BUY",
            theme="long",
            setup_type="pa_val_sweep_long",
            price=price,
            entry_low=el,
            entry_high=eh,
            stop_loss=sl,
            take_profits=tps,
            sentiment=sentiment,
            trigger_confirmed=sweep_confirmed,
        )
        reasons.extend(sweep_reasons)
        score, grade, reasons = _apply_smc_filter_score(
            direction="BUY",
            entry_low=el,
            entry_high=eh,
            analysis_5m=analysis_5m,
            analysis_15m=analysis_15m,
            score=score,
            reasons=reasons,
        )
        if sweep_confirmed:
            score = min(100.0, round(score + 5.0, 1))
            grade = _grade(score)
            reasons.append("PA 扫低收回已确认 (+5)")
        setup_type, note, score, grade, reasons = _finalize_pa_plan_meta(
            rule_fallback=rule_fallback,
            setup_type="pa_val_sweep_long",
            zone_label=zone.label,
            score=score,
            grade=grade,
            reasons=reasons,
        )
        signals.append(
            TradingSignal(
                name="右侧扫低做多",
                direction="BUY",
                direction_cn="买入",
                entry_low=el,
                entry_high=eh,
                stop_loss=sl,
                take_profits=tps,
                risk_reward=rr,
                sentiment_bias_pct=f"{bull_pct}%",
                position_size="15% 逆势轻仓",
                note=note,
                theme="long",
                setup_type=setup_type,
                status=status,
                trigger_confirmed=trigger_ok,
                trigger_note=trigger_note,
                score_total=score,
                score_grade=grade,
                score_reasons=reasons,
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


def _build_context_levels(
    price: float,
    swing_high: float,
    swing_low: float,
    swing_tf: str,
    swing_atr: float | None,
) -> list[dict[str, Any]]:
    """Structure levels kept for decision reference but too far for the 5m execution chart."""
    levels: list[dict[str, Any]] = []
    tf_label = swing_tf.upper()
    if not level_near_price(swing_low, price, swing_atr, atr_mult=SWING_ATR_MULT):
        levels.append(
            {
                "timeframe": swing_tf,
                "price_low": round(swing_low - 5, 2),
                "price_high": round(swing_low, 2),
                "price": round(swing_low, 2),
                "label": f"远位需求/摆动低点 ({tf_label})",
                "kind": "support",
                "role": "context",
            }
        )
    if not level_near_price(swing_high, price, swing_atr, atr_mult=SWING_ATR_MULT):
        levels.append(
            {
                "timeframe": swing_tf,
                "price": round(swing_high, 2),
                "label": f"远位供应/摆动高点 ({tf_label})",
                "kind": "resistance",
                "role": "context",
            }
        )
    return levels


def build_key_levels(
    price: float,
    metrics: dict,
    swing_high: float,
    swing_low: float,
    fib: list[dict],
    signals: list[TradingSignal],
    *,
    swing_tf: str = "4h",
    swing_atr: float | None = None,
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
    support_label = (
        "下方支撑"
        if zone_near_price(price, swing_low, swing_low + 12, swing_atr, atr_mult=SWING_ATR_MULT)
        else f"远位支撑 ({swing_tf.upper()})"
    )
    support_role = "execution" if support_label == "下方支撑" else "context"
    levels.append({
        "price_low": swing_low,
        "price_high": swing_low + 12,
        "label": support_label,
        "kind": "support",
        "role": support_role,
        "timeframe": swing_tf,
    })

    return sorted(levels, key=lambda x: -(x.get("price") or x.get("price_high", 0)))


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
    _support_kinds = {"swing_low", "strong_low", "weak_low"}
    for item in liquidity[:5]:
        kind = item.get("kind", "")
        line = f"{item['price']:.0f}：{item['label']}"
        if kind in _support_kinds:
            support.append(line)
        else:
            resist.append(line)
    return resist[:5], support[:5]


def _signal_value(signal: TradingSignal | dict[str, Any], key: str, default: Any = None) -> Any:
    if isinstance(signal, dict):
        return signal.get(key, default)
    return getattr(signal, key, default)


def _assign_signal_roles(signals: list[TradingSignal], sentiment: dict[str, float]) -> None:
    """Mark one primary plan by dominant sentiment theme; rest are alternates."""
    pref_theme = "short" if sentiment.get("bearish", 0) >= sentiment.get("bullish", 0) else "long"
    primary_set = False
    for sig in signals:
        if not primary_set and sig.theme == pref_theme and sig.status != "invalid":
            sig.signal_role = "primary"
            primary_set = True
        else:
            sig.signal_role = "alternate"


def build_strategy_plans(signals: list[TradingSignal | dict[str, Any]]) -> list[dict[str, Any]]:
    labels = ["方案 A（主策略）", "方案 B（备选）", "方案 C（逆势）"]
    plans = []
    eligible = [s for s in signals if _signal_value(s, "status", "candidate") != "invalid"]
    for i, sig in enumerate(eligible[:3]):
        tps = _signal_value(sig, "take_profits", []) or []
        name = _signal_value(sig, "name", "")
        plans.append({
            "name": labels[i] if i < len(labels) else name,
            "logic": _signal_value(sig, "note", ""),
            "entry": f"{_signal_value(sig, 'entry_low')} ~ {_signal_value(sig, 'entry_high')}",
            "stop_loss": _signal_value(sig, "stop_loss"),
            "targets": " / ".join(str(t) for t in tps),
            "theme": _signal_value(sig, "theme"),
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
    primary_tf = "4h" if analyses.get("4h") else "1h"
    swing_high = primary.swing_high if primary and primary.swing_high else metrics["daily_high"]
    swing_low = primary.swing_low if primary and primary.swing_low else metrics["daily_low"]
    swing_atr = primary.atr if primary else None

    fib = fibonacci_levels(swing_high, swing_low)
    price_action = build_price_action_summaries(data)
    if signals is None:
        signals = generate_trading_signals(
            price,
            analyses["5m"],
            analyses["15m"],
            swing_high,
            swing_low,
            sentiment,
            price_action=price_action,
            metrics=metrics,
        )
    _assign_signal_roles(signals, sentiment)
    conclusion = build_conclusion(sentiment, primary.trend if primary else "ranging", signals)

    tf_summary = build_tf_summaries(data, analyses, price=price)

    liquidity = build_liquidity_entries(
        analyses,
        price=price,
        swing_tf=primary_tf,
        swing_atr=swing_atr,
    )

    context_levels = _build_context_levels(price, swing_high, swing_low, primary_tf, swing_atr)

    risk_zone = "—"
    short_sigs = [s for s in signals if s.theme == "short"]
    if short_sigs:
        top = max(s.entry_high for s in short_sigs)
        risk_zone = f"{top:.0f}-{top + 18:.0f}"

    projections = trend_projections(price, swing_high, swing_low, sentiment)
    path_summary = build_path_summary(projections)
    key_levels = build_key_levels(
        price, metrics, swing_high, swing_low, fib, signals,
        swing_tf=primary_tf, swing_atr=swing_atr,
    )
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

    report = {
        "meta": {
            "symbol": "XAUUSD",
            "title": "XAUUSD 黄金/美元 机构级交易分析报告 (LuxAlgo SMC)",
            "strategy_title": "XAUUSD 黄金 短线交易策略图",
            "strategy_subtitle": "LuxAlgo SMC | 5min / 15min 简版执行策略",
            "updated_at": utc8_now().strftime("%Y-%m-%d %H:%M (UTC+8)"),
            "methodology": "LuxAlgo Smart Money Concepts",
            "indicator_notes": indicator_notes,
            "warnings": meta_warnings,
        },
        "metrics": metrics,
        "sentiment": sentiment,
        "conclusion": conclusion,
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
        "price_action": price_action,
        "liquidity": liquidity[:10],
        "context_levels": context_levels,
        "fibonacci": fib,
        "signals": [asdict(s) for s in signals],
        "projections": projections,
        "invalidation": invalidation_rules(analyses["15m"], swing_high, signals),
        "chart": {
            "timeframe": primary_tf,
            "swing_tf": primary_tf,
            "swing_high": swing_high,
            "swing_low": swing_low,
            "swing_atr": swing_atr,
            "exec_atr": analyses["5m"].atr,
            "macro_atr": analyses["15m"].atr,
            "swing_low_near": zone_near_price(
                price, swing_low - 5, swing_low, swing_atr, atr_mult=SWING_ATR_MULT,
            ),
            "swing_high_near": level_near_price(
                swing_high, price, swing_atr, atr_mult=SWING_ATR_MULT,
            ),
            "overlay_policy": "nearest_lux_internal_ob_visible_fvg",
        },
    }
    report["narrative_sections"] = build_rule_narrative_sections(report)
    report["market_overview"] = overview_bullets_from_sections(report["narrative_sections"])
    return report
