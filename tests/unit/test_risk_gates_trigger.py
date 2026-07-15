"""Risk gate trigger readiness for conditional plans."""

from __future__ import annotations

from src.analysis.risk_gates import apply_risk_gates, signal_trigger_ready
from src.core.types import RiskReview, TransactionProposal


def test_signal_trigger_ready_requires_confirmed_flag() -> None:
    assert signal_trigger_ready({"status": "candidate", "trigger_confirmed": False}) is False
    assert signal_trigger_ready({"status": "active", "trigger_confirmed": True}) is True
    assert signal_trigger_ready({"status": "invalid", "trigger_confirmed": True}) is False


def test_risk_gates_zero_scale_when_trigger_pending() -> None:
    signals = [
        {
            "name": "cand",
            "theme": "short",
            "direction": "SELL",
            "status": "candidate",
            "trigger_confirmed": False,
            "entry_low": 4067.0,
            "entry_high": 4070.0,
            "stop_loss": 4074.0,
            "take_profits": [4060.0, 4050.0],
        }
    ]
    proposal = TransactionProposal(
        primary_direction="short",
        signal_indices=[0],
        rationale=["t"],
        debate_bias="bearish",
    )
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, []),
        RiskReview("neutral", True, [0], 0.7, []),
        RiskReview("conservative", True, [0], 0.5, []),
    ]
    gated = apply_risk_gates(
        reviews,
        proposal,
        signals,
        current_price=4072.0,
        data_as_of={"executable": True, "data_age_hours": 0.1},
    )
    for review in gated:
        assert 0 in review.allowed_signal_indices
        assert review.position_scale == 0.0
        assert any("trigger" in n for n in review.notes)
