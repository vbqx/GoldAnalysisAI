"""Jin10 (金十数据) official MCP client — JSON-RPC over SSE."""

from __future__ import annotations

import json
import time
from typing import Any

import requests

from src.config import (
    JIN10_API_TOKEN,
    JIN10_MCP_PROTOCOL,
    JIN10_MCP_TIMEOUT,
    JIN10_MCP_URL,
)
from src.log import get_logger

log = get_logger(__name__)

_SESSION: dict[str, Any] = {"client": None, "connected_at": 0.0}
_SESSION_TTL_S = 300


def _parse_sse(text: str) -> list[dict[str, Any]]:
    """Parse Jin10 MCP SSE — payload may span multiple physical lines."""
    marker = "data: "
    idx = text.find(marker)
    if idx < 0:
        raise RuntimeError("jin10 MCP: no SSE data field")
    raw = text[idx + len(marker) :].strip()
    # Trim anything after the JSON object (rare trailing SSE noise)
    try:
        rpc = json.loads(raw)
    except json.JSONDecodeError:
        # Multi-line SSE body: reassemble lines until JSON parses
        lines = text[idx + len(marker) :].splitlines()
        buf: list[str] = []
        for line in lines:
            if line.startswith("event:"):
                break
            buf.append(line)
            try:
                rpc = json.loads("".join(buf))
                break
            except json.JSONDecodeError:
                continue
        else:
            raise
    return [{"event": "message", "data": rpc}]


def _pick_data(result: dict[str, Any] | None) -> Any:
    if not result:
        return None
    if result.get("structuredContent") is not None:
        return result["structuredContent"]
    content = result.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str):
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return text
    return result


class Jin10McpClient:
    def __init__(self, *, token: str, url: str = JIN10_MCP_URL, protocol: str = JIN10_MCP_PROTOCOL) -> None:
        self.url = url
        self.token = token
        self.protocol = protocol
        self.session_id: str | None = None
        self._req_id = 0

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        return headers

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    def _post(self, body: dict[str, Any], *, expect_response: bool = True) -> Any:
        last_exc: Exception | None = None
        for attempt in range(2):
            try:
                resp = requests.post(
                    self.url,
                    headers=self._headers(),
                    json=body,
                    timeout=JIN10_MCP_TIMEOUT,
                )
                break
            except requests.RequestException as exc:
                last_exc = exc
                if attempt == 0:
                    time.sleep(0.5)
        else:
            raise RuntimeError(f"jin10 MCP request failed: {last_exc}") from last_exc

        sid = resp.headers.get("mcp-session-id") or resp.headers.get("Mcp-Session-Id")
        if sid:
            self.session_id = sid

        if not expect_response:
            if resp.status_code not in (200, 202):
                raise RuntimeError(f"jin10 MCP HTTP {resp.status_code}: {resp.text[:200]}")
            return None

        if not resp.ok:
            raise RuntimeError(f"jin10 MCP HTTP {resp.status_code}: {resp.text[:400]}")

        ctype = resp.headers.get("content-type", "")
        if "text/event-stream" not in ctype:
            raise RuntimeError(f"jin10 MCP unexpected content-type: {ctype}")

        # Jin10 SSE is UTF-8; requests may mis-detect ISO-8859-1 and mangle CJK in resp.text
        body_text = resp.content.decode("utf-8")
        events = _parse_sse(body_text)
        message = next((e for e in events if e.get("event") == "message"), events[0])
        rpc = message["data"]
        if rpc.get("error"):
            err = rpc["error"]
            raise RuntimeError(f"jin10 MCP error {err.get('code')}: {err.get('message')}")
        return rpc.get("result")

    def connect(self) -> None:
        self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": self.protocol,
                    "capabilities": {},
                    "clientInfo": {"name": "goldAianalysis", "version": "1.0.0"},
                },
            }
        )
        self._post(
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            expect_response=False,
        )

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        result = self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments or {}},
            }
        )
        if isinstance(result, dict) and result.get("isError"):
            raise RuntimeError(f"jin10 tool {name} error: {result}")
        return _pick_data(result)


def get_jin10_client() -> Jin10McpClient:
    if not JIN10_API_TOKEN:
        raise RuntimeError("JIN10_API_TOKEN not set")
    now = time.time()
    cached = _SESSION.get("client")
    if cached and (now - float(_SESSION.get("connected_at") or 0)) < _SESSION_TTL_S:
        return cached  # type: ignore[return-value]
    client = Jin10McpClient(token=JIN10_API_TOKEN)
    client.connect()
    _SESSION["client"] = client
    _SESSION["connected_at"] = now
    return client


def jin10_call_tool(name: str, arguments: dict[str, Any] | None = None) -> Any:
    return get_jin10_client().call_tool(name, arguments)
