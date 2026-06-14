"""Unit tests for LLM JSON parsing fixes (BUG-01)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agents.llm.base import _parse_llm_json


def test_valid_json() -> None:
    data = _parse_llm_json('{"items": [], "confidence": 0.5}')
    assert data["confidence"] == 0.5
    print("PASS test_valid_json")


def test_wrapped_json() -> None:
    raw = 'Here is output:\n{"consensus_bias": "bullish", "confidence": 0.6}\n'
    data = _parse_llm_json(raw)
    assert data["consensus_bias"] == "bullish"
    print("PASS test_wrapped_json")


def test_trailing_comma() -> None:
    raw = '{"items": [{"a": 1},], "confidence": 0.5,}'
    data = _parse_llm_json(raw)
    assert data["confidence"] == 0.5
    print("PASS test_trailing_comma")


def test_rejects_non_object() -> None:
    try:
        _parse_llm_json("[1, 2, 3]")
        raise AssertionError("expected ValueError")
    except ValueError:
        print("PASS test_rejects_non_object")


def main() -> None:
    test_valid_json()
    test_wrapped_json()
    test_trailing_comma()
    test_rejects_non_object()
    print("\nAll LLM JSON parser tests passed.")


if __name__ == "__main__":
    main()
