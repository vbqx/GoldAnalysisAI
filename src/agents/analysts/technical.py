"""Technical Analyst — indicators + ICT structure summary."""

from __future__ import annotations

from src.agents.analysts.structure_zones import ict_zone_evidence
from src.analysis.ict_pa import TimeframeAnalysis, sentiment_score
from src.analysis.technical_context import (
    TF_WEIGHT,
    build_technical_context,
    distance_pct,
)
from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext
from src.data.sources.market import MarketDataSource
from src.indicators.technical import ema_relation

from src.agents.analysts.base import build_report


def _structure_bias(analyses: dict[str, TimeframeAnalysis]) -> tuple[Bias, list[EvidenceItem]]:
    items: list[EvidenceItem] = []
    bull = bear = 0.0
    for tf, weight in TF_WEIGHT.items():
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


def _ict_context_evidence(ctx: MarketContext) -> tuple[Bias, list[EvidenceItem]]:
    """Convert computed ICT context into analyst evidence instead of leaving it report-only."""
    items: list[EvidenceItem] = []
    bull = bear = 0.0
    price = ctx.price

    for tf, weight in TF_WEIGHT.items():
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
            (z for z in analysis.liquidity if z.kind in ("swing_high", "swing_low")),
            key=lambda lz: abs(distance_pct(price, float(lz.price))),
        )
        for zone in liquidity[:2]:
            dist_pct = distance_pct(price, float(zone.price))
            zone_strength = max(float(getattr(zone, "strength", 0.5)), 0.35)
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} 流动性 {zone.label} @ {zone.price:.1f} · 距现价 {dist_pct:+.2f}%",
                    strength=weight * 0.65 * zone_strength,
                    timeframe=tf,
                    refs={
                        "liquidity": zone.kind,
                        "price": round(float(zone.price), 2),
                        "dist_pct": round(dist_pct, 3),
                        "strength": zone.strength,
                        "swept": zone.swept,
                    },
                )
            )

    if bull > bear + 0.1:
        return "bullish", items
    if bear > bull + 0.1:
        return "bearish", items
    return "neutral", items


def _fibonacci_evidence(technical_ctx: dict, price: float) -> list[EvidenceItem]:
    fib = technical_ctx.get("fibonacci") or {}
    levels = fib.get("nearest") or fib.get("levels") or []
    timeframe = fib.get("timeframe")
    if not levels or not timeframe:
        return []

    items: list[EvidenceItem] = []
    for row in levels[:3]:
        level = float(row["price"])
        dist_pct = float(row.get("dist_pct", distance_pct(price, level)))
        items.append(
            EvidenceItem(
                category="technical",
                summary=(
                    f"{timeframe} Fib {row['ratio']:.3f} {row['significance']} "
                    f"{level:.1f} · 距现价 {dist_pct:+.2f}%"
                ),
                strength=float(row["probability"]),
                timeframe=timeframe,
                refs={
                    "fibonacci": row["ratio"],
                    "price": round(level, 2),
                    "dist_pct": round(dist_pct, 3),
                },
            )
        )
    return items


def _indicator_evidence(technical_ctx: dict) -> tuple[Bias, list[EvidenceItem]]:
    items: list[EvidenceItem] = []
    bull = bear = 0.0
    indicators = technical_ctx.get("indicators") or {}
    for tf, weight in TF_WEIGHT.items():
        row = indicators.get(tf) or {}
        values = row.get("indicators") or {}

        rsi = values.get("RSI14")
        if rsi is not None:
            if rsi >= 70:
                bias: Bias = "bearish"
                bear += weight * 0.5
                label = "超买"
            elif rsi <= 30:
                bias = "bullish"
                bull += weight * 0.5
                label = "超卖"
            else:
                bias = "neutral"
                label = "中性"
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} RSI14 {rsi:.1f} · {label}",
                    strength=weight * 0.45,
                    timeframe=tf,
                    refs={"indicator": "RSI14", "value": rsi, "bias": bias},
                )
            )

        adx = values.get("ADX14")
        if adx is not None:
            label = "趋势强" if adx >= 25 else "趋势弱/震荡"
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} ADX14 {adx:.1f} · {label}",
                    strength=weight * (0.5 if adx >= 25 else 0.3),
                    timeframe=tf,
                    refs={"indicator": "ADX14", "value": adx},
                )
            )

        macd = values.get("MACD")
        signal = values.get("MACD_SIGNAL")
        if macd is not None and signal is not None:
            if macd > signal:
                bull += weight * 0.45
                label = "动能偏多"
            elif macd < signal:
                bear += weight * 0.45
                label = "动能偏空"
            else:
                label = "动能中性"
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} MACD {macd:.2f}/{signal:.2f} · {label}",
                    strength=weight * 0.45,
                    timeframe=tf,
                    refs={"indicator": "MACD", "macd": macd, "signal": signal},
                )
            )

        atr = values.get("ATR14")
        if atr is not None:
            atr_pct = atr / max(float(technical_ctx.get("price") or 0), 1e-9) * 100
            items.append(
                EvidenceItem(
                    category="technical",
                    summary=f"{tf} ATR14 {atr:.2f} · 波动 {atr_pct:.2f}%",
                    strength=weight * 0.35,
                    timeframe=tf,
                    refs={"indicator": "ATR14", "value": atr, "atr_pct": round(atr_pct, 3)},
                )
            )

    if bull > bear + 0.1:
        return "bullish", items
    if bear > bull + 0.1:
        return "bearish", items
    return "neutral", items


def _quality_evidence(technical_ctx: dict) -> list[EvidenceItem]:
    quality = technical_ctx.get("quality") or {}
    score = float(quality.get("score") or 0)
    warnings = quality.get("warnings") or []
    if score >= 0.75 and not warnings:
        return []
    return [
        EvidenceItem(
            category="technical",
            summary=f"技术输入质量 {score:.0%}" + (f"：{'；'.join(warnings[:3])}" if warnings else ""),
            strength=max(min(score, 0.5), 0.15),
            refs={"source": "technical_quality", **quality},
        )
    ]


def _support_resistance_evidence(technical_ctx: dict) -> tuple[Bias, list[EvidenceItem]]:
    sr = technical_ctx.get("support_resistance") or {}
    items: list[EvidenceItem] = []
    bull = bear = 0.0

    nearest_resistance = sr.get("nearest_resistance")
    nearest_support = sr.get("nearest_support")
    for level, label, bias in (
        (nearest_resistance, "上方压力", "bearish"),
        (nearest_support, "下方支撑", "bullish"),
    ):
        if not level:
            continue
        dist_pct = float(level.get("dist_pct") or 0)
        price_txt = _level_price_text(level)
        strength = min(float(level.get("strength") or 0.35) + max(0.0, 0.25 - abs(dist_pct)) * 0.5, 0.85)
        items.append(
            EvidenceItem(
                category="technical",
                summary=f"{label} {price_txt}：{level.get('label')} · 距现价 {dist_pct:+.2f}%",
                strength=strength,
                timeframe=level.get("timeframe"),
                refs={"source": "support_resistance", **level},
            )
        )
        if abs(dist_pct) <= 0.25:
            if bias == "bearish":
                bear += strength
            else:
                bull += strength

    neutral = sr.get("neutral") or []
    if neutral:
        level = neutral[0]
        items.append(
            EvidenceItem(
                category="technical",
                summary=f"多空分界 {_level_price_text(level)}：{level.get('label')}",
                strength=min(float(level.get("strength") or 0.35), 0.6),
                timeframe=level.get("timeframe"),
                refs={"source": "support_resistance", **level},
            )
        )

    if bull > bear + 0.1:
        return "bullish", items
    if bear > bull + 0.1:
        return "bearish", items
    return "neutral", items


def _level_price_text(level: dict) -> str:
    if "price_low" in level and "price_high" in level:
        return f"{float(level['price_low']):.1f}-{float(level['price_high']):.1f}"
    return f"{float(level.get('price') or 0):.1f}"


def _pa_evidence(technical_ctx: dict) -> list[EvidenceItem]:
    """DGT volume profile / S&R facts for analyst evidence."""
    items: list[EvidenceItem] = []
    pa = technical_ctx.get("price_action") or {}
    block = pa.get("5m") or {}
    if not block.get("volume_ok", True):
        return items
    vp = block.get("volume_profile") or {}
    if vp.get("poc") is not None:
        items.append(
            EvidenceItem(
                category="technical",
                summary=(
                    f"5m 量价 POC {float(vp['poc']):.1f}"
                    f" · VA {float(vp.get('val') or 0):.1f}-{float(vp.get('vah') or 0):.1f}"
                ),
                strength=0.55,
                timeframe="5m",
                refs={"poc": vp.get("poc"), "vah": vp.get("vah"), "val": vp.get("val")},
            )
        )
    for lvl in (block.get("sr_levels") or [])[-3:]:
        price = lvl.get("price")
        if price is None:
            continue
        items.append(
            EvidenceItem(
                category="technical",
                summary=f"5m {lvl.get('label', '量价S/R')} @{float(price):.1f}",
                strength=0.4,
                timeframe="5m",
                refs={"price": price, "kind": lvl.get("kind")},
            )
        )
    return items


def run_technical_analyst(ctx: MarketContext) -> AnalystReport:
    technical_ctx = build_technical_context(ctx)
    market_items = MarketDataSource(ctx.enriched).fetch_evidence()
    struct_bias, struct_items = _structure_bias(ctx.analyses)
    ict_bias, ict_items = _ict_context_evidence(ctx)
    fib_items = _fibonacci_evidence(technical_ctx, ctx.price)
    indicator_bias, indicator_items = _indicator_evidence(technical_ctx)
    sr_bias, sr_items = _support_resistance_evidence(technical_ctx)
    quality_items = _quality_evidence(technical_ctx)
    pa_items = _pa_evidence(technical_ctx)

    ema_items: list[EvidenceItem] = []
    last_5m = ctx.enriched.get("5m")
    last = last_5m.iloc[-1] if last_5m is not None and not last_5m.empty else None
    relations = ema_relation(ctx.price, last) if last is not None else {}
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
    items = (
        market_items
        + struct_items
        + ema_items
        + zone_items
        + ict_items
        + fib_items
        + indicator_items
        + sr_items
        + pa_items
        + quality_items
    )

    biases = [struct_bias, ema_bias, ict_bias, indicator_bias, sr_bias]
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

    d1 = ctx.analyses.get("1d")
    if d1 and d1.trend == "bearish" and bias == "bullish":
        bias = "neutral"
        items.append(
            EvidenceItem(
                category="technical",
                summary="1d 结构偏空，短周期偏多信号降级为中性技术结论",
                strength=TF_WEIGHT.get("1d", 0.0),
                timeframe="1d",
                refs={"source": "major_timeframe_anchor", "trend": d1.trend},
            )
        )
    elif d1 and d1.trend == "bullish" and bias == "bearish":
        bias = "neutral"
        items.append(
            EvidenceItem(
                category="technical",
                summary="1d 结构偏多，短周期偏空信号降级为中性技术结论",
                strength=TF_WEIGHT.get("1d", 0.0),
                timeframe="1d",
                refs={"source": "major_timeframe_anchor", "trend": d1.trend},
            )
        )

    summary = (
        f"技术：结构 {struct_bias} / EMA {ema_bias} / ICT区位 {ict_bias} / 指标 {indicator_bias} / 支撑阻力 {sr_bias} / 多周期投票 "
        f"多 {vote['bullish']:.0f}% 空 {vote['bearish']:.0f}%"
    )
    quality = technical_ctx.get("quality") or {}
    quality_score = float(quality.get("score") or 0)
    warnings = quality.get("warnings") or []
    if warnings:
        summary += f" / 输入质量 {quality_score:.0%}（{'; '.join(warnings[:2])}）"
    report = build_report(agent="technical_analyst", items=items, bias=bias, summary=summary)
    if quality_score < 0.75:
        report.confidence = min(report.confidence, max(quality_score, 0.2))
    return report
