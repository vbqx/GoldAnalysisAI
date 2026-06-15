"""Shared LLM runner for Analyst Team specialists."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from src.agents.llm.base import run_llm_stage
from src.agents.llm.schemas import parse_analyst_report
from src.core.types import AnalystReport, LLMStageTrace, MarketContext
from src.llm.router import get_fast_client

ANALYST_JSON_SCHEMA = """{
  "bias": "bullish|bearish|neutral",
  "items": [{"category": "...", "summary": "...", "strength": 0.0-1.0, "timeframe": "4h", "source": "数据来源标签"}],
  "confidence": 0.0-1.0,
  "summary": "一句话结论"
}
items 至少 4 条；每条须含 source（如 jin10 / macro / tradingview_ict / tradingview_social）。"""


def run_specialist_llm(
    ctx: MarketContext,
    *,
    stage: str,
    agent: str,
    system: str,
    payload_fn: Callable[[MarketContext], dict[str, Any]],
    user_prefix: str,
) -> tuple[AnalystReport | None, LLMStageTrace]:
    client = get_fast_client()
    payload = payload_fn(ctx)
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": f"{user_prefix}\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage=stage,
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda d: parse_analyst_report(d, agent=agent),
    )
    if result:
        trace.confidence = result.confidence
    return result, trace
