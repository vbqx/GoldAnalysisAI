"""LLM Technical Analyst."""

from __future__ import annotations

from src.agents.llm.payload import technical_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 技术分析师，精通 PA/ICT/SMC 与 EMA/VWAP。
根据输入的多周期结构、BOS/CHoCH、OB/FVG 与 EMA 位置给出技术偏向。
不得编造未出现在输入中的价格或事件。
返回 JSON：
{ANALYST_JSON_SCHEMA}"""


def run_llm_technical_analyst(ctx: MarketContext) -> tuple[AnalystReport | None, LLMStageTrace]:
    return run_specialist_llm(
        ctx,
        stage="technical",
        agent="technical_analyst",
        system=SYSTEM,
        payload_fn=technical_analyst_payload,
        user_prefix="请输出技术分析报告：",
    )
