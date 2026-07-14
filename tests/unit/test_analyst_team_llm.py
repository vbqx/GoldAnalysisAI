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
        "level_reactions": [
            {
                "id": "tech_reaction:0",
                "label": "POC",
                "price": 4205.0,
                "timeframe": "5m",
                "expected_reaction": "支撑反弹",
                "rationale": "价在 POC 下方回踩",
            },
            {
                "id": "tech_reaction:1",
                "label": "VAL",
                "price": 4198.0,
                "timeframe": "15m",
                "expected_reaction": "跌破加速",
                "rationale": "失守价值区下沿",
            },
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
        with bind_run_config(agent_mode="hybrid", llm_enabled=True, llm_stage_analysts=True), patch.object(
            agent_factory, "run_llm_technical_analyst", side_effect=fake_technical
        ), patch.object(
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


def test_factory_analyst_team_llm_can_limit_to_single_specialist(monkeypatch) -> None:
    ctx = _sample_context()
    monkeypatch.setattr(agent_factory, "LLM_OVERRIDE_THRESHOLD", 0.65)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    llm_json = {
        "bias": "bullish",
        "confidence": 0.9,
        "summary": "LLM 单独调试技术分析师",
        "items": [
            {"category": "technical", "summary": "4h BOS 向上", "strength": 0.85, "timeframe": "4h"},
            {"category": "technical", "summary": "1h 趋势偏多", "strength": 0.8, "timeframe": "1h"},
            {"category": "technical", "summary": "EMA20 上方", "strength": 0.7, "timeframe": "5m"},
            {"category": "technical", "summary": "FVG 支撑", "strength": 0.65, "timeframe": "15m"},
        ],
        "level_reactions": [
            {
                "id": "tech_reaction:0",
                "label": "POC",
                "price": 4205.0,
                "timeframe": "5m",
                "expected_reaction": "支撑反弹",
            },
            {
                "id": "tech_reaction:1",
                "label": "阻力",
                "price": 4218.0,
                "timeframe": "15m",
                "expected_reaction": "承压回落",
            },
        ],
    }
    calls: list[str] = []

    def fake_technical(_ctx):
        from src.core.types import LLMStageTrace

        calls.append("technical")
        report = parse_analyst_report(llm_json, agent="technical_analyst")
        return report, LLMStageTrace(stage="technical", model="test-model", latency_ms=10)

    def fail_other(_ctx):
        raise AssertionError("non-selected analyst LLM runner should not be called")

    with bind_run_config(
        agent_mode="hybrid",
        llm_enabled=True,
        llm_stage_analysts=True,
        llm_analyst_only="technical",
    ), patch.object(agent_factory, "run_llm_technical_analyst", side_effect=fake_technical), patch.object(
        agent_factory, "run_llm_fundamentals_analyst", side_effect=fail_other
    ), patch.object(agent_factory, "run_llm_news_analyst", side_effect=fail_other), patch.object(
        agent_factory, "run_llm_sentiment_analyst", side_effect=fail_other
    ):
        meta = AgentPipelineMeta()
        team = agent_factory.run_analyst_team(ctx, meta)

    assert calls == ["technical"]
    assert team.technical.summary == "LLM 单独调试技术分析师"
    assert meta.stages["analyst_team"].source == "hybrid"
    assert meta.stages["technical"].source == "hybrid"
    assert meta.stages["fundamentals"].source == "rule"
    assert "llm_analyst_only=technical" in (meta.stages["fundamentals"].fallback_reason or "")


def test_factory_analyst_team_parallel_faster(monkeypatch) -> None:
    import time

    ctx = _sample_context()
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_ENABLED", True)
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_MAX_WORKERS", 4)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)
    delay = 0.08

    def slow(_ctx):
        from src.core.types import LLMStageTrace

        time.sleep(delay)
        return None, LLMStageTrace(stage="x", model="m", error="skip")

    t0 = time.perf_counter()
    with bind_run_config(agent_mode="hybrid", llm_enabled=True, llm_stage_analysts=True), patch.object(
        agent_factory, "run_llm_technical_analyst", side_effect=slow
    ), patch.object(
        agent_factory, "run_llm_fundamentals_analyst", side_effect=slow
    ), patch.object(agent_factory, "run_llm_news_analyst", side_effect=slow), patch.object(
        agent_factory, "run_llm_sentiment_analyst", side_effect=slow
    ):
        agent_factory.run_analyst_team(ctx, AgentPipelineMeta())
    elapsed = time.perf_counter() - t0
    assert elapsed < delay * 4


def test_factory_analyst_team_llm_mode_without_rule_baseline(monkeypatch) -> None:
    """Pure LLM mode skips rule baseline; successful parallel LLM must not assert."""
    ctx = _sample_context()
    monkeypatch.setattr(agent_factory, "LLM_PARALLEL_ENABLED", True)
    monkeypatch.setattr(agent_factory, "_use_llm_stage", lambda enabled: enabled)

    def fake_llm(stage: str):
        def _run(_ctx):
            from src.core.types import LLMStageTrace

            payload: dict = {
                "bias": "neutral",
                "confidence": 0.8,
                "summary": f"LLM {stage}",
                "items": [
                    {"category": stage, "summary": f"{stage} item {i}", "strength": 0.7}
                    for i in range(4)
                ],
            }
            if stage == "technical":
                payload["level_reactions"] = [
                    {
                        "id": "tech_reaction:0",
                        "label": "POC",
                        "price": 4200.0,
                        "timeframe": "5m",
                        "expected_reaction": "支撑反弹",
                    },
                    {
                        "id": "tech_reaction:1",
                        "label": "阻力",
                        "price": 4210.0,
                        "timeframe": "15m",
                        "expected_reaction": "承压回落",
                    },
                ]
            report = parse_analyst_report(payload, agent=f"{stage}_analyst")
            return report, LLMStageTrace(stage=stage, model="test-model", latency_ms=10)

        return _run

    with bind_run_config(agent_mode="llm", llm_enabled=True, llm_stage_analysts=True), patch.object(
        agent_factory, "run_llm_technical_analyst", side_effect=fake_llm("technical")
    ), patch.object(
        agent_factory, "run_llm_fundamentals_analyst", side_effect=fake_llm("fundamentals")
    ), patch.object(agent_factory, "run_llm_news_analyst", side_effect=fake_llm("news")), patch.object(
        agent_factory, "run_llm_sentiment_analyst", side_effect=fake_llm("sentiment")
    ):
        meta = AgentPipelineMeta()
        team = agent_factory.run_analyst_team(ctx, meta)

    assert team.technical.summary == "LLM technical"
    assert team.fundamentals.summary == "LLM fundamentals"
    assert meta.stages["analyst_team"].source == "llm"
    assert meta.stages["technical"].source == "llm"


def test_factory_analyst_team_llm_disabled_uses_rule(monkeypatch) -> None:
    ctx = _sample_context()

    with bind_run_config(llm_stage_analysts=False):
        meta = AgentPipelineMeta()
        team = agent_factory.run_analyst_team(ctx, meta)
    assert team.fundamentals.bias == "bearish"
    assert meta.stages["analyst_team"].source == "rule"
