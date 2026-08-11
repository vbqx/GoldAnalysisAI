"""Stable output contract for human-reviewed trading suggestions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

AdviceDecision = Literal["WAIT", "WATCH_LONG", "WATCH_SHORT", "AVOID"]
AdviceBias = Literal["bullish", "bearish", "mixed", "neutral"]
AdviceConfidence = Literal["low", "medium", "high"]


@dataclass
class AdviceEvidence:
    evidence_id: str
    kind: str
    statement: str
    timeframe: str = ""
    source: str = ""
    price: float | None = None


@dataclass
class AttentionZone:
    low: float
    high: float
    label: str


@dataclass
class AdviceSetup:
    direction: Literal["BUY", "SELL"]
    attention_zone: AttentionZone
    current_state: str
    rationale: list[str]
    confirmation_checklist: list[str]
    invalidation: str
    invalidation_level: float
    targets: list[float]
    evidence_ids: list[str]
    reward_risk_to_targets: list[float] = field(default_factory=list)


@dataclass
class AlternativeScenario:
    condition: str
    response: str


@dataclass
class AdviceAudit:
    passed: bool = True
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    policy_version: str = "human-advice-v2"


@dataclass
class AdvicePacket:
    decision: AdviceDecision
    bias: AdviceBias
    confidence: AdviceConfidence
    horizon: str
    summary: str
    current_price: float
    primary_setup: AdviceSetup | None
    alternative_scenario: AlternativeScenario | None
    market_context: list[str]
    risks: list[str]
    uncertainties: list[str]
    evidence: list[AdviceEvidence]
    audit: AdviceAudit = field(default_factory=AdviceAudit)
    schema_version: str = "2.0"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
