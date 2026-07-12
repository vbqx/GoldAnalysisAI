"""LLM analyst — optional narrative layer on top of rule-based pipeline."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import src.config as app_config
from src.analysis.narrative_sections import (
    validate_and_merge_llm_sections,
    validate_llm_top_level_fields,
)

from src.config import (
    LLM_BASE_URL,
    LLM_ENHANCE_CONCLUSION,
    LLM_MODEL,
)
from src.core.run_context import llm_narrative_enabled
from src.core.progress import get_progress
from src.core.types import LLMAnalysis, ManagerDecision, MarketContext, ResearchDebate
from src.llm.client import LLMClient, LLMClientError
from src.llm.context import build_llm_context
from src.llm.prompts import build_messages
from src.llm.router import client_for_model, llm_configured
from src.log import get_logger

log = get_logger(__name__)


def _error_result(report: dict[str, Any], error: str) -> LLMAnalysis:
    sections = deepcopy(report.get("narrative_sections") or {})
    audit: dict[str, Any] = {}
    for key, section in sections.items():
        section["source"] = "fallback"
        section["fallback_reason"] = error
        audit[key] = {"source": "fallback", "accepted": False, "fallback_reason": error}
    return LLMAnalysis(
        enabled=True,
        model=LLM_MODEL,
        provider=LLM_BASE_URL,
        error=error,
        narrative_sections=sections,
        narrative_section_audit=audit,
    )


def _disabled_result(reason: str = "LLM 未启用") -> LLMAnalysis:
    return LLMAnalysis(enabled=False, error=reason)


def _client_from_config() -> LLMClient:
    if not llm_configured():
        raise LLMClientError("未配置 LLM_API_KEY")
    return client_for_model(LLM_MODEL)


def _parse_result(data: dict[str, Any], *, model: str, provider: str) -> LLMAnalysis:
    action_plan = str(data.get("action_plan", "")).strip()
    risks = data.get("risks") or []
    if not isinstance(risks, list):
        risks = [str(risks)]
    watch = data.get("watch_levels") or []
    if not isinstance(watch, list):
        watch = [str(watch)]

    confidence = data.get("confidence", 0.5)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    return LLMAnalysis(
        enabled=True,
        model=model,
        provider=provider,
        market_summary=str(data.get("market_summary", "")).strip(),
        trade_thesis=str(data.get("trade_thesis", "")).strip(),
        action_plan=action_plan,
        risks=[str(r) for r in risks if str(r).strip()],
        watch_levels=[str(w) for w in watch if str(w).strip()],
        confidence=confidence,
        raw_response=json.dumps(data, ensure_ascii=False),
    )


def validate_llm_payload(
    data: dict[str, Any],
    report: dict[str, Any],
    *,
    facts: dict[str, Any] | None = None,
    mode: str | None = None,
    threshold: float | None = None,
    model: str | None = None,
    provider: str | None = None,
) -> LLMAnalysis:
    """Validate parsed LLM JSON against a report without calling the API."""
    from src.analysis.narrative_facts import build_narrative_facts_for_llm

    if facts is None:
        facts = build_narrative_facts_for_llm(report)
    result = _parse_result(
        data,
        model=model or LLM_MODEL or "offline",
        provider=provider or LLM_BASE_URL or "offline",
    )
    sections, section_audit = validate_and_merge_llm_sections(
        data.get("narrative_sections"),
        rule_sections=report.get("narrative_sections") or {},
        facts=facts,
        mode=mode or app_config.AGENT_MODE,
        threshold=app_config.LLM_OVERRIDE_THRESHOLD if threshold is None else threshold,
    )
    result.narrative_sections = sections
    result.narrative_section_audit = section_audit
    field_reasons = validate_llm_top_level_fields(data, facts=facts)
    rejected = {key: reason for key, reason in field_reasons.items() if reason}
    result.top_level_audit = {
        "accepted": not rejected,
        "fallback_reason": next(iter(rejected.values()), None) if rejected else None,
        "field_audit": field_reasons,
    }
    for field in rejected:
        setattr(result, field, "")
    return result


def run_llm_analysis(
    ctx: MarketContext,
    debate: ResearchDebate,
    decision: ManagerDecision,
    report: dict[str, Any],
) -> LLMAnalysis:
    """
    Call LLM to produce narrative analysis from structured pipeline output.
    Returns disabled/error result on failure — never raises to caller.
    """
    if not llm_narrative_enabled():
        return _disabled_result()

    try:
        client = _client_from_config()
        context = build_llm_context(ctx, debate, decision, report)
        messages = build_messages(context)
        log.info("llm analysis start model=%s", LLM_MODEL)

        from src.agents.llm.base import run_llm_stage

        data, trace = run_llm_stage(
            stage="llm_narrative",
            model=LLM_MODEL,
            client=client,
            messages=messages,
            parse=lambda payload: payload,
            temperature=0.0,
        )
        if data is None:
            return _error_result(report, trace.error or "LLM 报告文案失败")
        facts = context.get("narrative_facts") or {}
        result = validate_llm_payload(
            data,
            report,
            facts=facts,
            model=LLM_MODEL,
            provider=LLM_BASE_URL,
        )
        if result.top_level_audit.get("fallback_reason"):
            for field, reason in (result.top_level_audit.get("field_audit") or {}).items():
                if reason:
                    log.warning("llm top-level narrative rejected %s: %s", field, reason)
        log.info(
            "llm analysis done confidence=%.2f summary_len=%d",
            result.confidence,
            len(result.market_summary),
        )
        return result
    except LLMClientError as exc:
        log.warning("llm analysis failed: %s", exc)
        return _error_result(report, str(exc))
    except Exception as exc:
        log.exception("llm analysis unexpected error")
        return _error_result(report, str(exc))


def apply_llm_to_report(report: dict[str, Any], llm: LLMAnalysis) -> None:
    """Attach LLM output to report; optionally enhance rule-based conclusion."""
    report["llm_analysis"] = llm.to_dict()

    if llm.narrative_sections:
        report["narrative_sections"] = llm.narrative_sections
        stage_sources = report.setdefault("meta", {}).setdefault("stage_sources", {})
        stage_sources["narrative_sections"] = llm.narrative_section_audit

    top_audit = getattr(llm, "top_level_audit", None) or {}
    stage_sources = report.setdefault("meta", {}).setdefault("stage_sources", {})
    stage_sources["narrative_top_level"] = top_audit

    conclusion = report.setdefault("conclusion", {})
    if llm.market_summary:
        conclusion["llm_market_summary"] = llm.market_summary
    if llm.trade_thesis:
        conclusion["llm_trade_thesis"] = llm.trade_thesis
    if llm.action_plan:
        conclusion["llm_action_plan"] = llm.action_plan
    if llm.risks:
        conclusion["llm_risks"] = llm.risks

    if not llm.enabled or llm.error or not LLM_ENHANCE_CONCLUSION:
        return

    if report.get("meta", {}).get("observation_mode"):
        return

    if top_audit and not top_audit.get("accepted", True):
        return

    if llm.trade_thesis:
        conclusion["direction_summary"] = llm.trade_thesis
    if llm.action_plan:
        conclusion["action"] = llm.action_plan.replace("\n", "；")
        conclusion["header_conclusion"] = (
            f"{llm.trade_thesis}。{conclusion['action']}"
            if llm.trade_thesis
            else conclusion.get("header_conclusion", "")
        )
