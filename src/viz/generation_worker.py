"""Background report generation worker for Streamlit."""

from __future__ import annotations

import threading

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import RunConfig
from src.core.run_context import reset_run_config, set_run_config
from src.log import get_logger
from src.pipeline import run_analysis
from src.viz.generation_state import access_job, create_job, get_job
from src.viz.replay_loader import load_replay_bundle

log = get_logger(__name__)

_GEN_LOCK = threading.Lock()


class ModuleSyncProgressReporter(ProgressReporter):
    """Sync pipeline progress to module state for live UI polling."""

    def __init__(self, job_key: str) -> None:
        super().__init__()
        self._job_key = job_key
        self._sync()

    def _sync(self) -> None:
        from src.viz.generation_state import update_live

        with self._lock:
            job = access_job(self._job_key)
            prev = (job.live if job else {}) or {}
            external = self.external_snapshot or prev.get("external")
            steps = self.snapshot()
            snapshot = {
                "steps": steps,
                "llm_io": self.llm_io_snapshot(),
                "external": external,
                "headline": self._headline_from_steps(steps),
            }
        update_live(self._job_key, snapshot)

    @staticmethod
    def _headline_from_steps(steps: list[dict]) -> str:
        from src.viz.pipeline_progress import pipeline_progress_headline

        return pipeline_progress_headline(steps)

    def _on_change(self) -> None:
        self._sync()

    def _on_llm_chunk(self, stage: str, chunk: str) -> None:
        super()._on_llm_chunk(stage, chunk)
        self._sync()

    def llm_begin(self, stage: str, model: str, messages: list[dict[str, str]]) -> None:
        super().llm_begin(stage, model, messages)
        self._sync()

    def llm_end(self, stage: str, output: str, *, error: str | None = None, latency_ms: int | None = None) -> None:
        super().llm_end(stage, output, error=error, latency_ms=latency_ms)
        self._sync()

    def fail(self, step_id: str, detail: str = "") -> None:
        super().fail(step_id, detail)
        self._sync()

    def done(self, step_id: str, detail: str = "") -> None:
        super().done(step_id, detail)
        self._sync()

    def update(self, step_id: str, *, detail: str | None = None, label: str | None = None) -> None:
        super().update(step_id, detail=detail, label=label)
        self._sync()

    def stage_io(
        self,
        stage: str,
        *,
        input_text: str,
        output_text: str,
        latency_ms: int | None = None,
        label: str | None = None,
    ) -> None:
        super().stage_io(
            stage,
            input_text=input_text,
            output_text=output_text,
            latency_ms=latency_ms,
            label=label,
        )
        self._sync()


def format_generation_error(exc: BaseException) -> str:
    raw = str(exc or type(exc).__name__).strip()
    if not raw:
        return type(exc).__name__
    network_hint = "若在国内网络，可能需要代理/VPN 才能连接 TradingView WebSocket。"
    raw = raw.replace(f"{network_hint}. {network_hint}", network_hint)
    raw = raw.replace(f"{network_hint}。 {network_hint}", network_hint)
    if "TradingView fetch failed" in raw:
        if "returned empty data" in raw:
            return f"数据拉取失败：TradingView 返回空数据。{network_hint}"
        return f"数据拉取失败：{raw}"
    return raw


def start_generation(job_key: str, run_config: RunConfig, *, session_id: str) -> None:
    with _GEN_LOCK:
        job = get_job(job_key, session_id=session_id)
        if job is None:
            job = create_job(session_id, job_key.split(":", 1)[1])
        if job.result is not None or job.error is not None:
            return
        if job.thread and job.thread.is_alive():
            return

        if run_config.replay_mode and run_config.replay_run_id:
            active = access_job(job_key)
            try:
                bundle = load_replay_bundle(run_config)
                if active is not None:
                    active.result = bundle
                log.info(
                    "replay loaded run_id=%s price=%.2f",
                    run_config.replay_run_id,
                    bundle[0]["metrics"]["current_price"],
                )
            except BaseException as exc:
                log.exception("replay load failed run_id=%s", run_config.replay_run_id)
                if active is not None:
                    active.error = exc
            return

        def worker() -> None:
            from src.data.fetcher import clear_cache

            reporter = ModuleSyncProgressReporter(job_key)
            cfg_token = set_run_config(run_config.normalized())
            prog_token = set_progress(reporter)
            active = access_job(job_key)
            try:
                clear_cache()
                bundle = run_analysis()
                bundle[0].setdefault("meta", {})["run_config"] = run_config.to_dict()
                bundle[0]["meta"]["run_config_fingerprint"] = run_config.fingerprint()
                if active is not None:
                    active.result = bundle
                log.info(
                    "report ready price=%.2f job=%s config=%s",
                    bundle[0]["metrics"]["current_price"],
                    job_key,
                    run_config.to_dict(),
                )
            except BaseException as exc:
                log.exception("report generation failed job=%s", job_key)
                if active is not None:
                    active.error = exc
            finally:
                reset_progress(prog_token)
                reset_run_config(cfg_token)

        thread = threading.Thread(target=worker, daemon=True, name=f"report-gen-{job_key[:8]}")
        job.thread = thread
        thread.start()
