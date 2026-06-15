"""Sentiment Analyst — structure vote + TradingView community mood."""

from __future__ import annotations

from src.analysis.ict_pa import sentiment_score
from src.config import ANALYST_SOCIAL_MAX, TV_SOCIAL_ENABLED
from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext

from src.agents.analysts.base import build_report


def _social_note(ext, post_count: int) -> str:
    social = (ext.social_sentiment or "").strip()
    if social and social != "—":
        return social[:80] + ("…" if len(social) > 80 else "")
    if post_count:
        return f"TV {post_count} 条样本"
    if not TV_SOCIAL_ENABLED:
        return "TV 社媒未启用"
    return "TV Ideas/Minds 暂无数据"


def run_sentiment_analyst(ctx: MarketContext) -> AnalystReport:
    vote = sentiment_score(ctx.analyses)
    ext = ctx.external
    items: list[EvidenceItem] = [
        EvidenceItem(
            category="sentiment",
            summary=f"多周期结构情绪：多 {vote['bullish']:.0f}% / 空 {vote['bearish']:.0f}% / 震荡 {vote['ranging']:.0f}%",
            strength=max(vote["bullish"], vote["bearish"]) / 100,
            refs=vote,
        )
    ]

    for post in ext.social_posts[:ANALYST_SOCIAL_MAX]:
        title = str(post.get("title") or post.get("text") or "")[:120]
        if not title:
            continue
        kind = post.get("kind", "social")
        author = post.get("author", "")
        likes = post.get("likes", 0)
        delta = post.get("bias_delta", 0)
        items.append(
            EvidenceItem(
                category="sentiment",
                summary=f"[{kind}] {title}" + (f" · @{author}" if author else ""),
                strength=min(0.35 + abs(delta) * 0.08 + min(likes, 50) / 200, 0.75),
                refs={"source": "tradingview_social", "bias_delta": delta, "likes": likes},
            )
        )

    if ext.social_sentiment and ext.social_sentiment != "—":
        if not any(ext.social_sentiment[:30] in i.summary for i in items):
            items.append(
                EvidenceItem(
                    category="sentiment",
                    summary=f"社媒汇总：{ext.social_sentiment}",
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

    social_note = _social_note(ext, len(ext.social_posts))
    summary = f"情绪：结构投票 多 {bull:.0f}% / 空 {bear:.0f}% · {social_note}"
    return build_report(agent="sentiment_analyst", items=items, bias=bias, summary=summary)
