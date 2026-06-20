"""Unit tests for external data page helpers."""

from __future__ import annotations

import pandas as pd

from src.core.types import ExternalFactors, HeadlineItem
from src.data.fetch_pipeline import DataFetchResult
from src.viz.dashboard_components import _source_tags
from src.viz.external_data_view import external_payload_from_report, external_snapshot_from_fetch


def test_external_snapshot_from_fetch_includes_headlines() -> None:
    ext = ExternalFactors(
        dxy_impact="DXY 99.5",
        news_headlines=["黄金反弹"],
        headline_items=[
            HeadlineItem(source="jin10_flash", time="2026-01-01", title="测试快讯", text="", url=""),
        ],
        sources=["jin10_flash"],
    )
    fetched = DataFetchResult(raw={"5m": pd.DataFrame({"c": [1]})}, external=ext, source_label="TV")
    snap = external_snapshot_from_fetch(fetched)
    assert snap["dxy_impact"] == "DXY 99.5"
    assert snap["flash_headlines"]
    assert snap["phase"] == "fetch"


def test_external_payload_from_report_merges_calendar() -> None:
    report = {
        "meta": {"data_source": "TradingView"},
        "external": {"dxy_impact": "—", "news_topics": ["美联储"]},
        "calendar_events": [{"time": "10:00", "event": "CPI", "flag": "🇺🇸"}],
    }
    payload = external_payload_from_report(report, {"5m": pd.DataFrame(), "1d": pd.DataFrame()})
    assert payload["phase"] == "report"
    assert payload["calendar_events"][0]["event"] == "CPI"
    assert payload["news_topics"] == ["美联储"]


def test_placeholder_source_renders_orange_tag() -> None:
    html_out = _source_tags(["placeholder", "jin10_flash"])
    assert "ext-src-placeholder" in html_out
    assert "占位/回退" in html_out
    assert "金十快讯" in html_out
