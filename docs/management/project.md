# Project Overview

GoldAnalysisAI 是一个围绕 XAUUSD 的 PA / ICT / SMC 分析与交易决策实验项目。它的核心目标不是“生成一篇漂亮报告”，而是把数据、结构、LLM 决策、风控、回测和执行通道逐步整理成可审计的交易研究系统。

## 当前产品形态

- Streamlit 多页面仪表盘：机构级报告、外部数据、短线策略、LLM 决策链。
- 数据源：TradingView K 线、金十新闻/日历、DXY/US10Y、TradingView 社媒。
- 决策链：Analyst Team -> Bull/Bear Research -> Debate -> Level Proposal -> Trader -> Risk -> Manager。
- LLM：支持 rule / llm / hybrid 双轨，并在 `agent_trace` 与 `meta.llm_io` 中保留审计。
- MT5：只作为账号/后续执行通道，不参与行情和历史回测。

## Owner 心智模型

```text
行情与外部事实
-> 指标与 ICT/PA 结构
-> Analyst Team + LLM/规则研究
-> 辩论与交易计划
-> 风控与经理决策
-> 回测 / shadow / paper_mt5 / live_mt5
```

平时开发先看回测和 shadow 质量；模拟账户主要验证执行链，不承担历史回测职责。

## 当前最重要边界

- 回测默认不连接 MT5，也不读取 MT5 K 线。
- MT5 只用于账号检查、`order_check`、模拟下单、实盘下单等执行阶段。
- 没有历史样本前，UI 不应把结构权重表达为真实胜率。
- LLM 可以提议与复核，但必须经过 schema、validator、规则 fallback 和风控边界。

## 下一步入口

- 想跑项目：读 [../operations/setup.md](../operations/setup.md)。
- 想判断架构是否清楚：读 [../aspice/SWE.2-architecture/health-review.md](../aspice/SWE.2-architecture/health-review.md)。
- 想跑测试：读 [../aspice/governance/verification-strategy.md](../aspice/governance/verification-strategy.md)。
- 想让我持续优化：读 [codex-autonomy.md](./codex-autonomy.md)。
