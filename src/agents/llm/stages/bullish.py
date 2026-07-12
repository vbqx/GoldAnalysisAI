"""LLM bullish researcher."""

from __future__ import annotations

import json
from typing import Any

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import research_payload
from src.agents.llm.schemas import parse_agent_evidence
from src.core.types import AgentEvidence, AnalystTeam, LLMStageTrace, MarketContext
from src.llm.router import get_fast_client

from src.analysis.field_glossary import PA_SMC_PRIORITY, RESEARCH_PRIORITY_HINT

SYSTEM = (
    f"""你是 XAUUSD 看多研究员，精通 PA（量价结构）与 LuxAlgo SMC 分析。
{RESEARCH_PRIORITY_HINT}
{PA_SMC_PRIORITY}
输入 JSON 以 analyst_team 为主（四位分析师结论与证据）；structure_vote / event_risk 仅作交叉校验，不得绕过 analyst 重读原始新闻或重造结构结论。
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
    payload = research_payload(ctx, team, "bullish")
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
