# Current Status

本文是 owner 视角的当前状态，不记录历史流水账。历史金融评审和实跑快照在 `docs/reviews/`（见 [findings-status.md](../reviews/findings-status.md)）。

## 已具备

- 规则版分析链路已贯通：数据拉取、指标、ICT/PA、Analyst Team、研究、辩论、交易、风控、经理、报告。
- LLM 双轨已覆盖 Analyst Team、研究、辩论、点位、交易员、风控、经理和报告文案。
- Streamlit UI 已支持生成前配置、实时进度、外部数据页、短线策略页、LLM 决策链审计。
- 回测基础设施已有规则 baseline、历史 DXY overlay 和指标统计。
- MT5 账号连接边界已存在，但仅用于账号/执行通道；模拟下单尚未启用。

## 主要风险

- 完整 LLM 历史回放还没成为默认回测路径，当前 backtest 不能被解读为最终 LLM 实盘表现。
- 文档刚完成信息架构重组，后续迭代需要持续维护链接和权威边界。
- 外部数据源和 TradingView WebSocket 会受网络影响，集成测试可能慢或波动。
- 执行层尚未实现 `order_check`、模拟下单、熔断和回执审计。

## 推荐近期顺序

1. 完成文档和测试体系重构。
2. 评审架构边界，识别可合并/可延后的模块。
3. 实现 shadow mode，让实时决策先不下单只记录。
4. 实现 MT5 `order_check`，再进入模拟账户小手数下单。
5. 扩展完整 LLM historical replay，区分规则 baseline 和 LLM 决策表现。
