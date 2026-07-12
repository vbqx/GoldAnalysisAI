"""Agent factory — rule / llm / hybrid dispatch for each pipeline stage."""

from __future__ import annotations

import json
import time

from src.agents.analysts import run_analyst_team as rule_analyst_team
from src.agents.bearish import run_bearish_researcher as rule_bearish
from src.agents.bullish import run_bullish_researcher as rule_bullish
from src.agents.debate import run_debate as rule_debate
from src.agents.llm.payload import market_payload
from src.agents.llm.stages.analysts import (
    run_llm_fundamentals_analyst,
    run_llm_news_analyst,
    run_llm_sentiment_analyst,
    run_llm_technical_analyst,
)
from src.agents.llm.stages.bearish import run_llm_bearish
from src.agents.llm.stages.bullish import run_llm_bullish
from src.agents.llm.stages.debate import run_llm_debate
from src.agents.llm.stages.levels import run_llm_level_proposer
from src.agents.llm.stages.manager import run_llm_manager
from src.agents.llm.stages.risk import run_llm_risk
from src.agents.llm.stages.trader import run_llm_trader
from src.agents.manager import run_manager as rule_manager
from src.agents.risk import run_risk_team as rule_risk
from src.agents.trader import run_trader_agent as rule_trader
from src.analysis.risk_gates import apply_risk_gates
from src.config import (
    LLM_OVERRIDE_THRESHOLD,
    LLM_PARALLEL_ENABLED,
    LLM_PARALLEL_MAX_WORKERS,
    LLM_PARALLEL_RESEARCH,
)
from src.core.run_context import get_run_config
from src.core.parallel import run_parallel
from src.core.progress import get_progress
from src.analysis.report_engine import TradingSignal
from src.core.types import (
    AgentEvidence,
    AgentPipelineMeta,
    AnalystReport,
    AnalystTeam,
    LevelProposal,
    ManagerDecision,
    MarketContext,
    ResearchDebate,
    RiskReview,
    StageMeta,
    StageSource,
    TransactionProposal,
)
from src.llm.router import llm_configured
from src.log import get_logger

log = get_logger(__name__)


def _use_llm_stage(stage_enabled: bool) -> bool:
    if get_run_config().agent_mode == "rule":
        return False
    if not stage_enabled:
        return False
    if not llm_configured():
        log.warning("agent_mode=%s but LLM_API_KEY missing — fallback to rule", get_run_config().agent_mode)
        return False
    return True


def _pick_evidence(
    stage: str,
    rule_result: AgentEvidence,
    llm_result: AgentEvidence | None,
    trace,
    pipeline: AgentPipelineMeta,
) -> AgentEvidence:
    if get_run_config().agent_mode == "rule" or llm_result is None:
        pipeline.record(stage, StageMeta(source="rule", llm=trace if trace and trace.error else None))
        return rule_result

    if get_run_config().agent_mode == "llm":
        if llm_result and not trace.error:
            pipeline.record(stage, StageMeta(source="llm", llm=trace))
            return llm_result
        pipeline.record(stage, StageMeta(source="rule", fallback_reason=trace.error, llm=trace))
        return rule_result

    # hybrid
    if llm_result and not trace.error and llm_result.confidence >= LLM_OVERRIDE_THRESHOLD:
        pipeline.record(stage, StageMeta(source="hybrid", llm=trace))
        return llm_result

    reason = trace.error or f"confidence {llm_result.confidence:.2f} < {LLM_OVERRIDE_THRESHOLD}"
    # hybrid 且 LLM 已参与：source=hybrid + fallback，UI 显示「混合·规则」而非纯「规则」
    pipeline.record(
        stage,
        StageMeta(source="hybrid", fallback_reason=f"采用规则输出：{reason}", llm=trace),
    )
    return rule_result


def _pick_analyst_report(
    stage: str,
    rule_result: AnalystReport,
    llm_result: AnalystReport | None,
    trace,
    pipeline: AgentPipelineMeta,
) -> AnalystReport:
    if get_run_config().agent_mode == "rule" or llm_result is None:
        if _use_llm_stage(get_run_config().llm_stage_analysts):
            pipeline.record(
                stage,
                StageMeta(source="rule", llm=trace if trace and trace.error else None),
            )
        return rule_result

    if get_run_config().agent_mode == "llm":
        if llm_result and not trace.error:
            pipeline.record(stage, StageMeta(source="llm", llm=trace))
            return llm_result
        pipeline.record(stage, StageMeta(source="rule", fallback_reason=trace.error, llm=trace))
        return rule_result

    if llm_result and not trace.error and llm_result.confidence >= LLM_OVERRIDE_THRESHOLD:
        pipeline.record(stage, StageMeta(source="hybrid", llm=trace))
        return llm_result

    reason = trace.error or f"confidence {llm_result.confidence:.2f} < {LLM_OVERRIDE_THRESHOLD}"
    pipeline.record(
        stage,
        StageMeta(source="hybrid", fallback_reason=f"采用规则输出：{reason}", llm=trace),
    )
    return rule_result


def _analyst_team_aggregate_source(llm_picked: int, total: int = 4) -> StageSource:
    if llm_picked == 0:
        return "rule"
    if llm_picked == total and get_run_config().agent_mode == "llm":
        return "llm"
    return "hybrid"


def _use_llm_analyst(stage: str) -> bool:
    return not get_run_config().llm_analyst_only or stage == get_run_config().llm_analyst_only


def _needs_rule_baseline() -> bool:
    """Hybrid always needs rule output; pure LLM tries LLM first."""
    return get_run_config().agent_mode == "hybrid"


def _llm_stage_ok(llm_result, trace) -> bool:
    return llm_result is not None and not (trace and trace.error)


def _ensure_rule_baseline(rule_result, llm_result, trace, compute_rule):
    """Lazy rule baseline: skip in pure LLM mode when LLM already succeeded."""
    if rule_result is not None:
        return rule_result
    if get_run_config().agent_mode == "llm" and _llm_stage_ok(llm_result, trace):
        return None
    return compute_rule()


def run_analyst_team(ctx: MarketContext, pipeline: AgentPipelineMeta) -> AnalystTeam:
    prog = get_progress()
    prog.update("analyst_team", detail="技术 · 基本面 · 新闻 · 情绪")
    t0 = time.perf_counter()
    use_llm = _use_llm_stage(get_run_config().llm_stage_analysts)
    rule_team = rule_analyst_team(ctx) if (not use_llm or _needs_rule_baseline()) else None
    input_payload = market_payload(ctx)

    if not use_llm:
        assert rule_team is not None
        elapsed = int((time.perf_counter() - t0) * 1000)
        prog.stage_io(
            "analyst_team",
            input_text=json.dumps(input_payload, ensure_ascii=False, indent=2),
            output_text=json.dumps(rule_team.to_dict(), ensure_ascii=False, indent=2),
            latency_ms=elapsed,
        )
        pipeline.record("analyst_team", StageMeta(source="rule"))
        return rule_team

    runners: list[tuple[str, AnalystReport, object]] = [
        ("technical", rule_team.technical if rule_team else None, run_llm_technical_analyst),
        ("fundamentals", rule_team.fundamentals if rule_team else None, run_llm_fundamentals_analyst),
        ("news", rule_team.news if rule_team else None, run_llm_news_analyst),
        ("sentiment", rule_team.sentiment if rule_team else None, run_llm_sentiment_analyst),
    ]

    llm_tasks: list[tuple[str, object]] = []
    picked: dict[str, AnalystReport] = {}
    for stage, rule_report, run_llm in runners:
        if not _use_llm_analyst(stage):
            assert rule_report is not None
            picked[stage] = rule_report
            pipeline.record(
                stage,
                StageMeta(source="rule", fallback_reason=f"llm_analyst_only={get_run_config().llm_analyst_only}，跳过 LLM"),
            )
            continue
        llm_tasks.append((stage, run_llm))

    parallel_count = len(llm_tasks)
    if parallel_count > 1 and LLM_PARALLEL_ENABLED:
        prog.update("analyst_team", detail=f"{parallel_count} 路 LLM 并行推理…")
        llm_results = run_parallel(
            [(stage, lambda fn=run_llm, c=ctx: fn(c)) for stage, run_llm in llm_tasks],
            max_workers=min(LLM_PARALLEL_MAX_WORKERS, parallel_count),
            label="analyst_team",
        )
    else:
        detail = f"LLM 单个分析师：{get_run_config().llm_analyst_only}" if get_run_config().llm_analyst_only else "LLM 四位分析师…"
        prog.update("analyst_team", detail=detail)
        llm_results = {stage: run_llm(ctx) for stage, run_llm in llm_tasks}

    llm_picked = 0
    rule_fallback: AnalystTeam | None = rule_team
    for stage, rule_report, _run_llm in runners:
        if stage in picked:
            continue
        if stage not in llm_results:
            continue
        llm_report, trace = llm_results[stage]
        if rule_report is None and get_run_config().agent_mode == "llm" and _llm_stage_ok(llm_report, trace):
            pipeline.record(stage, StageMeta(source="llm", llm=trace))
            picked[stage] = llm_report
            llm_picked += 1
            continue
        if rule_report is None:
            if rule_fallback is None:
                rule_fallback = rule_analyst_team(ctx)
            rule_report = getattr(rule_fallback, stage)
        assert rule_report is not None
        report = _pick_analyst_report(stage, rule_report, llm_report, trace, pipeline)
        picked[stage] = report
        if llm_report is not None and report is llm_report:
            llm_picked += 1

    team = AnalystTeam(
        technical=picked["technical"],
        fundamentals=picked["fundamentals"],
        news=picked["news"],
        sentiment=picked["sentiment"],
    )
    elapsed = int((time.perf_counter() - t0) * 1000)
    prog.stage_io(
        "analyst_team",
        input_text=json.dumps(input_payload, ensure_ascii=False, indent=2),
        output_text=json.dumps(team.to_dict(), ensure_ascii=False, indent=2),
        latency_ms=elapsed,
    )
    pipeline.record("analyst_team", StageMeta(source=_analyst_team_aggregate_source(llm_picked)))
    return team


def run_bullish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam) -> AgentEvidence:
    use_llm = _use_llm_stage(get_run_config().llm_stage_bullish)
    rule_result = rule_bullish(ctx, team) if (not use_llm or _needs_rule_baseline()) else None
    if not use_llm:
        get_progress().update("bullish", detail="规则引擎")
        pipeline.record("bullish", StageMeta(source="rule"))
        assert rule_result is not None
        return rule_result

    get_progress().update("bullish", detail="LLM 推理中…")
    llm_result, trace = run_llm_bullish(ctx, team)
    rule_result = _ensure_rule_baseline(
        rule_result, llm_result, trace, lambda: rule_bullish(ctx, team)
    )
    if rule_result is None:
        pipeline.record("bullish", StageMeta(source="llm", llm=trace))
        return llm_result
    return _pick_evidence("bullish", rule_result, llm_result, trace, pipeline)


def run_bearish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam) -> AgentEvidence:
    use_llm = _use_llm_stage(get_run_config().llm_stage_bearish)
    rule_result = rule_bearish(ctx, team) if (not use_llm or _needs_rule_baseline()) else None
    if not use_llm:
        get_progress().update("bearish", detail="规则引擎")
        pipeline.record("bearish", StageMeta(source="rule"))
        assert rule_result is not None
        return rule_result

    get_progress().update("bearish", detail="LLM 推理中…")
    llm_result, trace = run_llm_bearish(ctx, team)
    rule_result = _ensure_rule_baseline(
        rule_result, llm_result, trace, lambda: rule_bearish(ctx, team)
    )
    if rule_result is None:
        pipeline.record("bearish", StageMeta(source="llm", llm=trace))
        return llm_result
    return _pick_evidence("bearish", rule_result, llm_result, trace, pipeline)


def research_uses_parallel_llm() -> bool:
    """True when bullish/bearish LLM stages should run concurrently (saves wall time)."""
    return (
        LLM_PARALLEL_ENABLED
        and LLM_PARALLEL_RESEARCH
        and _use_llm_stage(get_run_config().llm_stage_bullish)
        and _use_llm_stage(get_run_config().llm_stage_bearish)
    )


def run_research_team(
    ctx: MarketContext,
    pipeline: AgentPipelineMeta,
    team: AnalystTeam,
) -> tuple[AgentEvidence, AgentEvidence]:
    """Run bullish and bearish research in parallel when both stages use LLM.

    Called from ``orchestrator`` when ``research_uses_parallel_llm()`` is true.
    Hybrid mode still computes rule baselines before picking LLM vs rule output.
    """
    bull_llm = _use_llm_stage(get_run_config().llm_stage_bullish)
    bear_llm = _use_llm_stage(get_run_config().llm_stage_bearish)

    if bull_llm and bear_llm and LLM_PARALLEL_ENABLED and LLM_PARALLEL_RESEARCH:
        rule_bull = rule_bullish(ctx, team) if _needs_rule_baseline() else None
        rule_bear = rule_bearish(ctx, team) if _needs_rule_baseline() else None
        results = run_parallel(
            [
                ("bullish", lambda: run_llm_bullish(ctx, team)),
                ("bearish", lambda: run_llm_bearish(ctx, team)),
            ],
            max_workers=2,
            label="research",
        )
        bullish_llm, bull_trace = results.get("bullish", (None, None))
        bearish_llm, bear_trace = results.get("bearish", (None, None))
        rule_bull = _ensure_rule_baseline(
            rule_bull, bullish_llm, bull_trace, lambda: rule_bullish(ctx, team)
        )
        rule_bear = _ensure_rule_baseline(
            rule_bear, bearish_llm, bear_trace, lambda: rule_bearish(ctx, team)
        )
        if rule_bull is None:
            pipeline.record("bullish", StageMeta(source="llm", llm=bull_trace))
            bullish = bullish_llm
        else:
            bullish = _pick_evidence("bullish", rule_bull, bullish_llm, bull_trace, pipeline)
        if rule_bear is None:
            pipeline.record("bearish", StageMeta(source="llm", llm=bear_trace))
            bearish = bearish_llm
        else:
            bearish = _pick_evidence("bearish", rule_bear, bearish_llm, bear_trace, pipeline)
        return bullish, bearish

    raise RuntimeError("run_research_team called without parallel LLM enabled")


def _pick_debate(
    rule_result: ResearchDebate,
    llm_result: ResearchDebate | None,
    trace,
    pipeline: AgentPipelineMeta,
) -> ResearchDebate:
    if get_run_config().agent_mode == "rule" or llm_result is None:
        pipeline.record("debate", StageMeta(source="rule", llm=trace if trace and trace.error else None))
        return rule_result

    if get_run_config().agent_mode == "llm":
        if llm_result and not trace.error:
            pipeline.record("debate", StageMeta(source="llm", llm=trace))
            return llm_result
        pipeline.record("debate", StageMeta(source="rule", fallback_reason=trace.error, llm=trace))
        return rule_result

    if llm_result and not trace.error and llm_result.consensus_strength >= LLM_OVERRIDE_THRESHOLD:
        pipeline.record("debate", StageMeta(source="hybrid", llm=trace))
        return llm_result

    reason = trace.error or f"strength {llm_result.consensus_strength:.2f} < {LLM_OVERRIDE_THRESHOLD}"
    pipeline.record(
        "debate",
        StageMeta(source="hybrid", fallback_reason=f"采用规则输出：{reason}", llm=trace),
    )
    return rule_result


def run_debate(
    bullish: AgentEvidence,
    bearish: AgentEvidence,
    analyses,
    pipeline: AgentPipelineMeta,
    team: AnalystTeam,
    ctx: MarketContext,
) -> ResearchDebate:
    if not _use_llm_stage(get_run_config().llm_stage_debate):
        get_progress().update("debate", detail="规则引擎")
        rule_result = rule_debate(bullish, bearish, analyses, team, ctx)
        pipeline.record("debate", StageMeta(source="rule"))
        return rule_result

    get_progress().update("debate", detail="LLM 辩论中…")
    if _needs_rule_baseline() and LLM_PARALLEL_ENABLED:
        results = run_parallel(
            [
                ("rule", lambda: rule_debate(bullish, bearish, analyses, team, ctx)),
                ("llm", lambda: run_llm_debate(bullish, bearish, analyses, ctx=ctx, team=team)),
            ],
            max_workers=2,
            label="debate",
        )
        rule_result = results["rule"]
        llm_result, trace = results["llm"]
        return _pick_debate(rule_result, llm_result, trace, pipeline)

    llm_result, trace = run_llm_debate(bullish, bearish, analyses, ctx=ctx, team=team)
    if get_run_config().agent_mode == "llm" and llm_result is not None and not trace.error:
        pipeline.record("debate", StageMeta(source="llm", llm=trace))
        return llm_result
    rule_result = rule_debate(bullish, bearish, analyses, team, ctx)
    return _pick_debate(rule_result, llm_result, trace, pipeline)


def run_level_proposer(
    ctx: MarketContext,
    team: AnalystTeam,
    debate: ResearchDebate,
    pipeline: AgentPipelineMeta,
    rule_signals: list[TradingSignal],
) -> list[LevelProposal]:
    if not _use_llm_stage(get_run_config().llm_stage_levels):
        log.info("llm_levels disabled or unavailable; using rule candidates only")
        pipeline.record("llm_levels", StageMeta(source="rule", fallback_reason="LLM_LEVELS disabled"))
        return []

    get_progress().update("llm_levels", detail="LLM 点位建议")
    proposals, trace = run_llm_level_proposer(ctx, team, debate, rule_signals)
    if proposals is not None and not trace.error:
        log.info("llm_levels accepted as stage output proposals=%d", len(proposals))
        pipeline.record("llm_levels", StageMeta(source="llm", llm=trace))
        return proposals

    log.warning("llm_levels fallback to rule candidates reason=%s", trace.error or "no proposals")
    pipeline.record(
        "llm_levels",
        StageMeta(source="rule", fallback_reason=trace.error or "LLM levels returned no proposals", llm=trace),
    )
    return []


def run_trader(
    ctx: MarketContext,
    debate: ResearchDebate,
    pipeline: AgentPipelineMeta,
    signals: list[TradingSignal],
):
    rule_result = rule_trader(ctx, debate, signals)
    if not _use_llm_stage(get_run_config().llm_stage_trader):
        get_progress().update("trader", detail="规则引擎")
        pipeline.record("trader", StageMeta(source="rule"))
        return rule_result

    get_progress().update("trader", detail="LLM 交易员提案")
    llm_result, trace = run_llm_trader(ctx, debate, signals)
    if get_run_config().agent_mode == "llm" and llm_result is not None and not trace.error:
        pipeline.record("trader", StageMeta(source="llm", llm=trace))
        return llm_result, signals
    if (
        llm_result is not None
        and not trace.error
        and (trace.confidence or 0.0) >= LLM_OVERRIDE_THRESHOLD
    ):
        pipeline.record("trader", StageMeta(source="hybrid", llm=trace))
        return llm_result, signals
    reason = trace.error or f"confidence {(trace.confidence or 0.0):.2f} < {LLM_OVERRIDE_THRESHOLD}"
    pipeline.record("trader", StageMeta(source="hybrid", fallback_reason=f"采用规则输出：{reason}", llm=trace))
    return rule_result


def run_risk(
    proposal: TransactionProposal,
    signals: list,
    pipeline: AgentPipelineMeta,
    *,
    current_price: float = 0.0,
    data_as_of: dict | None = None,
    observation_mode: bool = False,
) -> list[RiskReview]:
    def _gate(reviews: list[RiskReview]) -> list[RiskReview]:
        return apply_risk_gates(
            reviews,
            proposal,
            signals,
            current_price=current_price,
            data_as_of=data_as_of,
            observation_mode=observation_mode,
        )

    rule_result = rule_risk(
        proposal,
        len(signals),
        signals=signals,
        current_price=current_price,
        data_as_of=data_as_of,
        observation_mode=observation_mode,
    )
    if not _use_llm_stage(get_run_config().llm_stage_risk):
        pipeline.record("risk", StageMeta(source="rule"))
        return rule_result

    llm_result, trace = run_llm_risk(proposal, len(signals))
    if get_run_config().agent_mode == "llm" and llm_result is not None and not trace.error:
        pipeline.record("risk", StageMeta(source="llm", llm=trace))
        return _gate(llm_result)
    if (
        llm_result is not None
        and not trace.error
        and (trace.confidence or 0.0) >= LLM_OVERRIDE_THRESHOLD
    ):
        pipeline.record("risk", StageMeta(source="hybrid", llm=trace))
        return _gate(llm_result)
    reason = trace.error or f"confidence {(trace.confidence or 0.0):.2f} < {LLM_OVERRIDE_THRESHOLD}"
    pipeline.record("risk", StageMeta(source="hybrid", fallback_reason=f"采用规则输出：{reason}", llm=trace))
    return rule_result


def run_manager(proposal: TransactionProposal, reviews: list[RiskReview], pipeline: AgentPipelineMeta) -> ManagerDecision:
    rule_result = rule_manager(proposal, reviews)
    if not _use_llm_stage(get_run_config().llm_stage_manager):
        pipeline.record("manager", StageMeta(source="rule"))
        return rule_result

    llm_result, trace = run_llm_manager(proposal, reviews)
    if get_run_config().agent_mode == "llm" and llm_result is not None and not trace.error:
        pipeline.record("manager", StageMeta(source="llm", llm=trace))
        return llm_result
    if (
        llm_result is not None
        and not trace.error
        and llm_result.confidence >= LLM_OVERRIDE_THRESHOLD
    ):
        pipeline.record("manager", StageMeta(source="hybrid", llm=trace))
        return llm_result
    confidence = llm_result.confidence if llm_result else 0.0
    reason = trace.error or f"confidence {confidence:.2f} < {LLM_OVERRIDE_THRESHOLD}"
    pipeline.record("manager", StageMeta(source="hybrid", fallback_reason=f"采用规则输出：{reason}", llm=trace))
    return rule_result
