"""LLM trader/risk/manager stage contracts."""

from __future__ import annotations

from unittest.mock import patch

from src.agents import factory as agent_factory
from src.agents.llm.schemas import (
    parse_manager_decision,
    parse_risk_reviews,
    parse_transaction_proposal,
)
from src.core.types import AgentPipelineMeta, LevelProposal, LLMStageTrace, ManagerDecision, RiskReview, TransactionProposal
from tests._run_config_helpers import bind_run_config


def test_parse_transaction_proposal_filters_unknown_indexes() -> None:
    proposal = parse_transaction_proposal(
        {
            "primary_direction": "short",
            "signal_indices": [0, 5, "1", 1],
            "rationale": ["short bias", "valid zone"],
        },
        debate_bias="bearish",
        signal_count=2,
    )

    assert proposal.primary_direction == "short"
    assert proposal.signal_indices == [0, 1]
    assert proposal.debate_bias == "bearish"


def test_parse_risk_reviews_requires_three_profiles_and_filters_indexes() -> None:
    proposal = TransactionProposal(
        primary_direction="short",
        signal_indices=[0, 1],
        rationale=["test"],
        debate_bias="bearish",
    )
    reviews = parse_risk_reviews(
        {
            "reviews": [
                {"profile": "aggressive", "approved": True, "allowed_signal_indices": [0, 9], "position_scale": 1.5},
                {"profile": "neutral", "approved": True, "allowed_signal_indices": [1], "position_scale": 0.7},
                {"profile": "conservative", "approved": False, "allowed_signal_indices": [0], "position_scale": 0.4},
            ]
        },
        proposal=proposal,
        signal_count=2,
    )

    assert [r.profile for r in reviews] == ["aggressive", "neutral", "conservative"]
    assert reviews[0].allowed_signal_indices == [0]
    assert reviews[0].position_scale == 1.0
    assert reviews[2].approved is False
    assert reviews[2].position_scale == 0.0


def test_parse_manager_decision_uses_only_approved_indexes() -> None:
    proposal = TransactionProposal(
        primary_direction="long",
        signal_indices=[0, 1],
        rationale=["test"],
        debate_bias="bullish",
    )
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, ["ok"]),
        RiskReview("neutral", False, [], 0.0, ["no"]),
        RiskReview("conservative", False, [], 0.0, ["no"]),
    ]

    decision = parse_manager_decision(
        {"action": "execute", "selected_signal_indices": [1, 0], "confidence": 0.8, "summary": "go small"},
        proposal=proposal,
        reviews=reviews,
    )

    assert decision.action == "execute"
    assert decision.selected_signal_indices == [0]
    assert decision.confidence == 0.8


def test_factory_trader_hybrid_accepts_high_confidence_llm(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "LLM_OVERRIDE_THRESHOLD", 0.65)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    llm_proposal = TransactionProposal(
        primary_direction="long",
        signal_indices=[1],
        rationale=["LLM selected long"],
        debate_bias="bullish",
    )

    def fake_rule(_ctx, _debate, signals):
        return (
            TransactionProposal("short", [0], ["rule selected short"], "bearish"),
            signals,
        )

    def fake_llm(_ctx, _debate, _signals, team=None):
        return llm_proposal, LLMStageTrace(stage="trader", model="test", confidence=0.9)

    with bind_run_config(agent_mode="hybrid", llm_enabled=True, llm_stage_trader=True), patch.object(
        agent_factory, "rule_trader", side_effect=fake_rule
    ), patch.object(
        agent_factory, "run_llm_trader", side_effect=fake_llm
    ):
        meta = AgentPipelineMeta()
        proposal, signals = agent_factory.run_trader(None, None, meta, ["s0", "s1"])  # type: ignore[arg-type]

    assert proposal is llm_proposal
    assert signals == ["s0", "s1"]
    assert meta.stages["trader"].source == "hybrid"


def test_factory_trader_runs_llm_in_observation_mode(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    llm_proposal = TransactionProposal(
        primary_direction="short",
        signal_indices=[0],
        rationale=["LLM short"],
        debate_bias="bearish",
    )

    with bind_run_config(agent_mode="llm", llm_enabled=True, llm_stage_trader=True), patch.object(
        agent_factory,
        "rule_trader",
        return_value=(TransactionProposal("short", [0], ["rule"], "bearish"), ["s0"]),
    ), patch.object(
        agent_factory,
        "run_llm_trader",
        return_value=(llm_proposal, LLMStageTrace(stage="trader", model="test", confidence=0.9)),
    ):
        meta = AgentPipelineMeta()
        proposal, signals = agent_factory.run_trader(
            None,
            None,
            meta,
            ["s0"],
            observation_mode=True,
        )  # type: ignore[arg-type]

    assert proposal is llm_proposal
    assert meta.stages["trader"].source == "llm"
    assert signals == ["s0"]


def test_factory_risk_runs_llm_then_gates_observation_mode(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    proposal = TransactionProposal("short", [0], ["test"], "bearish")
    llm_reviews = [
        RiskReview("aggressive", True, [0], 1.0, ["LLM ok"]),
        RiskReview("neutral", True, [0], 0.7, ["LLM ok"]),
        RiskReview("conservative", True, [0], 0.4, ["LLM ok"]),
    ]

    with bind_run_config(agent_mode="llm", llm_enabled=True, llm_stage_risk=True), patch.object(
        agent_factory,
        "rule_risk",
        return_value=[RiskReview("aggressive", False, [], 0.0, ["rule blocked"])],
    ), patch.object(
        agent_factory,
        "run_llm_risk",
        return_value=(llm_reviews, LLMStageTrace(stage="risk", model="test", confidence=0.9)),
    ):
        meta = AgentPipelineMeta()
        reviews = agent_factory.run_risk(
            proposal,
            [{"direction": "SELL", "theme": "short", "entry_low": 4130.0, "entry_high": 4132.0, "stop_loss": 4140.0, "take_profits": [4120.0]}],
            meta,
            current_price=4120.0,
            data_as_of={"executable": False, "data_age_hours": 40},
            observation_mode=True,
        )

    assert meta.stages["risk"].source == "llm"
    assert all(not review.approved for review in reviews)


def test_factory_manager_llm_mode_accepts_llm(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    proposal = TransactionProposal("short", [0], ["test"], "bearish")
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, ["ok"]),
        RiskReview("neutral", True, [0], 0.7, ["ok"]),
        RiskReview("conservative", False, [], 0.0, ["no"]),
    ]
    llm_decision = ManagerDecision("execute", "short", [0], 0.8, "execute")

    with bind_run_config(agent_mode="llm", llm_enabled=True, llm_stage_manager=True), patch.object(
        agent_factory, "run_llm_manager", return_value=(llm_decision, LLMStageTrace("manager", "test"))
    ):
        meta = AgentPipelineMeta()
        decision = agent_factory.run_manager(proposal, reviews, meta)

    assert decision is llm_decision
    assert meta.stages["manager"].source == "llm"


def test_factory_level_proposer_disabled_returns_empty(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: False)
    meta = AgentPipelineMeta()
    result = agent_factory.run_level_proposer(None, None, None, meta, [])  # type: ignore[arg-type]
    assert result == []
    assert meta.stages["llm_levels"].source == "rule"


def test_factory_level_proposer_accepts_llm_proposals(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)
    proposals = [
        LevelProposal(
            direction="BUY",
            entry_low=2650.0,
            entry_high=2652.0,
            stop_loss=2640.0,
            take_profits=[2665.0],
            setup_type="ob",
            reason="test zone",
            confidence=0.8,
        )
    ]
    trace = LLMStageTrace(stage="llm_levels", model="test")

    with bind_run_config(agent_mode="llm", llm_enabled=True, llm_stage_levels=True), patch.object(
        agent_factory, "run_llm_level_proposer", return_value=(proposals, trace)
    ):
        meta = AgentPipelineMeta()
        result = agent_factory.run_level_proposer(None, None, None, meta, [])  # type: ignore[arg-type]

    assert result is proposals
    assert meta.stages["llm_levels"].source == "llm"


def test_factory_level_proposer_falls_back_when_llm_empty(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)
    trace = LLMStageTrace(stage="llm_levels", model="test", error="no proposals")

    with bind_run_config(agent_mode="hybrid", llm_enabled=True, llm_stage_levels=True), patch.object(
        agent_factory, "run_llm_level_proposer", return_value=(None, trace)
    ):
        meta = AgentPipelineMeta()
        result = agent_factory.run_level_proposer(None, None, None, meta, [])  # type: ignore[arg-type]

    assert result == []
    assert meta.stages["llm_levels"].source == "rule"


def test_orchestrator_levels_not_skipped_in_observation_mode() -> None:
    """LLM level proposer must run in observation mode (same as trader/risk)."""
    from tests._bootstrap import ROOT

    src = (ROOT / "src" / "core" / "orchestrator.py").read_text(encoding="utf-8")
    start = src.index("llm_level_proposals = []")
    block = src[start : start + 700]
    assert "not observation_mode" not in block
    assert "run_level_proposer" in block
