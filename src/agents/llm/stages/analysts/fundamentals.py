"""LLM Fundamentals Analyst."""

from __future__ import annotations

from src.agents.llm.payload import fundamentals_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 基本面分析师，关注 macro_quotes（DXY/US10Y）、event_countdown（下一高影响事件小时数）与 calendar_high_impact。
根据 macro_quotes 与日历临近度评估黄金多空宏观偏向；若数据含「占位/回退」应在 summary 中标注。
不得编造未出现在输入中的经济数据。items 至少 4 条（每个 macro quote 至少 1 条），每条含 source=macro。
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
