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


@dataclass
class AgentEvidence:
    agent: str
    direction: Bias
    items: list[EvidenceItem]
    confidence: float
    summary: str

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

    def to_dict(self) -> dict[str, Any]:
        return {
            "bullish": self.bullish.to_dict(),
            "bearish": self.bearish.to_dict(),
            "consensus_bias": self.consensus_bias,
            "consensus_strength": self.consensus_strength,
            "discussion_notes": self.discussion_notes,
        }


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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExternalFactors:
    dxy_impact: str = "—"
    risk_events: str = "—"
    news_headlines: list[str] = field(default_factory=list)
    social_sentiment: str = "—"

    def to_dict(self) -> dict[str, str | list[str]]:
        return {
            "dxy_impact": self.dxy_impact,
            "risk_events": self.risk_events,
            "news_headlines": self.news_headlines,
            "social_sentiment": self.social_sentiment,
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "price": self.price,
            "metrics": self.metrics,
            "external": self.external.to_dict(),
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
    debate: dict[str, Any]
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
