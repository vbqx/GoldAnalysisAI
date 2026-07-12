"""PA plan target ladder ordering."""

from __future__ import annotations

from src.analysis.plan_signals import _buy_targets, _sell_targets
from src.analysis.report_invariants import validate_report_invariants


def test_sell_targets_descend_when_poc_between_geom_and_val() -> None:
    """POC can sit above the geometry TP but still below entry — ladder must sort."""
    tps = _sell_targets(
        4124.34,
        4126.74,
        poc=4124.03,
        val=4103.47,
        swing_low=4090.0,
    )
    assert tps is not None
    assert tps == (4124.03, 4113.16, 4103.47)


def test_buy_targets_ascend_nearest_first() -> None:
    tps = _buy_targets(
        4098.47,
        4103.47,
        price=4120.67,
        poc=4124.03,
        vah=4131.53,
        swing_high=4150.0,
        swing_low=4090.0,
    )
    assert tps[0] < tps[1] < tps[2]


def test_normalized_sell_signals_pass_invariant_gate() -> None:
    report = {
        "metrics": {"current_price": 4120.67},
        "signals": [
            {
                "name": "激进反抽做空",
                "direction": "SELL",
                "theme": "short",
                "entry_low": 4124.34,
                "entry_high": 4126.74,
                "stop_loss": 4129.14,
                "take_profits": list(
                    _sell_targets(
                        4124.34,
                        4126.74,
                        poc=4124.03,
                        val=4103.47,
                        swing_low=4090.0,
                    )
                    or []
                ),
            }
        ],
        "llm_analysis": {"enabled": False},
        "meta": {
            "execution_authorized": False,
            "observation_mode": True,
            "manager_decision": {"action": "wait"},
            "data_as_of": {"executable": False},
        },
    }
    inv = validate_report_invariants(report)
    geo_codes = {v["code"] for v in inv["violations"] if v["code"].startswith("INV-GEO")}
    assert geo_codes == set()
