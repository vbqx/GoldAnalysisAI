"""TradeAgent-style orchestrator — data → research → trade → risk → manager → report."""

from __future__ import annotations

import json
import time

from src.agents import factory as agent_factory
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.level_validator import validate_llm_levels
from src.analysis.audit_summary import build_audit_summary
from src.analysis.fact_registry import build_fact_registry
from src.analysis.report_invariant_gate import apply_report_invariant_gate
from src.analysis.report_invariants import validate_report_invariants
from src.analysis.report_reliability import compute_report_reliability
from src.analysis.data_freshness import build_data_as_of
from src.analysis.narrative_sections import build_rule_narrative_sections, overview_bullets_from_sections
from src.analysis.report_engine import (
    align_conclusion_with_manager_decision,
    apply_manager_authorization,
    build_final_decision_meta,
    build_report,
    compute_trading_signals,
    parse_risk_events_calendar,
)
from src.core.parallel import run_parallel
from src.core.progress import get_progress
from src.core.run_context import agent_mode, get_run_config, llm_narrative_enabled
from src.core.types import AgentPipelineMeta, AgentTrace, LLMAnalysis, StageMeta
from src.core.orchestrator_hooks import (
    begin_pipeline_run,
    fetch_market_data,
    finalize_pipeline_archive,
    publish_external_snapshot,
)
from src.data.aggregator import assemble_market_context
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
    run_id, t0 = begin_pipeline_run()
    prog = get_progress()

    try:
        fetched = fetch_market_data()
    except RuntimeError:
        raise
    publish_external_snapshot(fetched, prog)
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
    as_of = build_data_as_of(raw)
    observation_mode = not as_of.get("executable", False)

    llm_level_proposals = []
    level_validation = []
    if get_run_config().llm_stage_levels and agent_mode() != "rule":
        levels_detail = "LLM 点位建议"
        if observation_mode:
            levels_detail += " · 观察模式（不授权执行）"
        prog.update("trader", detail=levels_detail)
        llm_level_proposals = agent_factory.run_level_proposer(
            ctx, analyst_team, debate, pipeline_meta, signals
        )
        if llm_level_proposals:
            llm_signals, level_validation = validate_llm_levels(ctx, llm_level_proposals)
            signals = llm_signals + signals
    elif agent_mode() != "rule":
        pipeline_meta.record(
            "llm_levels",
            StageMeta(source="rule", fallback_reason="LLM_STAGE_LEVELS disabled"),
        )
    proposal, signals = agent_factory.run_trader(
        ctx,
        debate,
        pipeline_meta,
        signals,
        analyst_team,
        observation_mode=observation_mode,
    )
    prog.done("trader", f"{proposal.primary_direction} · {len(proposal.signal_indices)} 信号")
    log.info(
        "trader proposal direction=%s signals=%d selected_idx=%s",
        proposal.primary_direction,
        len(signals),
        proposal.signal_indices,
    )

    prog.start("risk", "风控审核", "激进 · 中性 · 保守")
    risk_reviews = agent_factory.run_risk(
        proposal,
        signals,
        pipeline_meta,
        current_price=ctx.price,
        data_as_of=as_of,
        observation_mode=observation_mode,
    )
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
    report["meta"]["agent_mode"] = agent_mode()
    report["meta"]["run_config"] = get_run_config().to_dict()
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
        "headline_items": [h.to_dict() for h in ctx.external.headline_items[:12]],
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

    report["meta"]["data_as_of"] = as_of
    report["meta"]["run_config_fingerprint"] = get_run_config().fingerprint()
    report["meta"]["observation_mode"] = observation_mode
    report["meta"]["run_archive_id"] = run_id
    if as_of.get("warnings"):
        report["meta"].setdefault("warnings", []).extend(as_of["warnings"])
    if report["meta"]["observation_mode"]:
        conclusion = report.setdefault("conclusion", {})
        prefix = "【快照观察，非实时执行】"
        if not str(conclusion.get("action", "")).startswith(prefix):
            conclusion["action"] = prefix + str(conclusion.get("action", ""))

    apply_manager_authorization(report, decision, risk_reviews, proposal=proposal)
    align_conclusion_with_manager_decision(report)
    report["narrative_sections"] = build_rule_narrative_sections(report)
    report["market_overview"] = overview_bullets_from_sections(report["narrative_sections"])
    log.debug(
        "signals authorized by manager: selected=%s scale=%.2f action=%s",
        decision.selected_signal_indices,
        decision.position_scale,
        decision.action,
    )

    narrative_llm_enabled = llm_narrative_enabled()
    report["meta"]["fact_registry"] = build_fact_registry(report)
    if narrative_llm_enabled:
        prog.start("llm_narrative", "LLM 报告文案", "深度分析生成中…")
    llm_result = (
        run_llm_analysis(ctx, debate, decision, report)
        if narrative_llm_enabled
        else LLMAnalysis(enabled=False)
    )
    apply_llm_to_report(report, llm_result)
    report.setdefault("meta", {})["final_decision"] = build_final_decision_meta(report)
    if narrative_llm_enabled:
        prog.stage_io(
            "narrative_validation",
            label="五块文案校验",
            input_text=json.dumps(
                {"mode": agent_mode(), "sections": list((llm_result.narrative_sections or {}).keys())},
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

    report["meta"]["fact_registry"] = build_fact_registry(report)
    report["meta"]["report_invariants"] = validate_report_invariants(
        report,
        registry=report["meta"]["fact_registry"],
    )
    report["meta"]["report_invariants"] = apply_report_invariant_gate(
        report,
        report["meta"]["report_invariants"],
    )
    report["meta"]["fact_registry"] = build_fact_registry(report)
    report["meta"]["report_reliability"] = compute_report_reliability(report)
    if not report["meta"]["report_invariants"].get("passed"):
        codes = [
            v.get("code")
            for v in report["meta"]["report_invariants"].get("violations", [])[:5]
        ]
        report["meta"].setdefault("warnings", []).append(
            f"报告一致性校验未通过（已降级处理）：{', '.join(c for c in codes if c)}"
        )

    trace = AgentTrace(
        context=ctx.to_dict(),
        analyst_team=analyst_team.to_dict(),
        debate=debate.to_dict(),
        llm_levels=[p.to_dict() for p in llm_level_proposals],
        validated_plans=level_validation,
        proposal=proposal.to_dict(),
        risk_reviews=[r.to_dict() for r in risk_reviews],
        decision=decision.to_dict(),
        llm=report.get("llm_analysis") if llm_result.enabled else None,
        stage_meta=pipeline_meta.to_dict(),
    )
    report["agent_trace"] = trace.to_dict()
    report["meta"]["generation_steps"] = prog.snapshot()
    report["meta"]["llm_io"] = prog.llm_io_snapshot()
    llm_latencies = [r.get("latency_ms") or 0 for r in report["meta"]["llm_io"] if r.get("kind") != "rule"]
    if llm_latencies:
        report["meta"]["llm_stages_wall_ms"] = max(llm_latencies)

    report["meta"]["audit_summary"] = build_audit_summary(
        report,
        decision=decision,
        stage_meta=pipeline_meta.to_dict(),
    )
    audit = report["meta"]["audit_summary"]
    log.info(
        "audit_summary authorized=%s signal_ids=%s observation=%s",
        audit.get("execution_authorized"),
        audit.get("authorized_signal_ids"),
        audit.get("observation_mode"),
    )

    elapsed = time.perf_counter() - t0
    log.info(
        "pipeline done price=%.2f elapsed=%.2fs run_id=%s",
        report["metrics"]["current_price"],
        elapsed,
        run_id,
    )
    finalize_pipeline_archive(
        run_id,
        fetched=fetched,
        report=report,
        enriched=enriched,
        analyses=analyses,
        elapsed_s=elapsed,
    )
    return report, enriched, analyses
