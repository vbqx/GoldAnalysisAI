"""Pipeline progress reporting — contextvar + noop for non-UI callers."""

from __future__ import annotations

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

    def set_external_snapshot(self, data: dict[str, Any]) -> None:
        self.external_snapshot = data
        self._on_change()

    def start(self, step_id: str, label: str, detail: str = "") -> None:
        self._finish_running()
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

    def llm_begin(self, stage: str, model: str, messages: list[dict[str, str]]) -> None:
        label = STAGE_LABELS.get(stage, stage)
        existing = self._find_llm(stage)
        if existing is not None and not existing.output and existing.error is None:
            existing.model = model
            existing.messages = list(messages)
            existing.latency_ms = None
        else:
            self.llm_io.append(LLMIORecord(stage=stage, label=label, model=model, messages=messages))
        self._on_llm_begin(stage, model, messages, label)

    def run_llm_stream(self, stage: str, chunk_iter) -> str:
        """Consume streamed chunks; Streamlit subclass uses st.write_stream."""
        parts: list[str] = []
        for chunk in chunk_iter:
            parts.append(chunk)
            self._on_llm_chunk(stage, chunk)
        return "".join(parts)

    def llm_end(self, stage: str, output: str, *, error: str | None = None, latency_ms: int | None = None) -> None:
        rec = self._find_llm(stage)
        if rec:
            rec.output = output
            rec.error = error
            rec.latency_ms = latency_ms
        self._on_llm_end(stage, output, error=error)

    def _find_llm(self, stage: str) -> LLMIORecord | None:
        for rec in reversed(self.llm_io):
            if rec.stage == stage:
                return rec
        return None

    def _on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str) -> None:
        pass

    def _on_llm_chunk(self, stage: str, chunk: str) -> None:
        pass

    def _on_llm_end(self, stage: str, output: str, *, error: str | None = None) -> None:
        pass

    def _find(self, step_id: str) -> PipelineProgressStep | None:
        for step in reversed(self.state.steps):
            if step.id == step_id:
                return step
        return None

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
