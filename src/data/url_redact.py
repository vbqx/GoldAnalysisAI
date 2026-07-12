"""Redact secrets from URLs before logging."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse


def redact_url(url: str) -> str:
    """Strip userinfo and query params; keep scheme, host, port."""
    if not url:
        return url
    parsed = urlparse(url.strip())
    host = parsed.hostname or ""
    if parsed.port:
        host = f"{host}:{parsed.port}"
    netloc = host
    return urlunparse((parsed.scheme or "http", netloc, "", "", "", ""))
