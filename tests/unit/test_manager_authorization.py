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
        {
            "name": "short A",
            "theme": "short",
            "status": "active",
            "trigger_confirmed": True,
            "position_size": "20%",
        },
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
    apply_manager_authorization(report, decision, reviews, proposal=proposal)

    roles = {s["name"]: s["signal_role"] for s in report["signals"]}
    assert roles["short A"] == "primary"
    assert roles["long B"] == "rejected"
    assert report["signals"][0]["name"] == "short A"
    assert report["signals"][0]["position_size"] == "缩仓"
    rejected = next(s for s in report["signals"] if s["name"] == "long B")
    assert "主方案" in rejected.get("rejection_reason", "")
    assert "short A" in rejected.get("rejection_reason", "")
    notes = rejected.get("rejection_notes") or []
    assert any("风控[" in n for n in notes)
    assert any("交易员" in n for n in notes)


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
            "status": "active",
            "trigger_confirmed": True,
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


def test_rejection_reason_explains_score_and_direction_gap() -> None:
    from src.analysis.report_engine import build_signal_rejection_notes
    from src.core.types import RiskReview, TransactionProposal

    primary = {
        "name": "LLM路径B·做空",
        "direction": "SELL",
        "score_total": 81.0,
        "score_grade": "A",
    }
    cand = {
        "name": "LLM路径C·做多",
        "direction": "BUY",
        "score_total": 38.0,
        "score_grade": "D",
        "score_reasons": ["逆主结构，结构支持仅 0%"],
    }
    notes = build_signal_rejection_notes(
        cand,
        decision_action="reduce",
        primary_name=primary["name"],
        primary_sig=primary,
        decision_summary="风控意见分歧，优选近端空头",
        decision_confidence=0.65,
        risk_reviews=[
            RiskReview("aggressive", False, [], 0.0, ["market snapshot not executable"]),
            RiskReview("neutral", False, [], 0.0, ["market snapshot not executable"]),
            RiskReview("conservative", False, [], 0.0, ["market snapshot not executable"]),
        ],
        candidate_index=2,
        proposal=TransactionProposal(
            primary_direction="short",
            signal_indices=[0, 1],
            rationale=["顺势近端空头优先"],
            debate_bias="bearish",
        ),
        validated_plans=[
            {
                "accepted": False,
                "reason": "BUY zone above current price",
                "proposal": {"path_id": "C", "direction": "BUY", "entry_low": 38.0},
            }
        ],
    )
    blob = "；".join(notes)
    assert "LLM路径B·做空" in blob
    assert "经理理由" in blob
    assert "风控[激进]否决" in blob
    assert "market snapshot not executable" in blob
    assert "交易员未提名" in blob
    assert "交易员理由" in blob
    assert "评分低于主方案" in blob
    assert "方向与主方案相反" in blob
    assert "逆主结构" in blob


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


def test_untriggered_candidate_keeps_plan_but_not_execution_ready() -> None:
    report = _minimal_report(
        [
            {
                "name": "short A",
                "theme": "short",
                "direction": "SELL",
                "direction_cn": "做空",
                "status": "candidate",
                "trigger_confirmed": False,
                "entry_low": 4067.31,
                "entry_high": 4070.71,
                "stop_loss": 4073.50,
                "take_profits": [4060.0, 4050.0],
                "trigger_note": "需 15m/5m 承压确认",
                "position_size": "30%",
            }
        ]
    )
    decision = ManagerDecision(
        action="reduce",
        primary_direction="short",
        selected_signal_indices=[0],
        confidence=0.7,
        summary="风控同意缩仓",
        position_scale=0.5,
    )
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, []),
        RiskReview("neutral", True, [0], 0.7, []),
        RiskReview("conservative", True, [0], 0.5, []),
    ]

    apply_manager_authorization(report, decision, reviews)
    align_conclusion_with_manager_decision(report)

    assert report["meta"]["plan_authorized"] is True
    assert report["meta"]["execution_ready"] is False
    assert report["meta"]["execution_authorized"] is False
    assert report["meta"]["authorized_position_scale"] == 0.0
    assert report["signals"][0]["signal_role"] == "primary"
    assert report["signals"][0]["position_size"] == "0% 等待触发"
    assert report["strategy_plans"]
    assert report["meta"]["primary_trigger_state"]["trigger_confirmed"] is False
    assert report["meta"]["final_decision"]["verdict_cn"] == "等待触发"
    assert report["meta"]["final_decision"]["execution_authorized"] is False
    assert "等待触发" in report["conclusion"]["header_conclusion"]
    assert "今日决策：执行" not in report["conclusion"]["header_conclusion"]
    assert "今日决策：缩仓执行" not in report["conclusion"]["header_conclusion"]


def test_triggered_active_signal_remains_execution_authorized() -> None:
    report = _minimal_report(
        [
            {
                "name": "short A",
                "theme": "short",
                "direction": "SELL",
                "direction_cn": "做空",
                "status": "active",
                "trigger_confirmed": True,
                "entry_low": 4130.0,
                "entry_high": 4132.0,
                "stop_loss": 4136.0,
                "take_profits": [4120.0, 4110.0],
                "trigger_note": "已承压确认",
                "position_size": "30%",
            }
        ]
    )
    decision = ManagerDecision(
        action="reduce",
        primary_direction="short",
        selected_signal_indices=[0],
        confidence=0.7,
        summary="缩仓执行",
        position_scale=0.5,
    )
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, []),
        RiskReview("neutral", True, [0], 0.7, []),
        RiskReview("conservative", True, [0], 0.5, []),
    ]
    apply_manager_authorization(report, decision, reviews)
    align_conclusion_with_manager_decision(report)

    assert report["meta"]["execution_authorized"] is True
    assert report["meta"]["execution_ready"] is True
    assert report["meta"]["plan_authorized"] is True
    assert report["meta"]["authorized_position_scale"] == 0.5
    assert report["meta"]["final_decision"]["verdict_cn"] == "缩仓执行"
