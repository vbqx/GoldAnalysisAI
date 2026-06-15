"""Analyst Team LLM dual-track tests."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.agents import factory as agent_factory
from src.agents.llm.schemas import parse_analyst_report
from src.analysis.ict_pa import analyze_timeframe
from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.types import AgentPipelineMeta, ExternalFactors, MacroQuote, MarketContext
from src.indicators.technical import enrich


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
        metrics={
            "current_price": price,
            "daily_change": 1.0,
            "daily_change_pct": 0.1,
            "daily_high": price + 10,
            "daily_low": price - 10,
        },
        price=price,
        external=ExternalFactors(
            dxy_impact="偏强 (104.0, 日 +0.50%) → 利空黄金",
            macro_quotes=[
                MacroQuote(
                    name="DXY",
                    symbol="TVC:DXY",
                    close=104.0,
                    change_pct=0.5,
                    impact="偏强 (104.0, 日 +0.50%) → 利空黄金",
                    bias="bearish",
                )
            ],
        ),
        source_label="test",
    )


def test_parse_analyst_report() -> None:
    raw = {
        "bias": "bearish",
        "confidence": 0.72,
        "summary": "DXY偏强",
        "items": [
            {"category": "fundamentals", "summary": "美元压制黄金", "strength": 0.7},
            {"category": "fundamentals", "summary": "US10Y上行", "strength": 0.65},
            {"category": "fundamentals", "summary": "实际利率偏高", "strength": 0.6},
            {"category": "fundamentals", "summary": "风险偏好回落", "strength": 0.55},
        ],
    }
    report = parse_analyst_report(raw, agent="fundamentals_analyst")
    assert report.bias == "bearish"
    assert report.confidence == 0.72
    assert report.items[0].summary == "美元压制黄金"


def test_factory_analyst_team_llm_hybrid_picks_high_confidence(monkeypatch) -> None:
    ctx = _sample_context()
    reporter = ProgressReporter()
    token = set_progress(reporter)
    monkeypatch.setattr(agent_factory, "AGENT_MODE", "hybrid")
    monkeypatch.setattr(agent_factory, "LLM_STAGE_ANALYSTS", True)
    monkeypatch.setattr(agent_factory, "LLM_OVERRIDE_THRESHOLD", 0.65)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    llm_json = {
        "bias": "bullish",
        "confidence": 0.9,
        "summary": "LLM 技术偏多",
        "items": [
            {"category": "technical", "summary": "4h BOS 向上", "strength": 0.85, "timeframe": "4h"},
            {"category": "technical", "summary": "1h 趋势偏多", "strength": 0.8, "timeframe": "1h"},
            {"category": "technical", "summary": "EMA20 上方", "strength": 0.7, "timeframe": "5m"},
            {"category": "technical", "summary": "FVG 支撑", "strength": 0.65, "timeframe": "15m"},
        ],
    }

    def fake_technical(_ctx):
        from src.core.types import LLMStageTrace

        report = parse_analyst_report(llm_json, agent="technical_analyst")
        return report, LLMStageTrace(stage="technical", model="test-model", latency_ms=10)

    def fake_other(_ctx):
        from src.core.types import LLMStageTrace

        return None, LLMStageTrace(stage="x", model="test-model", error="skip")

    try:
        with patch.object(agent_factory, "run_llm_technical_analyst", side_effect=fake_technical), patch.object(
            agent_factory, "run_llm_fundamentals_analyst", side_effect=fake_other
        ), patch.object(agent_factory, "run_llm_news_analyst", side_effect=fake_other), patch.object(
            agent_factory, "run_llm_sentiment_analyst", side_effect=fake_other
        ):
            meta = AgentPipelineMeta()
            team = agent_factory.run_analyst_team(ctx, meta)

        assert team.technical.summary == "LLM 技术偏多"
        assert team.technical.bias == "bullish"
        assert meta.stages["analyst_team"].source == "hybrid"
        assert meta.stages["technical"].source == "hybrid"
        assert meta.stages["fundamentals"].source == "rule"
    finally:
        reset_progress(token)


def test_factory_analyst_team_llm_disabled_uses_rule(monkeypatch) -> None:
    ctx = _sample_context()
    monkeypatch.setattr(agent_factory, "LLM_STAGE_ANALYSTS", False)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: False)

    meta = AgentPipelineMeta()
    team = agent_factory.run_analyst_team(ctx, meta)
    assert team.fundamentals.bias == "bearish"
    assert meta.stages["analyst_team"].source == "rule"
