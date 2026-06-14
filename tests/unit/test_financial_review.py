"""Financial review tests — FIN-* (see tests/cases/financial-review-cases.md).

Failing tests document confirmed bugs; file GitHub issues from pytest output.
"""
from __future__ import annotations

import re

import pandas as pd
import pytest

from src.agents.risk import run_risk_team
from src.analysis.ict_pa import FairValueGap, TimeframeAnalysis
from src.analysis.report_engine import build_conclusion, generate_trading_signals
from src.core.types import TransactionProposal
from src.indicators.technical import fibonacci_levels
from src.indicators.verify import indicator_snapshot


def _proposal(*, bias: str = "neutral", direction: str = "short") -> TransactionProposal:
    return TransactionProposal(
        primary_direction=direction,  # type: ignore[arg-type]
        signal_indices=[0, 1],
        rationale=["test"],
        debate_bias=bias,  # type: ignore[arg-type]
    )


@pytest.mark.financial
def test_fin_01_neutral_debate_aggressive_should_not_auto_approve() -> None:
    """FIN-01 / F-001: 震荡共识时不应默认通过 aggressive/neutral 档."""
    reviews = {r.profile: r for r in run_risk_team(_proposal(bias="neutral"), signal_count=3)}
    assert reviews["conservative"].approved is False
    # 文档意图：震荡市降低通过率；当前 L37 运算符优先级导致仍为 True
    assert reviews["aggressive"].approved is False, "aggressive 在 neutral 共识下不应 approved"
    assert reviews["neutral"].approved is False, "neutral 档在 neutral 共识下不应 approved"


@pytest.mark.financial
def test_fin_02_win_rate_matches_sentiment_not_backtest() -> None:
    """FIN-02 / F-002: win_rate 当前等于 sentiment 分量（命名误导，值本身一致）."""
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
    sentiment = {"bearish": 62.0, "bullish": 28.0, "ranging": 10.0}
    signals = generate_trading_signals(4215.0, a5, a15, 4300.0, 4200.0, sentiment)
    assert signals, "need at least one signal"
    assert signals[0].win_rate == "62%"
    # 字段名 win_rate 暗示回测胜率 — 见 FIN-UI-01 / Issue


@pytest.mark.financial
def test_fin_03_risk_reward_should_match_geometry() -> None:
    """FIN-03 / F-003: risk_reward 应由 entry/SL/TP 计算，非硬编码."""
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
        4215.0, a5, a15, 4300.0, 4200.0, {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0}
    )
    sig = signals[0]
    entry_mid = (sig.entry_low + sig.entry_high) / 2
    risk = abs(entry_mid - sig.stop_loss)
    reward = abs(entry_mid - sig.take_profits[0])
    assert risk > 0
    computed = reward / risk
    # 展示值应反映几何 R:R（容差 0.15），而非固定文案
    assert sig.risk_reward != "1:2.5 ~ 1:4" or computed >= 2.4, (
        f"risk_reward 硬编码为 {sig.risk_reward}，实际约 1:{computed:.1f}"
    )


@pytest.mark.financial
def test_fin_04_sweep_long_geometry() -> None:
    """FIN-04 / F-004: 扫低做多 magic number 文档化（当前固定 5/9 点）."""
    ts = pd.Timestamp("2026-06-01")
    a5 = TimeframeAnalysis("5m", "ranging", "—", "—", swing_high=4300.0, swing_low=4200.0)
    a15 = TimeframeAnalysis("15m", "ranging", "—", "—", swing_high=4300.0, swing_low=4200.0)
    signals = generate_trading_signals(
        4218.0, a5, a15, 4300.0, 4200.0, {"bearish": 50.0, "bullish": 40.0, "ranging": 10.0}
    )
    long_sig = next(s for s in signals if s.direction == "BUY")
    assert long_sig.entry_low == 4195.0
    assert long_sig.entry_high == 4200.0
    assert long_sig.stop_loss == 4191.0


@pytest.mark.financial
def test_fin_06_conclusion_no_hardcoded_price_without_signals() -> None:
    """FIN-06 / F-006: 无 signals 时 conclusion 不得含硬编码价位."""
    conclusion = build_conclusion(
        {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0},
        "bearish",
        [],
    )
    assert "4389" not in conclusion["action"]
    assert "4396" not in conclusion["action"]


@pytest.mark.financial
def test_fin_07_fibonacci_probability_is_static_map() -> None:
    """FIN-07 / F-007: probability 为静态常量（非统计）— 文档化行为."""
    levels = fibonacci_levels(4300.0, 4200.0)
    by_ratio = {lv["ratio"]: lv["probability"] for lv in levels}
    assert by_ratio[0.382] == 0.65
    assert by_ratio[0.618] == 0.70


@pytest.mark.financial
def test_fin_09_vwap_zero_volume_should_warn() -> None:
    """FIN-09 / F-009: Volume 全 0 时应有 VWAP 可用性警告."""
    idx = pd.date_range("2026-01-01", periods=20, freq="5min")
    df = pd.DataFrame(
        {
            "Open": 4200.0,
            "High": 4201.0,
            "Low": 4199.0,
            "Close": 4200.0,
            "Volume": 0,
            "EMA20": 4200.0,
            "EMA50": 4200.0,
            "EMA610": 4200.0,
            "VWAP": 4200.0,
        },
        index=idx,
    )
    snap = indicator_snapshot(df, "5m")
    notes_text = " ".join(snap.get("notes", []))
    assert re.search(r"VWAP|Volume|volume|成交量", notes_text, re.I), (
        "Volume 全 0 时应在 notes 中警告 VWAP 不可靠"
    )


@pytest.mark.financial
def test_fin_03_sell_signal_sl_entry_tp_order() -> None:
    """FIN-03: SELL 信号几何方向 SL > entry > TP1."""
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
    a15 = TimeframeAnalysis("15m", "bearish", "—", "—")
    signals = generate_trading_signals(
        4215.0, a5, a15, 4300.0, 4200.0, {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0}
    )
    sell = next(s for s in signals if s.direction == "SELL")
    entry_mid = (sell.entry_low + sell.entry_high) / 2
    assert sell.stop_loss > entry_mid > sell.take_profits[0]
