"""Trader agent — synthesizes debate + structure into transaction proposal."""

from __future__ import annotations

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

    long_idx = [i for i, s in enumerate(signals) if s.theme == "long"]
    short_idx = [i for i, s in enumerate(signals) if s.theme == "short"]

    if debate.consensus_bias == "bullish" and long_idx:
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
