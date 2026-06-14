"""Live API smoke tests — News / DXY / Social (requires network + proxy if needed).

Run:
    python tests/run.py --external
    pytest tests/integration/test_external_apis.py -v -m external_api
"""

from __future__ import annotations

import pytest

from src.config import FINNHUB_API_KEY, NEWS_RSS_ENABLED, TE_CALENDAR_ENABLED, TV_SOCIAL_ENABLED
from src.data.aggregator import merge_external
from src.data.sources.dxy import fetch_dxy_impact
from src.data.sources.fundamentals import FundamentalsDataSource
from src.data.sources.news import NewsDataSource
from src.data.sources.news_feed import fetch_news_bundle
from src.data.sources.social import SocialDataSource
from src.data.sources.social_feed import fetch_social_sentiment

pytestmark = [pytest.mark.integration, pytest.mark.slow, pytest.mark.external_api]


def _skip_if_placeholder(source: str, refs: dict, label: str) -> None:
    if source == "placeholder" or refs.get("source") == "placeholder":
        pytest.skip(f"{label} unavailable: {refs.get('error', 'placeholder')}")


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
def test_live_news_bundle_rss_or_finnhub() -> None:
    """Headlines from Finnhub (if key) and/or Google News RSS; risk_events non-empty."""
    headlines, risk, refs = fetch_news_bundle()

    has_finnhub = bool(FINNHUB_API_KEY)
    has_rss = NEWS_RSS_ENABLED

    if not has_finnhub and not has_rss:
        pytest.skip("FINNHUB_API_KEY empty and NEWS_RSS_ENABLED=false")

    if refs.get("source") == "placeholder" and not headlines:
        pytest.skip(f"news fetch failed: {refs.get('error', 'placeholder')}")

    assert risk and risk != "—"
    assert refs.get("source") in ("live", "partial")

    if headlines:
        assert len(headlines) >= 1
        assert all(isinstance(h, str) and h.strip() for h in headlines)
        if has_rss and not has_finnhub:
            assert "google_news_rss" in refs.get("sources", [])
    elif has_finnhub:
        assert "finnhub" in str(refs.get("sources")) or "finnhub_calendar" in str(
            refs.get("sources")
        )


@pytest.mark.external_api
@pytest.mark.skipif(not TE_CALENDAR_ENABLED, reason="TE_CALENDAR_ENABLED=false")
def test_live_te_calendar_scrape() -> None:
    """Trading Economics calendar via HTML scrape (no paid API)."""
    from src.data.sources.te_calendar_scraper import fetch_te_calendar

    risk = fetch_te_calendar()
    assert isinstance(risk, str)
    assert risk.strip()
    assert risk != "—"


@pytest.mark.external_api
@pytest.mark.skipif(not FINNHUB_API_KEY, reason="FINNHUB_API_KEY not set")
def test_live_finnhub_economic_calendar() -> None:
    """Finnhub calendar fallback — only when TE scrape disabled."""
    from src.config import TE_CALENDAR_ENABLED
    from src.data.sources.news_feed import _finnhub_calendar

    if TE_CALENDAR_ENABLED:
        pytest.skip("TE calendar scrape enabled; Finnhub calendar is fallback only")

    risk = _finnhub_calendar()
    assert isinstance(risk, str)
    assert risk.strip()
    if "403" in risk or "付费" in risk:
        pytest.skip("Finnhub calendar not available on free tier")
    assert risk != "—"


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
        pytest.skip("no live external data (TV/Finnhub/RSS/TE calendar all unavailable)")

    assert merged.dxy_impact != "—" or merged.news_headlines or merged.risk_events != "—"
