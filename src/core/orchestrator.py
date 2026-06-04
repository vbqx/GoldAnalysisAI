"""TradeAgent-style orchestrator — data → research → trade → risk → manager → report."""

from __future__ import annotations

import time

from src.agents import (
    run_bearish_researcher,
    run_bullish_researcher,
    run_debate,
    run_manager,
    run_risk_team,
    run_trader_agent,
)
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.report_engine import build_report
from src.core.types import AgentTrace
from src.data.aggregator import build_market_context
from src.data.fetcher import fetch_multi_timeframe
from src.indicators.technical import enrich
from src.log import get_logger

log = get_logger(__name__)


def run_trade_agent_pipeline() -> tuple[dict, dict, dict]:
    """
    End-to-end pipeline mirroring TradeAgent flow:

    1. Data layer      — market (+ news/social/fundamentals stubs)
    2. Enrich + ICT    — indicators + structure analysis
    3. Research team   — bullish / bearish → debate
    4. Trader agent    — transaction proposal
    5. Risk team       — aggressive / neutral / conservative
    6. Manager         — final decision
    7. Report builder  — same JSON schema for existing Streamlit UI
    """
    t0 = time.perf_counter()
    log.info("pipeline start")

    raw = fetch_multi_timeframe()
    log.debug(
        "raw bars: %s",
        {tf: len(df) for tf, df in raw.items()},
    )

    enriched = {tf: enrich(df) for tf, df in raw.items()}
    log.debug("indicators enriched for %s", list(enriched.keys()))

    analyses = {
        "5m": analyze_timeframe(enriched["5m"], "5m"),
        "15m": analyze_timeframe(enriched["15m"], "15m"),
        "1h": analyze_timeframe(enriched["1h"], "1h"),
        "4h": analyze_timeframe(enriched["4h"], "4h"),
    }
    for tf, a in analyses.items():
        log.debug(
            "%s structure trend=%s bos=%s choch=%s fvg=%d ob=%d",
            tf,
            a.trend,
            a.bos or "—",
            a.choch or "—",
            len(a.active_fvgs),
            len(a.order_blocks),
        )

    ctx = build_market_context(enriched, analyses)
    log.info(
        "market context price=%.2f source=%s",
        ctx.price,
        ctx.source_label,
    )

    bullish = run_bullish_researcher(ctx)
    bearish = run_bearish_researcher(ctx)
    log.info(
        "research bullish=%d items (conf=%.2f) bearish=%d items (conf=%.2f)",
        len(bullish.items),
        bullish.confidence,
        len(bearish.items),
        bearish.confidence,
    )

    debate = run_debate(bullish, bearish, analyses)
    log.info(
        "debate consensus=%s strength=%.2f",
        debate.consensus_bias,
        debate.consensus_strength,
    )

    proposal, signals = run_trader_agent(ctx, debate)
    log.info(
        "trader proposal direction=%s signals=%d selected_idx=%s",
        proposal.primary_direction,
        len(signals),
        proposal.signal_indices,
    )

    risk_reviews = run_risk_team(proposal, len(signals))
    for review in risk_reviews:
        log.info(
            "risk [%s] approved=%s scale=%.2f signals=%s",
            review.profile,
            review.approved,
            review.position_scale,
            review.allowed_signal_indices,
        )

    decision = run_manager(proposal, risk_reviews)
    log.info(
        "manager action=%s direction=%s confidence=%.2f — %s",
        decision.action,
        decision.primary_direction,
        decision.confidence,
        decision.summary,
    )

    report = build_report(enriched, analyses)
    report["meta"]["data_source"] = ctx.source_label
    report["external"] = {
        "dxy_impact": ctx.external.dxy_impact,
        "risk_events": ctx.external.risk_events,
    }

    trace = AgentTrace(
        context=ctx.to_dict(),
        debate=debate.to_dict(),
        proposal=proposal.to_dict(),
        risk_reviews=[r.to_dict() for r in risk_reviews],
        decision=decision.to_dict(),
    )
    report["agent_trace"] = trace.to_dict()

    if decision.selected_signal_indices:
        sig_dicts = report["signals"]
        ordered = [sig_dicts[i] for i in decision.selected_signal_indices if i < len(sig_dicts)]
        rest = [s for j, s in enumerate(sig_dicts) if j not in decision.selected_signal_indices]
        report["signals"] = ordered + rest
        log.debug("signals reordered by manager: %s", decision.selected_signal_indices)

    elapsed = time.perf_counter() - t0
    log.info(
        "pipeline done price=%.2f elapsed=%.2fs",
        report["metrics"]["current_price"],
        elapsed,
    )
    return report, enriched, analyses
