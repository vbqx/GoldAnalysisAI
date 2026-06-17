"""Analyst Team input density regression tests."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd
import pytest

from src.agents.analysts.technical import run_technical_analyst
from src.agents.analysts.fundamentals import run_fundamentals_analyst
from src.agents.analysts.news import run_news_analyst
from src.agents.analysts.sentiment import run_sentiment_analyst
from src.agents.llm.payload import news_analyst_payload
from src.analysis.ict_pa import FairValueGap, LiquidityZone, OrderBlock, TimeframeAnalysis
from src.agents.llm.schemas import parse_analyst_report
from src.core.types import CalendarEvent, ExternalFactors, HeadlineItem, MacroQuote, MarketContext
from src.data.context_builder import (
    build_jin10_kline_summary,
    finalize_market_context,
)
from src.data.fetch_pipeline import fetch_external_bundle
from src.data.news_topics import cluster_headline_topics
from src.data.sources.jin10_feed import fetch_jin10_kline
from src.indicators.technical import enrich


def _minimal_ctx(ext: ExternalFactors) -> MarketContext:
    df = pd.DataFrame(
        {
            "Open": [100.0, 101.0],
            "High": [101.0, 102.0],
            "Low": [99.0, 100.0],
            "Close": [100.5, 101.5],
            "Volume": [100, 120],
        }
    )
    ctx = MarketContext(
        enriched={"5m": df, "1d": df},
        analyses={},
        metrics={"current_price": 101.5, "daily_change_pct": 1.0},
        price=101.5,
        external=ext,
        source_label="test",
    )
    return finalize_market_context(ctx)


def _technical_ctx() -> MarketContext:
    idx = pd.date_range("2026-06-16", periods=32, freq="5min")
    raw = pd.DataFrame(
        {
            "Open": [100.0 + i * 0.1 for i in range(32)],
            "High": [101.0 + i * 0.1 for i in range(32)],
            "Low": [99.0 + i * 0.1 for i in range(32)],
            "Close": [100.5 + i * 0.1 for i in range(32)],
            "Volume": [100 + i for i in range(31)] + [260],
        },
        index=idx,
    )
    enriched = {tf: enrich(raw.copy()) for tf in ("1d", "4h", "1h", "15m", "5m")}
    now = idx[-1]
    analyses = {
        tf: TimeframeAnalysis(
            timeframe=tf,
            trend="bearish" if tf == "1d" else "bullish",
            bos="bearish @ 101.0" if tf == "1d" else "bullish @ 102.0",
            choch="无",
            order_blocks=[OrderBlock(high=106.0, low=104.0, direction="bearish", time=now)],
            fvgs=[FairValueGap(high=105.5, low=104.5, direction="bearish", time=now)],
            active_fvgs=[FairValueGap(high=105.5, low=104.5, direction="bearish", time=now)],
            liquidity=[LiquidityZone(price=106.5, kind="stop_hunt_high", label="Stop Hunt Above Highs")],
            swing_high=110.0,
            swing_low=90.0,
            premium_discount="premium",
            equilibrium=100.0,
            volume_signal="放量 1.8x — 聪明钱可能活跃",
        )
        for tf in ("1d", "4h", "1h", "15m", "5m")
    }
    ctx = MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics={
            "current_price": 103.6,
            "daily_change_pct": 1.0,
            "daily_high": 104.1,
            "daily_low": 102.1,
        },
        price=103.6,
        external=ExternalFactors(),
        source_label="test",
    )
    return finalize_market_context(ctx)


def _multi_analyst_ctx() -> MarketContext:
    ctx = _technical_ctx()
    ctx.external = ExternalFactors(
        dxy_impact="DXY 偏强 → 利空黄金",
        headline_items=[
            HeadlineItem(source="jin10_flash", text="地缘冲突升级，避险买盘推升黄金"),
            HeadlineItem(source="jin10_news", text="美联储官员暗示降息路径"),
        ],
        calendar_events=[
            CalendarEvent(time="2026-06-16 20:30", region="美国", event="美国6月CPI年率", importance=3.0),
        ],
        macro_quotes=[
            MacroQuote(name="DXY", symbol="TVC:DXY", close=104.0, change_pct=0.3, impact="偏强", bias="bearish"),
            MacroQuote(name="US10Y", symbol="TVC:US10Y", close=4.2, change_pct=0.1, impact="上行", bias="bearish"),
        ],
        social_sentiment="TV 社媒偏多",
        social_posts=[
            {"kind": "ideas", "title": "Gold breakout setup", "author": "tv_user", "likes": 24, "bias_delta": 2},
            {"kind": "minds", "text": "XAU looks bid", "author": "macro_user", "likes": 6, "bias_delta": 1},
        ],
        sources=["jin10_flash", "jin10_news", "jin10_calendar", "tradingview_social"],
    )
    return finalize_market_context(ctx)


def test_context_stats_counts_structured_fields() -> None:
    ext = ExternalFactors(
        headline_items=[
            HeadlineItem(source="jin10_flash", text="黄金上涨"),
            HeadlineItem(source="jin10_news", text="美联储讲话"),
        ],
        calendar_events=[CalendarEvent(time="t", region="美国", event="CPI", importance=3.0)],
        macro_quotes=[
            MacroQuote(
                name="DXY",
                symbol="TVC:DXY",
                close=104.0,
                change_pct=0.2,
                impact="偏强",
                bias="bearish",
            )
        ],
        sources=["jin10_flash", "jin10_news", "jin10_calendar"],
    )
    ctx = _minimal_ctx(ext)
    assert ctx.context_stats["headline_items"] == 2
    assert ctx.context_stats["calendar_events"] == 1
    assert ctx.context_stats["macro_quotes"] == 1


def test_context_stats_tracks_technical_inputs() -> None:
    ctx = _technical_ctx()
    tech = ctx.context_stats["technical_inputs"]
    assert tech["bars"]["1d"] == 32
    assert tech["premium_discount_known"] == 5
    assert tech["volume_signal_available"] == 5
    assert tech["liquidity_zones"] == 5
    assert "EMA20" in tech["by_timeframe"]["5m"]["indicator_ready"]


def test_context_stats_tracks_other_analyst_inputs() -> None:
    ctx = _multi_analyst_ctx()
    stats = ctx.context_stats["analyst_inputs"]
    assert stats["fundamentals"]["has_dxy"] is True
    assert stats["fundamentals"]["has_us10y"] is True
    assert stats["news"]["flash"] == 1
    assert stats["news"]["articles"] == 1
    assert stats["news"]["topics"]
    assert stats["sentiment"]["social_posts"] == 2
    assert stats["sentiment"]["social_bias_delta"] == 3


def test_technical_analyst_uses_extended_kline_inputs() -> None:
    ctx = _technical_ctx()
    report = run_technical_analyst(ctx)
    summaries = [item.summary for item in report.items]
    assert any("1d 结构趋势偏空" in summary for summary in summaries)
    assert any("Premium" in summary for summary in summaries)
    assert any("成交量信号" in summary for summary in summaries)
    assert any("流动性" in summary for summary in summaries)
    assert any("Fib" in summary for summary in summaries)


def test_fundamentals_analyst_multi_quote_evidence() -> None:
    ext = ExternalFactors(
        dxy_impact="偏强 → 利空黄金",
        macro_quotes=[
            MacroQuote(name="DXY", symbol="TVC:DXY", close=104.0, change_pct=0.3, impact="偏强", bias="bearish"),
            MacroQuote(name="US10Y", symbol="TVC:US10Y", close=4.2, change_pct=0.1, impact="上行", bias="bearish"),
        ],
    )
    ctx = _minimal_ctx(ext)
    report = run_fundamentals_analyst(ctx)
    assert len(report.items) >= 2
    assert report.bias == "bearish"


def test_fundamentals_analyst_uses_calendar_and_coverage_inputs() -> None:
    ctx = _multi_analyst_ctx()
    report = run_fundamentals_analyst(ctx)
    summaries = [item.summary for item in report.items]
    assert any("高影响宏观日历" in summary for summary in summaries)
    assert any("宏观报价覆盖" in summary for summary in summaries)


def test_news_analyst_structured_evidence_and_bias() -> None:
    ext = ExternalFactors(
        headline_items=[
            HeadlineItem(source="jin10_flash", text="地缘冲突升级，避险买盘推升黄金"),
        ],
        calendar_events=[
            CalendarEvent(time="2026-06-16 20:30", region="美国", event="美国6月CPI年率", importance=3.0),
        ],
        risk_events="2026-06-16 20:30 美国 美国6月CPI年率",
        sources=["jin10_flash", "jin10_calendar"],
    )
    ctx = _minimal_ctx(ext)
    report = run_news_analyst(ctx)
    assert len(report.items) >= 2
    assert any("CPI" in i.summary for i in report.items)


def test_news_analyst_uses_topics_and_channel_density() -> None:
    ctx = _multi_analyst_ctx()
    report = run_news_analyst(ctx)
    summaries = [item.summary for item in report.items]
    assert any("新闻输入密度" in summary for summary in summaries)
    assert any("新闻主题" in summary for summary in summaries)


def test_sentiment_analyst_uses_social_quality_and_structure_divergence() -> None:
    ctx = _multi_analyst_ctx()
    report = run_sentiment_analyst(ctx)
    summaries = [item.summary for item in report.items]
    assert any("社媒样本质量" in summary for summary in summaries)
    assert any("社媒方向汇总" in summary for summary in summaries)
    assert any("多周期结构分歧" in summary for summary in summaries)


def test_cluster_headline_topics() -> None:
    items = [
        HeadlineItem(source="jin10_flash", text="地缘冲突升级，避险买盘推升黄金"),
        HeadlineItem(source="jin10_news", text="美联储官员暗示降息路径"),
        HeadlineItem(source="jin10_flash", text="美国CPI数据即将公布"),
    ]
    topics = cluster_headline_topics(items)
    assert len(topics) >= 2
    assert topics[0]["count"] >= 1


@patch("src.data.context_builder.fetch_jin10_quote", return_value=({"close": "4300.0", "code": "XAUUSD"}, None))
def test_derived_spot_cross_check(_mock_quote) -> None:
    ext = ExternalFactors()
    ctx = _minimal_ctx(ext)
    ctx.price = 4305.0
    ctx = finalize_market_context(ctx)
    cross = ctx.derived.get("spot_cross_check") or {}
    assert cross.get("aligned") is True


def test_news_analyst_payload_channels() -> None:
    ext = ExternalFactors(
        headline_items=[
            HeadlineItem(source="jin10_flash", text="黄金短线拉升"),
            HeadlineItem(source="jin10_news", text="美联储降息预期升温"),
        ],
        calendar_events=[
            CalendarEvent(time="2026-06-16 20:30", region="美国", event="CPI", importance=3.0),
        ],
        sources=["jin10_flash", "jin10_news", "jin10_calendar"],
    )
    ctx = _minimal_ctx(ext)
    payload = news_analyst_payload(ctx)
    assert payload["channels"]["flash"]["count"] == 1
    assert payload["channels"]["articles"]["count"] == 1
    assert payload["channels"]["calendar"]["count"] == 1
    assert payload["news_topics"]


@patch("src.data.fetch_pipeline._fetch_fundamentals_external")
@patch("src.data.fetch_pipeline._fetch_social_external")
@patch("src.data.fetch_pipeline._fetch_news_external")
def test_fetch_external_bundle_parallel(mock_news, mock_social, mock_fund) -> None:
    mock_news.return_value = ExternalFactors(sources=["jin10_flash"])
    mock_social.return_value = ExternalFactors(social_sentiment="偏多")
    mock_fund.return_value = ExternalFactors(dxy_impact="偏强")
    ext = fetch_external_bundle(parallel_http=True)
    mock_news.assert_called_once()
    mock_social.assert_called_once()
    mock_fund.assert_called_once()
    assert "jin10_flash" in ext.sources


@patch("src.data.context_builder.fetch_jin10_kline", return_value=([{"close": 4300.0, "open": 4295.0, "time": "t"}], None))
@patch("src.data.context_builder.fetch_jin10_quote", return_value=({"close": "4300.0", "code": "XAUUSD"}, None))
def test_derived_kline_and_event_countdown(_mock_quote, _mock_kline) -> None:
    from datetime import datetime, timedelta

    future = (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")
    ext = ExternalFactors(
        calendar_events=[
            CalendarEvent(time=future, region="美国", event="CPI", importance=3.0),
        ],
    )
    ctx = _minimal_ctx(ext)
    ctx.price = 4305.0
    ctx = finalize_market_context(ctx)
    kline = ctx.derived.get("jin10_kline_summary") or {}
    assert kline.get("bars") == 1
    countdown = ctx.derived.get("event_countdown") or {}
    assert countdown.get("event") == "CPI"
    assert countdown.get("hours_until", 999) < 12


def test_build_jin10_kline_summary_aligned() -> None:
    summary = build_jin10_kline_summary(
        [{"open": 100.0, "close": 101.0, "time": "t1"}, {"open": 101.0, "close": 102.0, "time": "t2"}],
        102.1,
    )
    assert summary["aligned_with_tv"] is True
    assert summary["bars"] == 2


@patch("src.data.sources.jin10_feed.jin10_call_tool")
def test_fetch_jin10_kline_parses_bars(mock_call) -> None:
    import src.data.sources.jin10_feed as jf

    jf._CACHE.clear()
    mock_call.return_value = {
        "data": [{"close": 4300.0, "open": 4290.0, "time": "2026-06-16 10:00"}],
    }
    with patch("src.data.sources.jin10_feed.JIN10_KLINE_ENABLED", True):
        with patch("src.data.sources.jin10_feed.JIN10_ENABLED", True):
            with patch("src.data.sources.jin10_feed.JIN10_API_TOKEN", "t"):
                bars, err = fetch_jin10_kline()
    mock_call.assert_called_once_with("get_kline", {"code": "XAUUSD", "count": 20})
    assert err is None
    assert len(bars) == 1
    assert bars[0]["close"] == 4300.0


def test_parse_analyst_report_infers_source() -> None:
    report = parse_analyst_report(
        {
            "bias": "bullish",
            "confidence": 0.7,
            "summary": "ok",
            "items": [
                {"category": "news", "summary": "a", "strength": 0.5},
                {"category": "news", "summary": "b", "strength": 0.5},
                {"category": "news", "summary": "c", "strength": 0.5},
                {"category": "news", "summary": "d", "strength": 0.5},
            ],
        },
        agent="news_analyst",
    )
    assert all(i.refs.get("source") == "jin10" for i in report.items)


def test_parse_analyst_report_requires_min_items() -> None:
    with pytest.raises(ValueError, match="min"):
        parse_analyst_report(
            {
                "bias": "neutral",
                "confidence": 0.5,
                "summary": "too few",
                "items": [{"category": "news", "summary": "one", "strength": 0.5}],
            },
            agent="news_analyst",
        )
