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
from src.data.sources.te_calendar_scraper import fetch_te_calendar, scrape_te_calendar_html


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
@patch("src.data.sources.te_calendar_scraper.TE_CALENDAR_ENABLED", True)
@patch("src.data.sources.te_calendar_scraper.requests.get")
def test_te_calendar_direct(mock_get) -> None:
    from pathlib import Path

    html = Path("tests/fixtures/te_calendar_sample.html").read_text(encoding="utf-8")
    mock_resp = mock_get.return_value
    mock_resp.raise_for_status.return_value = None
    mock_resp.text = html

    risk = fetch_te_calendar()
    assert "Building Permits" in risk or "NAHB" in risk


@patch("src.data.sources.news_feed.fetch_te_calendar", return_value="2026-06-14 12:30 United States CPI YoY")
@patch("src.data.sources.news_feed.NEWS_RSS_ENABLED", False)
@patch("src.data.sources.news_feed.TE_CALENDAR_ENABLED", True)
@patch("src.data.sources.news_feed.FINNHUB_API_KEY", "")
def test_te_calendar_bundle(mock_fetch_te) -> None:
    headlines, risk, refs = fetch_news_bundle()
    assert "CPI" in risk
    assert "te_calendar_scrape" in refs.get("sources", [])


def test_te_calendar_parse_html() -> None:
    from datetime import date
    from pathlib import Path

    html = Path("tests/fixtures/te_calendar_sample.html").read_text(encoding="utf-8")
    events = scrape_te_calendar_html(html, today=date(2026, 6, 14), days=3, min_importance=2)
    assert len(events) >= 1
    assert any("Building Permits" in ev["event"] or "NAHB" in ev["event"] for ev in events)


@patch("src.data.sources.news_feed.TE_CALENDAR_ENABLED", False)
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


@patch("src.data.sources.social_feed.TV_SOCIAL_ENABLED", True)
@patch("src.data.sources.social_feed._fetch_tv_json")
def test_tv_social_sentiment_bullish(mock_fetch) -> None:
    import json
    from pathlib import Path

    ideas = json.loads(Path("tests/fixtures/tv_ideas_sample.json").read_text(encoding="utf-8"))
    mock_fetch.side_effect = lambda path, symbol: ideas if path == "ideas" else {"data": {"minds": {"results": []}}}

    summary, posts, refs = fetch_social_sentiment()
    assert refs["source"] == "tradingview_social"
    assert refs["ideas_count"] >= 1
    assert "偏多" in summary or "分歧" in summary or len(posts) >= 1


def test_tv_parse_ideas_and_minds() -> None:
    import json
    from pathlib import Path

    from src.data.sources.social_feed import parse_tv_ideas, parse_tv_minds

    ideas = json.loads(Path("tests/fixtures/tv_ideas_sample.json").read_text(encoding="utf-8"))
    parsed = parse_tv_ideas(ideas)
    assert len(parsed) == 2
    assert parsed[0]["bias_delta"] == 1

    minds_payload = {
        "data": {
            "minds": {
                "results": [
                    {
                        "text_ast": {
                            "type": "root",
                            "children": [{"type": "p", "children": ["Gold long breakout bullish"]}],
                        },
                        "total_likes": 5,
                        "author": {"username": "mind_user"},
                    }
                ]
            }
        }
    }
    minds = parse_tv_minds(minds_payload)
    assert minds[0]["bias_delta"] > 0


@patch("src.data.sources.social.fetch_social_sentiment")
def test_social_source_external(mock_fetch) -> None:
    mock_fetch.return_value = (
        "TV 社区偏多（60% 加权 · 10 条 Ideas/Minds）",
        [{"title": "gold long", "kind": "ideas", "author": "trader", "likes": 10}],
        {"source": "tradingview_social", "bias": "bullish"},
    )
    ext = SocialDataSource().fetch_external()
    assert "TV" in ext.social_sentiment
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
