"""Deterministic report quality score (heuristic — not calibrated win probability)."""

from __future__ import annotations

from typing import Any

_KNOWN_SOURCE_PREFIXES = (
    "jin10",
    "tradingview",
    "lux",
    "macro",
    "ict",
    "oanda",
    "tv:",
    "dgt",
    "sentiment",
    "fundamentals",
    "news",
    "external",
)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize_source(raw: str) -> str | None:
    text = str(raw or "").strip().lower()
    if not text or text in ("same", "unknown", "—"):
        return None
    for prefix in _KNOWN_SOURCE_PREFIXES:
        if text.startswith(prefix):
            return prefix
    return text.split(":")[0] if ":" in text else text


def _collect_item_sources(item: dict[str, Any]) -> set[str]:
    refs = item.get("refs") or {}
    sources: set[str] = set()
    for key in ("source", "provider", "symbol"):
        norm = _normalize_source(str(refs.get(key) or ""))
        if norm:
            sources.add(norm)
    return sources


def _data_quality(report: dict[str, Any]) -> float:
    as_of = (report.get("meta") or {}).get("data_as_of") or {}
    if as_of.get("executable"):
        return 1.0
    age = as_of.get("data_age_hours")
    if age is None:
        return 0.4
    if age <= 4:
        return 0.95
    if age <= 24:
        return 0.75
    if age <= 48:
        return 0.55
    return 0.35


def _freshness_quality(report: dict[str, Any]) -> float:
    meta = report.get("meta") or {}
    if meta.get("observation_mode"):
        return 0.5
    return _data_quality(report)


def _evidence_coverage(report: dict[str, Any]) -> float:
    trace = report.get("agent_trace") or {}
    team = trace.get("analyst_team") or {}
    roles = ("technical", "fundamentals", "news", "sentiment")
    filled = sum(1 for role in roles if (team.get(role) or {}).get("items"))
    debate = trace.get("debate") or {}
    bull = len((debate.get("bullish") or {}).get("items") or [])
    bear = len((debate.get("bearish") or {}).get("items") or [])
    debate_fill = min(1.0, (bull + bear) / 12)
    return _clamp((filled / 4) * 0.6 + debate_fill * 0.4)


def _source_diversity(report: dict[str, Any]) -> float:
    sources: set[str] = set()
    trace = report.get("agent_trace") or {}
    for side in ("bullish", "bearish"):
        block = (trace.get("debate") or {}).get(side) or trace.get(side) or {}
        if isinstance(block, dict):
            for item in block.get("items") or []:
                sources.update(_collect_item_sources(item))
    for role in ("technical", "fundamentals", "news", "sentiment"):
        for item in ((trace.get("analyst_team") or {}).get(role) or {}).get("items") or []:
            sources.update(_collect_item_sources(item))
    return _clamp(len(sources) / 6)


def _cross_timeframe_agreement(report: dict[str, Any]) -> float:
    tfs = report.get("timeframes") or {}
    trends = [str(info.get("trend") or "neutral") for info in tfs.values() if isinstance(info, dict)]
    if not trends:
        return 0.5
    bullish = sum(1 for t in trends if t == "bullish")
    bearish = sum(1 for t in trends if t == "bearish")
    dominant = max(bullish, bearish, len(trends) - bullish - bearish)
    return _clamp(dominant / len(trends))


def _bull_bear_separation(report: dict[str, Any]) -> float:
    trace = report.get("agent_trace") or {}
    debate = trace.get("debate") or {}
    bull = float((debate.get("bullish") or {}).get("confidence") or 0)
    bear = float((debate.get("bearish") or {}).get("confidence") or 0)
    return _clamp(abs(bull - bear))


def _schema_quality(report: dict[str, Any]) -> float:
    inv = (report.get("meta") or {}).get("report_invariants") or {}
    if inv.get("passed") is True and not inv.get("gate_applied"):
        return 1.0
    if inv.get("passed") is True and inv.get("remediated"):
        return 0.85
    count = int(inv.get("violation_count") or 0)
    return _clamp(1.0 - count * 0.15)


def compute_report_reliability(report: dict[str, Any]) -> dict[str, Any]:
    """Heuristic report quality score; not calibrated against historical outcomes."""
    components = {
        "data_quality": round(_data_quality(report), 3),
        "freshness_quality": round(_freshness_quality(report), 3),
        "evidence_coverage": round(_evidence_coverage(report), 3),
        "source_diversity": round(_source_diversity(report), 3),
        "cross_timeframe_agreement": round(_cross_timeframe_agreement(report), 3),
        "bull_bear_separation": round(_bull_bear_separation(report), 3),
        "schema_quality": round(_schema_quality(report), 3),
    }
    weights = {
        "data_quality": 0.2,
        "freshness_quality": 0.15,
        "evidence_coverage": 0.15,
        "source_diversity": 0.1,
        "cross_timeframe_agreement": 0.15,
        "bull_bear_separation": 0.1,
        "schema_quality": 0.15,
    }
    overall = sum(components[k] * weights[k] for k in weights)
    llm = report.get("llm_analysis") or {}
    score = round(_clamp(overall), 3)
    return {
        **components,
        "report_quality_score": score,
        "overall_reliability": score,
        "calibration_status": "heuristic",
        "model_self_reported_confidence": float(llm.get("confidence") or 0),
        "note": "report_quality_score 为启发式质量分，未做历史校准；不代表胜率",
    }
