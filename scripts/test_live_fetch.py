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
from src.data.sources.jin10_feed import fetch_jin10_bundle
from src.data.sources.news import NewsDataSource
from src.data.sources.social import SocialDataSource
from src.data.sources.social_feed import fetch_social_sentiment


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

    bundle = fetch_jin10_bundle()
    _block(
        "Jin10 MCP (flash + articles + calendar)",
        {
            "flash": bundle.flash[:3],
            "articles": bundle.articles[:3],
            "headlines_merged": bundle.headlines[:5],
            "headline_count": len(bundle.headlines),
            "risk_events": bundle.risk_events,
            "sources": bundle.sources,
            "errors": bundle.errors,
        },
    )

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
            "sources": merged.sources,
        },
    )

    ok = sum(
        1
        for flag in (
            dxy_refs.get("source") == "tradingview",
            bool(bundle.headlines) or bool(bundle.sources),
            bundle.risk_events != "—" and "占位" not in bundle.risk_events,
            social_refs.get("source") == "tradingview_social",
        )
        if flag
    )
    print(f"\n{'=' * 60}")
    print(f"Summary: {ok}/4 sources returned live data")
    return 0 if ok >= 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
