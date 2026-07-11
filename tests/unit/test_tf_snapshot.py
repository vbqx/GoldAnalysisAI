"""tf_snapshot unit tests."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import (
    FairValueGap,
    OrderBlock,
    StructureEvent,
    TimeframeAnalysis,
)
from src.analysis.tf_snapshot import SNAPSHOT_LIMIT, build_tf_snapshot


def test_build_tf_snapshot_lists_latest_five() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=20, freq="1h")
    events = []
    for i in range(6):
        events.append(
            StructureEvent(
                "BOS",
                "bullish",
                4100.0 + i,
                idx[i],
                scope="internal",
            )
        )
    analysis = TimeframeAnalysis(
        "1h",
        "bullish",
        "无",
        "无",
        order_blocks=[
            OrderBlock(4100 + i, 4090 + i, "bullish", idx[i]) for i in range(6)
        ],
        active_fvgs=[
            FairValueGap(4110 + i, 4105 + i, "bullish", idx[i]) for i in range(6)
        ],
        events=events,
        swing_high=4200.0,
        swing_low=4000.0,
    )

    panel = build_tf_snapshot(analysis)

    assert len(panel["bos_list"]) == SNAPSHOT_LIMIT
    assert panel["bos_list"][0]["price"] == 4105.0
    assert len(panel["order_blocks"]) == SNAPSHOT_LIMIT
    assert len(panel["fvgs"]) == SNAPSHOT_LIMIT
    assert panel["swing_high"] == 4200.0
    assert panel["strong_high"] == 4200.0
    assert panel["weak_low"] == 4000.0
