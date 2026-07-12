"""Risk management team — aggressive / neutral / conservative reviews."""

from __future__ import annotations

from typing import Any

from src.analysis.risk_gates import apply_risk_gates
from src.core.types import RiskProfile, RiskReview, TransactionProposal


def _review(
    profile: RiskProfile,
    proposal: TransactionProposal,
    signal_count: int,
) -> RiskReview:
    notes: list[str] = []
    if proposal.primary_direction == "wait":
        return RiskReview(
            profile=profile,
            approved=False,
            allowed_signal_indices=[],
            position_scale=0.0,
            notes=["无有效提案，风控建议观望"],
        )

    if profile == "aggressive":
        allowed = proposal.signal_indices[:]
        scale = 1.0
        notes.append("激进：允许全部提案信号，标准仓位")
    elif profile == "neutral":
        allowed = proposal.signal_indices[:2]
        scale = 0.7
        notes.append("中性：最多 2 个信号，缩仓档")
    else:
        allowed = proposal.signal_indices[:1]
        scale = 0.4
        notes.append("保守：仅主信号，试探档")

    allowed = [i for i in allowed if i < signal_count]

    if not allowed:
        approved = False
    elif proposal.debate_bias == "neutral":
        approved = False
        notes.append("共识震荡 — 各档暂不通过，等待方向确认")
        if profile == "conservative":
            allowed = allowed[:1]
    else:
        approved = True

    return RiskReview(
        profile=profile,
        approved=approved,
        allowed_signal_indices=allowed,
        position_scale=scale,
        notes=notes,
    )


def run_risk_team(
    proposal: TransactionProposal,
    signal_count: int,
    *,
    signals: list[Any] | None = None,
    current_price: float = 0.0,
    data_as_of: dict[str, Any] | None = None,
    observation_mode: bool = False,
) -> list[RiskReview]:
    reviews = [
        _review("aggressive", proposal, signal_count),
        _review("neutral", proposal, signal_count),
        _review("conservative", proposal, signal_count),
    ]
    if signals is None:
        return reviews
    return apply_risk_gates(
        reviews,
        proposal,
        signals,
        current_price=current_price,
        data_as_of=data_as_of,
        observation_mode=observation_mode,
    )
