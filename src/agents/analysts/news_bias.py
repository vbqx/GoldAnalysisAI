"""News / event bias inference from headlines and calendar."""

from __future__ import annotations

from src.core.types import Bias, CalendarEvent, HeadlineItem

_BULLISH = (
    "利好黄金",
    "降息",
    "偏鸽",
    "避险",
    "地缘",
    "冲突",
    "战争",
    "制裁",
    "美元走弱",
    "dovish",
    "rate cut",
    "safe haven",
    "weak dollar",
)

_BEARISH = (
    "利空黄金",
    "加息",
    "偏鹰",
    "美元走强",
    "hawkish",
    "rate hike",
    "strong dollar",
    "非农超预期",
    "cpi超预期",
    "通胀超预期",
)


def infer_news_bias(
    headlines: list[HeadlineItem],
    calendar: list[CalendarEvent],
    *,
    risk_text: str = "",
) -> Bias:
    corpus = " ".join(
        [h.text for h in headlines]
        + [c.event for c in calendar]
        + ([risk_text] if risk_text and risk_text != "—" else [])
    ).lower()

    bull = sum(1 for k in _BULLISH if k.lower() in corpus)
    bear = sum(1 for k in _BEARISH if k.lower() in corpus)
    high_impact = sum(1 for c in calendar if c.importance >= 3.0)

    if high_impact >= 2 and bull == bear:
        return "neutral"  # event risk dominates direction
    if bull > bear + 1:
        return "bullish"
    if bear > bull + 1:
        return "bearish"
    return "neutral"
