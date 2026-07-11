"""report_facts unit tests."""

from __future__ import annotations

import pandas as pd

from src.analysis.ict_pa import StructureEvent, TimeframeAnalysis, _swing_liquidity
from src.analysis.report_facts import build_liquidity_entries, build_tf_summaries


def test_build_liquidity_entries_use_swing_hl() -> None:
    analyses = {
        "1h": TimeframeAnalysis(
            "1h",
            "bullish",
            "无",
            "无",
            swing_high=4200.0,
            swing_low=4000.0,
            events=[StructureEvent("BOS", "bullish", 4100.0, pd.Timestamp("2026-06-20"), scope="internal")],
        )
    }
    analyses["1h"].liquidity = _swing_liquidity(4200.0, 4000.0)

    entries = build_liquidity_entries(analyses, price=4150.0, swing_tf="1h", swing_atr=20.0)
    kinds = {e["kind"] for e in entries}
    assert "swing_high" in kinds
    assert "swing_low" in kinds


def test_build_tf_summaries_include_ema_relation() -> None:
    idx = pd.date_range("2026-06-20 08:00", periods=10, freq="1h")
    df = pd.DataFrame(
        {
            "Open": [4100.0] * 10,
            "High": [4110.0] * 10,
            "Low": [4090.0] * 10,
            "Close": [4105.0] * 10,
            "Volume": [100] * 10,
        },
        index=idx,
    )
    analysis = TimeframeAnalysis("1h", "bullish", "无", "无", swing_high=4200.0, swing_low=4000.0)
    summaries = build_tf_summaries({"1h": df}, {"1h": analysis}, price=4105.0)
    assert "ema_relation" in summaries["1h"]
    assert summaries["1h"]["trend"] == "bullish"
