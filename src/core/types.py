"""Shared data contracts for the Advice V2 pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis

Bias = Literal["bullish", "bearish", "neutral"]


@dataclass
class EvidenceItem:
    """One source-backed fact produced by a market or external data source."""

    category: str
    summary: str
    strength: float
    timeframe: str | None = None
    refs: dict[str, Any] = field(default_factory=dict)
    evidence_id: str | None = None


@dataclass
class HeadlineItem:
    """Structured news headline retained as background context."""

    source: str
    text: str
    time: str = ""
    title: str = ""
    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CalendarEvent:
    """Structured macro-calendar event retained as risk context."""

    time: str
    region: str
    event: str
    importance: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def display(self) -> str:
        return f"{self.time} {self.region} {self.event}".strip()


@dataclass
class MacroQuote:
    """DXY or yield snapshot retained as background context."""

    name: str
    symbol: str
    close: float
    change_pct: float
    impact: str
    bias: Bias
    source: str = "tradingview"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExternalFactors:
    dxy_impact: str = "—"
    risk_events: str = "—"
    news_headlines: list[str] = field(default_factory=list)
    headline_items: list[HeadlineItem] = field(default_factory=list)
    calendar_events: list[CalendarEvent] = field(default_factory=list)
    macro_quotes: list[MacroQuote] = field(default_factory=list)
    social_sentiment: str = "—"
    social_posts: list[dict] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    fetch_errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        from src.config import ANALYST_CALENDAR_MAX, ANALYST_NEWS_MAX, ANALYST_SOCIAL_MAX

        return {
            "dxy_impact": self.dxy_impact,
            "risk_events": self.risk_events,
            "news_headlines": self.news_headlines[:ANALYST_NEWS_MAX],
            "headlines": [h.to_dict() for h in self.headline_items[:ANALYST_NEWS_MAX]],
            "flash_headlines": [
                h.to_dict() for h in self.headline_items if h.source == "jin10_flash"
            ][:ANALYST_NEWS_MAX],
            "article_headlines": [
                h.to_dict() for h in self.headline_items if h.source == "jin10_news"
            ][:ANALYST_NEWS_MAX],
            "calendar": [c.to_dict() for c in self.calendar_events[:ANALYST_CALENDAR_MAX]],
            "macro_quotes": [m.to_dict() for m in self.macro_quotes],
            "social_sentiment": self.social_sentiment,
            "social_posts": self.social_posts[:ANALYST_SOCIAL_MAX],
            "sources": self.sources,
            "fetch_errors": self.fetch_errors[:5],
        }


@dataclass
class MarketContext:
    """Frozen inputs used to produce one human-review suggestion."""

    enriched: dict[str, pd.DataFrame]
    analyses: dict[str, TimeframeAnalysis]
    metrics: dict[str, float]
    price: float
    external: ExternalFactors
    source_label: str
    derived: dict[str, Any] = field(default_factory=dict)
    context_stats: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "price": self.price,
            "metrics": self.metrics,
            "external": self.external.to_dict(),
            "derived": self.derived,
            "context_stats": self.context_stats,
            "source_label": self.source_label,
            "timeframes": list(self.analyses.keys()),
        }


@dataclass
class LLMStageTrace:
    """Audit metadata for the optional Advice V2 wording pass."""

    stage: str
    model: str
    latency_ms: int = 0
    error: str | None = None
    confidence: float | None = None
    tier: str = ""
    attempts: int = 0
    attempt_log: list[dict[str, Any]] = field(default_factory=list)
    input_chars: int = 0
    input_tokens_est: int = 0
    output_chars: int = 0
    output_tokens_est: int = 0
    budget_action: str = "none"
    usage: dict[str, Any] | None = None
    same_model_strategy: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
