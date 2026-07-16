"""Background report generation worker for Streamlit."""

from __future__ import annotations

import threading
import time

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import RunConfig
from src.core.run_context import reset_run_config, set_run_config
from src.log import get_logger
from src.pipeline import run_analysis
from src.viz.generation_state import access_job, create_job, get_job
from src.viz.replay_loader import load_replay_bundle

log = get_logger(__name__)

_GEN_LOCK = threading.Lock()
_LIVE_LLM_OUTPUT_CAP = 6000
_LIVE_LLM_MESSAGE_CAP = 800
_CHUNK_SYNC_INTERVAL_S = 1.5


def _is_streaming_llm_record(rec: dict) -> bool:
    if rec.get("kind") == "rule" or rec.get("model") == "规则引擎":
        return False
    if rec.get("error"):
        return False
    return rec.get("latency_ms") is None


def compact_llm_io_for_live(records: list[dict]) -> list[dict]:
    """Trim LLM I/O for polling UI — avoids multi-MB widget payloads during streaming."""
    compacted: list[dict] = []
    for rec in records:
        streaming = _is_streaming_llm_record(rec)
        row: dict = {
            "stage": rec.get("stage"),
            "label": rec.get("label"),
            "model": rec.get("model"),
            "error": rec.get("error"),
            "latency_ms": rec.get("latency_ms"),
            "kind": rec.get("kind"),
            "tier": rec.get("tier"),
            "attempt": rec.get("attempt"),
            "input_chars": rec.get("input_chars"),
            "input_tokens_est": rec.get("input_tokens_est"),
            "output_chars": rec.get("output_chars"),
            "output_tokens_est": rec.get("output_tokens_est"),
            "budget_action": rec.get("budget_action"),
            "same_model_strategy": rec.get("same_model_strategy"),
        }
        if streaming:
            row["output"] = ""
            row["stream_chars"] = len(str(rec.get("output") or ""))
            row["messages"] = []
        else:
            row["output"] = str(rec.get("output") or "")
            trimmed_msgs: list[dict[str, str]] = []
            for msg in (rec.get("messages") or [])[:3]:
                content = str(msg.get("content") or "")
                if len(content) > _LIVE_LLM_MESSAGE_CAP:
                    content = content[:_LIVE_LLM_MESSAGE_CAP] + "…"
                trimmed_msgs.append({"role": str(msg.get("role") or "user"), "content": content})
            row["messages"] = trimmed_msgs
            out = row["output"]
            if len(out) > _LIVE_LLM_OUTPUT_CAP:
                row["output"] = "…" + out[-_LIVE_LLM_OUTPUT_CAP:]
        compacted.append(row)
    return compacted


class ModuleSyncProgressReporter(ProgressReporter):
    """Sync pipeline progress to module state for live UI polling."""

    def __init__(self, job_key: str) -> None:
        super().__init__()
        self._job_key = job_key
        self._last_io_sync = 0.0
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
                "llm_io": compact_llm_io_for_live(self.llm_io_snapshot()),
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
        now = time.monotonic()
        if now - self._last_io_sync >= _CHUNK_SYNC_INTERVAL_S:
            self._last_io_sync = now
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
    if isinstance(exc, ModuleNotFoundError):
        missing = str(getattr(exc, "name", "") or exc).strip()
        if missing in ("tvDatafeed", "tvdatafeed"):
            return (
                "缺少 TradingView 数据依赖 tvDatafeed（PyPI 包名 tvdatafeed-enhanced）。"
                "请在项目目录执行：python -m pip install -r requirements.txt，"
                "再用 python run_app.py 重启（勿用裸 streamlit run）。"
            )
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
            from src.run.archive.store import archive_failure_run
            from src.run.pipeline_run import get_current_run_id, set_current_run_id

            reporter = ModuleSyncProgressReporter(job_key)
            cfg_token = set_run_config(run_config.normalized())
            prog_token = set_progress(reporter)
            active = access_job(job_key)
            t0 = time.perf_counter()
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
                run_id = get_current_run_id()
                if run_id:
                    try:
                        archive_failure_run(
                            run_id,
                            format_generation_error(exc),
                            run_config=run_config.normalized(),
                            elapsed_s=time.perf_counter() - t0,
                        )
                    except Exception:
                        log.exception("partial archive failed run_id=%s", run_id)
                if active is not None:
                    active.error = exc
            finally:
                reset_progress(prog_token)
                reset_run_config(cfg_token)
                set_current_run_id(None)

        thread = threading.Thread(target=worker, daemon=True, name=f"report-gen-{job_key[:8]}")
        job.thread = thread
        thread.start()
