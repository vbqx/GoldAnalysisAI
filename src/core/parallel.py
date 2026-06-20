"""Thread-pool helpers with ContextVar propagation for pipeline parallelism."""

from __future__ import annotations

import contextvars
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TypeVar

from src.log import get_logger

log = get_logger(__name__)

T = TypeVar("T")


class ParallelTaskError(Exception):
    """One or more parallel tasks failed."""

    def __init__(self, errors: dict[str, BaseException]) -> None:
        self.errors = errors
        names = ", ".join(sorted(errors))
        super().__init__(f"parallel tasks failed: {names}")


def run_parallel(
    tasks: list[tuple[str, Callable[[], T]]],
    *,
    max_workers: int,
    label: str = "",
    raise_on_error: bool = False,
) -> dict[str, T]:
    """Run independent callables in a thread pool.

    Each worker runs inside ``copy_context()`` so ``ContextVar`` values such as
    ``ProgressReporter`` are visible in child threads.
    """
    if not tasks:
        return {}

    workers = max(1, min(max_workers, len(tasks)))
    if len(tasks) == 1:
        name, fn = tasks[0]
        return {name: fn()}

    def _run(
        name: str,
        fn: Callable[[], T],
        worker_ctx: contextvars.Context,
    ) -> tuple[str, T | None, BaseException | None]:
        try:
            return name, worker_ctx.run(fn), None
        except BaseException as exc:
            return name, None, exc

    results: dict[str, T] = {}
    errors: dict[str, BaseException] = {}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_run, name, fn, contextvars.copy_context()): name
            for name, fn in tasks
        }
        for future in as_completed(futures):
            name, value, err = future.result()
            if err is not None:
                errors[name] = err
                log.warning("parallel task %s failed%s: %s", name, f" ({label})" if label else "", err)
            else:
                results[name] = value  # type: ignore[assignment]

    if errors and raise_on_error:
        raise ParallelTaskError(errors)
    return results
