"""Debate stage routing and parallel prep tests."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.agents import factory as agent_factory
from src.agents.analysts import run_analyst_team as rule_analyst_team
from src.analysis.ict_pa import analyze_timeframe
from src.core.types import (
    AgentEvidence,
    AgentPipelineMeta,
    EvidenceItem,
    ExternalFactors,
    LLMStageTrace,
    MarketContext,
    ResearchDebate,
)
from src.indicators.technical import enrich
from src.llm.router import get_debate_client, get_fast_client, get_strong_client
from tests._run_config_helpers import bind_run_config


def _sample_context() -> MarketContext:
    idx = pd.date_range("2026-01-01", periods=120, freq="5min", tz="UTC")
    close = 4200.0 + pd.Series(range(120), dtype=float) * 0.05
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [100] * 120,
        },
        index=idx,
    )
    enriched = {tf: enrich(df) for tf in ("5m", "15m", "1h", "4h", "1d")}
    analyses = {tf: analyze_timeframe(enriched[tf], tf) for tf in enriched}
    price = float(close.iloc[-1])
    return MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics={"current_price": price, "daily_change": 1.0, "daily_change_pct": 0.1},
        price=price,
        external=ExternalFactors(),
        source_label="test",
    )


def _evidence(direction: str) -> AgentEvidence:
    return AgentEvidence(
        agent=f"{direction}_researcher",
        direction=direction,  # type: ignore[arg-type]
        items=[EvidenceItem(category="research", summary=direction, strength=0.7)],
        confidence=0.7,
        summary=direction,
    )


def test_debate_client_uses_fast_when_configured(monkeypatch) -> None:
    monkeypatch.setattr("src.llm.router.LLM_DEBATE_USE_FAST", True)
    assert get_debate_client().model == get_fast_client().model

    monkeypatch.setattr("src.llm.router.LLM_DEBATE_USE_FAST", False)
    assert get_debate_client().model == get_strong_client().model


def test_run_debate_llm_mode_skips_rule_until_fallback(monkeypatch) -> None:
    ctx = _sample_context()
    team = rule_analyst_team(ctx)
    bull = _evidence("bullish")
    bear = _evidence("bearish")
    debate = ResearchDebate(
        bullish=bull,
        bearish=bear,
        consensus_bias="bearish",
        consensus_strength=0.8,
        discussion_notes=["llm note"],
    )
    meta = AgentPipelineMeta()

    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    with bind_run_config(agent_mode="llm", llm_enabled=True, llm_stage_debate=True), patch.object(
        agent_factory, "rule_debate"
    ) as rule_mock, patch.object(
        agent_factory,
        "run_llm_debate",
        return_value=(debate, LLMStageTrace(stage="debate", model="m", latency_ms=10)),
    ) as llm_mock:
        result = agent_factory.run_debate(bull, bear, ctx.analyses, meta, team, ctx)

    assert result.consensus_bias == "bearish"
    rule_mock.assert_not_called()
    llm_mock.assert_called_once()
