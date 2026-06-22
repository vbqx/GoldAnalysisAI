"""Trader agent — synthesizes debate + structure into transaction proposal.

Financial review (F-014): ``sentiment_score(ctx.analyses)`` gates direction before
debate branches. When structure is bearish (bear_pct >= bull_pct), short signals are
primary unless debate is strongly bullish (strength >= 0.6). Long signals may still
appear as alternates in ``signal_indices``. Orchestrator then reorders report signals
and sets ``signal_role`` (primary/alternate) for UI badges.
"""

from __future__ import annotations

from src.analysis.ict_pa import sentiment_score
from src.analysis.report_engine import TradingSignal
from src.core.types import MarketContext, ResearchDebate, TransactionProposal


def run_trader_agent(
    ctx: MarketContext,
    debate: ResearchDebate,
    signals: list[TradingSignal],
) -> tuple[TransactionProposal, list[TradingSignal]]:

    rationale = [
        f"研究员共识：{debate.consensus_bias}（强度 {debate.consensus_strength:.0%}）",
        *debate.discussion_notes[-2:],
    ]

    long_idx = [
        i for i, s in enumerate(signals)
        if s.theme == "long" and getattr(s, "status", "candidate") != "invalid"
    ]
    short_idx = [
        i for i, s in enumerate(signals)
        if s.theme == "short" and getattr(s, "status", "candidate") != "invalid"
    ]

    # F-014: structure sentiment gates primary direction; debate only overrides on strong consensus.
    sentiment = sentiment_score(ctx.analyses)
    bull_pct = sentiment.get("bullish", 33)
    bear_pct = sentiment.get("bearish", 33)
    struct_bearish = bear_pct >= bull_pct
    struct_bullish = bull_pct > bear_pct

    strong_debate = debate.consensus_strength >= 0.6

    if struct_bearish and short_idx:
        if (
            debate.consensus_bias == "bearish"
            or debate.consensus_bias != "bullish"
            or not strong_debate
        ):
            primary_dir = "short"
            chosen = short_idx[:2] + long_idx[:1]
            rationale.append("交易员：结构偏空，优先做空方案（做多仅作逆势备选）")
        elif debate.consensus_bias == "bullish" and long_idx:
            primary_dir = "long"
            chosen = long_idx[:1]
            rationale.append("交易员：强多共识下采用做多方案")
        else:
            primary_dir = "short"
            chosen = short_idx[:2]
            rationale.append("交易员：默认采用结构做空方案")
    elif struct_bullish and long_idx:
        if (
            debate.consensus_bias == "bullish"
            or debate.consensus_bias != "bearish"
            or not strong_debate
        ):
            primary_dir = "long"
            chosen = long_idx[:1] + short_idx[:1]
            rationale.append("交易员：结构偏多，优先做多方案（做空仅作逆势备选）")
        elif debate.consensus_bias == "bearish" and short_idx:
            primary_dir = "short"
            chosen = short_idx[:2]
            rationale.append("交易员：强空共识下采用做空方案")
        else:
            primary_dir = "long"
            chosen = long_idx[:1]
            rationale.append("交易员：默认采用结构做多方案")
    elif debate.consensus_bias == "bullish" and long_idx:
        primary_dir = "long"
        chosen = long_idx[:1] + short_idx[:0]
        rationale.append("交易员：优先采用做多方案")
    elif debate.consensus_bias == "bearish" and short_idx:
        primary_dir = "short"
        chosen = short_idx[:2] + long_idx[:1]
        rationale.append("交易员：优先采用做空方案")
    elif short_idx:
        primary_dir = "short"
        chosen = short_idx
        rationale.append("交易员：默认采用结构做空方案（含备选）")
    elif long_idx:
        primary_dir = "long"
        chosen = long_idx
        rationale.append("交易员：无做空区，保留扫低做多备选")
    else:
        primary_dir = "wait"
        chosen = []
        rationale.append("交易员：暂无合格入场区，建议观望")

    return (
        TransactionProposal(
            primary_direction=primary_dir,
            signal_indices=chosen,
            rationale=rationale,
            debate_bias=debate.consensus_bias,
        ),
        signals,
    )
