"""Data source protocols (TradeAgent data layer)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.core.types import EvidenceItem, ExternalFactors


@runtime_checkable
class DataSource(Protocol):
    name: str

    def fetch(self) -> list[EvidenceItem] | ExternalFactors:
        ...
