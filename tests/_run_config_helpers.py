"""Helpers for binding RunConfig in unit tests (ContextVar, not module globals)."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

from src.core.run_config import RunConfig, run_config_from_env
from src.core.run_context import reset_run_config, set_run_config


@contextmanager
def bind_run_config(**overrides: Any) -> Iterator[RunConfig]:
    """Bind RunConfig for the current test thread; restore previous on exit."""
    data = run_config_from_env().to_dict()
    data.update(overrides)
    cfg = RunConfig.from_dict(data)
    token = set_run_config(cfg)
    try:
        yield cfg
    finally:
        reset_run_config(token)
