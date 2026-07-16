"""Pipeline progress reporting — contextvar + noop for non-UI callers."""

from __future__ import annotations

import threading
import time
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Literal

StepStatus = Literal["pending", "running", "done", "error", "skipped"]


@dataclass
class PipelineProgressStep:
    id: str
    label: str
    status: StepStatus = "pending"
    detail: str = ""
    elapsed_ms: int | None = None
    started_at: float | None = None


@dataclass
class PipelineProgressState:
    steps: list[PipelineProgressStep] = field(default_factory=list)
    started_at: float = field(default_factory=time.perf_counter)

    def to_dict(self) -> list[dict[str, Any]]:
        return [
            {
                "id": s.id,
                "label": s.label,
                "status": s.status,
                "detail": s.detail,
                "elapsed_ms": s.elapsed_ms,
            }
            for s in self.steps
        ]


@dataclass
class LLMIORecord:
    stage: str
    label: str
    model: str
    messages: list[dict[str, str]]
    output: str = ""
    error: str | None = None
    latency_ms: int | None = None
    kind: Literal["llm", "rule"] = "llm"
    # Issue #37 — auditable routing / budget / retry telemetry
    tier: str = ""
    attempt: int = 0
    attempts: list[dict[str, Any]] = field(default_factory=list)
    input_chars: int | None = None
    input_tokens_est: int | None = None
    output_chars: int | None = None
    output_tokens_est: int | None = None
    usage: dict[str, Any] | None = None
    budget: dict[str, Any] | None = None
    budget_action: str = "none"
    same_model_strategy: bool | None = None
    policy_version: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "label": self.label,
            "model": self.model,
            "messages": self.messages,
            "output": self.output,
            "error": self.error,
            "latency_ms": self.latency_ms,
            "kind": self.kind,
            "tier": self.tier,
            "attempt": self.attempt,
            "attempts": list(self.attempts),
            "input_chars": self.input_chars,
            "input_tokens_est": self.input_tokens_est,
            "output_chars": self.output_chars,
            "output_tokens_est": self.output_tokens_est,
            "usage": self.usage,
            "budget": self.budget,
            "budget_action": self.budget_action,
            "same_model_strategy": self.same_model_strategy,
            "policy_version": self.policy_version,
        }


STAGE_LABELS = {
    "fetch": "数据拉取",
    "context": "数据拉取",
    "analyst_team": "Analyst Team",
    "technical": "技术分析师",
    "fundamentals": "基本面分析师",
    "news": "新闻分析师",
    "sentiment": "情绪分析师",
    "bullish": "看多研究",
    "bearish": "看空研究",
    "debate": "多空辩论",
    "llm_narrative": "报告文案",
}


class ProgressReporter:
    """Records pipeline step transitions; subclasses may render to UI."""

    def __init__(self) -> None:
        self.state = PipelineProgressState()
        self.llm_io: list[LLMIORecord] = []
        self.external_snapshot: dict[str, Any] | None = None
        self._lock = threading.RLock()

    def set_external_snapshot(self, data: dict[str, Any]) -> None:
        self.external_snapshot = data
        self._on_change()

    def start(self, step_id: str, label: str, detail: str = "") -> None:
        self._finish_all_running()
        step = PipelineProgressStep(
            id=step_id, label=label, status="running", detail=detail, started_at=time.perf_counter()
        )
        self.state.steps.append(step)
        self._on_change()

    def start_sibling(self, step_id: str, label: str, detail: str = "") -> None:
        """Mark an additional step running without finishing other running steps."""
        step = PipelineProgressStep(
            id=step_id, label=label, status="running", detail=detail, started_at=time.perf_counter()
        )
        self.state.steps.append(step)
        self._on_change()

    def update(self, step_id: str, *, detail: str | None = None, label: str | None = None) -> None:
        step = self._find(step_id)
        if not step:
            return
        if detail is not None:
            step.detail = detail
        if label is not None:
            step.label = label
        self._on_change()

    def done(self, step_id: str, detail: str = "") -> None:
        step = self._find(step_id)
        if not step:
            return
        step.status = "done"
        if detail:
            step.detail = detail
        step.elapsed_ms = self._elapsed_since_step_start(step)
        self._on_change()

    def fail(self, step_id: str, detail: str = "") -> None:
        step = self._find(step_id)
        if not step:
            return
        step.status = "error"
        step.detail = detail
        step.elapsed_ms = self._elapsed_since_step_start(step)
        self._on_change()

    def skip(self, step_id: str, label: str, detail: str = "") -> None:
        self.state.steps.append(
            PipelineProgressStep(id=step_id, label=label, status="skipped", detail=detail)
        )
        self._on_change()

    def snapshot(self) -> list[dict[str, Any]]:
        return self.state.to_dict()

    def llm_io_snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return [r.to_dict() for r in self.llm_io]

    def stage_io(
        self,
        stage: str,
        *,
        input_text: str,
        output_text: str,
        latency_ms: int | None = None,
        label: str | None = None,
    ) -> None:
        """Record rule-based stage input/output for the generation I/O panel."""
        resolved_label = label or STAGE_LABELS.get(stage, stage)
        with self._lock:
            self.llm_io.append(
                LLMIORecord(
                    stage=stage,
                    label=resolved_label,
                    model="规则引擎",
                    messages=[{"role": "user", "content": input_text}],
                    output=output_text,
                    latency_ms=latency_ms,
                    kind="rule",
                )
            )

    def llm_begin(
        self,
        stage: str,
        model: str,
        messages: list[dict[str, str]],
        *,
        telemetry: dict[str, Any] | None = None,
    ) -> None:
        label = STAGE_LABELS.get(stage, stage)
        tel = telemetry or {}
        with self._lock:
            existing = self._find_llm(stage)
            reuse = bool(tel.get("reuse"))
            open_slot = (
                existing is not None
                and existing.error is None
                and existing.latency_ms is None
            )
            if existing is not None and (reuse or open_slot):
                existing.model = model
                existing.messages = list(messages)
                existing.latency_ms = None
                existing.error = None
                if not tel.get("keep_output"):
                    existing.output = ""
                self._apply_telemetry(existing, tel)
            else:
                self.llm_io.append(self._new_llm_record(stage, label, model, messages, tel))
        self._on_llm_begin(stage, model, messages, label)

    def llm_note_attempt(
        self,
        stage: str,
        *,
        attempt: int,
        reason: str,
        error: str | None = None,
        latency_ms: int | None = None,
    ) -> None:
        with self._lock:
            rec = self._find_llm(stage)
            if not rec:
                return
            rec.attempt = attempt
            rec.attempts.append(
                {
                    "attempt": attempt,
                    "reason": reason,
                    "error": error,
                    "latency_ms": latency_ms,
                }
            )

    def run_llm_stream(self, stage: str, chunk_iter) -> str:
        """Consume streamed chunks; Streamlit subclass uses st.write_stream."""
        parts: list[str] = []
        for chunk in chunk_iter:
            parts.append(chunk)
            self._on_llm_chunk(stage, chunk)
        return "".join(parts)

    def llm_end(
        self,
        stage: str,
        output: str,
        *,
        error: str | None = None,
        latency_ms: int | None = None,
        telemetry: dict[str, Any] | None = None,
    ) -> None:
        with self._lock:
            rec = self._find_llm(stage)
            if rec:
                rec.output = output
                rec.error = error
                rec.latency_ms = latency_ms
                if telemetry:
                    self._apply_telemetry(rec, telemetry)
                    out_est = telemetry.get("output_chars")
                    if out_est is None and output:
                        from src.llm.stage_policy import estimate_text_size

                        size = estimate_text_size(output)
                        rec.output_chars = size["output_chars"]
                        rec.output_tokens_est = size["output_tokens_est"]
        self._on_llm_end(stage, output, error=error)

    def _new_llm_record(
        self,
        stage: str,
        label: str,
        model: str,
        messages: list[dict[str, str]],
        tel: dict[str, Any],
    ) -> LLMIORecord:
        rec = LLMIORecord(stage=stage, label=label, model=model, messages=list(messages))
        self._apply_telemetry(rec, tel)
        return rec

    @staticmethod
    def _apply_telemetry(rec: LLMIORecord, tel: dict[str, Any]) -> None:
        if "tier" in tel and tel["tier"] is not None:
            rec.tier = str(tel["tier"] or "")
        if "attempt" in tel and tel["attempt"] is not None:
            rec.attempt = int(tel["attempt"])
        if "input_chars" in tel:
            rec.input_chars = tel["input_chars"]
        if "input_tokens_est" in tel:
            rec.input_tokens_est = tel["input_tokens_est"]
        if "output_chars" in tel:
            rec.output_chars = tel["output_chars"]
        if "output_tokens_est" in tel:
            rec.output_tokens_est = tel["output_tokens_est"]
        if "usage" in tel:
            rec.usage = tel["usage"]
        if "budget" in tel:
            rec.budget = tel["budget"]
        if "budget_action" in tel and tel["budget_action"] is not None:
            rec.budget_action = str(tel["budget_action"])
        if "same_model_strategy" in tel:
            rec.same_model_strategy = tel["same_model_strategy"]
        if "policy_version" in tel and tel["policy_version"] is not None:
            rec.policy_version = str(tel["policy_version"])

    def _find_llm(self, stage: str) -> LLMIORecord | None:
        for rec in reversed(self.llm_io):
            if rec.stage == stage:
                return rec
        return None

    def _on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str) -> None:
        pass

    def _on_llm_chunk(self, stage: str, chunk: str) -> None:
        with self._lock:
            rec = self._find_llm(stage)
            if rec:
                rec.output += chunk

    def _on_llm_end(self, stage: str, output: str, *, error: str | None = None) -> None:
        pass

    def _find(self, step_id: str) -> PipelineProgressStep | None:
        for step in reversed(self.state.steps):
            if step.id == step_id:
                return step
        return None

    def _finish_all_running(self) -> None:
        for step in self.state.steps:
            if step.status == "running":
                step.status = "done"
                step.elapsed_ms = self._elapsed_since_step_start(step)

    def _finish_running(self) -> None:
        for step in reversed(self.state.steps):
            if step.status == "running":
                step.status = "done"
                step.elapsed_ms = self._elapsed_since_step_start(step)
                break

    def _elapsed_since_step_start(self, step: PipelineProgressStep) -> int | None:
        if step.started_at is None:
            return None
        return int((time.perf_counter() - step.started_at) * 1000)

    def _on_change(self) -> None:
        pass


class NoOpProgressReporter(ProgressReporter):
    pass


_progress_ctx: ContextVar[ProgressReporter | None] = ContextVar("pipeline_progress", default=None)


def get_progress() -> ProgressReporter:
    return _progress_ctx.get() or _NOOP


def set_progress(reporter: ProgressReporter | None):
    return _progress_ctx.set(reporter)


def reset_progress(token) -> None:
    _progress_ctx.reset(token)


_NOOP = NoOpProgressReporter()
