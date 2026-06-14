"""Apply system / env HTTP proxy for requests and WebSocket clients."""

from __future__ import annotations

import os


def read_system_proxy() -> str | None:
    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        if val := os.environ.get(key):
            return val

    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        )
        try:
            enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if enable:
                server, _ = winreg.QueryValueEx(key, "ProxyServer")
                server = server.split(";")[0].strip()
                return f"http://{server}" if "://" not in server else server
        finally:
            winreg.CloseKey(key)
    except Exception:
        pass

    return None


def apply_system_proxy() -> str | None:
    """Set http_proxy/https_proxy from env or Windows registry (idempotent)."""
    proxy = read_system_proxy()
    if proxy:
        os.environ.setdefault("http_proxy", proxy)
        os.environ.setdefault("https_proxy", proxy)
    return proxy
