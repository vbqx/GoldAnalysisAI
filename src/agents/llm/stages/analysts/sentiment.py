"""LLM Sentiment Analyst."""

from __future__ import annotations

from src.agents.llm.payload import sentiment_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 市场情绪分析师。
输入：structure_sentiment、timeframe_trends、social_posts（TV Ideas/Minds）、event_countdown（宏观事件临近时可放大波动预期）。
结合结构投票与社媒样本评估短期情绪；若 social_posts 为空，仅依据结构投票并在 summary 说明。
不得编造未给出的社媒指标。items 至少 4 条，每条含 source。
返回 JSON：
{ANALYST_JSON_SCHEMA}"""


def run_llm_sentiment_analyst(ctx: MarketContext) -> tuple[AnalystReport | None, LLMStageTrace]:
    return run_specialist_llm(
        ctx,
        stage="sentiment",
        agent="sentiment_analyst",
        system=SYSTEM,
        payload_fn=sentiment_analyst_payload,
        user_prefix="请输出情绪分析报告：",
    )
