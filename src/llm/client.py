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
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

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

        log.debug("llm stream model=%s url=%s", self.model, url)
        try:
            resp = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
        except requests.RequestException as exc:
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
        except (ChunkedEncodingError, ConnectionError, Timeout, RequestException) as exc:
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

