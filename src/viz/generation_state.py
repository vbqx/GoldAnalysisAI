"""Background report generation jobs — keyed by session + generation UUID."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any

_GEN_TTL_S = 3600.0


@dataclass
class GenerationJob:
    session_id: str
    generation_id: str
    thread: threading.Thread | None = None
    result: tuple[dict, dict, dict] | None = None
    error: BaseException | None = None
    live: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.monotonic)

    @property
    def key(self) -> str:
        return f"{self.session_id}:{self.generation_id}"


_STORE: dict[str, GenerationJob] = {}
_LOCK = threading.Lock()


def purge_expired() -> None:
    now = time.monotonic()
    with _LOCK:
        stale = [k for k, job in _STORE.items() if now - job.created_at > _GEN_TTL_S]
        for key in stale:
            _STORE.pop(key, None)


def access_job(job_key: str) -> GenerationJob | None:
    purge_expired()
    with _LOCK:
        return _STORE.get(job_key)


def get_job(job_key: str, *, session_id: str) -> GenerationJob | None:
    purge_expired()
    with _LOCK:
        job = _STORE.get(job_key)
    if job is None or job.session_id != session_id:
        return None
    return job


def create_job(session_id: str, generation_id: str) -> GenerationJob:
    purge_expired()
    job = GenerationJob(session_id=session_id, generation_id=generation_id)
    with _LOCK:
        _STORE[job.key] = job
    return job


def drop_job(job_key: str, *, session_id: str) -> None:
    with _LOCK:
        job = _STORE.get(job_key)
        if job and job.session_id == session_id:
            _STORE.pop(job_key, None)


def update_live(job_key: str, snapshot: dict[str, Any]) -> None:
    with _LOCK:
        job = _STORE.get(job_key)
        if job is not None:
            job.live = snapshot
