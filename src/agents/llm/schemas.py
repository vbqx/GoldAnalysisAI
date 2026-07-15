"""Parse LLM JSON into pipeline domain types."""

from __future__ import annotations

from typing import Any

from src.config import ANALYST_TEAM_ITEMS_MAX, LLM_MIN_ANALYST_ITEMS, PAYLOAD_EVIDENCE_MAX
from src.core.types import (
    AgentEvidence,
    AnalystReport,
    Bias,
    EvidenceItem,
    LevelProposal,
    ManagerDecision,
    ResearchDebate,
    RiskProfile,
    RiskReview,
    TransactionProposal,
)

_DEFAULT_ITEM_SOURCE = {
    "technical": "tradingview_ict",
    "structure": "tradingview_ict",
    "price_action": "dgt_price_action",
    "lux_panel": "lux_smc_panel",
    "fundamentals": "macro",
    "news": "jin10",
    "sentiment": "tradingview_social",
    "external": "external",
}


def _item_refs(row: dict[str, Any], category: str) -> dict[str, Any]:
    refs = row.get("refs") if isinstance(row.get("refs"), dict) else {}
    if refs.get("source"):
        return refs
    source = row.get("source")
    if source:
        return {**refs, "source": str(source)}
    default = _DEFAULT_ITEM_SOURCE.get(category)
    if default:
        return {**refs, "source": default}
    return refs


def _clamp_strength(v: Any) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.3
    return max(0.0, min(1.0, f))


def _string_list(value: Any, *, fallback: list[str] | None = None, limit: int = 8) -> list[str]:
    if isinstance(value, list):
        out = [str(v).strip() for v in value if str(v).strip()]
        return out[:limit]
    text = str(value or "").strip()
    if text:
        return [text]
    return fallback or []


def _index_list(value: Any, *, allowed: set[int]) -> list[int]:
    if not isinstance(value, list):
        return []
    out: list[int] = []
    for raw in value:
        try:
            idx = int(raw)
        except (TypeError, ValueError):
            continue
        if idx in allowed and idx not in out:
            out.append(idx)
    return out


def _float_field(row: dict[str, Any], name: str) -> float:
    try:
        return float(row[name])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"level proposal missing numeric {name}") from exc


def _parse_level_reactions(data: dict[str, Any], *, agent: str) -> list[dict[str, Any]]:
    """Technical analyst reaction hypotheses at POC / VA / S/R."""
    raw = data.get("level_reactions") or data.get("key_level_reactions") or []
    out: list[dict[str, Any]] = []
    if isinstance(raw, list):
        for idx, row in enumerate(raw[:8]):
            if not isinstance(row, dict):
                continue
            label = str(row.get("label") or row.get("level") or row.get("name") or "").strip()
            reaction = str(
                row.get("expected_reaction") or row.get("reaction") or row.get("price_reaction") or ""
            ).strip()
            if not label and not reaction:
                continue
            price_raw = row.get("price")
            price: float | None
            try:
                price = round(float(price_raw), 2) if price_raw is not None else None
            except (TypeError, ValueError):
                price = None
            rid = str(row.get("id") or row.get("evidence_id") or "").strip() or f"{agent}:reaction:{idx}"
            fact_ids = [
                str(value).strip()
                for value in (row.get("fact_ids") or [])
                if isinstance(value, (str, int, float)) and str(value).strip()
            ]
            relationships: list[dict[str, Any]] = []
            for relation in (row.get("relationships") or [])[:8]:
                if not isinstance(relation, dict):
                    continue
                relation_type = str(relation.get("type") or "").strip().lower()
                left_ids = [
                    str(value).strip()
                    for value in (relation.get("left_fact_ids") or [])
                    if isinstance(value, (str, int, float)) and str(value).strip()
                ]
                right_ids = [
                    str(value).strip()
                    for value in (relation.get("right_fact_ids") or [])
                    if isinstance(value, (str, int, float)) and str(value).strip()
                ]
                if relation_type in ("overlap", "near", "contradiction") and left_ids and right_ids:
                    relationships.append(
                        {
                            "type": relation_type,
                            "left_fact_ids": left_ids,
                            "right_fact_ids": right_ids,
                        }
                    )
            out.append(
                {
                    "id": rid,
                    "label": label,
                    "price": price,
                    "timeframe": str(row.get("timeframe") or "").strip() or None,
                    "expected_reaction": reaction,
                    "rationale": str(row.get("rationale") or row.get("why") or "").strip(),
                    "strength": _clamp_strength(row.get("strength", 0.5)),
                    "fact_ids": sorted(set(fact_ids)),
                    "relationships": relationships,
                }
            )
    return out


def _level_reactions_from_items(items: list[EvidenceItem]) -> list[dict[str, Any]]:
    recovered: list[dict[str, Any]] = []
    for item in items:
        if item.category != "level_reaction" and not item.refs.get("expected_reaction"):
            continue
        price_raw = item.refs.get("price")
        try:
            price = round(float(price_raw), 2) if price_raw is not None else None
        except (TypeError, ValueError):
            price = None
        recovered.append(
            {
                "id": item.evidence_id or "",
                "label": str(item.refs.get("label") or item.summary).strip(),
                "price": price,
                "timeframe": item.timeframe,
                "expected_reaction": str(item.refs.get("expected_reaction") or item.summary).strip(),
                "rationale": "",
                "strength": item.strength,
                "fact_ids": list(item.refs.get("fact_ids") or []),
                "relationships": list(item.refs.get("relationships") or []),
            }
        )
    return recovered


def _merge_level_reactions_into_items(
    items: list[EvidenceItem],
    reactions: list[dict[str, Any]],
    *,
    agent: str,
) -> list[EvidenceItem]:
    """Expose reactions as evidence for research / levels binding."""
    existing_ids = {i.evidence_id for i in items if i.evidence_id}
    merged = list(items)
    for idx, row in enumerate(reactions):
        rid = str(row.get("id") or "").strip() or f"{agent}:reaction:{idx}"
        if rid in existing_ids:
            continue
        label = str(row.get("label") or "").strip()
        reaction = str(row.get("expected_reaction") or "").strip()
        price = row.get("price")
        price_bit = f" @{price}" if price is not None else ""
        tf = row.get("timeframe")
        tf_bit = f"{tf} " if tf else ""
        summary = str(row.get("rationale") or "").strip()
        if not summary:
            summary = f"{tf_bit}{label}{price_bit}：{reaction}".strip(" ：")
        merged.append(
            EvidenceItem(
                category="level_reaction",
                summary=summary,
                strength=float(row.get("strength") or 0.5),
                timeframe=tf if isinstance(tf, str) else None,
                refs={
                    "source": "dgt_price_action",
                    "price": price,
                    "label": label,
                    "expected_reaction": reaction,
                    "fact_ids": list(row.get("fact_ids") or []),
                    "relationships": list(row.get("relationships") or []),
                },
                evidence_id=rid,
            )
        )
        existing_ids.add(rid)
    return merged


def parse_analyst_report(data: dict[str, Any], *, agent: str) -> AnalystReport:
    bias = str(data.get("bias", "neutral")).lower()
    if bias not in ("bullish", "bearish", "neutral"):
        bias = "neutral"

    items_raw = data.get("items") or []
    items: list[EvidenceItem] = []
    if isinstance(items_raw, list):
        for idx, row in enumerate(items_raw[:ANALYST_TEAM_ITEMS_MAX]):
            if not isinstance(row, dict):
                continue
            summary = str(row.get("summary", "")).strip()
            if not summary:
                continue
            category = str(row.get("category", "external"))
            refs = _item_refs(row, category)
            evidence_id = str(row.get("evidence_id") or "").strip() or f"{agent}:{idx}"
            items.append(
                EvidenceItem(
                    category=category,
                    summary=summary,
                    strength=_clamp_strength(row.get("strength", 0.3)),
                    timeframe=row.get("timeframe"),
                    refs=refs,
                    evidence_id=evidence_id,
                )
            )

    level_reactions = _parse_level_reactions(data, agent=agent)
    if not level_reactions:
        level_reactions = _level_reactions_from_items(items)
    if agent == "technical_analyst" and len(level_reactions) < 2:
        raise ValueError(
            f"technical_analyst needs >=2 level_reactions "
            f"(POC/VA/S/R + expected_reaction), got {len(level_reactions)}"
        )
    if level_reactions:
        items = _merge_level_reactions_into_items(items, level_reactions, agent=agent)

    if len(items) < LLM_MIN_ANALYST_ITEMS:
        raise ValueError(
            f"{agent} returned {len(items)} items (min {LLM_MIN_ANALYST_ITEMS})"
        )

    confidence = _clamp_strength(data.get("confidence", 0.5))
    summary = str(data.get("summary", "")).strip()
    if not summary:
        summary = f"LLM {agent}：共 {len(items)} 条证据，偏向 {bias}，置信 {confidence:.0%}"

    return AnalystReport(
        agent=agent,
        bias=bias,  # type: ignore[arg-type]
        items=items,
        confidence=confidence,
        summary=summary,
        level_reactions=level_reactions if agent == "technical_analyst" else [],
    )


def parse_agent_evidence(
    data: dict[str, Any],
    *,
    agent: str,
    direction: Bias,
    allowed_evidence_ids: set[str] | None = None,
    evidence_registry: dict[str, EvidenceItem] | None = None,
) -> AgentEvidence:
    from src.agents.analysts.evidence_provenance import (
        blend_research_confidence,
        build_research_provenance_meta,
        parse_research_items,
    )

    items_raw = data.get("items") or []
    model_confidence = _clamp_strength(data.get("confidence", 0.5))
    summary = str(data.get("summary", "")).strip()

    if allowed_evidence_ids is not None:
        if not isinstance(items_raw, list):
            raise ValueError(f"{agent} returned non-list items")
        items, dropped = parse_research_items(
            items_raw,
            agent=agent,
            direction=direction,
            allowed_ids=allowed_evidence_ids,
            registry=evidence_registry or {},
            item_refs_fn=_item_refs,
        )
        meta = build_research_provenance_meta(
            items,
            allowed_ids=allowed_evidence_ids,
            model_confidence=model_confidence,
            dedupe_dropped=dropped,
        )
        confidence = blend_research_confidence(model_confidence, meta)
    else:
        items: list[EvidenceItem] = []
        if isinstance(items_raw, list):
            for idx, row in enumerate(items_raw[:PAYLOAD_EVIDENCE_MAX]):
                if not isinstance(row, dict):
                    continue
                summary_text = str(row.get("summary", "")).strip()
                if not summary_text:
                    continue
                category = str(row.get("category", "structure"))
                refs = _item_refs(row, category)
                evidence_id = str(row.get("evidence_id") or "").strip() or f"{agent}:{idx}"
                items.append(
                    EvidenceItem(
                        category=category,
                        summary=summary_text,
                        strength=_clamp_strength(row.get("strength", 0.3)),
                        timeframe=row.get("timeframe"),
                        refs=refs,
                        evidence_id=evidence_id,
                    )
                )
        meta = build_research_provenance_meta(
            items,
            allowed_ids=set(),
            model_confidence=model_confidence,
        )
        confidence = blend_research_confidence(model_confidence, meta)

    if not summary:
        summary = f"LLM：共 {len(items)} 条证据，置信度 {confidence:.2f}"

    return AgentEvidence(
        agent=agent,
        direction=direction,
        items=items,
        confidence=confidence,
        summary=summary,
        provenance_meta=meta,
    )


def parse_research_debate(
    data: dict[str, Any],
    *,
    bullish: AgentEvidence,
    bearish: AgentEvidence,
) -> ResearchDebate:
    from src.agents.analysts.evidence_provenance import (
        blend_debate_consensus,
        build_debate_provenance_meta,
    )

    bias = str(data.get("consensus_bias", "neutral")).lower()
    if bias not in ("bullish", "bearish", "neutral"):
        bias = "neutral"

    model_strength = _clamp_strength(data.get("consensus_strength", 0.5))
    debate_meta = build_debate_provenance_meta(
        bullish.items,
        bearish.items,
        model_consensus_strength=model_strength,
    )
    strength = blend_debate_consensus(model_strength, debate_meta)
    debate_meta["consensus_strength"] = round(strength, 3)

    notes_raw = data.get("discussion_notes") or []
    notes: list[str] = []
    if isinstance(notes_raw, list):
        notes = [str(n).strip() for n in notes_raw if str(n).strip()]

    dissent = str(data.get("dissent", "")).strip()
    if dissent:
        notes.append(f"分歧：{dissent}")

    if not notes:
        notes = ["LLM 辩论：已生成共识"]

    return ResearchDebate(
        bullish=bullish,
        bearish=bearish,
        consensus_bias=bias,  # type: ignore[arg-type]
        consensus_strength=strength,
        discussion_notes=notes,
        debate_meta=debate_meta,
    )


_GENERIC_LEVEL_REASON = "LLM proposed level based on supplied market structure."


def _compose_level_deduction_reason(
    *,
    anchor_level: str,
    expected_reaction: str,
    deduction: str,
    reason: str,
) -> str:
    """Build audit-friendly reason from structured reaction thesis fields."""
    if reason and reason != _GENERIC_LEVEL_REASON:
        return reason
    parts: list[str] = []
    if anchor_level:
        parts.append(f"锚点 {anchor_level}")
    if expected_reaction:
        parts.append(f"预期反应：{expected_reaction}")
    if deduction:
        parts.append(f"推演：{deduction}")
    return "；".join(parts) if parts else reason


def _level_deduction_quality(
    *,
    anchor_level: str,
    expected_reaction: str,
    deduction: str,
    reason: str,
    reaction_evidence_id: str,
) -> bool:
    """Prefer binding to technical reactions; allow short bind reason or legacy thesis."""
    if reaction_evidence_id and (anchor_level or expected_reaction or deduction or reason):
        return True
    structured = bool(deduction) and bool(anchor_level or expected_reaction)
    if structured:
        return True
    if reason and reason != _GENERIC_LEVEL_REASON and len(reason) >= 12:
        return True
    return False


def parse_level_proposals(data: dict[str, Any]) -> list[LevelProposal]:
    raw_setups = data.get("setups") or data.get("levels") or []
    if not isinstance(raw_setups, list):
        raise ValueError("level proposer returned non-list setups")

    proposals: list[LevelProposal] = []
    for idx, row in enumerate(raw_setups[:5]):
        if not isinstance(row, dict):
            continue
        direction = str(row.get("direction", "")).upper()
        if direction not in ("BUY", "SELL"):
            continue
        path_id = str(row.get("path_id") or row.get("path") or "").strip().upper()
        if path_id not in ("A", "B", "C"):
            raise ValueError(f"level proposal[{idx}] missing or invalid path_id (must be A/B/C)")

        entry_low = _float_field(row, "entry_low")
        entry_high = _float_field(row, "entry_high")
        if entry_low > entry_high:
            entry_low, entry_high = entry_high, entry_low

        tps_raw = row.get("take_profits") or row.get("targets") or []
        if not isinstance(tps_raw, list):
            tps_raw = [tps_raw]
        take_profits: list[float] = []
        for tp in tps_raw[:3]:
            try:
                take_profits.append(float(tp))
            except (TypeError, ValueError):
                continue
        if not take_profits:
            raise ValueError("level proposal missing take_profits")

        anchor_level = str(
            row.get("anchor_level") or row.get("anchor") or row.get("key_level") or ""
        ).strip()
        expected_reaction = str(
            row.get("expected_reaction") or row.get("reaction") or row.get("price_reaction") or ""
        ).strip()
        deduction = str(
            row.get("deduction") or row.get("thesis") or row.get("order_thesis") or ""
        ).strip()
        reaction_evidence_id = str(
            row.get("reaction_evidence_id") or row.get("level_reaction_id") or row.get("anchor_id") or ""
        ).strip()
        reason = str(row.get("reason", "")).strip()
        reason = _compose_level_deduction_reason(
            anchor_level=anchor_level,
            expected_reaction=expected_reaction,
            deduction=deduction,
            reason=reason,
        )
        if not _level_deduction_quality(
            anchor_level=anchor_level,
            expected_reaction=expected_reaction,
            deduction=deduction,
            reason=reason,
            reaction_evidence_id=reaction_evidence_id,
        ):
            raise ValueError(
                f"level proposal[{idx}] path {path_id} missing technical reaction bind "
                "(need reaction_evidence_id from technical.level_reactions, "
                "or anchor_level+expected_reaction+short deduction)"
            )

        proposals.append(
            LevelProposal(
                direction=direction,  # type: ignore[arg-type]
                entry_low=round(entry_low, 2),
                entry_high=round(entry_high, 2),
                stop_loss=round(_float_field(row, "stop_loss"), 2),
                take_profits=[round(tp, 2) for tp in take_profits],
                setup_type=str(row.get("setup_type", "llm_level")).strip() or "llm_level",
                reason=reason,
                confidence=_clamp_strength(row.get("confidence", 0.5)),
                invalidation=str(row.get("invalidation", "")).strip(),
                path_id=path_id,
                anchor_level=anchor_level,
                expected_reaction=expected_reaction,
                deduction=deduction,
                reaction_evidence_id=reaction_evidence_id,
            )
        )

    _validate_level_path_contract(proposals)
    return proposals


def _validate_level_path_contract(proposals: list[LevelProposal]) -> None:
    if len(proposals) != 3:
        raise ValueError(f"level proposer must return exactly 3 setups, got {len(proposals)}")
    paths = sorted(p.path_id for p in proposals)
    if paths != ["A", "B", "C"]:
        raise ValueError(f"path_id must be A,B,C exactly once, got {[p.path_id for p in proposals]}")


def parse_transaction_proposal(
    data: dict[str, Any],
    *,
    debate_bias: Bias,
    signal_count: int,
) -> TransactionProposal:
    direction = str(data.get("primary_direction", "wait")).lower()
    if direction not in ("long", "short", "wait"):
        direction = "wait"

    allowed = set(range(max(0, signal_count)))
    indices = _index_list(data.get("signal_indices"), allowed=allowed)
    if direction == "wait":
        indices = []

    rationale = _string_list(
        data.get("rationale") or data.get("reasons"),
        fallback=["LLM trader generated a transaction proposal."],
    )
    return TransactionProposal(
        primary_direction=direction,  # type: ignore[arg-type]
        signal_indices=indices,
        rationale=rationale,
        debate_bias=debate_bias,
    )


def parse_risk_reviews(
    data: dict[str, Any],
    *,
    proposal: TransactionProposal,
    signal_count: int,
) -> list[RiskReview]:
    raw_reviews = data.get("reviews") or data.get("risk_reviews") or []
    if not isinstance(raw_reviews, list):
        raise ValueError("risk stage returned non-list reviews")

    allowed_profiles: tuple[RiskProfile, ...] = ("aggressive", "neutral", "conservative")
    proposal_allowed = {idx for idx in proposal.signal_indices if 0 <= idx < signal_count}
    by_profile: dict[str, RiskReview] = {}
    for row in raw_reviews:
        if not isinstance(row, dict):
            continue
        profile = str(row.get("profile", "")).lower()
        if profile not in allowed_profiles:
            continue
        indices = _index_list(row.get("allowed_signal_indices"), allowed=proposal_allowed)
        scale = _clamp_strength(row.get("position_scale", 0.0))
        approved = bool(row.get("approved")) and bool(indices) and proposal.primary_direction != "wait"
        by_profile[profile] = RiskReview(
            profile=profile,  # type: ignore[arg-type]
            approved=approved,
            allowed_signal_indices=indices,
            position_scale=scale if approved else 0.0,
            notes=_string_list(row.get("notes"), fallback=[f"LLM {profile} 风控审核"]),
        )

    missing = [p for p in allowed_profiles if p not in by_profile]
    if missing:
        raise ValueError(f"risk stage missing profiles: {', '.join(missing)}")
    return [by_profile[p] for p in allowed_profiles]


def parse_manager_decision(
    data: dict[str, Any],
    *,
    proposal: TransactionProposal,
    reviews: list[RiskReview],
) -> ManagerDecision:
    action = str(data.get("action", "wait")).lower()
    if action not in ("execute", "reduce", "wait"):
        action = "wait"

    approved = {
        idx
        for review in reviews
        if review.approved
        for idx in review.allowed_signal_indices
    }
    selected = _index_list(data.get("selected_signal_indices"), allowed=approved)
    if action == "wait" or not selected:
        action = "wait"
        selected = []

    summary = str(data.get("summary", "")).strip()
    if not summary:
        summary = "LLM manager generated the final trade authorization."

    scale = 0.0
    if selected:
        scales = [
            review.position_scale
            for review in reviews
            if review.approved and set(review.allowed_signal_indices).intersection(selected)
        ]
        scale = min(scales) if scales else 0.0

    return ManagerDecision(
        action=action,  # type: ignore[arg-type]
        primary_direction=proposal.primary_direction,
        selected_signal_indices=selected,
        confidence=_clamp_strength(data.get("confidence", 0.0 if action == "wait" else 0.5)),
        summary=summary,
        position_scale=scale if action != "wait" else 0.0,
    )
