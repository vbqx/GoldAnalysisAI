"""LLM debate moderator."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import debate_payload, evidence_payload
from src.agents.llm.schemas import parse_research_debate
from src.core.types import AgentEvidence, AnalystTeam, LLMStageTrace, MarketContext, ResearchDebate
from src.llm.router import get_debate_client

SYSTEM = """你是 XAUUSD 交易辩论主持人。
阅读多空研究员证据、Analyst Team 摘要、新闻主题聚类与 upcoming_calendar（未来宏观事件）。
给出共识偏向；高影响日历临近时应提高波动风险提示。
返回 JSON：
{
  "consensus_bias": "bullish|bearish|neutral",
  "consensus_strength": 0.0-1.0,
  "discussion_notes": ["要点1", "要点2", "要点3"],
  "dissent": "可选：保留的分歧说明"
}
discussion_notes 至少 3 条。"""


def run_llm_debate(
    bullish: AgentEvidence,
    bearish: AgentEvidence,
    analyses,
    *,
    ctx: MarketContext | None = None,
    team: AnalystTeam | None = None,
) -> tuple[ResearchDebate | None, LLMStageTrace]:
    client = get_debate_client()
    payload = debate_payload(bullish, bearish, analyses, ctx=ctx, team=team)
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"主持辩论并输出共识：\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="debate",
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda d: parse_research_debate(d, bullish=bullish, bearish=bearish),
        temperature=0.0,
    )
    if result:
        trace.confidence = result.consensus_strength
    return result, trace
