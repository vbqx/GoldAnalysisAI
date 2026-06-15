"""External data sources — DXY, Jin10 MCP, social (mocked HTTP / TradingView)."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.data.sources.dxy import fetch_dxy_impact
from src.data.sources.fundamentals import FundamentalsDataSource
from src.core.types import CalendarEvent, HeadlineItem
from src.data.sources.jin10_feed import Jin10NewsBundle, fetch_jin10_bundle
from src.data.sources.news import NewsDataSource
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


@patch("src.data.sources.fundamentals.fetch_macro_quotes")
def test_fundamentals_source_uses_dxy(mock_fetch) -> None:
    from src.core.types import MacroQuote

    mock_fetch.return_value = [
        MacroQuote(
            name="DXY",
            symbol="TVC:DXY",
            close=104.2,
            change_pct=0.3,
            impact="偏强 (104.2, 日 +0.30%) → 利空黄金",
            bias="bearish",
        )
    ]
    ext = FundamentalsDataSource().fetch_external()
    assert "利空黄金" in ext.dxy_impact
    items = FundamentalsDataSource().fetch_evidence()
    assert items[0].refs.get("source") == "tradingview"


@patch(
    "src.data.sources.jin10_feed.fetch_jin10_flash",
    return_value=(
        [HeadlineItem(source="jin10_flash", text="2026-06-16 10:00 现货黄金突破4200美元", time="2026-06-16")],
        None,
    ),
)
@patch(
    "src.data.sources.jin10_feed.fetch_jin10_articles",
    return_value=(
        [HeadlineItem(source="jin10_news", text="2026-06-16 09:00 一周展望：黄金等待筑底", time="2026-06-16")],
        None,
    ),
)
@patch(
    "src.data.sources.jin10_feed.fetch_jin10_calendar",
    return_value=(
        [CalendarEvent(time="2026-06-16 20:30", region="美国", event="美国6月CPI年率", importance=3.0)],
        None,
    ),
)
def test_jin10_bundle_flash_articles_calendar(_cal, _articles, _flash) -> None:
    bundle = fetch_jin10_bundle()
    assert "黄金" in bundle.flash[0]
    assert "黄金" in bundle.articles[0]
    assert "CPI" in bundle.risk_events
    assert "jin10_flash" in bundle.sources
    assert "jin10_news" in bundle.sources
    assert "jin10_calendar" in bundle.sources


@patch("src.data.sources.jin10_feed.JIN10_ENABLED", False)
@patch("src.data.sources.jin10_feed.JIN10_API_TOKEN", "")
def test_jin10_bundle_requires_token() -> None:
    bundle = fetch_jin10_bundle()
    assert bundle.headlines == []
    assert "JIN10_API_TOKEN" in str(bundle.errors)


def test_jin10_calendar_filters_gold_events() -> None:
    from src.data.sources.jin10_feed import fetch_jin10_calendar

    rows = {
        "items": [
            {
                "time": "2026-06-16 20:30",
                "country": "美国",
                "event": "美国6月CPI年率",
                "importance": "3",
            },
            {
                "time": "2026-06-16 22:00",
                "country": "美国",
                "event": "NAHB Housing Market Index",
                "importance": "2",
            },
        ]
    }
    with patch("src.data.sources.jin10_feed.jin10_call_tool", return_value=rows):
        with patch("src.data.sources.jin10_feed.JIN10_ENABLED", True):
            with patch("src.data.sources.jin10_feed.JIN10_API_TOKEN", "t"):
                events, err = fetch_jin10_calendar()
    assert err is None
    assert any("CPI" in e.event for e in events)
    assert not any("NAHB" in e.event for e in events)


def test_gold_macro_event_filter() -> None:
    from src.data.sources.gold_relevance import is_gold_macro_event

    assert is_gold_macro_event("美国6月CPI年率", "美国", importance=3)
    assert not is_gold_macro_event("NAHB Housing Market Index", "美国", importance=2)
    assert is_gold_macro_event("中国MLF操作", "中国", importance=2)


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


@patch("src.data.sources.news.fetch_jin10_bundle")
def test_news_source_evidence(mock_bundle) -> None:
    mock_bundle.return_value = Jin10NewsBundle(
        flash=["Gold hits record high"],
        articles=["Weekly gold outlook bullish"],
        flash_items=[HeadlineItem(source="jin10_flash", text="Gold hits record high")],
        article_items=[HeadlineItem(source="jin10_news", text="Weekly gold outlook bullish")],
        calendar_events=[
            CalendarEvent(time="2026-06-16 20:30", region="美国", event="美国6月CPI年率", importance=3.0)
        ],
        risk_events="2026-06-16 20:30 美国 美国6月CPI年率",
        sources=["jin10_flash", "jin10_news", "jin10_calendar"],
    )
    items = NewsDataSource().fetch_evidence()
    assert any("Gold hits" in i.summary for i in items)
    assert any("Weekly gold" in i.summary for i in items)
    assert any("CPI" in i.summary for i in items)


@patch(
    "src.data.sources.jin10_feed.fetch_jin10_flash",
    return_value=([HeadlineItem(source="jin10_flash", text="flash headline")], None),
)
@patch("src.data.sources.jin10_feed.fetch_jin10_articles", return_value=([], "jin10 articles empty"))
@patch("src.data.sources.jin10_feed.fetch_jin10_calendar", return_value=([], None))
def test_news_source_external(_cal, _articles, _flash) -> None:
    ext = NewsDataSource().fetch_external()
    assert ext.news_headlines
    assert "jin10_flash" in ext.sources
