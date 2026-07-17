"""Dynamic boundary verification for previously indirect high-risk units."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.core import orchestrator
from src.viz import report_views


class _Context:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


class _StreamlitDouble:
    def __init__(self) -> None:
        self.markdown = Mock()
        self.warning = Mock()
        self.info = Mock()
        self.caption = Mock()
        self.plotly_chart = Mock()

    @staticmethod
    def columns(spec, **_kwargs):
        count = spec if isinstance(spec, int) else len(spec)
        return [_Context() for _ in range(count)]

    @staticmethod
    def container(**_kwargs):
        return _Context()


def test_run_trade_agent_pipeline_propagates_fetch_boundary_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The top-level state machine must not hide an explicit fetch failure."""
    failure = RuntimeError("controlled fetch failure")
    begin = Mock(return_value=("run-id", 0.0))
    fetch = Mock(side_effect=failure)
    monkeypatch.setattr(orchestrator, "begin_pipeline_run", begin)
    monkeypatch.setattr(orchestrator, "get_progress", Mock())
    monkeypatch.setattr(orchestrator, "fetch_market_data", fetch)

    with pytest.raises(RuntimeError) as caught:
        orchestrator.run_trade_agent_pipeline()

    assert caught.value is failure
    begin.assert_called_once_with()
    fetch.assert_called_once_with()


def test_render_institutional_report_composes_controlled_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The long report renderer composes its child contracts without live UI."""
    st = _StreamlitDouble()
    chart = Mock()
    donut = Mock()
    monkeypatch.setattr(report_views, "st", st)
    monkeypatch.setattr(report_views, "_embed_chart", chart)
    monkeypatch.setattr(report_views, "build_sentiment_donut", Mock(return_value=donut))
    monkeypatch.setattr(report_views, "chart_iframe_height", Mock(return_value=80))
    monkeypatch.setattr(report_views, "conclusion_display_lines", Mock(return_value=["wait"]))
    for name in (
        "render_final_decision_banner",
        "render_decision_summary",
        "render_narrative_section",
        "render_trading_plans",
        "render_bottom_row",
        "render_footer",
    ):
        monkeypatch.setattr(report_views, name, Mock(return_value=f"<{name}>"))

    report = {
        "meta": {"title": "report", "updated_at": "now", "methodology": "rule"},
        "conclusion": {},
        "narrative_sections": {key: {"text": key} for key in ("market_overview", "liquidity", "4h", "1h", "15m")},
        "sentiment": {"bullish": 30, "bearish": 40, "ranging": 30},
        "timeframes": {key: {} for key in ("4h", "1h", "15m")},
        "signals": [],
    }
    analyses = {key: object() for key in ("4h", "1h", "15m", "5m")}

    report_views.render_institutional_report(report, {}, analyses)

    assert chart.call_count == 4
    donut.update_layout.assert_called_once()
    assert st.markdown.call_count >= 8
