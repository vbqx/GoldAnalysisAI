# Architecture Review

本文从可读性、边界和臃肿度审视当前项目。它不是 roadmap；只记录“现在的结构是否健康”。

## 总体判断

项目功能已经明显超过一个简单 Streamlit 报告工具，当前更接近“研究 + 决策 + 回测 + 执行”的交易实验平台。模块数量偏多，但大多数复杂度来自真实需求：多数据源、LLM 双轨、审计 UI、回测、未来 MT5 执行。主要问题不是代码绝对臃肿，而是边界需要持续保持清楚。

## 分层评审

| 层 | 当前状态 | 判断 |
|----|----------|------|
| 数据层 | TradingView K 线 + 外部新闻/宏观/社媒 | 必须保留；MT5 不应进入行情路径 |
| 指标/结构层 | indicators + ICT/PA 启发式 | 必须保留；后续可独立标准化 ICT interpreter |
| Agent 层 | rule agents + factory 调度 | 必须保留；factory 已是关键边界 |
| LLM 层 | stages + payload + schemas + transport | 必须保留；schema/fallback 是安全边界 |
| 回测层 | replay infra + rule baseline | 必须保留；需扩展 full LLM replay |
| 执行层 | MT5 account bridge | 应延后下单；先做 `order_check` 与 shadow |
| UI 层 | Streamlit report + decision audit | 必须保留；可继续压缩默认视图 |

## 可合并或延后

- `docs/archive/` 中历史审计只保留引用，不参与当前架构判断。
- GitHub issue 批量脚本属于维护工具，可保留但不应出现在 owner 主路径。
- GUI 细节验收应进入测试/归档，不再放 roadmap。
- MT5 order_send 应延后到 shadow 和 order_check 稳定之后。

## 关键边界

- 回测：历史 point-in-time 输入 -> 决策链 -> 撮合模拟，不连接 MT5。
- Shadow：实时输入 -> 决策链 -> 纸面订单记录，不调用 MT5 下单。
- Paper MT5：实时决策通过 -> `order_check` -> 模拟账户 `order_send`。
- Live MT5：在 paper 稳定后启用，并必须有 kill switch、每日亏损、订单数、手数和重复开仓限制。

## 结论

当前架构可继续演进，不建议大规模重写。优化重点应放在：

1. 让文档权威来源清楚。
2. 让测试分层和输出边界清楚。
3. 让回测、shadow、paper、live 的运行模式清楚。
4. 后续代码重构只围绕真实痛点，不为了“看起来轻”而削掉审计能力。
