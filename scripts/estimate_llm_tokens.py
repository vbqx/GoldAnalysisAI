#!/usr/bin/env python3
"""Rough per-stage LLM token budget (offline, sample context)."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.export_sample_report import _sample_context
from src.agents.analysts import run_analyst_team
from src.agents.bearish import run_bearish_researcher
from src.agents.bullish import run_bullish_researcher
from src.agents.debate import run_debate
from src.agents.llm.payload import (
    debate_payload,
    fundamentals_analyst_payload,
    level_proposer_payload,
    manager_payload,
    market_payload,
    news_analyst_payload,
    risk_payload,
    sentiment_analyst_payload,
    technical_analyst_payload,
    trader_payload,
)
from src.agents.manager import run_manager
from src.agents.risk import run_risk_team
from src.agents.trader import run_trader_agent
from src.analysis.report_engine import build_report, compute_trading_signals
from src.llm.context import build_llm_context
from src.llm.prompts import NARRATIVE_SECTIONS_PROMPT, SYSTEM_PROMPT


def _sys(mod: str) -> str:
    return getattr(importlib.import_module(mod), "SYSTEM")


def _est(chars: int) -> int:
    return int(chars / 1.8)


def main() -> int:
    ctx = _sample_context()
    team = run_analyst_team(ctx)
    bull = run_bullish_researcher(ctx, team)
    bear = run_bearish_researcher(ctx, team)
    debate = run_debate(bull, bear, ctx.analyses, team=team, ctx=ctx)
    signals = compute_trading_signals(ctx)
    proposal, signals = run_trader_agent(ctx, debate, signals)
    risk = run_risk_team(proposal, len(signals))
    decision = run_manager(proposal, risk)
    report = build_report(ctx.enriched, ctx.analyses, signals=signals)

    out_est = {
        "technical": 500,
        "fundamentals": 400,
        "news": 500,
        "sentiment": 400,
        "bullish": 600,
        "bearish": 600,
        "debate": 500,
        "trader": 300,
        "risk": 600,
        "manager": 200,
        "levels": 800,
        "llm_narrative": 2500,
    }

    stages = [
        ("technical", "FAST", _sys("src.agents.llm.stages.analysts.technical"), technical_analyst_payload(ctx)),
        ("fundamentals", "FAST", _sys("src.agents.llm.stages.analysts.fundamentals"), fundamentals_analyst_payload(ctx)),
        ("news", "FAST", _sys("src.agents.llm.stages.analysts.news"), news_analyst_payload(ctx)),
        ("sentiment", "FAST", _sys("src.agents.llm.stages.analysts.sentiment"), sentiment_analyst_payload(ctx)),
        ("bullish", "FAST", _sys("src.agents.llm.stages.bullish"), market_payload(ctx, team)),
        ("bearish", "FAST", _sys("src.agents.llm.stages.bearish"), market_payload(ctx, team)),
        ("debate", "STRONG", _sys("src.agents.llm.stages.debate"), debate_payload(bull, bear, ctx.analyses, ctx=ctx, team=team)),
        ("trader", "STRONG", _sys("src.agents.llm.stages.trader"), trader_payload(ctx, debate, signals)),
        ("risk", "STRONG", _sys("src.agents.llm.stages.risk"), risk_payload(proposal, len(signals))),
        ("manager", "STRONG", _sys("src.agents.llm.stages.manager"), manager_payload(proposal, risk)),
        ("levels", "STRONG", _sys("src.agents.llm.stages.levels"), level_proposer_payload(ctx, team, debate, signals)),
        ("llm_narrative", "REPORT", SYSTEM_PROMPT + NARRATIVE_SECTIONS_PROMPT, build_llm_context(ctx, debate, decision, report)),
    ]

    print(f"{'stage':<16} {'model':<8} {'payload_KB':>10} {'in_tok':>8} {'out~':>6}")
    total_in = total_out = 0
    for name, model, system, payload in stages:
        body = json.dumps(payload, ensure_ascii=False)
        user = f"prefix\n{body}"
        inn = _est(len(system) + len(user))
        out = out_est[name]
        total_in += inn
        total_out += out
        print(f"{name:<16} {model:<8} {len(body)/1024:10.1f} {inn:8d} {out:6d}")
    total = total_in + total_out
    print("-" * 56)
    print(f"Sum input ~{total_in:,} tok  output ~{total_out:,} tok  total ~{total:,} tok")
    print(f"If cost=2 CNY/run => ~{2 / total * 1000:.3f} CNY per 1k tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
