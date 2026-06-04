"""Macro / fundamentals for gold — DXY, rates placeholder."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors


class FundamentalsDataSource:
    name = "fundamentals"

    def fetch_external(self) -> ExternalFactors:
        # TODO: DXY live feed, real yields, COT
        return ExternalFactors(dxy_impact="偏强 → 利空黄金")

    def fetch_evidence(self) -> list[EvidenceItem]:
        ext = self.fetch_external()
        return [
            EvidenceItem(
                category="external",
                summary=f"美元指数影响：{ext.dxy_impact}",
                strength=0.35,
                refs={"dxy_impact": ext.dxy_impact},
            )
        ]
