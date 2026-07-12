"""Validate, dedupe and score evidence IDs across analyst → research → debate."""

from __future__ import annotations

from typing import Any

from src.core.types import AnalystTeam, Bias, EvidenceItem


def analyst_evidence_ids(team: AnalystTeam) -> set[str]:
    ids: set[str] = set()
    for role in ("technical", "fundamentals", "news", "sentiment"):
        for item in getattr(team, role).items:
            eid = (item.evidence_id or "").strip()
            if eid:
                ids.add(eid)
    return ids


def evidence_registry(team: AnalystTeam) -> dict[str, EvidenceItem]:
    reg: dict[str, EvidenceItem] = {}
    for role in ("technical", "fundamentals", "news", "sentiment"):
        for item in getattr(team, role).items:
            eid = (item.evidence_id or "").strip()
            if eid:
                reg[eid] = item
    return reg


def is_new_structure_id(evidence_id: str, agent: str) -> bool:
    """Deprecated: Research must not mint structure IDs; kept for tests/docs."""
    return False


def _allowed_id(evidence_id: str, *, agent: str, allowed_ids: set[str]) -> bool:
    eid = evidence_id.strip()
    if not eid:
        return False
    return eid in allowed_ids


def dedupe_evidence_items(items: list[EvidenceItem]) -> tuple[list[EvidenceItem], int]:
    """Keep strongest item per evidence_id."""
    best: dict[str, EvidenceItem] = {}
    for item in items:
        eid = (item.evidence_id or "").strip()
        if not eid:
            continue
        prev = best.get(eid)
        if prev is None or item.strength > prev.strength:
            best[eid] = item
    dropped = max(0, len(items) - len(best))
    out = sorted(best.values(), key=lambda i: i.strength, reverse=True)
    return out, dropped


def _restore_refs(item: EvidenceItem, registry: dict[str, EvidenceItem]) -> EvidenceItem:
    eid = (item.evidence_id or "").strip()
    upstream = registry.get(eid)
    if upstream is None:
        return item
    merged_refs = dict(upstream.refs)
    merged_refs.update({k: v for k, v in item.refs.items() if v})
    if not merged_refs.get("source") and upstream.refs.get("source"):
        merged_refs["source"] = upstream.refs["source"]
    merged_refs.setdefault("upstream_id", eid)
    return EvidenceItem(
        category=item.category,
        summary=item.summary,
        strength=item.strength,
        timeframe=item.timeframe or upstream.timeframe,
        refs=merged_refs,
        evidence_id=eid,
    )


def parse_research_items(
    rows: list[dict[str, Any]],
    *,
    agent: str,
    direction: Bias,
    allowed_ids: set[str],
    registry: dict[str, EvidenceItem],
    item_refs_fn,
) -> tuple[list[EvidenceItem], int]:
    """Parse LLM research items with ID whitelist, ref restore and dedupe."""
    parsed: list[EvidenceItem] = []

    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        summary = str(row.get("summary", "")).strip()
        if not summary:
            continue
        evidence_id = str(row.get("evidence_id") or "").strip()
        if not evidence_id:
            raise ValueError(f"{agent} item[{idx}] missing evidence_id")
        if not _allowed_id(evidence_id, agent=agent, allowed_ids=allowed_ids):
            raise ValueError(f"{agent} item[{idx}] unknown evidence_id: {evidence_id}")

        category = str(row.get("category", "structure"))
        refs = item_refs_fn(row, category)
        try:
            strength = float(row.get("strength", 0.3))
        except (TypeError, ValueError):
            strength = 0.3
        strength = max(0.0, min(1.0, strength))

        item = EvidenceItem(
            category=category,
            summary=summary,
            strength=strength,
            timeframe=row.get("timeframe"),
            refs=refs,
            evidence_id=evidence_id,
        )
        if evidence_id in registry:
            item = _restore_refs(item, registry)
        parsed.append(item)

    deduped, dropped = dedupe_evidence_items(parsed)
    return deduped, dropped


def build_research_provenance_meta(
    items: list[EvidenceItem],
    *,
    allowed_ids: set[str],
    model_confidence: float,
    dedupe_dropped: int = 0,
) -> dict[str, Any]:
    if not items:
        return {
            "model_confidence": round(model_confidence, 3),
            "computed_confidence": 0.0,
            "upstream_coverage": 0.0,
            "source_diversity": 0.0,
            "unique_evidence_ids": 0,
            "dedupe_dropped": dedupe_dropped,
        }

    upstream = sum(1 for i in items if (i.evidence_id or "") in allowed_ids)
    coverage = upstream / len(items)
    sources = {str(i.refs.get("source")) for i in items if i.refs.get("source")}
    diversity = min(1.0, len(sources) / max(1, len(items)))
    avg_strength = sum(i.strength for i in items) / len(items)
    computed = 0.35 * coverage + 0.25 * diversity + 0.40 * avg_strength

    return {
        "model_confidence": round(model_confidence, 3),
        "computed_confidence": round(computed, 3),
        "upstream_coverage": round(coverage, 3),
        "source_diversity": round(diversity, 3),
        "unique_evidence_ids": len({i.evidence_id for i in items}),
        "dedupe_dropped": dedupe_dropped,
    }


def blend_research_confidence(model_confidence: float, meta: dict[str, Any]) -> float:
    computed = float(meta.get("computed_confidence") or 0.0)
    return max(0.0, min(1.0, 0.45 * model_confidence + 0.55 * computed))


def build_debate_provenance_meta(
    bullish: list[EvidenceItem],
    bearish: list[EvidenceItem],
    *,
    model_consensus_strength: float,
) -> dict[str, Any]:
    bull_ids = {i.evidence_id for i in bullish if i.evidence_id}
    bear_ids = {i.evidence_id for i in bearish if i.evidence_id}
    union = bull_ids | bear_ids
    overlap = bull_ids & bear_ids
    n_bull, n_bear = len(bullish), len(bearish)
    balance = min(n_bull, n_bear) / max(n_bull, n_bear, 1)
    overlap_penalty = len(overlap) / max(len(union), 1)
    computed = 0.40 * balance + 0.35 * (1.0 - overlap_penalty) + 0.25 * min(n_bull, n_bear) / 6.0
    computed = max(0.0, min(1.0, computed))
    return {
        "model_consensus_strength": round(model_consensus_strength, 3),
        "computed_consensus_strength": round(computed, 3),
        "bullish_item_count": n_bull,
        "bearish_item_count": n_bear,
        "evidence_balance": round(balance, 3),
        "shared_evidence_ids": sorted(overlap),
        "unique_evidence_ids": len(union),
    }


def blend_debate_consensus(model_strength: float, meta: dict[str, Any]) -> float:
    computed = float(meta.get("computed_consensus_strength") or 0.0)
    return max(0.0, min(1.0, 0.40 * model_strength + 0.60 * computed))
