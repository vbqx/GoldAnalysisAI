"""LLM Sentiment Analyst."""

from __future__ import annotations

from src.agents.llm.payload import sentiment_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 市场情绪分析师。
结合多周期结构情绪投票、各周期 trend 与 external.social_sentiment（Reddit r/Gold+r/Forex）评估短期情绪。
若 social_sentiment 为「—」，仅依据结构投票，并在 summary 中说明社媒不可用；不得编造未给出的社媒指标。
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
