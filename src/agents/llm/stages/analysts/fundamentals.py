"""LLM Fundamentals Analyst."""

from __future__ import annotations

from src.agents.llm.payload import fundamentals_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 基本面分析师，关注美元指数、实际利率与宏观对黄金的影响。
根据 external 字段（dxy_impact、risk_events 等）评估黄金多空宏观偏向；若数据含「占位/回退」应在 summary 中标注不确定性。
不得编造未出现在输入中的经济数据。
返回 JSON：
{ANALYST_JSON_SCHEMA}"""


def run_llm_fundamentals_analyst(ctx: MarketContext) -> tuple[AnalystReport | None, LLMStageTrace]:
    return run_specialist_llm(
        ctx,
        stage="fundamentals",
        agent="fundamentals_analyst",
        system=SYSTEM,
        payload_fn=fundamentals_analyst_payload,
        user_prefix="请输出基本面分析报告：",
    )
