"""LLM debate moderator."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import evidence_payload
from src.agents.llm.schemas import parse_research_debate
from src.analysis.ict_pa import sentiment_score
from src.core.types import AgentEvidence, LLMStageTrace, ResearchDebate
from src.llm.router import get_strong_client


SYSTEM = """你是 XAUUSD 交易辩论主持人。
阅读多空研究员证据与多周期 sentiment，给出共识偏向。
返回 JSON：
{
  "consensus_bias": "bullish|bearish|neutral",
  "consensus_strength": 0.0-1.0,
  "discussion_notes": ["要点1", "要点2"],
  "dissent": "可选：保留的分歧说明"
}"""


def run_llm_debate(
    bullish: AgentEvidence,
    bearish: AgentEvidence,
    analyses,
) -> tuple[ResearchDebate | None, LLMStageTrace]:
    client = get_strong_client()
    sentiment = sentiment_score(analyses)
    payload = {
        "bullish": evidence_payload(bullish),
        "bearish": evidence_payload(bearish),
        "sentiment_vote": sentiment,
    }
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
    )
    if result:
        trace.confidence = result.consensus_strength
    return result, trace
