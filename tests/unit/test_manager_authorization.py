"""Manager authorization mapping into report signals."""

from __future__ import annotations

from src.agents.manager import run_manager
from src.analysis.report_engine import (
    align_conclusion_with_manager_decision,
    apply_manager_authorization,
)
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
    assert report["signals"][0]["position_size"] == "缩仓"


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


def test_wait_aligns_conclusion_with_manager_decision() -> None:
    report = _minimal_report([{"name": "x", "theme": "long", "status": "candidate", "position_size": "30%"}])
    report["conclusion"] = {
        "direction_summary": "主方向偏多，关注回调支撑",
        "action": "不追空，优先等待回调至需求区做多",
        "header_conclusion": "主方向偏多。不追空，优先等待回调至需求区做多",
    }
    decision = ManagerDecision(
        action="wait",
        primary_direction="wait",
        selected_signal_indices=[],
        confidence=0.0,
        summary="风控未通过，维持观望",
        position_scale=0.0,
    )
    apply_manager_authorization(report, decision, [])
    align_conclusion_with_manager_decision(report)

    assert "今日决策：观望" in report["conclusion"]["header_conclusion"]
    assert "暂不执行" in report["conclusion"]["action"]
    assert report["conclusion"]["direction_summary"] == "结构背景：主方向偏多，关注回调支撑"
    assert report["conclusion"]["direction_summary"] != report["conclusion"]["header_conclusion"]
    assert report["conclusion"]["structure_direction_summary"] == "主方向偏多，关注回调支撑"
    assert report["meta"]["final_decision"]["execution_authorized"] is False


def test_execute_aligns_conclusion_with_primary_plan() -> None:
    report = _minimal_report([
        {
            "name": "short A",
            "theme": "short",
            "direction_cn": "做空",
            "status": "candidate",
            "entry_low": 4130.0,
            "entry_high": 4132.0,
            "trigger_note": "反弹至阻力区触发",
            "position_size": "30%",
        },
    ])
    report["conclusion"] = {"direction_summary": "old", "action": "old", "header_conclusion": "old"}
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
    align_conclusion_with_manager_decision(report)

    header = report["conclusion"]["header_conclusion"]
    assert "今日决策" in header
    assert "4130-4132" in header
    assert report["conclusion"]["direction_summary"] == "反弹至阻力区触发"
    assert report["conclusion"]["direction_summary"] != header
    assert report["meta"]["final_decision"]["execution_authorized"] is True
    assert report["meta"]["final_decision"]["primary_plan"]["zone"] == "4130-4132"


def test_observation_mode_blocks_execution_despite_execute_decision() -> None:
    report = _minimal_report([{"name": "short A", "theme": "short", "status": "candidate", "position_size": "30%"}])
    report["meta"]["observation_mode"] = True
    decision = ManagerDecision(
        action="execute",
        primary_direction="short",
        selected_signal_indices=[0],
        confidence=0.8,
        summary="LLM wanted execute",
        position_scale=0.7,
    )
    reviews = [RiskReview("neutral", True, [0], 0.7, [])]

    apply_manager_authorization(report, decision, reviews)

    assert report["meta"]["execution_authorized"] is False
    assert report["signals"][0]["signal_role"] == "rejected"
    assert report["strategy_plans"] == []
