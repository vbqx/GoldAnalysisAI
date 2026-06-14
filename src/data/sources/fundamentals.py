"""Macro / fundamentals for gold — DXY via TradingView."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors
from src.data.sources.dxy import fetch_dxy_impact


class FundamentalsDataSource:
    name = "fundamentals"

    def fetch_external(self) -> ExternalFactors:
        impact, _refs = fetch_dxy_impact()
        return ExternalFactors(dxy_impact=impact)

    def fetch_evidence(self) -> list[EvidenceItem]:
        impact, refs = fetch_dxy_impact()
        is_live = refs.get("source") == "tradingview"
        strength = 0.6 if is_live and refs.get("bias") in ("bullish", "bearish") else 0.35
        return [
            EvidenceItem(
                category="external",
                summary=f"美元指数影响：{impact}",
                strength=strength,
                refs=refs,
            )
        ]
