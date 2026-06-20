"""Tests for src.core.parallel."""

from __future__ import annotations

import contextvars
import time

from src.core.parallel import ParallelTaskError, run_parallel

_test_ctx: contextvars.ContextVar[int] = contextvars.ContextVar("parallel_test_ctx", default=0)


def test_run_parallel_single_task() -> None:
    results = run_parallel([("a", lambda: 42)], max_workers=4)
    assert results == {"a": 42}


def test_run_parallel_collects_results() -> None:
    results = run_parallel(
        [
            ("a", lambda: 1),
            ("b", lambda: 2),
            ("c", lambda: 3),
        ],
        max_workers=3,
    )
    assert results == {"a": 1, "b": 2, "c": 3}


def test_run_parallel_propagates_contextvar() -> None:
    token = _test_ctx.set(99)

    def read_ctx() -> int:
        return _test_ctx.get()

    try:
        results = run_parallel([("x", read_ctx)], max_workers=1)
        assert results["x"] == 99
    finally:
        _test_ctx.reset(token)


def test_run_parallel_faster_than_serial(monkeypatch) -> None:
    delay = 0.12

    def slow(name: str):
        def _fn() -> str:
            time.sleep(delay)
            return name

        return _fn

    t0 = time.perf_counter()
    run_parallel(
        [(f"t{i}", slow(f"t{i}")) for i in range(4)],
        max_workers=4,
    )
    parallel_elapsed = time.perf_counter() - t0

    t0 = time.perf_counter()
    for i in range(4):
        time.sleep(delay)
    serial_elapsed = time.perf_counter() - t0

    assert parallel_elapsed < serial_elapsed * 0.75


def test_run_parallel_raise_on_error() -> None:
    def boom() -> None:
        raise ValueError("boom")

    try:
        run_parallel([("ok", lambda: 1), ("bad", boom)], max_workers=2, raise_on_error=True)
        assert False, "expected ParallelTaskError"
    except ParallelTaskError as exc:
        assert "bad" in exc.errors
