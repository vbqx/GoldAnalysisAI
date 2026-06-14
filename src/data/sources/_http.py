"""Shared HTTP helpers for external data sources."""

from __future__ import annotations

import json
import time
from typing import Any

import requests

from src.config import EXTERNAL_HTTP_RETRIES, EXTERNAL_HTTP_TIMEOUT
from src.log import get_logger

log = get_logger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": "GoldAnalysisAI/1.0 (+https://github.com/vbqx/GoldAnalysisAI)",
    "Accept": "application/json, application/xml, text/xml, */*",
}


def get_json(url: str, *, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> Any:
    return json.loads(get_text(url, params=params, headers=headers))


def get_text(url: str, *, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> str:
    merged = {**DEFAULT_HEADERS, **(headers or {})}
    last_exc: Exception | None = None
    attempts = EXTERNAL_HTTP_RETRIES + 1

    for attempt in range(attempts):
        try:
            resp = requests.get(
                url,
                params=params,
                headers=merged,
                timeout=EXTERNAL_HTTP_TIMEOUT,
            )
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            last_exc = exc
            log.warning("HTTP GET failed %s attempt %d/%d: %s", url, attempt + 1, attempts, exc)
            if attempt < attempts - 1:
                time.sleep(1.0 * (attempt + 1))

    raise RuntimeError(f"HTTP GET failed for {url}: {last_exc}") from last_exc
