"""Jin10 MCP — flash, articles, macro calendar (structured + legacy strings)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from src.config import (
    ANALYST_CALENDAR_MAX,
    JIN10_API_TOKEN,
    JIN10_ARTICLE_LIMIT,
    JIN10_CACHE_TTL,
    JIN10_ENABLED,
    JIN10_FLASH_LIMIT,
    JIN10_KEYWORD,
    JIN10_KLINE_CODE,
    JIN10_KLINE_COUNT,
    JIN10_KLINE_ENABLED,
    JIN10_KLINE_PERIOD,
    JIN10_NEWS_LIMIT,
    JIN10_QUOTE_CODE,
    JIN10_QUOTE_ENABLED,
)
from src.core.types import CalendarEvent, HeadlineItem
from src.data.sources.gold_relevance import is_gold_macro_event, matches_gold_headline
from src.data.sources.jin10_mcp_client import jin10_call_tool
from src.log import get_logger

log = get_logger(__name__)

_CACHE: dict[str, tuple[float, Any]] = {}


@dataclass
class Jin10NewsBundle:
    flash: list[str] = field(default_factory=list)
    articles: list[str] = field(default_factory=list)
    flash_items: list[HeadlineItem] = field(default_factory=list)
    article_items: list[HeadlineItem] = field(default_factory=list)
    calendar_events: list[CalendarEvent] = field(default_factory=list)
    risk_events: str = "—"
    sources: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def headline_items(self) -> list[HeadlineItem]:
        return self.article_items + self.flash_items

    @property
    def headlines(self) -> list[str]:
        seen: set[str] = set()
        merged: list[str] = []
        for item in self.headline_items:
            text = item.text.strip()
            if not text or text in seen:
                continue
            seen.add(text)
            merged.append(text[:240])
            if len(merged) >= JIN10_NEWS_LIMIT:
                break
        return merged

    @property
    def is_live(self) -> bool:
        return bool(self.sources)


def _cached(key: str, ttl: int, fn: Callable[[], Any]) -> tuple[Any, str | None]:
    if ttl > 0:
        hit = _CACHE.get(key)
        if hit and (time.time() - hit[0]) < ttl:
            return hit[1], None
    try:
        value = fn()
    except Exception as exc:
        log.warning("jin10 %s failed: %s", key, exc)
        return None, str(exc)
    if ttl > 0 and value is not None:
        _CACHE[key] = (time.time(), value)
    return value, None


def _iter_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if not isinstance(data, dict):
        return []
    for key in ("items", "data", "list", "results", "flash_list", "events"):
        block = data.get(key)
        if isinstance(block, list):
            return [x for x in block if isinstance(x, dict)]
        if isinstance(block, dict):
            nested = _iter_rows(block)
            if nested:
                return nested
    return [data]


def _is_relevant(text: str, keyword: str) -> bool:
    return matches_gold_headline(text) or bool(keyword and keyword in text)


def _parse_flash_item(row: dict[str, Any]) -> HeadlineItem:
    content = str(row.get("content") or row.get("title") or row.get("text") or "").strip()
    stamp = str(row.get("time") or row.get("datetime") or row.get("published_at") or "").strip()
    title = str(row.get("title") or "").strip()
    text = f"{stamp} {content}".strip() if stamp and content else content
    return HeadlineItem(
        source="jin10_flash",
        text=text[:240],
        time=stamp,
        title=title or content[:80],
        url=str(row.get("url") or ""),
    )


def _parse_article_item(row: dict[str, Any]) -> HeadlineItem:
    title = str(row.get("title") or "").strip()
    intro = str(row.get("introduction") or row.get("content") or "").strip()
    stamp = str(row.get("time") or row.get("datetime") or "").strip()
    if title and intro and intro not in title:
        body = f"{title} — {intro[:160]}"
    else:
        body = title or intro
    text = f"{stamp} {body}".strip() if stamp and body else body
    return HeadlineItem(
        source="jin10_news",
        text=text[:240],
        time=stamp,
        title=title or body[:80],
        url=str(row.get("url") or ""),
    )


def _parse_calendar_row(row: dict[str, Any]) -> CalendarEvent | None:
    event = str(
        row.get("event")
        or row.get("title")
        or row.get("name")
        or row.get("indicator")
        or row.get("content")
        or ""
    ).strip()
    if not event:
        return None
    region = str(row.get("country") or row.get("region") or row.get("area") or "").strip()
    stamp = str(
        row.get("time")
        or row.get("datetime")
        or row.get("pub_time")
        or row.get("date")
        or ""
    ).strip()
    importance = row.get("importance") or row.get("star") or row.get("level")
    imp = 3.0 if str(importance) in ("3", "high", "高") else 2.0 if str(importance) in ("2", "medium", "中") else 1.0
    if not is_gold_macro_event(event, region, importance=imp):
        return None
    return CalendarEvent(time=stamp, region=region, event=event, importance=imp)


def _collect_items(
    rows: list[dict[str, Any]],
    *,
    parse_fn: Callable[[dict[str, Any]], HeadlineItem],
    keyword: str,
    limit: int,
    fallback: bool,
) -> list[HeadlineItem]:
    items: list[HeadlineItem] = []
    seen: set[str] = set()
    for row in rows:
        item = parse_fn(row)
        if not item.text or item.text in seen:
            continue
        if _is_relevant(item.text, keyword):
            seen.add(item.text)
            items.append(item)
        if len(items) >= limit:
            break
    if not items and fallback and rows:
        for row in rows[:limit]:
            item = parse_fn(row)
            if item.text and item.text not in seen:
                items.append(item)
    return items


def fetch_jin10_flash() -> tuple[list[HeadlineItem], str | None]:
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        return [], "JIN10_API_TOKEN not set"

    keyword = JIN10_KEYWORD.strip()
    cache_key = f"flash:{keyword or 'all'}"

    def _pull() -> Any:
        return jin10_call_tool("list_flash", {})

    data, err = _cached(cache_key, JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return [], err

    items = _collect_items(
        _iter_rows(data),
        parse_fn=_parse_flash_item,
        keyword=keyword,
        limit=JIN10_FLASH_LIMIT,
        fallback=True,
    )
    return items, None if items else (err or "jin10 flash empty")


def fetch_jin10_articles() -> tuple[list[HeadlineItem], str | None]:
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        return [], "JIN10_API_TOKEN not set"

    keyword = JIN10_KEYWORD.strip()
    cache_key = f"articles:{keyword or 'list'}"

    def _pull() -> Any:
        if keyword:
            return jin10_call_tool("search_news", {"keyword": keyword})
        return jin10_call_tool("list_news", {})

    data, err = _cached(cache_key, JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return [], err

    items = _collect_items(
        _iter_rows(data),
        parse_fn=_parse_article_item,
        keyword=keyword,
        limit=JIN10_ARTICLE_LIMIT,
        fallback=not keyword,
    )
    return items, None if items else (err or "jin10 articles empty")


def fetch_jin10_calendar() -> tuple[list[CalendarEvent], str | None]:
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        return [], "JIN10_API_TOKEN not set"

    def _pull() -> Any:
        return jin10_call_tool("list_calendar", {})

    data, err = _cached("calendar", JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return [], err

    events: list[CalendarEvent] = []
    seen: set[str] = set()
    for row in _iter_rows(data):
        ev = _parse_calendar_row(row)
        if not ev:
            continue
        key = ev.display()
        if key in seen:
            continue
        seen.add(key)
        events.append(ev)
        if len(events) >= ANALYST_CALENDAR_MAX:
            break

    if events:
        return events, None
    return [], err or "jin10 calendar no gold-relevant events"


def fetch_jin10_risk_events() -> tuple[str, str | None]:
    events, err = fetch_jin10_calendar()
    if events:
        from src.data.calendar_utils import calendar_to_risk_text, filter_upcoming_calendar_events

        upcoming = filter_upcoming_calendar_events(events)
        if upcoming:
            return calendar_to_risk_text(upcoming), None
    return "—", err


def fetch_jin10_bundle() -> Jin10NewsBundle:
    """Pull flash + articles + calendar in one call."""
    bundle = Jin10NewsBundle()
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        bundle.errors.append("JIN10_API_TOKEN not configured (https://mcp.jin10.com/app)")
        return bundle

    flash_items, flash_err = fetch_jin10_flash()
    if flash_err:
        bundle.errors.append(f"jin10_flash: {flash_err}")
    if flash_items:
        bundle.flash_items = flash_items
        bundle.flash = [i.text for i in flash_items]
        bundle.sources.append("jin10_flash")

    article_items, article_err = fetch_jin10_articles()
    if article_err:
        bundle.errors.append(f"jin10_news: {article_err}")
    if article_items:
        bundle.article_items = article_items
        bundle.articles = [i.text for i in article_items]
        bundle.sources.append("jin10_news")

    calendar, cal_err = fetch_jin10_calendar()
    if cal_err:
        bundle.errors.append(f"jin10_calendar: {cal_err}")
    if calendar:
        from src.data.calendar_utils import calendar_to_risk_text, filter_upcoming_calendar_events

        upcoming = filter_upcoming_calendar_events(calendar)
        bundle.calendar_events = upcoming
        bundle.risk_events = calendar_to_risk_text(upcoming) if upcoming else "—"
        bundle.sources.append("jin10_calendar")

    return bundle


fetch_jin10_headlines = fetch_jin10_flash


def fetch_jin10_quote(code: str | None = None) -> tuple[dict[str, Any] | None, str | None]:
    """XAUUSD spot quote via Jin10 MCP get_quote (cached)."""
    if not JIN10_QUOTE_ENABLED or not JIN10_ENABLED or not JIN10_API_TOKEN:
        return None, "JIN10 quote disabled"

    symbol = (code or JIN10_QUOTE_CODE).strip() or "XAUUSD"
    cache_key = f"quote:{symbol}"

    def _pull() -> Any:
        return jin10_call_tool("get_quote", {"code": symbol})

    data, err = _cached(cache_key, JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return None, err
    if isinstance(data, dict) and data.get("data"):
        inner = data["data"]
        if isinstance(inner, dict):
            return inner, None
        return data, None
    return None, err or "jin10 quote empty"


def _normalize_kline_bars(data: Any) -> list[dict[str, Any]]:
    rows = _iter_rows(data)
    bars: list[dict[str, Any]] = []
    for row in rows:
        close = row.get("close") or row.get("c") or row.get("price")
        if close is None:
            continue
        try:
            close_f = float(close)
        except (TypeError, ValueError):
            continue
        bars.append(
            {
                "time": row.get("time") or row.get("datetime") or row.get("t") or "",
                "open": row.get("open") or row.get("o"),
                "high": row.get("high") or row.get("h"),
                "low": row.get("low") or row.get("l"),
                "close": close_f,
                "volume": row.get("volume") or row.get("v"),
            }
        )
    return bars


def fetch_jin10_kline(
    code: str | None = None,
    *,
    period: str | None = None,
    count: int | None = None,
) -> tuple[list[dict[str, Any]], str | None]:
    """XAUUSD K-line via Jin10 MCP get_kline (cached).

    MCP accepts ``code`` + ``count``; optional integer ``time`` via ``JIN10_KLINE_PERIOD``.
    Do not pass string periods like ``"1m"`` — the API expects an integer when ``time`` is set.
    """
    if not JIN10_KLINE_ENABLED or not JIN10_ENABLED or not JIN10_API_TOKEN:
        return [], "JIN10 kline disabled"

    symbol = (code or JIN10_KLINE_CODE).strip() or "XAUUSD"
    bar_count = count or JIN10_KLINE_COUNT
    period = JIN10_KLINE_PERIOD
    cache_key = f"kline:{symbol}:{period or 'default'}:{bar_count}"

    def _pull() -> Any:
        args: dict[str, Any] = {"code": symbol, "count": bar_count}
        if period is not None:
            args["time"] = period
        return jin10_call_tool("get_kline", args)

    data, err = _cached(cache_key, JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return [], err
    if isinstance(data, dict) and data.get("data"):
        inner = data["data"]
        bars = _normalize_kline_bars(inner)
        return bars, None if bars else (err or "jin10 kline empty")
    bars = _normalize_kline_bars(data)
    return bars, None if bars else (err or "jin10 kline empty")
