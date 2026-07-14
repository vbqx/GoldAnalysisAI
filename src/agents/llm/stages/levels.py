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

输入优先用：technical_level_reactions（技术分析师反应假设）、debate 共识、structure_context、rule_signals。
不得编造宏观事件；不得重写技术分析长推演。

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
      "reaction_evidence_id": "必须引用 technical_level_reactions[].id",
      "anchor_level": "从对应反应复制/改写：周期+标签+价位",
      "expected_reaction": "从对应反应复制：承压/反弹/假突破回收等",
      "deduction": "一句绑定：为何在该反应确认后挂此入场区（勿长文）",
      "reason": "一句话汇总",
      "invalidation": "失效条件",
      "confidence": 0.0
    }}
  ],
  "bias": "bullish|bearish|neutral",
  "summary": "一句总览"
}}

硬性约束：
- 恰好 3 个 setup，path_id=A/B/C。
- A 顺 debate；B 备选；C 对冲/失效备用。
- 每条优先填 reaction_evidence_id；入场区贴近被引用反应的价位。
- SELL：SL 在入场上方、TP1 在下方；入场在现价上方或含现价。
- BUY：SL 在入场下方、TP1 在上方；入场在现价下方或含现价。
- technical_level_reactions 为空时，仅可据 structure_context 的 POC/VA/S/R 定区，并仍写清 anchor/reaction/短 deduction。
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
        "llm level proposer start model=%s price=%.2f debate=%s rule_signals=%d reactions=%d",
        client.model,
        ctx.price,
        debate.consensus_bias,
        len(rule_signals),
        len(payload.get("technical_level_reactions") or []),
    )
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                "请提案 A/B/C 入场区：绑定 technical_level_reactions 的锚点与预期反应，"
                "只写一句下单绑定理由，不要重写技术分析。\n"
                f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
            ),
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
