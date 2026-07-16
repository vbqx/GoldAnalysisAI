"""Shared utilities for LLM agent stages."""

from __future__ import annotations

import json
import re
import time
from typing import Any, Callable, TypeVar

from src.config import LLM_STAGE_WARN_MS
from src.core.progress import get_progress
from src.core.types import LLMStageTrace
from src.llm.client import LLMClient, LLMClientError
from src.llm.stage_policy import (
    apply_input_budget,
    build_routing_strategy,
    estimate_text_size,
    get_stage_policy,
)
from src.log import get_logger

log = get_logger(__name__)

T = TypeVar("T")

# Fix #4 [Bug] LLM 阶段 JSON 解析偶发失败，hybrid 模式回退规则引擎
# Issue #37: transport + JSON/schema share one countable attempt budget (no nested 3×3).


def _backoff_seconds(attempt: int) -> float:
    from src.config import LLM_RETRY_BACKOFF_BASE_S

    return LLM_RETRY_BACKOFF_BASE_S * (2**attempt)


def _parse_llm_json(raw: str) -> dict[str, Any]:
    """Parse LLM JSON output with light repair for truncated / wrapped responses."""
    text = raw.strip()
    if not text:
        raise json.JSONDecodeError("empty response", text, 0)

    attempts = [text]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        attempts.append(text[start : end + 1])

    for candidate in list(attempts):
        attempts.append(re.sub(r",(\s*[}\]])", r"\1", candidate))

    last_err: json.JSONDecodeError | None = None
    for candidate in attempts:
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
            raise ValueError("LLM JSON 根节点必须是 object")
        except json.JSONDecodeError as exc:
            last_err = exc
            continue

    assert last_err is not None
    raise last_err


def _stream_once(
    client: LLMClient,
    messages: list[dict[str, str]],
    *,
    stage: str,
    temperature: float,
) -> str:
    """Single upstream SSE request (no retries). Progress chunk updates only."""
    prog = get_progress()
    return prog.run_llm_stream(
        stage,
        client.chat_stream(
            messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        ),
    )


def stream_llm_json(
    client: LLMClient,
    messages: list[dict[str, str]],
    *,
    stage: str,
    temperature: float = 0.2,
    max_attempts: int | None = None,
) -> str:
    """Stream JSON with a countable attempt budget (transport only).

    Prefer :func:`run_llm_stage` for production stages — it unifies transport and
    JSON/schema retries under the same budget. This helper remains for transport
    unit tests and ad-hoc callers.
    """
    policy = get_stage_policy(stage)
    budget = max_attempts if max_attempts is not None else policy.max_attempts
    budget = max(1, int(budget))
    last_exc: LLMClientError | None = None
    for attempt in range(budget):
        temp = temperature if attempt == 0 else min(temperature + 0.1, 0.5)
        try:
            return _stream_once(client, messages, stage=stage, temperature=temp)
        except LLMClientError as exc:
            last_exc = exc
            if attempt + 1 < budget:
                wait = _backoff_seconds(attempt)
                log.warning(
                    "llm stage %s transport retry %d/%d after %.1fs: %s",
                    stage,
                    attempt + 1,
                    budget - 1,
                    wait,
                    exc,
                )
                time.sleep(wait)
                continue
            raise
    assert last_exc is not None
    raise last_exc


def run_llm_stage(
    *,
    stage: str,
    model: str,
    client: LLMClient,
    messages: list[dict[str, str]],
    parse: Callable[[dict[str, Any]], T],
    temperature: float = 0.2,
) -> tuple[T | None, LLMStageTrace]:
    """Execute one LLM stage with a unified attempt budget and telemetry."""
    policy = get_stage_policy(stage)
    routing = build_routing_strategy()
    messages, budget_action, budget_meta = apply_input_budget(messages, policy)
    if budget_action != "none":
        log.warning(
            "llm stage %s input budget %s: %s",
            stage,
            budget_action,
            budget_meta.get("budget_note"),
        )

    prog = get_progress()
    telemetry = {
        "tier": policy.tier,
        "attempt": 0,
        "input_chars": budget_meta.get("input_chars"),
        "input_tokens_est": budget_meta.get("input_tokens_est"),
        "budget": {
            "max_attempts": policy.max_attempts,
            "input_chars_soft": policy.input_chars_soft,
            "input_chars_hard": policy.input_chars_hard,
            "original_input_chars": budget_meta.get("original_input_chars"),
            "budget_note": budget_meta.get("budget_note"),
        },
        "budget_action": budget_action,
        "same_model_strategy": routing.get("same_model_strategy"),
        "policy_version": routing.get("policy_version"),
        "usage": None,  # provider usage not available on SSE path yet
    }
    prog.llm_begin(stage, model, messages, telemetry=telemetry)

    t0 = time.perf_counter()
    last_exc: Exception | None = None
    attempt_log: list[dict[str, Any]] = []
    max_attempts = policy.max_attempts
    raw = ""

    for attempt in range(max_attempts):
        attempt_t0 = time.perf_counter()
        temp = temperature if attempt == 0 else min(temperature + 0.1, 0.5)
        try:
            raw = _stream_once(client, messages, stage=stage, temperature=temp)
            data = _parse_llm_json(raw)
            result = parse(data)
            elapsed = int((time.perf_counter() - t0) * 1000)
            out_size = estimate_text_size(raw)
            end_tel = {
                **telemetry,
                "attempt": attempt + 1,
                **out_size,
                "usage": None,
            }
            prog.llm_end(stage, raw, latency_ms=elapsed, telemetry=end_tel)
            if elapsed >= policy.soft_latency_ms or elapsed >= LLM_STAGE_WARN_MS:
                log.warning(
                    "llm stage %s over soft latency: %dms (warn %dms)",
                    stage,
                    elapsed,
                    policy.soft_latency_ms,
                )
            if attempt:
                log.info("llm stage %s ok %dms (attempt %d)", stage, elapsed, attempt + 1)
            else:
                log.info("llm stage %s ok %dms", stage, elapsed)
            return result, LLMStageTrace(
                stage=stage,
                model=model,
                latency_ms=elapsed,
                tier=policy.tier,
                attempts=attempt + 1,
                attempt_log=attempt_log,
                input_chars=int(budget_meta.get("input_chars") or 0),
                input_tokens_est=int(budget_meta.get("input_tokens_est") or 0),
                output_chars=out_size["output_chars"],
                output_tokens_est=out_size["output_tokens_est"],
                budget_action=budget_action,
                usage=None,
                same_model_strategy=bool(routing.get("same_model_strategy")),
            )
        except LLMClientError as exc:
            attempt_ms = int((time.perf_counter() - attempt_t0) * 1000)
            entry = {
                "attempt": attempt + 1,
                "reason": "transport",
                "error": str(exc),
                "latency_ms": attempt_ms,
            }
            attempt_log.append(entry)
            prog.llm_note_attempt(
                stage,
                attempt=attempt + 1,
                reason="transport",
                error=str(exc),
                latency_ms=attempt_ms,
            )
            last_exc = exc
            if attempt + 1 >= max_attempts:
                break
            wait = _backoff_seconds(attempt)
            log.warning(
                "llm stage %s transport retry %d/%d after %.1fs: %s",
                stage,
                attempt + 1,
                max_attempts - 1,
                wait,
                exc,
            )
            time.sleep(wait)
            prog.llm_begin(
                stage,
                model,
                messages,
                telemetry={**telemetry, "attempt": attempt + 1, "reuse": True},
            )
            continue
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            attempt_ms = int((time.perf_counter() - attempt_t0) * 1000)
            entry = {
                "attempt": attempt + 1,
                "reason": "json_schema",
                "error": str(exc),
                "latency_ms": attempt_ms,
            }
            attempt_log.append(entry)
            prog.llm_note_attempt(
                stage,
                attempt=attempt + 1,
                reason="json_schema",
                error=str(exc),
                latency_ms=attempt_ms,
            )
            last_exc = exc
            if attempt + 1 >= max_attempts:
                break
            wait = _backoff_seconds(attempt)
            log.warning(
                "llm stage %s json retry %d/%d after %.1fs: %s",
                stage,
                attempt + 1,
                max_attempts - 1,
                wait,
                exc,
            )
            time.sleep(wait)
            prog.llm_begin(
                stage,
                model,
                messages,
                telemetry={**telemetry, "attempt": attempt + 1, "reuse": True},
            )
            continue

    elapsed = int((time.perf_counter() - t0) * 1000)
    err = str(last_exc) if last_exc else "llm stage failed"
    prog.llm_end(
        stage,
        raw,
        error=err,
        latency_ms=elapsed,
        telemetry={
            **telemetry,
            "attempt": len(attempt_log),
            **estimate_text_size(raw),
        },
    )
    log.warning("llm stage %s failed after %d attempts: %s", stage, len(attempt_log), last_exc)
    return None, LLMStageTrace(
        stage=stage,
        model=model,
        latency_ms=elapsed,
        error=err,
        tier=policy.tier,
        attempts=len(attempt_log),
        attempt_log=attempt_log,
        input_chars=int(budget_meta.get("input_chars") or 0),
        input_tokens_est=int(budget_meta.get("input_tokens_est") or 0),
        budget_action=budget_action,
        same_model_strategy=bool(routing.get("same_model_strategy")),
    )
