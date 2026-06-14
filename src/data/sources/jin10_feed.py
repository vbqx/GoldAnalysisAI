"""Jin10 MCP — flash, articles, macro calendar."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from src.config import (
    JIN10_API_TOKEN,
    JIN10_ARTICLE_LIMIT,
    JIN10_CACHE_TTL,
    JIN10_ENABLED,
    JIN10_FLASH_LIMIT,
    JIN10_KEYWORD,
    JIN10_NEWS_LIMIT,
)
from src.data.sources.gold_relevance import is_gold_macro_event, matches_gold_headline
from src.data.sources.jin10_mcp_client import jin10_call_tool
from src.log import get_logger

log = get_logger(__name__)

_CACHE: dict[str, tuple[float, Any]] = {}


@dataclass
class Jin10NewsBundle:
    flash: list[str] = field(default_factory=list)
    articles: list[str] = field(default_factory=list)
    risk_events: str = "—"
    sources: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def headlines(self) -> list[str]:
        seen: set[str] = set()
        merged: list[str] = []
        for text in self.articles + self.flash:
            if not text or text in seen:
                continue
            seen.add(text)
            merged.append(text)
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


def _flash_text(row: dict[str, Any]) -> str:
    content = str(row.get("content") or row.get("title") or row.get("text") or "").strip()
    stamp = str(row.get("time") or row.get("datetime") or row.get("published_at") or "").strip()
    if stamp and content:
        return f"{stamp} {content}".strip()
    return content


def _article_text(row: dict[str, Any]) -> str:
    title = str(row.get("title") or "").strip()
    intro = str(row.get("introduction") or row.get("content") or "").strip()
    stamp = str(row.get("time") or row.get("datetime") or "").strip()
    if title and intro and intro not in title:
        body = f"{title} — {intro[:160]}"
    else:
        body = title or intro
    if stamp and body:
        return f"{stamp} {body}".strip()
    return body


def _calendar_line(row: dict[str, Any]) -> str:
    event = str(
        row.get("event")
        or row.get("title")
        or row.get("name")
        or row.get("indicator")
        or row.get("content")
        or ""
    ).strip()
    if not event:
        return ""
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
        return ""
    return f"{stamp} {region} {event}".strip()


def _collect_headlines(
    rows: list[dict[str, Any]],
    *,
    text_fn: Callable[[dict[str, Any]], str],
    keyword: str,
    limit: int,
    fallback: bool,
) -> list[str]:
    headlines: list[str] = []
    seen: set[str] = set()
    for row in rows:
        text = text_fn(row)
        if not text or text in seen:
            continue
        if _is_relevant(text, keyword):
            seen.add(text)
            headlines.append(text[:240])
        if len(headlines) >= limit:
            break
    if not headlines and fallback and rows:
        for row in rows[:limit]:
            text = text_fn(row)
            if text and text not in seen:
                headlines.append(text[:240])
    return headlines


def fetch_jin10_flash() -> tuple[list[str], str | None]:
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        return [], "JIN10_API_TOKEN not set"

    keyword = JIN10_KEYWORD.strip()
    cache_key = f"flash:{keyword or 'all'}"

    def _pull() -> Any:
        return jin10_call_tool("list_flash", {})

    data, err = _cached(cache_key, JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return [], err

    headlines = _collect_headlines(
        _iter_rows(data),
        text_fn=_flash_text,
        keyword=keyword,
        limit=JIN10_FLASH_LIMIT,
        fallback=True,
    )
    return headlines, None if headlines else (err or "jin10 flash empty")


def fetch_jin10_articles() -> tuple[list[str], str | None]:
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

    headlines = _collect_headlines(
        _iter_rows(data),
        text_fn=_article_text,
        keyword=keyword,
        limit=JIN10_ARTICLE_LIMIT,
        fallback=not keyword,
    )
    return headlines, None if headlines else (err or "jin10 articles empty")


def fetch_jin10_risk_events() -> tuple[str, str | None]:
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        return "—", "JIN10_API_TOKEN not set"

    def _pull() -> Any:
        return jin10_call_tool("list_calendar", {})

    data, err = _cached("calendar", JIN10_CACHE_TTL, _pull)
    if err and data is None:
        return "—", err

    lines: list[str] = []
    seen: set[str] = set()
    for row in _iter_rows(data):
        line = _calendar_line(row)
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
        if len(lines) >= 8:
            break

    if lines:
        return "；".join(lines[:6]), None
    return "—", err or "jin10 calendar no gold-relevant events"


def fetch_jin10_bundle() -> Jin10NewsBundle:
    """Pull flash + articles + calendar in one call."""
    bundle = Jin10NewsBundle()
    if not JIN10_ENABLED or not JIN10_API_TOKEN:
        bundle.errors.append("JIN10_API_TOKEN not configured (https://mcp.jin10.com/app)")
        return bundle

    flash, flash_err = fetch_jin10_flash()
    if flash_err:
        bundle.errors.append(f"jin10_flash: {flash_err}")
    if flash:
        bundle.flash = flash
        bundle.sources.append("jin10_flash")

    articles, article_err = fetch_jin10_articles()
    if article_err:
        bundle.errors.append(f"jin10_news: {article_err}")
    if articles:
        bundle.articles = articles
        bundle.sources.append("jin10_news")

    risk, cal_err = fetch_jin10_risk_events()
    if cal_err:
        bundle.errors.append(f"jin10_calendar: {cal_err}")
    if risk != "—":
        bundle.risk_events = risk
        bundle.sources.append("jin10_calendar")

    return bundle


# Backward-compatible aliases
fetch_jin10_headlines = fetch_jin10_flash
