"""Single entry point for UI replay — inspect + load_bundle or forensic snapshot."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.run import RunConfig, inspect_run_archive, load_bundle
from src.run.archive.schema import CompatibilityLevel
from src.run.archive.store import load_fetch, load_forensic_bundle


def _upgrade_to_advice_v2(
    run_id: str,
    bundle: tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]:
    report, enriched, analyses = bundle
    if report.get("artifact_kind") == "human_review_advice" and report.get("advice"):
        return bundle
    from src.advice import build_advice_packet, build_advice_report
    from src.core.types import ExternalFactors
    from src.data.aggregator import assemble_market_context

    replay_warnings = ["旧报告内容已忽略；Advice V2 使用归档行情和结构事实重新生成建议。"]
    try:
        fetched = load_fetch(run_id)
        external = fetched.external
        source_label = fetched.source_label
    except (FileNotFoundError, ValueError):
        external = ExternalFactors(
            fetch_errors=["旧归档不含可用的外部数据快照；本次建议仅使用归档行情和结构事实。"]
        )
        source_label = str((report.get("meta") or {}).get("source_label") or "archive")
        replay_warnings.append("外部背景快照不可用；不会重新联网获取数据。")
    ctx = assemble_market_context(enriched, analyses, external, source_label)
    saved_at = (report.get("meta") or {}).get("viewing_replay_saved_at")
    if saved_at:
        parsed = pd.Timestamp(saved_at)
        if parsed.tzinfo is None:
            parsed = parsed.tz_localize("UTC")
        ctx.derived["evaluation_time"] = parsed.to_pydatetime()
    advice = build_advice_packet(ctx)
    rebuilt = build_advice_report(
        ctx,
        advice,
        run_id=run_id,
        run_config={"replay_mode": True, "replay_run_id": run_id},
    )
    rebuilt["meta"].update(
        {
            "viewing_replay": True,
            "viewing_replay_run_id": run_id,
            "rebuilt_from_legacy_archive": True,
            "archive_replay_warnings": replay_warnings,
        }
    )
    return rebuilt, enriched, analyses


def load_replay_bundle(
    run_config: RunConfig,
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]:
    """Load a saved run for replay or forensic review."""
    cfg = run_config.normalized()
    if not cfg.replay_mode or not cfg.replay_run_id:
        raise ValueError("replay mode requires replay_run_id")

    run_id = cfg.replay_run_id
    inspection = inspect_run_archive(run_id)
    if inspection.level == CompatibilityLevel.INCOMPATIBLE:
        detail = "; ".join(inspection.errors) or "incompatible archive"
        raise ValueError(f"run archive {run_id}: {detail}")

    if inspection.loadable:
        try:
            return _upgrade_to_advice_v2(run_id, load_bundle(run_id))
        except (FileNotFoundError, ValueError):
            if inspection.replayable:
                raise
    bundle = load_forensic_bundle(run_id)
    if bundle[1] and bundle[2]:
        try:
            return _upgrade_to_advice_v2(run_id, bundle)
        except (FileNotFoundError, ValueError):
            pass
    return bundle

