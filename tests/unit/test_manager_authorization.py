"""Manager authorization mapping into report signals."""

from __future__ import annotations

from src.agents.manager import run_manager
from src.analysis.report_engine import apply_manager_authorization
from src.core.types import ManagerDecision, RiskReview, TransactionProposal


def _minimal_report(signals: list[dict]) -> dict:
    return {
        "signals": signals,
        "sentiment": {"bullish": 80.0, "bearish": 10.0, "ranging": 10.0},
        "strategy_plans": [],
        "meta": {},
    }


def test_manager_selection_is_only_primary_not_sentiment_theme() -> None:
    signals = [
        {"name": "short A", "theme": "short", "status": "candidate", "position_size": "20%"},
        {"name": "long B", "theme": "long", "status": "candidate", "position_size": "30%"},
    ]
    report = _minimal_report(signals)
    proposal = TransactionProposal(
        primary_direction="short",
        signal_indices=[0],
        rationale=["test"],
        debate_bias="bearish",
    )
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, []),
        RiskReview("neutral", True, [0], 0.7, []),
        RiskReview("conservative", True, [0], 0.4, []),
    ]
    decision = run_manager(proposal, reviews)
    apply_manager_authorization(report, decision, reviews)

    roles = {s["name"]: s["signal_role"] for s in report["signals"]}
    assert roles["short A"] == "primary"
    assert roles["long B"] == "rejected"
    assert report["signals"][0]["name"] == "short A"
    assert "40%" in report["signals"][0]["position_size"]


def test_wait_action_clears_executable_plans() -> None:
    report = _minimal_report([{"name": "x", "theme": "long", "status": "candidate", "position_size": "30%"}])
    decision = ManagerDecision(
        action="wait",
        primary_direction="wait",
        selected_signal_indices=[],
        confidence=0.0,
        summary="wait",
        position_scale=0.0,
    )
    apply_manager_authorization(report, decision, [])
    assert report["strategy_plans"] == []
    assert report["signals"][0]["signal_role"] == "rejected"
    assert report["meta"]["execution_authorized"] is False
