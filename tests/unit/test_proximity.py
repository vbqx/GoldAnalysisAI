"""Proximity filter tests for execution vs context structure."""

from __future__ import annotations

from src.analysis.proximity import level_near_price, zone_near_price


def test_zone_near_price_inside_band() -> None:
    assert zone_near_price(4155.0, 4150.0, 4160.0, 10.0)


def test_zone_far_by_atr() -> None:
    assert not zone_near_price(4155.0, 4020.0, 4025.0, 12.0, atr_mult=1.0)


def test_level_near_price_pct_fallback() -> None:
    assert level_near_price(4155.0, 4140.0, None, atr_mult=1.0)
