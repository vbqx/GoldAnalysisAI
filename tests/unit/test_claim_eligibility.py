"""Issue #36: conflicting/uncalibrated tech claims cannot drive execution."""

from __future__ import annotations

import pandas as pd

from src.analysis.claim_eligibility import (
    CLAIM_POLICY_VERSION,
    adjudicate_level_proposal_claim,
    claim_allows_execution_authorization,
)
from src.analysis.ict_pa import FairValueGap, OrderBlock, TimeframeAnalysis
from src.analysis.level_validator import validate_llm_levels
from src.analysis.report_engine import apply_manager_authorization, align_conclusion_with_manager_decision
from src.analysis.report_invariants import validate_report_invariants
from src.core.types import ExternalFactors, LevelProposal, ManagerDecision, MarketContext, RiskReview


def _analysis_with_fvgs(
    tf: str,
    *,
    atr: float,
    fvgs: list[FairValueGap],
) -> TimeframeAnalysis:
    return TimeframeAnalysis(
        timeframe=tf,
        trend="bearish",
        bos="",
        choch="",
        atr=atr,
        fvgs=list(fvgs),
        active_fvgs=list(fvgs),
    )


def _wide_fvg_ctx(*, ob_low: float | None = None, ob_high: float | None = None) -> MarketContext:
    ts = pd.Timestamp("2026-07-14 15:00", tz="UTC")
    fvg = FairValueGap(high=4070.7, low=4067.3, direction="bearish", time=ts)
    obs = []
    if ob_low is not None and ob_high is not None:
        obs.append(OrderBlock(high=ob_high, low=ob_low, direction="bearish", time=ts))
    analyses = {
        "1h": _analysis_with_fvgs("1h", atr=4.8, fvgs=[fvg]),
        "5m": TimeframeAnalysis(
            timeframe="5m",
            trend="bearish",
            bos="",
            choch="",
            atr=3.0,
            order_blocks=obs,
        ),
    }
    return MarketContext(
        enriched={},
        analyses=analyses,
        metrics={"current_price": 4065.0},
        price=4065.0,
        external=ExternalFactors(),
        source_label="issue36-relationship-fixture",
    )


def _archive_fixture_ctx() -> MarketContext:
    """Reproduce Issue #36 archive geometry around 4067–4071."""
    ts = pd.Timestamp("2026-07-14 15:00", tz="UTC")
    bear_thin = FairValueGap(high=4070.71, low=4067.31, direction="bearish", time=ts)
    bull_wide = FairValueGap(high=4071.00, low=4031.915, direction="bullish", time=ts)
    bull_15m = FairValueGap(high=4068.985, low=4031.035, direction="bullish", time=ts)
    analyses = {
        "1h": _analysis_with_fvgs("1h", atr=18.7446, fvgs=[bear_thin, bull_wide]),
        "15m": _analysis_with_fvgs("15m", atr=8.0, fvgs=[bull_15m]),
        "5m": _analysis_with_fvgs("5m", atr=3.0, fvgs=[]),
        "4h": _analysis_with_fvgs("4h", atr=25.0, fvgs=[]),
    }
    return MarketContext(
        enriched={},
        analyses=analyses,
        metrics={"current_price": 4065.0},
        price=4065.0,
        external=ExternalFactors(),
        source_label="issue36-fixture",
    )


def test_thin_bearish_fvg_with_opposite_overlap_is_observation_only() -> None:
    ctx = _archive_fixture_ctx()
    proposal = LevelProposal(
        direction="SELL",
        entry_low=4067.31,
        entry_high=4070.71,
        stop_loss=4073.50,
        take_profits=[4055.0, 4045.0],
        setup_type="llm_fvg",
        reason="1H 看跌 FVG 与 5m 量价连续阻力共振",
        confidence=0.8,
        path_id="A",
        reaction_evidence_id="tech_reaction:0",
        anchor_level="1H FVG 4067.31-4070.71",
        expected_reaction="承压回落",
        deduction="共振做空",
    )
    reactions = [
        {
            "id": "tech_reaction:0",
            "label": "1H bearish FVG",
            "price": 4068.5,
            "timeframe": "1h",
            "expected_reaction": "承压回落",
            "rationale": "thin gap",
            "strength": 0.8,
        }
    ]
    claim = adjudicate_level_proposal_claim(proposal, ctx, level_reactions=reactions)
    assert claim.policy_version == CLAIM_POLICY_VERSION
    assert claim.eligibility == "observation_only"
    assert claim.quality["best_width_atr_ratio"] is not None
    assert claim.quality["best_width_atr_ratio"] < 0.35
    assert claim.counterevidence
    assert any(c["kind"] == "overlapping_opposite_fvg" for c in claim.counterevidence)
    assert claim.fact_ids
    assert not claim.allows_execution_authorization


def test_missing_reaction_id_is_uncitable() -> None:
    ctx = _archive_fixture_ctx()
    proposal = LevelProposal(
        direction="SELL",
        entry_low=4067.31,
        entry_high=4070.71,
        stop_loss=4073.50,
        take_profits=[4055.0],
        setup_type="llm_fvg",
        reason="bogus bind",
        confidence=0.7,
        path_id="B",
        reaction_evidence_id="tech_reaction:missing",
    )
    claim = adjudicate_level_proposal_claim(proposal, ctx, level_reactions=[])
    assert claim.eligibility == "uncitable"


def test_free_text_confluence_without_fact_ids_is_not_core_execution() -> None:
    ctx = _wide_fvg_ctx(ob_low=4050.0, ob_high=4054.0)
    proposal = LevelProposal(
        direction="SELL",
        entry_low=4067.3,
        entry_high=4070.7,
        stop_loss=4074.0,
        take_profits=[4055.0],
        setup_type="llm_fvg",
        reason="1h FVG 与远离入场区的 5m OB 共振",
        confidence=0.8,
        path_id="A",
        reaction_evidence_id="tech_reaction:0",
    )
    reactions = [{"id": "tech_reaction:0", "rationale": proposal.reason}]

    claim = adjudicate_level_proposal_claim(proposal, ctx, level_reactions=reactions)

    assert claim.eligibility != "core_execution"
    assert claim.quality["structured_fact_bind"] is False
    assert any(c["kind"] == "missing_structured_fact_bind" for c in claim.counterevidence)


def test_single_bound_fvg_with_free_text_confluence_still_needs_relationship() -> None:
    ctx = _wide_fvg_ctx(ob_low=4050.0, ob_high=4054.0)
    proposal = LevelProposal(
        direction="SELL",
        entry_low=4067.3,
        entry_high=4070.7,
        stop_loss=4074.0,
        take_profits=[4055.0],
        setup_type="llm_fvg",
        reason="FVG 与未绑定的 OB 共振",
        confidence=0.8,
        path_id="A",
        reaction_evidence_id="tech_reaction:0",
    )
    reactions = [
        {
            "id": "tech_reaction:0",
            "fact_ids": ["1h.fvg.0.low", "1h.fvg.0.high"],
            "rationale": proposal.reason,
        }
    ]

    claim = adjudicate_level_proposal_claim(proposal, ctx, level_reactions=reactions)

    assert claim.eligibility != "core_execution"
    assert any(c["kind"] == "missing_fact_relationships" for c in claim.counterevidence)


def test_false_ob_overlap_relationship_is_observation_only() -> None:
    ctx = _wide_fvg_ctx(ob_low=4061.04, ob_high=4065.32)
    proposal = LevelProposal(
        direction="SELL",
        entry_low=4067.31,
        entry_high=4070.71,
        stop_loss=4073.5,
        take_profits=[4055.0],
        setup_type="llm_fvg",
        reason="FVG 与 OB 共振",
        confidence=0.8,
        path_id="A",
        reaction_evidence_id="tech_reaction:0",
    )
    reactions = [
        {
            "id": "tech_reaction:0",
            "fact_ids": [
                "1h.fvg.0.low",
                "1h.fvg.0.high",
                "5m.ob.0.low",
                "5m.ob.0.high",
            ],
            "relationships": [
                {
                    "type": "overlap",
                    "left_fact_ids": ["1h.fvg.0.low", "1h.fvg.0.high"],
                    "right_fact_ids": ["5m.ob.0.low", "5m.ob.0.high"],
                }
            ],
        }
    ]

    claim = adjudicate_level_proposal_claim(proposal, ctx, level_reactions=reactions)

    assert claim.eligibility == "observation_only"
    assert any(c["kind"] == "invalid_claimed_relationship" for c in claim.counterevidence)
    assert claim.quality["verified_relationship_count"] == 0


def test_valid_traceable_fvg_ob_overlap_can_be_core_execution() -> None:
    ctx = _wide_fvg_ctx(ob_low=4068.0, ob_high=4071.0)
    proposal = LevelProposal(
        direction="SELL",
        entry_low=4067.31,
        entry_high=4070.71,
        stop_loss=4073.5,
        take_profits=[4055.0],
        setup_type="llm_fvg_ob",
        reason="结构化 FVG/OB 重叠",
        confidence=0.8,
        path_id="A",
        reaction_evidence_id="tech_reaction:0",
    )
    reactions = [
        {
            "id": "tech_reaction:0",
            "fact_ids": [
                "1h.fvg.0.low",
                "1h.fvg.0.high",
                "5m.ob.0.low",
                "5m.ob.0.high",
            ],
            "relationships": [
                {
                    "type": "overlap",
                    "left_fact_ids": ["1h.fvg.0.low", "1h.fvg.0.high"],
                    "right_fact_ids": ["5m.ob.0.low", "5m.ob.0.high"],
                }
            ],
        }
    ]

    claim = adjudicate_level_proposal_claim(proposal, ctx, level_reactions=reactions)

    assert claim.eligibility == "core_execution"
    assert claim.quality["structured_fact_bind"] is True
    assert claim.quality["verified_relationship_count"] == 1
    assert "5m.ob.0.low" in claim.fact_ids


def test_validate_llm_levels_rejects_uncitable_and_tags_observation() -> None:
    ctx = _archive_fixture_ctx()
    proposals = [
        LevelProposal(
            direction="SELL",
            entry_low=4067.31,
            entry_high=4070.71,
            stop_loss=4073.50,
            take_profits=[4055.0, 4045.0],
            setup_type="llm_fvg",
            reason="conflicted resonance",
            confidence=0.8,
            path_id="A",
            reaction_evidence_id="tech_reaction:0",
            anchor_level="1H FVG",
            expected_reaction="承压",
            deduction="短推演",
        ),
        LevelProposal(
            direction="SELL",
            entry_low=4080.0,
            entry_high=4085.0,
            stop_loss=4090.0,
            take_profits=[4070.0, 4060.0],
            setup_type="llm_fvg",
            reason="missing reaction",
            confidence=0.6,
            path_id="B",
            reaction_evidence_id="tech_reaction:ghost",
            anchor_level="x",
            expected_reaction="y",
            deduction="z",
        ),
        LevelProposal(
            direction="BUY",
            entry_low=4058.0,
            entry_high=4062.0,
            stop_loss=4052.0,
            take_profits=[4070.0, 4080.0],
            setup_type="llm_fvg",
            reason="hedge long when local support holds near VAL",
            confidence=0.55,
            path_id="C",
            anchor_level="15m support",
            expected_reaction="收回",
            deduction="支撑试探",
        ),
    ]
    reactions = [
        {
            "id": "tech_reaction:0",
            "label": "1H FVG",
            "price": 4068.0,
            "timeframe": "1h",
            "expected_reaction": "承压",
            "rationale": "r",
            "strength": 0.8,
        }
    ]
    signals, audit = validate_llm_levels(ctx, proposals, level_reactions=reactions)
    by_path = {row["proposal"]["path_id"]: row for row in audit}
    assert by_path["B"]["accepted"] is False
    assert by_path["B"]["claim"]["eligibility"] == "uncitable"
    a_sig = next(s for s in signals if s.name.startswith("LLM路径A"))
    assert a_sig.claim_eligibility == "observation_only"
    assert a_sig.counterevidence
    assert a_sig.claim_id
    assert a_sig.claim_fact_ids
    assert a_sig.reaction_evidence_id == "tech_reaction:0"


def test_observation_claim_cannot_authorize_execution() -> None:
    report = {
        "signals": [
            {
                "name": "LLM路径A·做空",
                "theme": "short",
                "direction": "SELL",
                "direction_cn": "做空",
                "status": "active",
                "trigger_confirmed": True,
                "entry_low": 4067.31,
                "entry_high": 4070.71,
                "stop_loss": 4073.50,
                "take_profits": [4055.0],
                "claim_eligibility": "observation_only",
                "claim_id": "level_claim:A:SELL",
                "counterevidence": [{"kind": "overlapping_opposite_fvg"}],
                "position_size": "30%",
            }
        ],
        "meta": {"data_as_of": {"executable": True}},
        "strategy_plans": [],
        "conclusion": {},
    }
    decision = ManagerDecision(
        action="reduce",
        primary_direction="short",
        selected_signal_indices=[0],
        confidence=0.7,
        summary="缩仓",
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
    assert report["meta"]["execution_authorized"] is False
    assert "证据" in report["signals"][0]["position_size"] or "观察" in report["signals"][0]["position_size"]
    assert "证据" in report["meta"]["final_decision"]["verdict_cn"] or "观察" in report["meta"]["final_decision"]["verdict_cn"]


def test_inv_claim_flags_execution_with_non_core_eligibility() -> None:
    report = {
        "metrics": {"current_price": 4065.0},
        "signals": [
            {
                "name": "bad",
                "direction": "SELL",
                "entry_low": 4067.31,
                "entry_high": 4070.71,
                "stop_loss": 4073.5,
                "take_profits": [4055.0],
                "signal_id": "sig-x",
                "signal_role": "primary",
                "status": "active",
                "trigger_confirmed": True,
                "claim_eligibility": "observation_only",
            }
        ],
        "meta": {
            "execution_authorized": True,
            "authorized_signal_ids": ["sig-x"],
            "manager_decision": {"action": "reduce"},
            "final_decision": {"action": "reduce"},
            "stage_sources": {},
        },
        "llm_analysis": {},
        "conclusion": {},
    }
    result = validate_report_invariants(report)
    assert "INV-CLAIM-001" in {v["code"] for v in result["violations"]}


def test_claim_allows_execution_default_for_rule_signals() -> None:
    assert claim_allows_execution_authorization({}) is True
    assert claim_allows_execution_authorization({"claim_eligibility": ""}) is True
    assert claim_allows_execution_authorization({"claim_eligibility": "core_execution"}) is True
    assert claim_allows_execution_authorization({"claim_eligibility": "supporting"}) is False
