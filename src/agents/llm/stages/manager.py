"""LLM portfolio manager stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import manager_payload
from src.agents.llm.schemas import parse_manager_decision
from src.core.types import LLMStageTrace, ManagerDecision, RiskReview, TransactionProposal
from src.llm.router import get_strong_client

SYSTEM = """You are the final XAUUSD portfolio manager.
Authorize execution only when risk reviews support it. Prefer reduce when approvals are mixed.
Use only signal indexes approved by risk. Return JSON:
{
  "action": "execute|reduce|wait",
  "selected_signal_indices": [0],
  "confidence": 0.0-1.0,
  "summary": "one concise authorization summary"
}"""


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
            "content": f"Make the final authorization:\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="manager",
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda d: parse_manager_decision(d, proposal=proposal, reviews=reviews),
    )
    if result:
        trace.confidence = result.confidence
    return result, trace
