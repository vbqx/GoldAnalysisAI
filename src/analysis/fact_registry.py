"""Canonical fact registry with as-of, source and provenance contracts."""

from __future__ import annotations

from typing import Any

FACT_REGISTRY_VERSION = "fr-v2"
CALCULATION_VERSION = "pa-v3"


def _as_of_utc(report: dict[str, Any]) -> str | None:
    as_of = (report.get("meta") or {}).get("data_as_of") or {}
    return as_of.get("last_bar_time_utc") or as_of.get("as_of_utc")


def _register_numeric(
    facts: dict[str, dict[str, Any]],
    *,
    fact_id: str,
    value: Any,
    source: str,
    timeframe: str | None = None,
    quality: str = "verified",
    as_of: str | None = None,
    refs: dict[str, Any] | None = None,
) -> None:
    if value is None:
        return
    try:
        numeric = round(float(value), 2)
    except (TypeError, ValueError):
        return
    entry = {
        "fact_id": fact_id,
        "value": numeric,
        "value_type": "numeric",
        "as_of": as_of,
        "source": source,
        "timeframe": timeframe,
        "calculation_version": CALCULATION_VERSION,
        "quality": quality,
    }
    if refs:
        entry["refs"] = refs
    if fact_id in facts and facts[fact_id].get("value") != numeric:
        facts[fact_id]["quality"] = "conflict"
        facts[fact_id]["conflict_value"] = numeric
        return
    facts[fact_id] = entry


def _register_text(
    facts: dict[str, dict[str, Any]],
    *,
    fact_id: str,
    value: Any,
    source: str,
    timeframe: str | None = None,
    quality: str = "verified",
    as_of: str | None = None,
    refs: dict[str, Any] | None = None,
) -> None:
    text = str(value or "").strip()
    if not text:
        return
    entry = {
        "fact_id": fact_id,
        "value": text,
        "value_type": "text",
        "as_of": as_of,
        "source": source,
        "timeframe": timeframe,
        "calculation_version": CALCULATION_VERSION,
        "quality": quality,
    }
    if refs:
        entry["refs"] = refs
    if fact_id in facts and facts[fact_id].get("value") != text:
        facts[fact_id]["quality"] = "conflict"
        facts[fact_id]["conflict_value"] = text
        return
    facts[fact_id] = entry


def _pa_fact_id(tf: str, suffix: str) -> str:
    if tf == "session":
        return f"pa.session.{suffix}"
    return f"pa.{tf}.{suffix}"


def _calendar_state(report: dict[str, Any]) -> str:
    external = report.get("external") or {}
    fetch_errors = [str(e).lower() for e in (external.get("fetch_errors") or [])]
    if any("calendar" in err or "macro" in err for err in fetch_errors):
        return "fetch_failed"
    cal_rows = report.get("calendar_events") or external.get("calendar_events") or []
    if cal_rows:
        return "has_events"
    risk = str(external.get("risk_events") or "").strip()
    if risk and risk not in ("—", "-", "none", "None"):
        return "has_events"
    count = external.get("calendar_count")
    if count == 0:
        return "confirmed_empty"
    if count is None and not risk:
        return "unknown"
    return "confirmed_empty"


def _register_timeframes(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None, source: str) -> None:
    for tf, info in (report.get("timeframes") or {}).items():
        if not isinstance(info, dict):
            continue
        for key in ("swing_high", "swing_low"):
            _register_numeric(
                facts,
                fact_id=f"{tf}.{key}",
                value=info.get(key),
                source="lux_smc",
                timeframe=tf,
                as_of=as_of,
            )
        _register_text(
            facts,
            fact_id=f"{tf}.trend",
            value=info.get("trend"),
            source="lux_smc",
            timeframe=tf,
            as_of=as_of,
        )
        for idx, ob in enumerate(info.get("order_blocks") or []):
            if not isinstance(ob, dict):
                continue
            for side in ("low", "high"):
                _register_numeric(
                    facts,
                    fact_id=f"{tf}.ob.{idx}.{side}",
                    value=ob.get(side),
                    source="lux_smc",
                    timeframe=tf,
                    as_of=as_of,
                    refs={"direction": ob.get("direction"), "kind": "order_block"},
                )
        for idx, fvg in enumerate(info.get("fvgs") or []):
            if not isinstance(fvg, dict):
                continue
            try:
                low = float(fvg["low"])
                high = float(fvg["high"])
                width = abs(high - low)
            except (KeyError, TypeError, ValueError):
                low = high = width = None
            atr_raw = info.get("atr")
            try:
                atr = float(atr_raw) if atr_raw is not None else None
            except (TypeError, ValueError):
                atr = None
            width_atr = (width / atr) if (width is not None and atr and atr > 0) else None
            fvg_refs = {
                "direction": fvg.get("direction"),
                "kind": "fvg",
                "width": round(width, 4) if width is not None else None,
                "width_atr_ratio": round(width_atr, 4) if width_atr is not None else None,
                "atr": atr,
            }
            for side in ("low", "high"):
                _register_numeric(
                    facts,
                    fact_id=f"{tf}.fvg.{idx}.{side}",
                    value=fvg.get(side),
                    source="lux_smc",
                    timeframe=tf,
                    as_of=as_of,
                    refs=fvg_refs,
                )


def _register_price_action(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None) -> None:
    for tf, block in (report.get("price_action") or {}).items():
        vp = (block or {}).get("volume_profile") or {}
        pa_refs = {
            "lookback_mode": (block or {}).get("lookback_mode"),
            "lookback_bars": (block or {}).get("lookback_bars"),
            "lookback_requested": (block or {}).get("lookback_requested"),
            "profile_source": (block or {}).get("profile_source"),
        }
        for key in ("poc", "vah", "val"):
            _register_numeric(
                facts,
                fact_id=_pa_fact_id(tf, key),
                value=vp.get(key),
                source="dgt_price_action",
                timeframe=tf,
                as_of=as_of,
                refs=pa_refs,
            )
        for idx, lvl in enumerate((block or {}).get("sr_levels") or []):
            _register_numeric(
                facts,
                fact_id=_pa_fact_id(tf, f"sr.{idx}"),
                value=lvl.get("price"),
                source=str(lvl.get("label") or "sr"),
                timeframe=tf,
                as_of=as_of,
                refs={"kind": lvl.get("kind"), "direction": lvl.get("direction")},
            )


def _register_freshness(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None, source: str) -> None:
    data_as_of = (report.get("meta") or {}).get("data_as_of") or {}
    _register_text(
        facts,
        fact_id="freshness.market_status",
        value=data_as_of.get("market_status"),
        source=source,
        timeframe="spot",
        as_of=as_of,
    )
    if data_as_of.get("executable") is not None:
        _register_text(
            facts,
            fact_id="freshness.executable",
            value=str(bool(data_as_of.get("executable"))).lower(),
            source=source,
            timeframe="spot",
            as_of=as_of,
        )
    if data_as_of.get("data_age_hours") is not None:
        _register_numeric(
            facts,
            fact_id="freshness.data_age_hours",
            value=data_as_of.get("data_age_hours"),
            source=source,
            timeframe="spot",
            as_of=as_of,
            quality="verified",
        )

    stats = (report.get("meta") or {}).get("context_stats") or {}
    bars = ((stats.get("technical_inputs") or {}).get("bars") or {})
    for tf, count in bars.items():
        _register_numeric(
            facts,
            fact_id=f"bar.{tf}.count",
            value=count,
            source=source,
            timeframe=tf,
            as_of=as_of,
            quality="verified" if count else "degraded",
        )


def _register_external(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None) -> None:
    external = report.get("external") or {}
    cal_state = _calendar_state(report)
    _register_text(
        facts,
        fact_id="calendar.state",
        value=cal_state,
        source="macro_calendar",
        timeframe="1d",
        as_of=as_of,
        quality="degraded" if cal_state in ("fetch_failed", "unknown") else "verified",
    )

    for idx, row in enumerate(report.get("calendar_events") or external.get("calendar_events") or []):
        if not isinstance(row, dict):
            continue
        _register_text(
            facts,
            fact_id=f"calendar.event.{idx}.time",
            value=row.get("time") or row.get("datetime"),
            source="macro_calendar",
            timeframe="1d",
            as_of=as_of,
            refs={"event": row.get("event"), "region": row.get("region")},
        )

    for idx, headline in enumerate(external.get("headline_items") or []):
        if not isinstance(headline, dict):
            continue
        _register_text(
            facts,
            fact_id=f"news.{idx}.published_at",
            value=headline.get("time") or headline.get("published_at"),
            source=str(headline.get("source") or "jin10"),
            timeframe="news",
            as_of=headline.get("time") or headline.get("published_at") or as_of,
            quality="verified" if headline.get("time") or headline.get("published_at") else "degraded",
            refs={"title": headline.get("title") or headline.get("text", "")[:80]},
        )

    for idx, quote in enumerate(external.get("macro_quotes") or []):
        if not isinstance(quote, dict):
            continue
        name = str(quote.get("name") or idx)
        symbol = str(quote.get("symbol") or "macro")
        quote_as_of = quote.get("as_of") or quote.get("bar_time") or quote.get("time")
        macro_quality = "verified" if quote_as_of else "degraded"
        macro_as_of = str(quote_as_of) if quote_as_of else None
        refs = {"name": name, "bias": quote.get("bias")}
        if quote_as_of:
            refs["quote_as_of"] = macro_as_of
        else:
            refs["pit_alignment"] = "unknown"
        _register_numeric(
            facts,
            fact_id=f"macro.{name}.close",
            value=quote.get("close"),
            source=symbol,
            timeframe="1d",
            as_of=macro_as_of or as_of,
            quality=macro_quality,
            refs=refs,
        )
        _register_numeric(
            facts,
            fact_id=f"macro.{name}.change_pct",
            value=quote.get("change_pct"),
            source=symbol,
            timeframe="1d",
            as_of=as_of,
        )

    cross = external.get("spot_cross_check")
    if isinstance(cross, dict) and cross.get("drift_points") is not None:
        _register_numeric(
            facts,
            fact_id="macro.spot_cross_check.drift_points",
            value=cross.get("drift_points"),
            source="OANDA:XAUUSD",
            timeframe="spot",
            as_of=as_of,
            quality="verified",
        )


def build_fact_registry(report: dict[str, Any]) -> dict[str, Any]:
    """Register numeric and text facts referenced by narrative validation and UI."""
    as_of = _as_of_utc(report)
    source = str((report.get("meta") or {}).get("data_source") or "OANDA:XAUUSD")
    facts: dict[str, dict[str, Any]] = {}

    metrics = report.get("metrics") or {}
    for key in ("current_price", "daily_low", "daily_high", "prev_close"):
        _register_numeric(
            facts,
            fact_id=f"metrics.{key}",
            value=metrics.get(key),
            source=source,
            timeframe="spot",
            as_of=as_of,
        )

    for idx, row in enumerate(report.get("liquidity") or []):
        _register_numeric(
            facts,
            fact_id=f"liquidity.{idx}",
            value=row.get("price"),
            source=str(row.get("label") or "liquidity"),
            timeframe=row.get("timeframe"),
            as_of=as_of,
            refs={"kind": row.get("kind"), "role": row.get("role")},
        )

    _register_timeframes(facts, report, as_of=as_of, source=source)
    _register_price_action(facts, report, as_of=as_of)

    for sig in report.get("signals") or []:
        sid = str(sig.get("signal_id") or sig.get("name") or "signal")
        for key in ("entry_low", "entry_high", "stop_loss"):
            _register_numeric(
                facts,
                fact_id=f"signal.{sid}.{key}",
                value=sig.get(key),
                source="trade_plan",
                timeframe="5m",
                as_of=as_of,
                quality="verified" if sig.get("signal_role") in ("primary", "alternate") else "candidate",
            )
        for tp_idx, tp in enumerate(sig.get("take_profits") or []):
            _register_numeric(
                facts,
                fact_id=f"signal.{sid}.tp.{tp_idx}",
                value=tp,
                source="trade_plan",
                timeframe="5m",
                as_of=as_of,
            )

    sentiment = report.get("sentiment") or {}
    for key in ("bullish", "bearish", "ranging"):
        _register_numeric(
            facts,
            fact_id=f"sentiment.{key}",
            value=sentiment.get(key),
            source="structure_vote",
            timeframe="multi",
            as_of=as_of,
        )

    _register_freshness(facts, report, as_of=as_of, source=source)
    _register_external(facts, report, as_of=as_of)

    price_index: dict[str, list[str]] = {}
    for fact_id, row in facts.items():
        if row.get("value_type") != "numeric":
            continue
        key = f"{float(row['value']):.2f}"
        price_index.setdefault(key, []).append(fact_id)

    conflicts = [fid for fid, row in facts.items() if row.get("quality") == "conflict"]
    return {
        "version": FACT_REGISTRY_VERSION,
        "as_of": as_of,
        "source": source,
        "facts": facts,
        "price_index": price_index,
        "conflict_fact_ids": conflicts,
        "fact_count": len(facts),
    }


def allowed_prices(registry: dict[str, Any]) -> set[float]:
    return {
        float(row["value"])
        for row in (registry.get("facts") or {}).values()
        if row.get("value_type", "numeric") == "numeric"
    }


def fact_lookup(registry: dict[str, Any], price: float, *, tolerance: float = 0.51) -> list[str]:
    """Resolve a displayed price to registered fact IDs."""
    matches: list[str] = []
    for row in (registry.get("facts") or {}).values():
        if row.get("value_type", "numeric") != "numeric":
            continue
        if abs(float(row["value"]) - float(price)) <= tolerance:
            matches.append(str(row["fact_id"]))
    return matches


def fact_ids_for_signal(sig: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """Map signal geometry fields to canonical fact_ids when registered."""
    sid = str(sig.get("signal_id") or sig.get("name") or "signal")
    out: dict[str, Any] = {"signal_id": sid}
    mapping = {
        "entry_low": f"signal.{sid}.entry_low",
        "entry_high": f"signal.{sid}.entry_high",
        "stop_loss": f"signal.{sid}.stop_loss",
    }
    facts = (registry.get("facts") or {})
    for field, fact_id in mapping.items():
        if fact_id in facts:
            out[f"{field}_fact_id"] = fact_id
    tp_ids = []
    for idx in range(len(sig.get("take_profits") or [])):
        fid = f"signal.{sid}.tp.{idx}"
        if fid in facts:
            tp_ids.append(fid)
    if tp_ids:
        out["take_profit_fact_ids"] = tp_ids
    return out


def compact_fact_index(registry: dict[str, Any], *, limit: int = 120) -> list[dict[str, Any]]:
    """Slim fact list for LLM payloads — cite fact_id instead of duplicating numbers."""
    rows = list((registry.get("facts") or {}).values())
    rows.sort(key=lambda r: str(r.get("fact_id")))
    out: list[dict[str, Any]] = []
    for row in rows[:limit]:
        item = {
            "fact_id": row["fact_id"],
            "value": row["value"],
            "value_type": row.get("value_type", "numeric"),
            "timeframe": row.get("timeframe"),
            "source": row.get("source"),
            "as_of": row.get("as_of"),
            "quality": row.get("quality"),
        }
        if row.get("refs"):
            item["refs"] = row["refs"]
        out.append(item)
    return out
