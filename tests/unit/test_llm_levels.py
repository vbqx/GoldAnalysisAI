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
                    "path_id": "A",
                    "direction": "sell",
                    "entry_low": 4210,
                    "entry_high": 4205,
                    "stop_loss": 4218,
                    "take_profits": ["4195", 4180],
                    "setup_type": "fvg",
                    "reason": "bearish FVG retest",
                    "confidence": 0.8,
                },
                {
                    "path_id": "B",
                    "direction": "sell",
                    "entry_low": 4220,
                    "entry_high": 4215,
                    "stop_loss": 4228,
                    "take_profits": [4205, 4190],
                    "reason": "alt retest",
                    "confidence": 0.7,
                },
                {
                    "path_id": "C",
                    "direction": "buy",
                    "entry_low": 4188,
                    "entry_high": 4192,
                    "stop_loss": 4182,
                    "take_profits": [4200, 4210],
                    "reason": "hedge long",
                    "confidence": 0.55,
                },
            ]
        }
    )

    assert len(proposals) == 3
    assert proposals[0].direction == "SELL"
    assert proposals[0].entry_low == 4205
    assert proposals[0].entry_high == 4210
    assert proposals[0].take_profits == [4195.0, 4180.0]
    assert proposals[0].path_id == "A"


def test_parse_level_proposals_rejects_incomplete_contract() -> None:
    import pytest

    with pytest.raises(ValueError, match="exactly 3 setups"):
        parse_level_proposals(
            {
                "setups": [
                    {
                        "path_id": "A",
                        "direction": "sell",
                        "entry_low": 4210,
                        "entry_high": 4205,
                        "stop_loss": 4218,
                        "take_profits": [4195],
                        "reason": "one",
                        "confidence": 0.8,
                    },
                    {
                        "path_id": "B",
                        "direction": "buy",
                        "entry_low": 4188,
                        "entry_high": 4192,
                        "stop_loss": 4182,
                        "take_profits": [4200],
                        "reason": "two",
                        "confidence": 0.6,
                    },
                ]
            }
        )


def test_parse_level_proposals_reads_path_id() -> None:
    import pytest

    with pytest.raises(ValueError, match="exactly 3 setups"):
        parse_level_proposals(
            {
                "setups": [
                    {
                        "path_id": "B",
                        "direction": "BUY",
                        "entry_low": 4190,
                        "entry_high": 4195,
                        "stop_loss": 4185,
                        "take_profits": [4205],
                        "reason": "val support",
                        "confidence": 0.6,
                    }
                ]
            }
        )


def test_parse_level_proposals_rejects_missing_path_id() -> None:
    import pytest

    with pytest.raises(ValueError, match="invalid path_id"):
        parse_level_proposals(
            {
                "setups": [
                    {
                        "direction": "SELL",
                        "entry_low": 4210,
                        "entry_high": 4205,
                        "stop_loss": 4218,
                        "take_profits": [4195, 4180, 4170],
                        "reason": "one",
                        "confidence": 0.8,
                    },
                    {
                        "direction": "SELL",
                        "entry_low": 4220,
                        "entry_high": 4215,
                        "stop_loss": 4228,
                        "take_profits": [4200, 4190, 4180],
                        "reason": "two",
                        "confidence": 0.7,
                    },
                    {
                        "direction": "BUY",
                        "entry_low": 4188,
                        "entry_high": 4192,
                        "stop_loss": 4182,
                        "take_profits": [4200, 4210, 4220],
                        "reason": "three",
                        "confidence": 0.6,
                    },
                ]
            }
        )


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


def test_validate_llm_levels_rejects_malformed_tp_ladder() -> None:
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


def test_validate_llm_levels_names_path_signals() -> None:
    signals, _ = validate_llm_levels(
        _ctx(),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4205,
                entry_high=4210,
                stop_loss=4218,
                take_profits=[4195, 4184],
                setup_type="llm_fvg",
                reason="path A short",
                confidence=0.74,
                path_id="A",
            )
        ],
    )
    assert signals[0].name == "LLM路径A·做空"


def test_validate_llm_levels_rejects_sell_zone_below_price() -> None:
    signals, audit = validate_llm_levels(
        _ctx(price=4120.0),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4116.0,
                entry_high=4118.0,
                stop_loss=4121.0,
                take_profits=[4105.0],
                setup_type="llm_poc_va",
                reason="stale resistance",
                confidence=0.7,
            )
        ],
    )
    assert signals == []
    assert audit[0]["accepted"] is False
    assert "below current price" in audit[0]["reason"]


def test_validate_llm_levels_rejects_malformed_tp_ladder() -> None:
    signals, audit = validate_llm_levels(
        _ctx(),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4205,
                entry_high=4210,
                stop_loss=4218,
                take_profits=[4118.84, 4124.03, 4103.47],
                setup_type="llm_poc_va",
                reason="bad ladder",
                confidence=0.74,
                path_id="A",
            )
        ],
    )
    assert signals == []
    assert audit[0]["accepted"] is False
    assert "take_profits" in audit[0]["reason"]


def test_validate_llm_levels_accepts_valid_sell_geometry() -> None:
    signals, audit = validate_llm_levels(
        _ctx(price=4211.0),
        [
            LevelProposal(
                direction="SELL",
                entry_low=4200.0,
                entry_high=4205.0,
                stop_loss=4210.0,
                take_profits=[4188.0, 4175.0],
                setup_type="llm_fvg",
                reason="expired bearish FVG retest",
                confidence=0.74,
            )
        ],
    )

    assert signals == []
    assert audit[0]["accepted"] is False
    assert "breached stop_loss" in audit[0]["reason"]

