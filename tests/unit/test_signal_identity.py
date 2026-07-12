"""Stable signal identity tests."""

from __future__ import annotations

from src.analysis.signal_identity import stable_signal_id


def test_stable_signal_id_ignores_list_position() -> None:
    plan = {
        "direction": "SELL",
        "theme": "short",
        "entry_low": 4130.0,
        "entry_high": 4132.0,
        "stop_loss": 4145.0,
        "take_profits": [4110.0, 4090.0],
        "setup_type": "pa_resistance_short",
    }
    assert stable_signal_id(plan) == stable_signal_id(dict(plan))


def test_stable_signal_id_changes_when_geometry_changes() -> None:
    base = {
        "direction": "SELL",
        "theme": "short",
        "entry_low": 4130.0,
        "entry_high": 4132.0,
        "stop_loss": 4145.0,
        "take_profits": [4110.0],
        "setup_type": "pa_resistance_short",
    }
    other = dict(base)
    other["stop_loss"] = 4150.0
    assert stable_signal_id(base) != stable_signal_id(other)
