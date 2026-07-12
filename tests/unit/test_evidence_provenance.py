"""Evidence ID and refs preservation across analyst → research → debate."""

from __future__ import annotations

import pytest

from src.agents.analysts.base import build_report, items_for_direction
from src.agents.analysts.evidence_provenance import dedupe_evidence_items
from src.agents.llm.schemas import parse_agent_evidence, parse_research_debate
from src.core.types import AgentEvidence, AnalystReport, EvidenceItem


def test_build_report_assigns_evidence_ids() -> None:
    report = build_report(
        agent="technical_analyst",
        items=[EvidenceItem(category="technical", summary="trend up", strength=0.8, refs={"source": "ict"})],
        bias="bullish",
    )
    assert report.items[0].evidence_id == "technical_analyst:0"
    assert report.items[0].refs["source"] == "ict"


def test_items_for_direction_preserves_evidence_id_and_refs() -> None:
    reports = [
        AnalystReport(
            agent="news_analyst",
            bias="bullish",
            items=[
                EvidenceItem(
                    category="news",
                    summary="headline",
                    strength=0.7,
                    refs={"source": "jin10"},
                    evidence_id="news_analyst:0",
                )
            ],
            confidence=0.6,
            summary="news",
        )
    ]
    merged = items_for_direction(reports, "bullish")
    assert merged[0].evidence_id == "news_analyst:0"
    assert merged[0].refs["source"] == "jin10"
    assert merged[0].refs["upstream_id"] == "news_analyst:0"


def test_parse_agent_evidence_preserves_refs_and_id_with_whitelist() -> None:
    allowed = {"sentiment_analyst:1"}
    evidence = parse_agent_evidence(
        {
            "items": [
                {
                    "evidence_id": "sentiment_analyst:1",
                    "category": "analyst_sentiment_analyst",
                    "summary": "social bullish",
                    "strength": 0.75,
                    "refs": {"source": "tradingview_social"},
                }
            ],
            "confidence": 0.7,
            "summary": "ok",
        },
        agent="bullish_researcher_llm",
        direction="bullish",
        allowed_evidence_ids=allowed,
    )
    assert evidence.items[0].evidence_id == "sentiment_analyst:1"
    assert evidence.items[0].refs["source"] == "tradingview_social"
    assert evidence.provenance_meta["upstream_coverage"] == 1.0
    assert evidence.provenance_meta["model_confidence"] == 0.7
    assert 0.0 < evidence.confidence <= 1.0


def test_parse_agent_evidence_restores_refs_when_llm_drops_them() -> None:
    registry = {
        "sentiment_analyst:1": EvidenceItem(
            category="sentiment",
            summary="orig",
            strength=0.8,
            refs={"source": "tradingview_social", "analyst": "sentiment_analyst"},
            evidence_id="sentiment_analyst:1",
        )
    }
    evidence = parse_agent_evidence(
        {
            "items": [
                {
                    "evidence_id": "sentiment_analyst:1",
                    "category": "analyst_sentiment_analyst",
                    "summary": "social bullish",
                    "strength": 0.75,
                    "refs": {},
                }
            ],
            "confidence": 0.7,
            "summary": "ok",
        },
        agent="bullish_researcher_llm",
        direction="bullish",
        allowed_evidence_ids={"sentiment_analyst:1"},
        evidence_registry=registry,
    )
    assert evidence.items[0].refs["source"] == "tradingview_social"


def test_parse_agent_evidence_rejects_missing_id() -> None:
    with pytest.raises(ValueError, match="missing evidence_id"):
        parse_agent_evidence(
            {"items": [{"summary": "no id", "strength": 0.5}], "confidence": 0.5},
            agent="bullish_researcher_llm",
            direction="bullish",
            allowed_evidence_ids={"technical_analyst:0"},
        )


def test_parse_agent_evidence_rejects_unknown_id() -> None:
    with pytest.raises(ValueError, match="unknown evidence_id"):
        parse_agent_evidence(
            {
                "items": [
                    {
                        "evidence_id": "fabricated:99",
                        "summary": "bad",
                        "strength": 0.5,
                    }
                ],
                "confidence": 0.5,
            },
            agent="bullish_researcher_llm",
            direction="bullish",
            allowed_evidence_ids={"technical_analyst:0"},
        )


def test_parse_agent_evidence_rejects_fabricated_structure_id() -> None:
    import pytest

    with pytest.raises(ValueError, match="unknown evidence_id"):
        parse_agent_evidence(
            {
                "items": [
                    {
                        "evidence_id": "fabricated:structure:99",
                        "category": "structure",
                        "summary": "fake",
                        "strength": 0.6,
                        "refs": {},
                    }
                ],
                "confidence": 0.6,
            },
            agent="bullish_researcher_llm",
            direction="bullish",
            allowed_evidence_ids={"technical_analyst:0"},
        )


def test_dedupe_evidence_items_keeps_strongest() -> None:
    items = [
        EvidenceItem("x", "weak", 0.4, refs={}, evidence_id="a:0"),
        EvidenceItem("x", "strong", 0.9, refs={}, evidence_id="a:0"),
    ]
    deduped, dropped = dedupe_evidence_items(items)
    assert len(deduped) == 1
    assert deduped[0].summary == "strong"
    assert dropped == 1


def test_parse_research_debate_includes_provenance_meta() -> None:
    bull = AgentEvidence(
        "bullish_researcher_llm",
        "bullish",
        [EvidenceItem("s", "b1", 0.8, refs={"source": "ict"}, evidence_id="technical_analyst:0")],
        0.7,
        "bull",
        provenance_meta={"upstream_coverage": 1.0},
    )
    bear = AgentEvidence(
        "bearish_researcher_llm",
        "bearish",
        [
            EvidenceItem("s", "b2", 0.7, refs={"source": "macro"}, evidence_id="fundamentals_analyst:0"),
            EvidenceItem("s", "b3", 0.6, refs={"source": "jin10"}, evidence_id="news_analyst:0"),
        ],
        0.65,
        "bear",
    )
    debate = parse_research_debate(
        {"consensus_bias": "bearish", "consensus_strength": 0.8, "discussion_notes": ["a", "b", "c"]},
        bullish=bull,
        bearish=bear,
    )
    assert debate.debate_meta["bearish_item_count"] == 2
    assert debate.debate_meta["model_consensus_strength"] == 0.8
    assert "computed_consensus_strength" in debate.debate_meta
    assert 0.0 < debate.consensus_strength <= 1.0
