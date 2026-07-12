"""Background generation worker — replay short-circuit and error formatting."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.core.run_config import RunConfig, run_config_for_mode
from src.viz import generation_state as gs
from src.viz.generation_worker import format_generation_error, start_generation


@pytest.fixture
def clean_generation_state() -> None:
    gs._STORE.clear()
    yield
    gs._STORE.clear()


def test_format_generation_error_tradingview_empty_data() -> None:
    raw = "TradingView fetch failed: returned empty data"
    msg = format_generation_error(RuntimeError(raw))
    assert "TradingView 返回空数据" in msg
    assert "代理" in msg or "VPN" in msg


def test_format_generation_error_deduplicates_network_hint() -> None:
    hint = "若在国内网络，可能需要代理/VPN 才能连接 TradingView WebSocket。"
    raw = f"TradingView fetch failed: timeout. {hint}. {hint}"
    msg = format_generation_error(RuntimeError(raw))
    assert msg.count(hint) == 1


def test_format_generation_error_plain_exception() -> None:
    assert format_generation_error(ValueError("bad config")) == "bad config"


def test_start_generation_replay_loads_bundle_without_thread(clean_generation_state) -> None:
    bundle = ({"metrics": {"current_price": 2650.0}, "meta": {}}, {"5m": object()}, {"5m": {}})
    cfg = RunConfig(replay_mode=True, replay_run_id="20260101T120000Z").normalized()
    job_key = "sess-1:gen-1"
    gs.create_job("sess-1", "gen-1")

    with patch("src.viz.generation_worker.load_replay_bundle", return_value=bundle) as load_replay:
        start_generation(job_key, cfg, session_id="sess-1")

    load_replay.assert_called_once_with(cfg)
    job = gs.access_job(job_key)
    assert job is not None
    assert job.result is bundle
    assert job.thread is None or not job.thread.is_alive()


def test_start_generation_replay_failure_sets_job_error(clean_generation_state) -> None:
    cfg = RunConfig(replay_mode=True, replay_run_id="missing").normalized()
    job_key = "sess-2:gen-2"
    gs.create_job("sess-2", "gen-2")

    with patch("src.viz.generation_worker.load_replay_bundle", side_effect=ValueError("not found")):
        start_generation(job_key, cfg, session_id="sess-2")

    job = gs.access_job(job_key)
    assert job is not None
    assert isinstance(job.error, ValueError)
    assert "not found" in str(job.error)


def test_start_generation_live_run_binds_normalized_config(clean_generation_state) -> None:
    cfg = RunConfig(agent_mode="llm", llm_enabled=True, llm_stage_trader=True)
    job_key = "sess-3:gen-3"
    gs.create_job("sess-3", "gen-3")
    bundle = ({"metrics": {"current_price": 1.0}, "meta": {}}, {}, {})

    captured: dict = {}

    def fake_set_run_config(config):
        captured["config"] = config
        return MagicMock()

    def fake_worker_run():
        pass

    with patch("src.viz.generation_worker.set_run_config", side_effect=fake_set_run_config), patch(
        "src.viz.generation_worker.set_progress", return_value=MagicMock()
    ), patch("src.viz.generation_worker.reset_progress"), patch(
        "src.viz.generation_worker.reset_run_config"
    ), patch("src.data.fetcher.clear_cache"), patch(
        "src.viz.generation_worker.run_analysis", return_value=bundle
    ), patch("threading.Thread") as thread_cls:
        thread_cls.return_value = MagicMock()
        start_generation(job_key, cfg, session_id="sess-3")

        worker_target = thread_cls.call_args.kwargs.get("target") or thread_cls.call_args[1]["target"]
        worker_target()

    assert captured["config"] == cfg.normalized()
    thread_cls.assert_called_once()
