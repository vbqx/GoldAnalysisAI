"""Parallel bullish / bearish research tests."""

from __future__ import annotations

import time
from unittest.mock import patch

import pandas as pd

from src.agents import factory as agent_factory
from src.analysis.ict_pa import analyze_timeframe
from src.core.types import AgentEvidence, AgentPipelineMeta, EvidenceItem, ExternalFactors, MarketContext
from src.indicators.technical import enrich
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


def _fake_evidence(label: str) -> AgentEvidence:
    return AgentEvidence(
        agent="test_researcher",
        direction="bullish",
        items=[EvidenceItem(category="research", summary=label, strength=0.8)],
        confidence=0.8,
        summary=label,
    )


def test_research_parallel_faster_than_serial(monkeypatch) -> None:
    from src.agents.analysts import run_analyst_team as rule_analyst_team

    ctx = _sample_context()
    team = rule_analyst_team(ctx)
    delay = 0.1

    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_ENABLED", True)
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_RESEARCH", True)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    def slow_bull(_ctx, _team):
        from src.core.types import LLMStageTrace

        time.sleep(delay)
        return _fake_evidence("bull"), LLMStageTrace(stage="bullish", model="m", latency_ms=1)

    def slow_bear(_ctx, _team):
        from src.core.types import LLMStageTrace

        time.sleep(delay)
        return _fake_evidence("bear"), LLMStageTrace(stage="bearish", model="m", latency_ms=1)

    meta = AgentPipelineMeta()
    with bind_run_config(
        agent_mode="hybrid",
        llm_enabled=True,
        llm_stage_bullish=True,
        llm_stage_bearish=True,
    ), patch.object(agent_factory, "run_llm_bullish", side_effect=slow_bull), patch.object(
        agent_factory, "run_llm_bearish", side_effect=slow_bear
    ):
        t0 = time.perf_counter()
        bull, bear = agent_factory.run_research_team(ctx, meta, team)
        parallel_elapsed = time.perf_counter() - t0

    assert bull.summary == "bull"
    assert bear.summary == "bear"
    assert parallel_elapsed < delay * 1.75


def test_research_parallel_llm_mode_without_rule_baseline(monkeypatch) -> None:
    from src.agents.analysts import run_analyst_team as rule_analyst_team

    ctx = _sample_context()
    team = rule_analyst_team(ctx)
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_ENABLED", True)
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_RESEARCH", True)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    def fake_bull(_ctx, _team):
        from src.core.types import LLMStageTrace

        return _fake_evidence("bull llm"), LLMStageTrace(stage="bullish", model="m", latency_ms=1)

    def fake_bear(_ctx, _team):
        from src.core.types import LLMStageTrace

        return _fake_evidence("bear llm"), LLMStageTrace(stage="bearish", model="m", latency_ms=1)

    meta = AgentPipelineMeta()
    with bind_run_config(
        agent_mode="llm",
        llm_enabled=True,
        llm_stage_bullish=True,
        llm_stage_bearish=True,
    ), patch.object(agent_factory, "run_llm_bullish", side_effect=fake_bull), patch.object(
        agent_factory, "run_llm_bearish", side_effect=fake_bear
    ):
        bull, bear = agent_factory.run_research_team(ctx, meta, team)

    assert bull.summary == "bull llm"
    assert bear.summary == "bear llm"
    assert meta.stages["bullish"].source == "llm"
    assert meta.stages["bearish"].source == "llm"


def test_research_uses_parallel_llm_flag(monkeypatch) -> None:
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_ENABLED", True)
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_RESEARCH", True)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    with bind_run_config(
        agent_mode="hybrid",
        llm_enabled=True,
        llm_stage_bullish=True,
        llm_stage_bearish=True,
    ):
        assert agent_factory.research_uses_parallel_llm() is True

    with bind_run_config(
        agent_mode="hybrid",
        llm_enabled=True,
        llm_stage_bullish=True,
        llm_stage_bearish=False,
    ):
        assert agent_factory.research_uses_parallel_llm() is False
