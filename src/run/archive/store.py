"""Persist each pipeline run under its own folder; replay loads the saved bundle as-is."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.analysis.ict_pa import (
    FairValueGap,
    LiquidityZone,
    OrderBlock,
    StructureEvent,
    TimeframeAnalysis,
)
from src.run.config import RunConfig
from src.core.types import CalendarEvent, ExternalFactors, HeadlineItem, MacroQuote
from src.data.fetch_pipeline import DataFetchResult
from src.run.archive.compat import (
    inspect_archive,
    load_manifest,
    migrate_analyses_payload,
    migrate_fetch_payload,
    migrate_frame_payload,
    normalize_report,
    upgrade_manifest_if_needed,
)
from src.run.archive.index import list_index_entries, rebuild_index_from_disk, upsert_index_entry
from src.run.archive.prune import prune_archives
from src.run.archive.schema import (
    ARTIFACT_ANALYSIS,
    ARTIFACT_FETCH,
    ARTIFACT_FRAME,
    SCHEMA_VERSION,
    artifact_envelope,
    build_manifest,
)
from src.run.archive.completion import (
    PIPELINE_STATUS_COMPLETE,
    PIPELINE_STATUS_DEGRADED,
    PIPELINE_STATUS_FAILED,
    PIPELINE_STATUS_PARTIAL,
    assert_pipeline_replay_ready,
)
from src.data.fetcher import format_utc8
from src.log import get_logger

log = get_logger(__name__)

ARCHIVE_VERSION = SCHEMA_VERSION  # backward compat alias for tests/importers
ARCHIVES_ROOT = Path(__file__).resolve().parents[3] / ".cache" / "run_archives"


def archives_root() -> Path:
    return ARCHIVES_ROOT


def run_dir(run_id: str) -> Path:
    return archives_root() / run_id


def _sanitize_json(obj: Any) -> Any:
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return round(obj, 6) if abs(obj) < 1e8 else obj
    if isinstance(obj, dict):
        return {k: _sanitize_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_json(v) for v in obj]
    return obj


def allocate_run_id() -> str:
    base = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = base
    suffix = 1
    while run_dir(run_id).exists():
        run_id = f"{base}_{suffix}"
        suffix += 1
    return run_id


def inspect_run_archive(run_id: str) -> Any:
    return inspect_archive(run_id, run_dir(run_id))


def _archive_row_from_path(run_id: str, path: Path) -> dict[str, Any] | None:
    if not path.is_dir():
        return None
    if not (path / "manifest.json").is_file() and not (path / "meta.json").is_file():
        return None
    try:
        inspection = inspect_archive(run_id, path)
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    manifest = inspection.manifest
    summary = manifest.get("summary") or {}
    row = {
        "run_id": run_id,
        "saved_at": manifest.get("saved_at") or summary.get("saved_at"),
        "schema_version": inspection.schema_version,
        "compatibility": inspection.level.value,
        "compatibility_warnings": inspection.warnings,
        "pipeline_status": summary.get("pipeline_status"),
        "replayable": inspection.replayable,
        "current_price": summary.get("current_price"),
        "bars_summary": summary.get("bars_summary") or {},
        "run_config": manifest.get("run_config") or {},
        "source_label": summary.get("source_label"),
        "path": str(path),
    }
    meta_path = path / "meta.json"
    if meta_path.is_file():
        try:
            legacy_meta = json.loads(meta_path.read_text(encoding="utf-8"))
            row.setdefault("saved_at", legacy_meta.get("saved_at"))
            row.setdefault("current_price", legacy_meta.get("current_price"))
            row.setdefault("bars_summary", legacy_meta.get("bars_summary"))
            row.setdefault("run_config", legacy_meta.get("run_config"))
        except (OSError, json.JSONDecodeError):
            pass
    return row


def _scan_archives(*, limit: int = 100) -> list[dict[str, Any]]:
    root = archives_root()
    if not root.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    for path in root.iterdir():
        if not path.is_dir() or path.name == "index.json":
            continue
        row = _archive_row_from_path(path.name, path)
        if row:
            rows.append(row)
    rows.sort(key=lambda row: str(row.get("saved_at") or ""), reverse=True)
    return rows[:limit]


def list_archives(*, limit: int = 100) -> list[dict[str, Any]]:
    root = archives_root()
    if not root.is_dir():
        return []
    indexed = list_index_entries(root, limit=limit)
    if indexed:
        return indexed[:limit]
    rows = _scan_archives(limit=max(limit, 500))
    if rows:
        rebuild_index_from_disk(root, rows)
    return rows[:limit]


def archives_exist() -> bool:
    return bool(list_archives(limit=1))


def archive_label(meta: dict[str, Any]) -> str:
    run_id = str(meta.get("run_id") or "—")
    saved_at = format_utc8(meta.get("saved_at") or run_id)
    mode = str((meta.get("run_config") or {}).get("agent_mode") or "—")
    price = meta.get("current_price")
    price_text = f"{float(price):.2f}" if isinstance(price, (int, float)) else "—"
    bars = meta.get("bars_summary") or {}
    bar_5m = bars.get("5m", "—")
    compat = str(meta.get("compatibility") or "")
    pipeline_status = str(meta.get("pipeline_status") or "")
    tag = ""
    if pipeline_status == PIPELINE_STATUS_PARTIAL:
        tag = " · ⚠中断"
    elif pipeline_status == PIPELINE_STATUS_FAILED:
        tag = " · ❌失败"
    elif pipeline_status == PIPELINE_STATUS_DEGRADED:
        tag = " · ⚠校验降级"
    elif meta.get("replayable") is False and pipeline_status == PIPELINE_STATUS_COMPLETE:
        tag = " · ⚠不可回放"
    return f"{saved_at} · {mode} · {price_text} · 5m {bar_5m}根{tag}"


def _ts_to_str(value: Any) -> str:
    return pd.Timestamp(value).isoformat()


def _ts_from_str(value: str | None) -> pd.Timestamp | None:
    if not value:
        return None
    return pd.Timestamp(value)


def _encode_order_block(row: OrderBlock) -> dict[str, Any]:
    return {
        "high": row.high,
        "low": row.low,
        "direction": row.direction,
        "time": _ts_to_str(row.time),
        "label": row.label,
    }


def _decode_order_block(payload: dict[str, Any]) -> OrderBlock:
    return OrderBlock(
        high=float(payload["high"]),
        low=float(payload["low"]),
        direction=payload["direction"],
        time=_ts_from_str(payload.get("time")) or pd.Timestamp.utcnow(),
        label=str(payload.get("label") or "OB"),
    )


def _encode_fvg(row: FairValueGap) -> dict[str, Any]:
    return {
        "high": row.high,
        "low": row.low,
        "direction": row.direction,
        "time": _ts_to_str(row.time),
        "label": row.label,
    }


def _decode_fvg(payload: dict[str, Any]) -> FairValueGap:
    return FairValueGap(
        high=float(payload["high"]),
        low=float(payload["low"]),
        direction=payload["direction"],
        time=_ts_from_str(payload.get("time")) or pd.Timestamp.utcnow(),
        label=str(payload.get("label") or "FVG"),
    )


def _encode_structure_event(row: StructureEvent) -> dict[str, Any]:
    return {
        "kind": row.kind,
        "direction": row.direction,
        "price": row.price,
        "time": _ts_to_str(row.time),
        "pivot_time": _ts_to_str(row.pivot_time) if row.pivot_time is not None else None,
        "scope": row.scope,
    }


def _decode_structure_event(payload: dict[str, Any]) -> StructureEvent:
    return StructureEvent(
        kind=payload["kind"],
        direction=payload["direction"],
        price=float(payload["price"]),
        time=_ts_from_str(payload.get("time")) or pd.Timestamp.utcnow(),
        pivot_time=_ts_from_str(payload.get("pivot_time")),
        scope=payload.get("scope") or "swing",
    )


def _encode_liquidity(row: LiquidityZone) -> dict[str, Any]:
    return {
        "price": row.price,
        "kind": row.kind,
        "label": row.label,
        "strength": row.strength,
        "swept": row.swept,
    }


def _decode_liquidity(payload: dict[str, Any]) -> LiquidityZone:
    return LiquidityZone(
        price=float(payload["price"]),
        kind=str(payload.get("kind") or ""),
        label=str(payload.get("label") or ""),
        strength=float(payload.get("strength") or 0.5),
        swept=bool(payload.get("swept")),
    )


def encode_analysis(analysis: TimeframeAnalysis) -> dict[str, Any]:
    return {
        "timeframe": analysis.timeframe,
        "trend": analysis.trend,
        "bos": analysis.bos,
        "choch": analysis.choch,
        "order_blocks": [_encode_order_block(x) for x in analysis.order_blocks],
        "fvgs": [_encode_fvg(x) for x in analysis.fvgs],
        "active_fvgs": [_encode_fvg(x) for x in analysis.active_fvgs],
        "liquidity": [_encode_liquidity(x) for x in analysis.liquidity],
        "swing_high": analysis.swing_high,
        "swing_low": analysis.swing_low,
        "events": [_encode_structure_event(x) for x in analysis.events],
        "premium_discount": analysis.premium_discount,
        "equilibrium": analysis.equilibrium,
        "volume_signal": analysis.volume_signal,
        "atr": analysis.atr,
        "last_close": analysis.last_close,
        "recent_high": analysis.recent_high,
        "recent_low": analysis.recent_low,
    }


def decode_analysis(payload: dict[str, Any]) -> TimeframeAnalysis:
    return TimeframeAnalysis(
        timeframe=str(payload.get("timeframe") or ""),
        trend=payload.get("trend") or "ranging",
        bos=str(payload.get("bos") or "无"),
        choch=str(payload.get("choch") or "无"),
        order_blocks=[_decode_order_block(x) for x in payload.get("order_blocks") or [] if isinstance(x, dict)],
        fvgs=[_decode_fvg(x) for x in payload.get("fvgs") or [] if isinstance(x, dict)],
        active_fvgs=[_decode_fvg(x) for x in payload.get("active_fvgs") or [] if isinstance(x, dict)],
        liquidity=[_decode_liquidity(x) for x in payload.get("liquidity") or [] if isinstance(x, dict)],
        swing_high=payload.get("swing_high"),
        swing_low=payload.get("swing_low"),
        events=[_decode_structure_event(x) for x in payload.get("events") or [] if isinstance(x, dict)],
        premium_discount=str(payload.get("premium_discount") or "unknown"),
        equilibrium=payload.get("equilibrium"),
        volume_signal=str(payload.get("volume_signal") or "N/A"),
        atr=payload.get("atr"),
        last_close=payload.get("last_close"),
        recent_high=payload.get("recent_high"),
        recent_low=payload.get("recent_low"),
    )


def _frame_to_json(df: pd.DataFrame) -> dict[str, Any]:
    out = df.copy()
    if getattr(out.index, "tz", None) is not None:
        out.index = out.index.tz_convert("UTC")
    index = [ts.isoformat() for ts in pd.to_datetime(out.index, utc=True)]
    return {
        "columns": [str(c) for c in out.columns],
        "index": index,
        "data": out.where(pd.notna(out), None).values.tolist(),
    }


def _frame_from_json(payload: dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame(payload["data"], columns=payload["columns"])
    df.index = pd.to_datetime(payload["index"], utc=True)
    return df


def _external_to_json(external: ExternalFactors) -> dict[str, Any]:
    return {
        "dxy_impact": external.dxy_impact,
        "risk_events": external.risk_events,
        "news_headlines": list(external.news_headlines),
        "headline_items": [item.to_dict() for item in external.headline_items],
        "calendar_events": [event.to_dict() for event in external.calendar_events],
        "macro_quotes": [quote.to_dict() for quote in external.macro_quotes],
        "social_sentiment": external.social_sentiment,
        "social_posts": list(external.social_posts),
        "sources": list(external.sources),
        "fetch_errors": list(external.fetch_errors),
    }


def _external_from_json(payload: dict[str, Any]) -> ExternalFactors:
    headlines = payload.get("headline_items") or []
    calendar = payload.get("calendar_events") or []
    quotes = payload.get("macro_quotes") or []
    return ExternalFactors(
        dxy_impact=str(payload.get("dxy_impact") or "—"),
        risk_events=str(payload.get("risk_events") or "—"),
        news_headlines=[str(x) for x in payload.get("news_headlines") or []],
        headline_items=[
            HeadlineItem(
                source=str(row.get("source") or ""),
                text=str(row.get("text") or ""),
                time=str(row.get("time") or ""),
                title=str(row.get("title") or ""),
                url=str(row.get("url") or ""),
            )
            for row in headlines
            if isinstance(row, dict)
        ],
        calendar_events=[
            CalendarEvent(
                time=str(row.get("time") or ""),
                region=str(row.get("region") or ""),
                event=str(row.get("event") or ""),
                importance=float(row.get("importance") or 1.0),
            )
            for row in calendar
            if isinstance(row, dict)
        ],
        macro_quotes=[
            MacroQuote(
                name=str(row.get("name") or ""),
                symbol=str(row.get("symbol") or ""),
                close=float(row.get("close") or 0.0),
                change_pct=float(row.get("change_pct") or 0.0),
                impact=str(row.get("impact") or ""),
                bias=str(row.get("bias") or "neutral"),  # type: ignore[arg-type]
                source=str(row.get("source") or "tradingview"),
            )
            for row in quotes
            if isinstance(row, dict)
        ],
        social_sentiment=str(payload.get("social_sentiment") or "—"),
        social_posts=[row for row in payload.get("social_posts") or [] if isinstance(row, dict)],
        sources=[str(x) for x in payload.get("sources") or []],
        fetch_errors=[str(x) for x in payload.get("fetch_errors") or []],
    )


def _fetch_payload(fetched: DataFetchResult) -> dict[str, Any]:
    body = {
        "source_label": fetched.source_label,
        "bars_summary": fetched.bars_summary,
        "raw": {tf: _frame_to_json(df) for tf, df in fetched.raw.items()},
        "external": _external_to_json(fetched.external),
    }
    return artifact_envelope(kind="fetch", artifact_version=ARTIFACT_FETCH, payload=body)


def load_fetch(run_id: str) -> DataFetchResult:
    directory = run_dir(run_id)
    manifest = load_manifest(run_id, directory)
    fetch_rel = str((manifest.get("artifacts") or {}).get("fetch", {}).get("path") or "fetch.json")
    path = directory / fetch_rel
    if not path.is_file():
        raise FileNotFoundError(f"run archive fetch not found: {path}")
    payload = migrate_fetch_payload(json.loads(path.read_text(encoding="utf-8")))
    raw_payload = payload.get("raw") or {}
    raw = {tf: _frame_from_json(migrate_frame_payload(frame)) for tf, frame in raw_payload.items()}
    external = _external_from_json(payload.get("external") or {})
    return DataFetchResult(
        raw=raw,
        external=external,
        source_label=str(payload.get("source_label") or "archive"),
    )


def load_enriched(run_id: str) -> dict[str, pd.DataFrame]:
    directory = run_dir(run_id)
    manifest = load_manifest(run_id, directory)
    enriched_spec = (manifest.get("artifacts") or {}).get("enriched") or {}
    enriched_dir = directory / str(enriched_spec.get("dir") or "enriched")
    if not enriched_dir.is_dir():
        raise FileNotFoundError(f"run archive enriched not found: {enriched_dir}")
    enriched: dict[str, pd.DataFrame] = {}
    for path in sorted(enriched_dir.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        frame_payload = migrate_frame_payload(raw)
        enriched[path.stem] = _frame_from_json(frame_payload)
    if not enriched:
        raise FileNotFoundError(f"run archive enriched is empty: {enriched_dir}")
    return enriched


def load_analyses(run_id: str, enriched: dict[str, pd.DataFrame]) -> dict[str, TimeframeAnalysis]:
    directory = run_dir(run_id)
    manifest = load_manifest(run_id, directory)
    analyses_rel = str((manifest.get("artifacts") or {}).get("analyses", {}).get("path") or "analyses.json")
    path = directory / analyses_rel
    if path.is_file():
        raw = json.loads(path.read_text(encoding="utf-8"))
        payload = migrate_analyses_payload(raw)
        return {
            tf: decode_analysis(row)
            for tf, row in payload.items()
            if isinstance(row, dict)
        }
    from src.analysis.ict_pa import analyze_timeframe

    log.warning("run archive %s missing analyses.json — rebuilding from enriched", run_id)
    return {tf: analyze_timeframe(df, tf) for tf, df in enriched.items()}


def load_archive_meta(run_id: str) -> dict[str, Any]:
    directory = run_dir(run_id)
    manifest = upgrade_manifest_if_needed(load_manifest(run_id, directory), run_id, directory)
    meta_path = directory / "meta.json"
    if meta_path.is_file():
        legacy = json.loads(meta_path.read_text(encoding="utf-8"))
        legacy["manifest"] = manifest
        return legacy
    return {"manifest": manifest, "run_id": run_id}


def load_report(run_id: str) -> dict[str, Any]:
    directory = run_dir(run_id)
    manifest = load_manifest(run_id, directory)
    report_rel = str((manifest.get("artifacts") or {}).get("report", {}).get("path") or "report.json")
    path = directory / report_rel
    if not path.is_file():
        raise FileNotFoundError(f"run archive report not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_bundle(run_id: str) -> tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]:
    """Load saved (report, enriched, analyses) without re-running the pipeline."""
    directory = run_dir(run_id)
    inspection = inspect_archive(run_id, directory)
    if not inspection.loadable:
        raise ValueError(
            f"run archive {run_id} is not loadable: {'; '.join(inspection.errors)}"
        )

    manifest = upgrade_manifest_if_needed(inspection.manifest, run_id, directory)
    load_warnings = list(inspection.warnings)

    report_raw = load_report(run_id)
    contract_version = int(
        (manifest.get("replay") or {}).get("report_contract_version") or 1
    )
    report, report_warnings = normalize_report(report_raw, contract_version=contract_version)
    load_warnings.extend(report_warnings)

    enriched = load_enriched(run_id)
    analyses = load_analyses(run_id, enriched)

    report.setdefault("meta", {})
    report["meta"]["viewing_replay"] = True
    report["meta"]["viewing_replay_run_id"] = run_id
    report["meta"]["viewing_replay_saved_at"] = manifest.get("saved_at")
    report["meta"]["archive_schema_version"] = inspection.schema_version
    report["meta"]["archive_compatibility"] = inspection.level.value
    report["meta"]["archive_pipeline_status"] = (manifest.get("summary") or {}).get("pipeline_status")
    report["meta"]["archive_replayable"] = inspection.replayable
    report["meta"]["archived_producer_build"] = (manifest.get("producer") or {}).get("build")
    if load_warnings:
        report["meta"]["archive_replay_warnings"] = load_warnings
        log.warning(
            "run archive %s replay degraded: %s",
            run_id,
            "; ".join(load_warnings[:5]),
        )
    return report, enriched, analyses


def load_archive_5m_bars(run_id: str) -> pd.DataFrame:
    """Load 5m OHLCV from a saved run archive (shared contract with backtest)."""
    fetched = load_fetch(run_id)
    if "5m" not in fetched.raw:
        raise FileNotFoundError(f"run archive {run_id} has no 5m bars")
    return fetched.raw["5m"]


def _failure_payload(reason: str, *, step: str | None = None) -> dict[str, Any]:
    return {
        "reason": reason,
        "step": step or "",
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }


def _stub_failure_report(
    *,
    run_config: RunConfig,
    reason: str,
    generation_steps: list[dict] | None = None,
    llm_io: list[dict] | None = None,
    current_price: float | None = None,
) -> dict[str, Any]:
    cfg = run_config.normalized()
    metrics: dict[str, Any] = {}
    if current_price is not None:
        metrics["current_price"] = current_price
    return {
        "metrics": metrics,
        "meta": {
            "title": "流水线未完成 — 问题现场快照",
            "updated_at": format_utc8(datetime.now(timezone.utc).isoformat()),
            "agent_mode": cfg.agent_mode,
            "run_config": cfg.to_dict(),
            "run_config_fingerprint": cfg.fingerprint(),
            "pipeline_status": PIPELINE_STATUS_FAILED,
            "failure_reason": reason,
            "generation_steps": generation_steps or [],
            "llm_io": llm_io or [],
        },
    }


def _persist_archive_folder(
    run_id: str,
    *,
    run_config: RunConfig,
    summary: dict[str, Any],
    report: dict[str, Any],
    fetched: DataFetchResult | None = None,
    enriched: dict[str, pd.DataFrame] | None = None,
    analyses: dict[str, TimeframeAnalysis] | None = None,
    failure: dict[str, Any] | None = None,
) -> Path:
    target = run_dir(run_id)
    target.mkdir(parents=True, exist_ok=True)
    saved_at = datetime.now(timezone.utc).isoformat()
    cfg = run_config.normalized()

    if fetched is not None:
        (target / "fetch.json").write_text(
            json.dumps(_fetch_payload(fetched), ensure_ascii=False),
            encoding="utf-8",
        )
    (target / "report.json").write_text(
        json.dumps(_sanitize_json(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if analyses:
        analyses_body = {tf: encode_analysis(row) for tf, row in analyses.items()}
        (target / "analyses.json").write_text(
            json.dumps(
                artifact_envelope(kind="analysis", artifact_version=ARTIFACT_ANALYSIS, payload=analyses_body),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    if enriched:
        enriched_dir = target / "enriched"
        enriched_dir.mkdir(exist_ok=True)
        for tf, df in enriched.items():
            frame_body = _frame_to_json(df)
            (enriched_dir / f"{tf}.json").write_text(
                json.dumps(
                    artifact_envelope(kind="frame", artifact_version=ARTIFACT_FRAME, payload=frame_body),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
    if failure:
        (target / "failure.json").write_text(
            json.dumps(_sanitize_json(failure), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    pipeline_status = str(summary.get("pipeline_status") or PIPELINE_STATUS_COMPLETE)
    manifest = build_manifest(
        run_id=run_id,
        saved_at=saved_at,
        run_config=cfg.to_dict(),
        summary=summary,
    )
    (target / "manifest.json").write_text(
        json.dumps(_sanitize_json(manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    meta = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "saved_at": saved_at,
        "run_config": cfg.to_dict(),
        "run_config_fingerprint": cfg.fingerprint(),
        "pipeline_status": pipeline_status,
        **summary,
    }
    (target / "meta.json").write_text(
        json.dumps(_sanitize_json(meta), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    inspection = inspect_archive(run_id, target)
    index_row = {
        "run_id": run_id,
        "saved_at": saved_at,
        "schema_version": SCHEMA_VERSION,
        "compatibility": inspection.level.value,
        "pipeline_status": pipeline_status,
        "replayable": inspection.replayable,
        "current_price": summary.get("current_price"),
        "bars_summary": summary.get("bars_summary") or {},
        "run_config": cfg.to_dict(),
        "source_label": summary.get("source_label"),
        "path": str(target),
    }
    upsert_index_entry(archives_root(), index_row)
    all_rows = list_archives(limit=10000)
    prune_archives(archives_root(), all_rows)
    log.info(
        "run archived id=%s schema=v%s status=%s replayable=%s path=%s",
        run_id,
        SCHEMA_VERSION,
        pipeline_status,
        inspection.replayable,
        target,
    )
    return target


def archive_failure_run(
    run_id: str,
    reason: str,
    *,
    run_config: RunConfig,
    elapsed_s: float,
    fetched: DataFetchResult | None = None,
    enriched: dict[str, pd.DataFrame] | None = None,
    analyses: dict[str, TimeframeAnalysis] | None = None,
    report: dict[str, Any] | None = None,
    failure_step: str | None = None,
) -> Path | None:
    """Persist a partial/failed run for forensics (not full replay)."""
    target = run_dir(run_id)
    if target.exists():
        try:
            existing = load_archive_meta(run_id)
            if str(existing.get("pipeline_status") or "") == PIPELINE_STATUS_COMPLETE:
                return target
        except (OSError, json.JSONDecodeError, ValueError):
            pass

    from src.core.progress import get_progress

    prog = get_progress()
    steps = prog.snapshot()
    llm_io = prog.llm_io_snapshot()
    running = [s for s in steps if str(s.get("status") or "") == "running"]
    status = PIPELINE_STATUS_PARTIAL if running else PIPELINE_STATUS_FAILED

    if report is None:
        price = None
        if fetched is not None and fetched.raw.get("5m") is not None and not fetched.raw["5m"].empty:
            price = float(fetched.raw["5m"]["Close"].iloc[-1])
        report = _stub_failure_report(
            run_config=run_config,
            reason=reason,
            generation_steps=steps,
            llm_io=llm_io,
            current_price=price,
        )
    else:
        report.setdefault("meta", {})
        report["meta"]["failure_reason"] = reason
        report["meta"]["pipeline_status"] = status
        if not report["meta"].get("generation_steps"):
            report["meta"]["generation_steps"] = steps
        if not report["meta"].get("llm_io"):
            report["meta"]["llm_io"] = llm_io

    summary = {
        "source_label": fetched.source_label if fetched else None,
        "current_price": report.get("metrics", {}).get("current_price"),
        "bars_summary": fetched.bars_summary if fetched else {},
        "elapsed_s": round(elapsed_s, 3),
        "observation_mode": report.get("meta", {}).get("observation_mode"),
        "pipeline_status": status,
        "failure_reason": reason,
        "failure_step": failure_step or (running[0].get("id") if running else ""),
    }
    return _persist_archive_folder(
        run_id,
        run_config=run_config,
        summary=summary,
        report=report,
        fetched=fetched,
        enriched=enriched or None,
        analyses=analyses or None,
        failure=_failure_payload(reason, step=failure_step),
    )


def load_forensic_bundle(
    run_id: str,
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]:
    """Load a partial/failed archive for problem-scene review (not full chart replay)."""
    directory = run_dir(run_id)
    if not directory.is_dir():
        raise FileNotFoundError(f"run archive not found: {run_id}")

    inspection = inspect_archive(run_id, directory)
    manifest = upgrade_manifest_if_needed(inspection.manifest, run_id, directory)
    summary = manifest.get("summary") or {}

    report: dict[str, Any]
    report_warnings: list[str] = []
    try:
        report_raw = load_report(run_id)
        contract_version = int((manifest.get("replay") or {}).get("report_contract_version") or 1)
        report, report_warnings = normalize_report(report_raw, contract_version=contract_version)
    except FileNotFoundError:
        failure_path = directory / "failure.json"
        reason = "unknown failure"
        if failure_path.is_file():
            failure = json.loads(failure_path.read_text(encoding="utf-8"))
            reason = str(failure.get("reason") or reason)
        cfg_dict = manifest.get("run_config") if isinstance(manifest.get("run_config"), dict) else {}
        stub_cfg = RunConfig.from_dict(cfg_dict)
        report, report_warnings = normalize_report(
            _stub_failure_report(run_config=stub_cfg, reason=reason),
            contract_version=1,
        )

    load_warnings = list(inspection.warnings) + report_warnings
    try:
        enriched = load_enriched(run_id)
    except (FileNotFoundError, ValueError):
        enriched = {}
        load_warnings.append("enriched bars unavailable — charts may be empty")
    try:
        analyses = load_analyses(run_id, enriched) if enriched else {}
    except (FileNotFoundError, ValueError):
        analyses = {}

    report.setdefault("meta", {})
    report["meta"]["viewing_replay"] = True
    report["meta"]["viewing_replay_forensic"] = True
    report["meta"]["viewing_replay_run_id"] = run_id
    report["meta"]["viewing_replay_saved_at"] = manifest.get("saved_at")
    report["meta"]["archive_schema_version"] = inspection.schema_version
    report["meta"]["archive_compatibility"] = inspection.level.value
    report["meta"]["archive_pipeline_status"] = summary.get("pipeline_status")
    report["meta"]["archive_replayable"] = inspection.replayable
    report["meta"]["archived_producer_build"] = (manifest.get("producer") or {}).get("build")
    if summary.get("failure_reason"):
        report["meta"]["failure_reason"] = summary.get("failure_reason")
    if load_warnings:
        report["meta"]["archive_replay_warnings"] = load_warnings
    return report, enriched, analyses


def archive_run(
    run_id: str,
    *,
    fetched: DataFetchResult,
    report: dict[str, Any],
    enriched: dict[str, pd.DataFrame],
    analyses: dict[str, TimeframeAnalysis],
    run_config: RunConfig,
    elapsed_s: float,
) -> Path:
    cfg = run_config.normalized()
    meta = report.get("meta") or {}
    pipeline_status = str(meta.get("pipeline_status") or PIPELINE_STATUS_COMPLETE)
    if pipeline_status == PIPELINE_STATUS_COMPLETE:
        assert_pipeline_replay_ready(report)
    summary = {
        "source_label": fetched.source_label,
        "current_price": report.get("metrics", {}).get("current_price"),
        "bars_summary": fetched.bars_summary,
        "elapsed_s": round(elapsed_s, 3),
        "observation_mode": meta.get("observation_mode"),
        "pipeline_status": pipeline_status,
    }
    return _persist_archive_folder(
        run_id,
        run_config=cfg,
        summary=summary,
        report=report,
        fetched=fetched,
        enriched=enriched,
        analyses=analyses,
    )
