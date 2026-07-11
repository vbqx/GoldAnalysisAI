#!/usr/bin/env python3
"""Export a脱敏 sample report JSON for docs/reference/examples/ (no network)."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.agents import factory as agent_factory
from src.agents.analysts import run_analyst_team
from src.agents.bearish import run_bearish_researcher
from src.agents.bullish import run_bullish_researcher
from src.agents.debate import run_debate
from src.agents.manager import run_manager
from src.agents.risk import run_risk_team
from src.agents.trader import run_trader_agent
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.report_engine import build_report, compute_trading_signals
from src.analysis.narrative_sections import build_rule_narrative_sections
from src.config import AGENT_MODE
from src.core.types import (
    AgentPipelineMeta,
    AgentTrace,
    ExternalFactors,
    HeadlineItem,
    MacroQuote,
    MarketContext,
)
from src.indicators.technical import enrich

OUT = ROOT / "docs" / "reference" / "examples" / "sample-report.json"


def _sanitize(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return round(obj, 4) if abs(obj) < 1e6 else obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def _sample_context() -> MarketContext:
    idx = pd.date_range("2026-06-01", periods=120, freq="5min", tz="UTC")
    close = pd.Series(2650.0 + pd.Series(range(120), dtype=float).to_numpy() * 0.08, index=idx)
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [120] * 120,
        },
        index=idx,
    )
    enriched = {tf: enrich(df) for tf in ("5m", "15m", "1h", "4h", "1d")}
    analyses = {tf: analyze_timeframe(enriched[tf], tf) for tf in enriched}
    price = round(float(close.iloc[-1]), 2)
    external = ExternalFactors(
        dxy_impact="偏强 (104.2, 日 +0.35%) → 利空黄金",
        news_headlines=["【样例】美联储官员发表鹰派言论", "【样例】地缘局势推升避险需求"],
        risk_events="【样例】美国 CPI 公布 · 高影响",
        headline_items=[
            HeadlineItem(
                source="jin10_flash",
                time="2026-06-15 10:30",
                title="【样例】黄金短线拉升",
                text="脱敏示例快讯，非实时数据。",
            )
        ],
        macro_quotes=[
            MacroQuote(
                name="DXY",
                symbol="TVC:DXY",
                close=104.2,
                change_pct=0.35,
                impact="偏强 → 利空黄金",
                bias="bearish",
            )
        ],
        social_sentiment="偏多 58% / 偏空 42%（样例）",
        sources={"dxy": "sample", "news": "sample", "social": "sample"},
    )
    return MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics={
            "current_price": price,
            "daily_change": -8.5,
            "daily_change_pct": -0.32,
            "daily_high": price + 12,
            "daily_low": price - 15,
        },
        price=price,
        external=external,
        source_label="OANDA:XAUUSD (sample)",
        context_stats={
            "headline_count": 1,
            "calendar_count": 1,
            "macro_quote_count": 1,
            "note": "脱敏样例，非 live 流水线输出",
        },
    )


def main() -> int:
    ctx = _sample_context()
    pipeline_meta = AgentPipelineMeta()

    team = run_analyst_team(ctx)
    bullish = run_bullish_researcher(ctx, team)
    bearish = run_bearish_researcher(ctx, team)
    debate = run_debate(bullish, bearish, ctx.analyses, team=team, ctx=ctx)
    signals = compute_trading_signals(ctx)
    proposal, signals = run_trader_agent(ctx, debate, signals)
    risk_reviews = run_risk_team(proposal, len(signals))
    decision = run_manager(proposal, risk_reviews)

    report = build_report(ctx.enriched, ctx.analyses, signals=signals)
    report["metrics"] = {**report.get("metrics", {}), **ctx.metrics}
    report["meta"]["data_source"] = ctx.source_label
    report["meta"]["agent_mode"] = AGENT_MODE
    report["meta"]["stage_sources"] = pipeline_meta.to_dict()
    report["meta"]["stage_sources"]["narrative_sections"] = {
        key: {"source": "rule", "accepted": True}
        for key in ("market_overview", "liquidity", "4h", "1h", "15m")
    }
    report["meta"]["context_stats"] = ctx.context_stats
    report["meta"]["sample"] = True
    report["meta"]["disclaimer"] = "脱敏样例 JSON，仅供文档与测试参考，非 live 报告"

    report["external"] = {
        "dxy_impact": ctx.external.dxy_impact,
        "news_headlines": ctx.external.news_headlines,
        "macro_quotes": [m.to_dict() for m in ctx.external.macro_quotes],
        "social_sentiment": ctx.external.social_sentiment,
        "sources": ctx.external.sources,
    }
    report["llm_levels"] = []
    report["validated_plans"] = []
    report["narrative_sections"] = build_rule_narrative_sections(report)

    trace = AgentTrace(
        context={"price": ctx.price, "sample": True},
        analyst_team=team.to_dict(),
        debate=debate.to_dict(),
        llm_levels=[],
        validated_plans=[],
        proposal=proposal.to_dict(),
        risk_reviews=[r.to_dict() for r in risk_reviews],
        decision=decision.to_dict(),
        stage_meta=pipeline_meta.to_dict(),
    )
    report["agent_trace"] = trace.to_dict()

    report = _sanitize(report)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
