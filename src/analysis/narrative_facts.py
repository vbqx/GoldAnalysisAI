"""Single builder for narrative LLM facts — shared by context and offline validation."""

from __future__ import annotations

from typing import Any

from src.analysis.narrative_sections import build_narrative_facts
from src.analysis.technical_context import build_technical_context
from src.config import ANALYST_ICT_EVENTS_MAX
from src.core.types import MarketContext

NARRATIVE_ICT_PER_TF = max(3, ANALYST_ICT_EVENTS_MAX // 2)


def build_narrative_facts_for_llm(
    report: dict[str, Any],
    *,
    ctx: MarketContext | None = None,
    technical_context: dict[str, Any] | None = None,
    event_limit: int | None = None,
    compact_for_llm: bool = True,
) -> dict[str, Any]:
    """Build narrative_facts once from report + optional market context."""
    limit = NARRATIVE_ICT_PER_TF if event_limit is None else event_limit
    if technical_context is None:
        if ctx is not None:
            technical_context = build_technical_context(ctx, event_limit=limit)
        else:
            technical_context = {}
    return build_narrative_facts(report, technical_context, compact_for_llm=compact_for_llm)


__all__ = ["NARRATIVE_ICT_PER_TF", "build_narrative_facts", "build_narrative_facts_for_llm"]
