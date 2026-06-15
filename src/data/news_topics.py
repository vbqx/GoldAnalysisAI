"""Cluster Jin10 headlines into macro themes for debate / derived context."""

from __future__ import annotations

from src.core.types import HeadlineItem

_TOPIC_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("地缘与避险", ("地缘", "冲突", "战争", "以色列", "伊朗", "避险", "袭击", "停火", "制裁")),
    ("美联储与利率", ("美联储", "联储", "利率", "降息", "加息", "powell", "fomc", "沃什")),
    ("通胀与就业", ("cpi", "ppi", "非农", "就业", "失业", "通胀", "pce", "adp")),
    ("美元与汇率", ("美元", "dxy", "汇率", "美债", "收益率", "us10y", "国债")),
    ("原油与商品", ("原油", "oil", "白银", "silver", "铜", "商品", "石油")),
    ("黄金专题", ("黄金", "金价", "xau", "贵金属", "gold")),
]


def cluster_headline_topics(
    items: list[HeadlineItem],
    *,
    max_topics: int = 3,
) -> list[dict[str, object]]:
    """Rule-based topic buckets from headline text."""
    buckets: dict[str, list[str]] = {name: [] for name, _ in _TOPIC_RULES}
    for item in items:
        text = item.text.lower()
        for name, keywords in _TOPIC_RULES:
            if any(k.lower() in text for k in keywords):
                buckets[name].append(item.text[:120])
                break

    topics: list[dict[str, object]] = []
    for name, samples in buckets.items():
        if not samples:
            continue
        topics.append(
            {
                "topic": name,
                "count": len(samples),
                "samples": samples[:3],
            }
        )
    topics.sort(key=lambda t: int(t["count"]), reverse=True)
    return topics[:max_topics]
