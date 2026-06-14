"""Economic calendar via Trading Economics HTML scrape (free, no API key).

The calendar page exposes event rows in server HTML when ``calendar-range`` /
``calendar-importance`` cookies are set — no paid API or browser automation.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone

from bs4 import BeautifulSoup

import requests

from src.config import (
    EXTERNAL_HTTP_RETRIES,
    EXTERNAL_HTTP_TIMEOUT,
    TE_CALENDAR_COUNTRY,
    TE_CALENDAR_DAYS,
    TE_CALENDAR_ENABLED,
    TE_CALENDAR_MIN_IMPORTANCE,
)
from src.log import get_logger

log = get_logger(__name__)

_TE_CALENDAR_URL = "https://tradingeconomics.com/calendar"
_DATE_CLASS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_COUNTRY_COOKIE: dict[str, str] = {
    "united states": "usa",
    "us": "usa",
    "usa": "usa",
    "china": "chn",
    "euro area": "emu",
    "european union": "eun",
    "united kingdom": "gbr",
    "japan": "jpn",
    "germany": "deu",
    "france": "fra",
    "canada": "can",
    "australia": "aus",
}


def _country_cookie_slug(country: str) -> str:
    key = country.strip().lower()
    if key in _COUNTRY_COOKIE:
        return _COUNTRY_COOKIE[key]
    if len(key) == 3 and key.isalpha():
        return key
    return key.replace(" ", "")[:3]


def _range_cookie(days: int) -> str:
    if days <= 1:
        return "1"
    if days == 2:
        return "2"
    if days <= 7:
        return "3"
    if days <= 14:
        return "4"
    return "5"


def _parse_row(row) -> dict | None:
    event_el = row.select_one("a.calendar-event")
    event = (event_el.get_text(" ", strip=True) if event_el else "").strip()
    if not event:
        event = str(row.get("data-event") or "").strip().title()
    if not event:
        return None

    country = str(row.get("data-country") or "").strip()
    if not country:
        iso = row.select_one(".calendar-iso")
        country = iso.get_text(strip=True) if iso else ""

    time_cell = row.find("td")
    event_date: date | None = None
    event_time = ""
    if time_cell:
        for cls in time_cell.get("class") or []:
            if _DATE_CLASS_RE.match(cls):
                event_date = date.fromisoformat(cls)
                break
        event_time = time_cell.get_text(" ", strip=True)

    importance = 0
    if time_cell:
        span = time_cell.select_one("[class*='calendar-date-']")
        if span:
            for cls in span.get("class") or []:
                m = re.search(r"calendar-date-(\d)", cls)
                if m:
                    importance = int(m.group(1))
                    break

    ref = row.select_one(".calendar-reference")
    if ref:
        ref_txt = ref.get_text(strip=True)
        if ref_txt:
            event = f"{event} {ref_txt}"

    return {
        "date": event_date,
        "time": event_time,
        "country": country,
        "event": event,
        "importance": importance,
    }


def _format_event(ev: dict) -> str:
    parts: list[str] = []
    if ev.get("date"):
        parts.append(ev["date"].isoformat())
    if ev.get("time"):
        parts.append(ev["time"])
    if ev.get("country"):
        parts.append(ev["country"])
    parts.append(ev["event"])
    return " ".join(parts).strip()


def _is_relevant(ev: dict, *, today: date, horizon: date, min_importance: int) -> bool:
    ev_date = ev.get("date")
    if ev_date is None or ev_date < today or ev_date > horizon:
        return False
    importance = int(ev.get("importance") or 0)
    if importance >= min_importance:
        return True
    country = str(ev.get("country") or "").lower()
    return country in ("united states", "us", "usa") and importance >= max(1, min_importance - 1)


def scrape_te_calendar_html(html: str, *, today: date | None = None, days: int = 2, min_importance: int = 2) -> list[dict]:
    """Parse calendar rows from TE HTML."""
    today = today or datetime.now(timezone.utc).date()
    horizon = today + timedelta(days=max(1, days))
    soup = BeautifulSoup(html, "lxml")
    events: list[dict] = []
    for row in soup.select("tr[data-id]"):
        ev = _parse_row(row)
        if ev and _is_relevant(ev, today=today, horizon=horizon, min_importance=min_importance):
            events.append(ev)
    events.sort(key=lambda e: (e.get("date") or today, e.get("time") or ""))
    return events


def fetch_te_calendar() -> str:
    """Return risk_events text for the next TE_CALENDAR_DAYS days."""
    if not TE_CALENDAR_ENABLED:
        return "—"

    country_slug = _country_cookie_slug(TE_CALENDAR_COUNTRY)
    cookies = {
        "calendar-range": _range_cookie(TE_CALENDAR_DAYS),
        "calendar-importance": str(max(1, min(3, TE_CALENDAR_MIN_IMPORTANCE))),
        "calendar-countries": country_slug,
    }
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    html = ""
    last_exc: Exception | None = None
    attempts = EXTERNAL_HTTP_RETRIES + 1
    for attempt in range(attempts):
        try:
            resp = requests.get(
                _TE_CALENDAR_URL,
                headers=headers,
                cookies=cookies,
                timeout=EXTERNAL_HTTP_TIMEOUT,
            )
            resp.raise_for_status()
            html = resp.text
            break
        except requests.RequestException as exc:
            last_exc = exc
            log.warning(
                "TE calendar scrape failed attempt %d/%d: %s",
                attempt + 1,
                attempts,
                exc,
            )
    else:
        log.warning("Trading Economics calendar scrape failed: %s", last_exc)
        return "—"

    today = datetime.now(timezone.utc).date()
    events = scrape_te_calendar_html(
        html,
        today=today,
        days=TE_CALENDAR_DAYS,
        min_importance=TE_CALENDAR_MIN_IMPORTANCE,
    )
    if not events:
        return f"近 {TE_CALENDAR_DAYS} 天无高影响宏观事件（Trading Economics 抓取）"

    lines = [_format_event(ev) for ev in events[:8]]
    return "；".join(lines[:5])
