"""Tests for PA-primary trading plans with SMC filter."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import (
    FairValueGap,
    OrderBlock,
    StructureEvent,
    TimeframeAnalysis,
)
from src.analysis.plan_signals import smc_filter_adjustment
from src.analysis.report_engine import generate_trading_signals


def _pa_block() -> dict:
    return {
        "5m": {
            "volume_ok": True,
            "sr_levels": [
                {
                    "price": 4220.0,
                    "direction": "resistance",
                    "kind": "consecutive_sr",
                    "label": "量价连续阻力",
                    "time": "2026-06-01T00:00:00",
                },
                {
                    "price": 4200.0,
                    "direction": "support",
                    "kind": "consecutive_sr",
                    "label": "量价连续支撑",
                    "time": "2026-06-01T00:00:00",
                },
            ],
            "volume_profile": {
                "poc": 4210.0,
                "vah": 4225.0,
                "val": 4198.0,
            },
        }
    }


def _bearish_analyses() -> tuple[TimeframeAnalysis, TimeframeAnalysis]:
    ts = pd.Timestamp("2026-06-01")
    fvg = FairValueGap(high=4218.0, low=4215.0, direction="bearish", time=ts)
    ob = OrderBlock(high=4219.0, low=4216.0, direction="bearish", time=ts)
    a5 = TimeframeAnalysis(
        timeframe="5m",
        trend="bearish",
        bos="bearish @ 4212",
        choch="—",
        fvgs=[fvg],
        order_blocks=[ob],
        swing_high=4300.0,
        swing_low=4180.0,
        events=[
            StructureEvent(kind="BOS", direction="bearish", price=4212.0, time=ts),
        ],
    )
    a15 = TimeframeAnalysis("15m", "bearish", "—", "—", swing_high=4300.0, swing_low=4180.0)
    return a5, a15


def test_pa_primary_short_uses_resistance_not_fvg() -> None:
    a5, a15 = _bearish_analyses()
    sentiment = {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0}
    signals = generate_trading_signals(
        4215.0,
        a5,
        a15,
        4300.0,
        4180.0,
        sentiment,
        price_action=_pa_block(),
    )
    sell = next(s for s in signals if s.direction == "SELL" and s.setup_type == "pa_resistance_short")
    assert 4218.0 <= sell.entry_high <= 4222.0
    assert sell.stop_loss > sell.entry_high
    assert "PA 主" in sell.note


def test_smc_filter_penalizes_counter_structure() -> None:
    a5, a15 = _bearish_analyses()
    aligned = smc_filter_adjustment(
        direction="SELL",
        entry_low=4218.0,
        entry_high=4221.0,
        analysis_5m=a5,
        analysis_15m=a15,
    )
    assert aligned.bonus > 0

    ts = pd.Timestamp("2026-06-01")
    bull_a5 = TimeframeAnalysis(
        "5m",
        "bullish",
        "-",
        "bullish @ 4220",
        events=[StructureEvent(kind="CHoCH", direction="bullish", price=4220.0, time=ts)],
    )
    counter = smc_filter_adjustment(
        direction="SELL",
        entry_low=4218.0,
        entry_high=4221.0,
        analysis_5m=bull_a5,
        analysis_15m=a15,
    )
    assert counter.bonus < aligned.bonus


def test_no_price_action_falls_back_to_rule_pa() -> None:
    ts = pd.Timestamp("2026-06-01")
    fvg = FairValueGap(high=4220.0, low=4210.0, direction="bearish", time=ts)
    a5 = TimeframeAnalysis(
        timeframe="5m",
        trend="bearish",
        bos="—",
        choch="—",
        fvgs=[fvg],
        active_fvgs=[fvg],
        swing_high=4300.0,
        swing_low=4200.0,
    )
    a15 = TimeframeAnalysis("15m", "bearish", "—", "—", swing_high=4300.0, swing_low=4200.0)
    signals = generate_trading_signals(
        4215.0,
        a5,
        a15,
        4300.0,
        4200.0,
        {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0},
        price_action=None,
        metrics={"daily_high": 4225.0, "daily_low": 4190.0},
    )
    assert any(s.setup_type.startswith("rule_pa_") for s in signals)
    assert any("规则 PA" in s.note for s in signals)


def test_pa_long_uses_val_zone() -> None:
    a5, a15 = _bearish_analyses()
    signals = generate_trading_signals(
        4215.0,
        a5,
        a15,
        4300.0,
        4180.0,
        {"bearish": 40.0, "bullish": 45.0, "ranging": 15.0},
        price_action=_pa_block(),
    )
    long_sig = next(s for s in signals if s.direction == "BUY")
    assert long_sig.setup_type == "pa_val_sweep_long"
    assert long_sig.entry_high == 4198.0
