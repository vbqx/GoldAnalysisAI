"""Pipeline signal generation — single source for trader and report."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.agents.trader import run_trader_agent
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.report_engine import build_report, compute_trading_signals
from src.core.types import AgentEvidence, ExternalFactors, MarketContext, ResearchDebate
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
        external=ExternalFactors(),
        source_label="test",
    )


def test_build_report_uses_provided_signals_without_regenerating() -> None:
    ctx = _sample_context()
    signals = compute_trading_signals(ctx)

    with patch(
        "src.analysis.report_engine.generate_trading_signals",
        side_effect=AssertionError("build_report must not regenerate signals"),
    ):
        report = build_report(ctx.enriched, ctx.analyses, signals=signals)

    assert len(report["signals"]) == len(signals)
    assert report["signals"][0]["name"] == signals[0].name


def test_trader_and_report_share_same_signal_objects() -> None:
    ctx = _sample_context()
    signals = compute_trading_signals(ctx)
    empty = AgentEvidence("test", "neutral", [], 0.5, "—")
    debate = ResearchDebate(
        bullish=empty,
        bearish=empty,
        consensus_bias="bearish",
        consensus_strength=0.6,
        discussion_notes=["test"],
    )
    proposal, returned = run_trader_agent(ctx, debate, signals)
    report = build_report(ctx.enriched, ctx.analyses, signals=signals)

    assert returned is signals
    assert proposal.signal_indices
    idx = proposal.signal_indices[0]
    assert report["signals"][idx]["name"] == signals[idx].name
