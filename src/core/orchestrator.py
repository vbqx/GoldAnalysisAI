"""TradeAgent-style orchestrator — data → research → trade → risk → manager → report."""

from __future__ import annotations

import time

from src.agents import factory as agent_factory
from src.config import AGENT_MODE, LLM_ENABLED
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.report_engine import build_report
from src.core.progress import get_progress
from src.core.types import AgentPipelineMeta, AgentTrace
from src.data.aggregator import build_market_context
from src.data.fetcher import fetch_multi_timeframe
from src.indicators.technical import enrich
from src.llm.analyst import apply_llm_to_report, run_llm_analysis
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
    prog = get_progress()

    prog.start("fetch", "拉取多周期行情", "TradingView / OANDA")
    raw = fetch_multi_timeframe()
    prog.done("fetch", f"{len(raw)} 个周期")
    log.debug(
        "raw bars: %s",
        {tf: len(df) for tf, df in raw.items()},
    )

    prog.start("indicators", "计算技术指标")
    enriched = {tf: enrich(df) for tf, df in raw.items()}
    prog.done("indicators")
    log.debug("indicators enriched for %s", list(enriched.keys()))

    prog.start("ict", "ICT 结构分析", "5m · 15m · 1h · 4h · 1d")
    analyses = {
        "5m": analyze_timeframe(enriched["5m"], "5m"),
        "15m": analyze_timeframe(enriched["15m"], "15m"),
        "1h": analyze_timeframe(enriched["1h"], "1h"),
        "4h": analyze_timeframe(enriched["4h"], "4h"),
        "1d": analyze_timeframe(enriched["1d"], "1d"),
    }
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

    prog.start("context", "构建市场上下文")
    ctx = build_market_context(enriched, analyses)
    prog.done("context", f"现价 {ctx.price:.2f}")
    log.info(
        "market context price=%.2f source=%s",
        ctx.price,
        ctx.source_label,
    )

    pipeline_meta = AgentPipelineMeta()

    prog.start("bullish", "看多研究")
    bullish = agent_factory.run_bullish(ctx, pipeline_meta)
    prog.done("bullish", f"{len(bullish.items)} 条 · 置信 {bullish.confidence:.0%}")

    prog.start("bearish", "看空研究")
    bearish = agent_factory.run_bearish(ctx, pipeline_meta)
    prog.done("bearish", f"{len(bearish.items)} 条 · 置信 {bearish.confidence:.0%}")
    log.info(
        "research bullish=%d items (conf=%.2f) bearish=%d items (conf=%.2f)",
        len(bullish.items),
        bullish.confidence,
        len(bearish.items),
        bearish.confidence,
    )

    prog.start("debate", "多空辩论")
    debate = agent_factory.run_debate(bullish, bearish, analyses, pipeline_meta)
    prog.done("debate", f"共识 {debate.consensus_bias} · {debate.consensus_strength:.0%}")
    log.info(
        "debate consensus=%s strength=%.2f",
        debate.consensus_bias,
        debate.consensus_strength,
    )

    prog.start("trader", "交易员提案")
    proposal, signals = agent_factory.run_trader(ctx, debate, pipeline_meta)
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
    report = build_report(enriched, analyses)
    report["meta"]["data_source"] = ctx.source_label
    report["meta"]["agent_mode"] = AGENT_MODE
    report["meta"]["stage_sources"] = pipeline_meta.to_dict()
    prog.done("report")

    report["external"] = {
        "dxy_impact": ctx.external.dxy_impact,
        "risk_events": ctx.external.risk_events,
    }

    if LLM_ENABLED:
        prog.start("llm_narrative", "LLM 报告文案", "深度分析生成中…")
    llm_result = run_llm_analysis(ctx, debate, decision, report)
    apply_llm_to_report(report, llm_result)
    if LLM_ENABLED:
        if llm_result.error:
            prog.fail("llm_narrative", llm_result.error)
        else:
            prog.done("llm_narrative", llm_result.model or "完成")
    else:
        prog.skip("llm_narrative", "LLM 报告文案", "未启用")

    trace = AgentTrace(
        context=ctx.to_dict(),
        debate=debate.to_dict(),
        proposal=proposal.to_dict(),
        risk_reviews=[r.to_dict() for r in risk_reviews],
        decision=decision.to_dict(),
        llm=llm_result.to_dict() if llm_result.enabled else None,
        stage_meta=pipeline_meta.to_dict(),
    )
    report["agent_trace"] = trace.to_dict()
    report["meta"]["generation_steps"] = prog.snapshot()
    report["meta"]["llm_io"] = prog.llm_io_snapshot()

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
