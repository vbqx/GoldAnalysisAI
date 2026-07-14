"""LLM Technical Analyst."""

from __future__ import annotations

from src.agents.llm.payload import technical_analyst_payload
from src.agents.llm.stages.analysts._common import run_specialist_llm
from src.core.types import AnalystReport, LLMStageTrace, MarketContext
from src.analysis.field_glossary import ANALYST_PRIORITY_HINT, PA_SMC_PRIORITY

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
      "rationale": "一两句：为何预期该反应（引用 payload 中的 PA/SMC 事实）",
      "strength": 0.0
    }
  ],
  "confidence": 0.0-1.0,
  "summary": "一句话结论"
}
items 至少 4 条；level_reactions 至少 2 条（供下游点位提案绑定，勿只写空方向）。"""

SYSTEM = f"""你是 XAUUSD 技术分析师。{ANALYST_PRIORITY_HINT}

{PA_SMC_PRIORITY}

输入优先级：
1. timeframes + lux_timeframe_panels（SMC 主）— 趋势、BOS/CHoCH、OB/FVG、溢价折价
2. price_action / price_action_summary（PA 辅）— POC/VA、量价 S/R、共振确认
3. support_resistance、indicators / fibonacci / market_position / ema_vwap_relation（参考）

输出要求：
- items 至少 4 条：至少 2 条 category="lux_panel" 或 structure（SMC，source="lux_smc_panel"）
- 至少 2 条 category="price_action"（PA，source="dgt_price_action"，优先 5m/15m POC/VA 或近端 S/R）
- **level_reactions 至少 2 条（本阶段主责）**：标出关键 POC/VAH/VAL/量价支撑阻力（含周期与价格），
  并写清价格到达后的预期反应与简短 rationale。这是点位提案的唯一反应假设来源；不要写完整下单计划（入场/止损/止盈留给点位阶段）。
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
            "请输出技术分析报告（SMC 定结构，PA 确认价位）。"
            "务必填写 level_reactions：关键位 + 到价预期反应（供点位提案绑定）："
        ),
    )
