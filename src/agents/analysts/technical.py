"""Technical Analyst — indicators + ICT structure summary."""

from __future__ import annotations

from src.agents.analysts.structure_zones import ict_zone_evidence
from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext
from src.data.sources.market import MarketDataSource
from src.indicators.technical import ema_relation, fibonacci_levels

from src.agents.analysts.base import build_report

_TF_WEIGHT = {"1d": 0.20, "4h": 0.30, "1h": 0.25, "15m": 0.15, "5m": 0.10}


def _structure_bias(analyses: dict[str, TimeframeAnalysis]) -> tuple[Bias, list[EvidenceItem]]:
    items: list[EvidenceItem] = []
    bull = bear = 0.0
    for tf, weight in _TF_WEIGHT.items():
        a = analyses.get(tf)
        if not a:
            continue
        if a.trend == "bullish":
            bull += weight
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 结构趋势偏多",
                    strength=weight,
                    timeframe=tf,
                )
            )
        elif a.trend == "bearish":
            bear += weight
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 结构趋势偏空",
                    strength=weight,
                    timeframe=tf,
                )
            )
        if a.bos and a.bos != "无":
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} {a.bos}",
                    strength=weight * 0.85,
                    timeframe=tf,
                )
            )
        if a.choch and a.choch != "无":
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} {a.choch}",
                    strength=weight * 0.9,
                    timeframe=tf,
                )
            )

    if bull > bear + 0.1:
        return "bullish", items
    if bear > bull + 0.1:
        return "bearish", items
    return "neutral", items


def _distance_pct(price: float, level: float) -> float:
    if price <= 0:
        return 0.0
    return (price - level) / price * 100


def _ict_context_evidence(ctx: MarketContext) -> tuple[Bias, list[EvidenceItem]]:
    """Convert computed ICT context into analyst evidence instead of leaving it report-only."""
    items: list[EvidenceItem] = []
    bull = bear = 0.0
    price = ctx.price

    for tf, weight in _TF_WEIGHT.items():
        analysis = ctx.analyses.get(tf)
        if not analysis:
            continue

        if analysis.premium_discount != "unknown":
            label = {
                "premium": "Premium 溢价区",
                "discount": "Discount 折价区",
                "equilibrium": "Equilibrium 均衡区",
            }.get(analysis.premium_discount, analysis.premium_discount)
            refs = {"zone": analysis.premium_discount}
            eq_text = ""
            if analysis.equilibrium:
                refs["equilibrium"] = round(analysis.equilibrium, 2)
                eq_text = f" · 均衡位 {analysis.equilibrium:.1f}"
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 价格处于 {label}{eq_text}",
                    strength=weight * 0.75,
                    timeframe=tf,
                    refs=refs,
                )
            )
            if analysis.premium_discount == "discount":
                bull += weight * 0.75
            elif analysis.premium_discount == "premium":
                bear += weight * 0.75

        if analysis.volume_signal != "N/A":
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 成交量信号：{analysis.volume_signal}",
                    strength=weight * 0.45,
                    timeframe=tf,
                    refs={"volume_signal": analysis.volume_signal},
                )
            )

        liquidity = sorted(
            analysis.liquidity,
            key=lambda lz: abs(_distance_pct(price, float(lz.price))),
        )
        for zone in liquidity[:2]:
            dist_pct = _distance_pct(price, float(zone.price))
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 流动性 {zone.label} @ {zone.price:.1f} · 距现价 {dist_pct:+.2f}%",
                    strength=weight * 0.65,
                    timeframe=tf,
                    refs={
                        "liquidity": zone.kind,
                        "price": round(float(zone.price), 2),
                        "dist_pct": round(dist_pct, 3),
                    },
                )
            )

    if bull > bear + 0.1:
        return "bullish", items
    if bear > bull + 0.1:
        return "bearish", items
    return "neutral", items


def _fibonacci_evidence(ctx: MarketContext) -> list[EvidenceItem]:
    primary = ctx.analyses.get("4h") or ctx.analyses.get("1h") or ctx.analyses.get("1d")
    if not primary:
        return []

    swing_high = primary.swing_high or ctx.metrics.get("daily_high")
    swing_low = primary.swing_low or ctx.metrics.get("daily_low")
    if not swing_high or not swing_low or swing_high <= swing_low:
        return []

    levels = fibonacci_levels(float(swing_high), float(swing_low))
    ranked = sorted(
        levels,
        key=lambda row: abs(_distance_pct(ctx.price, float(row["price"]))),
    )
    items: list[EvidenceItem] = []
    for row in ranked[:3]:
        level = float(row["price"])
        dist_pct = _distance_pct(ctx.price, level)
        items.append(
            EvidenceItem(
                category="technical",
                summary=(
                    f"{primary.timeframe} Fib {row['ratio']:.3f} {row['significance']} "
                    f"{level:.1f} · 距现价 {dist_pct:+.2f}%"
                ),
                strength=float(row["probability"]),
                timeframe=primary.timeframe,
                refs={
                    "fibonacci": row["ratio"],
                    "price": round(level, 2),
                    "dist_pct": round(dist_pct, 3),
                },
            )
        )
    return items


def run_technical_analyst(ctx: MarketContext) -> AnalystReport:
    market_items = MarketDataSource(ctx.enriched).fetch_evidence()
    struct_bias, struct_items = _structure_bias(ctx.analyses)
    ict_bias, ict_items = _ict_context_evidence(ctx)
    fib_items = _fibonacci_evidence(ctx)

    ema_items: list[EvidenceItem] = []
    last = ctx.enriched["5m"].iloc[-1]
    relations = ema_relation(ctx.price, last)
    above = sum(1 for v in relations.values() if v == "上方")
    below = sum(1 for v in relations.values() if v == "下方")
    for col, rel in relations.items():
        if rel == "N/A":
            continue
        ema_items.append(
            EvidenceItem(
                category="technical",
                summary=f"价格位于 {col} {rel}",
                strength=0.45,
                timeframe="5m",
                refs={col: rel},
            )
        )

    ema_bias: Bias = "neutral"
    if above > below:
        ema_bias = "bullish"
    elif below > above:
        ema_bias = "bearish"

    vote = sentiment_score(ctx.analyses)
    zone_items = ict_zone_evidence(ctx)
    items = market_items + struct_items + ema_items + zone_items + ict_items + fib_items

    biases = [struct_bias, ema_bias, ict_bias]
    if vote["bullish"] > vote["bearish"] + 8:
        biases.append("bullish")
    elif vote["bearish"] > vote["bullish"] + 8:
        biases.append("bearish")
    else:
        biases.append("neutral")

    bull_votes = biases.count("bullish")
    bear_votes = biases.count("bearish")
    if bull_votes > bear_votes:
        bias: Bias = "bullish"
    elif bear_votes > bull_votes:
        bias = "bearish"
    else:
        bias = "neutral"

    summary = (
        f"技术：结构 {struct_bias} / EMA {ema_bias} / ICT区位 {ict_bias} / 多周期投票 "
        f"多 {vote['bullish']:.0f}% 空 {vote['bearish']:.0f}%"
    )
    return build_report(agent="technical_analyst", items=items, bias=bias, summary=summary)
