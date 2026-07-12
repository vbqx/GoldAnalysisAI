"""Thread-local runtime configuration for pipeline runs (no module-global mutation)."""

from __future__ import annotations

from contextvars import ContextVar, Token
from contextlib import contextmanager
from typing import Iterator

from src.run.config import RunConfig, run_config_from_env

_run_config: ContextVar[RunConfig | None] = ContextVar("run_config", default=None)


def set_run_config(config: RunConfig) -> Token:
    """Bind immutable run config to the current thread / async context."""
    return _run_config.set(config.normalized())


def reset_run_config(token: Token) -> None:
    _run_config.reset(token)


def get_run_config() -> RunConfig:
    cfg = _run_config.get()
    if cfg is not None:
        return cfg
    return run_config_from_env()


@contextmanager
def run_config_scope(config: RunConfig) -> Iterator[RunConfig]:
    """Context manager for tests and background workers."""
    token = set_run_config(config)
    try:
        yield config.normalized()
    finally:
        reset_run_config(token)


def agent_mode() -> str:
    return get_run_config().agent_mode


def llm_narrative_enabled() -> bool:
    cfg = get_run_config()
    return bool(cfg.llm_enabled) and cfg.agent_mode in ("llm", "hybrid")
