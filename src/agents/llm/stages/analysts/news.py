"""LLM News Analyst."""

from __future__ import annotations

from src.agents.llm.payload import news_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext

SYSTEM = f"""你是 XAUUSD 新闻与事件风险分析师。
输入 channels 分三类：
- flash（快讯）：即时冲击，items 应引用具体快讯标题，标注短线波动方向
- articles（资讯）：政策/宏观叙事，items 应评估对中期黄金方向的影响
- calendar（日历）：高 importance 事件必须单独成条 evidence，含时间与事件名
news_topics 为规则聚类主题，可辅助归纳辩论焦点，不得编造未给出的标题。
不得编造新闻标题或未给出的讲话/数据。items 至少 4 条，且应覆盖至少 2 个 channel。
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
