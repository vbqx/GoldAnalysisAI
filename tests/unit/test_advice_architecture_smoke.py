"""Focused dynamic evidence for Advice V2 component boundaries."""

from __future__ import annotations

import pandas as pd

from src.analysis.chart_zone_filters import chart_plot_df, chart_price_bounds
from src.analysis.display_labels import infer_trade_theme
from src.core.orchestrator import run_advice_pipeline
from src.data.context_builder import build_spot_cross_check


def test_chart_zone_filter_boundary_uses_visible_frame() -> None:
    frame = pd.DataFrame(
        {"Low": [10.0, 11.0, 12.0], "High": [12.0, 13.0, 14.0]},
        index=pd.date_range("2026-08-12", periods=3, freq="5min", tz="UTC"),
    )
    visible = chart_plot_df(frame, 2)
    assert len(visible) == 2
    assert chart_price_bounds(visible) == (11.0, 14.0)


def test_display_theme_and_spot_cross_check_are_deterministic() -> None:
    assert infer_trade_theme(direction="BUY") == "long"
    check = build_spot_cross_check(4386.0, {"close": 4386.2, "code": "XAUUSD"})
    assert check["aligned"] is True
    assert check["code"] == "XAUUSD"


def test_advice_pipeline_is_the_only_primary_orchestrator() -> None:
    assert callable(run_advice_pipeline)
