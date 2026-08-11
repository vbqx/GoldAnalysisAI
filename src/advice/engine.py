"""Build one falsifiable trading suggestion for manual review.

The engine does not authorize or execute trades.  It reduces verified market
facts to exactly one watch setup, or explicitly returns WAIT/AVOID.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from src.advice.audit import audit_advice
from src.advice.types import (
    AdviceEvidence,
    AdvicePacket,
    AdviceSetup,
    AlternativeScenario,
    AttentionZone,
)
from src.analysis.data_freshness import build_data_as_of
from src.analysis.technical_context import support_resistance_context
from src.core.types import MarketContext

_HORIZON = "未来 2～6 小时"
_TF_CN = {"1d": "日线", "4h": "4小时", "1h": "1小时", "15m": "15分钟", "5m": "5分钟"}


def _bias(ctx: MarketContext) -> tuple[str, str, list[str]]:
    trend_4h = getattr(ctx.analyses.get("4h"), "trend", "ranging")
    trend_1h = getattr(ctx.analyses.get("1h"), "trend", "ranging")
    trend_15m = getattr(ctx.analyses.get("15m"), "trend", "ranging")
    context = [
        f"4小时结构{_trend_cn(trend_4h)}",
        f"1小时结构{_trend_cn(trend_1h)}",
        f"15分钟结构{_trend_cn(trend_15m)}",
    ]
    if trend_4h == trend_1h and trend_4h in ("bullish", "bearish"):
        confidence = "high" if trend_15m == trend_4h else "medium"
        return trend_4h, confidence, context
    if trend_4h in ("bullish", "bearish") and trend_1h == "ranging":
        return trend_4h, "medium", context
    if trend_1h in ("bullish", "bearish") and trend_4h == "ranging":
        return trend_1h, "low", context
    if trend_4h != trend_1h and {trend_4h, trend_1h} == {"bullish", "bearish"}:
        return "mixed", "low", context
    return "neutral", "low", context


def _trend_cn(value: str) -> str:
    return {"bullish": "偏多", "bearish": "偏空", "ranging": "震荡"}.get(value, "不明")


def _level_bounds(row: dict[str, Any]) -> tuple[float, float]:
    price = float(row.get("price") or 0.0)
    low = float(row.get("price_low") if row.get("price_low") is not None else price)
    high = float(row.get("price_high") if row.get("price_high") is not None else price)
    return min(low, high), max(low, high)


def _source_family(row: dict[str, Any]) -> str:
    source = str(row.get("source") or "unknown")
    return source.split(":", 1)[0]


def _evidence_id(row: dict[str, Any], index: int) -> str:
    tf = str(row.get("timeframe") or "market")
    source = _source_family(row)
    price = float(row.get("price") or 0.0)
    return f"level:{tf}:{source}:{price:.2f}:{index}"


def _cluster_levels(
    rows: list[dict[str, Any]],
    *,
    tolerance: float,
) -> list[list[dict[str, Any]]]:
    clusters: list[list[dict[str, Any]]] = []
    for row in sorted(rows, key=lambda item: float(item.get("price") or 0.0)):
        price = float(row.get("price") or 0.0)
        matched = next(
            (
                cluster
                for cluster in clusters
                if abs(price - sum(float(x.get("price") or 0.0) for x in cluster) / len(cluster))
                <= tolerance
            ),
            None,
        )
        if matched is None:
            clusters.append([row])
        else:
            matched.append(row)
    return clusters


def _cluster_rank(cluster: list[dict[str, Any]], price: float) -> tuple[int, float, float]:
    families = {_source_family(row) for row in cluster}
    timeframes = {str(row.get("timeframe") or "") for row in cluster}
    center = sum(float(row.get("price") or 0.0) for row in cluster) / len(cluster)
    breadth = len(families) + len({tf for tf in timeframes if tf})
    strength = sum(float(row.get("strength") or 0.0) for row in cluster)
    return breadth, strength, -abs(price - center)


def _pick_cluster(
    rows: list[dict[str, Any]],
    *,
    direction: str,
    price: float,
    tolerance: float,
    max_distance: float,
) -> list[dict[str, Any]] | None:
    eligible: list[dict[str, Any]] = []
    for row in rows:
        low, high = _level_bounds(row)
        if direction == "BUY" and low <= price and price - high <= max_distance:
            eligible.append(row)
        elif direction == "SELL" and high >= price and low - price <= max_distance:
            eligible.append(row)
    clusters = _cluster_levels(eligible, tolerance=tolerance)
    # One isolated geometric level is analysis context, not a trade suggestion.
    qualified = [
        cluster
        for cluster in clusters
        if len({_source_family(row) for row in cluster}) >= 2
        or len({str(row.get("timeframe") or "") for row in cluster if row.get("timeframe")}) >= 2
    ]
    if not qualified:
        return None
    return max(qualified, key=lambda cluster: _cluster_rank(cluster, price))


def _zone_from_cluster(cluster: list[dict[str, Any]]) -> AttentionZone:
    bounds = [_level_bounds(row) for row in cluster]
    low = min(item[0] for item in bounds)
    high = max(item[1] for item in bounds)
    labels = []
    for row in cluster:
        label = str(row.get("label") or "结构价位")
        if label not in labels:
            labels.append(label)
    return AttentionZone(round(low, 2), round(high, 2), " · ".join(labels[:3]))


def _target_prices(
    rows: list[dict[str, Any]],
    *,
    direction: str,
    zone: AttentionZone,
    tolerance: float,
) -> list[float]:
    candidates: list[float] = []
    for cluster in _cluster_levels(rows, tolerance=tolerance):
        center = sum(float(row.get("price") or 0.0) for row in cluster) / len(cluster)
        if direction == "BUY" and center > zone.high:
            candidates.append(center)
        elif direction == "SELL" and center < zone.low:
            candidates.append(center)
    ordered = sorted(set(round(value, 2) for value in candidates), reverse=direction == "SELL")
    return ordered[:2]


def _rr(direction: str, zone: AttentionZone, invalidation: float, targets: list[float]) -> list[float]:
    entry = (zone.low + zone.high) / 2
    risk = entry - invalidation if direction == "BUY" else invalidation - entry
    if risk <= 0:
        return []
    return [
        round(max(0.0, (target - entry if direction == "BUY" else entry - target) / risk), 2)
        for target in targets
    ]


def _human_checklist(direction: str, zone: AttentionZone) -> list[str]:
    zone_text = f"{zone.low:.2f}–{zone.high:.2f}"
    if direction == "BUY":
        return [
            f"价格进入 {zone_text} 关注区，而不是在区间上方追价",
            "5分钟出现扫低收回、明显下影拒绝，或连续收盘守住关注区",
            "5分钟形成新的看涨 CHoCH/BOS；若直接跌穿则不确认",
        ]
    return [
        f"价格进入 {zone_text} 关注区，而不是在区间下方追价",
        "5分钟出现扫高回落、明显上影拒绝，或连续收盘受阻于关注区",
        "5分钟形成新的看跌 CHoCH/BOS；若直接突破则不确认",
    ]


def _risks(ctx: MarketContext) -> list[str]:
    risks: list[str] = []
    high_events = [event for event in ctx.external.calendar_events if float(event.importance) >= 0.8]
    if high_events:
        risks.append("临近高影响宏观事件，确认前需重新检查事件时间与波动")
    if ctx.external.fetch_errors:
        risks.append("部分外部数据抓取失败，宏观信息仅作背景参考")
    analysis_15m = ctx.analyses.get("15m")
    if analysis_15m and "放量" in str(analysis_15m.volume_signal):
        risks.append("15分钟处于放量状态，关注区可能出现快速穿越")
    return risks[:3]


def _no_setup_packet(
    *,
    decision: str,
    bias: str,
    confidence: str,
    price: float,
    context: list[str],
    summary: str,
    risks: list[str],
    uncertainties: list[str],
    evidence: list[AdviceEvidence],
) -> AdvicePacket:
    packet = AdvicePacket(
        decision=decision,  # type: ignore[arg-type]
        bias=bias,  # type: ignore[arg-type]
        confidence=confidence,  # type: ignore[arg-type]
        horizon=_HORIZON,
        summary=summary,
        current_price=round(price, 2),
        primary_setup=None,
        alternative_scenario=None,
        market_context=context,
        risks=risks,
        uncertainties=uncertainties,
        evidence=evidence,
    )
    return replace(packet, audit=audit_advice(packet))


def build_advice_packet(ctx: MarketContext) -> AdvicePacket:
    price = float(ctx.price)
    bias, confidence, context = _bias(ctx)
    evidence = [
        AdviceEvidence(
            evidence_id=f"structure:{tf}:trend",
            kind="structure",
            statement=f"{_TF_CN.get(tf, tf)}结构{_trend_cn(analysis.trend)}",
            timeframe=tf,
            source="ict_pa",
        )
        for tf in ("4h", "1h", "15m")
        if (analysis := ctx.analyses.get(tf)) is not None
    ]
    risks = _risks(ctx)
    freshness = build_data_as_of(ctx.enriched, now=ctx.derived.get("evaluation_time"))
    if not freshness.get("executable", False):
        return _no_setup_packet(
            decision="AVOID",
            bias=bias,
            confidence="low",
            price=price,
            context=context,
            summary="数据快照不满足时效要求，本次不形成交易建议。",
            risks=risks,
            uncertainties=list(freshness.get("warnings") or []),
            evidence=evidence,
        )
    if bias in ("mixed", "neutral"):
        return _no_setup_packet(
            decision="WAIT",
            bias=bias,
            confidence=confidence,
            price=price,
            context=context,
            summary="4小时与1小时方向没有形成清晰一致性，当前以观望为主。",
            risks=risks,
            uncertainties=["高周期方向存在冲突，强行选择多空会放大主观偏差"],
            evidence=evidence,
        )

    direction = "BUY" if bias == "bullish" else "SELL"
    levels = support_resistance_context(ctx, limit=16)
    atr_15m = float(getattr(ctx.analyses.get("15m"), "atr", 0.0) or 0.0)
    atr_5m = float(getattr(ctx.analyses.get("5m"), "atr", 0.0) or 0.0)
    volatility = max(atr_15m, atr_5m * 2.0, price * 0.001)
    tolerance = max(volatility * 0.35, price * 0.0008)
    max_distance = max(volatility * 2.5, price * 0.008)
    source_rows = levels["support" if direction == "BUY" else "resistance"]
    target_rows = levels["resistance" if direction == "BUY" else "support"]
    cluster = _pick_cluster(
        source_rows,
        direction=direction,
        price=price,
        tolerance=tolerance,
        max_distance=max_distance,
    )
    if not cluster:
        side = "支撑" if direction == "BUY" else "阻力"
        return _no_setup_packet(
            decision="WAIT",
            bias=bias,
            confidence=confidence,
            price=price,
            context=context,
            summary=f"方向背景{_trend_cn(bias)}，但附近没有通过多源验证的{side}关注区。",
            risks=risks,
            uncertainties=[f"当前仅有孤立{side}，不足以形成首选交易建议"],
            evidence=evidence,
        )

    zone = _zone_from_cluster(cluster)
    targets = _target_prices(target_rows, direction=direction, zone=zone, tolerance=tolerance)
    if not targets:
        return _no_setup_packet(
            decision="WAIT",
            bias=bias,
            confidence=confidence,
            price=price,
            context=context,
            summary=f"方向背景{_trend_cn(bias)}，但当前结构没有提供清晰的目标空间。",
            risks=risks,
            uncertainties=["缺少方向一侧的有效目标价位，无法评价建议空间"],
            evidence=evidence,
        )

    buffer = max(volatility * 0.55, price * 0.0007)
    invalidation = round(zone.low - buffer, 2) if direction == "BUY" else round(zone.high + buffer, 2)
    cluster_ids: list[str] = []
    for index, row in enumerate(cluster):
        item_id = _evidence_id(row, index)
        cluster_ids.append(item_id)
        evidence.append(
            AdviceEvidence(
                evidence_id=item_id,
                kind="level",
                statement=str(row.get("label") or "结构价位"),
                timeframe=str(row.get("timeframe") or ""),
                source=str(row.get("source") or ""),
                price=round(float(row.get("price") or 0.0), 2),
            )
        )
    state = (
        "价格正在关注区内，等待人工确认价格行为"
        if zone.low <= price <= zone.high
        else "价格尚未进入关注区，不建议追价"
    )
    side_cn = "做多" if direction == "BUY" else "做空"
    setup = AdviceSetup(
        direction=direction,  # type: ignore[arg-type]
        attention_zone=zone,
        current_state=state,
        rationale=[
            f"4小时与1小时结构共同{_trend_cn(bias)}",
            f"关注区由 {len(cluster_ids)} 条不同周期或来源的结构事实共同支持",
            "入场判断保留给人工确认，宏观新闻不直接决定入场价",
        ],
        confirmation_checklist=_human_checklist(direction, zone),
        invalidation=(
            f"15分钟有效跌破 {invalidation:.2f} 后取消本次做多思路"
            if direction == "BUY"
            else f"15分钟有效突破 {invalidation:.2f} 后取消本次做空思路"
        ),
        invalidation_level=invalidation,
        targets=targets,
        evidence_ids=cluster_ids,
        reward_risk_to_targets=_rr(direction, zone, invalidation, targets),
    )
    opposite = "做空" if direction == "BUY" else "做多"
    alternative = AlternativeScenario(
        condition=(
            f"15分钟收盘跌破 {invalidation:.2f}，随后反抽不能重新站回"
            if direction == "BUY"
            else f"15分钟收盘突破 {invalidation:.2f}，随后回踩没有跌回"
        ),
        response=f"取消首选{side_cn}思路，仅在新结构形成后重新评估{opposite}，不自动反手。",
    )
    decision = "WATCH_LONG" if direction == "BUY" else "WATCH_SHORT"
    packet = AdvicePacket(
        decision=decision,
        bias=bias,  # type: ignore[arg-type]
        confidence=confidence,  # type: ignore[arg-type]
        horizon=_HORIZON,
        summary=f"当前{_trend_cn(bias)}，关注 {zone.low:.2f}–{zone.high:.2f} 的人工确认机会；未进入或未确认前不追价。",
        current_price=round(price, 2),
        primary_setup=setup,
        alternative_scenario=alternative,
        market_context=context,
        risks=risks,
        uncertainties=["建议基于当前快照；价格到达关注区时应重新核对结构与事件风险"],
        evidence=evidence,
    )
    audited = audit_advice(packet)
    if not audited.passed:
        packet = _no_setup_packet(
            decision="AVOID",
            bias=bias,
            confidence="low",
            price=price,
            context=context,
            summary="候选建议未通过一致性审核，本次不形成交易建议。",
            risks=risks,
            uncertainties=audited.violations,
            evidence=evidence,
        )
        packet.audit.warnings.extend(audited.warnings)
        return packet
    return replace(packet, audit=audited)
