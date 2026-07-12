"""Direction-aware signal geometry helpers."""

from __future__ import annotations

from typing import Any


def _dedupe_preserve_order(levels: list[float]) -> list[float]:
    out: list[float] = []
    for level in levels:
        if level not in out:
            out.append(level)
    return out


def normalize_take_profits(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    take_profits: list[float],
    theme: str = "",
) -> list[float]:
    """Sort take-profit levels from nearest to farthest in trade direction."""
    if not take_profits:
        return []
    entry_mid = (float(entry_low) + float(entry_high)) / 2.0
    raw = f"{direction} {theme}".lower()
    is_short = raw.strip() in ("sell", "short") or "short" in raw or "sell" in raw
    cleaned: list[float] = []
    for raw in take_profits:
        try:
            cleaned.append(round(float(raw), 2))
        except (TypeError, ValueError):
            continue
    if is_short:
        valid = [tp for tp in cleaned if tp < entry_mid]
        return _dedupe_preserve_order(sorted(valid, reverse=True))
    valid = [tp for tp in cleaned if tp > entry_mid]
    return _dedupe_preserve_order(sorted(valid))


def normalize_signal_take_profits(signal: dict[str, Any]) -> list[float]:
    """Return direction-aware TP ladder for a report/signal dict."""
    tps = signal.get("take_profits") or []
    if not tps:
        return []
    return normalize_take_profits(
        direction=str(signal.get("direction") or ""),
        theme=str(signal.get("theme") or ""),
        entry_low=float(signal.get("entry_low") or 0),
        entry_high=float(signal.get("entry_high") or 0),
        take_profits=[float(x) for x in tps if x is not None],
    )
