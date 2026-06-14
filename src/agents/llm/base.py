"""Shared utilities for LLM agent stages."""

from __future__ import annotations

import json
import re
import time
from typing import Any, Callable, TypeVar

from src.core.progress import get_progress
from src.core.types import LLMStageTrace
from src.llm.client import LLMClient, LLMClientError
from src.log import get_logger

log = get_logger(__name__)

T = TypeVar("T")

# Fix #4 [Bug] LLM 阶段 JSON 解析偶发失败，hybrid 模式回退规则引擎
# 解析或传输失败时自动重试；传输错误使用指数退避（整次 SSE 请求重打，非流内续传）。
_MAX_STAGE_RETRIES = 2
_TRANSPORT_BACKOFF_BASE_S = 1.0


def _parse_llm_json(raw: str) -> dict[str, Any]:
    """Parse LLM JSON output with light repair for truncated / wrapped responses.

    Fix #4 [Bug] LLM 阶段 JSON 解析偶发失败，hybrid 模式回退规则引擎
    原因：模型返回非纯 JSON、尾随逗号或截断时直接 json.loads 会抛错。
    """
    text = raw.strip()
    if not text:
        raise json.JSONDecodeError("empty response", text, 0)

    attempts = [text]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        attempts.append(text[start : end + 1])

    # Strip trailing commas before } or ]
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


def _backoff_seconds(attempt: int) -> float:
    return _TRANSPORT_BACKOFF_BASE_S * (2**attempt)


def stream_llm_json(
    client: LLMClient,
    messages: list[dict[str, str]],
    *,
    stage: str,
    temperature: float = 0.2,
) -> str:
    """Stream an LLM JSON response with transport retries. Raises LLMClientError on exhaustion."""
    last_exc: LLMClientError | None = None
    for attempt in range(_MAX_STAGE_RETRIES + 1):
        temp = temperature if attempt == 0 else min(temperature + 0.1, 0.5)
        try:
            return _stream_json_response(client, messages, stage=stage, temperature=temp)
        except LLMClientError as exc:
            last_exc = exc
            if attempt < _MAX_STAGE_RETRIES:
                wait = _backoff_seconds(attempt)
                log.warning(
                    "llm stage %s transport retry %d/%d after %.1fs: %s",
                    stage,
                    attempt + 1,
                    _MAX_STAGE_RETRIES,
                    wait,
                    exc,
                )
                time.sleep(wait)
                continue
            raise
    assert last_exc is not None
    raise last_exc


def _stream_json_response(
    client: LLMClient,
    messages: list[dict[str, str]],
    *,
    stage: str,
    temperature: float,
) -> str:
    prog = get_progress()
    prog.llm_begin(stage, client.model, messages)
    t0 = time.perf_counter()
    try:
        raw = prog.run_llm_stream(
            stage,
            client.chat_stream(
                messages,
                temperature=temperature,
                response_format={"type": "json_object"},
            ),
        )
        elapsed = int((time.perf_counter() - t0) * 1000)
        prog.llm_end(stage, raw, latency_ms=elapsed)
        return raw
    except LLMClientError as exc:
        elapsed = int((time.perf_counter() - t0) * 1000)
        prog.llm_end(stage, "", error=str(exc), latency_ms=elapsed)
        raise


def run_llm_stage(
    *,
    stage: str,
    model: str,
    client: LLMClient,
    messages: list[dict[str, str]],
    parse: Callable[[dict[str, Any]], T],
    temperature: float = 0.2,
) -> tuple[T | None, LLMStageTrace]:
    """Execute one LLM stage with streaming I/O; returns (result, trace)."""
    t0 = time.perf_counter()
    last_exc: Exception | None = None

    for attempt in range(_MAX_STAGE_RETRIES + 1):
        try:
            temp = temperature if attempt == 0 else min(temperature + 0.1, 0.5)
            raw = stream_llm_json(client, messages, stage=stage, temperature=temp)
            data = _parse_llm_json(raw)
            result = parse(data)
            elapsed = int((time.perf_counter() - t0) * 1000)
            trace = LLMStageTrace(stage=stage, model=model, latency_ms=elapsed)
            if attempt:
                log.info("llm stage %s ok %dms (retry %d)", stage, elapsed, attempt)
            else:
                log.info("llm stage %s ok %dms", stage, elapsed)
            return result, trace
        except LLMClientError as exc:
            elapsed = int((time.perf_counter() - t0) * 1000)
            log.warning("llm stage %s failed after retries: %s", stage, exc)
            return None, LLMStageTrace(stage=stage, model=model, latency_ms=elapsed, error=str(exc))
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            last_exc = exc
            if attempt < _MAX_STAGE_RETRIES:
                log.warning(
                    "llm stage %s json retry %d/%d: %s",
                    stage,
                    attempt + 1,
                    _MAX_STAGE_RETRIES,
                    exc,
                )
                time.sleep(_backoff_seconds(attempt))
                continue

    elapsed = int((time.perf_counter() - t0) * 1000)
    log.warning("llm stage %s failed: %s", stage, last_exc)
    return None, LLMStageTrace(
        stage=stage, model=model, latency_ms=elapsed, error=str(last_exc),
    )
