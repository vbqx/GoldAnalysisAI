"""Quick live fetch smoke test for external data sources."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.aggregator import merge_external
from src.data.sources.dxy import fetch_dxy_impact
from src.data.sources.fundamentals import FundamentalsDataSource
from src.data.sources.news import NewsDataSource
from src.data.sources.news_feed import fetch_news_bundle
from src.data.sources.social import SocialDataSource
from src.data.sources.social_feed import fetch_social_sentiment
from src.data.sources.te_calendar_scraper import fetch_te_calendar


def _block(title: str, body: object) -> None:
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)
    if isinstance(body, (dict, list)):
        print(json.dumps(body, ensure_ascii=False, indent=2))
    else:
        print(body)


def main() -> int:
    print("Live external data fetch test\n")

    dxy_impact, dxy_refs = fetch_dxy_impact()
    _block("DXY (TradingView)", {"impact": dxy_impact, "refs": dxy_refs})

    headlines, risk, news_refs = fetch_news_bundle()
    _block(
        "News bundle",
        {
            "headlines": headlines[:5],
            "headline_count": len(headlines),
            "risk_events": risk,
            "refs": news_refs,
        },
    )

    te_cal = fetch_te_calendar()
    _block("TE calendar scrape", te_cal)

    social_summary, posts, social_refs = fetch_social_sentiment()
    _block(
        "Social (TradingView Ideas/Minds)",
        {
            "summary": social_summary,
            "posts": posts[:3],
            "refs": social_refs,
        },
    )

    merged = merge_external(
        NewsDataSource().fetch_external(),
        FundamentalsDataSource().fetch_external(),
        SocialDataSource().fetch_external(),
    )
    _block(
        "Merged ExternalFactors",
        {
            "dxy_impact": merged.dxy_impact,
            "news_headlines": merged.news_headlines[:3],
            "risk_events": merged.risk_events,
            "social_sentiment": merged.social_sentiment,
        },
    )

    ok = sum(
        1
        for flag in (
            dxy_refs.get("source") == "tradingview",
            bool(headlines) or news_refs.get("sources"),
            te_cal and te_cal != "—",
            social_refs.get("source") == "tradingview_social",
        )
        if flag
    )
    print(f"\n{'=' * 60}")
    print(f"Summary: {ok}/4 sources returned live data")
    return 0 if ok >= 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
