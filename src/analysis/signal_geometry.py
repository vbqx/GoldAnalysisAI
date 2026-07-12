"""Direction-aware signal geometry helpers."""

from __future__ import annotations


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
        return sorted(valid, reverse=True)
    valid = [tp for tp in cleaned if tp > entry_mid]
    return sorted(valid)
