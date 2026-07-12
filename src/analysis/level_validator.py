"""Validate LLM proposed levels before they enter trading plans."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from src.analysis.ict_pa import sentiment_score
from src.analysis.report_engine import (
    TradingSignal,
    _compute_risk_reward,
    _setup_status_and_score,
    _stop_breached,
)
from src.core.types import LevelProposal, MarketContext
from src.log import get_logger

log = get_logger(__name__)


def _location_error(ctx: MarketContext, proposal: LevelProposal) -> str | None:
    price = float(ctx.price)
    if proposal.direction == "SELL" and proposal.entry_high < price:
        return (
            f"SELL entry zone {proposal.entry_low:.2f}-{proposal.entry_high:.2f} "
            f"is below current price {price:.2f}"
        )
    if proposal.direction == "BUY" and proposal.entry_low > price:
        return (
            f"BUY entry zone {proposal.entry_low:.2f}-{proposal.entry_high:.2f} "
            f"is above current price {price:.2f}"
        )
    return None


def _llm_signal_name(proposal: LevelProposal) -> str:
    direction_cn = "做空" if proposal.direction == "SELL" else "做多"
    path = str(proposal.path_id or "").upper()
    if path in ("A", "B", "C"):
        return f"LLM路径{path}·{direction_cn}"
    return f"LLM建议{direction_cn}"


def _tp_ladder_error(proposal: LevelProposal) -> str | None:
    tps = proposal.take_profits
    if len(tps) < 2:
        return None
    entry_mid = (proposal.entry_low + proposal.entry_high) / 2
    if proposal.direction == "SELL":
        if any(tp >= entry_mid for tp in tps):
            return "SELL take_profits must stay below entry_mid"
        for left, right in zip(tps, tps[1:]):
            if left <= right:
                return "SELL take_profits must descend nearest-to-farthest"
    else:
        if any(tp <= entry_mid for tp in tps):
            return "BUY take_profits must stay above entry_mid"
        for left, right in zip(tps, tps[1:]):
            if left >= right:
                return "BUY take_profits must ascend nearest-to-farthest"
    return None


def _geometry_error(proposal: LevelProposal) -> str | None:
    entry_mid = (proposal.entry_low + proposal.entry_high) / 2
    tp1 = proposal.take_profits[0] if proposal.take_profits else None
    if tp1 is None:
        return "missing TP1"
    ladder_error = _tp_ladder_error(proposal)
    if ladder_error:
        return ladder_error
    if proposal.direction == "SELL":
        if proposal.stop_loss <= proposal.entry_high:
            return "SELL stop_loss must be above entry_high"
        if tp1 >= entry_mid:
            return "SELL TP1 must be below entry_mid"
    else:
        if proposal.stop_loss >= proposal.entry_low:
            return "BUY stop_loss must be below entry_low"
        if tp1 <= entry_mid:
            return "BUY TP1 must be above entry_mid"
    return None


def _position_size(confidence: float, grade: str) -> str:
    if confidence >= 0.72 and grade in ("A", "B"):
        return "LLM建议 · 标准仓位"
    if confidence >= 0.55:
        return "LLM建议 · 半仓观察"
    return "LLM建议 · 轻仓观察"


def validate_llm_levels(
    ctx: MarketContext,
    proposals: list[LevelProposal],
) -> tuple[list[TradingSignal], list[dict[str, Any]]]:
    """Convert valid LLM level proposals into existing TradingSignal objects."""
    log.info("validating llm level proposals count=%d price=%.2f", len(proposals), ctx.price)
    sentiment = sentiment_score(ctx.analyses)
    accepted: list[TradingSignal] = []
    audit: list[dict[str, Any]] = []

    for idx, proposal in enumerate(proposals):
        base = proposal.to_dict()
        error = _geometry_error(proposal)
        if error is None and _stop_breached(
            price=ctx.price,
            direction=proposal.direction,
            stop_loss=proposal.stop_loss,
        ):
            error = f"current price {ctx.price:.2f} has already breached stop_loss {proposal.stop_loss:.2f}"
        if error is None:
            error = _location_error(ctx, proposal)
        if error:
            log.info(
                "llm level rejected idx=%d direction=%s entry=%.2f-%.2f sl=%.2f reason=%s",
                idx,
                proposal.direction,
                proposal.entry_low,
                proposal.entry_high,
                proposal.stop_loss,
                error,
            )
            audit.append({"index": idx, "accepted": False, "reason": error, "proposal": base})
            continue

        direction = proposal.direction
        theme = "short" if direction == "SELL" else "long"
        direction_cn = "做空" if direction == "SELL" else "做多"
        setup_type = proposal.setup_type
        if not setup_type.startswith("llm_"):
            setup_type = f"llm_{setup_type}"
        note = proposal.reason
        if proposal.invalidation:
            note = f"{note} 失效条件：{proposal.invalidation}"

        signal_name = _llm_signal_name(proposal)
        status, trigger_confirmed, trigger_note, score, grade, reasons = _setup_status_and_score(
            name=signal_name,
            direction=direction,
            theme=theme,
            setup_type=setup_type,
            price=ctx.price,
            entry_low=proposal.entry_low,
            entry_high=proposal.entry_high,
            stop_loss=proposal.stop_loss,
            take_profits=proposal.take_profits,
            sentiment=sentiment,
            trigger_confirmed=False,
        )
        reasons.append(f"LLM confidence {proposal.confidence:.0%}")

        signal = TradingSignal(
            name=signal_name,
            direction=direction,
            direction_cn=direction_cn,
            entry_low=proposal.entry_low,
            entry_high=proposal.entry_high,
            stop_loss=proposal.stop_loss,
            take_profits=proposal.take_profits,
            risk_reward=_compute_risk_reward(
                direction=direction,
                entry_low=proposal.entry_low,
                entry_high=proposal.entry_high,
                stop_loss=proposal.stop_loss,
                take_profits=proposal.take_profits,
            ),
            sentiment_bias_pct=(
                f"{sentiment.get('bearish' if theme == 'short' else 'bullish', 0):.0f}%"
            ),
            position_size=_position_size(proposal.confidence, grade),
            note=note,
            theme=theme,
            setup_type=setup_type,
            status=status,
            trigger_confirmed=trigger_confirmed,
            trigger_note=trigger_note,
            score_total=score,
            score_grade=grade,
            score_reasons=reasons,
        )
        accepted.append(signal)
        log.info(
            "llm level accepted idx=%d direction=%s entry=%.2f-%.2f sl=%.2f grade=%s score=%.1f",
            idx,
            direction,
            proposal.entry_low,
            proposal.entry_high,
            proposal.stop_loss,
            grade,
            score,
        )
        audit.append({
            "index": idx,
            "accepted": True,
            "reason": "geometry and scoring passed",
            "signal": asdict(signal),
            "proposal": base,
        })

    log.info("llm level validation complete accepted=%d rejected=%d", len(accepted), len(audit) - len(accepted))
    return accepted, audit
