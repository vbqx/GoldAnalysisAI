"""LLM trader stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import trader_payload
from src.agents.llm.schemas import parse_transaction_proposal
from src.analysis.report_engine import TradingSignal
from src.core.types import LLMStageTrace, MarketContext, ResearchDebate, TransactionProposal
from src.llm.router import get_strong_client

SYSTEM = """You are the XAUUSD trader agent.
Choose a primary direction and a small set of candidate signal indexes from the supplied list.
Never invent levels. Never reference a signal index that is not present. Invalid signals must not be selected.
Return JSON:
{
  "primary_direction": "long|short|wait",
  "signal_indices": [0, 1],
  "confidence": 0.0-1.0,
  "rationale": ["reason 1", "reason 2"]
}"""


def run_llm_trader(
    ctx: MarketContext,
    debate: ResearchDebate,
    signals: list[TradingSignal],
) -> tuple[TransactionProposal | None, LLMStageTrace]:
    client = get_strong_client()
    payload = trader_payload(ctx, debate, signals)
    confidence_holder = {"value": None}

    def _parse(data: dict) -> TransactionProposal:
        try:
            confidence_holder["value"] = max(0.0, min(1.0, float(data.get("confidence", 0.5))))
        except (TypeError, ValueError):
            confidence_holder["value"] = 0.5
        return parse_transaction_proposal(
            data,
            debate_bias=debate.consensus_bias,
            signal_count=len(signals),
        )

    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"Create the trader proposal:\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="trader",
        model=client.model,
        client=client,
        messages=messages,
        parse=_parse,
    )
    if result:
        trace.confidence = confidence_holder["value"]
    return result, trace
