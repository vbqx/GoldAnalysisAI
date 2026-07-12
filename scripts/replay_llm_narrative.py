#!/usr/bin/env python3
"""Replay saved LLM narrative JSON against report validators (zero API tokens)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis.narrative_sections import SECTION_KEYS, build_rule_narrative_sections
from src.llm.analyst import apply_llm_to_report, validate_llm_payload


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_llm_payload(report: dict, llm_path: Path | None) -> dict:
    if llm_path is not None:
        payload = _load_json(llm_path)
        if isinstance(payload, dict) and "narrative_sections" in payload:
            return payload
        raise SystemExit(f"{llm_path} 不是有效的 LLM narrative JSON")
    llm = report.get("llm_analysis") or {}
    raw = llm.get("raw_response")
    if not raw:
        raise SystemExit(
            "报告里没有 llm_analysis.raw_response。请用 --llm 指定一次真实跑出来的 JSON。"
        )
    return json.loads(raw)


def _print_audit(result) -> None:
    print("\n=== narrative_sections ===")
    for key in SECTION_KEYS:
        audit = (result.narrative_section_audit or {}).get(key) or {}
        section = (result.narrative_sections or {}).get(key) or {}
        source = section.get("source", "?")
        accepted = audit.get("accepted", source == "llm")
        reason = audit.get("fallback_reason") or "—"
        print(f"  {key:16} source={source:8} accepted={accepted}  {reason}")

    print("\n=== top_level ===")
    top = result.top_level_audit or {}
    print(f"  accepted={top.get('accepted', True)}  reason={top.get('fallback_reason') or '—'}")
    for field, reason in (top.get("field_audit") or {}).items():
        if reason:
            print(f"    {field}: {reason}")

    llm_blocks = sum(
        1 for key in SECTION_KEYS if (result.narrative_sections or {}).get(key, {}).get("source") == "llm"
    )
    print(f"\nSUMMARY llm_sections={llm_blocks}/{len(SECTION_KEYS)} top_level_accepted={top.get('accepted', True)}")
    if result.market_summary:
        print(f"  market_summary: {len(result.market_summary)} 字")
    if result.trade_thesis:
        print(f"  trade_thesis:   {len(result.trade_thesis)} 字")
    if result.action_plan:
        print(f"  action_plan:    {len(result.action_plan)} 字")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "tests/fixtures/replay_min_report.json",
        help="报告 JSON（默认 tests/fixtures/replay_min_report.json）",
    )
    parser.add_argument(
        "--llm",
        type=Path,
        default=None,
        help="LLM 返回 JSON；省略则从 report.llm_analysis.raw_response 读取",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="把校验结果写回 report 的 narrative_sections / llm_analysis（仅 stdout 摘要）",
    )
    args = parser.parse_args()

    report = _load_json(args.report)
    if not report.get("narrative_sections"):
        report["narrative_sections"] = build_rule_narrative_sections(report)

    payload = _load_llm_payload(report, args.llm)
    result = validate_llm_payload(payload, report)
    _print_audit(result)

    if args.apply:
        apply_llm_to_report(report, result)
        print("\n已写入 report 内存副本（未保存文件）。可用 --apply 配合自行 dump。")


if __name__ == "__main__":
    main()
