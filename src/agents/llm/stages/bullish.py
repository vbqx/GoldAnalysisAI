"""LLM bullish researcher."""

from __future__ import annotations

import json
from typing import Any

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import market_payload
from src.agents.llm.schemas import parse_agent_evidence
from src.core.types import AgentEvidence, AnalystTeam, LLMStageTrace, MarketContext
from src.llm.router import get_fast_client

from src.analysis.field_glossary import PA_SMC_PRIORITY, RESEARCH_PRIORITY_HINT

SYSTEM = (
    f"""你是 XAUUSD 看多研究员，精通 LuxAlgo SMC 与 DGT 量价分析。
{RESEARCH_PRIORITY_HINT}
{PA_SMC_PRIORITY}
输入 JSON 含 analyst_team（技术/基本面/新闻/情绪四位分析师报告）与多周期结构事实。
优先引用 analyst_team 中与看多方向一致的证据，并补充 SMC 结构看多事实；PA 量价共振可加强置信度；不得编造价格或事件。
返回 JSON：
"""
    + """{
  "items": [{"category": "structure|liquidity|external|analyst_*", "summary": "...", "strength": 0.0-1.0, "timeframe": "4h"}],
  "confidence": 0.0-1.0,
  "summary": "一句话总结"
}"""
)


def run_llm_bullish(ctx: MarketContext, team: AnalystTeam | None = None) -> tuple[AgentEvidence | None, LLMStageTrace]:
    client = get_fast_client()
    payload = market_payload(ctx, team)
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
