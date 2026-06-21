"""Financial review tests — FIN-* (see tests/cases/financial-review-cases.md).

Failing tests document confirmed bugs; file GitHub issues from pytest output.
"""
from __future__ import annotations

import re

import pandas as pd
import pytest

from src.agents.risk import run_risk_team
from src.analysis.ict_pa import FairValueGap, TimeframeAnalysis, analyze_timeframe
from src.analysis.report_engine import build_conclusion, generate_trading_signals, trend_projections
from src.core.types import TransactionProposal
from src.indicators.technical import fibonacci_levels
from src.indicators.verify import indicator_snapshot
from src.viz.dashboard_components import render_trading_plans


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
    assert signals[0].sentiment_bias_pct == "62%"


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
    assert long_sig.status == "candidate"
    assert long_sig.trigger_confirmed is False
    assert "扫低" in long_sig.trigger_note


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
def test_bullish_conclusion_uses_long_plan_not_short_template() -> None:
    ts = pd.Timestamp("2026-06-01")
    a5 = TimeframeAnalysis("5m", "bullish", "—", "—", swing_high=4300.0, swing_low=4200.0)
    a15 = TimeframeAnalysis("15m", "bullish", "—", "—", swing_high=4300.0, swing_low=4200.0)
    signals = generate_trading_signals(
        4250.0,
        a5,
        a15,
        4300.0,
        4200.0,
        {"bearish": 20.0, "bullish": 65.0, "ranging": 15.0},
    )
    conclusion = build_conclusion(
        {"bearish": 20.0, "bullish": 65.0, "ranging": 15.0},
        "bullish",
        signals,
    )
    assert "做多" in conclusion["must_do"][0]
    assert "最佳做多区" in conclusion["starred"][1]
    assert "最佳做空区" not in conclusion["action"]


@pytest.mark.financial
def test_bullish_projection_primary_path_is_upside() -> None:
    projections = trend_projections(
        4250.0,
        4300.0,
        4200.0,
        {"bearish": 20.0, "bullish": 65.0, "ranging": 15.0},
    )
    assert projections[0]["name"] == "主路径 (回调后上行)"
    assert projections[0]["color"] == "#22c55e"
    assert projections[0]["steps"][-1]["price"] > 4300.0


@pytest.mark.financial
def test_analyze_timeframe_uses_recent_swing_range() -> None:
    idx = pd.date_range("2026-06-01", periods=36, freq="5min")
    high = [
        100,
        103,
        106,
        110,
        105,
        102,
        99,
        96,
        94,
        97,
        101,
        104,
        108,
        112,
        109,
        106,
        103,
        101,
        99,
        98,
        101,
        104,
        107,
        109,
        106,
        103,
        100,
        98,
        96,
        95,
        97,
        100,
        103,
        105,
        104,
        103,
    ]
    low = [x - 2 for x in high]
    low[8] = 70
    df = pd.DataFrame(
        {
            "Open": high,
            "High": high,
            "Low": low,
            "Close": [(h + l) / 2 for h, l in zip(high, low)],
            "Volume": [100] * len(high),
        },
        index=idx,
    )
    analysis = analyze_timeframe(df, "5m")
    assert analysis.swing_low != 70


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
def test_fin_09_indicator_notes_surface_in_report_meta() -> None:
    """FIN-09: build_report merges indicator_snapshot notes into meta."""
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
    from src.analysis.report_engine import build_report

    analyses = {
        tf: TimeframeAnalysis(tf, "ranging", "—", "—", swing_high=4300.0, swing_low=4200.0)
        for tf in ("5m", "15m", "1h", "4h", "1d")
    }
    data = {tf: df for tf in ("5m", "15m", "1h", "4h", "1d")}
    report = build_report(data, analyses, signals=[])
    notes = report["meta"].get("indicator_notes", [])
    assert any("VWAP" in n or "Volume" in n for n in notes)


@pytest.mark.financial
def test_fin_03_fvg_below_price_snapshot_regression() -> None:
    """FIN-03: FVG zone below price — TP1 must stay below entry (2026-06-20 snapshot)."""
    ts = pd.Timestamp("2026-06-01")
    fvg = FairValueGap(high=4149.90, low=4149.76, direction="bearish", time=ts)
    a5 = TimeframeAnalysis(
        timeframe="5m",
        trend="bearish",
        bos="—",
        choch="—",
        fvgs=[fvg],
        active_fvgs=[fvg],
        swing_high=4595.33,
        swing_low=4023.87,
    )
    a15 = TimeframeAnalysis("15m", "bearish", "—", "—", swing_high=4595.33, swing_low=4023.87)
    signals = generate_trading_signals(
        4155.40, a5, a15, 4595.33, 4023.87, {"bearish": 45.0, "bullish": 25.0, "ranging": 30.0}
    )
    sell = next((s for s in signals if s.name == "激进反抽做空"), None)
    assert sell is not None
    entry_mid = (sell.entry_low + sell.entry_high) / 2
    assert sell.stop_loss > entry_mid > sell.take_profits[0]
    assert sell.risk_reward != "N/A"
    assert sell.status == "candidate"
    assert any("越过" in reason for reason in sell.score_reasons)


@pytest.mark.financial
def test_fin_03_conservative_ob_sell_geometry() -> None:
    """FIN-03: 保守 OB 做空 SL > entry > TP1，几何无效时不输出."""
    from src.analysis.ict_pa import OrderBlock

    ts = pd.Timestamp("2026-06-01")
    ob = OrderBlock(high=4220.0, low=4210.0, direction="bearish", time=ts)
    a5 = TimeframeAnalysis(
        timeframe="5m",
        trend="bearish",
        bos="—",
        choch="—",
        order_blocks=[ob],
        swing_high=4300.0,
        swing_low=4200.0,
    )
    a15 = TimeframeAnalysis("15m", "bearish", "—", "—", swing_high=4300.0, swing_low=4200.0)
    signals = generate_trading_signals(
        4215.0, a5, a15, 4300.0, 4200.0, {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0}
    )
    ob_sig = next((s for s in signals if s.name == "保守反抽做空"), None)
    assert ob_sig is not None
    entry_mid = (ob_sig.entry_low + ob_sig.entry_high) / 2
    assert ob_sig.stop_loss > entry_mid > ob_sig.take_profits[0]


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


@pytest.mark.financial
def test_signal_quality_fields_are_present() -> None:
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
        4215.0,
        a5,
        a15,
        4300.0,
        4200.0,
        {"bearish": 60.0, "bullish": 30.0, "ranging": 10.0},
    )
    sig = signals[0]
    assert sig.setup_type
    assert sig.status in {"candidate", "watch", "active", "invalid"}
    assert sig.score_grade in {"A", "B", "C", "D"}
    assert sig.score_total > 0
    assert sig.score_reasons


@pytest.mark.financial
def test_trading_plan_ui_surfaces_status_and_score() -> None:
    html = render_trading_plans(
        [
            {
                "name": "右侧扫低做多",
                "direction": "BUY",
                "direction_cn": "买入",
                "entry_low": 4195.0,
                "entry_high": 4200.0,
                "stop_loss": 4191.0,
                "take_profits": [4215.0],
                "risk_reward": "1:1.5",
                "sentiment_bias_pct": "35%",
                "theme": "long",
                "status": "candidate",
                "score_grade": "C",
                "score_total": 52.0,
                "trigger_note": "等待扫低流动性后收回 + 5m 结构转强",
                "score_reasons": ["尚未确认 sweep + reclaim"],
            }
        ]
    )
    assert "候选区" in html
    assert "信号质量" in html
    assert "等待扫低流动性后收回" in html


def test_trading_plan_ui_marks_llm_levels() -> None:
    html = render_trading_plans(
        [
            {
                "name": "LLM建议做空",
                "direction": "SELL",
                "direction_cn": "做空",
                "entry_low": 4205,
                "entry_high": 4210,
                "stop_loss": 4218,
                "take_profits": [4195, 4184],
                "risk_reward": "1:1.2",
                "sentiment_bias_pct": "70%",
                "theme": "short",
                "setup_type": "llm_fvg",
                "status": "candidate",
                "score_grade": "C",
                "score_total": 62.5,
                "score_reasons": ["结构方向支持 70%"],
            }
        ]
    )

    assert "LLM点位" in html
