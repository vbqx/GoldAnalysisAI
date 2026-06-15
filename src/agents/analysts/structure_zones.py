"""ICT structure zone distance helpers for technical analyst."""

from __future__ import annotations

from src.analysis.ict_pa import TimeframeAnalysis
from src.core.types import EvidenceItem, MarketContext

_TF_ZONE_WEIGHT = {"4h": 0.55, "1h": 0.5, "15m": 0.4}


def ict_zone_evidence(ctx: MarketContext) -> list[EvidenceItem]:
    """FVG / OB proximity to current price."""
    price = ctx.price
    if price <= 0:
        return []

    items: list[EvidenceItem] = []
    seen: set[str] = set()

    for tf, weight in _TF_ZONE_WEIGHT.items():
        analysis: TimeframeAnalysis | None = ctx.analyses.get(tf)
        if not analysis:
            continue

        for fvg in analysis.active_fvgs[:3]:
            mid = (float(fvg.low) + float(fvg.high)) / 2
            dist_pct = (price - mid) / price * 100
            summary = f"{tf} FVG {fvg.direction} 区间 {fvg.low:.1f}-{fvg.high:.1f} · 距现价 {dist_pct:+.2f}%"
            if summary in seen:
                continue
            seen.add(summary)
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=summary,
                    strength=weight,
                    timeframe=tf,
                    refs={"zone": "fvg", "dist_pct": round(dist_pct, 3)},
                )
            )

        for ob in analysis.order_blocks[-3:]:
            mid = (float(ob.low) + float(ob.high)) / 2
            dist_pct = (price - mid) / price * 100
            summary = f"{tf} OB {ob.direction} 区间 {ob.low:.1f}-{ob.high:.1f} · 距现价 {dist_pct:+.2f}%"
            if summary in seen:
                continue
            seen.add(summary)
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=summary,
                    strength=weight * 0.9,
                    timeframe=tf,
                    refs={"zone": "ob", "dist_pct": round(dist_pct, 3)},
                )
            )

    return items[:10]
