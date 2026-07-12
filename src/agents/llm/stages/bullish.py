"""LLM bullish researcher."""

from __future__ import annotations

import json
from typing import Any

from src.agents.analysts.evidence_provenance import analyst_evidence_ids, evidence_registry
from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import RESEARCH_ITEMS_SCHEMA, research_payload
from src.agents.llm.schemas import parse_agent_evidence
from src.core.types import AgentEvidence, AnalystTeam, LLMStageTrace, MarketContext
from src.llm.router import get_fast_client

from src.analysis.field_glossary import PA_SMC_PRIORITY, RESEARCH_PRIORITY_HINT

_RESEARCH_ITEMS_SCHEMA = RESEARCH_ITEMS_SCHEMA

SYSTEM = (
    f"""你是 XAUUSD 看多研究员，精通 PA（量价结构）与 LuxAlgo SMC 分析。
{RESEARCH_PRIORITY_HINT}
{PA_SMC_PRIORITY}
输入 JSON 以 analyst_team 为主（四位分析师结论与 evidence_id + refs）；structure_vote / event_risk 仅作交叉校验，不得绕过 analyst 重读原始新闻或重造结构结论。
对 analyst_team 已有证据：必须保留原 evidence_id 与 refs，仅可压缩 summary；新增结构证据才分配新 evidence_id。
返回 JSON：
"""
    + """{
  "items": ["""
    + _RESEARCH_ITEMS_SCHEMA
    + """],
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
    allowed = analyst_evidence_ids(team) if team else None
    registry = evidence_registry(team) if team else None
    result, trace = run_llm_stage(
        stage="bullish",
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda d: parse_agent_evidence(
            d,
            agent="bullish_researcher_llm",
            direction="bullish",
            allowed_evidence_ids=allowed,
            evidence_registry=registry,
        ),
    )
    if result:
        trace.confidence = result.confidence
    return result, trace
