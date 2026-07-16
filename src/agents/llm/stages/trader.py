"""LLM trader stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import trader_payload
from src.agents.llm.schemas import parse_transaction_proposal
from src.analysis.field_glossary import INTRADAY_GOLD_MANDATE, TRADER_PRIORITY_HINT
from src.analysis.report_engine import TradingSignal
from src.core.types import AnalystTeam, LLMStageTrace, MarketContext, ResearchDebate, TransactionProposal
from src.llm.router import client_for_stage

SYSTEM = f"""你是 XAUUSD 黄金日内交易员智能体。
{TRADER_PRIORITY_HINT}
根据 debate（高周期方向）与 analyst_team_summaries 从 candidate_signals 中选择主方向与日内 signal_index；
不得重读原始市场数据或重新发明价位；不要把 4H/1H 大区间当追单价。
返回 JSON：
{{
  "primary_direction": "long|short|wait",
  "signal_indices": [0, 1],
  "confidence": 0.0-1.0,
  "rationale": ["依据1", "依据2"]
}}"""


def run_llm_trader(
    ctx: MarketContext,
    debate: ResearchDebate,
    signals: list[TradingSignal],
    team: AnalystTeam | None = None,
) -> tuple[TransactionProposal | None, LLMStageTrace]:
    client = client_for_stage("trader")
    payload = trader_payload(ctx, debate, signals, team=team)
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
            "content": f"请生成交易员提案：\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="trader",
        model=client.model,
        client=client,
        messages=messages,
        parse=_parse,
        temperature=0.0,
    )
    if result:
        trace.confidence = confidence_holder["value"]
    return result, trace
