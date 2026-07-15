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

# Injected into every trading-relevant LLM stage + JSON payloads.
INTRADAY_GOLD_MANDATE = (
    "交易对象与风格：XAUUSD 黄金日内交易（非波段/多日持仓为主）。"
    "层级：4H/1H（辅以当日 session 量价）定方向与趋势偏见；"
    "主路径：仅在 15m 或 5m 寻找**顺该偏见**的日内入场区（回踩/承压/扫过收回确认后再挂）。"
    "潜在反转：必须单独识别，不得装作没有——"
    "（1）标出高周期失效位与关键 CHoCH/扫过 VA 外侧等反转条件；"
    "（2）未触发前反转只作观察/对冲预案（path C 或观望），不得升格为主方向；"
    "（3）仅当 15m/5m 出现明确反转确认（如关键位假突破回收失败、结构 CHoCH 且价格站到 VA 外侧）"
    "才允许把反向方案写为备选执行，并写清触发与失效。"
    "禁止用 4H/1H 价位直接当市价入场；禁止把多日波段方案写成主交易计划。"
)

# Unified PA/SMC hierarchy — keep in sync with narrative_combine.COMBINATION_RULES.
PA_SMC_PRIORITY = f"""{INTRADAY_GOLD_MANDATE}

PA 与 SMC 主次（按场景，不得混用）：
1) 报告五块叙事 market_overview/liquidity/4h/1h/15m：PA 为主（POC/VAH/VAL、量价 S/R、价值区区位写主干）；SMC 为辅（仅引用 allowed_levels 中的结构价，不写 BOS/CHoCH/OB/FVG 进主干句）。
2) 交易计划 action_plan/watch_levels：高周期定方向后，用 15m/5m PA 定入场/止损/目标区；SMC 仅后台过滤，不进文案。
3) 多空研究/技术 Analyst：SMC（4H/1H）定结构方向；PA 作确认；入场相关证据优先标 15m/5m。
4) 共振：SMC 区间与 PA 价位相距 ≤8 点时须分别点明来源，不得合并为一个指标名。"""

# Embedded once per price_action_summary payload (keep short).
PA_SUMMARY_HINT: list[str] = [
    "黄金日内：4H/1H 定方向；15m/5m 顺势入场；潜在反转单独标失效位，确认前不作主方案",
    "各周期 Fixed-360 POC 不可混用；lookback_bars / profile_source=ltf_5m|native_tf",
    "nearest_support/resistance=近端量价S/R；不得编造 JSON 未出现的价格或结构",
]

ANALYST_PRIORITY_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "结构判断以 SMC（timeframes/lux_timeframe_panels）为主，先读 4H/1H 定偏见；"
    "PA（price_action_summary）为辅确认价位与共振；"
    "level_reactions：至少 1 条顺势日内锚点（15m/5m），"
    "并至少 1 条潜在反转/失效相关锚点（如 VAL/VAH 外侧、关键阻力失守后预期）并写清触发条件；"
    "引用 POC/VA 必须带周期（禁止混用）。"
)

NARRATIVE_PRIORITY_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "叙事五块以 PA 为主；4H/1H 写背景方向，15m 写执行前景；"
    "market_overview/conditions 须点到潜在反转或失效观察（无则写暂无）；"
    "SMC 仅 allowed_levels 引用，不写 BOS/CHoCH/OB 主干。"
)

RESEARCH_PRIORITY_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "以 analyst_team 结论提取同向 evidence；"
    "方向论据优先 4H/1H；入场相关论据优先 15m/5m；"
    "对手方向须提炼「潜在反转触发条件」证据（可保留但不得压过未失效的主偏见）。"
    "structure_vote / event_risk 仅作交叉校验，不得绕过 analyst。"
)

TRADER_PRIORITY_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "依据 debate 共识选方向（应已体现高周期偏见）；"
    "candidate_signals 的入场几何应是 15m/5m 日内区，不得另造 4H 级别市价追单。"
    "只选 payload 中存在的 signal_index。"
)

DEBATE_PRIORITY_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "综合多空证据时先对齐高周期方向与主路径执行条件；"
    "discussion_notes 必须点明潜在反转触发条件（或写「暂无明确反转触发」）；"
    "未触发前共识仍跟主偏见，不得因少数反向证据直接翻盘；"
    "不得引入 payload 外的新闻或价位。"
)

LEVELS_PRIORITY_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "定区以 PA 为主；入场/止损/止盈几何必须落在 15m 或 5m（含 session 共振时可注明）；"
    "4H/1H 仅作方向与失效背景，不得把大周期区间直接当入口。"
    "A=顺偏见主路径；B=同向备选/更优回踩；"
    "C=潜在反转或主路径失效后的对冲预案（须写清触发条件，未触发不可当主单）。"
    "setup_type 优先 llm_poc_va|llm_volume_sr；"
    "绑定 technical.level_reactions：一句 deduction，禁止长文重写技术分析。"
)

RISK_MANAGER_HINT = (
    f"{INTRADAY_GOLD_MANDATE} "
    "只审核交易员提案与已批准 signal_index；"
    "若方案把 4H/1H 大区间当日内市价追单，应降级或否决。"
)
