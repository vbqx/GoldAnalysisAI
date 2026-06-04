"""Market data source — TradingView OHLCV (primary)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.core.types import EvidenceItem
from src.data.fetcher import daily_metrics


class MarketDataSource:
    name = "market"

    def __init__(self, enriched: dict[str, pd.DataFrame]) -> None:
        self._enriched = enriched

    def fetch_evidence(self) -> list[EvidenceItem]:
        df_1d = self._enriched["1d"]
        df_5m = self._enriched["5m"]
        m = daily_metrics(df_1d)
        last_5m = df_5m.iloc[-1]

        items: list[EvidenceItem] = [
            EvidenceItem(
                category="market",
                summary=f"现价 {m['current_price']:.2f}，日涨跌 {m['daily_change']:+.2f} ({m['daily_change_pct']:+.2f}%)",
                strength=min(abs(m["daily_change_pct"]) / 3.0, 1.0),
                timeframe="1d",
                refs={"current_price": m["current_price"], "daily_change_pct": m["daily_change_pct"]},
            ),
            EvidenceItem(
                category="market",
                summary=f"日高 {m['daily_high']:.2f} / 日低 {m['daily_low']:.2f}",
                strength=0.5,
                timeframe="1d",
                refs={"daily_high": m["daily_high"], "daily_low": m["daily_low"]},
            ),
        ]

        for col, label in (("EMA20", "EMA20"), ("EMA50", "EMA50"), ("VWAP", "VWAP")):
            if col in last_5m and pd.notna(last_5m[col]):
                val = float(last_5m[col])
                side = "上方" if m["current_price"] > val else "下方"
                items.append(
                    EvidenceItem(
                        category="market",
                        summary=f"价格位于 {label} {side} ({val:.2f})",
                        strength=0.4,
                        timeframe="5m",
                        refs={col: val},
                    )
                )
        return items
