"""LLM level proposer stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import level_proposer_payload
from src.agents.llm.schemas import parse_level_proposals
from src.analysis.field_glossary import INTRADAY_GOLD_MANDATE, LEVELS_PRIORITY_HINT, PA_SMC_PRIORITY
from src.core.types import AnalystTeam, LLMStageTrace, LevelProposal, MarketContext, ResearchDebate
from src.llm.router import client_for_stage
from src.log import get_logger

log = get_logger(__name__)

SYSTEM = f"""你是 XAUUSD 黄金日内价位提案员。
{LEVELS_PRIORITY_HINT}
{PA_SMC_PRIORITY}

输入优先用：technical_level_reactions（须优先绑 15m/5m 反应）、technical_claim_facts、debate 共识、structure_context、rule_signals。
不得编造宏观事件；不得重写技术分析长推演；入场几何不得落在纯 4H/1H 大区间。

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
- A 顺 debate 偏见主路径；B 同向备选（更优回踩/更紧止损）；
  C 潜在反转或主路径失效后的对冲预案——invalidation/deduction 必须写清触发条件
  （如收盘站回 VAL 外侧 + 15m CHoCH）；未触发时不得把 C 写成可立即执行的主单。
- 每条优先填 reaction_evidence_id；入场区贴近被引用反应的结构化 fact_ids（C 可绑反转/失效锚点）。
- 不得在 deduction/reason 中新增 reaction.fact_ids/relationships 未声明的“共振”事实；自由文本没有授权效力。
- SELL：SL 在入场上方、TP1 在下方；入场在现价上方或含现价。
- BUY：SL 在入场下方、TP1 在上方；入场在现价下方或含现价。
- technical_level_reactions 为空时，仅可据 structure_context 的 15m/5m/session POC/VA/S/R 定区，并仍写清 anchor/reaction/短 deduction。
"""


def run_llm_level_proposer(
    ctx: MarketContext,
    team: AnalystTeam,
    debate: ResearchDebate,
    rule_signals: list[object],
) -> tuple[list[LevelProposal] | None, LLMStageTrace]:
    client = client_for_stage("llm_levels")
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
                f"{INTRADAY_GOLD_MANDATE} "
                "请提案 A/B/C：A/B 顺偏见日内入场，C 写潜在反转/失效对冲（含触发条件）。"
                "优先绑定 15m/5m 的 technical_level_reactions；一句绑定理由，勿重写技术分析。\n"
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
