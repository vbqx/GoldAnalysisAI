"""Single constrained LLM pass for Advice V2 wording."""

from __future__ import annotations

import json
import re
from dataclasses import replace
from typing import Any

from src.advice.audit import audit_advice
from src.advice.types import AdvicePacket
from src.llm.stage import run_llm_stage
from src.core.types import LLMStageTrace
from src.llm.router import client_for_stage, llm_configured

SYSTEM = """你是 XAUUSD 交易建议编辑器，不是交易执行者。
系统已用确定性规则给出方向、关注区、失效位、目标和证据。你只能改善中文解释，严禁：
1. 修改 decision、bias、confidence、方向或任何数值；
2. 新增价格、概率、胜率、仓位或未经输入支持的事实；
3. 同时推荐相反方向；
4. 使用“必涨、必跌、最佳、确定”等承诺性措辞。
输出 JSON：
{
  "summary": "一句当前建议",
  "market_context": ["事实1", "事实2", "事实3"],
  "rationale": ["理由1", "理由2", "理由3"],
  "confirmation_checklist": ["人工确认1", "人工确认2", "人工确认3"],
  "risks": ["风险1"],
  "uncertainties": ["不确定性1"]
}
若 primary_setup 为 null，rationale 与 confirmation_checklist 必须返回空数组。"""


def _strings(value: Any, *, limit: int, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    rows = [str(item).strip() for item in value if str(item).strip()]
    if len(rows) > limit:
        raise ValueError(f"{field} exceeds {limit} items")
    return rows


def _parse(data: dict[str, Any], *, has_setup: bool) -> dict[str, Any]:
    summary = str(data.get("summary") or "").strip()
    if not summary:
        raise ValueError("summary is required")
    parsed = {
        "summary": summary,
        "market_context": _strings(data.get("market_context"), limit=4, field="market_context"),
        "rationale": _strings(data.get("rationale"), limit=4, field="rationale"),
        "confirmation_checklist": _strings(
            data.get("confirmation_checklist"), limit=4, field="confirmation_checklist"
        ),
        "risks": _strings(data.get("risks"), limit=4, field="risks"),
        "uncertainties": _strings(data.get("uncertainties"), limit=4, field="uncertainties"),
    }
    if has_setup and (not parsed["rationale"] or not parsed["confirmation_checklist"]):
        raise ValueError("setup wording requires rationale and confirmation_checklist")
    if not has_setup and (parsed["rationale"] or parsed["confirmation_checklist"]):
        raise ValueError("no-setup wording must not invent a setup")
    return parsed


def _allowed_prices(packet: AdvicePacket) -> list[float]:
    values = [packet.current_price]
    setup = packet.primary_setup
    if setup:
        values.extend(
            [
                setup.attention_zone.low,
                setup.attention_zone.high,
                setup.invalidation_level,
                *setup.targets,
            ]
        )
    return values


def _assert_no_new_prices(payload: dict[str, Any], allowed: list[float]) -> None:
    text = json.dumps(payload, ensure_ascii=False)
    # Small integers are timeframe/checklist language. Price-like numbers must be whitelisted.
    numbers = [float(raw.replace(",", "")) for raw in re.findall(r"(?<!\w)(\d[\d,]*(?:\.\d+)?)(?!\w)", text)]
    invented = [value for value in numbers if value >= 100 and not any(abs(value - ref) <= 0.51 for ref in allowed)]
    if invented:
        raise ValueError("LLM wording introduced unapproved prices: " + ", ".join(f"{x:g}" for x in invented[:5]))


def enhance_advice(packet: AdvicePacket) -> tuple[AdvicePacket, LLMStageTrace | None]:
    """Improve prose while preserving the deterministic decision contract."""
    if not llm_configured():
        return packet, None
    client = client_for_stage("advisor")
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": "请仅编辑以下建议的文字字段：\n"
            + json.dumps(packet.to_dict(), ensure_ascii=False, indent=2),
        },
    ]
    result, trace = run_llm_stage(
        stage="advisor",
        model=client.model,
        client=client,
        messages=messages,
        parse=lambda data: _parse(data, has_setup=packet.primary_setup is not None),
        temperature=0.1,
    )
    if result is None:
        return packet, trace
    _assert_no_new_prices(result, _allowed_prices(packet))
    setup = packet.primary_setup
    if setup:
        setup = replace(
            setup,
            rationale=result["rationale"],
            confirmation_checklist=result["confirmation_checklist"],
        )
    enhanced = replace(
        packet,
        summary=result["summary"],
        market_context=result["market_context"] or packet.market_context,
        risks=result["risks"],
        uncertainties=result["uncertainties"],
        primary_setup=setup,
    )
    audit = audit_advice(enhanced)
    if not audit.passed:
        raise ValueError("LLM wording caused advice audit failure: " + "; ".join(audit.violations))
    return replace(enhanced, audit=audit), trace
