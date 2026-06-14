"""News + economic calendar — TE scrape / Finnhub + Google News RSS."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from src.config import FINNHUB_API_KEY, NEWS_RSS_ENABLED, TE_CALENDAR_ENABLED
from src.data.sources._http import get_json, get_text
from src.data.sources.te_calendar_scraper import fetch_te_calendar
from src.log import get_logger

log = get_logger(__name__)

_GOLD_KEYWORDS = (
    "gold",
    "xau",
    "xauusd",
    "fed",
    "federal reserve",
    "inflation",
    "cpi",
    "nfp",
    "powell",
    "dollar",
    "treasury",
    "rate",
    "黄金",
)

_PLACEHOLDER_EVENTS = "美盘数据/讲话 → 波动放大（占位）"


def _matches_gold(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in _GOLD_KEYWORDS)


def _finnhub_news() -> list[str]:
    if not FINNHUB_API_KEY:
        return []
    try:
        data = get_json(
            "https://finnhub.io/api/v1/news",
            params={"category": "general", "token": FINNHUB_API_KEY},
        )
    except Exception as exc:
        log.warning("finnhub news failed: %s", exc)
        return []
    if not isinstance(data, list):
        return []
    headlines: list[str] = []
    for item in data[:30]:
        if not isinstance(item, dict):
            continue
        headline = str(item.get("headline", "")).strip()
        if headline and _matches_gold(headline):
            source = str(item.get("source", "")).strip()
            suffix = f" ({source})" if source else ""
            headlines.append(f"{headline}{suffix}")
    return headlines[:8]


def _finnhub_calendar() -> str:
    if not FINNHUB_API_KEY:
        return "—"
    try:
        today = datetime.now(timezone.utc).date()
        end = today + timedelta(days=2)
        data = get_json(
            "https://finnhub.io/api/v1/calendar/economic",
            params={
                "from": today.isoformat(),
                "to": end.isoformat(),
                "token": FINNHUB_API_KEY,
            },
        )
    except Exception as exc:
        log.warning("finnhub calendar failed (free tier may lack access): %s", exc)
        if "403" in str(exc):
            return "Finnhub 经济日历需付费档（免费 Key 403）"
        return "—"
    events = data.get("economicCalendar") if isinstance(data, dict) else None
    if not isinstance(events, list):
        return "—"

    high: list[str] = []
    for ev in events:
        if not isinstance(ev, dict):
            continue
        impact = str(ev.get("impact", "")).lower()
        country = str(ev.get("country", "")).upper()
        event = str(ev.get("event", "")).strip()
        if not event:
            continue
        if impact in ("high", "3") or (country == "US" and impact in ("medium", "2", "high", "3")):
            t = str(ev.get("time", ""))[:16].replace("T", " ")
            high.append(f"{t} {country} {event}".strip())

    if not high:
        return "近 48h 无高影响美元宏观事件（Finnhub）"
    return "；".join(high[:5])


def _rss_news() -> list[str]:
    if not NEWS_RSS_ENABLED:
        return []
    url = "https://news.google.com/rss/search?q=gold+OR+XAUUSD+OR+Federal+Reserve&hl=en-US&gl=US&ceid=US:en"
    raw = get_text(url)
    root = ET.fromstring(raw)
    headlines: list[str] = []
    for item in root.findall(".//item"):
        title_el = item.find("title")
        if title_el is None or not title_el.text:
            continue
        title = title_el.text.strip()
        if title and _matches_gold(title):
            headlines.append(title)
        if len(headlines) >= 8:
            break
    return headlines


def _economic_calendar() -> tuple[str, str | None]:
    """Return (risk_events text, source tag for refs)."""
    if TE_CALENDAR_ENABLED:
        risk = fetch_te_calendar()
        if risk != "—":
            return risk, "te_calendar_scrape"
        return risk, None

    if FINNHUB_API_KEY:
        risk = _finnhub_calendar()
        if risk != "—":
            return risk, "finnhub_calendar"
        return risk, None

    return "—", None


def fetch_news_bundle() -> tuple[list[str], str, dict]:
    """Return (headlines, risk_events, refs)."""
    refs: dict = {"sources": []}
    headlines: list[str] = []

    try:
        if FINNHUB_API_KEY:
            headlines = _finnhub_news()
            if headlines:
                refs["sources"].append("finnhub_news")

        risk, cal_source = _economic_calendar()
        if cal_source:
            refs["sources"].append(cal_source)

        if not headlines and NEWS_RSS_ENABLED:
            headlines = _rss_news()
            if headlines:
                refs["sources"].append("google_news_rss")

        if risk == "—":
            risk = (
                "关注美盘数据/央行讲话（RSS 模式 · 未配置经济日历）"
                if headlines
                else _PLACEHOLDER_EVENTS
            )

        if not headlines and not FINNHUB_API_KEY and not TE_CALENDAR_ENABLED and not NEWS_RSS_ENABLED:
            refs["source"] = "placeholder"
            return [], _PLACEHOLDER_EVENTS, refs

        refs["headline_count"] = len(headlines)
        refs["source"] = "live" if headlines or refs.get("sources") else "partial"
        return headlines, risk, refs
    except Exception as exc:
        log.warning("news fetch failed: %s", exc)
        return [], _PLACEHOLDER_EVENTS, {"source": "placeholder", "error": str(exc)}
