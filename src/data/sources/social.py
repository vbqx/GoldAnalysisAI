"""Social sentiment source — placeholder."""

from __future__ import annotations

from src.core.types import EvidenceItem


class SocialDataSource:
    name = "social"

    def fetch_evidence(self) -> list[EvidenceItem]:
        # TODO: X / Reddit / EODHD social API
        return []
