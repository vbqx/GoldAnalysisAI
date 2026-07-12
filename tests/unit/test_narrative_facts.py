"""Unified narrative facts builder for LLM context."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.analysis.narrative_facts import build_narrative_facts_for_llm
from src.core.types import ExternalFactors, MarketContext
from src.analysis.ict_pa import analyze_timeframe
from src.indicators.technical import enrich


def _sample_context() -> MarketContext:
    idx = pd.date_range("2026-01-01", periods=60, freq="5min", tz="UTC")
    close = 4200.0 + pd.Series(range(60), dtype=float) * 0.05
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [100] * 60,
        },
        index=idx,
    )
    enriched = {"5m": enrich(df)}
    analyses = {"5m": analyze_timeframe(enriched["5m"], "5m")}
    price = float(close.iloc[-1])
    return MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics={"current_price": price},
        price=price,
        external=ExternalFactors(),
        derived={},
        context_stats={},
        source_label="test",
    )


def _minimal_report() -> dict:
    return {
        "metrics": {"current_price": 2650.0},
        "signals": [],
        "liquidity": [],
        "timeframes": {},
        "sentiment": {},
        "conclusion": {},
        "meta": {},
    }


def test_build_narrative_facts_for_llm_with_ctx_builds_technical_context() -> None:
    ctx = _sample_context()
    with patch("src.analysis.narrative_facts.build_technical_context") as build_tc:
        build_tc.return_value = {"5m": {"trend": "bullish"}}
        facts = build_narrative_facts_for_llm(_minimal_report(), ctx=ctx)
    build_tc.assert_called_once()
    assert facts["common"]["metrics"]["current_price"] == 2650.0


def test_build_narrative_facts_for_llm_uses_explicit_technical_context() -> None:
    explicit = {"5m": {"trend": "bearish"}}
    with patch("src.analysis.narrative_facts.build_technical_context") as build_tc:
        facts = build_narrative_facts_for_llm(
            _minimal_report(),
            technical_context=explicit,
        )
    build_tc.assert_not_called()
    assert "common" in facts


def test_build_narrative_facts_for_llm_respects_event_limit() -> None:
    ctx = _sample_context()
    with patch("src.analysis.narrative_facts.build_technical_context") as build_tc:
        build_tc.return_value = {}
        build_narrative_facts_for_llm(_minimal_report(), ctx=ctx, event_limit=2)
    assert build_tc.call_args.kwargs["event_limit"] == 2
