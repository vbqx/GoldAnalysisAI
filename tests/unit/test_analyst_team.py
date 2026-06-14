"""Analyst Team unit tests — TradingAgents-style specialist layer."""

from __future__ import annotations

import pandas as pd

from src.agents.analysts import run_analyst_team
from src.agents.analysts.base import items_for_direction
from src.agents.bearish import run_bearish_researcher
from src.agents.bullish import run_bullish_researcher
from src.agents.debate import run_debate
from src.analysis.ict_pa import TimeframeAnalysis, analyze_timeframe
from src.core.types import AnalystReport, AnalystTeam, EvidenceItem, ExternalFactors, MarketContext
from src.indicators.technical import enrich


def _sample_context() -> MarketContext:
    idx = pd.date_range("2026-01-01", periods=120, freq="5min", tz="UTC")
    base = 4200.0
    close = base + pd.Series(range(120), dtype=float) * 0.05
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
    return MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics={"current_price": float(close.iloc[-1]), "daily_change": 1.0, "daily_change_pct": 0.1},
        price=float(close.iloc[-1]),
        external=ExternalFactors(),
        source_label="test",
    )


def test_analyst_team_has_four_specialists() -> None:
    team = run_analyst_team(_sample_context())
    assert isinstance(team, AnalystTeam)
    assert team.technical.agent == "technical_analyst"
    assert team.fundamentals.agent == "fundamentals_analyst"
    assert team.news.agent == "news_analyst"
    assert team.sentiment.agent == "sentiment_analyst"
    assert len(team.reports) == 4


def test_fundamentals_analyst_reads_dxy_placeholder() -> None:
    team = run_analyst_team(_sample_context())
    assert team.fundamentals.bias == "bearish"
    assert any("美元指数" in i.summary for i in team.fundamentals.items)


def test_bullish_researcher_includes_matching_analyst_items() -> None:
    ctx = _sample_context()
    team = run_analyst_team(ctx)
    without = run_bullish_researcher(ctx)
    with_team = run_bullish_researcher(ctx, team)
    assert len(with_team.items) >= len(without.items)


def test_items_for_direction_filters_bias() -> None:
    reports = [
        AnalystReport(
            agent="technical_analyst",
            bias="bullish",
            items=[EvidenceItem(category="technical", summary="test bull", strength=0.8)],
            confidence=0.7,
            summary="bull",
        ),
        AnalystReport(
            agent="fundamentals_analyst",
            bias="bearish",
            items=[EvidenceItem(category="fundamentals", summary="test bear", strength=0.8)],
            confidence=0.7,
            summary="bear",
        ),
    ]
    bull_items = items_for_direction(reports, "bullish")
    assert len(bull_items) == 1
    assert "technical" in bull_items[0].category


def test_debate_includes_analyst_summaries() -> None:
    ctx = _sample_context()
    team = run_analyst_team(ctx)
    bull = run_bullish_researcher(ctx, team)
    bear = run_bearish_researcher(ctx, team)
    debate = run_debate(bull, bear, ctx.analyses, team)
    assert any("Analyst Team" in note for note in debate.discussion_notes)
    assert any("technical_analyst" in note for note in debate.discussion_notes)


def test_factory_records_analyst_team_stage_io() -> None:
    from src.agents import factory as agent_factory
    from src.core.progress import ProgressReporter, reset_progress, set_progress
    from src.core.types import AgentPipelineMeta

    ctx = _sample_context()
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        meta = AgentPipelineMeta()
        agent_factory.run_analyst_team(ctx, meta)
        records = reporter.llm_io_snapshot()
        assert any(r["stage"] == "analyst_team" for r in records)
        rec = next(r for r in records if r["stage"] == "analyst_team")
        assert rec["kind"] == "rule"
        assert rec["model"] == "规则引擎"
        assert "technical" in rec["output"]
    finally:
        reset_progress(token)
