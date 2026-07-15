"""LLM Technical Analyst."""

from __future__ import annotations

from src.agents.llm.payload import technical_analyst_payload
from src.agents.llm.stages.analysts._common import run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext
from src.analysis.field_glossary import ANALYST_PRIORITY_HINT, INTRADAY_GOLD_MANDATE, PA_SMC_PRIORITY

TECHNICAL_JSON_SCHEMA = """{
  "bias": "bullish|bearish|neutral",
  "items": [{"category": "...", "summary": "...", "strength": 0.0-1.0, "timeframe": "4h", "source": "数据来源标签"}],
  "level_reactions": [
    {
      "id": "tech_reaction:0",
      "label": "POC|VAH|VAL|量价阻力|量价支撑|OB高|FVG低 等",
      "price": 0.0,
      "timeframe": "5m|15m|1h|4h",
      "expected_reaction": "承压回落|支撑反弹|假突破回收|扫低后收回 等",
      "fact_ids": ["逐字引用 technical_claim_facts[].fact_ids；区间须同时引用 low/high"],
      "relationships": [
        {
          "type": "overlap|near|contradiction",
          "left_fact_ids": ["一个事实实体的完整 fact_ids"],
          "right_fact_ids": ["另一个事实实体的完整 fact_ids"]
        }
      ],
      "rationale": "一两句：为何预期该反应（引用 payload 中的 PA/SMC 事实）",
      "strength": 0.0
    }
  ],
  "confidence": 0.0-1.0,
  "summary": "一句话结论"
}
items 至少 4 条；level_reactions 至少 2 条（供下游点位提案绑定，勿只写空方向）。"""

SYSTEM = f"""你是 XAUUSD 黄金日内技术分析师。{ANALYST_PRIORITY_HINT}

{PA_SMC_PRIORITY}

输入优先级：
1. timeframes + lux_timeframe_panels（SMC 主）— 先 4H/1H 定趋势偏见，再看 15m/5m 结构
2. price_action / price_action_summary（PA 辅）— 高周期确认方向，15m/5m/session 供日内锚点
3. support_resistance、indicators / fibonacci / market_position / ema_vwap_relation（参考）

输出要求：
- items 至少 4 条：至少 2 条 category="lux_panel" 或 structure（SMC，source="lux_smc_panel"；须含 4H 或 1H）
- 至少 2 条 category="price_action"（PA，source="dgt_price_action"；至少一条 timeframe=15m 或 5m）
- **level_reactions 至少 2 条**：至少 1 条 15m/5m **顺势**日内锚点；
  至少 1 条 **潜在反转/失效** 锚点（如关键 VA 外侧、结构失守后预期反向反应），rationale 写清触发条件；
  可另附 4H/1H 趋势位。不要写完整下单计划（留给点位阶段）。
- 每条 reaction 必须从 technical_claim_facts 逐字复制 fact_ids；区间事实必须同时引用 low/high。
  多个事实声称“共振/接近/矛盾”时必须填写 relationships，rationale 不得增加结构化字段中不存在的事实关系。
- summary 一句写清：主偏见 + 反转观察条件（无则写「暂无明确反转触发」）
- spot/kline 与 TV 价偏差大时在 summary 标注

返回 JSON：
{TECHNICAL_JSON_SCHEMA}"""


def run_llm_technical_analyst(ctx: MarketContext) -> tuple[AnalystReport | None, LLMStageTrace]:
    return run_specialist_llm(
        ctx,
        stage="technical",
        agent="technical_analyst",
        system=SYSTEM,
        payload_fn=technical_analyst_payload,
        user_prefix=(
            f"{INTRADAY_GOLD_MANDATE} "
            "请输出技术分析报告：4H/1H 定方向，15m/5m 给日内反应锚点。"
            "务必填写 level_reactions（至少含一条 15m 或 5m）："
        ),
    )
