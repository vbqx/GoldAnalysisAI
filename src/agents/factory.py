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
from src.agents.manager import run_manager as rule_manager
from src.agents.risk import run_risk_team as rule_risk
from src.agents.trader import run_trader_agent as rule_trader
from src.config import (
    AGENT_MODE,
    LLM_OVERRIDE_THRESHOLD,
    LLM_STAGE_ANALYSTS,
    LLM_STAGE_DEBATE,
    LLM_STAGE_RESEARCH,
)
from src.core.progress import get_progress
from src.analysis.report_engine import TradingSignal
from src.core.types import (
    AgentEvidence,
    AgentPipelineMeta,
    AnalystReport,
    AnalystTeam,
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
    if AGENT_MODE == "rule":
        return False
    if not stage_enabled:
        return False
    if not llm_configured():
        log.warning("AGENT_MODE=%s but LLM_API_KEY missing — fallback to rule", AGENT_MODE)
        return False
    return True


def _pick_evidence(
    stage: str,
    rule_result: AgentEvidence,
    llm_result: AgentEvidence | None,
    trace,
    pipeline: AgentPipelineMeta,
) -> AgentEvidence:
    if AGENT_MODE == "rule" or llm_result is None:
        pipeline.record(stage, StageMeta(source="rule", llm=trace if trace and trace.error else None))
        return rule_result

    if AGENT_MODE == "llm":
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
    if AGENT_MODE == "rule" or llm_result is None:
        if _use_llm_stage(LLM_STAGE_ANALYSTS):
            pipeline.record(
                stage,
                StageMeta(source="rule", llm=trace if trace and trace.error else None),
            )
        return rule_result

    if AGENT_MODE == "llm":
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
    if llm_picked == total and AGENT_MODE == "llm":
        return "llm"
    return "hybrid"


def run_analyst_team(ctx: MarketContext, pipeline: AgentPipelineMeta) -> AnalystTeam:
    prog = get_progress()
    prog.update("analyst_team", detail="技术 · 基本面 · 新闻 · 情绪")
    t0 = time.perf_counter()
    rule_team = rule_analyst_team(ctx)
    input_payload = market_payload(ctx)

    if not _use_llm_stage(LLM_STAGE_ANALYSTS):
        elapsed = int((time.perf_counter() - t0) * 1000)
        prog.stage_io(
            "analyst_team",
            input_text=json.dumps(input_payload, ensure_ascii=False, indent=2),
            output_text=json.dumps(rule_team.to_dict(), ensure_ascii=False, indent=2),
            latency_ms=elapsed,
        )
        pipeline.record("analyst_team", StageMeta(source="rule"))
        return rule_team

    prog.update("analyst_team", detail="LLM 四位分析师…")
    runners: list[tuple[str, AnalystReport, object]] = [
        ("technical", rule_team.technical, run_llm_technical_analyst),
        ("fundamentals", rule_team.fundamentals, run_llm_fundamentals_analyst),
        ("news", rule_team.news, run_llm_news_analyst),
        ("sentiment", rule_team.sentiment, run_llm_sentiment_analyst),
    ]

    llm_picked = 0
    picked: dict[str, AnalystReport] = {}
    for stage, rule_report, run_llm in runners:
        llm_report, trace = run_llm(ctx)
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
    pipeline.record("analyst_team", StageMeta(source=_analyst_team_aggregate_source(llm_picked)))
    return team


def run_bullish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam) -> AgentEvidence:
    rule_result = rule_bullish(ctx, team)
    if not _use_llm_stage(LLM_STAGE_RESEARCH):
        get_progress().update("bullish", detail="规则引擎")
        pipeline.record("bullish", StageMeta(source="rule"))
        return rule_result

    get_progress().update("bullish", detail="LLM 推理中…")
    llm_result, trace = run_llm_bullish(ctx, team)
    return _pick_evidence("bullish", rule_result, llm_result, trace, pipeline)


def run_bearish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam) -> AgentEvidence:
    rule_result = rule_bearish(ctx, team)
    if not _use_llm_stage(LLM_STAGE_RESEARCH):
        get_progress().update("bearish", detail="规则引擎")
        pipeline.record("bearish", StageMeta(source="rule"))
        return rule_result

    get_progress().update("bearish", detail="LLM 推理中…")
    llm_result, trace = run_llm_bearish(ctx, team)
    return _pick_evidence("bearish", rule_result, llm_result, trace, pipeline)


def _pick_debate(
    rule_result: ResearchDebate,
    llm_result: ResearchDebate | None,
    trace,
    pipeline: AgentPipelineMeta,
) -> ResearchDebate:
    if AGENT_MODE == "rule" or llm_result is None:
        pipeline.record("debate", StageMeta(source="rule", llm=trace if trace and trace.error else None))
        return rule_result

    if AGENT_MODE == "llm":
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
) -> ResearchDebate:
    rule_result = rule_debate(bullish, bearish, analyses, team)
    if not _use_llm_stage(LLM_STAGE_DEBATE):
        get_progress().update("debate", detail="规则引擎")
        pipeline.record("debate", StageMeta(source="rule"))
        return rule_result

    get_progress().update("debate", detail="LLM 辩论中…")
    llm_result, trace = run_llm_debate(bullish, bearish, analyses)
    return _pick_debate(rule_result, llm_result, trace, pipeline)


def run_trader(
    ctx: MarketContext,
    debate: ResearchDebate,
    pipeline: AgentPipelineMeta,
    signals: list[TradingSignal],
):
    pipeline.record("trader", StageMeta(source="rule"))
    return rule_trader(ctx, debate, signals)


def run_risk(proposal: TransactionProposal, signal_count: int, pipeline: AgentPipelineMeta) -> list[RiskReview]:
    pipeline.record("risk", StageMeta(source="rule"))
    return rule_risk(proposal, signal_count)


def run_manager(proposal: TransactionProposal, reviews: list[RiskReview], pipeline: AgentPipelineMeta) -> ManagerDecision:
    pipeline.record("manager", StageMeta(source="rule"))
    return rule_manager(proposal, reviews)
