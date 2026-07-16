"""ModuleSyncProgressReporter must accept llm_begin telemetry kwargs (#37/#runtime)."""

from __future__ import annotations

from src.viz.generation_worker import ModuleSyncProgressReporter


def test_module_sync_llm_begin_accepts_telemetry(monkeypatch) -> None:
    updates: list[dict] = []

    monkeypatch.setattr(
        "src.viz.generation_state.update_live",
        lambda _key, snapshot: updates.append(snapshot),
    )
    monkeypatch.setattr(
        "src.viz.generation_worker.access_job",
        lambda _key: type("J", (), {"live": {}})(),
    )

    reporter = ModuleSyncProgressReporter("job-test")
    reporter.llm_begin(
        "technical",
        "m",
        [{"role": "user", "content": "hi"}],
        telemetry={"tier": "fast", "input_chars": 12, "budget_action": "none"},
    )
    reporter.llm_end(
        "technical",
        '{"ok":true}',
        latency_ms=10,
        telemetry={"output_chars": 9},
    )
    snap = reporter.llm_io_snapshot()
    assert snap[-1]["tier"] == "fast"
    assert snap[-1]["input_chars"] == 12
    assert updates  # synced to live state
