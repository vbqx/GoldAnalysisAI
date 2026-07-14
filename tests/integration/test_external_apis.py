"""Live API smoke tests — Jin10 MCP / DXY / Social (requires network + credentials).

Run:
    python tests/run.py --external
    pytest tests/integration/test_external_apis.py -v -m external_api
"""

from __future__ import annotations

import pytest

from src.config import JIN10_API_TOKEN, JIN10_ENABLED, TV_SOCIAL_ENABLED
from src.data.aggregator import merge_external
from src.data.sources.dxy import fetch_dxy_impact
from src.data.sources.fundamentals import FundamentalsDataSource
from src.data.sources.jin10_feed import fetch_jin10_bundle
from src.data.sources.news import NewsDataSource
from src.data.sources.social import SocialDataSource
from src.data.sources.social_feed import fetch_social_sentiment

pytestmark = [pytest.mark.integration, pytest.mark.slow, pytest.mark.external_api]


def _skip_if_placeholder(source: str, refs: dict, label: str) -> None:
    if source == "placeholder" or refs.get("source") == "placeholder":
        pytest.skip(f"{label} unavailable: {refs.get('error', refs.get('errors'))}")


@pytest.mark.external_api
def test_live_dxy_tradingview() -> None:
    """DXY daily snapshot via TradingView TVC:DXY."""
    impact, refs = fetch_dxy_impact()
    _skip_if_placeholder("tradingview", refs, "DXY")

    assert refs["source"] == "tradingview"
    assert refs.get("close", 0) > 50
    assert refs.get("bias") in ("bullish", "bearish", "neutral")
    assert any(k in impact for k in ("利空黄金", "利好黄金", "影响有限", "中性"))


@pytest.mark.external_api
@pytest.mark.skipif(not JIN10_ENABLED or not JIN10_API_TOKEN, reason="JIN10_API_TOKEN not set")
def test_live_jin10_news_bundle() -> None:
    """Flash + articles + calendar from Jin10 official MCP.

    Empty calendar windows are healthy: risk_events may be "—" when no events.
    """
    bundle = fetch_jin10_bundle()

    if not bundle.sources and not bundle.headlines:
        pytest.skip(f"Jin10 MCP failed: {bundle.errors}")

    assert (
        "jin10_flash" in bundle.sources
        or "jin10_news" in bundle.sources
        or "jin10_calendar" in bundle.sources
    )
    # Separate feed health from "there are calendar events today".
    has_flash_or_news = bool(bundle.headlines) or bool(bundle.flash) or bool(bundle.articles)
    assert has_flash_or_news or "jin10_calendar" in bundle.sources

    if bundle.calendar_events:
        assert bundle.risk_events and bundle.risk_events != "—"
    else:
        # Legitimate empty window — placeholder risk text is OK.
        assert bundle.risk_events is not None

    ext = NewsDataSource().fetch_external()
    assert (
        ext.news_headlines
        or (ext.risk_events and ext.risk_events != "—")
        or "jin10_calendar" in (ext.sources or [])
        or "jin10_flash" in (ext.sources or [])
        or "jin10_news" in (ext.sources or [])
    )


@pytest.mark.external_api
@pytest.mark.skipif(not TV_SOCIAL_ENABLED, reason="TV_SOCIAL_ENABLED=false")
def test_live_tradingview_social_sentiment() -> None:
    """TradingView Ideas + Minds community sentiment for XAUUSD."""
    summary, posts, refs = fetch_social_sentiment()

    if refs.get("source") in ("placeholder", "disabled"):
        pytest.skip(f"TV social unavailable: {refs.get('error', refs.get('source'))}")

    assert refs["source"] == "tradingview_social"
    assert refs.get("post_count", 0) > 0
    assert summary and summary != "—"
    assert "TV" in summary


@pytest.mark.external_api
def test_live_data_sources_fetch_external() -> None:
    """DataSource wrappers return mergeable ExternalFactors."""
    news = NewsDataSource().fetch_external()
    fund = FundamentalsDataSource().fetch_external()
    social = SocialDataSource().fetch_external()
    merged = merge_external(news, fund, social)

    live_count = sum(
        1
        for ok in (
            fund.dxy_impact != "—" and "占位" not in fund.dxy_impact,
            bool(news.news_headlines),
            news.risk_events != "—" and "占位" not in news.risk_events,
            social.social_sentiment != "—",
        )
        if ok
    )

    if live_count == 0:
        pytest.skip("no live external data (Jin10 MCP / TV unavailable)")

    assert merged.dxy_impact != "—" or merged.news_headlines or merged.risk_events != "—"
