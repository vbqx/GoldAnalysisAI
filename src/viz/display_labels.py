"""Chinese display labels for agent trace and decision UI."""

from __future__ import annotations

BIAS_CN = {
    "bullish": "偏多",
    "bearish": "偏空",
    "neutral": "中性",
}

ACTION_CN = {
    "execute": "执行",
    "reduce": "缩仓执行",
    "wait": "观望",
}

TRADE_DIRECTION_CN = {
    "long": "做多",
    "short": "做空",
    "wait": "观望",
}

RISK_PROFILE_CN = {
    "aggressive": "激进",
    "neutral": "中性",
    "conservative": "保守",
}

NARRATIVE_SOURCE_CN = {
    "rule": "规则",
    "llm": "LLM",
    "fallback": "规则兜底",
}


def label_bias(value: object) -> str:
    key = str(value or "").strip().lower()
    return BIAS_CN.get(key, str(value or "—"))


def label_action(value: object) -> str:
    key = str(value or "").strip().lower()
    return ACTION_CN.get(key, str(value or "—"))


def label_trade_direction(value: object) -> str:
    key = str(value or "").strip().lower()
    return TRADE_DIRECTION_CN.get(key, str(value or "—"))


def label_risk_profile(value: object) -> str:
    key = str(value or "").strip().lower()
    return RISK_PROFILE_CN.get(key, str(value or "—"))


def label_position_scale(scale: object) -> str:
    try:
        value = float(scale or 0)
    except (TypeError, ValueError):
        return "—"
    if value <= 0:
        return "观望"
    if value >= 0.85:
        return "标准仓"
    if value >= 0.55:
        return "缩仓"
    return "试探仓"


# Chart / plan card styling (shared with analysis layer)
TF_LABELS = {"4h": "4H", "1h": "1H", "15m": "15M", "5m": "5M", "1d": "1D"}
TRADE_COLOR_SHORT = "#dc2626"
TRADE_COLOR_LONG = "#16a34a"


def infer_trade_theme(
    *,
    theme: str = "",
    direction: str = "",
    direction_cn: str = "",
) -> str:
    """Return ``short`` or ``long`` for plan cards and decision styling."""
    t = str(theme or "").strip().lower()
    if t in ("short", "long"):
        return t
    raw = f"{direction} {direction_cn}".lower()
    if raw.strip() in ("sell", "short", "bearish", "se") or any(x in raw for x in ("空", "卖")):
        return "short"
    if raw.strip() in ("buy", "long", "bullish") or any(x in raw for x in ("多", "买")):
        return "long"
    return "long"


def execution_banner(meta: dict | None) -> str:
    """Explain why trading plans may differ from trader/manager rows."""
    meta = meta or {}
    if meta.get("execution_authorized"):
        return ""
    parts: list[str] = ["以下仅为规则引擎候选方案，未经经理授权，不可按此执行。"]
    if meta.get("observation_mode"):
        parts.append("当前为快照观察模式（周末闭市或行情滞后），风控已全部否决。")
    decision = meta.get("manager_decision") or {}
    action = str(decision.get("action") or "").lower()
    if action == "wait":
        parts.append("经理决策：观望。")
    summary = str(decision.get("summary") or "").strip()
    if summary:
        parts.append(summary[:120])
    return " ".join(parts)
