"""Social sentiment — Reddit r/Gold + r/Forex."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors
from src.data.sources.social_feed import fetch_social_sentiment


class SocialDataSource:
    name = "social"

    def fetch_external(self) -> ExternalFactors:
        summary, refs = self.fetch_external_summary()
        if summary == "—" or refs.get("source") != "reddit":
            return ExternalFactors()
        return ExternalFactors(social_sentiment=summary)

    def fetch_external_summary(self) -> tuple[str, dict]:
        summary, _posts, refs = fetch_social_sentiment()
        return summary, refs

    def fetch_evidence(self) -> list[EvidenceItem]:
        summary, posts, refs = fetch_social_sentiment()
        if refs.get("source") != "reddit" or summary == "—":
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
            items.append(
                EvidenceItem(
                    category="external",
                    summary=f"r/{post['subreddit']}：{post['title'][:120]}",
                    strength=min(0.35 + post.get("upvote_ratio", 0.5) * 0.3, 0.75),
                    refs={"source": "reddit", "score": post.get("score"), "subreddit": post.get("subreddit")},
                )
            )
        return items
