"""Shared types for the TradeAgent-style pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

import pandas as pd

from src.analysis.ict_pa import TimeframeAnalysis

Bias = Literal["bullish", "bearish", "neutral"]
RiskProfile = Literal["aggressive", "neutral", "conservative"]
StageSource = Literal["rule", "llm", "hybrid"]


@dataclass
class EvidenceItem:
    """Single fact derived from a data source or structure engine."""

    category: str  # market | structure | liquidity | external
    summary: str
    strength: float  # 0.0 – 1.0
    timeframe: str | None = None
    refs: dict[str, Any] = field(default_factory=dict)
    evidence_id: str | None = None


@dataclass
class AnalystReport:
    """Specialist analyst output (TradingAgents-style Analyst Team)."""

    agent: str  # technical_analyst | fundamentals_analyst | news_analyst | sentiment_analyst
    bias: Bias
    items: list[EvidenceItem]
    confidence: float
    summary: str
    # Technical analyst: reaction hypotheses at POC / VA / S/R (consumed by level proposer).
    level_reactions: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["items"] = [asdict(i) for i in self.items]
        return d


@dataclass
class AnalystTeam:
    """Four specialist reports consumed by bull/bear researchers."""

    technical: AnalystReport
    fundamentals: AnalystReport
    news: AnalystReport
    sentiment: AnalystReport

    @property
    def reports(self) -> list[AnalystReport]:
        return [self.technical, self.fundamentals, self.news, self.sentiment]

    def to_dict(self) -> dict[str, Any]:
        return {
            "technical": self.technical.to_dict(),
            "fundamentals": self.fundamentals.to_dict(),
            "news": self.news.to_dict(),
            "sentiment": self.sentiment.to_dict(),
        }


@dataclass
class AgentEvidence:
    agent: str
    direction: Bias
    items: list[EvidenceItem]
    confidence: float
    summary: str
    provenance_meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["items"] = [asdict(i) for i in self.items]
        return d


@dataclass
class ResearchDebate:
    bullish: AgentEvidence
    bearish: AgentEvidence
    consensus_bias: Bias
    consensus_strength: float
    discussion_notes: list[str]
    debate_meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bullish": self.bullish.to_dict(),
            "bearish": self.bearish.to_dict(),
            "consensus_bias": self.consensus_bias,
            "consensus_strength": self.consensus_strength,
            "discussion_notes": self.discussion_notes,
            "debate_meta": self.debate_meta,
        }


@dataclass
class LevelProposal:
    """LLM proposed trade level, before deterministic validation."""

    direction: Literal["BUY", "SELL"]
    entry_low: float
    entry_high: float
    stop_loss: float
    take_profits: list[float]
    setup_type: str
    reason: str
    confidence: float
    invalidation: str = ""
    path_id: str = ""
    source: str = "llm"
    # Bind to technical analyst level_reactions (short order rationale, not full TA).
    anchor_level: str = ""
    expected_reaction: str = ""
    deduction: str = ""
    reaction_evidence_id: str = ""
    # Issue #36: claim → fact → quality → eligibility (filled at validation).
    claim_id: str = ""
    fact_ids: list[str] = field(default_factory=list)
    claim_eligibility: str = ""
    claim_quality: dict[str, Any] = field(default_factory=dict)
    counterevidence: list[dict[str, Any]] = field(default_factory=list)
    claim_policy_version: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TransactionProposal:
    primary_direction: Literal["long", "short", "wait"]
    signal_indices: list[int]
    rationale: list[str]
    debate_bias: Bias

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RiskReview:
    profile: RiskProfile
    approved: bool
    allowed_signal_indices: list[int]
    position_scale: float  # 1.0 = full, 0.5 = half
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ManagerDecision:
    action: Literal["execute", "reduce", "wait"]
    primary_direction: str
    selected_signal_indices: list[int]
    confidence: float
    summary: str
    position_scale: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HeadlineItem:
    """Structured news headline for Analyst Team payloads."""

    source: str  # jin10_flash | jin10_news
    text: str
    time: str = ""
    title: str = ""
    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CalendarEvent:
    """Structured macro calendar row."""

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
    """DXY / yields snapshot for fundamentals analyst."""

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
    """All inputs available to the agent team."""

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
    """Per-stage LLM call audit metadata."""

    stage: str
    model: str
    latency_ms: int = 0
    error: str | None = None
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StageMeta:
    """Records which implementation produced a pipeline stage output."""

    source: StageSource
    fallback_reason: str | None = None
    llm: LLMStageTrace | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"source": self.source}
        if self.fallback_reason:
            d["fallback_reason"] = self.fallback_reason
        if self.llm:
            d["llm"] = self.llm.to_dict()
        return d


@dataclass
class AgentPipelineMeta:
    """Collects per-stage source metadata for agent_trace."""

    stages: dict[str, StageMeta] = field(default_factory=dict)

    def record(self, name: str, meta: StageMeta) -> None:
        self.stages[name] = meta

    def to_dict(self) -> dict[str, Any]:
        return {k: v.to_dict() for k, v in self.stages.items()}


@dataclass
class AgentTrace:
    """Full audit trail — stored in report under agent_trace (UI optional)."""

    context: dict[str, Any]
    analyst_team: dict[str, Any]
    debate: dict[str, Any]
    llm_levels: list[dict[str, Any]]
    validated_plans: list[dict[str, Any]]
    proposal: dict[str, Any]
    risk_reviews: list[dict[str, Any]]
    decision: dict[str, Any]
    llm: dict[str, Any] | None = None
    stage_meta: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LLMAnalysis:
    """Optional LLM narrative layer (default disabled)."""

    enabled: bool = False
    model: str = ""
    provider: str = ""
    market_summary: str = ""
    trade_thesis: str = ""
    action_plan: str = ""
    risks: list[str] = field(default_factory=list)
    watch_levels: list[str] = field(default_factory=list)
    confidence: float = 0.0
    raw_response: str | None = None
    error: str | None = None
    narrative_sections: dict[str, Any] = field(default_factory=dict)
    narrative_section_audit: dict[str, Any] = field(default_factory=dict)
    top_level_audit: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
