"""Stable evidence identifiers for analyst → research → debate provenance."""

from __future__ import annotations

from src.core.types import EvidenceItem


def assign_evidence_ids(agent: str, items: list[EvidenceItem]) -> list[EvidenceItem]:
    """Ensure every item has a stable ``{agent}:{index}`` id."""
    out: list[EvidenceItem] = []
    for idx, item in enumerate(items):
        eid = (item.evidence_id or "").strip() or f"{agent}:{idx}"
        out.append(
            EvidenceItem(
                category=item.category,
                summary=item.summary,
                strength=item.strength,
                timeframe=item.timeframe,
                refs=dict(item.refs),
                evidence_id=eid,
            )
        )
    return out
