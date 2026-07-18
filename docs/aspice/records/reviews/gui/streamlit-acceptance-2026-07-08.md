# GUI 验收快照：2026-07-08

**状态**：✅ 已完成

本文件保存 2026-07-08 的 Streamlit GUI 验收记录。当前 UI 事实以 `src/viz/`、[docs/operations/walkthrough.md](../../../../operations/walkthrough.md) 和 [docs/aspice/governance/verification-strategy.md](../../../governance/verification-strategy.md) 为准。

索引：[review-index.md](../review-index.md) · [findings-status.md](../findings-status.md)

## 已执行

1. 网络恢复后重跑真实数据链路：Streamlit `localhost:8501` 可访问，成功生成 XAUUSD 报告，时间戳为 `2026-07-08 23:31 (UTC+8)`。
2. 逐页桌面宽度 `1440x1200` 与移动宽度 `390x900` 检查：首页、外部数据、短线策略、LLM 决策链均非空白页，无 Streamlit 异常、无横向溢出、无关键组件越界。
3. 首页检查：`decision-summary`、`primary-plan-focus`、备选计划卡正常渲染；主计划不再在焦点卡和下方列表重复展示。
4. 外部数据页检查：`external-feed` 正常渲染，新闻、财经日历、DXY、社媒/TradingView 二次加工摘要在同一审计区内展示。
5. 短线策略页检查：`decision-summary`、`primary-plan-focus`、`strategy-layout-anchor`、价位阶梯正常渲染；移动端按单列顺序收敛。
6. LLM 决策链页检查：`agent-stage-summary` 正常渲染，阶段摘要优先展示，生成 I/O 与完整 JSON 保持在审计层。
7. 代码级检查：`src/viz` 相关模块 `py_compile` 通过；样例 report 组件审计通过。

## 残余说明

真实链路耗时受 TradingView、外部新闻源与 LLM 响应影响；该轮第二次完整回归耗时较长，但最终成功进入报告态并完成四页 GUI 验收。
