"""OpenAI-compatible chat completion client (requests-based)."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError, RequestException, Timeout

from src.log import get_logger

log = get_logger(__name__)


class LLMClientError(RuntimeError):
    pass


class LLMClient:
    """Minimal client for /v1/chat/completions (OpenAI, DeepSeek, Ollama, etc.)."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        timeout: int | float | None = None,
        connect_timeout: float | None = None,
        read_timeout: float | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        from src.config import LLM_CONNECT_TIMEOUT, LLM_READ_TIMEOUT

        if connect_timeout is not None:
            self.connect_timeout = float(connect_timeout)
        elif timeout is not None:
            self.connect_timeout = min(30.0, float(timeout))
        else:
            self.connect_timeout = LLM_CONNECT_TIMEOUT

        if read_timeout is not None:
            self.read_timeout = float(read_timeout)
        elif timeout is not None:
            self.read_timeout = float(timeout)
        else:
            self.read_timeout = LLM_READ_TIMEOUT

    @property
    def timeout(self) -> float:
        """Legacy alias — returns read/chunk-idle timeout."""
        return self.read_timeout

    def _request_timeout(self) -> tuple[float, float]:
        return (self.connect_timeout, self.read_timeout)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _parse_sse_line(self, line: str) -> str | None:
        line = line.strip()
        if not line.startswith("data:"):
            return None
        payload = line[5:].strip()
        if payload == "[DONE]":
            return None
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return None
        try:
            delta = data["choices"][0].get("delta") or {}
            content = delta.get("content")
        except (KeyError, IndexError, TypeError):
            return None
        if isinstance(content, str) and content:
            return content
        return None

    def chat_stream(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        response_format: dict[str, str] | None = None,
    ) -> Iterator[str]:
        """Yield text chunks from an OpenAI-compatible SSE stream."""
        url = f"{self.base_url}/chat/completions"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if response_format:
            payload["response_format"] = response_format

        log.debug(
            "llm stream model=%s url=%s connect=%.1fs read_idle=%.1fs",
            self.model,
            url,
            self.connect_timeout,
            self.read_timeout,
        )
        try:
            resp = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=self._request_timeout(),
                stream=True,
            )
        except Timeout as exc:
            raise LLMClientError(
                f"LLM 连接/读取超时 (connect={self.connect_timeout}s, read_idle={self.read_timeout}s): {exc}"
            ) from exc
        except RequestException as exc:
            raise LLMClientError(f"LLM 请求失败: {exc}") from exc

        if resp.status_code >= 400:
            raise LLMClientError(f"LLM HTTP {resp.status_code}: {resp.text[:500]}")

        try:
            for raw in resp.iter_lines():
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
                chunk = self._parse_sse_line(line)
                if chunk:
                    yield chunk
        except Timeout as exc:
            raise LLMClientError(
                f"LLM 流式读取超时 (read_idle={self.read_timeout}s，长时间无 SSE 数据): {exc}"
            ) from exc
        except (ChunkedEncodingError, ConnectionError, RequestException) as exc:
            raise LLMClientError(f"LLM 流式读取失败: {exc}") from exc

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        response_format: dict[str, str] | None = None,
    ) -> str:
        parts = list(
            self.chat_stream(
                messages,
                temperature=temperature,
                response_format=response_format,
            )
        )
        content = "".join(parts).strip()
        if not content:
            raise LLMClientError("LLM 返回空内容")
        return content

    def chat_json(self, messages: list[dict[str, str]], *, temperature: float = 0.2) -> dict[str, Any]:
        raw = self.chat(
            messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMClientError(f"LLM JSON 解析失败: {raw[:300]}") from exc
        if not isinstance(parsed, dict):
            raise LLMClientError("LLM JSON 根节点必须是 object")
        return parsed
