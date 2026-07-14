"""LLM payload funnel — each stage receives upstream conclusions, not full raw dumps."""

from __future__ import annotations

import pandas as pd

from src.agents.analysts import run_analyst_team
from src.agents.bearish import run_bearish_researcher
from src.agents.bullish import run_bullish_researcher
from src.agents.debate import run_debate
from src.agents.llm.payload import (
    analyst_team_input_payload,
    debate_payload,
    level_proposer_payload,
    manager_payload,
    research_payload,
    risk_payload,
    trader_decision_payload,
    trader_payload,
)
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.report_engine import compute_trading_signals
from src.core.types import (
    AgentEvidence,
    AnalystReport,
    AnalystTeam,
    EvidenceItem,
    ExternalFactors,
    MacroQuote,
    MarketContext,
    ResearchDebate,
    RiskReview,
    TransactionProposal,
)
from src.indicators.technical import enrich


def _sample_context() -> MarketContext:
    idx = pd.date_range("2026-01-01", periods=120, freq="5min", tz="UTC")
    close = 4200.0 + pd.Series(range(120), dtype=float) * 0.05
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [100] * 120,
        },
        index=idx,
    )
    enriched = {tf: enrich(df) for tf in ("5m", "15m", "1h", "4h", "1d")}
    analyses = {tf: analyze_timeframe(enriched[tf], tf) for tf in enriched}
    price = float(close.iloc[-1])
    return MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics={
            "current_price": price,
            "daily_high": price + 10,
            "daily_low": price - 10,
        },
        price=price,
        external=ExternalFactors(
            dxy_impact="偏强",
            macro_quotes=[
                MacroQuote(
                    name="DXY",
                    symbol="TVC:DXY",
                    close=104.0,
                    change_pct=0.5,
                    impact="偏强",
                    bias="bearish",
                )
            ],
        ),
        derived={
            "news_topics": [{"topic": "美联储", "count": 3}],
            "upcoming_calendar": [{"time": "2026-07-13", "region": "US", "event": "CPI"}],
            "event_countdown": {"hours": 12.0, "event": "CPI"},
            "calendar_high_impact_count": 1,
        },
        context_stats={"technical_inputs": {"5m_bars": 120}},
        source_label="test",
    )


def _sample_team() -> AnalystTeam:
    def _report(agent: str, bias: str) -> AnalystReport:
        return AnalystReport(
            agent=agent,
            bias=bias,  # type: ignore[arg-type]
            confidence=0.7,
            summary=f"{agent} summary",
            items=[
                EvidenceItem(category="structure", summary=f"{agent} item 1", strength=0.8),
                EvidenceItem(category="external", summary=f"{agent} item 2", strength=0.6),
            ],
        )

    return AnalystTeam(
        technical=_report("technical_analyst", "bullish"),
        fundamentals=_report("fundamentals_analyst", "bearish"),
        news=_report("news_analyst", "neutral"),
        sentiment=_report("sentiment_analyst", "bullish"),
    )


def test_research_payload_excludes_raw_external_and_timeframes(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", True)
    ctx = _sample_context()
    team = _sample_team()
    payload = research_payload(ctx, team, "bullish")

    assert "analyst_team" in payload
    assert payload["direction"] == "bullish"
    assert "structure_vote" in payload
    assert "event_risk" in payload
    assert "external" not in payload
    assert "timeframes" not in payload
    assert "derived" not in payload
    assert "metrics" not in payload


def _sample_debate() -> ResearchDebate:
    bull = AgentEvidence("bullish_researcher", "bullish", [], 0.6, "bull")
    bear = AgentEvidence("bearish_researcher", "bearish", [], 0.5, "bear")
    return ResearchDebate(
        bullish=bull,
        bearish=bear,
        consensus_bias="bearish",
        consensus_strength=0.72,
        discussion_notes=["note 1", "note 2"],
    )


def test_trader_payload_excludes_market_when_funnel(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", True)
    ctx = _sample_context()
    team = _sample_team()
    debate = _sample_debate()
    signals = compute_trading_signals(ctx)
    payload = trader_payload(ctx, debate, signals, team=team)

    assert "market" not in payload
    assert "analyst_team_summaries" in payload
    assert payload["debate"]["consensus_bias"] == "bearish"
    assert "candidate_signals" in payload
    assert "structure_vote" in payload


def test_debate_payload_includes_analyst_top_items_when_funnel(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", True)
    ctx = _sample_context()
    team = _sample_team()
    bull = AgentEvidence("bullish_researcher", "bullish", [], 0.6, "bull")
    bear = AgentEvidence("bearish_researcher", "bearish", [], 0.5, "bear")
    payload = debate_payload(bull, bear, ctx.analyses, ctx=ctx, team=team)

    assert "analyst_team" in payload
    assert "items" in payload["analyst_team"]["technical"]
    assert "derived" not in payload
    assert "event_risk" in payload


def test_level_proposer_payload_includes_technical_level_reactions(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", True)
    ctx = _sample_context()
    team = _sample_team()
    team.technical.level_reactions = [
        {
            "id": "tech_reaction:0",
            "label": "POC",
            "price": 4200.0,
            "timeframe": "5m",
            "expected_reaction": "承压回落",
        }
    ]
    debate = _sample_debate()
    payload = level_proposer_payload(ctx, team, debate, [])
    assert payload["technical_level_reactions"][0]["id"] == "tech_reaction:0"
    assert "reaction_evidence_id" in payload["level_constraints"]["execution"]


def test_level_proposer_payload_uses_structure_context_not_external(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", True)
    ctx = _sample_context()
    team = _sample_team()
    debate = _sample_debate()
    signals = compute_trading_signals(ctx)
    payload = level_proposer_payload(ctx, team, debate, signals)

    assert "structure_context" in payload
    assert "external" not in payload
    assert "analyst_team" in payload


def test_manager_payload_unchanged_proposal_only() -> None:
    proposal = TransactionProposal("short", [0], ["rationale"], "bearish")
    reviews = [
        RiskReview("aggressive", True, [0], 1.0, ["ok"]),
        RiskReview("neutral", True, [0], 0.7, ["ok"]),
        RiskReview("conservative", False, [], 0.0, ["no"]),
    ]
    payload = manager_payload(proposal, reviews)

    assert "proposal" in payload
    assert "risk_reviews" in payload
    assert len(payload["risk_reviews"]) == 3
    assert "market" not in payload
    assert "analyst_team" not in payload


def test_analyst_team_input_payload_has_per_specialist_keys() -> None:
    ctx = _sample_context()
    payload = analyst_team_input_payload(ctx)

    assert set(payload.keys()) == {"technical", "fundamentals", "news", "sentiment", "context_stats"}
    assert "external" not in payload["technical"]
    assert "channels" in payload["news"]


def test_legacy_payload_when_funnel_disabled(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", False)
    ctx = _sample_context()
    team = run_analyst_team(ctx)
    bull = run_bullish_researcher(ctx, team)
    bear = run_bearish_researcher(ctx, team)
    debate = run_debate(bull, bear, ctx.analyses, team=team, ctx=ctx)
    signals = compute_trading_signals(ctx)

    research = research_payload(ctx, team, "bullish")
    assert "external" in research
    assert "timeframes" in research

    trader = trader_payload(ctx, debate, signals, team=team)
    assert "market" in trader

    deb = debate_payload(bull, bear, ctx.analyses, ctx=ctx, team=team)
    assert "derived" in deb
    assert "analyst_team_summaries" in deb


def test_risk_payload_is_proposal_only() -> None:
    proposal = TransactionProposal("short", [0], ["test"], "bearish")
    payload = risk_payload(proposal, signal_count=3)
    assert payload["proposal"]["primary_direction"] == "short"
    assert payload["signal_count"] == 3
    assert payload["profiles"] == ["aggressive", "neutral", "conservative"]
    assert "market" not in payload


def test_trader_decision_payload_excludes_raw_market(monkeypatch) -> None:
    monkeypatch.setattr("src.agents.llm.payload.LLM_PAYLOAD_FUNNEL", True)
    ctx = _sample_context()
    team = _sample_team()
    debate = _sample_debate()
    signals = compute_trading_signals(ctx)
    payload = trader_decision_payload(ctx, debate, team, signals)
    assert "market" not in payload
    assert "candidate_signals" in payload
    assert payload["debate"]["consensus_bias"] == "bearish"

    routed = trader_payload(ctx, debate, signals, team=team)
    assert "market" not in routed
    assert "analyst_team_summaries" in routed
