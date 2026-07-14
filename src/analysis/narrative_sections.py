"""Institutional narrative sections shared by rule and LLM report paths."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from src.analysis.narrative_combine import (
    COMBINATION_RULES,
    build_pa_llm_summary,
    entry_resonance_text,
    liquidity_pa_side_text,
    nearest_pa_sr,
    pa_block,
    pa_trend_label,
    tf_pa_condition,
    tf_pa_context_line,
    tf_pa_invalidation,
    tf_pa_structure_levels,
    value_zone_position,
)

SECTION_KEYS = ("market_overview", "liquidity", "4h", "1h", "15m")
OVERVIEW_VOLUME_FALLBACK_TFS = ("15m", "5m")
LIQUIDITY_PA_FALLBACK_TFS = ("15m", "1h")
SECTION_FIELDS = ("summary", "context", "levels", "conditions", "invalidation")
MAX_VISIBLE_LINES = 6
_SECTION_LIST_CAPS = {"context": 1, "levels": 2, "conditions": 1}
# XAUUSD prices are 1000+; skip DXY (~100), yields, % and other macro prints.
_PRICE_TOKEN_MIN = 500.0

_NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?")


def _fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "—"
    return f"{number:.0f}" if number.is_integer() else f"{number:.2f}".rstrip("0").rstrip(".")


def _section(
    summary: str,
    *,
    context: list[str] | None = None,
    levels: list[str] | None = None,
    conditions: list[str] | None = None,
    invalidation: str = "",
) -> dict[str, Any]:
    section = {
        "summary": summary.strip(),
        "context": [x for x in (context or []) if x][:1],
        "levels": [x for x in (levels or []) if x][:2],
        "conditions": [x for x in (conditions or []) if x][:1],
        "invalidation": invalidation.strip(),
        "source": "rule",
        "confidence": 1.0,
        "fallback_reason": None,
    }
    return section


def _intraday_pa_block(report: dict[str, Any]) -> dict[str, Any]:
    """Session-day PA block when available."""
    return (report.get("price_action") or {}).get("session") or {}


def _overview_volume_context(report: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Prefer session-day POC/VA; fall back to 15m then 5m."""
    session = _intraday_pa_block(report)
    if (session.get("volume_profile") or {}).get("poc") is not None:
        return session, "当日"
    for tf in OVERVIEW_VOLUME_FALLBACK_TFS:
        block = pa_block(report, tf)
        if (block.get("volume_profile") or {}).get("poc") is not None:
            return block, tf
    return pa_block(report, "15m"), "15m"


def _liquidity_pa_context(report: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Intraday liquidity narrative uses session S/R; 5m reserved for entry plans only."""
    session = _intraday_pa_block(report)
    if session.get("sr_levels") or (session.get("volume_profile") or {}).get("poc") is not None:
        return session, "日内"
    for tf in LIQUIDITY_PA_FALLBACK_TFS:
        block = pa_block(report, tf)
        if block.get("sr_levels") or (block.get("volume_profile") or {}).get("poc") is not None:
            return block, tf
    return pa_block(report, "15m"), "15m"


def build_rule_narrative_sections(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build deterministic, screenshot-density copy from report facts."""
    metrics = report.get("metrics") or {}
    price = metrics.get("current_price")
    daily_low, daily_high = metrics.get("daily_low"), metrics.get("daily_high")
    conclusion = report.get("conclusion") or {}
    signals = [s for s in (report.get("signals") or []) if s.get("status") != "invalid" and s.get("signal_role") != "rejected"]
    primary = next((s for s in signals if s.get("signal_role") == "primary"), signals[0] if signals else {})

    trends = [pa_trend_label(price, (pa_block(report, tf).get("volume_profile") or {})) for tf in ("4h", "1h", "15m")]
    dominant = max(set(trends), key=trends.count) if trends else "待确认"
    aligned = len(set(trends)) == 1
    overview_context = (
        f"4H、1H、15m 量价价值区一致，当前以{dominant}路径为主。"
        if aligned
        else "多周期量价价值区分歧，当前以关键量价位确认后的路径为准。"
    )
    overview_levels = []
    pa_overview, volume_label = _overview_volume_context(report)
    vp_overview = pa_overview.get("volume_profile") or {}
    if daily_low is not None and daily_high is not None:
        day_part = f"日内已走 {_fmt(daily_low)}-{_fmt(daily_high)}"
        if vp_overview.get("poc") is not None:
            overview_levels.append(
                f"{day_part}；{volume_label} POC {_fmt(vp_overview['poc'])}，"
                f"VA {_fmt(vp_overview.get('val'))}-{_fmt(vp_overview.get('vah'))}。"
            )
        else:
            overview_levels.append(f"{day_part}。")
    elif vp_overview.get("poc") is not None:
        overview_levels.append(
            f"{volume_label} POC {_fmt(vp_overview['poc'])}，"
            f"价值区 {_fmt(vp_overview.get('val'))}-{_fmt(vp_overview.get('vah'))}。"
        )
    if primary.get("entry_low") is not None and primary.get("entry_high") is not None:
        resonance = entry_resonance_text(primary, pa_overview)
        overview_levels.append(
            f"PA 入场区 {_fmt(primary['entry_low'])}-{_fmt(primary['entry_high'])}{resonance}。"
        )
    va_pos = value_zone_position(price, vp_overview)
    overview_summary = f"现价{_fmt(price)}附近，日内主方向为{dominant}"
    if va_pos:
        overview_summary += f"，{va_pos}"
    overview_summary += "。"
    condition = str(conclusion.get("action") or "等待价格到达关键区域后再确认，不在区间中部追单。")
    invalidation = str(conclusion.get("direction_summary") or "关键结构被反向突破后，当前判断失效并重新评估。")
    sections = {
        "market_overview": _section(
            overview_summary,
            context=[overview_context], levels=overview_levels,
            conditions=[condition], invalidation=invalidation,
        )
    }

    pa_liq, liq_label = _liquidity_pa_context(report)
    pa_liq_sr = pa_liq.get("sr_levels") or []
    vp_liq = pa_liq.get("volume_profile") or {}
    liq_levels = []
    pa_res_above = nearest_pa_sr(pa_liq_sr, price, "resistance", limit=3)
    pa_res_below = nearest_pa_sr(pa_liq_sr, price, "support", limit=3)
    above_line = liquidity_pa_side_text("上方", pa_res_above)
    below_line = liquidity_pa_side_text("下方", pa_res_below)
    if above_line:
        liq_levels.append(above_line)
    if below_line:
        liq_levels.append(below_line)
    if not liq_levels and vp_liq.get("poc") is not None:
        liq_levels.append(
            f"{liq_label} POC {_fmt(vp_liq['poc'])}，VA {_fmt(vp_liq.get('val'))}-{_fmt(vp_liq.get('vah'))}。"
        )
    nearest_above = pa_res_above[0].split("(")[0] if pa_res_above else "上方最近量价位"
    nearest_below = pa_res_below[0].split("(")[0] if pa_res_below else "下方最近量价位"
    sections["liquidity"] = _section(
        "量价支撑阻力为主：先扫过关键线再收回，再谈反转。",
        context=[f"{liq_label}连续量价/放量衰竭/高波动线反映成交密集区；POC/VAH/VAL 定价值区。"],
        levels=liq_levels,
        conditions=[f"扫过{nearest_above}后跌回可观察空头；扫过{nearest_below}后收回可观察多头。"],
        invalidation="价格持续站在被突破量价位外侧时，反转假设失效。",
    )

    roles = {
        "4h": "大级别背景",
        "1h": "当前结构阶段",
        "15m": "执行前结构",
    }
    for tf in ("4h", "1h", "15m"):
        pa_tf = pa_block(report, tf)
        vp_tf = pa_tf.get("volume_profile") or {}
        trend = pa_trend_label(price, vp_tf)
        pa_line = tf_pa_context_line(tf, vp_tf, price)
        spike_n = int(pa_tf.get("volume_spike_count") or 0)
        hv_n = int(pa_tf.get("high_volatility_count") or 0)
        structure = pa_line or "量价 Profile 待确认"
        if spike_n or hv_n:
            extras = []
            if spike_n:
                extras.append(f"放量衰竭 {spike_n} 处")
            if hv_n:
                extras.append(f"高波动 {hv_n} 处")
            structure += " · " + "，".join(extras)
        structure += "。"
        levels = tf_pa_structure_levels(pa_tf, price, tf=tf)
        condition = tf_pa_condition(tf, trend=trend, vp=vp_tf)
        invalidation = tf_pa_invalidation(trend, vp_tf)
        sections[tf] = _section(
            f"{roles[tf]}：{trend}。",
            context=[structure], levels=levels, conditions=[condition], invalidation=invalidation,
        )
    return sections


def section_to_bullets(section: dict[str, Any]) -> list[str]:
    """Flatten one narrative section into legacy bullet lines."""
    rows: list[str] = []
    if section.get("summary"):
        rows.append(str(section["summary"]))
    rows.extend(str(x) for x in section.get("context") or [])
    rows.extend(str(x) for x in section.get("levels") or [])
    rows.extend(str(x) for x in section.get("conditions") or [])
    if section.get("invalidation"):
        rows.append(str(section["invalidation"]))
    return [row for row in rows if row.strip()]


def overview_bullets_from_sections(sections: dict[str, dict[str, Any]]) -> list[str]:
    """Legacy `market_overview` list derived from canonical narrative_sections."""
    return section_to_bullets(sections.get("market_overview") or {})[:6]


def build_narrative_facts(
    report: dict[str, Any],
    technical_context: dict[str, Any],
    *,
    compact_for_llm: bool = False,
) -> dict[str, Any]:
    """Compact, auditable facts sent to the final narrative LLM."""
    context_levels: list[dict[str, Any]] = []
    authorized_execution_levels: list[dict[str, Any]] = []

    def add_context(level_id: str, value: Any, source: str, *, timeframe: str | None = None, kind: str = "level") -> None:
        if value is None:
            return
        try:
            number = round(float(value), 2)
        except (TypeError, ValueError):
            return
        context_levels.append(
            {"id": level_id, "price": number, "source": source, "timeframe": timeframe, "kind": kind}
        )

    def add_execution(level_id: str, value: Any, source: str, *, signal_id: str, kind: str = "execution") -> None:
        if value is None:
            return
        try:
            number = round(float(value), 2)
        except (TypeError, ValueError):
            return
        authorized_execution_levels.append(
            {
                "id": level_id,
                "price": number,
                "source": source,
                "signal_id": signal_id,
                "kind": kind,
            }
        )

    metrics = report.get("metrics") or {}
    for key in ("current_price", "daily_low", "daily_high", "prev_close"):
        add_context(f"metrics.{key}", metrics.get(key), f"metrics.{key}")
    for idx, row in enumerate(report.get("liquidity") or []):
        add_context(
            f"liquidity.{idx}",
            row.get("price"),
            str(row.get("label") or "liquidity"),
            timeframe=row.get("timeframe"),
            kind=str(row.get("kind") or "liquidity"),
        )
    for tf, info in (report.get("timeframes") or {}).items():
        add_context(f"{tf}.swing_high", info.get("swing_high"), "swing_high", timeframe=tf)
        add_context(f"{tf}.swing_low", info.get("swing_low"), "swing_low", timeframe=tf)
        for group in ("order_blocks", "fvgs"):
            for idx, row in enumerate(info.get(group) or []):
                add_context(f"{tf}.{group}.{idx}.low", row.get("low"), group, timeframe=tf, kind="zone_low")
                add_context(f"{tf}.{group}.{idx}.high", row.get("high"), group, timeframe=tf, kind="zone_high")
    authorized_signals = [
        s
        for s in (report.get("signals") or [])
        if s.get("signal_role") in ("primary", "alternate")
    ]
    for signal in authorized_signals:
        sid = str(signal.get("signal_id") or "unknown")
        for key in ("entry_low", "entry_high", "stop_loss"):
            add_execution(f"{sid}.{key}", signal.get(key), key, signal_id=sid, kind="validated_signal")
        try:
            entry_low = float(signal["entry_low"])
            entry_high = float(signal["entry_high"])
            add_execution(
                f"{sid}.entry_mid",
                (entry_low + entry_high) / 2.0,
                "entry_mid",
                signal_id=sid,
                kind="validated_signal",
            )
        except (KeyError, TypeError, ValueError):
            pass
        for target_idx, target in enumerate(signal.get("take_profits") or []):
            add_execution(f"{sid}.tp.{target_idx}", target, "take_profit", signal_id=sid, kind="validated_signal")
    for tf, block in (report.get("price_action") or {}).items():
        vp = (block or {}).get("volume_profile") or {}
        for key in ("poc", "vah", "val"):
            add_context(f"price_action.{tf}.{key}", vp.get(key), key, timeframe=tf, kind="volume_profile")
        for idx, lvl in enumerate((block or {}).get("sr_levels") or []):
            add_context(
                f"price_action.{tf}.sr.{idx}",
                lvl.get("price"),
                str(lvl.get("label") or "sr"),
                timeframe=tf,
                kind="sr",
            )

    quality = (technical_context.get("quality") or {}) if isinstance(technical_context, dict) else {}
    price_action = report.get("price_action") or technical_context.get("price_action") or {}
    primary = next((s for s in authorized_signals if s.get("signal_role") == "primary"), None)
    if primary is None and authorized_signals:
        primary = authorized_signals[0]
    if primary is None:
        eligible = [s for s in (report.get("signals") or []) if s.get("signal_role") != "rejected"]
        primary = eligible[0] if eligible else {}
    facts: dict[str, Any] = {
        "common": {
            "metrics": metrics,
            "sentiment": report.get("sentiment") or {},
            "conclusion": report.get("conclusion") or {},
            "primary_signal": primary or {},
            "manager_decision": report.get("meta", {}).get("manager_decision")
            or (report.get("agent_trace") or {}).get("decision")
            or {},
            "quality": quality or {"status": "unavailable", "warnings": ["technical quality unavailable"]},
        },
        "liquidity": report.get("liquidity") or [],
        "timeframes": {tf: (report.get("timeframes") or {}).get(tf, {}) for tf in ("4h", "1h", "15m")},
        "price_action_summary": build_pa_llm_summary(price_action, price=metrics.get("current_price")),
        "combination_rules": COMBINATION_RULES,
        "context_levels": context_levels,
        "authorized_execution_levels": authorized_execution_levels,
        "allowed_levels": context_levels,
        "authorized_signals": authorized_signals,
        "role_constraints": {
            "market_overview": COMBINATION_RULES["market_overview"],
            "liquidity": COMBINATION_RULES["liquidity"],
            "4h": COMBINATION_RULES["4h"],
            "1h": COMBINATION_RULES["1h"],
            "15m": COMBINATION_RULES["15m"],
        },
    }
    if not compact_for_llm:
        facts["price_action"] = price_action
    return facts


def validate_and_merge_llm_sections(
    raw_sections: Any,
    *,
    rule_sections: dict[str, dict[str, Any]],
    facts: dict[str, Any],
    mode: str,
    threshold: float,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Validate each LLM block independently and fall back only that block."""
    output: dict[str, dict[str, Any]] = {}
    audit: dict[str, Any] = {}
    allowed = {
        round(float(x["price"]), 2)
        for x in facts.get("context_levels", facts.get("allowed_levels", []))
    }
    expected_bias = _expected_bias(facts)
    supplied = raw_sections if isinstance(raw_sections, dict) else {}

    for key in SECTION_KEYS:
        candidate = supplied.get(key)
        reason = _validate_section(candidate, allowed=allowed, expected_bias=expected_bias)
        confidence = _confidence(candidate)
        if reason is None and mode == "hybrid" and confidence < threshold:
            reason = f"confidence {confidence:.2f} < {threshold:.2f}"
        if reason is None:
            accepted = _normalize_llm_section(candidate)
            output[key] = accepted
            audit[key] = {"source": "llm", "accepted": True, "confidence": confidence}
        else:
            fallback = deepcopy(rule_sections.get(key) or _section(
                "数据不足，等待确认。",
                conditions=["仅在结构与关键价位确认后再执行。"],
                invalidation="缺少可验证事实时，不建立方向性判断。",
            ))
            fallback["source"] = "fallback"
            fallback["fallback_reason"] = reason
            output[key] = fallback
            audit[key] = {"source": "fallback", "accepted": False, "fallback_reason": reason, "confidence": confidence}
    return output, audit


def _confidence(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float((value or {}).get("confidence", 0.0))))
    except (TypeError, ValueError, AttributeError):
        return 0.0


def _capped_section_lists(value: dict[str, Any]) -> dict[str, list[str]]:
    capped: dict[str, list[str]] = {}
    for key, limit in _SECTION_LIST_CAPS.items():
        rows = value.get(key, [])
        if not isinstance(rows, list):
            rows = []
        capped[key] = [str(x).strip() for x in rows if str(x).strip()][:limit]
    return capped


def _section_visible_lines(value: dict[str, Any]) -> int:
    """Count UI rows after the same list caps applied during merge."""
    capped = _capped_section_lists(value)
    summary = 1 if str(value.get("summary", "")).strip() else 0
    invalidation = 1 if str(value.get("invalidation", "")).strip() else 0
    return summary + len(capped["context"]) + len(capped["levels"]) + len(capped["conditions"]) + invalidation


def _normalize_llm_section(value: dict[str, Any]) -> dict[str, Any]:
    capped = _capped_section_lists(value)
    return {
        "summary": str(value["summary"]).strip(),
        "context": capped["context"],
        "levels": capped["levels"],
        "conditions": capped["conditions"],
        "invalidation": str(value["invalidation"]).strip(),
        "source": "llm",
        "confidence": _confidence(value),
        "fallback_reason": None,
    }


def _validate_section(value: Any, *, allowed: set[float], expected_bias: str) -> str | None:
    if not isinstance(value, dict):
        return "missing or invalid section"
    if str(value.get("source", "llm")) not in ("llm", ""):
        return "unknown source"
    if not str(value.get("summary", "")).strip() or not str(value.get("invalidation", "")).strip():
        return "summary and invalidation are required"
    for key in ("context", "levels", "conditions"):
        rows = value.get(key, [])
        if not isinstance(rows, list) or any(not isinstance(x, str) for x in rows):
            return f"{key} must be a string list"
    visible = _section_visible_lines(value)
    if visible > MAX_VISIBLE_LINES:
        return f"visible lines {visible} > {MAX_VISIBLE_LINES}"
    text = " ".join(
        [str(value.get("summary", "")), *value.get("context", []), *value.get("levels", []), *value.get("conditions", []), str(value.get("invalidation", ""))]
    )
    if "胜率" in text:
        return "unsupported win-rate wording"
    for token in _NUMBER_RE.findall(text):
        number = float(token)
        if number < _PRICE_TOKEN_MIN:
            continue
        if not any(
            abs(number - candidate) <= narrative_price_tolerance(token, candidate)
            for candidate in allowed
        ):
            return f"unapproved price {token}"
    if expected_bias == "bearish" and any(word in text for word in ("主方向偏多", "以做多为主", "优先做多")):
        return "direction conflicts with manager/rule conclusion"
    if expected_bias == "bullish" and any(word in text for word in ("主方向偏空", "以做空为主", "优先做空")):
        return "direction conflicts with manager/rule conclusion"
    return None


def _expected_bias(facts: dict[str, Any]) -> str:
    common = facts.get("common") or {}
    signal = common.get("primary_signal") or {}
    direction = str(signal.get("direction") or signal.get("theme") or "").lower()
    if direction in ("short", "bearish", "sell"):
        return "bearish"
    if direction in ("long", "bullish", "buy"):
        return "bullish"
    decision = common.get("manager_decision") or {}
    mgr_dir = str(decision.get("primary_direction") or "").lower()
    if mgr_dir in ("short", "bearish"):
        return "bearish"
    if mgr_dir in ("long", "bullish"):
        return "bullish"
    sentiment = common.get("sentiment") or {}
    return "bearish" if float(sentiment.get("bearish", 0)) > float(sentiment.get("bullish", 0)) else "bullish"


def narrative_price_tolerance(token: str, reference: float) -> float:
    """Match LLM price tokens to whitelist levels.

    - Bare integers (``4000``, ``4021``): ±5 for psychological round-offs near spot/levels.
    - Decimals: keep tight (≤0.51) so invented cents stay rejected.
    """
    del reference
    if "." in token:
        return 0.51
    return 5.0


def _price_tolerance(reference: float) -> float:
    """Legacy helper — prefer :func:`narrative_price_tolerance` with the raw token."""
    return max(1.0, abs(reference) * 0.0002)


def _unapproved_prices(text: str, allowed: set[float]) -> str | None:
    if not allowed:
        return None
    for token in _NUMBER_RE.findall(text):
        number = float(token)
        if number < _PRICE_TOKEN_MIN:
            continue
        if not any(
            abs(number - candidate) <= narrative_price_tolerance(token, candidate)
            for candidate in allowed
        ):
            return f"unapproved price {token}"
    return None


_EXECUTABLE_ON_WAIT = (
    "立即执行",
    "立即入场",
    "立即开仓",
    "现在入场",
    "现在开仓",
    "市价入场",
    "市价开仓",
    "马上入场",
    "马上开仓",
    "可追空",
    "可追多",
    "可考虑做空",
    "可考虑做多",
    "优先做空",
    "优先做多",
    "追空至",
    "追多至",
    "追空",
    "追多",
)

_EXECUTABLE_ON_WAIT_PATTERNS = (
    r"等待.{0,16}(做空|做多|追空|追多)",
    r"反弹.{0,12}(做空|追空)",
    r"回踩.{0,12}(做多|追多)",
    r"跌破.{0,24}(追空|做空)",
    r"突破.{0,24}(追多|做多)",
    r"可.{0,4}(做空|做多|追空|追多)",
)


def _executable_wording_on_wait(text: str) -> bool:
    if any(phrase in text for phrase in _EXECUTABLE_ON_WAIT):
        return True
    return any(re.search(pattern, text) for pattern in _EXECUTABLE_ON_WAIT_PATTERNS)


def _direction_conflict(text: str, expected_bias: str) -> str | None:
    if expected_bias == "bearish" and any(
        word in text for word in ("主方向偏多", "以做多为主", "优先做多", "分批做多")
    ):
        return "direction conflicts with authorized bearish plan"
    if expected_bias == "bullish" and any(
        word in text for word in ("主方向偏空", "以做空为主", "优先做空", "分批做空")
    ):
        return "direction conflicts with authorized bullish plan"
    return None


def _execution_authorized(facts: dict[str, Any]) -> bool:
    execution_allowed = facts.get("authorized_execution_levels") or []
    if not execution_allowed:
        return False
    decision = (facts.get("common") or {}).get("manager_decision") or {}
    return str(decision.get("action") or "") not in ("wait", "")


def validate_llm_top_level_fields(
    llm: dict[str, Any],
    *,
    facts: dict[str, Any],
) -> dict[str, str | None]:
    """Per-field validation; value is rejection reason or None when accepted."""
    context_allowed = {
        round(float(x["price"]), 2)
        for x in facts.get("context_levels", facts.get("allowed_levels", []))
    }
    execution_allowed = {
        round(float(x["price"]), 2) for x in facts.get("authorized_execution_levels", [])
    }
    # Summary/thesis may cite authorized SL/TP/entry as well as structure levels.
    narrative_allowed = context_allowed | execution_allowed
    execution_ok = _execution_authorized(facts)
    action_plan_allowed = execution_allowed if execution_ok else context_allowed
    expected_bias = _expected_bias(facts)
    decision = (facts.get("common") or {}).get("manager_decision") or {}
    manager_wait = str(decision.get("action") or "") == "wait"

    fields = {
        "market_summary": str(llm.get("market_summary") or ""),
        "trade_thesis": str(llm.get("trade_thesis") or ""),
        "action_plan": str(llm.get("action_plan") or ""),
    }
    reasons: dict[str, str | None] = {key: None for key in fields}

    if not any(value.strip() for value in fields.values()):
        return {key: "empty top-level narrative" for key in fields}

    visible_lines = sum(1 for value in fields.values() if value.strip()) + sum(
        value.count("\n") for value in fields.values()
    )
    if visible_lines > MAX_VISIBLE_LINES:
        msg = f"top-level visible lines {visible_lines} > {MAX_VISIBLE_LINES}"
        return {key: msg for key in fields}

    for key, text in fields.items():
        if not text.strip():
            continue
        if "胜率" in text:
            reasons[key] = "unsupported win-rate wording"
            continue
        allowed = action_plan_allowed if key == "action_plan" else narrative_allowed
        violation = _unapproved_prices(text, allowed)
        if violation:
            prefix = "action_plan" if key == "action_plan" else "narrative"
            reasons[key] = f"{prefix}: {violation}"
            continue
        if key in ("trade_thesis", "action_plan"):
            conflict = _direction_conflict(text, expected_bias)
            if conflict:
                reasons[key] = conflict
                continue
        if key == "action_plan" and manager_wait and _executable_wording_on_wait(text):
            reasons[key] = "executable wording while manager action is wait"
            continue
        if key == "action_plan" and not execution_ok and _executable_wording_on_wait(text):
            reasons[key] = "executable wording without manager authorization"

    return reasons


def validate_llm_top_level(
    llm: dict[str, Any],
    *,
    facts: dict[str, Any],
) -> str | None:
    """Validate market_summary / trade_thesis / action_plan against authorized facts."""
    field_reasons = validate_llm_top_level_fields(llm, facts=facts)
    for reason in field_reasons.values():
        if reason:
            return reason
    return None
