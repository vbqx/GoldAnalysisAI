"""LLM News Analyst."""

from __future__ import annotations

from src.agents.llm.payload import news_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 新闻与事件风险分析师。
评估头条与日历事件对黄金波动与方向的影响；无头条时侧重事件风险与波动提示，bias 通常为 neutral。
不得编造新闻标题或未给出的讲话/数据。
返回 JSON：
{ANALYST_JSON_SCHEMA}"""


def run_llm_news_analyst(ctx: MarketContext) -> tuple[AnalystReport | None, LLMStageTrace]:
    return run_specialist_llm(
        ctx,
        stage="news",
        agent="news_analyst",
        system=SYSTEM,
        payload_fn=news_analyst_payload,
        user_prefix="请输出新闻/事件风险分析报告：",
    )
