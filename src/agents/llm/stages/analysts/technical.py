"""LLM Technical Analyst."""

from __future__ import annotations

from src.agents.llm.payload import technical_analyst_payload
from src.agents.llm.stages.analysts._common import ANALYST_JSON_SCHEMA, run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext
from src.analysis.field_glossary import ANALYST_PRIORITY_HINT, PA_SMC_PRIORITY

SYSTEM = f"""你是 XAUUSD 技术分析师。{ANALYST_PRIORITY_HINT}

{PA_SMC_PRIORITY}

输入优先级：
1. timeframes + lux_timeframe_panels（SMC 主）— 趋势、BOS/CHoCH、OB/FVG、溢价折价
2. price_action / price_action_summary（PA 辅）— POC/VA、量价 S/R、共振确认
3. support_resistance、indicators / fibonacci / market_position / ema_vwap_relation（参考）

输出要求：
- items 至少 4 条：至少 2 条 category="lux_panel" 或 structure（SMC，source="lux_smc_panel"）
- 至少 2 条 category="price_action"（PA，source="dgt_price_action"，优先 5m/15m POC/VA 或近端 S/R）
- spot/kline 与 TV 价偏差大时在 summary 标注

返回 JSON：
{ANALYST_JSON_SCHEMA}"""


def run_llm_technical_analyst(ctx: MarketContext) -> tuple[AnalystReport | None, LLMStageTrace]:
    return run_specialist_llm(
        ctx,
        stage="technical",
        agent="technical_analyst",
        system=SYSTEM,
        payload_fn=technical_analyst_payload,
        user_prefix="请输出技术分析报告（SMC 定结构，PA 确认价位）：",
    )
