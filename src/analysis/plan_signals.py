"""PA-primary trading plans with SMC as score filter only.

Entry / stop / targets come from DGT volume profile and S/R levels.
SMC OB/FVG overlap and BOS/CHoCH only adjust confidence — plans are never blocked.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.analysis.ict_pa import TimeframeAnalysis
from src.analysis.narrative_combine import RESONANCE_TOLERANCE
from src.config import SIGNAL_SL_BELOW_SWING, SIGNAL_SWEEP_OFFSET


@dataclass
class _PaZone:
    entry_low: float
    entry_high: float
    label: str


@dataclass
class _SmcFilter:
    bonus: float
    reasons: list[str]


def pa_usable(price_action: dict[str, Any] | None) -> bool:
    if not price_action:
        return False
    block = price_action.get("5m") or {}
    vp = block.get("volume_profile") or {}
    sr = block.get("sr_levels") or []
    if vp.get("poc") is not None or vp.get("vah") is not None:
        return True
    return bool(sr)


def _rule_sr_level(price: float, direction: str, label: str) -> dict[str, Any]:
    return {
        "price": round(float(price), 2),
        "direction": direction,
        "kind": "rule_anchor",
        "label": label,
        "time": "",
    }


def build_rule_pa_block(
    *,
    price: float,
    swing_high: float,
    swing_low: float,
    analysis_5m: TimeframeAnalysis,
    price_action: dict[str, Any] | None = None,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Synthesize minimal 5m PA facts from price anchors when DGT output is insufficient."""
    pa5 = (price_action or {}).get("5m") or {}
    existing_vp = pa5.get("volume_profile") or {}
    metrics = metrics or {}
    vp: dict[str, Any] = {}

    for key in ("poc", "vah", "val", "profile_high", "profile_low"):
        if existing_vp.get(key) is not None:
            vp[key] = existing_vp[key]

    daily_high = metrics.get("daily_high")
    daily_low = metrics.get("daily_low")
    recent_high = analysis_5m.recent_high
    recent_low = analysis_5m.recent_low

    above_candidates = [
        vp.get("vah"),
        vp.get("profile_high"),
        recent_high,
        daily_high,
        analysis_5m.swing_high,
        swing_high,
    ]
    below_candidates = [
        vp.get("val"),
        vp.get("profile_low"),
        recent_low,
        daily_low,
        analysis_5m.swing_low,
        swing_low,
    ]

    above = [float(x) for x in above_candidates if x is not None and float(x) >= float(price) * 0.998]
    below = [float(x) for x in below_candidates if x is not None and float(x) <= float(price) * 1.002]

    if vp.get("vah") is None and above:
        vp["vah"] = round(min(above), 2)
    if vp.get("val") is None and below:
        vp["val"] = round(max(below), 2)
    if vp.get("poc") is None:
        if vp.get("vah") is not None and vp.get("val") is not None:
            vp["poc"] = round((float(vp["vah"]) + float(vp["val"])) / 2, 2)
        else:
            vp["poc"] = round(float(price), 2)

    sr_levels = list(pa5.get("sr_levels") or [])
    has_res = any(lvl.get("direction") == "resistance" for lvl in sr_levels)
    has_sup = any(lvl.get("direction") == "support" for lvl in sr_levels)

    if not has_res and above:
        anchor = min(above)
        label = "日内高点" if daily_high is not None and abs(anchor - float(daily_high)) < 0.02 else "规则阻力"
        sr_levels.append(_rule_sr_level(anchor, "resistance", label))
    if not has_sup and below:
        anchor = max(below)
        label = "日内低点" if daily_low is not None and abs(anchor - float(daily_low)) < 0.02 else "规则支撑"
        sr_levels.append(_rule_sr_level(anchor, "support", label))

    return {
        "timeframe": "5m",
        "volume_ok": bool(pa5.get("volume_ok")),
        "rule_fallback": True,
        "volume_profile": vp,
        "sr_levels": sr_levels,
    }


def _atr(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis) -> float:
    return analysis_5m.atr or analysis_15m.atr or 5.0


def _zone_band(center: float, atr: float, *, ratio: float = 0.2) -> tuple[float, float]:
    half = max(atr * ratio, 1.5)
    return round(center - half, 2), round(center + half * 0.6, 2)


def _nearest_pa_sr(
    sr_levels: list[dict[str, Any]],
    price: float,
    direction: str,
) -> dict[str, Any] | None:
    parsed = [
        lvl
        for lvl in sr_levels
        if lvl.get("direction") == direction and lvl.get("price") is not None
    ]
    if direction == "resistance":
        # Short zones must sit at/above market — never pick support-turned-resistance below price.
        parsed = [lvl for lvl in parsed if float(lvl["price"]) >= float(price)]
        parsed.sort(key=lambda x: float(x["price"]))
    else:
        parsed = [lvl for lvl in parsed if float(lvl["price"]) <= float(price)]
        parsed.sort(key=lambda x: -float(x["price"]))
    return parsed[0] if parsed else None


def _vah_zone(vp: dict[str, Any], atr: float) -> _PaZone | None:
    vah = vp.get("vah")
    if vah is None:
        return None
    el, eh = _zone_band(float(vah), atr, ratio=0.18)
    return _PaZone(el, eh, "VAH 拒绝区")


def _resistance_zone(sr: dict[str, Any], atr: float) -> _PaZone:
    price = float(sr["price"])
    el, eh = _zone_band(price, atr, ratio=0.15)
    label = str(sr.get("label") or "量价阻力")
    return _PaZone(el, eh, label)


def _val_zone(vp: dict[str, Any], atr: float) -> _PaZone | None:
    val = vp.get("val")
    if val is None:
        return None
    el, eh = _zone_band(float(val), atr, ratio=0.18)
    return _PaZone(el, eh, "VAL 支撑区")


def _support_zone(sr: dict[str, Any], atr: float) -> _PaZone:
    price = float(sr["price"])
    el, eh = _zone_band(price, atr, ratio=0.15)
    label = str(sr.get("label") or "量价支撑")
    return _PaZone(round(price - max(atr * 0.15, 1.5), 2), round(price, 2), label)


def _sell_targets(
    entry_low: float,
    entry_high: float,
    *,
    poc: float | None,
    val: float | None,
    swing_low: float,
) -> tuple[float, float, float] | None:
    from src.analysis.signal_geometry import normalize_take_profits

    entry_mid = (entry_low + entry_high) / 2
    zone_width = max(entry_high - entry_low, 0.01)
    candidates: list[float] = [
        round(entry_mid - max(zone_width * 1.5, entry_mid * 0.003), 2),
    ]
    if poc is not None:
        poc_tp = round(float(poc), 2)
        if poc_tp < entry_mid:
            candidates.append(poc_tp)
    candidates.append(round(swing_low + (entry_mid - swing_low) * 0.35, 2))
    if val is not None:
        val_tp = round(float(val), 2)
        if val_tp < entry_mid:
            candidates.append(val_tp)
    candidates.append(round(swing_low, 2))

    ordered = normalize_take_profits(
        direction="SELL",
        theme="short",
        entry_low=entry_low,
        entry_high=entry_high,
        take_profits=candidates,
    )
    if len(ordered) < 3:
        return None
    tp1, tp2, tp3 = ordered[0], ordered[1], ordered[2]
    if tp1 >= entry_mid or tp3 >= tp1:
        return None
    return tp1, tp2, tp3


def _buy_targets(
    entry_low: float,
    entry_high: float,
    *,
    price: float,
    poc: float | None,
    vah: float | None,
    swing_high: float,
    swing_low: float,
) -> tuple[float, float, float]:
    from src.analysis.signal_geometry import normalize_take_profits

    entry_mid = (entry_low + entry_high) / 2
    candidates: list[float] = [round(price, 2)]
    if poc is not None:
        poc_tp = round(float(poc), 2)
        if poc_tp > entry_mid:
            candidates.append(poc_tp)
    candidates.append(round(swing_low + (swing_high - swing_low) * 0.382, 2))
    if vah is not None:
        vah_tp = round(float(vah), 2)
        if vah_tp > entry_mid:
            candidates.append(vah_tp)
    candidates.append(round(swing_low + (swing_high - swing_low) * 0.5, 2))

    ordered = normalize_take_profits(
        direction="BUY",
        theme="long",
        entry_low=entry_low,
        entry_high=entry_high,
        take_profits=candidates,
    )
    if len(ordered) >= 3:
        return ordered[0], ordered[1], ordered[2]
    while len(ordered) < 3:
        ordered.append(round(ordered[-1] + max(entry_mid * 0.002, 1.0), 2))
    return ordered[0], ordered[1], ordered[2]


def _smc_zones(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis) -> list[tuple[float, float, str]]:
    zones: list[tuple[float, float, str]] = []
    for analysis in (analysis_5m, analysis_15m):
        for ob in analysis.order_blocks:
            zones.append((ob.low, ob.high, "OB"))
        for fvg in analysis.fvgs:
            zones.append((fvg.low, fvg.high, "FVG"))
    return zones


def _zone_overlaps_entry(
    zone_low: float,
    zone_high: float,
    entry_low: float,
    entry_high: float,
    *,
    tolerance: float = RESONANCE_TOLERANCE,
) -> bool:
    mid = (entry_low + entry_high) / 2
    zone_mid = (zone_low + zone_high) / 2
    if abs(zone_mid - mid) <= tolerance:
        return True
    return not (zone_high < entry_low - tolerance or zone_low > entry_high + tolerance)


def _structure_shifted(
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
    *,
    direction: str,
) -> bool:
    want = direction.lower()
    return any(
        (event.direction or "").lower() == want
        and (event.kind or "").upper() in ("BOS", "CHOCH")
        for analysis in (analysis_5m, analysis_15m)
        for event in analysis.events
    )


def smc_filter_adjustment(
    *,
    direction: str,
    entry_low: float,
    entry_high: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
) -> _SmcFilter:
    """Score-only SMC filter; never suppresses a PA plan."""
    bonus = 0.0
    reasons: list[str] = []
    theme = "short" if direction == "SELL" else "long"
    events = [
        event
        for analysis in (analysis_5m, analysis_15m)
        for event in analysis.events
        if (event.kind or "").upper() in ("BOS", "CHOCH")
    ]
    aligned = [e for e in events if e.direction == ("bearish" if theme == "short" else "bullish")]
    counter = [e for e in events if e.direction == ("bullish" if theme == "short" else "bearish")]

    if aligned:
        bonus += 8.0
        kinds = "/".join(sorted({(e.kind or "").upper() for e in aligned}))
        reasons.append(f"SMC {kinds} 与 PA 方向一致 (+8)")
    elif counter:
        bonus -= 10.0
        reasons.append("SMC 结构反向，PA 计划降分 (-10)")
    else:
        bonus -= 3.0
        reasons.append("SMC 无明确结构确认，仅作参考 (-3)")

    resonance = False
    for zl, zh, kind in _smc_zones(analysis_5m, analysis_15m):
        if _zone_overlaps_entry(zl, zh, entry_low, entry_high):
            resonance = True
            bonus += 6.0
            reasons.append(f"SMC {kind} 与 PA 入场区共振 (+6)")
            break
    if not resonance:
        bonus -= 4.0
        reasons.append("SMC 结构区未对齐 PA 价位 (-4)")

    return _SmcFilter(bonus=bonus, reasons=reasons)


def val_sweep_confirmed(
    *,
    price: float,
    val: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
) -> tuple[bool, list[str]]:
    """PA VAL sweep + reclaim; CHoCH/BOS bullish is SMC filter, not hard gate."""
    recent_low = analysis_5m.recent_low
    close = analysis_5m.last_close if analysis_5m.last_close is not None else price
    atr = _atr(analysis_5m, analysis_15m)
    sweep_buffer = max(atr * 0.10, 0.5)
    swept = recent_low is not None and float(recent_low) < float(val) - sweep_buffer
    reclaimed = float(close) > float(val)
    shifted = _structure_shifted(analysis_5m, analysis_15m, direction="bullish")
    reasons: list[str] = []
    if swept:
        reasons.append("VAL 下方流动性已扫")
    else:
        reasons.append("尚未扫过 VAL")
    if reclaimed:
        reasons.append("收盘收回 VAL 上方")
    else:
        reasons.append("尚未收回 VAL")
    if shifted:
        reasons.append("SMC 结构转强确认")
    confirmed = swept and reclaimed and shifted
    if confirmed:
        reasons.append("PA sweep + reclaim confirmed")
    return confirmed, reasons


def build_pa_short_aggressive(
    *,
    price: float,
    pa_block: dict[str, Any],
    swing_low: float,
    atr: float,
) -> tuple[_PaZone, float, list[float]] | None:
    sr = _nearest_pa_sr(pa_block.get("sr_levels") or [], price, "resistance")
    if sr is None:
        return None
    zone = _resistance_zone(sr, atr)
    if zone.entry_high < float(price):
        return None
    vp = pa_block.get("volume_profile") or {}
    targets = _sell_targets(
        zone.entry_low,
        zone.entry_high,
        poc=vp.get("poc"),
        val=vp.get("val"),
        swing_low=swing_low,
    )
    if targets is None:
        return None
    zone_width = max(zone.entry_high - zone.entry_low, 0.01)
    sl = round(zone.entry_high + max(zone_width, atr * 0.35), 2)
    return zone, sl, list(targets)


def build_pa_short_conservative(
    *,
    price: float,
    pa_block: dict[str, Any],
    swing_low: float,
    atr: float,
) -> tuple[_PaZone, float, list[float]] | None:
    vp = pa_block.get("volume_profile") or {}
    zone = _vah_zone(vp, atr)
    if zone is None:
        sr = _nearest_pa_sr(pa_block.get("sr_levels") or [], price, "resistance")
        if sr is None:
            return None
        zone = _resistance_zone(sr, atr)
    targets = _sell_targets(
        zone.entry_low,
        zone.entry_high,
        poc=vp.get("poc"),
        val=vp.get("val"),
        swing_low=swing_low,
    )
    if targets is None:
        return None
    zone_width = max(zone.entry_high - zone.entry_low, 0.01)
    sl = round(zone.entry_high + max(zone_width * 1.2, atr * 0.45), 2)
    return zone, sl, list(targets)


def build_pa_long_sweep(
    *,
    price: float,
    pa_block: dict[str, Any],
    swing_high: float,
    swing_low: float,
    analysis_5m: TimeframeAnalysis,
    analysis_15m: TimeframeAnalysis,
) -> tuple[_PaZone, float, list[float], bool, list[str]] | None:
    vp = pa_block.get("volume_profile") or {}
    atr = _atr(analysis_5m, analysis_15m)
    val = vp.get("val")
    if val is not None:
        sweep_offset = max(atr * 0.35, SIGNAL_SWEEP_OFFSET)
        stop_buffer = max(atr * 0.65, SIGNAL_SL_BELOW_SWING)
        entry_low = round(float(val) - sweep_offset, 2)
        entry_high = round(float(val), 2)
        sl = round(float(val) - stop_buffer, 2)
        zone = _PaZone(entry_low, entry_high, "VAL 扫低收回")
        confirmed, sweep_reasons = val_sweep_confirmed(
            price=price,
            val=float(val),
            analysis_5m=analysis_5m,
            analysis_15m=analysis_15m,
        )
    else:
        sr = _nearest_pa_sr(pa_block.get("sr_levels") or [], price, "support")
        if sr is None:
            return None
        zone = _support_zone(sr, atr)
        sweep_offset = max(atr * 0.35, SIGNAL_SWEEP_OFFSET)
        stop_buffer = max(atr * 0.65, SIGNAL_SL_BELOW_SWING)
        support_price = float(sr["price"])
        entry_low = round(support_price - sweep_offset, 2)
        entry_high = round(support_price, 2)
        sl = round(support_price - stop_buffer, 2)
        zone = _PaZone(entry_low, entry_high, zone.label)
        confirmed = False
        sweep_reasons = ["量价支撑待扫低收回"]

    tps = list(
        _buy_targets(
            zone.entry_low,
            zone.entry_high,
            price=price,
            poc=vp.get("poc"),
            vah=vp.get("vah"),
            swing_high=swing_high,
            swing_low=swing_low,
        )
    )
    return zone, sl, tps, confirmed, sweep_reasons
