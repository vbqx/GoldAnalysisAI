"""LLM level proposer stage."""

from __future__ import annotations

import json

from src.agents.llm.base import run_llm_stage
from src.agents.llm.payload import level_proposer_payload
from src.agents.llm.schemas import parse_level_proposals
from src.core.types import AnalystTeam, LLMStageTrace, LevelProposal, MarketContext, ResearchDebate
from src.llm.router import get_strong_client
from src.log import get_logger

log = get_logger(__name__)

SYSTEM = """You are an XAUUSD institutional level proposer.
Use only the supplied market facts, analyst summaries, debate consensus, and rule candidate signals.
Do not invent unsupported macro events or hidden order flow.

Return JSON only:
{
  "setups": [
    {
      "direction": "BUY|SELL",
      "entry_low": 0.0,
      "entry_high": 0.0,
      "stop_loss": 0.0,
      "take_profits": [0.0, 0.0, 0.0],
      "setup_type": "llm_fvg|llm_order_block|llm_liquidity_sweep|llm_breakout_retest|llm_pullback",
      "reason": "why this zone is supported by the supplied facts",
      "invalidation": "specific condition that cancels this setup",
      "confidence": 0.0
    }
  ],
  "bias": "bullish|bearish|neutral",
  "summary": "brief rationale"
}

Hard constraints:
- SELL: stop_loss must be above the entry zone; first take profit must be below the entry zone.
- BUY: stop_loss must be below the entry zone; first take profit must be above the entry zone.
- Prefer 1 to 3 setups. If levels are unclear, return an empty setups array.
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
            "content": f"Propose validated candidate trade levels from this evidence:\n{json.dumps(payload, ensure_ascii=False, indent=2)}",
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
