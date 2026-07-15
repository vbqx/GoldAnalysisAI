"""SMC + DGT Price Action narrative combination helpers.

Rules (also documented in docs/architecture/smc-pa-narrative.md):
- SMC owns structure direction, OB/FVG, BOS/CHoCH, swing liquidity, trade entry zones.
- PA owns POC/VAH/VAL, volume S/R, spikes; used to confirm or qualify SMC levels.
- Resonance: when SMC zone and PA level are within tolerance, call it out explicitly.
"""

from __future__ import annotations

from typing import Any

from src.analysis.dgt_price_action import DEFAULT_LOOKBACK
from src.analysis.field_glossary import PA_SUMMARY_HINT

RESONANCE_TOLERANCE = 8.0  # XAUUSD points

COMBINATION_RULES: dict[str, str] = {
    "market_overview": "多周期 PA 价值区投票定主方向；当日(session) POC/VA 定日内成交控制区；PA 交易计划入场区单独标注。",
    "liquidity": "仅 PA 日内(session) 量价 S/R 与 VAH/VAL；上方阻力、下方支撑分侧叙述；5m 仅用于入场计划。",
    "4h": "仅 PA：该周期 Fixed-360 POC/VA 与现价区位；放量/高波动线作大级别阻力支撑；禁止套用 5m/session POC。",
    "1h": "仅 PA：该周期 Fixed-360 POC/VA 与近端量价阻力支撑；不写 BOS/CHoCH/OB。",
    "15m": "仅 PA：该周期 Fixed-360 POC/VA、近端 S/R；触发条件基于量价收回/拒绝。",
    "trading_plans": "PA 定入场/止损/止盈；SMC 仅作计划评分过滤，不进文案主干。",
    "llm": "黄金日内：4H/1H 定方向，15m/5m 定执行；各周期量价独立；只能引用 allowed_levels / price_action_summary 价格。",
}


def _fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "—"
    return f"{number:.0f}" if number.is_integer() else f"{number:.2f}".rstrip("0").rstrip(".")


def pa_block(report: dict[str, Any], tf: str) -> dict[str, Any]:
    return (report.get("price_action") or {}).get(tf) or {}


def value_zone_position(price: float | None, vp: dict[str, Any]) -> str:
    if price is None or not vp.get("poc"):
        return ""
    vah, val = vp.get("vah"), vp.get("val")
    if vah is not None and float(price) > float(vah):
        return "现价在量价价值区上方"
    if val is not None and float(price) < float(val):
        return "现价在量价价值区下方"
    if val is not None and vah is not None:
        return "现价在量价价值区内"
    return ""


def nearest_pa_sr(
    sr_levels: list[dict[str, Any]],
    price: float | None,
    direction: str,
    *,
    limit: int = 3,
) -> list[str]:
    if price is None:
        return []
    parsed = [
        lvl
        for lvl in sr_levels
        if lvl.get("direction") == direction and lvl.get("price") is not None
    ]
    if direction == "resistance":
        parsed = [lvl for lvl in parsed if float(lvl["price"]) >= float(price) * 0.998]
        parsed.sort(key=lambda x: float(x["price"]))
    else:
        parsed = [lvl for lvl in parsed if float(lvl["price"]) <= float(price) * 1.002]
        parsed.sort(key=lambda x: -float(x["price"]))
    out: list[str] = []
    seen: set[float] = set()
    for lvl in parsed:
        p = round(float(lvl["price"]), 2)
        if p in seen:
            continue
        seen.add(p)
        kind = str(lvl.get("label") or lvl.get("kind") or "S/R")
        out.append(f"{_fmt(p)}({kind})")
        if len(out) >= limit:
            break
    return out


def zone_midpoint(zone: str | None) -> float | None:
    if not zone or "-" not in zone:
        return None
    parts = zone.replace(" ", "").split("-")
    try:
        return (float(parts[0]) + float(parts[1])) / 2
    except (TypeError, ValueError):
        return None


def resonance_note(
    smc_zone: str | None,
    pa_prices: list[float],
    *,
    tolerance: float = RESONANCE_TOLERANCE,
) -> str:
    mid = zone_midpoint(smc_zone)
    if mid is None or not pa_prices:
        return ""
    for p in pa_prices:
        if abs(p - mid) <= tolerance:
            return "，与量价位共振"
    return ""


def entry_resonance_text(
    signal: dict[str, Any],
    pa_block_5m: dict[str, Any],
    *,
    tolerance: float = RESONANCE_TOLERANCE,
) -> str:
    el, eh = signal.get("entry_low"), signal.get("entry_high")
    if el is None or eh is None:
        return ""
    mid = (float(el) + float(eh)) / 2
    vp = pa_block_5m.get("volume_profile") or {}
    notes: list[str] = []
    for key, label in (("vah", "VAH"), ("val", "VAL"), ("poc", "POC")):
        val = vp.get(key)
        if val is not None and abs(float(val) - mid) <= tolerance:
            notes.append(label)
    sr_prices = [float(x["price"]) for x in pa_block_5m.get("sr_levels") or [] if x.get("price") is not None]
    for p in sr_prices:
        if abs(p - mid) <= tolerance:
            notes.append("量价S/R")
            break
    if not notes:
        return ""
    return f"（贴近{'/'.join(dict.fromkeys(notes))}共振）"


def pa_trend_label(price: float | None, vp: dict[str, Any]) -> str:
    """Infer trend wording from price vs PA value area only."""
    pos = value_zone_position(price, vp)
    if "上方" in pos:
        return "偏多"
    if "下方" in pos:
        return "偏空"
    if pos:
        return "震荡"
    return "待确认"


def liquidity_pa_side_text(side_label: str, pa_labels: list[str]) -> str | None:
    if not pa_labels:
        return None
    return f"{side_label}：量价 " + " / ".join(pa_labels) + "。"


def tf_pa_structure_levels(
    pa_tf: dict[str, Any],
    price: float | None,
    *,
    tf: str,
) -> list[str]:
    """Up to two PA level lines for 4h/1h/15m panels."""
    levels: list[str] = []
    vp = pa_tf.get("volume_profile") or {}
    sr = pa_tf.get("sr_levels") or []
    if vp.get("poc") is not None and vp.get("vah") is not None and vp.get("val") is not None:
        levels.append(
            f"POC {_fmt(vp['poc'])}，VA {_fmt(vp['val'])}-{_fmt(vp['vah'])}。"
        )
    resist = nearest_pa_sr(sr, price, "resistance", limit=2)
    support = nearest_pa_sr(sr, price, "support", limit=2)
    if resist and len(levels) < 2:
        levels.append("阻力：" + " / ".join(resist) + "。")
    if support and len(levels) < 2:
        levels.append("支撑：" + " / ".join(support) + "。")
    if tf == "15m" and not resist and vp.get("vah") is not None:
        levels.append(f"近端 VAH 拒绝参考 {_fmt(vp['vah'])}。")
    return levels[:2]


def tf_pa_condition(tf: str, *, trend: str, vp: dict[str, Any]) -> str:
    if tf == "15m":
        return "等待量价关键区收回或拒绝确认，现价不追单。"
    if trend == "偏多":
        return "回踩 POC/VAL 守住可维持修复；有效跌破 VAL 转等待。"
    if trend == "偏空":
        return "反抽 POC/VAH 受阻可维持回落；有效站上 VAH 转等待。"
    return "价值区内保持等待，突破 VA 边界并回踩确认后再跟随。"


def tf_pa_invalidation(trend: str, vp: dict[str, Any]) -> str:
    vah, val = vp.get("vah"), vp.get("val")
    if trend == "偏多" and vah is not None:
        return f"有效跌破 VAL {_fmt(val)} 后，当前偏多量价假设失效。"
    if trend == "偏空" and val is not None:
        return f"有效站上 VAH {_fmt(vah)} 后，当前偏空量价假设失效。"
    if vah is not None and val is not None:
        return f"有效脱离 VA {_fmt(val)}-{_fmt(vah)} 且无法收回时，当前判断失效。"
    return "关键量价位被有效突破前，不确认新的单边路径。"


def liquidity_side_text(
    side_label: str,
    smc_rows: list[dict[str, Any]],
    pa_labels: list[str],
) -> str | None:
    parts: list[str] = []
    if smc_rows:
        parts.append("结构 " + " / ".join(_fmt(x["price"]) for x in smc_rows[:4]))
    if pa_labels:
        parts.append("量价 " + " / ".join(pa_labels))
    if not parts:
        return None
    return f"{side_label}：" + "；".join(parts) + "。"


def tf_pa_context_line(tf: str, vp: dict[str, Any], price: float | None) -> str:
    if not vp.get("poc"):
        return ""
    poc, vah, val = vp.get("poc"), vp.get("vah"), vp.get("val")
    pos = value_zone_position(price, vp)
    base = f"量价 POC {_fmt(poc)}"
    if vah is not None and val is not None:
        base += f"，VA {_fmt(val)}-{_fmt(vah)}"
    if pos and tf in ("1h", "15m", "5m"):
        base += f"，{pos}"
    return base


def build_pa_llm_summary(
    price_action: dict[str, Any],
    *,
    price: float | None,
) -> dict[str, Any]:
    """Compact per-TF PA facts for LLM (technical / narrative / levels).

    Each of 5m/15m/1h/4h is an independent Fixed-360 profile; ``session`` is
    day-anchored. Always preserve lookback + profile_source so models do not
    treat HTF POC as interchangeable with 5m/session.
    """
    out: dict[str, Any] = {}
    for tf, block in price_action.items():
        if not isinstance(block, dict):
            continue
        vp = block.get("volume_profile") or {}
        sr = block.get("sr_levels") or []
        lookback_mode = block.get("lookback_mode") or ("session" if tf == "session" else "fixed")
        lookback_requested = block.get("lookback_requested")
        if lookback_requested is None and lookback_mode == "fixed":
            lookback_requested = DEFAULT_LOOKBACK
        out[tf] = {
            "lookback_mode": lookback_mode,
            "lookback_requested": lookback_requested,
            "lookback_bars": block.get("lookback_bars"),
            "profile_source": block.get("profile_source")
            or ("session" if lookback_mode == "session" else "native_tf"),
            "volume_ok": block.get("volume_ok"),
            "volume_spike_count": block.get("volume_spike_count"),
            "high_volatility_count": block.get("high_volatility_count"),
            "poc": vp.get("poc"),
            "vah": vp.get("vah"),
            "val": vp.get("val"),
            "value_zone_position": value_zone_position(price, vp),
            "nearest_resistance": nearest_pa_sr(sr, price, "resistance", limit=4),
            "nearest_support": nearest_pa_sr(sr, price, "support", limit=4),
            "supply_demand_zone_count": len(vp.get("supply_demand_zones") or []),
        }
    if out:
        out["_hint"] = PA_SUMMARY_HINT
    return out
