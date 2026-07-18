# SWE.2 软件架构设计

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.2 |
| 状态 | 受控基线 |
| 用途 | 评审组件职责、接口和运行模式 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 架构总览

| 组件 | 名称 | 软件单元 | 职责 |
|---|---|---|---|
| ARC-APP | 应用入口与运行配置 | 6 | 解析配置，启动 Streamlit，页面复用会话报告。 |
| ARC-CORE | 主编排与进度 | 12 | 按配置驱动 fetch、analysis、agents、report、archive，并发布阶段状态。 |
| ARC-DATA | 行情与外部数据 | 30 | 拉取、标准化、合并、标记来源与失败，并计算 as-of。 |
| ARC-INDICATORS | 指标计算 | 3 | 从冻结 OHLCV 计算技术指标并报告输入质量。 |
| ARC-ANALYSIS | 事实、结构、信号与报告门禁 | 29 | 计算 point-in-time 事实、计划、授权门禁、叙事和可靠度。 |
| ARC-AGENTS | 规则/LLM Agent 编排 | 36 | 运行 Analyst、Research、Debate、Levels、Trader、Risk、Manager 并保留来源。 |
| ARC-LLM | LLM 传输、上下文和策略 | 9 | 路由模型、构造上下文、传输/重试、解析并记录 I/O。 |
| ARC-RUN | 运行上下文与归档 | 12 | 建立运行 ID，原子保存成功/失败归档，验证兼容并加载回放。 |
| ARC-BACKTEST | Point-in-time 回测 | 6 | 截取历史数据、生成规则信号、应用宏观状态、模拟成交并汇总指标。 |
| ARC-VIZ | Streamlit 展示 | 21 | 展示报告、图表、外部数据、决策链、拒绝原因、回放和配置。 |
| ARC-TOOLS | 开发、审核与运维工具 | 18 | 校验连接、检查归档、生成样例和执行 ASPICE 一致性检查。 |

## 运行模式

| 模式 | 行为 |
|---|---|
| MODE-RULE | 规则 Agent 和确定性门禁，不调用 LLM。 |
| MODE-LLM | 配置的 LLM 阶段提供结构化结果，失败显式记录。 |
| MODE-HYBRID | 规则 baseline 先运行，合格 LLM 结果才可覆盖。 |
| MODE-REPLAY | 加载兼容归档，不执行 fetch 或新的 LLM 调用。 |

<a id="arc-app"></a>

## ARC-APP

**名称**：应用入口与运行配置

| 属性 | 内容 |
|---|---|
| 源码范围 | app.py、run_app.py、views/** |
| 静态接口 | run_app.py CLI、Streamlit session、RunConfig |
| 动态行为 | 解析配置，启动 Streamlit，页面复用会话报告。 |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 详细设计 | [查看 6 个软件单元](./SWE.3-software-detailed-design.md#arc-app) |

<a id="arc-core"></a>

## ARC-CORE

**名称**：主编排与进度

| 属性 | 内容 |
|---|---|
| 源码范围 | src/core/**、src/pipeline.py |
| 静态接口 | run_trade_agent_pipeline、ProgressReporter、core dataclasses |
| 动态行为 | 按配置驱动 fetch、analysis、agents、report、archive，并发布阶段状态。 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 详细设计 | [查看 12 个软件单元](./SWE.3-software-detailed-design.md#arc-core) |

<a id="arc-data"></a>

## ARC-DATA

**名称**：行情与外部数据

| 属性 | 内容 |
|---|---|
| 源码范围 | src/data/** |
| 静态接口 | DataFetchResult、MarketContext、DataSource、archive payload |
| 动态行为 | 拉取、标准化、合并、标记来源与失败，并计算 as-of。 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 详细设计 | [查看 30 个软件单元](./SWE.3-software-detailed-design.md#arc-data) |

<a id="arc-indicators"></a>

## ARC-INDICATORS

**名称**：指标计算

| 属性 | 内容 |
|---|---|
| 源码范围 | src/indicators/** |
| 静态接口 | enriched OHLCV、indicator snapshot |
| 动态行为 | 从冻结 OHLCV 计算技术指标并报告输入质量。 |
| 关联需求 | [SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001) |
| 详细设计 | [查看 3 个软件单元](./SWE.3-software-detailed-design.md#arc-indicators) |

<a id="arc-analysis"></a>

## ARC-ANALYSIS

**名称**：事实、结构、信号与报告门禁

| 属性 | 内容 |
|---|---|
| 源码范围 | src/analysis/** |
| 静态接口 | TimeframeAnalysis、TradingSignal、FactRegistry、invariant result |
| 动态行为 | 计算 point-in-time 事实、计划、授权门禁、叙事和可靠度。 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 详细设计 | [查看 29 个软件单元](./SWE.3-software-detailed-design.md#arc-analysis) |

<a id="arc-agents"></a>

## ARC-AGENTS

**名称**：规则/LLM Agent 编排

| 属性 | 内容 |
|---|---|
| 源码范围 | src/agents/** |
| 静态接口 | AnalystTeam、AgentEvidence、TransactionProposal、RiskReview、ManagerDecision |
| 动态行为 | 运行 Analyst、Research、Debate、Levels、Trader、Risk、Manager 并保留来源。 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 详细设计 | [查看 36 个软件单元](./SWE.3-software-detailed-design.md#arc-agents) |

<a id="arc-llm"></a>

## ARC-LLM

**名称**：LLM 传输、上下文和策略

| 属性 | 内容 |
|---|---|
| 源码范围 | src/llm/** |
| 静态接口 | LLMClient、stage payload、JSON schema parser |
| 动态行为 | 路由模型、构造上下文、传输/重试、解析并记录 I/O。 |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 详细设计 | [查看 9 个软件单元](./SWE.3-software-detailed-design.md#arc-llm) |

<a id="arc-run"></a>

## ARC-RUN

**名称**：运行上下文与归档

| 属性 | 内容 |
|---|---|
| 源码范围 | src/run/** |
| 静态接口 | RunContext、manifest、archive schema/index |
| 动态行为 | 建立运行 ID，原子保存成功/失败归档，验证兼容并加载回放。 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 详细设计 | [查看 12 个软件单元](./SWE.3-software-detailed-design.md#arc-run) |

<a id="arc-backtest"></a>

## ARC-BACKTEST

**名称**：Point-in-time 回测

| 属性 | 内容 |
|---|---|
| 源码范围 | src/backtest/** |
| 静态接口 | BacktestConfig、BacktestResult、TradeResult |
| 动态行为 | 截取历史数据、生成规则信号、应用宏观状态、模拟成交并汇总指标。 |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 详细设计 | [查看 6 个软件单元](./SWE.3-software-detailed-design.md#arc-backtest) |

<a id="arc-viz"></a>

## ARC-VIZ

**名称**：Streamlit 展示

| 属性 | 内容 |
|---|---|
| 源码范围 | src/viz/** |
| 静态接口 | report dict、chart HTML、Streamlit widgets/session |
| 动态行为 | 展示报告、图表、外部数据、决策链、拒绝原因、回放和配置。 |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 详细设计 | [查看 21 个软件单元](./SWE.3-software-detailed-design.md#arc-viz) |

<a id="arc-tools"></a>

## ARC-TOOLS

**名称**：开发、审核与运维工具

| 属性 | 内容 |
|---|---|
| 源码范围 | scripts/** |
| 静态接口 | CLI commands、audit artifacts |
| 动态行为 | 校验连接、检查归档、生成样例和执行 ASPICE 一致性检查。 |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 详细设计 | [查看 18 个软件单元](./SWE.3-software-detailed-design.md#arc-tools) |

## 组件接口

| 接口 | 提供者 | 消费者 | 契约 |
|---|---|---|---|
| IF-DATA-CONTEXT | ARC-DATA、ARC-INDICATORS | ARC-ANALYSIS、ARC-AGENTS | MarketContext + enriched timeframe DataFrames；时间索引必须带 UTC 语义。 |
| IF-ANALYSIS-AGENTS | ARC-ANALYSIS | ARC-AGENTS、ARC-LLM | 结构化事实、稳定 evidence/fact IDs 和候选计划；自由文本不得替代核心关系。 |
| IF-AGENTS-REPORT | ARC-AGENTS | ARC-ANALYSIS、ARC-CORE | AgentTrace、ManagerDecision 和授权 signal IDs。 |
| IF-REPORT-ARCHIVE | ARC-ANALYSIS、ARC-CORE | ARC-RUN、ARC-VIZ | 版本化 report schema；归档和 UI 消费同一门禁后快照。 |
