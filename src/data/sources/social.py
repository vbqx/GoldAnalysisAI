"""Social sentiment — TradingView Ideas + Minds."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors
from src.data.sources.social_feed import fetch_social_sentiment

_TV_SOURCE = "tradingview_social"


class SocialDataSource:
    name = "social"

    def fetch_external(self) -> ExternalFactors:
        summary, posts, refs = fetch_social_sentiment()
        if refs.get("source") == _TV_SOURCE:
            return ExternalFactors(
                social_sentiment=summary,
                social_posts=posts,
                sources=[_TV_SOURCE],
            )
        if refs.get("source") == "disabled":
            return ExternalFactors(social_sentiment="TV 社媒已关闭（TV_SOCIAL_ENABLED=false）")
        if summary and summary != "—":
            return ExternalFactors(social_sentiment=summary, social_posts=posts)
        return ExternalFactors()

    def fetch_external_summary(self) -> tuple[str, dict]:
        summary, _posts, refs = fetch_social_sentiment()
        return summary, refs

    def fetch_evidence(self) -> list[EvidenceItem]:
        summary, posts, refs = fetch_social_sentiment()
        if refs.get("source") != _TV_SOURCE or summary == "—":
            return []

        items: list[EvidenceItem] = [
            EvidenceItem(
                category="external",
                summary=f"社媒情绪：{summary}",
                strength=0.5,
                refs=refs,
            )
        ]
        for post in posts[:4]:
            kind = post.get("kind") or "ideas"
            author = post.get("author") or "—"
            title = str(post.get("title") or "")[:120]
            likes = int(post.get("likes") or 0)
            items.append(
                EvidenceItem(
                    category="external",
                    summary=f"TV {kind} · {author}：{title}",
                    strength=min(0.35 + min(likes, 500) / 500 * 0.35, 0.75),
                    refs={
                        "source": _TV_SOURCE,
                        "kind": kind,
                        "author": author,
                        "likes": likes,
                    },
                )
            )
        return items
