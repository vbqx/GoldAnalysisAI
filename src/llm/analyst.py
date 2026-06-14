"""LLM analyst — optional narrative layer on top of rule-based pipeline."""

from __future__ import annotations

import json
from typing import Any

from src.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_ENABLED,
    LLM_ENHANCE_CONCLUSION,
    LLM_MODEL,
    LLM_TIMEOUT,
)
from src.core.progress import get_progress
from src.core.types import LLMAnalysis, ManagerDecision, MarketContext, ResearchDebate
from src.llm.client import LLMClient, LLMClientError
from src.llm.context import build_llm_context
from src.llm.prompts import build_messages
from src.log import get_logger

log = get_logger(__name__)


def _disabled_result(reason: str = "LLM 未启用") -> LLMAnalysis:
    return LLMAnalysis(enabled=False, error=reason)


def _client_from_config() -> LLMClient:
    if not LLM_API_KEY:
        raise LLMClientError("未配置 LLM_API_KEY")
    return LLMClient(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        model=LLM_MODEL,
        timeout=LLM_TIMEOUT,
    )


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
    if not LLM_ENABLED:
        return _disabled_result()

    try:
        client = _client_from_config()
        context = build_llm_context(ctx, debate, decision, report)
        messages = build_messages(context)
        log.info("llm analysis start model=%s", LLM_MODEL)

        from src.agents.llm.base import _parse_llm_json, stream_llm_json

        raw = stream_llm_json(
            client,
            messages,
            stage="llm_narrative",
            temperature=0.3,
        )
        data = _parse_llm_json(raw)
        result = _parse_result(data, model=LLM_MODEL, provider=LLM_BASE_URL)
        log.info(
            "llm analysis done confidence=%.2f summary_len=%d",
            result.confidence,
            len(result.market_summary),
        )
        return result
    except LLMClientError as exc:
        log.warning("llm analysis failed: %s", exc)
        return LLMAnalysis(enabled=True, model=LLM_MODEL, provider=LLM_BASE_URL, error=str(exc))
    except Exception as exc:
        log.exception("llm analysis unexpected error")
        return LLMAnalysis(enabled=True, model=LLM_MODEL, provider=LLM_BASE_URL, error=str(exc))


def apply_llm_to_report(report: dict[str, Any], llm: LLMAnalysis) -> None:
    """Attach LLM output to report; optionally enhance rule-based conclusion."""
    report["llm_analysis"] = llm.to_dict()

    if not llm.enabled or llm.error or not LLM_ENHANCE_CONCLUSION:
        return

    conclusion = report.setdefault("conclusion", {})
    if llm.market_summary:
        conclusion["llm_market_summary"] = llm.market_summary
    if llm.trade_thesis:
        conclusion["llm_trade_thesis"] = llm.trade_thesis
        conclusion["direction_summary"] = llm.trade_thesis
    if llm.action_plan:
        conclusion["llm_action_plan"] = llm.action_plan
        conclusion["action"] = llm.action_plan.replace("\n", "；")
        conclusion["header_conclusion"] = (
            f"{llm.trade_thesis}。{conclusion['action']}"
            if llm.trade_thesis
            else conclusion.get("header_conclusion", "")
        )
    if llm.risks:
        conclusion["llm_risks"] = llm.risks
