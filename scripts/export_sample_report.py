#!/usr/bin/env python3
"""Export a deterministic, non-live Advice V2 sample report."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/aspice/SWE.3-detailed-design/reference/examples/sample-report.json"
UPDATED_AT = "2026-08-12 12:00 (UTC+8)"


def build_sample() -> dict:
    return {
        "artifact_kind": "human_review_advice",
        "artifact_version": 2,
        "meta": {
            "title": "XAUUSD 人工审核交易建议（脱敏样例）",
            "updated_at": UPDATED_AT,
            "sample": True,
            "methodology": "结构事实 + 确定性审计 + 人工确认",
            "data_source": "fixture:XAUUSD",
            "run_archive_id": "sample-advice-v2",
            "run_config": {"generation_mode": "rule", "llm_enabled": False, "replay_mode": False, "replay_run_id": ""},
            "run_config_fingerprint": "sample0000000000",
            "data_as_of": {"executable": True, "warnings": []},
            "observation_mode": True,
            "advice_source": "rule",
            "advisor_trace": None,
            "generation_steps": [],
            "llm_io": [],
        },
        "metrics": {
            "current_price": 4386.97,
            "daily_high": 4403.20,
            "daily_low": 4358.10,
            "daily_change_pct": 0.42,
        },
        "advice": {
            "decision": "WATCH_LONG",
            "bias": "bullish",
            "confidence": "medium",
            "horizon": "未来 2–8 小时",
            "summary": "高周期结构偏多，等待价格回到 4367.68–4376.64 后由人工确认，不追价。",
            "current_price": 4386.97,
            "primary_setup": {
                "direction": "BUY",
                "attention_zone": {"low": 4367.68, "high": 4376.64, "label": "15m 支撑 · 1h FVG"},
                "current_state": "价格尚未进入关注区，不建议追价",
                "rationale": ["4h 与 1h 结构共同偏多", "关注区由不同周期的结构事实共同支持"],
                "confirmation_checklist": ["价格进入关注区", "5m 出现拒绝下跌行为", "5m 形成新的看涨结构转折"],
                "invalidation": "15m 有效跌破 4359.53 后取消做多思路",
                "invalidation_level": 4359.53,
                "targets": [4397.42, 4420.50],
                "evidence_ids": ["level:15m:pa:4371.20:0", "level:1h:ict:4374.80:1"],
                "reward_risk_to_targets": [2.0, 3.83],
            },
            "alternative_scenario": {
                "condition": "15m 收盘跌破 4359.53，反抽不能重新站回",
                "response": "取消首选做多思路；不自动反手，等待新结构后重新评估。",
            },
            "market_context": ["4小时结构偏多", "1小时结构偏多", "15分钟结构震荡"],
            "risks": ["样例不包含实时事件风险，实际确认前必须重新核对日历"],
            "uncertainties": ["建议基于生成时的市场快照"],
            "evidence": [
                {"evidence_id": "structure:4h:trend", "kind": "structure", "statement": "4小时结构偏多", "timeframe": "4h", "source": "ict_pa", "price": None},
                {"evidence_id": "structure:1h:trend", "kind": "structure", "statement": "1小时结构偏多", "timeframe": "1h", "source": "ict_pa", "price": None},
                {"evidence_id": "level:15m:pa:4371.20:0", "kind": "level", "statement": "15m 支撑", "timeframe": "15m", "source": "pa:support", "price": 4371.20},
                {"evidence_id": "level:1h:ict:4374.80:1", "kind": "level", "statement": "1h FVG", "timeframe": "1h", "source": "ict:fvg", "price": 4374.80},
            ],
            "audit": {"passed": True, "violations": [], "warnings": [], "policy_version": "human-advice-v2"},
            "schema_version": "2.0",
        },
        "timeframes": {"4h": {"trend": "bullish"}, "1h": {"trend": "bullish"}, "15m": {"trend": "ranging"}, "5m": {"trend": "ranging"}},
        "levels": {"support": [], "resistance": []},
        "external": {"dxy_impact": "—", "risk_events": "—", "calendar_events": [], "headlines": [], "macro_quotes": [], "sources": [], "fetch_errors": [], "source_policy": "外部数据只作背景与事件风险参考，不直接生成入场价位。"},
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(build_sample(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
