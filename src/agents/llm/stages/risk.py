"""LLM risk review stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import risk_payload
from src.agents.llm.schemas import parse_risk_reviews
from src.analysis.field_glossary import RISK_MANAGER_HINT
from src.core.types import LLMStageTrace, RiskReview, TransactionProposal
from src.llm.router import get_strong_client

SYSTEM = f"""你是 XAUUSD 三档风控委员会（激进 / 中性 / 保守）。
{RISK_MANAGER_HINT}
分别审核交易员提案；position_scale 取值 0~1；只能使用提案中已有的 signal_index；notes 必须用简体中文。
返回 JSON：
{{
  "confidence": 0.0-1.0,
  "reviews": [
    {{"profile": "aggressive", "approved": true, "allowed_signal_indices": [0], "position_scale": 1.0, "notes": ["..."]}},
    {{"profile": "neutral", "approved": true, "allowed_signal_indices": [0], "position_scale": 0.7, "notes": ["..."]}},
    {{"profile": "conservative", "approved": false, "allowed_signal_indices": [], "position_scale": 0.0, "notes": ["..."]}}
  ]
}}"""


def run_llm_risk(
    proposal: TransactionProposal,
    signal_count: int,
) -> tuple[list[RiskReview] | None, LLMStageTrace]:
    client = get_strong_client()
    payload = risk_payload(proposal, signal_count)
    confidence_holder = {"value": None}

    def _parse(data: dict) -> list[RiskReview]:
        try:
            confidence_holder["value"] = max(0.0, min(1.0, float(data.get("confidence", 0.5))))
        except (TypeError, ValueError):
            confidence_holder["value"] = 0.5
        return parse_risk_reviews(data, proposal=proposal, signal_count=signal_count)

    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"请审核交易员提案：\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="risk",
        model=client.model,
        client=client,
        messages=messages,
        parse=_parse,
        temperature=0.0,
    )
    if result:
        trace.confidence = confidence_holder["value"]
    return result, trace
