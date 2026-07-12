"""Calendar parsing and filtering — no data-source imports."""

from __future__ import annotations

import re
from datetime import datetime

from src.core.types import CalendarEvent


def parse_event_time(raw: str) -> datetime | None:
    text = (raw or "").strip()
    if not text:
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    match = re.search(r"(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})", text)
    if match:
        try:
            return datetime.strptime(f"{match.group(1)} {match.group(2)}", "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    return None


def filter_upcoming_calendar_events(events: list[CalendarEvent]) -> list[CalendarEvent]:
    """Keep only future (or very recent) events with parseable times."""
    now = datetime.now()
    kept: list[CalendarEvent] = []
    for event in events:
        when = parse_event_time(event.time)
        if when is None:
            continue
        hours = (when - now).total_seconds() / 3600
        if hours >= -1:
            kept.append(event)
    return kept


def calendar_to_risk_text(events: list[CalendarEvent], *, limit: int = 6) -> str:
    if not events:
        return "—"
    return "；".join(e.display() for e in events[:limit])
