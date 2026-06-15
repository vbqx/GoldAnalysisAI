"""Macro / fundamentals for gold — DXY + US10Y via TradingView."""

from __future__ import annotations

from src.core.types import EvidenceItem, ExternalFactors, MacroQuote
from src.data.sources.macro import fetch_dxy_quote, fetch_macro_quotes


class FundamentalsDataSource:
    name = "fundamentals"

    def fetch_external(self) -> ExternalFactors:
        quotes = fetch_macro_quotes()
        dxy = next((q for q in quotes if q.name == "DXY"), None)
        impact = dxy.impact if dxy else "—"
        sources = ["tradingview_dxy"] if dxy else []
        if any(q.name == "US10Y" for q in quotes):
            sources.append("tradingview_us10y")
        return ExternalFactors(
            dxy_impact=impact,
            macro_quotes=quotes,
            sources=sources,
        )

    def fetch_evidence(self) -> list[EvidenceItem]:
        return macro_quotes_to_evidence(fetch_macro_quotes())


def macro_quotes_to_evidence(quotes: list[MacroQuote]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for q in quotes:
        is_live = q.source == "tradingview"
        strength = 0.6 if is_live and q.bias != "neutral" else 0.4
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=f"{q.name}：{q.impact}",
                strength=strength,
                refs=q.to_dict(),
            )
        )
    if not items:
        return [
            EvidenceItem(
                category="fundamentals",
                summary="宏观数据暂不可用（DXY/US10Y 拉取失败）",
                strength=0.25,
                refs={"source": "placeholder"},
            )
        ]
    return items


def external_macro_evidence(ext: ExternalFactors) -> list[EvidenceItem]:
    if ext.macro_quotes:
        return macro_quotes_to_evidence(ext.macro_quotes)
    if ext.dxy_impact != "—":
        return [
            EvidenceItem(
                category="fundamentals",
                summary=f"美元指数影响：{ext.dxy_impact}",
                strength=0.45,
                refs={"source": "tradingview_dxy"},
            )
        ]
    return FundamentalsDataSource().fetch_evidence()
