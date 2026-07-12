"""Stable signal identifiers derived from plan geometry."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_signal_id(signal: dict[str, Any]) -> str:
    """Content-addressed ID — stable across reordering of candidate lists."""
    direction = str(signal.get("direction") or signal.get("theme") or "").upper()
    tps = [round(float(x), 2) for x in (signal.get("take_profits") or []) if x is not None]
    payload = {
        "direction": direction,
        "entry_low": round(float(signal.get("entry_low") or 0), 2),
        "entry_high": round(float(signal.get("entry_high") or 0), 2),
        "stop_loss": round(float(signal.get("stop_loss") or 0), 2),
        "take_profits": tps,
        "setup_type": str(signal.get("setup_type") or ""),
        "timeframe": str(signal.get("timeframe") or signal.get("chart_timeframe") or ""),
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"sig-{digest}"
