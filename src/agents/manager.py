"""Manager — final authorization based on risk reviews."""

from __future__ import annotations

from src.core.types import ManagerDecision, RiskReview, TransactionProposal


def _scale_for_indices(reviews: list[RiskReview], indices: list[int]) -> float:
    if not indices:
        return 0.0
    selected = set(indices)
    scales = [
        review.position_scale
        for review in reviews
        if review.approved and selected.intersection(review.allowed_signal_indices)
    ]
    return min(scales) if scales else 0.0


def _evidence_confidence(
    reviews: list[RiskReview],
    proposal: TransactionProposal,
    *,
    action: str,
) -> float:
    """Derive manager confidence from how many risk profiles approved the proposal."""
    approved = sum(1 for review in reviews if review.approved)
    base = {3: 0.78, 2: 0.66, 1: 0.52}.get(approved, 0.35)
    if proposal.debate_bias == "neutral":
        base *= 0.85
    if action == "reduce":
        base *= 0.92
    elif action == "wait":
        return 0.0
    return round(min(0.92, max(0.25, base)), 2)


def run_manager(proposal: TransactionProposal, reviews: list[RiskReview]) -> ManagerDecision:
    neutral = next(r for r in reviews if r.profile == "neutral")
    conservative = next(r for r in reviews if r.profile == "conservative")

    if not proposal.signal_indices or proposal.primary_direction == "wait":
        return ManagerDecision(
            action="wait",
            primary_direction="wait",
            selected_signal_indices=[],
            confidence=0.0,
            summary="经理：无交易提案或风控未通过，维持观望",
            position_scale=0.0,
        )

    if conservative.approved and conservative.allowed_signal_indices:
        selected = conservative.allowed_signal_indices
        action = "reduce"
        summary = "经理：保守风控通过，缩减至主信号执行"
        scale = _scale_for_indices(reviews, selected)
        confidence = _evidence_confidence(reviews, proposal, action=action)
    elif neutral.approved and neutral.allowed_signal_indices:
        selected = neutral.allowed_signal_indices
        action = "execute"
        summary = "经理：中性风控通过，按标准方案执行"
        scale = _scale_for_indices(reviews, selected)
        confidence = _evidence_confidence(reviews, proposal, action=action)
    else:
        aggressive = next(r for r in reviews if r.profile == "aggressive")
        if aggressive.approved:
            selected = aggressive.allowed_signal_indices[:1]
            action = "reduce"
            summary = "经理：仅激进档通过，极小仓位试探"
            scale = _scale_for_indices(reviews, selected)
            confidence = _evidence_confidence(reviews, proposal, action=action)
        else:
            return ManagerDecision(
                action="wait",
                primary_direction=proposal.primary_direction,
                selected_signal_indices=[],
                confidence=0.0,
                summary="经理：三档风控均未通过，取消执行",
                position_scale=0.0,
            )

    return ManagerDecision(
        action=action,
        primary_direction=proposal.primary_direction,
        selected_signal_indices=selected,
        confidence=confidence,
        summary=summary,
        position_scale=scale,
    )
