"""External data sources — DXY, news, social (mocked HTTP / TradingView)."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.data.sources.dxy import fetch_dxy_impact
from src.data.sources.fundamentals import FundamentalsDataSource
from src.data.sources.news import NewsDataSource
from src.data.sources.news_feed import fetch_news_bundle
from src.data.sources.social import SocialDataSource
from src.data.sources.social_feed import fetch_social_sentiment


def _dxy_df(change_pct: float) -> pd.DataFrame:
    prev = 100.0
    latest = prev * (1 + change_pct / 100)
    return pd.DataFrame({"Close": [prev, latest]})


@patch("src.data.sources.dxy.fetch_symbol_daily")
def test_dxy_bearish_on_strength(mock_tv) -> None:
    mock_tv.return_value = _dxy_df(0.5)
    impact, refs = fetch_dxy_impact()
    assert "利空黄金" in impact
    assert refs["source"] == "tradingview"
    assert refs["bias"] == "bearish"


@patch("src.data.sources.dxy.fetch_symbol_daily")
def test_dxy_bullish_on_weakness(mock_tv) -> None:
    mock_tv.return_value = _dxy_df(-0.4)
    impact, refs = fetch_dxy_impact()
    assert "利好黄金" in impact
    assert refs["bias"] == "bullish"


@patch("src.data.sources.dxy.fetch_symbol_daily", side_effect=RuntimeError("tv down"))
def test_dxy_fallback_placeholder(mock_tv) -> None:
    impact, refs = fetch_dxy_impact()
    assert refs["source"] == "placeholder"
    assert "偏强" in impact or "回退" in impact


@patch("src.data.sources.fundamentals.fetch_dxy_impact")
def test_fundamentals_source_uses_dxy(mock_fetch) -> None:
    mock_fetch.return_value = ("偏强 (104.2, 日 +0.30%) → 利空黄金", {"source": "tradingview", "bias": "bearish"})
    ext = FundamentalsDataSource().fetch_external()
    assert "利空黄金" in ext.dxy_impact
    items = FundamentalsDataSource().fetch_evidence()
    assert items[0].refs.get("source") == "tradingview"


@patch("src.data.sources.news_feed.FINNHUB_API_KEY", "test-key")
@patch("src.data.sources.news_feed._finnhub_news")
@patch("src.data.sources.news_feed._finnhub_calendar")
def test_news_finnhub_bundle(mock_cal, mock_news) -> None:
    mock_news.return_value = ["Fed holds rates (Reuters)"]
    mock_cal.return_value = "2026-06-14 US CPI"
    headlines, risk, refs = fetch_news_bundle()
    assert headlines == ["Fed holds rates (Reuters)"]
    assert "CPI" in risk
    assert refs["source"] == "live"


@patch("src.data.sources.news_feed.FINNHUB_API_KEY", "")
@patch("src.data.sources.news_feed.get_text")
def test_news_rss_fallback(mock_text) -> None:
    rss = """<?xml version="1.0"?>
    <rss><channel>
      <item><title>Gold rises on Fed outlook</title></item>
    </channel></rss>"""
    mock_text.return_value = rss
    headlines, risk, refs = fetch_news_bundle()
    assert any("Gold" in h for h in headlines)
    assert "google_news_rss" in refs.get("sources", [])


@patch("src.data.sources.social_feed.get_json")
def test_reddit_sentiment_bullish(mock_json) -> None:
    mock_json.return_value = {
        "data": {
            "children": [
                {"data": {"title": "Gold bullish breakout long support", "score": 50, "upvote_ratio": 0.9, "stickied": False}},
                {"data": {"title": "XAUUSD rally moon", "score": 30, "upvote_ratio": 0.85, "stickied": False}},
            ]
        }
    }
    summary, posts, refs = fetch_social_sentiment()
    assert refs["source"] == "reddit"
    assert "偏多" in summary or len(posts) >= 1


@patch("src.data.sources.social.fetch_social_sentiment")
def test_social_source_external(mock_fetch) -> None:
    mock_fetch.return_value = (
        "Reddit 偏多（60% 加权 · 10 帖）",
        [{"title": "gold long", "subreddit": "Gold", "score": 10, "upvote_ratio": 0.8}],
        {"source": "reddit", "bias": "bullish"},
    )
    ext = SocialDataSource().fetch_external()
    assert "Reddit" in ext.social_sentiment
    items = SocialDataSource().fetch_evidence()
    assert any("社媒情绪" in i.summary for i in items)


@patch("src.data.sources.news.fetch_news_bundle")
def test_news_source_evidence(mock_bundle) -> None:
    mock_bundle.return_value = (
        ["Gold hits record high"],
        "近 48h 无高影响美元宏观事件（Finnhub）",
        {"source": "live", "sources": ["finnhub_news"]},
    )
    items = NewsDataSource().fetch_evidence()
    assert any("Gold hits" in i.summary for i in items)
