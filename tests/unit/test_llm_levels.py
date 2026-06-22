"""LLM level proposal parsing and validation tests."""

from __future__ import annotations

from src.agents.llm.schemas import parse_level_proposals
from src.analysis.ict_pa import TimeframeAnalysis
from src.analysis.level_validator import validate_llm_levels
from src.core.types import ExternalFactors, LevelProposal, MarketContext


def _ctx(price: float = 4200.0) -> MarketContext:
    analyses = {
        tf: TimeframeAnalysis(
            timeframe=tf,
            trend="bearish" if tf in ("4h", "1h", "15m") else "ranging",
            bos="",
            choch="",
        )
        for tf in ("1d", "4h", "1h", "15m", "5m")
    }
    return MarketContext(
        enriched={},
        analyses=analyses,
        metrics={"current_price": price},
        price=price,
        external=ExternalFactors(),
        source_label="test",
    )


def test_parse_level_proposals_normalizes_entry_and_targets() -> None:
    proposals = parse_level_proposals(
        {
            "setups": [
                {
                    "direction": "sell",
                    "entry_low": 4210,
                    "entry_high": 4205,
                    "stop_loss": 4218,
                    "take_profits": ["4195", 4180],
                    "setup_type": "fvg",
                    "reason": "bearish FVG retest",
                    "confidence": 0.8,
                }
            ]
        }
    )

    assert len(proposals) == 1
    assert proposals[0].direction == "SELL"
    assert proposals[0].entry_low == 4205
    assert proposals[0].entry_high == 4210
    assert proposals[0].take_profits == [4195.0, 4180.0]


def test_validate_llm_levels_accepts_valid_sell_geometry() -> None:
    signals, audit = validate_llm_levels(
        _ctx(),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4205,
                entry_high=4210,
                stop_loss=4218,
                take_profits=[4195, 4184],
                setup_type="llm_fvg",
                reason="retest bearish FVG",
                confidence=0.74,
                invalidation="close above 4218",
            )
        ],
    )

    assert len(signals) == 1
    assert audit[0]["accepted"] is True
    assert signals[0].direction == "SELL"
    assert signals[0].setup_type == "llm_fvg"
    assert signals[0].status in {"candidate", "watch", "active", "invalid"}
    assert any("LLM confidence" in r for r in signals[0].score_reasons)


def test_validate_llm_levels_rejects_invalid_sell_geometry() -> None:
    signals, audit = validate_llm_levels(
        _ctx(),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4205,
                entry_high=4210,
                stop_loss=4208,
                take_profits=[4195],
                setup_type="llm_fvg",
                reason="bad stop",
                confidence=0.7,
            )
        ],
    )

    assert signals == []
    assert audit[0]["accepted"] is False
    assert "stop_loss" in audit[0]["reason"]

def test_validate_llm_levels_rejects_sell_after_stop_breached() -> None:
    signals, audit = validate_llm_levels(
        _ctx(price=4187.77),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4181.63,
                entry_high=4183.38,
                stop_loss=4184.26,
                take_profits=[4169.96, 4140.12],
                setup_type="llm_fvg",
                reason="expired bearish FVG retest",
                confidence=0.74,
            )
        ],
    )

    assert signals == []
    assert audit[0]["accepted"] is False
    assert "breached stop_loss" in audit[0]["reason"]

