"""LLM Technical Analyst."""

from __future__ import annotations

from src.agents.llm.payload import technical_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 技术分析师，精通 PA/ICT/SMC 与 EMA/VWAP。
输入字段：market_position（EMA/VWAP/区间）、jin10_kline_summary（金十 K 线摘要）、spot_cross_check（TV vs 金十报价）、多周期 structure。
根据 BOS/CHoCH、OB/FVG 距离与 EMA 位置给出技术偏向；若 spot/kline 与 TV 价偏差大应在 summary 标注。
不得编造未出现在输入中的价格或事件。items 至少 4 条，覆盖不少于 2 个 timeframe，每条含 source。
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
