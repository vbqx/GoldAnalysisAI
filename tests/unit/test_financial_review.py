"""Financial review tests — FIN-* (see tests/cases/financial-review-cases.md).

Failing tests document confirmed bugs; file GitHub issues from pytest output.
"""
from __future__ import annotations

import re

import pandas as pd
import pytest

from src.agents.risk import run_risk_team
from src.analysis.ict_pa import (
    FairValueGap,
    StructureEvent,
    TimeframeAnalysis,
    analyze_timeframe,
)
from src.analysis.report_engine import TradingSignal, build_conclusion, build_strategy_plans, generate_trading_signals, trend_projections
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
def test_sweep_long_requires_reclaim_and_structure_shift() -> None:
    a5 = TimeframeAnalysis(
        "5m",
        "ranging",
        "-",
        "bullish @ 4204.00",
        swing_high=4300.0,
        swing_low=4200.0,
        events=[
            StructureEvent(
                kind="CHoCH",
                direction="bullish",
                price=4204.0,
                time=pd.Timestamp("2026-06-01"),
            )
        ],
        last_close=4202.0,
        recent_low=4198.5,
    )
    a15 = TimeframeAnalysis("15m", "ranging", "-", "-", swing_high=4300.0, swing_low=4200.0)

    signals = generate_trading_signals(
        4202.0, a5, a15, 4300.0, 4200.0, {"bearish": 35.0, "bullish": 45.0, "ranging": 20.0}
    )
    long_sig = next(s for s in signals if s.direction == "BUY")

    assert long_sig.trigger_confirmed is True
    assert long_sig.status == "active"
    assert any("扫低收回已确认" in reason or "PA sweep" in reason for reason in long_sig.score_reasons)


@pytest.mark.financial
def test_sweep_long_without_structure_shift_stays_candidate() -> None:
    a5 = TimeframeAnalysis(
        "5m",
        "ranging",
        "-",
        "-",
        swing_high=4300.0,
        swing_low=4200.0,
        last_close=4202.0,
        recent_low=4198.5,
    )
    a15 = TimeframeAnalysis("15m", "ranging", "-", "-", swing_high=4300.0, swing_low=4200.0)

    signals = generate_trading_signals(
        4202.0, a5, a15, 4300.0, 4200.0, {"bearish": 35.0, "bullish": 45.0, "ranging": 20.0}
    )
    long_sig = next(s for s in signals if s.direction == "BUY")

    assert long_sig.trigger_confirmed is False
    assert long_sig.status == "candidate"


@pytest.mark.financial
def test_sweep_long_without_reclaim_stays_candidate() -> None:
    a5 = TimeframeAnalysis(
        "5m",
        "ranging",
        "-",
        "bullish @ 4204.00",
        swing_high=4300.0,
        swing_low=4200.0,
        events=[
            StructureEvent(
                kind="CHoCH",
                direction="bullish",
                price=4204.0,
                time=pd.Timestamp("2026-06-01"),
            )
        ],
        atr=10.0,
        last_close=4199.0,
        recent_low=4197.0,
    )
    a15 = TimeframeAnalysis("15m", "ranging", "-", "-", swing_high=4300.0, swing_low=4200.0)

    signals = generate_trading_signals(
        4199.0, a5, a15, 4300.0, 4200.0, {"bearish": 35.0, "bullish": 45.0, "ranging": 20.0}
    )
    long_sig = next(s for s in signals if s.direction == "BUY")

    assert long_sig.trigger_confirmed is False
    assert long_sig.status == "candidate"
    assert any("reclaim" in reason for reason in long_sig.score_reasons)


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
def test_analyze_timeframe_carries_atr_and_recent_prices() -> None:
    idx = pd.date_range("2026-06-01", periods=20, freq="5min")
    df = pd.DataFrame(
        {
            "Open": [100.0 + i * 0.1 for i in range(20)],
            "High": [101.0 + i * 0.1 for i in range(20)],
            "Low": [99.0 + i * 0.1 for i in range(20)],
            "Close": [100.5 + i * 0.1 for i in range(20)],
            "Volume": [100] * 20,
            "ATR14": [None] * 19 + [12.5],
        },
        index=idx,
    )

    analysis = analyze_timeframe(df, "5m")

    assert analysis.atr == 12.5
    assert analysis.last_close == pytest.approx(102.4)
    assert analysis.recent_high == pytest.approx(102.9)
    assert analysis.recent_low == pytest.approx(100.5)



@pytest.mark.financial
def test_liquidity_uses_swing_high_low() -> None:
    idx = pd.date_range("2026-06-01", periods=30, freq="5min")
    df = pd.DataFrame(
        {
            "Open": [4200.0 + (i % 3) for i in range(30)],
            "High": [4202.0 + (i % 3) for i in range(30)],
            "Low": [4198.0 + (i % 3) for i in range(30)],
            "Close": [4201.0 + (i % 3) for i in range(30)],
            "Volume": [100] * 30,
        },
        index=idx,
    )
    analysis = analyze_timeframe(df, "5m")
    kinds = {z.kind for z in analysis.liquidity}
    assert kinds <= {"swing_high", "swing_low"}
    for zone in analysis.liquidity:
        assert "摆动" in zone.label


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
        tf: TimeframeAnalysis(
            tf,
            "ranging",
            "—",
            "—",
            events=[StructureEvent("BOS", "bearish", 4240.0, idx[-2], scope="internal")],
            swing_high=4300.0,
            swing_low=4200.0,
        )
        for tf in ("5m", "15m", "1h", "4h", "1d")
    }
    data = {tf: df for tf in ("5m", "15m", "1h", "4h", "1d")}
    report = build_report(data, analyses, signals=[])
    notes = report["meta"].get("indicator_notes", [])
    assert any("VWAP" in n or "Volume" in n for n in notes)
    for tf in ("4h", "1h", "15m"):
        panel = report["timeframes"][tf]
        assert panel["trend"] == analyses[tf].trend
        assert panel["bos_list"][0]["kind"] == "BOS"
        assert "ema_relation" in panel
        assert {"strong_high", "weak_high", "strong_low", "weak_low"} <= set(panel)


@pytest.mark.financial
def test_fin_03_fvg_below_price_snapshot_regression() -> None:
    """FIN-03: 规则 PA 做空几何仍须满足 SL > entry > TP1."""
    ts = pd.Timestamp("2026-06-01")
    a5 = TimeframeAnalysis(
        timeframe="5m",
        trend="bearish",
        bos="—",
        choch="—",
        swing_high=4595.33,
        swing_low=4023.87,
    )
    a15 = TimeframeAnalysis("15m", "bearish", "—", "—", swing_high=4595.33, swing_low=4023.87)
    price_action = {
        "5m": {
            "volume_ok": True,
            "sr_levels": [
                {
                    "price": 4162.0,
                    "direction": "resistance",
                    "kind": "consecutive_sr",
                    "label": "量价阻力",
                    "time": ts.isoformat(),
                }
            ],
            "volume_profile": {"poc": 4150.0, "vah": 4162.0, "val": 4140.0},
        }
    }
    signals = generate_trading_signals(
        4155.40,
        a5,
        a15,
        4595.33,
        4023.87,
        {"bearish": 45.0, "bullish": 25.0, "ranging": 30.0},
        price_action=price_action,
    )
    sell = next((s for s in signals if s.name == "激进反抽做空"), None)
    assert sell is not None
    entry_mid = (sell.entry_low + sell.entry_high) / 2
    assert sell.stop_loss > entry_mid > sell.take_profits[0]
    assert sell.risk_reward != "N/A"
    assert sell.setup_type == "pa_resistance_short"


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
def test_crossed_stop_signal_is_invalid_not_watch() -> None:
    ts = pd.Timestamp("2026-06-01")
    a5 = TimeframeAnalysis(
        timeframe="5m",
        trend="bearish",
        bos="?",
        choch="?",
        swing_high=4215.0,
        swing_low=4140.0,
    )
    a15 = TimeframeAnalysis("15m", "bearish", "?", "?", swing_high=4215.0, swing_low=4140.0)
    price_action = {
        "5m": {
            "volume_ok": True,
            "sr_levels": [
                {
                    "price": 4200.0,
                    "direction": "resistance",
                    "kind": "consecutive_sr",
                    "label": "量价阻力",
                    "time": ts.isoformat(),
                }
            ],
            "volume_profile": {"poc": 4188.0, "vah": 4200.0, "val": 4175.0},
        }
    }

    signals = generate_trading_signals(
        4205.0,
        a5,
        a15,
        4215.0,
        4140.0,
        {"bearish": 70.0, "bullish": 20.0, "ranging": 10.0},
        price_action=price_action,
    )

    assert signals
    sell = next(s for s in signals if s.direction == "SELL")
    assert sell.status == "invalid"
    assert sell.stop_loss <= 4205.0
    assert "已越过止损" in "；".join(sell.score_reasons)


@pytest.mark.financial
def test_strategy_plans_skip_invalid_expired_signals() -> None:
    expired = TradingSignal(
        name="过期 FVG 做空",
        direction="SELL",
        direction_cn="卖出",
        entry_low=4181.63,
        entry_high=4183.38,
        stop_loss=4184.26,
        take_profits=[4169.96, 4140.12],
        risk_reward="1:2.0",
        sentiment_bias_pct="70%",
        position_size="轻仓试探",
        note="失效 FVG 回测方案 A",
        theme="short",
        status="invalid",
    )
    valid = TradingSignal(
        name="有效反弹做空",
        direction="SELL",
        direction_cn="卖出",
        entry_low=4187.0,
        entry_high=4190.0,
        stop_loss=4193.0,
        take_profits=[4174.0, 4160.0],
        risk_reward="1:2.0",
        sentiment_bias_pct="70%",
        position_size="轻仓试探",
        note="当前有效方案",
        theme="short",
        status="candidate",
    )

    plans = build_strategy_plans([expired, valid])

    assert len(plans) == 1
    assert plans[0]["name"] == "方案 A（主策略）"
    assert plans[0]["entry"] == "4187.0 ~ 4190.0"
    assert "4181.63" not in plans[0]["entry"]


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
    assert "置信" in html
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

    assert "LLM" in html


def test_trading_plan_ui_shows_rejected_expander_with_reason() -> None:
    html = render_trading_plans(
        [
            {
                "name": "LLM路径A·做空",
                "direction": "SELL",
                "direction_cn": "做空",
                "entry_low": 4060,
                "entry_high": 4065,
                "stop_loss": 4070,
                "take_profits": [4040],
                "theme": "short",
                "status": "candidate",
                "signal_role": "primary",
                "signal_id": "sig-a",
                "setup_type": "llm_poc_va",
            },
            {
                "name": "右侧扫低做多",
                "direction": "BUY",
                "direction_cn": "做多",
                "entry_low": 4044,
                "entry_high": 4049,
                "stop_loss": 4040,
                "take_profits": [4060],
                "theme": "long",
                "status": "candidate",
                "signal_role": "rejected",
                "signal_id": "sig-b",
                "rejection_reason": "经理选用主方案「LLM路径A·做空」，本方案未进入授权列表；方向与主方案相反",
                "rejection_notes": [
                    "经理选用主方案「LLM路径A·做空」，本方案未进入授权列表",
                    "风控[激进]否决 · 仓位0%：market snapshot not executable",
                    "交易员未提名本方案（主方向 short，提名索引 [0]）",
                    "方向与主方案相反，作逆势/备用库存保留，不进本次授权",
                ],
            },
        ],
        meta={"execution_authorized": True, "authorized_signal_ids": ["sig-a"]},
    )
    assert "未选用 / 已拒绝候选" in html
    assert "拒绝原因" in html
    assert "主方案" in html
    assert "风控[激进]否决" in html
    assert "reject-list" in html
    assert "被拒绝" in html
    assert "候选区" not in html.split("未选用 / 已拒绝候选")[-1]
    # Minified HTML must still include rendered plan-grid (not markdown-escaped).
    assert 'class="plan-grid"' in html
    assert "\n    <div" not in html  # no indented blank-line code-fence bait


def test_trading_plan_ui_renders_three_unified_cards() -> None:
    signals = [
        {
            "name": "激进反抽做空",
            "direction": "SELL",
            "direction_cn": "卖出",
            "entry_low": 4210.0,
            "entry_high": 4215.0,
            "stop_loss": 4220.0,
            "take_profits": [4200.0, 4190.0, 4180.0],
            "risk_reward": "1:2.0",
            "sentiment_bias_pct": "62%",
            "theme": "short",
            "signal_role": "primary",
            "status": "candidate",
            "score_grade": "B",
            "score_total": 68.0,
            "trigger_note": "等待反抽失败",
        },
        {
            "name": "保守反抽做空",
            "direction": "SELL",
            "direction_cn": "卖出",
            "entry_low": 4220.0,
            "entry_high": 4225.0,
            "stop_loss": 4230.0,
            "take_profits": [4210.0],
            "risk_reward": "1:1.5",
            "sentiment_bias_pct": "57%",
            "theme": "short",
            "signal_role": "alternate",
            "status": "candidate",
            "score_grade": "C",
            "score_total": 55.0,
            "trigger_note": "等待反抽失败",
        },
        {
            "name": "右侧扫低做多",
            "direction": "BUY",
            "direction_cn": "买入",
            "entry_low": 4195.0,
            "entry_high": 4200.0,
            "stop_loss": 4191.0,
            "take_profits": [4215.0],
            "risk_reward": "1:1.5",
            "sentiment_bias_pct": "28%",
            "theme": "long",
            "signal_role": "alternate",
            "status": "candidate",
            "score_grade": "C",
            "score_total": 52.0,
            "trigger_note": "等待 sweep + reclaim",
        },
    ]
    html = render_trading_plans(signals)
    assert "方案 A（主策略）" in html
    assert "方案 B（备选）" in html
    assert "方案 C（逆势）" in html
    assert html.count("plan-card") == 3
    assert html.count("置信") == 3
