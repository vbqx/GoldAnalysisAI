"""Progress reporter thread-safety tests."""

from __future__ import annotations

import threading

from src.core.progress import ProgressReporter


def test_progress_concurrent_llm_io() -> None:
    reporter = ProgressReporter()
    stages = ("technical", "fundamentals", "news", "sentiment")

    def worker(stage: str) -> None:
        reporter.llm_begin(stage, "test-model", [{"role": "user", "content": stage}])
        for chunk in ("a", "b", "c"):
            reporter._on_llm_chunk(stage, chunk)
        reporter.llm_end(stage, f'{{"stage":"{stage}"}}', latency_ms=5)

    threads = [threading.Thread(target=worker, args=(s,)) for s in stages]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    snapshot = reporter.llm_io_snapshot()
    assert len(snapshot) == 4
    by_stage = {r["stage"]: r for r in snapshot}
    for stage in stages:
        assert stage in by_stage
        assert by_stage[stage]["model"] == "test-model"
        assert by_stage[stage]["latency_ms"] == 5
