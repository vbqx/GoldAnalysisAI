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


def _social_bias_delta(posts: list[dict]) -> float:
    total = 0.0
    for post in posts:
        try:
            total += float(post.get("bias_delta") or 0)
        except (TypeError, ValueError):
            continue
    return total


def _sentiment_context_evidence(ctx: MarketContext, vote: dict[str, float]) -> list[EvidenceItem]:
    """Capture sample quality and structure/social disagreement for auditability."""
    ext = ctx.external
    items: list[EvidenceItem] = []

    trends = {tf: analysis.trend for tf, analysis in ctx.analyses.items()}
    if len(set(trends.values())) > 1:
        trend_text = " · ".join(f"{tf}:{trend}" for tf, trend in sorted(trends.items()))
        items.append(
            EvidenceItem(
                category="sentiment",
                summary=f"多周期结构分歧：{trend_text}",
                strength=0.35,
                refs={"source": "structure_sentiment", "trends": trends},
            )
        )

    post_count = len(ext.social_posts)
    if post_count:
        kind_counts: dict[str, int] = {}
        likes_total = 0
        for post in ext.social_posts:
            kind = str(post.get("kind") or "social")
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
            try:
                likes_total += int(post.get("likes") or 0)
            except (TypeError, ValueError):
                continue
        avg_likes = likes_total / post_count if post_count else 0
        items.append(
            EvidenceItem(
                category="sentiment",
                summary=f"社媒样本质量：{post_count} 条 · 平均 likes {avg_likes:.1f}",
                strength=0.35 + min(post_count / max(ANALYST_SOCIAL_MAX, 1), 1.0) * 0.25,
                refs={
                    "source": "tradingview_social",
                    "post_count": post_count,
                    "kind_counts": kind_counts,
                    "avg_likes": round(avg_likes, 2),
                },
            )
        )

    social_delta = _social_bias_delta(ext.social_posts)
    if social_delta:
        direction = "偏多" if social_delta > 0 else "偏空"
        items.append(
            EvidenceItem(
                category="sentiment",
                summary=f"社媒方向汇总：{direction} delta {social_delta:+.1f}",
                strength=min(0.35 + abs(social_delta) * 0.06, 0.7),
                refs={"source": "tradingview_social", "bias_delta_sum": round(social_delta, 3)},
            )
        )

    if ext.fetch_errors:
        social_errors = [err for err in ext.fetch_errors if "social" in err.lower() or "tv" in err.lower()]
        if social_errors:
            items.append(
                EvidenceItem(
                    category="sentiment",
                    summary=f"情绪数据源告警：{social_errors[0][:160]}",
                    strength=0.2,
                    refs={"source": "fetch_errors", "errors": social_errors[:3]},
                )
            )

    return items


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
    items.extend(_sentiment_context_evidence(ctx, vote))

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
    social_delta = _social_bias_delta(ext.social_posts)
    if abs(bull - bear) < 10:
        if abs(social_delta) >= 2:
            bias: Bias = "bullish" if social_delta > 0 else "bearish"
        else:
            bias = "neutral"
    elif bull > bear:
        bias = "bullish"
    else:
        bias = "bearish"

    social_note = _social_note(ext, len(ext.social_posts))
    summary = f"情绪：结构投票 多 {bull:.0f}% / 空 {bear:.0f}% · 社媒delta {social_delta:+.1f} · {social_note}"
    return build_report(agent="sentiment_analyst", items=items, bias=bias, summary=summary)
