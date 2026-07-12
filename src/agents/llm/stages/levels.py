"""LLM level proposer stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import level_proposer_payload
from src.agents.llm.schemas import parse_level_proposals
from src.analysis.field_glossary import LEVELS_PRIORITY_HINT, PA_SMC_PRIORITY
from src.core.types import AnalystTeam, LLMStageTrace, LevelProposal, MarketContext, ResearchDebate
from src.llm.router import get_strong_client
from src.log import get_logger

log = get_logger(__name__)

SYSTEM = f"""你是 XAUUSD 机构级价位提案员。
{LEVELS_PRIORITY_HINT}
{PA_SMC_PRIORITY}

仅使用输入中的 structure_context、analyst_team、debate 共识与 rule_signals 候选；不得编造宏观事件或未给出的订单流。
返回 JSON：
{{
  "setups": [
    {{
      "path_id": "A|B|C",
      "direction": "BUY|SELL",
      "entry_low": 0.0,
      "entry_high": 0.0,
      "stop_loss": 0.0,
      "take_profits": [0.0, 0.0, 0.0],
      "setup_type": "llm_poc_va|llm_volume_sr|llm_fvg|llm_order_block|llm_liquidity_sweep|llm_breakout_retest|llm_pullback",
      "reason": "为何该区间有 PA/SMC 事实支撑",
      "invalidation": "失效条件",
      "confidence": 0.0
    }}
  ],
  "bias": "bullish|bearish|neutral",
  "summary": "简要理由"
}}

硬性约束：
- 必须返回恰好 3 个 setup，path_id 分别为 A、B、C（不可重复）。
- A：与 debate 共识一致的主策略路径（顺势、优先执行级）。
- B：备选/条件触发路径（可同向不同入场区，或等待结构确认后再执行）。
- C：逆势/对冲/失败备用路径（与 A 相反方向，或主路径失效后的 Plan B）。
- SELL：stop_loss 高于入场区；首个 take_profit 低于入场区；入场区应在现价上方或包含现价（等待反抽），不得整段落在现价下方。
- BUY：stop_loss 低于入场区；首个 take_profit 高于入场区；入场区应在现价下方或包含现价（等待回踩），不得整段落在现价上方。
- 三个路径的 entry/stop/target 必须互不重复；价位不清晰时返回空 setups 数组。
"""


def run_llm_level_proposer(
    ctx: MarketContext,
    team: AnalystTeam,
    debate: ResearchDebate,
    rule_signals: list[object],
) -> tuple[list[LevelProposal] | None, LLMStageTrace]:
    client = get_strong_client()
    payload = level_proposer_payload(ctx, team, debate, rule_signals)
    log.info(
        "llm level proposer start model=%s price=%.2f debate=%s rule_signals=%d",
        client.model,
        ctx.price,
        debate.consensus_bias,
        len(rule_signals),
    )
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"请基于下列证据提案交易区间（PA 定区，SMC 仅确认）：\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
        },
    ]
    result, trace = run_llm_stage(
        stage="llm_levels",
        model=client.model,
        client=client,
        messages=messages,
        parse=parse_level_proposals,
        temperature=0.15,
    )
    if result:
        trace.confidence = max(p.confidence for p in result)
        log.info("llm level proposer returned proposals=%d max_confidence=%.2f", len(result), trace.confidence)
    elif trace.error:
        log.warning("llm level proposer failed error=%s", trace.error)
    else:
        log.info("llm level proposer returned no proposals")
    return result, trace
