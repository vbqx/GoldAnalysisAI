"""Narrative formatting for analyst team stage I/O."""

from __future__ import annotations

from src.llm.narrative_output import format_llm_narrative


def test_analyst_team_narrative_html() -> None:
    raw = """{
      "technical": {"bias": "bullish", "confidence": 0.7, "summary": "结构偏多", "items": []},
      "fundamentals": {"bias": "bearish", "confidence": 0.55, "summary": "DXY偏强", "items": []},
      "news": {"bias": "neutral", "confidence": 0.3, "summary": "事件风险", "items": []},
      "sentiment": {"bias": "bearish", "confidence": 0.6, "summary": "结构投票偏空", "items": []}
    }"""
    html = format_llm_narrative("analyst_team", raw)
    assert "技术分析师" in html
    assert "基本面分析师" in html
    assert "偏多" in html
