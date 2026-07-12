"""Deterministic manager/risk chain stability (no LLM)."""

from __future__ import annotations

from src.agents.manager import run_manager
from src.agents.risk import run_risk_team
from src.analysis.report_engine import apply_manager_authorization
from src.core.types import TransactionProposal


def _run_chain() -> dict:
    signals = [
        {
            "name": "short A",
            "theme": "short",
            "direction": "SELL",
            "status": "active",
            "entry_low": 2660.0,
            "entry_high": 2662.0,
            "stop_loss": 2670.0,
            "take_profits": [2645.0, 2630.0],
        },
        {
            "name": "long B",
            "theme": "long",
            "direction": "BUY",
            "status": "candidate",
            "entry_low": 2640.0,
            "entry_high": 2642.0,
            "stop_loss": 2630.0,
            "take_profits": [2655.0],
        },
    ]
    proposal = TransactionProposal(
        primary_direction="short",
        signal_indices=[0],
        rationale=["structure bearish"],
        debate_bias="bearish",
    )
    reviews = run_risk_team(
        proposal,
        len(signals),
        signals=signals,
        current_price=2661.0,
        data_as_of={"executable": True, "data_age_hours": 1.0},
        observation_mode=False,
    )
    decision = run_manager(proposal, reviews)
    report = {"signals": [dict(s) for s in signals], "strategy_plans": [], "meta": {}}
    apply_manager_authorization(report, decision, reviews)
    primary = next(s for s in report["signals"] if s.get("signal_role") == "primary")
    return {
        "action": decision.action,
        "selected": tuple(decision.selected_signal_indices),
        "signal_id": primary.get("signal_id"),
        "position_size": primary.get("position_size"),
        "confidence": decision.confidence,
    }


def test_manager_chain_identical_across_five_runs() -> None:
    baseline = _run_chain()
    for _ in range(4):
        assert _run_chain() == baseline
