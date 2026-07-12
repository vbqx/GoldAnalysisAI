"""Tests for take-profit ordering."""

from __future__ import annotations

from src.analysis.signal_geometry import normalize_take_profits


def test_short_targets_sorted_nearest_first() -> None:
    ordered = normalize_take_profits(
        direction="SELL",
        theme="short",
        entry_low=4130.0,
        entry_high=4132.0,
        take_profits=[4118.84, 4124.03, 4103.47],
    )
    assert ordered == [4124.03, 4118.84, 4103.47]


def test_long_targets_sorted_nearest_first() -> None:
    ordered = normalize_take_profits(
        direction="BUY",
        theme="long",
        entry_low=4130.0,
        entry_high=4132.0,
        take_profits=[4150.0, 4140.5, 4160.0],
    )
    assert ordered == [4140.5, 4150.0, 4160.0]
