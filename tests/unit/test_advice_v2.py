"""Advice V2 contract, selection, and consistency tests."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import pytest

from src.advice.audit import audit_advice
from src.advice.engine import build_advice_packet
from src.advice.llm import _assert_no_new_prices, _parse
from src.advice.report import build_advice_report
from src.advice.types import AdvicePacket, AdviceSetup, AttentionZone
from src.analysis.ict_pa import FairValueGap, OrderBlock, TimeframeAnalysis
from src.core.types import ExternalFactors, MarketContext


def _bars(*, stale: bool = False) -> pd.DataFrame:
    end = pd.Timestamp("2025-01-01", tz="UTC") if stale else pd.Timestamp.now(tz="UTC").floor("5min")
    idx = pd.date_range(end=end, periods=180, freq="5min")
    close = pd.Series([99.5 + i / 360 for i in range(len(idx))], index=idx)
    return pd.DataFrame(
        {
            "Open": close - 0.1,
            "High": close + 0.4,
            "Low": close - 0.4,
            "Close": close,
            "Volume": 100.0,
            "ATR14": 1.0,
        },
        index=idx,
    )


def _context(*, conflict: bool = False, stale: bool = False) -> MarketContext:
    data = {tf: _bars(stale=stale) for tf in ("5m", "15m", "1h", "4h", "1d")}
    now = datetime.now(timezone.utc)
    trends = {
        "5m": "bullish",
        "15m": "bullish",
        "1h": "bearish" if conflict else "bullish",
        "4h": "bullish",
        "1d": "bullish",
    }
    analyses = {
        tf: TimeframeAnalysis(
            timeframe=tf,
            trend=trend,  # type: ignore[arg-type]
            bos="bullish @ 99.80",
            choch="无",
            atr=1.0,
            last_close=100.0,
            recent_high=100.4,
            recent_low=99.4,
            swing_high=104.0,
            swing_low=96.0,
        )
        for tf, trend in trends.items()
    }
    analyses["15m"].order_blocks = [OrderBlock(99.2, 99.0, "bullish", now)]
    analyses["5m"].active_fvgs = [FairValueGap(99.4, 99.2, "bullish", now)]
    analyses["5m"].order_blocks = [OrderBlock(103.2, 102.8, "bearish", now)]
    return MarketContext(
        enriched=data,
        analyses=analyses,
        metrics={
            "current_price": 100.0,
            "daily_high": 102.0,
            "daily_low": 97.0,
            "prev_close": 99.0,
            "daily_change": 1.0,
            "daily_change_pct": 1.0,
        },
        price=100.0,
        external=ExternalFactors(),
        source_label="test",
    )


def test_bullish_context_yields_one_human_review_setup() -> None:
    packet = build_advice_packet(_context())
    assert packet.decision == "WATCH_LONG"
    assert packet.primary_setup is not None
    assert packet.primary_setup.direction == "BUY"
    assert packet.primary_setup.attention_zone.high <= packet.current_price
    assert packet.primary_setup.invalidation_level < packet.primary_setup.attention_zone.low
    assert len(packet.primary_setup.confirmation_checklist) == 3
    assert packet.audit.passed


def test_conflicting_high_timeframes_return_wait_without_forced_plan() -> None:
    packet = build_advice_packet(_context(conflict=True))
    assert packet.decision == "WAIT"
    assert packet.bias == "mixed"
    assert packet.primary_setup is None


def test_stale_data_returns_avoid() -> None:
    packet = build_advice_packet(_context(stale=True))
    assert packet.decision == "AVOID"
    assert packet.primary_setup is None
    assert packet.confidence == "low"


def test_historical_evaluation_uses_archive_time_not_wall_clock() -> None:
    ctx = _context(stale=True)
    ctx.derived["evaluation_time"] = pd.Timestamp("2025-01-01 01:00", tz="UTC").to_pydatetime()
    packet = build_advice_packet(ctx)
    report = build_advice_report(ctx, packet, run_id="historic", run_config={"replay_mode": True})

    assert packet.decision != "AVOID"
    assert report["meta"]["data_as_of"]["executable"] is True


def test_audit_rejects_direction_geometry_conflict() -> None:
    packet = AdvicePacket(
        decision="WATCH_LONG",
        bias="bullish",
        confidence="medium",
        horizon="未来 2～6 小时",
        summary="测试",
        current_price=100.0,
        primary_setup=AdviceSetup(
            direction="BUY",
            attention_zone=AttentionZone(101.0, 102.0, "错误区域"),
            current_state="测试",
            rationale=["测试"],
            confirmation_checklist=["测试"],
            invalidation="测试",
            invalidation_level=103.0,
            targets=[99.0],
            evidence_ids=["e1"],
        ),
        alternative_scenario=None,
        market_context=[],
        risks=[],
        uncertainties=[],
        evidence=[],
    )
    audit = audit_advice(packet)
    assert not audit.passed
    assert len(audit.violations) >= 3


def test_llm_wording_schema_cannot_invent_setup_or_price() -> None:
    with pytest.raises(ValueError, match="must not invent"):
        _parse(
            {
                "summary": "观望",
                "market_context": [],
                "rationale": ["强行做多"],
                "confirmation_checklist": [],
                "risks": [],
                "uncertainties": [],
            },
            has_setup=False,
        )
    with pytest.raises(ValueError, match="unapproved prices"):
        _assert_no_new_prices({"summary": "关注 1234.5"}, [100.0, 99.0])


def test_report_contract_contains_no_v1_decision_chain() -> None:
    ctx = _context()
    packet = build_advice_packet(ctx)
    report = build_advice_report(ctx, packet, run_id="test", run_config={"generation_mode": "rule"})
    assert report["artifact_kind"] == "human_review_advice"
    assert report["artifact_version"] == 2
    assert report["advice"]["decision"] == "WATCH_LONG"
    for removed in ("agent_trace", "signals", "projections", "path_summary", "validated_plans"):
        assert removed not in report
