"""TradeAgent-style orchestrator — data → research → trade → risk → manager → report."""

from __future__ import annotations

import json
import time

from src.agents import factory as agent_factory
from src.config import AGENT_MODE, LLM_ENABLED
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.level_validator import validate_llm_levels
from src.analysis.report_engine import build_report, build_strategy_plans, compute_trading_signals, parse_risk_events_calendar
from src.core.parallel import run_parallel
from src.core.progress import get_progress
from src.core.types import AgentPipelineMeta, AgentTrace, LLMAnalysis, StageMeta
from src.data.aggregator import assemble_market_context
from src.data.fetch_pipeline import fetch_all_data
from src.data.tradingview import compute_price_drift_1d
from src.indicators.technical import enrich
from src.llm.analyst import apply_llm_to_report, run_llm_analysis
from src.log import get_logger

log = get_logger(__name__)


def run_trade_agent_pipeline() -> tuple[dict, dict, dict]:
    """
    End-to-end pipeline mirroring TradeAgent flow:

    1. 数据拉取        — K 线 + 新闻 / DXY / 社媒（fetch_pipeline）
    2. Enrich + ICT    — indicators + structure analysis
    3. Research team   — bullish / bearish → debate
    4. Trader agent    — transaction proposal
    5. Risk team       — aggressive / neutral / conservative
    6. Manager         — final decision
    7. Report builder  — same JSON schema for existing Streamlit UI
    """
    t0 = time.perf_counter()
    log.info("pipeline start")
    prog = get_progress()

    try:
        fetched = fetch_all_data()
    except RuntimeError:
        raise
    from src.viz.external_data_view import external_snapshot_from_fetch

    prog.set_external_snapshot(external_snapshot_from_fetch(fetched))
    raw = fetched.raw
    log.debug(
        "raw bars: %s",
        {tf: len(df) for tf, df in raw.items()},
    )

    prog.start("indicators", "计算技术指标")
    enriched = run_parallel(
        [(tf, lambda t=tf, d=df: enrich(d)) for tf, df in raw.items()],
        max_workers=5,
        label="indicators",
    )
    prog.done("indicators")
    log.debug("indicators enriched for %s", list(enriched.keys()))

    prog.start("ict", "ICT 结构分析", "5m · 15m · 1h · 4h · 1d")
    analyses = run_parallel(
        [(tf, lambda t=tf: analyze_timeframe(enriched[t], t)) for tf in ("5m", "15m", "1h", "4h", "1d")],
        max_workers=5,
        label="ict",
    )
    prog.done("ict")
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

    ctx = assemble_market_context(enriched, analyses, fetched.external, fetched.source_label)
    log.info(
        "market context price=%.2f source=%s",
        ctx.price,
        ctx.source_label,
    )

    pipeline_meta = AgentPipelineMeta()

    prog.start("analyst_team", "Analyst Team", "技术 · 基本面 · 新闻 · 情绪")
    analyst_team = agent_factory.run_analyst_team(ctx, pipeline_meta)
    prog.done(
        "analyst_team",
        f"技术 {analyst_team.technical.bias} · 基本面 {analyst_team.fundamentals.bias}",
    )
    log.info(
        "analyst team technical=%s fundamentals=%s news=%s sentiment=%s",
        analyst_team.technical.bias,
        analyst_team.fundamentals.bias,
        analyst_team.news.bias,
        analyst_team.sentiment.bias,
    )

    if agent_factory.research_uses_parallel_llm():
        prog.start("bullish", "看多研究", "与看空并行 LLM")
        prog.start_sibling("bearish", "看空研究", "与看多并行 LLM")
        bullish, bearish = agent_factory.run_research_team(ctx, pipeline_meta, analyst_team)
        prog.done("bullish", f"{len(bullish.items)} 条 · 置信 {bullish.confidence:.0%}")
        prog.done("bearish", f"{len(bearish.items)} 条 · 置信 {bearish.confidence:.0%}")
    else:
        prog.start("bullish", "看多研究")
        bullish = agent_factory.run_bullish(ctx, pipeline_meta, analyst_team)
        prog.done("bullish", f"{len(bullish.items)} 条 · 置信 {bullish.confidence:.0%}")
        prog.start("bearish", "看空研究")
        bearish = agent_factory.run_bearish(ctx, pipeline_meta, analyst_team)
        prog.done("bearish", f"{len(bearish.items)} 条 · 置信 {bearish.confidence:.0%}")
    log.info(
        "research bullish=%d items (conf=%.2f) bearish=%d items (conf=%.2f)",
        len(bullish.items),
        bullish.confidence,
        len(bearish.items),
        bearish.confidence,
    )

    prog.start("debate", "多空辩论")
    debate_signals = run_parallel(
        [
            (
                "debate",
                lambda: agent_factory.run_debate(
                    bullish, bearish, analyses, pipeline_meta, analyst_team, ctx
                ),
            ),
            ("signals", lambda: compute_trading_signals(ctx)),
        ],
        max_workers=2,
        label="debate_prep",
    )
    debate = debate_signals["debate"]
    signals = debate_signals["signals"]
    prog.done("debate", f"共识 {debate.consensus_bias} · {debate.consensus_strength:.0%}")
    log.info(
        "debate consensus=%s strength=%.2f",
        debate.consensus_bias,
        debate.consensus_strength,
    )

    prog.start("trader", "交易员提案")
    llm_level_proposals = []
    level_validation = []
    if agent_factory.LLM_STAGE_LEVELS and AGENT_MODE != "rule":
        prog.update("trader", detail="LLM level proposal")
        llm_level_proposals = agent_factory.run_level_proposer(ctx, analyst_team, debate, pipeline_meta, signals)
        llm_signals, level_validation = validate_llm_levels(ctx, llm_level_proposals)
        signals = llm_signals + signals
    else:
        pipeline_meta.record(
            "llm_levels",
            StageMeta(source="rule", fallback_reason="LLM_STAGE_LEVELS disabled"),
        )
    proposal, signals = agent_factory.run_trader(ctx, debate, pipeline_meta, signals)
    prog.done("trader", f"{proposal.primary_direction} · {len(proposal.signal_indices)} 信号")
    log.info(
        "trader proposal direction=%s signals=%d selected_idx=%s",
        proposal.primary_direction,
        len(signals),
        proposal.signal_indices,
    )

    prog.start("risk", "风控审核", "激进 · 中性 · 保守")
    risk_reviews = agent_factory.run_risk(proposal, len(signals), pipeline_meta)
    approved = sum(1 for r in risk_reviews if r.approved)
    prog.done("risk", f"{approved}/{len(risk_reviews)} 通过")
    for review in risk_reviews:
        log.info(
            "risk [%s] approved=%s scale=%.2f signals=%s",
            review.profile,
            review.approved,
            review.position_scale,
            review.allowed_signal_indices,
        )

    prog.start("manager", "经理决策")
    decision = agent_factory.run_manager(proposal, risk_reviews, pipeline_meta)
    prog.done("manager", f"{decision.action} · 置信 {decision.confidence:.0%}")
    log.info(
        "manager action=%s direction=%s confidence=%.2f — %s",
        decision.action,
        decision.primary_direction,
        decision.confidence,
        decision.summary,
    )

    prog.start("report", "组装报告")
    report = build_report(enriched, analyses, signals=signals)
    report["meta"]["data_source"] = ctx.source_label
    report["meta"]["agent_mode"] = AGENT_MODE
    report["meta"]["stage_sources"] = pipeline_meta.to_dict()
    report["meta"]["stage_sources"]["narrative_sections"] = {
        key: {"source": "rule", "accepted": True}
        for key in ("market_overview", "liquidity", "4h", "1h", "15m")
    }
    report["llm_levels"] = [p.to_dict() for p in llm_level_proposals]
    report["validated_plans"] = level_validation
    drift_1d = compute_price_drift_1d(raw["5m"], raw["1d"])
    report["meta"]["price_drift_1d"] = drift_1d
    if abs(drift_1d) > 0.5:
        report["meta"].setdefault("warnings", []).append(
            f"独立 1d 收盘与 5m 聚合 1d 相差 {drift_1d:+.2f} 点，请以 5m 现价为准核对执行价"
        )
    prog.done("report")

    report["external"] = {
        "dxy_impact": ctx.external.dxy_impact,
        "risk_events": ctx.external.risk_events,
        "news_headlines": ctx.external.news_headlines[:12],
        "headline_count": len(ctx.external.headline_items),
        "calendar_count": len(ctx.external.calendar_events),
        "macro_quotes": [m.to_dict() for m in ctx.external.macro_quotes],
        "news_topics": ctx.derived.get("news_topics", []),
        "event_countdown": ctx.derived.get("event_countdown", {}),
        "spot_cross_check": ctx.derived.get("spot_cross_check"),
        "jin10_kline_summary": ctx.derived.get("jin10_kline_summary"),
        "social_sentiment": ctx.external.social_sentiment,
        "social_posts": ctx.external.social_posts[:8],
        "sources": ctx.external.sources,
        "fetch_errors": ctx.external.fetch_errors[:5],
    }
    report["meta"]["context_stats"] = ctx.context_stats

    live_cal = parse_risk_events_calendar(ctx.external.risk_events)
    if live_cal:
        report["calendar_events"] = live_cal

    narrative_llm_enabled = LLM_ENABLED and AGENT_MODE in ("llm", "hybrid")
    if narrative_llm_enabled:
        prog.start("llm_narrative", "LLM 报告文案", "深度分析生成中…")
    llm_result = (
        run_llm_analysis(ctx, debate, decision, report)
        if narrative_llm_enabled
        else LLMAnalysis(enabled=False)
    )
    apply_llm_to_report(report, llm_result)
    if narrative_llm_enabled:
        prog.stage_io(
            "narrative_validation",
            label="五块文案校验",
            input_text=json.dumps(
                {"mode": AGENT_MODE, "sections": list((llm_result.narrative_sections or {}).keys())},
                ensure_ascii=False,
            ),
            output_text=json.dumps(llm_result.narrative_section_audit, ensure_ascii=False),
        )
        if llm_result.error:
            prog.fail("llm_narrative", llm_result.error)
        else:
            prog.done("llm_narrative", llm_result.model or "完成")
    else:
        prog.skip("llm_narrative", "LLM 报告文案", "未启用")

    trace = AgentTrace(
        context=ctx.to_dict(),
        analyst_team=analyst_team.to_dict(),
        debate=debate.to_dict(),
        llm_levels=[p.to_dict() for p in llm_level_proposals],
        validated_plans=level_validation,
        proposal=proposal.to_dict(),
        risk_reviews=[r.to_dict() for r in risk_reviews],
        decision=decision.to_dict(),
        llm=llm_result.to_dict() if llm_result.enabled else None,
        stage_meta=pipeline_meta.to_dict(),
    )
    report["agent_trace"] = trace.to_dict()
    report["meta"]["generation_steps"] = prog.snapshot()
    report["meta"]["llm_io"] = prog.llm_io_snapshot()
    llm_latencies = [r.get("latency_ms") or 0 for r in report["meta"]["llm_io"] if r.get("kind") != "rule"]
    if llm_latencies:
        report["meta"]["llm_stages_wall_ms"] = max(llm_latencies)

    if decision.selected_signal_indices:
        sig_dicts = report["signals"]
        ordered = [sig_dicts[i] for i in decision.selected_signal_indices if i < len(sig_dicts)]
        rest = [s for j, s in enumerate(sig_dicts) if j not in decision.selected_signal_indices]
        combined = ordered + rest
        sent = report.get("sentiment") or {}
        bearish_dominant = sent.get("bearish", 0) >= sent.get("bullish", 0)
        pref_theme = "short" if bearish_dominant else "long"
        combined.sort(key=lambda s: 0 if s.get("theme") == pref_theme else 1)
        for sig in combined:
            sig["signal_role"] = "primary" if sig.get("theme") == pref_theme else "alternate"
        report["signals"] = combined
        report["strategy_plans"] = build_strategy_plans(combined)
        log.debug("signals reordered by manager + sentiment theme: %s", decision.selected_signal_indices)

    elapsed = time.perf_counter() - t0
    log.info(
        "pipeline done price=%.2f elapsed=%.2fs",
        report["metrics"]["current_price"],
        elapsed,
    )
    return report, enriched, analyses
