"""Deterministic unit verification for shared external HTTP adapters."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
import requests

from src.data.sources import _http


def test_post_json_applies_contract_and_returns_decoded_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Mock()
    response.json.return_value = {"ok": True}
    monkeypatch.setattr(_http.requests, "post", Mock(return_value=response))

    result = _http.post_json(
        "https://supplier.invalid/api",
        body={"symbol": "XAUUSD"},
        headers={"X-Test": "1"},
        timeout=3,
    )

    assert result == {"ok": True}
    response.raise_for_status.assert_called_once_with()
    _, kwargs = _http.requests.post.call_args
    assert kwargs["timeout"] == 3
    assert kwargs["json"] == {"symbol": "XAUUSD"}
    assert kwargs["headers"]["Content-Type"] == "application/json"
    assert kwargs["headers"]["X-Test"] == "1"


def test_post_json_retries_then_raises_auditable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    failure = requests.Timeout("supplier timeout")
    post = Mock(side_effect=failure)
    sleep = Mock()
    monkeypatch.setattr(_http, "EXTERNAL_HTTP_RETRIES", 1)
    monkeypatch.setattr(_http.requests, "post", post)
    monkeypatch.setattr(_http.time, "sleep", sleep)

    with pytest.raises(RuntimeError, match="HTTP POST failed") as caught:
        _http.post_json("https://supplier.invalid/api", body=[])

    assert caught.value.__cause__ is failure
    assert post.call_count == 2
    sleep.assert_called_once_with(1.0)


def test_get_text_and_get_json_use_bounded_http_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Mock(text='{"price": 2400.5}')
    get = Mock(return_value=response)
    monkeypatch.setattr(_http.requests, "get", get)

    assert _http.get_text("https://supplier.invalid/quote") == '{"price": 2400.5}'
    assert _http.get_json("https://supplier.invalid/quote") == {"price": 2400.5}
    assert get.call_count == 2
    assert all(call.kwargs["timeout"] == _http.EXTERNAL_HTTP_TIMEOUT for call in get.call_args_list)
    assert response.raise_for_status.call_count == 2
