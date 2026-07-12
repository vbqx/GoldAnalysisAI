"""ExternalFactors legacy string fields — no data-source imports."""

from __future__ import annotations

from src.config import ANALYST_NEWS_MAX
from src.core.types import ExternalFactors, HeadlineItem
from src.data.calendar_utils import calendar_to_risk_text, filter_upcoming_calendar_events
from src.log import get_logger

log = get_logger(__name__)


def headlines_to_strings(items: list[HeadlineItem], *, limit: int | None = None) -> list[str]:
    cap = limit or ANALYST_NEWS_MAX
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = item.text.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text[:240])
        if len(out) >= cap:
            break
    return out


def sync_external_legacy_fields(ext: ExternalFactors) -> None:
    """Keep news_headlines / risk_events in sync with structured fields."""
    if ext.headline_items:
        ext.news_headlines = headlines_to_strings(ext.headline_items)
    upcoming = filter_upcoming_calendar_events(ext.calendar_events)
    dropped = len(ext.calendar_events) - len(upcoming)
    if dropped:
        log.info("calendar filter dropped %d past/unknown events (kept %d)", dropped, len(upcoming))
    ext.risk_events = calendar_to_risk_text(upcoming) if upcoming else "—"
