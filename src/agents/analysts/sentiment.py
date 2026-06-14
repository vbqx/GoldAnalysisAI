"""Sentiment Analyst — structure vote + TradingView community mood."""

from __future__ import annotations

from src.analysis.ict_pa import sentiment_score
from src.config import TV_SOCIAL_ENABLED
from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext
from src.data.sources.social import SocialDataSource

from src.agents.analysts.base import build_report


def _social_note(ext, social_items: list) -> str:
    social = (ext.social_sentiment or "").strip()
    if social and social != "—":
        return social[:60] + ("…" if len(social) > 60 else "")
    if social_items:
        return f"TV {len(social_items)} 条样本"
    if not TV_SOCIAL_ENABLED:
        return "TV 社媒未启用"
    return "TV Ideas/Minds 暂无数据"


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

    ext = ctx.external
    social_items = SocialDataSource().fetch_evidence()
    for item in social_items:
        if not any(item.summary in i.summary for i in items):
            items.append(item)

    if ext.social_sentiment and ext.social_sentiment != "—":
        if not any(ext.social_sentiment[:30] in i.summary for i in items):
            items.append(
                EvidenceItem(
                    category="sentiment",
                    summary=f"社媒情绪：{ext.social_sentiment}",
                    strength=0.45,
                    refs={"source": "tradingview_social"},
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

    social_note = _social_note(ext, social_items)
    summary = f"情绪：结构投票 多 {bull:.0f}% / 空 {bear:.0f}% · {social_note}"
    return build_report(agent="sentiment_analyst", items=items, bias=bias, summary=summary)
