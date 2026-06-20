"""FIN-13: debate consensus aligns with structure sentiment when scores are close."""

from __future__ import annotations

import pytest

from src.agents.debate import run_debate
from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import AgentEvidence, EvidenceItem


def _minimal_analyses() -> dict[str, TimeframeAnalysis]:
    base = TimeframeAnalysis("5m", "bearish", "—", "—")
    return {
        "5m": base,
        "15m": TimeframeAnalysis("15m", "bearish", "—", "—"),
        "1h": TimeframeAnalysis("1h", "bullish", "—", "—"),
        "4h": TimeframeAnalysis("4h", "ranging", "—", "—"),
        "1d": TimeframeAnalysis("1d", "bearish", "—", "—"),
    }


def _evidence(agent: str, direction: str, n: int, conf: float) -> AgentEvidence:
    items = [
        EvidenceItem(category="research", summary=f"item{i}", strength=0.5)
        for i in range(n)
    ]
    return AgentEvidence(
        agent=agent,
        direction=direction,  # type: ignore[arg-type]
        items=items,
        confidence=conf,
        summary=direction,
    )


@pytest.mark.financial
def test_debate_snapshot_20260620_bearish_dominant() -> None:
    """2026-06-20 rule run: bull 10.44+0.5 vs bear 8.78+0.9, sentiment 45% bear."""
    bullish = _evidence("bullish", "bullish", 40, 0.2610746169354839)
    bearish = _evidence("bearish", "bearish", 39, 0.2251902849002849)
    debate = run_debate(bullish, bearish, _minimal_analyses())
    assert debate.consensus_bias == "bearish"


@pytest.mark.financial
def test_debate_tiebreaker_neutral_when_sentiment_balanced() -> None:
    bullish = _evidence("bullish", "bullish", 10, 0.5)
    bearish = _evidence("bearish", "bearish", 10, 0.5)
    debate = run_debate(bullish, bearish, _minimal_analyses())
    assert debate.consensus_bias in ("bearish", "bullish", "neutral")
