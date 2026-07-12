"""Run archive save/load and replay selection tests."""

from __future__ import annotations

import pandas as pd
import pytest

from src.analysis.ict_pa import TimeframeAnalysis, analyze_timeframe
from src.core.run_config import RunConfig, run_config_for_mode
from src.core.types import CalendarEvent, ExternalFactors, HeadlineItem, MacroQuote
from src.data.fetch_pipeline import DataFetchResult
from src.data.run_archive import (
    allocate_run_id,
    archive_label,
    archive_run,
    archives_exist,
    decode_analysis,
    encode_analysis,
    list_archives,
    load_analyses,
    load_bundle,
    load_fetch,
    load_report,
    run_dir,
)


def _sample_fetch() -> DataFetchResult:
    idx = pd.date_range("2026-06-01", periods=24, freq="5min", tz="UTC")
    close = pd.Series(2650.0, index=idx)
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": [100] * len(idx),
        },
        index=idx,
    )
    external = ExternalFactors(
        dxy_impact="偏强",
        risk_events="CPI",
        news_headlines=["样例新闻"],
        headline_items=[HeadlineItem(source="jin10_flash", text="快讯", time="2026-06-01 10:00")],
        calendar_events=[CalendarEvent(time="2026-06-02 20:30", region="US", event="NFP", importance=5.0)],
        macro_quotes=[
            MacroQuote(
                name="DXY",
                symbol="DXY",
                close=104.2,
                change_pct=0.3,
                impact="偏强",
                bias="bearish",
            )
        ],
        social_sentiment="偏多",
        social_posts=[{"title": "post", "bullish_votes": 10}],
        sources=["tradingview", "jin10"],
        fetch_errors=[],
    )
    return DataFetchResult(raw={"5m": df, "15m": df}, external=external, source_label="tradingview")


def test_analysis_roundtrip() -> None:
    idx = pd.date_range("2026-06-01", periods=60, freq="5min", tz="UTC")
    close = pd.Series(2650.0, index=idx)
    df = pd.DataFrame(
        {"Open": close, "High": close + 1, "Low": close - 1, "Close": close, "Volume": 100},
        index=idx,
    )
    original = analyze_timeframe(df, "5m")
    restored = decode_analysis(encode_analysis(original))
    assert restored.timeframe == original.timeframe
    assert restored.trend == original.trend
    assert len(restored.order_blocks) == len(original.order_blocks)


def test_archive_roundtrip_and_load_bundle(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    fetched = _sample_fetch()
    enriched = {"5m": fetched.raw["5m"]}
    analyses = {"5m": analyze_timeframe(enriched["5m"], "5m")}
    report = {
        "metrics": {"current_price": 2650.0},
        "meta": {"agent_mode": "llm"},
        "llm_analysis": {"enabled": True, "market_summary": "测试"},
    }
    archive_run(
        run_id,
        fetched=fetched,
        report=report,
        enriched=enriched,
        analyses=analyses,
        run_config=run_config_for_mode("llm"),
        elapsed_s=12.5,
    )
    assert archives_exist()
    rows = list_archives()
    assert len(rows) == 1
    assert rows[0]["run_id"] == run_id
    assert "2650" in archive_label(rows[0])

    bundle = load_bundle(run_id)
    assert bundle[0]["llm_analysis"]["market_summary"] == "测试"
    assert bundle[0]["meta"]["viewing_replay"] is True
    assert "5m" in bundle[1]
    assert isinstance(bundle[2]["5m"], TimeframeAnalysis)

    assert len(load_fetch(run_id).raw["5m"]) == 24
    assert load_report(run_id)["metrics"]["current_price"] == 2650.0
    assert (run_dir(run_id) / "analyses.json").is_file()
    assert (run_dir(run_id) / "manifest.json").is_file()


def test_load_analyses_rebuilds_when_missing(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    fetched = _sample_fetch()
    enriched = {"5m": fetched.raw["5m"]}
    report = {"metrics": {"current_price": 2650.0}, "meta": {}}
    archive_run(
        run_id,
        fetched=fetched,
        report=report,
        enriched=enriched,
        analyses={"5m": analyze_timeframe(enriched["5m"], "5m")},
        run_config=run_config_for_mode("rule"),
        elapsed_s=1.0,
    )
    (run_dir(run_id) / "analyses.json").unlink()
    analyses = load_analyses(run_id, enriched)
    assert "5m" in analyses


def test_replay_run_config_fingerprint() -> None:
    a = RunConfig(replay_mode=True, replay_run_id="20260712T074512Z").normalized()
    b = RunConfig(replay_mode=True, replay_run_id="20260712T080000Z").normalized()
    assert a.fingerprint() != b.fingerprint()


def test_load_missing_archive_raises(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    with pytest.raises(ValueError):
        load_bundle("missing-run")


def test_legacy_v1_archive_without_manifest_loads(tmp_path, monkeypatch) -> None:
    """Pre-manifest folders (schema v1) must remain replayable after app upgrades."""
    import json

    from src.data.run_archive_schema import artifact_envelope, ARTIFACT_FRAME

    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = "20260101T120000Z"
    folder = run_dir(run_id)
    folder.mkdir(parents=True)
    idx = pd.date_range("2026-06-01", periods=12, freq="5min", tz="UTC")
    close = pd.Series(2650.0, index=idx)
    df = pd.DataFrame(
        {"Open": close, "High": close + 1, "Low": close - 1, "Close": close, "Volume": 100},
        index=idx,
    )
    frame = {
        "columns": list(df.columns),
        "index": [ts.isoformat() for ts in df.index],
        "data": df.values.tolist(),
    }
    (folder / "meta.json").write_text(
        json.dumps(
            {
                "version": 1,
                "run_id": run_id,
                "saved_at": "2026-01-01T12:00:00+00:00",
                "run_config": {"agent_mode": "llm"},
                "current_price": 2650.0,
                "bars_summary": {"5m": 12},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (folder / "report.json").write_text(
        json.dumps({"metrics": {"current_price": 2650.0}}, ensure_ascii=False),
        encoding="utf-8",
    )
    enriched_dir = folder / "enriched"
    enriched_dir.mkdir()
    (enriched_dir / "5m.json").write_text(
        json.dumps(
            artifact_envelope(kind="frame", artifact_version=ARTIFACT_FRAME, payload=frame),
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    bundle = load_bundle(run_id)
    assert bundle[0]["metrics"]["current_price"] == 2650.0
    assert (folder / "manifest.json").is_file()


def test_inspect_marks_missing_analyses_degraded(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run.archive.store.archives_root", lambda: tmp_path)
    run_id = allocate_run_id()
    fetched = _sample_fetch()
    enriched = {"5m": fetched.raw["5m"]}
    archive_run(
        run_id,
        fetched=fetched,
        report={"metrics": {"current_price": 2650.0}, "meta": {}},
        enriched=enriched,
        analyses={"5m": analyze_timeframe(enriched["5m"], "5m")},
        run_config=run_config_for_mode("rule"),
        elapsed_s=1.0,
    )
    (run_dir(run_id) / "analyses.json").unlink()
    from src.data.run_archive import inspect_run_archive
    from src.data.run_archive_schema import CompatibilityLevel

    inspection = inspect_run_archive(run_id)
    assert inspection.loadable
    assert inspection.level == CompatibilityLevel.DEGRADED

