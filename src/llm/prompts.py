"""Prompt templates for XAUUSD institutional analysis."""

from __future__ import annotations

import json
from typing import Any

SYSTEM_PROMPT = """你是专业的 XAUUSD 黄金机构级交易分析师，精通 Price Action、ICT、SMC。
你将收到一份由规则引擎与多智能体流水线生成的结构化 JSON 报告数据。

要求：
1. 仅基于给定数据分析，不要编造未提供的价格或新闻
2. 用中文输出，风格简洁专业，面向交易员
3. 必须返回合法 JSON，字段如下：
{
  "market_summary": "2-4 句市场总览",
  "trade_thesis": "1-3 句主交易逻辑（多空方向与依据）",
  "action_plan": "2-4 条可执行操作建议（含入场区/止损/注意事项）",
  "risks": ["风险1", "风险2", "风险3"],
  "confidence": 0.0到1.0的数值,
  "watch_levels": ["关键价位1", "关键价位2"]
}
4. action_plan 为字符串，多条建议用换行分隔
5. 不构成投资建议免责声明可省略（报告页已有）"""


def build_messages(context: dict[str, Any]) -> list[dict[str, str]]:
    user_content = (
        "请根据以下 XAUUSD 结构化分析数据，生成机构级文字结论（JSON）：\n\n"
        f"{json.dumps(context, ensure_ascii=False, indent=2)}"
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
