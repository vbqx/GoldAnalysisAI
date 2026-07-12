"""LLM portfolio manager stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import manager_payload
from src.agents.llm.schemas import parse_manager_decision
from src.analysis.field_glossary import RISK_MANAGER_HINT
from src.core.types import LLMStageTrace, ManagerDecision, RiskReview, TransactionProposal
from src.llm.router import get_strong_client

SYSTEM = f"""你是 XAUUSD 最终授权经理。
{RISK_MANAGER_HINT}
仅在风控批准时授权执行；批准意见分歧时优先 reduce；只能使用风控 allowed_signal_indices 中的索引。
summary 必须用简体中文，一句话说明授权或观望原因。
返回 JSON：
{{
  "action": "execute|reduce|wait",
  "selected_signal_indices": [0],
  "confidence": 0.0-1.0,
  "summary": "一句简洁授权结论（简体中文）"
}}"""


def run_llm_manager(
    proposal: TransactionProposal,
    reviews: list[RiskReview],
) -> tuple[ManagerDecision | None, LLMStageTrace]:
    client = get_strong_client()
    payload = manager_payload(proposal, reviews)
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"请做出最终授权决策：\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="manager",
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda d: parse_manager_decision(d, proposal=proposal, reviews=reviews),
        temperature=0.0,
    )
    if result:
        trace.confidence = result.confidence
    return result, trace
