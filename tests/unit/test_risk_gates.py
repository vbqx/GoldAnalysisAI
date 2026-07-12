"""Deterministic risk gate tests."""

from __future__ import annotations

from src.analysis.risk_gates import apply_risk_gates, validate_signal_geometry
from src.core.types import RiskReview, TransactionProposal


def _long_signal(**overrides) -> dict:
    base = {
        "theme": "long",
        "direction": "BUY",
        "entry_low": 2650.0,
        "entry_high": 2652.0,
        "stop_loss": 2640.0,
        "take_profits": [2665.0, 2680.0],
        "status": "active",
    }
    base.update(overrides)
    return base


def test_validate_signal_geometry_passes_valid_long() -> None:
    assert validate_signal_geometry(_long_signal(), current_price=2651.0) == []


def test_validate_signal_geometry_blocks_bad_stop() -> None:
    issues = validate_signal_geometry(_long_signal(stop_loss=2660.0), current_price=2651.0)
    assert any("stop" in issue for issue in issues)


def test_apply_risk_gates_rejects_negative_index() -> None:
    proposal = TransactionProposal(
        primary_direction="long",
        signal_indices=[0],
        rationale=["test"],
        debate_bias="bullish",
    )
    reviews = [
        RiskReview("neutral", True, [-1], 0.7, []),
    ]
    signals = [_long_signal(), _long_signal(entry_low=2700.0, entry_high=2702.0, stop_loss=2690.0)]
    gated = apply_risk_gates(
        reviews,
        proposal,
        signals,
        current_price=2651.0,
        data_as_of={"executable": True},
        observation_mode=False,
    )
    assert not gated[0].approved
    assert gated[0].allowed_signal_indices == []


def test_apply_risk_gates_veto_in_observation_mode() -> None:
    proposal = TransactionProposal(
        primary_direction="long",
        signal_indices=[0],
        rationale=["test"],
        debate_bias="bullish",
    )
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, []),
        RiskReview("neutral", True, [0], 0.7, []),
        RiskReview("conservative", True, [0], 0.4, []),
    ]
    gated = apply_risk_gates(
        reviews,
        proposal,
        [_long_signal()],
        current_price=2651.0,
        data_as_of={"executable": False},
        observation_mode=True,
    )
    assert all(not review.approved for review in gated)
    assert all(review.position_scale == 0.0 for review in gated)
