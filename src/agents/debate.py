"""Research debate — bull vs bear discussion → consensus."""

from __future__ import annotations

from src.analysis.ict_pa import sentiment_score
from src.core.types import AgentEvidence, Bias, ResearchDebate


def run_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses) -> ResearchDebate:
    notes: list[str] = []
    bull_score = bullish.confidence * max(len(bullish.items), 1)
    bear_score = bearish.confidence * max(len(bearish.items), 1)

    sentiment = sentiment_score(analyses)
    bull_pct = sentiment.get("bullish", 33)
    bear_pct = sentiment.get("bearish", 33)

    notes.append(f"看多研究员：{bullish.summary}")
    notes.append(f"看空研究员：{bearish.summary}")
    notes.append(f"多周期技术投票：多 {bull_pct:.0f}% / 空 {bear_pct:.0f}% / 震荡 {sentiment.get('ranging', 0):.0f}%")

    combined_bull = bull_score + bull_pct / 100
    combined_bear = bear_score + bear_pct / 100

    if abs(combined_bull - combined_bear) < 0.15:
        bias: Bias = "neutral"
        strength = 0.5
        notes.append("讨论结论：多空证据接近，倾向震荡/等待确认")
    elif combined_bull > combined_bear:
        bias = "bullish"
        strength = min(combined_bull / (combined_bull + combined_bear + 0.01), 1.0)
        notes.append("讨论结论：看多证据占优，但需关注上方流动性")
    else:
        bias = "bearish"
        strength = min(combined_bear / (combined_bull + combined_bear + 0.01), 1.0)
        notes.append("讨论结论：看空证据占优，关注反抽卖区")

    return ResearchDebate(
        bullish=bullish,
        bearish=bearish,
        consensus_bias=bias,
        consensus_strength=strength,
        discussion_notes=notes,
    )
