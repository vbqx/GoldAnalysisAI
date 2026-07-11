"""Shared PA/SMC glossary and compact LLM field hints."""

from __future__ import annotations

# One-line glossaries — reused in prompts; details live in payload labels/values.
PA_GLOSSARY = (
    "PA（DGT 量价，辅/确认或叙事主）= POC 成交控制价；VAH/VAL 价值区上下沿；"
    "sr_levels=连续量价/放量/高波动支撑阻力"
)

SMC_GLOSSARY = (
    "SMC（LuxAlgo 结构，主/方向）= 内结构 Internal、摆动 Swing；"
    "OB/FVG 订单块/公允价值缺口；Strong/Weak H/L 强弱高低；BOS/CHoCH 结构突破/特征改变"
)

# Unified PA/SMC hierarchy — keep in sync with narrative_combine.COMBINATION_RULES.
PA_SMC_PRIORITY = """PA 与 SMC 主次（按场景，不得混用）：
1) 报告五块叙事 market_overview/liquidity/4h/1h/15m：PA 为主（POC/VAH/VAL、量价 S/R、价值区区位写主干）；SMC 为辅（仅引用 allowed_levels 中的结构价，不写 BOS/CHoCH/OB/FVG 进主干句）。
2) 交易计划 action_plan/watch_levels：PA 定入场/止损/目标区；SMC 仅后台过滤，不进文案。
3) 多空研究/技术 Analyst：SMC 定结构方向（趋势/BOS/CHoCH/OB/FVG/流动性）；PA 作确认（共振、拒绝、扫过收回）。
4) 共振：SMC 区间与 PA 价位相距 ≤8 点时须分别点明来源，不得合并为一个指标名。"""

# Embedded once per price_action_summary payload (3 lines max).
PA_SUMMARY_HINT: list[str] = [
    "poc/vah/val=价值区控制价与上下沿；nearest_support/resistance=近端量价 S/R",
    "叙事面板以 PA 为主；lux_timeframe_panels/timeframes 供结构确认，不得压过 PA 主干",
    "不得编造 JSON 中未出现的价格、事件或结构",
]

ANALYST_PRIORITY_HINT = (
    "结构判断以 SMC（timeframes/lux_timeframe_panels）为主；"
    "PA（price_action_summary）为辅，用于确认价位与共振。"
)

NARRATIVE_PRIORITY_HINT = (
    "叙事五块以 PA（POC/VAH/VAL、量价 S/R）为主；"
    "SMC 结构价仅作 allowed_levels 引用，4h/1h/15m/liquidity 不写 BOS/CHoCH/OB 主干。"
)

RESEARCH_PRIORITY_HINT = (
    "提取证据时 SMC 定结构方向，PA 量价作确认；"
    "category=structure|liquidity 偏 SMC，可引用 analyst 的 price_action 条目。"
)
