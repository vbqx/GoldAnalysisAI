"""Data freshness / as-of contract for reports and analyst inputs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.log import get_logger

log = get_logger(__name__)

_STALE_BAR_HOURS = 36.0
_FRESH_BAR_HOURS = 4.0


def _bar_timestamp(df: pd.DataFrame | None) -> datetime | None:
    if df is None or df.empty:
        return None
    ts = df.index[-1]
    if not isinstance(ts, pd.Timestamp):
        return None
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    return ts.to_pydatetime()


def build_data_as_of(
    raw: dict[str, pd.DataFrame],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Summarize bar freshness and whether prices are safe to treat as live."""
    now = now or datetime.now(timezone.utc)
    exec_df = raw.get("5m")
    if exec_df is None or exec_df.empty:
        exec_df = raw.get("1h")
    if exec_df is None or exec_df.empty:
        exec_df = raw.get("1d")
    last_bar = _bar_timestamp(exec_df)
    age_hours: float | None = None
    if last_bar is not None:
        ref = last_bar if last_bar.tzinfo else last_bar.replace(tzinfo=timezone.utc)
        age_hours = (now - ref).total_seconds() / 3600.0

    market_status = "open"
    warnings: list[str] = []
    if now.weekday() >= 5:
        market_status = "closed_snapshot"
        warnings.append("周末闭市：报告基于最近可用 K 线快照，非实时可执行价。")
    elif age_hours is not None and age_hours > _STALE_BAR_HOURS:
        market_status = "closed_snapshot"
        label = last_bar.strftime("%Y-%m-%d %H:%M UTC") if last_bar else "—"
        warnings.append(f"行情已滞后约 {age_hours:.0f} 小时（末根 K 线 {label}），请勿按现价即时执行。")

    executable = (
        market_status == "open"
        and age_hours is not None
        and age_hours <= _FRESH_BAR_HOURS
    )

    payload = {
        "as_of_utc": now.strftime("%Y-%m-%d %H:%M UTC"),
        "last_bar_time_utc": last_bar.strftime("%Y-%m-%d %H:%M UTC") if last_bar else None,
        "data_age_hours": round(age_hours, 1) if age_hours is not None else None,
        "market_status": market_status,
        "executable": executable,
        "warnings": warnings,
    }
    log.info(
        "data_as_of status=%s executable=%s age_h=%s warnings=%d",
        market_status,
        executable,
        payload["data_age_hours"],
        len(warnings),
    )
    return payload
