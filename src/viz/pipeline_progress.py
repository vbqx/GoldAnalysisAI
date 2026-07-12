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


def pipeline_progress_headline(steps: list[dict] | None) -> str:
    """Human-readable summary of the current pipeline step for waiting UI."""
    rows = steps or []
    running = [s for s in rows if s.get("status") == "running"]
    if running:
        parts: list[str] = []
        for step in running:
            label = str(step.get("label") or step.get("id") or "处理中")
            detail = str(step.get("detail") or "").strip()
            parts.append(f"{label} — {detail}" if detail else label)
        return " · ".join(parts)
    if rows:
        last = rows[-1]
        status = last.get("status")
        label = str(last.get("label") or last.get("id") or "")
        if status == "done" and label:
            return f"最新完成：{label}；后续阶段继续运行中…"
        if status == "error" and label:
            detail = str(last.get("detail") or "").strip()
            return f"阶段失败：{label}" + (f" — {detail}" if detail else "")
    return "流水线启动中…"


def _format_step(step: PipelineProgressStep) -> str:
    icon = _STATUS_ICONS.get(step.status, "•")
    detail = f" — {step.detail}" if step.detail else ""
    timing = ""
    if step.elapsed_ms is not None and step.status in ("done", "error"):
        if step.elapsed_ms >= 1000:
            timing = f" ({step.elapsed_ms / 1000:.1f}s)"
        elif step.elapsed_ms == 0:
            timing = " (<1ms)"
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


def _render_llm_io_text(*, label: str, key: str, text: str, height: int = 360) -> None:
    if label:
        st.markdown(f'<p class="io-label">{label}</p>', unsafe_allow_html=True)
    st.text_area(
        label or key,
        value=text,
        height=height,
        disabled=True,
        label_visibility="collapsed",
        key=key,
    )


def _render_llm_output_panel(
    *,
    stage: str,
    output: str,
    error: str | None = None,
    json_height: int = 320,
    widget_key: str | None = None,
) -> None:
    if error:
        st.error(error)
        return
    raw = output or ""
    out_key = widget_key or f"llm_out_{stage}"
    st.caption("原始输出（JSON）")
    _render_llm_io_text(
        label="",
        key=out_key,
        text=format_llm_output(raw)[:16000] + ("…" if len(raw) > 16000 else ""),
        height=json_height,
    )
    st.caption("整理摘要")
    st.markdown(format_llm_narrative(stage, raw), unsafe_allow_html=True)


def is_streaming_llm_record(rec: dict) -> bool:
    """True while an LLM call is in flight (begin → end, including partial output)."""
    if rec.get("kind") == "rule" or rec.get("model") == "规则引擎":
        return False
    if rec.get("error"):
        return False
    return rec.get("latency_ms") is None


def partition_llm_records_for_live(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split in-flight LLM records from completed ones for the live generation panel."""
    filtered = _filter_llm_io_records(records)
    active = [r for r in filtered if is_streaming_llm_record(r)]
    completed = [r for r in filtered if not is_streaming_llm_record(r)]
    return active, completed


def render_live_llm_status_lightweight(live: dict) -> None:
    """Minimal LLM status for waiting UI — no text_area widgets (prevents Streamlit blank-screen)."""
    records = live.get("llm_io") or []
    if not records:
        return
    active, completed = partition_llm_records_for_live(records)
    if not active and not completed:
        return
    st.markdown('<p class="section-h">LLM 状态</p>', unsafe_allow_html=True)
    for rec in active:
        label = rec.get("label") or rec.get("stage") or "LLM"
        model = rec.get("model") or "—"
        chars = rec.get("stream_chars")
        if chars is None:
            chars = len(str(rec.get("output") or ""))
        st.markdown(f"- 🔄 **{label}** · `{model}` · 已输出 {chars} 字符")
    if completed:
        st.caption(f"已完成 {len(completed)} 个阶段；完整 Prompt / JSON 见生成完成后的「LLM 决策链」。")


def render_live_llm_streams(active: list[dict]) -> None:
    """Prominent streaming panel fed by background-thread chunk snapshots."""
    if not active:
        return
    st.markdown('<p class="section-h">🤖 LLM 实时推理</p>', unsafe_allow_html=True)
    for idx, rec in enumerate(active):
        stage = rec.get("stage", "")
        label = rec.get("label", stage)
        model = rec.get("model", "")
        output = rec.get("output") or ""
        st.markdown(f"**🔄 {label}** · `{model}`")
        with st.container(border=True):
            msgs = rec.get("messages") or []
            st.caption("输入（Prompt）")
            _render_llm_io_text(
                label="",
                key=f"live_{idx}_in_{stage}",
                text=format_messages(msgs),
                height=200,
            )
            char_note = f" · {len(output)} 字符" if output else ""
            st.caption(f"输出（流式）{char_note}")
            if output:
                preview = format_llm_output(output)
                if len(preview) > 12000:
                    preview = "…\n" + preview[-12000:]
                _render_llm_io_text(
                    label="",
                    key=f"live_{idx}_out_{stage}",
                    text=preview,
                    height=280,
                )
            else:
                st.markdown("_等待模型响应…_")


def _filter_llm_io_records(records: list[dict]) -> list[dict]:
    has_llm_analyst = any(
        r.get("stage") in ("technical", "fundamentals", "news", "sentiment")
        and r.get("kind") != "rule"
        and r.get("model") != "规则引擎"
        for r in records
    )
    if not has_llm_analyst:
        return records
    return [
        r
        for r in records
        if not (
            r.get("stage") == "analyst_team"
            and (r.get("kind") == "rule" or r.get("model") == "规则引擎")
        )
    ]


def render_llm_io_history(
    records: list[dict], *, title: str = "智能体 I/O", expand_last: bool = False
) -> None:
    """Full-width LLM call history."""
    records = _filter_llm_io_records(records)
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
            expanded=(i == len(records) - 1) if expand_last else (i == 0),
        ):
            input_label = "输入" if is_rule else "输入（Prompt）"
            output_label = "输出" if is_rule else "输出（JSON）"
            msgs = rec.get("messages") or []
            _render_llm_io_text(
                label=input_label,
                key=f"io_{i}_in_{stage}",
                text=format_messages(msgs),
                height=360,
            )
            if rec.get("error"):
                st.error(rec["error"])
            else:
                raw = rec.get("output") or ""
                _render_llm_io_text(
                    label=output_label,
                    key=f"io_{i}_out_{stage}",
                    text=format_llm_output(raw)[:16000] + ("…" if len(raw) > 16000 else ""),
                    height=360,
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
                f"prompt_{stage}",
                value=format_messages(messages),
                height=280,
                disabled=True,
                label_visibility="collapsed",
                key=f"reporter_in_{stage}",
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
                _render_llm_output_panel(
                    stage=stage,
                    output=output,
                    json_height=260,
                    widget_key=f"reporter_out_{stage}",
                )

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
