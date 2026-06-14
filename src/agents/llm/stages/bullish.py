"""LLM bullish researcher."""

from __future__ import annotations

import json
from typing import Any

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import market_payload
from src.agents.llm.schemas import parse_agent_evidence
from src.core.types import AgentEvidence, LLMStageTrace, MarketContext
from src.llm.router import get_fast_client

SYSTEM = """你是 XAUUSD 看多研究员，精通 PA/ICT/SMC。
仅基于输入 JSON 中的事实提取看多证据，不得编造价格或事件。
返回 JSON：
{
  "items": [{"category": "structure|liquidity|external", "summary": "...", "strength": 0.0-1.0, "timeframe": "4h"}],
  "confidence": 0.0-1.0,
  "summary": "一句话总结"
}"""


def run_llm_bullish(ctx: MarketContext) -> tuple[AgentEvidence | None, LLMStageTrace]:
    client = get_fast_client()
    payload = market_payload(ctx)
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"提取看多证据：\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="bullish",
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda d: parse_agent_evidence(d, agent="bullish_researcher_llm", direction="bullish"),
    )
    if result:
        trace.confidence = result.confidence
    return result, trace
