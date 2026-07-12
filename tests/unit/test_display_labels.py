"""Display label helpers for Chinese UI."""

from __future__ import annotations

from src.viz.display_labels import (
    execution_banner,
    infer_trade_theme,
    label_action,
    label_bias,
    label_risk_profile,
    label_trade_direction,
)


def test_label_bias_cn() -> None:
    assert label_bias("bearish") == "偏空"
    assert label_action("wait") == "观望"
    assert label_trade_direction("short") == "做空"


def test_infer_trade_theme_from_direction_and_cn() -> None:
    assert infer_trade_theme(direction="SELL") == "short"
    assert infer_trade_theme(direction_cn="做多") == "long"
    assert infer_trade_theme(theme="short") == "short"


def test_execution_banner_observation_mode() -> None:
    msg = execution_banner({"execution_authorized": False, "observation_mode": True})
    assert "观察模式" in msg
    assert "未经经理授权" in msg


def test_label_risk_profile_cn() -> None:
    assert label_risk_profile("conservative") == "保守"
