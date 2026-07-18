# SWE.3 软件详细设计

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 按架构组件进入模块与逐函数详细设计 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 阅读规则

SWE.3 采用“一个过程入口、一个组件一份文档”。本页只负责导航，避免把全部函数塞入单个巨型文件。

当前覆盖 **182 个软件单元**、**1082 个函数或方法**。函数卡片由受控源码和验证映射生成，不在生成文件中手工修改。

人工维护的关键单元补充设计见 [关键单元设计](./critical-units.md)，接口与 schema 参考见 [详细设计参考](./reference/README.md)。

## 组件导航

| 架构组件 | 软件单元 | 函数 | 关联需求 |
|---|---|---|---|
| [ARC-APP — 应用入口与运行配置](./ARC-APP.md) | 6 | 14 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| [ARC-CORE — 主编排与进度](./ARC-CORE.md) | 12 | 68 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| [ARC-DATA — 行情与外部数据](./ARC-DATA.md) | 30 | 134 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| [ARC-INDICATORS — 指标计算](./ARC-INDICATORS.md) | 3 | 12 | [SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| [ARC-ANALYSIS — 事实、结构、信号与报告门禁](./ARC-ANALYSIS.md) | 29 | 267 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| [ARC-AGENTS — 规则/LLM Agent 编排](./ARC-AGENTS.md) | 36 | 129 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| [ARC-LLM — LLM 传输、上下文和策略](./ARC-LLM.md) | 9 | 52 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| [ARC-RUN — 运行上下文与归档](./ARC-RUN.md) | 12 | 87 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| [ARC-BACKTEST — Point-in-time 回测](./ARC-BACKTEST.md) | 6 | 35 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| [ARC-VIZ — Streamlit 展示](./ARC-VIZ.md) | 21 | 191 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| [ARC-TOOLS — 开发、审核与运维工具](./ARC-TOOLS.md) | 18 | 93 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |

## 共同契约

- 前置条件：调用方满足函数签名、所属单元状态和关联需求约束。
- 后置条件：正常返回满足返回契约；副作用不得超出函数卡片记录的类别。
- 静态扫描未发现显式异常或副作用，不代表底层依赖绝不会产生间接行为。
