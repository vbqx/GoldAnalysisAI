"""FIN-14: trader respects structure sentiment when debate is not strongly opposing."""

from __future__ import annotations

import pytest

from src.agents.trader import run_trader_agent
from src.analysis.ict_pa import TimeframeAnalysis
from src.analysis.report_engine import TradingSignal
from src.core.types import AgentEvidence, MarketContext, ResearchDebate


def _ctx(analyses: dict) -> MarketContext:
    return MarketContext(
        enriched={},
        price=4155.0,
        metrics={"current_price": 4155.0, "daily_high": 4200.0, "daily_low": 4100.0},
        analyses=analyses,
        external=None,  # type: ignore[arg-type]
        source_label="test",
    )


def _debate(bias: str, strength: float) -> ResearchDebate:
    stub = _evidence("stub", bias, 1, strength)
    return ResearchDebate(
        bullish=stub,
        bearish=stub,
        consensus_bias=bias,  # type: ignore[arg-type]
        consensus_strength=strength,
        discussion_notes=[],
    )


def _evidence(agent: str, direction: str, n: int, conf: float) -> AgentEvidence:
    from src.core.types import EvidenceItem

    items = [
        EvidenceItem(category="research", summary=f"item{i}", strength=0.5)
        for i in range(n)
    ]
    return AgentEvidence(
        agent=agent,
        direction=direction,  # type: ignore[arg-type]
        items=items,
        confidence=conf,
        summary=direction,
    )


def _signals() -> list[TradingSignal]:
    short_sig = TradingSignal(
        name="保守反抽做空",
        direction="SELL",
        direction_cn="卖出",
        entry_low=4177.0,
        entry_high=4183.0,
        stop_loss=4190.0,
        take_profits=[4167.0, 4100.0, 4023.0],
        risk_reward="1:1.3",
        sentiment_bias_pct="45%",
        position_size="20%",
        note="OB short",
        theme="short",
    )
    long_sig = TradingSignal(
        name="右侧扫低做多",
        direction="BUY",
        direction_cn="买入",
        entry_low=4018.0,
        entry_high=4023.0,
        stop_loss=4014.0,
        take_profits=[4155.0, 4200.0, 4300.0],
        risk_reward="1:10",
        sentiment_bias_pct="25%",
        position_size="15%",
        note="sweep long",
        theme="long",
    )
    return [
        TradingSignal(
            name="激进反抽做空",
            direction="SELL",
            direction_cn="卖出",
            entry_low=4149.0,
            entry_high=4150.0,
            stop_loss=4152.0,
            take_profits=[4140.0, 4100.0, 4023.0],
            risk_reward="1:2",
            sentiment_bias_pct="45%",
            position_size="30%",
            note="FVG",
            theme="short",
        ),
        short_sig,
        long_sig,
    ]


def _bearish_analyses() -> dict:
    return {
        "5m": TimeframeAnalysis("5m", "bearish", "—", "—"),
        "15m": TimeframeAnalysis("15m", "bearish", "—", "—"),
        "1h": TimeframeAnalysis("1h", "bullish", "—", "—"),
        "4h": TimeframeAnalysis("4h", "ranging", "—", "—"),
        "1d": TimeframeAnalysis("1d", "bearish", "—", "—"),
    }


@pytest.mark.financial
def test_trader_prefers_short_when_bearish_sentiment_and_debate_bearish() -> None:
    debate = _debate("bearish", 0.54)
    proposal, _ = run_trader_agent(_ctx(_bearish_analyses()), debate, _signals())
    assert proposal.primary_direction == "short"
    assert proposal.signal_indices[0] in (0, 1)


@pytest.mark.financial
def test_trader_short_when_bearish_sentiment_weak_bullish_debate() -> None:
    """Bearish structure + debate bullish but strength < 0.6 → still short."""
    debate = _debate("bullish", 0.54)
    proposal, _ = run_trader_agent(_ctx(_bearish_analyses()), debate, _signals())
    assert proposal.primary_direction == "short"
