"""Deterministic risk gates before position scale is applied."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from src.analysis.signal_geometry import normalize_take_profits
from src.config import RISK_REWARD_DISPLAY_CAP
from src.log import get_logger

log = get_logger(__name__)

MIN_RISK_REWARD = 1.0
MAX_ENTRY_DISTANCE_PCT = 1.5


def _signal_dict(sig: Any) -> dict[str, Any]:
    if isinstance(sig, dict):
        return sig
    if is_dataclass(sig):
        return asdict(sig)
    return {}


def _entry_mid(sig: dict[str, Any]) -> float:
    return (float(sig.get("entry_low") or 0) + float(sig.get("entry_high") or 0)) / 2.0


def _risk_reward(sig: dict[str, Any]) -> float:
    theme = str(sig.get("theme") or sig.get("direction") or "").lower()
    is_short = "short" in theme or str(sig.get("direction", "")).upper() == "SELL"
    entry = _entry_mid(sig)
    sl = float(sig.get("stop_loss") or 0)
    tps = sig.get("take_profits") or []
    if not tps or entry <= 0 or sl <= 0:
        return 0.0
    tp = float(tps[0])
    if is_short:
        risk = sl - entry
        reward = entry - tp
    else:
        risk = entry - sl
        reward = tp - entry
    if risk <= 0 or reward <= 0:
        return 0.0
    return min(reward / risk, RISK_REWARD_DISPLAY_CAP)


def validate_signal_geometry(sig: Any, *, current_price: float) -> list[str]:
    """Return blocking issues for one signal (empty = pass)."""
    row = _signal_dict(sig)
    if row.get("status") == "invalid":
        return ["signal invalid"]
    theme = str(row.get("theme") or "").lower()
    direction = str(row.get("direction") or "").upper()
    is_short = theme == "short" or direction == "SELL"
    is_long = theme == "long" or direction == "BUY"
    if not is_short and not is_long:
        return ["unknown direction"]

    entry = _entry_mid(row)
    sl = float(row.get("stop_loss") or 0)
    if entry <= 0 or sl <= 0:
        return ["missing entry or stop"]

    if is_short:
        if sl <= entry:
            return ["short stop must be above entry zone"]
    elif sl >= entry:
        return ["long stop must be below entry zone"]

    tps_raw = [float(x) for x in (row.get("take_profits") or []) if x is not None]
    ordered = normalize_take_profits(
        direction=direction,
        theme=theme,
        entry_low=float(row.get("entry_low") or entry),
        entry_high=float(row.get("entry_high") or entry),
        take_profits=tps_raw,
    )
    if tps_raw and ordered != tps_raw:
        return ["take-profit levels out of order"]

    rr = _risk_reward(row)
    if rr < MIN_RISK_REWARD:
        return [f"risk/reward {rr:.2f} < {MIN_RISK_REWARD:.1f}"]

    if current_price > 0:
        dist_pct = abs(entry - current_price) / current_price * 100
        if dist_pct > MAX_ENTRY_DISTANCE_PCT and row.get("status") == "active":
            return [f"entry {dist_pct:.1f}% away from price (> {MAX_ENTRY_DISTANCE_PCT:.1f}%)"]

    return []


def apply_risk_gates(
    reviews: list,
    proposal,
    signals: list[Any],
    *,
    current_price: float,
    data_as_of: dict[str, Any] | None = None,
    observation_mode: bool = False,
) -> list:
    """Filter risk reviews through deterministic gates; may veto approval/scale."""
    as_of = data_as_of or {}
    global_block: list[str] = []
    if observation_mode or not as_of.get("executable", True):
        global_block.append("market snapshot not executable (stale or closed)")
    if as_of.get("data_age_hours") is not None and float(as_of["data_age_hours"]) > 36:
        global_block.append("price data too stale for sizing")

    gated = []
    for review in reviews:
        notes = list(review.notes)
        allowed = list(review.allowed_signal_indices)
        approved = review.approved
        scale = float(review.position_scale)

        if global_block:
            notes.extend(global_block)
            approved = False
            scale = 0.0
            allowed = []
            log.warning(
                "risk gate [%s] blocked: %s",
                review.profile,
                "; ".join(global_block),
            )
        else:
            kept: list[int] = []
            seen: set[int] = set()
            for idx in allowed:
                if not isinstance(idx, int) or idx < 0 or idx >= len(signals):
                    notes.append(f"signal index {idx} invalid")
                    continue
                if idx in seen:
                    notes.append(f"duplicate signal index {idx}")
                    continue
                seen.add(idx)
                issues = validate_signal_geometry(signals[idx], current_price=current_price)
                if issues:
                    notes.append(f"signal {idx}: " + "; ".join(issues))
                    continue
                kept.append(idx)
            allowed = kept
            if not allowed:
                approved = False
                scale = 0.0
                notes.append("no signal passed geometry gates")
                log.warning("risk gate [%s] no signal passed geometry", review.profile)

        from src.core.types import RiskReview

        gated.append(
            RiskReview(
                profile=review.profile,
                approved=approved,
                allowed_signal_indices=allowed,
                position_scale=scale if approved else 0.0,
                notes=notes,
            )
        )
    return gated
