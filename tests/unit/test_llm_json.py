"""Unit tests — LLM JSON parsing (UT-01 ~ UT-04)."""
from __future__ import annotations

import json

import pytest

from src.agents.llm.base import _parse_llm_json


def test_valid_json() -> None:
    data = _parse_llm_json('{"items": [], "confidence": 0.5}')
    assert data["confidence"] == 0.5


def test_wrapped_json() -> None:
    raw = 'Here is output:\n{"consensus_bias": "bullish", "confidence": 0.6}\n'
    data = _parse_llm_json(raw)
    assert data["consensus_bias"] == "bullish"


def test_trailing_comma() -> None:
    raw = '{"items": [{"a": 1},], "confidence": 0.5,}'
    data = _parse_llm_json(raw)
    assert data["confidence"] == 0.5


def test_rejects_non_object() -> None:
    with pytest.raises(ValueError):
        _parse_llm_json("[1, 2, 3]")


def test_empty_raises() -> None:
    with pytest.raises(json.JSONDecodeError):
        _parse_llm_json("   ")
