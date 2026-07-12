"""Format archived run configuration for replay / forensic banners."""

from __future__ import annotations

from typing import Any


def format_archived_run_config(run_config: dict[str, Any] | None) -> str:
    cfg = run_config or {}
    mode = cfg.get("agent_mode") or "—"
    narrative = "开" if cfg.get("llm_enabled") else "关"
    stages = []
    for key, label in (
        ("llm_stage_analysts", "分析师"),
        ("llm_stage_bullish", "看多"),
        ("llm_stage_bearish", "看空"),
        ("llm_stage_debate", "辩论"),
        ("llm_stage_levels", "点位"),
        ("llm_stage_trader", "交易员"),
        ("llm_stage_risk", "风控"),
        ("llm_stage_manager", "经理"),
    ):
        if cfg.get(key):
            stages.append(label)
    stage_text = "、".join(stages) if stages else "（无 LLM 阶段）"
    only = str(cfg.get("llm_analyst_only") or "").strip()
    if only:
        stage_text += f" · analyst_only={only}"
    return f"模式 `{mode}` · 报告文案 `{narrative}` · LLM 阶段 {stage_text}"


def pipeline_status_label(status: str | None) -> str:
    mapping = {
        "complete": "已完成",
        "partial": "中断（partial）",
        "failed": "失败（failed）",
    }
    return mapping.get(str(status or "").strip().lower(), status or "—")
