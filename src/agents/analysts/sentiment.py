"""Sentiment Analyst — structure vote + social mood (placeholder)."""

from __future__ import annotations

from src.analysis.ict_pa import sentiment_score
from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext
from src.data.sources.social import SocialDataSource

from src.agents.analysts.base import build_report


def run_sentiment_analyst(ctx: MarketContext) -> AnalystReport:
    vote = sentiment_score(ctx.analyses)
    items: list[EvidenceItem] = [
        EvidenceItem(
            category="sentiment",
            summary=f"多周期结构情绪：多 {vote['bullish']:.0f}% / 空 {vote['bearish']:.0f}% / 震荡 {vote['ranging']:.0f}%",
            strength=max(vote["bullish"], vote["bearish"]) / 100,
            refs=vote,
        )
    ]

    social_items = SocialDataSource().fetch_evidence()
    items.extend(social_items)

    ext = ctx.external
    if ext.social_sentiment and ext.social_sentiment != "—":
        items.append(
            EvidenceItem(
                category="sentiment",
                summary=f"社媒情绪：{ext.social_sentiment}",
                strength=0.45,
            )
        )

    bull = vote["bullish"]
    bear = vote["bearish"]
    if abs(bull - bear) < 10:
        bias: Bias = "neutral"
    elif bull > bear:
        bias = "bullish"
    else:
        bias = "bearish"

    social_note = "社媒数据待接入" if not social_items else f"社媒 {len(social_items)} 条"
    summary = f"情绪：结构投票偏多 {bull:.0f}% / 偏空 {bear:.0f}% · {social_note}"
    return build_report(agent="sentiment_analyst", items=items, bias=bias, summary=summary)
