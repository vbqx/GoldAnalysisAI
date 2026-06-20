"""Shared rule-mode pipeline coherence validation (FIN-INT-03)."""

from __future__ import annotations

from typing import Any

from src.analysis.ict_pa import TimeframeAnalysis
from src.indicators.verify import indicator_snapshot, indicator_table_rows


def _bias_score(bias: str) -> int:
    return {"bearish": -1, "neutral": 0, "bullish": 1}.get(bias, 0)


def validate_pipeline_coherence(
    report: dict[str, Any],
    data: dict[str, Any],
    analyses: dict[str, TimeframeAnalysis],
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Return (issues, notes, summary) for a completed pipeline run."""
    issues: list[str] = []
    notes: list[str] = []

    price = report["metrics"]["current_price"]
    sentiment = report["sentiment"]
    conclusion = report["conclusion"]
    trace = report.get("agent_trace", {})
    debate = trace.get("debate", {})
    team = trace.get("analyst_team", {})

    for tf in ("5m", "15m"):
        snap = indicator_snapshot(data[tf], tf)
        for col in ("RSI14", "MACD", "ADX14", "ATR14", "EMA20", "VWAP"):
            if col not in snap:
                issues.append(f"指标校验缺失 {tf}.{col}")
    notes.append(
        f"指标校验列: {list(indicator_table_rows([indicator_snapshot(data['5m'], '5m')])[0].keys())}"
    )

    tech = team.get("technical", {})
    d1_trend = analyses["1d"].trend
    if d1_trend == "bearish" and tech.get("bias") not in ("bearish", "neutral"):
        issues.append(f"1d trend={d1_trend} 但技术分析师 bias={tech.get('bias')}")
    if d1_trend == "bullish" and tech.get("bias") not in ("bullish", "neutral"):
        issues.append(f"1d trend={d1_trend} 但技术分析师 bias={tech.get('bias')}")

    if sentiment["bearish"] >= sentiment["bullish"]:
        if "偏空" not in conclusion.get("market_sentiment", "") and "空" not in conclusion.get(
            "direction_summary", ""
        ):
            issues.append("空头情绪占优但结论未体现偏空")
    else:
        if "偏多" not in conclusion.get("market_sentiment", "") and "多" not in conclusion.get(
            "direction_summary", ""
        ):
            issues.append("多头情绪占优但结论未体现偏多")

    debate_bias = debate.get("consensus_bias", "")
    sent_bias = "bearish" if sentiment["bearish"] >= sentiment["bullish"] else "bullish"
    if _bias_score(debate_bias) * _bias_score(sent_bias) < 0:
        issues.append(
            f"辩论共识 {debate_bias} 与结构情绪主导 {sent_bias} "
            f"({sentiment['bearish']:.0f}/{sentiment['bullish']:.0f}/{sentiment['ranging']:.0f}) 方向相反"
        )

    bull_conf = float(trace.get("bullish", {}).get("confidence", 0) or 0)
    bear_conf = float(trace.get("bearish", {}).get("confidence", 0) or 0)
    if bear_conf > bull_conf + 0.1 and debate_bias != "bearish":
        issues.append(f"看空置信 {bear_conf:.0%} > 看多 {bull_conf:.0%} 但辩论非 bearish")
    if bull_conf > bear_conf + 0.1 and debate_bias != "bullish":
        issues.append(f"看多置信 {bull_conf:.0%} > 看空 {bear_conf:.0%} 但辩论非 bullish")

    for sig in report.get("signals", []):
        label = sig.get("name") or sig.get("title") or sig.get("direction", "?")
        entry_mid = (sig["entry_low"] + sig["entry_high"]) / 2
        if sig["direction"] == "SELL":
            if sig["take_profits"] and sig["take_profits"][0] > entry_mid:
                issues.append(
                    f"做空信号 {label}: TP1 {sig['take_profits'][0]} 高于入场 {entry_mid:.2f}"
                )
            if sig["stop_loss"] < entry_mid:
                issues.append(
                    f"做空信号 {label}: SL {sig['stop_loss']} 低于入场 {entry_mid:.2f}"
                )
        if sig["direction"] == "BUY":
            if sig["take_profits"] and sig["take_profits"][0] < entry_mid:
                issues.append(
                    f"做多信号 {label}: TP1 {sig['take_profits'][0]} 低于入场 {entry_mid:.2f}"
                )

    swing_high = report["chart"]["swing_high"]
    swing_low = report["chart"]["swing_low"]
    for proj in report.get("projections", []):
        prices = [s["price"] for s in proj["steps"]]
        if max(prices) > swing_high + (swing_high - swing_low) * 0.5:
            issues.append(f"路径 {proj['name']} 目标价超出 swing 合理范围: {max(prices)}")
        if min(prices) < swing_low - (swing_high - swing_low) * 0.5:
            issues.append(f"路径 {proj['name']} 目标价超出 swing 合理范围: {min(prices)}")

    proposal = trace.get("proposal", {})
    if sentiment["bearish"] >= sentiment["bullish"] and proposal.get("primary_direction") == "long":
        if debate_bias != "bullish" or float(debate.get("consensus_strength", 0) or 0) < 0.6:
            issues.append("结构偏空但交易员主方向为 long（F-014）")

    summary = {
        "price": price,
        "sentiment": sentiment,
        "conclusion_mood": conclusion.get("market_sentiment"),
        "debate": {"bias": debate_bias, "strength": debate.get("consensus_strength")},
        "analyst_team": {
            k: team.get(k, {}).get("bias")
            for k in ("technical", "fundamentals", "news", "sentiment")
        },
        "structure": {tf: analyses[tf].trend for tf in ("1d", "4h", "1h", "15m", "5m")},
        "bull_conf": bull_conf,
        "bear_conf": bear_conf,
        "signals": len(report.get("signals", [])),
        "issues": issues,
        "notes": notes,
    }
    return issues, notes, summary
