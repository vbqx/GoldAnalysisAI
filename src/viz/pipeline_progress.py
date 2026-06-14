"""Streamlit UI for pipeline step progress and live LLM I/O."""

from __future__ import annotations

import streamlit as st

from src.core.progress import PipelineProgressStep, ProgressReporter, StepStatus
from src.llm.format_io import format_llm_output, format_messages
from src.llm.narrative_output import format_llm_narrative
from src.viz.llm_meta import format_latency_ms

_STATUS_ICONS: dict[StepStatus, str] = {
    "pending": "⏳",
    "running": "🔄",
    "done": "✅",
    "error": "❌",
    "skipped": "⏭️",
}


def _format_step(step: PipelineProgressStep) -> str:
    icon = _STATUS_ICONS.get(step.status, "•")
    detail = f" — {step.detail}" if step.detail else ""
    timing = ""
    if step.elapsed_ms is not None and step.status in ("done", "error"):
        if step.elapsed_ms >= 1000:
            timing = f" ({step.elapsed_ms / 1000:.1f}s)"
        else:
            timing = f" ({step.elapsed_ms}ms)"
    weight = "**" if step.status == "running" else ""
    end_weight = "**" if step.status == "running" else ""
    return f"{icon} {weight}{step.label}{end_weight}{detail}{timing}"


def render_progress_steps(steps: list[dict], *, title: str = "生成步骤") -> None:
    if not steps:
        return
    if title:
        st.markdown(f'<p class="section-h">{title}</p>', unsafe_allow_html=True)
    for raw in steps:
        step = PipelineProgressStep(
            id=raw.get("id", ""),
            label=raw.get("label", ""),
            status=raw.get("status", "done"),
            detail=raw.get("detail", ""),
            elapsed_ms=raw.get("elapsed_ms"),
        )
        st.markdown(_format_step(step))


def _render_llm_output_panel(*, stage: str, output: str, error: str | None = None, json_height: int = 220) -> None:
    if error:
        st.error(error)
        return
    raw = output or ""
    st.caption("原始输出（JSON）")
    st.text_area(
        f"llm_out_{stage}",
        format_llm_output(raw)[:16000] + ("…" if len(raw) > 16000 else ""),
        height=json_height,
        disabled=True,
        label_visibility="collapsed",
    )
    st.caption("整理摘要")
    st.markdown(format_llm_narrative(stage, raw), unsafe_allow_html=True)


def render_llm_io_history(
    records: list[dict], *, title: str = "智能体 I/O", expand_last: bool = False
) -> None:
    """Full-width LLM call history."""
    if not records:
        if title:
            st.caption("暂无 LLM 调用记录")
        return
    if title:
        st.markdown(f'<p class="section-h">{title}</p>', unsafe_allow_html=True)
    for i, rec in enumerate(records):
        is_rule = rec.get("kind") == "rule" or rec.get("model") == "规则引擎"
        status = "❌" if rec.get("error") else ("📋" if is_rule else "✅")
        timing = ""
        if rec.get("latency_ms"):
            timing = f" · {format_latency_ms(rec['latency_ms'])}"
        stage = rec.get("stage", str(i))
        model = rec.get("model", "")
        with st.expander(
            f"{status} {rec.get('label', stage)} · `{model}`{timing}",
            expanded=(i == len(records) - 1) if expand_last else (i == 0 and stage == "analyst_team"),
        ):
            in_col, out_col = st.columns(2)
            with in_col:
                st.markdown("**输入**" if is_rule else "**输入（Prompt）**")
                msgs = rec.get("messages") or []
                st.text_area(
                    f"llm_in_{stage}",
                    format_messages(msgs),
                    height=280,
                    disabled=True,
                    label_visibility="collapsed",
                )
            with out_col:
                st.markdown("**输出**" if is_rule else "**输出（JSON）**")
                if rec.get("error"):
                    st.error(rec["error"])
                else:
                    raw = rec.get("output") or ""
                    st.text_area(
                        f"llm_out_{stage}",
                        format_llm_output(raw)[:16000] + ("…" if len(raw) > 16000 else ""),
                        height=280,
                        disabled=True,
                        label_visibility="collapsed",
                    )
            if not rec.get("error"):
                st.markdown("**整理摘要**")
                st.markdown(
                    format_llm_narrative(stage, rec.get("output") or ""),
                    unsafe_allow_html=True,
                )


class StreamlitProgressReporter(ProgressReporter):
    """Renders pipeline steps + live streaming LLM I/O."""

    def __init__(self, *, progress_slot=None, llm_slot=None) -> None:
        super().__init__()
        self._slot = progress_slot or st.empty()
        self._llm_panel = llm_slot
        self._llm_blocks: dict[str, dict] = {}
        self._llm_header_shown = False
        self._paint("正在初始化报告生成…")

    def _paint(self, headline: str) -> None:
        lines = [_format_step(s) for s in self.state.steps]
        body = "\n\n".join(lines) if lines else "_首次加载约需 2–3 分钟（含数据拉取与 LLM 推理）_"
        self._slot.info(f"**{headline}**\n\n{body}")

    def _on_change(self) -> None:
        running = next((s for s in reversed(self.state.steps) if s.status == "running"), None)
        if running:
            headline = f"正在：{running.label}"
            if running.detail:
                headline = f"{headline} — {running.detail}"
        elif self.state.steps:
            headline = "报告生成完成"
        else:
            headline = "正在生成报告…"
        self._paint(headline)

    def _on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str) -> None:
        if self._llm_panel is None:
            return
        with self._llm_panel:
            if not self._llm_header_shown:
                st.markdown("#### 🤖 LLM 实时调用")
                self._llm_header_shown = True
            expander = st.expander(f"🔄 {label} · `{model}`", expanded=True)
            expander.caption("输入（Prompt）")
            expander.text_area(
                f"llm_in_{stage}",
                format_messages(messages),
                height=200,
                disabled=True,
                label_visibility="collapsed",
            )
            expander.caption("输出（流式）")
            output_box = expander.empty()
            output_box.markdown("_等待模型响应…_")
            self._llm_blocks[stage] = {"expander": expander, "output_box": output_box, "buffer": ""}

    def run_llm_stream(self, stage: str, chunk_iter) -> str:
        block = self._llm_blocks.get(stage)
        if not block or self._llm_panel is None:
            return super().run_llm_stream(stage, chunk_iter)

        def _gen():
            for chunk in chunk_iter:
                block["buffer"] += chunk
                yield chunk

        with block["expander"]:
            full = st.write_stream(_gen())
        return full or block["buffer"]

    def _on_llm_end(self, stage: str, output: str, *, error: str | None = None) -> None:
        block = self._llm_blocks.get(stage)
        if not block:
            return
        rec = self._find_llm(stage)
        label = rec.label if rec else stage
        model = rec.model if rec else ""
        timing = ""
        if rec and rec.latency_ms:
            timing = f" · {format_latency_ms(rec.latency_ms)}"
        icon = "❌" if error else "✅"
        block["expander"].markdown(f"**{icon} {label}** · `{model}`{timing}")
        if error:
            block["output_box"].error(error)
        elif output:
            with block["output_box"].container():
                _render_llm_output_panel(stage=stage, output=output, json_height=180)

    def complete(self, *, ok: bool = True) -> None:
        if not self.state.steps:
            self._slot.success("已加载缓存报告")
            return
        if ok:
            self._slot.success("**报告生成完成**")
        else:
            failed = next((s for s in reversed(self.state.steps) if s.status == "error"), None)
            detail = f" — {failed.detail}" if failed and failed.detail else ""
            self._paint(f"报告生成失败{detail}")
            self._slot.error("报告生成失败，请查看上方步骤或点击侧边栏「刷新报告」重试")
