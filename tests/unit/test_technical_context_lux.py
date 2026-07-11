"""Lux structure fields in LLM timeframe_context."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import (
    FairValueGap,
    OrderBlock,
    StructureEvent,
    TimeframeAnalysis,
)
from src.analysis.tf_snapshot import SNAPSHOT_LIMIT
from src.analysis.technical_context import build_technical_context, timeframe_context
from src.core.types import MarketContext
from src.core.types import ExternalFactors


def test_timeframe_context_includes_lux_lists_for_llm() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=20, freq="1h")
    events = [
        StructureEvent("BOS", "bullish", 4100.0 + i, idx[i], scope="internal")
        for i in range(6)
    ]
    analysis = TimeframeAnalysis(
        "1h",
        "bullish",
        "无",
        "无",
        order_blocks=[OrderBlock(4100 + i, 4090 + i, "bullish", idx[i]) for i in range(3)],
        active_fvgs=[FairValueGap(4110, 4105, "bullish", idx[10])],
        events=events,
        swing_high=4200.0,
        swing_low=4000.0,
    )

    ctx = timeframe_context("1h", analysis, price=4150.0)

    assert len(ctx["bos_list"]) == SNAPSHOT_LIMIT
    assert ctx["bos_list"][0]["scope"] == "internal"
    assert ctx["strong_high"] == 4200.0
    assert ctx["weak_low"] == 4000.0
    assert len(ctx["order_blocks"]) == 3


def test_build_technical_context_exposes_ui_aligned_lux_panels() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=20, freq="1h")
    df = pd.DataFrame(
        {
            "Open": [4100.0] * len(idx),
            "High": [4120.0] * len(idx),
            "Low": [4080.0] * len(idx),
            "Close": [4110.0] * len(idx),
            "Volume": [100.0] * len(idx),
        },
        index=idx,
    )
    analyses = {
        tf: TimeframeAnalysis(
            tf,
            "bullish",
            "无",
            "无",
            events=[StructureEvent("BOS", "bullish", 4110.0, idx[-1], scope="internal")],
            order_blocks=[OrderBlock(4100.0, 4090.0, "bullish", idx[-1])],
            active_fvgs=[FairValueGap(4110.0, 4105.0, "bullish", idx[-1])],
            swing_high=4200.0,
            swing_low=4000.0,
        )
        for tf in ("4h", "1h", "15m")
    }
    ctx = MarketContext(
        enriched={tf: df.copy() for tf in ("4h", "1h", "15m", "5m")},
        analyses=analyses,
        metrics={"current_price": 4110.0},
        price=4110.0,
        external=ExternalFactors(),
        source_label="test",
    )

    payload = build_technical_context(ctx)

    assert set(payload["lux_timeframe_panels"]) == {"4h", "1h", "15m"}
    panel = payload["lux_timeframe_panels"]["1h"]
    assert panel["bos_list"][0]["kind"] == "BOS"
    assert panel["order_blocks"][0]["direction"] == "bullish"
    assert panel["fvgs"][0]["low"] == 4105.0
