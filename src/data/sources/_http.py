"""Shared HTTP helpers for external data sources."""

from __future__ import annotations

import json
import time
from typing import Any

import requests

from src.config import EXTERNAL_HTTP_RETRIES, EXTERNAL_HTTP_TIMEOUT
from src.data.proxy_env import apply_system_proxy
from src.log import get_logger

log = get_logger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, application/xml, text/xml, text/html, */*",
}

# Ensure proxy env is set before any external HTTP (same as TradingView K-line path).
apply_system_proxy()


def post_json(
    url: str,
    *,
    body: dict[str, Any] | list[Any],
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int | None = None,
) -> Any:
    merged = {**DEFAULT_HEADERS, **(headers or {})}
    merged.setdefault("Content-Type", "application/json")
    last_exc: Exception | None = None
    attempts = EXTERNAL_HTTP_RETRIES + 1
    req_timeout = timeout if timeout is not None else EXTERNAL_HTTP_TIMEOUT

    for attempt in range(attempts):
        try:
            resp = requests.post(
                url,
                params=params,
                json=body,
                headers=merged,
                timeout=req_timeout,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            last_exc = exc
            log.warning("HTTP POST failed %s attempt %d/%d: %s", url, attempt + 1, attempts, exc)
            if attempt < attempts - 1:
                time.sleep(1.0 * (attempt + 1))

    raise RuntimeError(f"HTTP POST failed for {url}: {last_exc}") from last_exc


def get_json(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    cookies: dict[str, str] | None = None,
) -> Any:
    return json.loads(get_text(url, params=params, headers=headers, cookies=cookies))


def get_text(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    cookies: dict[str, str] | None = None,
) -> str:
    merged = {**DEFAULT_HEADERS, **(headers or {})}
    last_exc: Exception | None = None
    attempts = EXTERNAL_HTTP_RETRIES + 1

    for attempt in range(attempts):
        try:
            resp = requests.get(
                url,
                params=params,
                headers=merged,
                cookies=cookies,
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
