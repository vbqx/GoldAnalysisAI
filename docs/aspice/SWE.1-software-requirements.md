# SWE.1 软件需求分析

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.1 |
| 状态 | 受控基线 |
| 用途 | 理解、评审并追踪软件需求 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 基线概览

本基线包含 **26 条软件需求**。需求按唯一 ID 管理，并链接到架构组件、验证措施和接受准则。

| 优先级 | 数量 |
|---|---|
| P0 | 14 |
| P1 | 12 |

## 需求目录

| ID | 标题 | 类型 | 优先级 | 状态 |
|---|---|---|---|---|
| [SWR-CORE-001](#swr-core-001) | 交易分析流水线 | functional | P0 | agreed |
| [SWR-CORE-002](#swr-core-002) | 运行模式配置 | functional | P1 | agreed |
| [SWR-DATA-001](#swr-data-001) | 多周期 XAUUSD 行情 | functional | P0 | agreed |
| [SWR-DATA-002](#swr-data-002) | 外部证据源 | reliability | P1 | agreed |
| [SWR-DATA-003](#swr-data-003) | 数据时效与 as-of | reliability | P0 | agreed |
| [SWR-ANA-001](#swr-ana-001) | 技术与价格行为事实 | functional | P0 | agreed |
| [SWR-ANA-002](#swr-ana-002) | 交易计划几何 | functional | P0 | agreed |
| [SWR-ANA-003](#swr-ana-003) | 确定性风险和触发门禁 | reliability | P0 | agreed |
| [SWR-AGT-001](#swr-agt-001) | 规则 Agent 决策链 | functional | P1 | agreed |
| [SWR-LLM-001](#swr-llm-001) | 分阶段 LLM 决策链 | functional | P1 | agreed |
| [SWR-LLM-002](#swr-llm-002) | LLM schema 与回退 | reliability | P0 | agreed |
| [SWR-LLM-003](#swr-llm-003) | LLM 主张证据资格 | reliability | P0 | agreed |
| [SWR-REP-001](#swr-rep-001) | 报告结构契约 | functional | P0 | agreed |
| [SWR-REP-002](#swr-rep-002) | 事实注册与来源 | reliability | P0 | agreed |
| [SWR-REP-003](#swr-rep-003) | 最终报告不变量门禁 | reliability | P0 | agreed |
| [SWR-REP-004](#swr-rep-004) | 报告可靠度 | reliability | P1 | agreed |
| [SWR-ARC-001](#swr-arc-001) | 运行归档 | functional | P1 | agreed |
| [SWR-ARC-002](#swr-arc-002) | 归档兼容与回放 | compatibility | P1 | agreed |
| [SWR-BT-001](#swr-bt-001) | Point-in-time 规则回测 | functional | P1 | agreed |
| [SWR-UI-001](#swr-ui-001) | Streamlit 报告界面 | functional | P1 | agreed |
| [SWR-UI-002](#swr-ui-002) | 决策审计展示 | reliability | P0 | agreed |
| [SWR-CFG-001](#swr-cfg-001) | 配置与密钥边界 | security | P0 | agreed |
| [SWR-NFR-001](#swr-nfr-001) | 外部失败可恢复 | reliability | P0 | agreed |
| [SWR-NFR-002](#swr-nfr-002) | 可观测与可审计 | maintainability | P1 | agreed |
| [SWR-NFR-003](#swr-nfr-003) | 离线发布门禁 | maintainability | P1 | agreed |
| [SWR-NFR-004](#swr-nfr-004) | 可复现配置基线 | compatibility | P1 | agreed |

<a id="swr-core-001"></a>

## SWR-CORE-001

**标题**：交易分析流水线

系统应从受控运行配置启动数据获取、分析、Agent 决策、报告组装和归档，并返回结构化报告、行情数据和分析结果。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/management/project.md |
| 验证准则 | 离线集成测试证明主流水线按顺序完成且输出满足报告契约。 |
| 运行环境影响 | CPython 3.12；Windows 为主要开发环境，CI 使用 Linux。 |
| 架构组件 | [ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-core-002"></a>

## SWR-CORE-002

**标题**：运行模式配置

系统应在 rule、llm、hybrid 和 replay 模式间使用冻结的运行配置，并将有效配置写入审计记录。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/system-overview.md |
| 验证准则 | 配置单元测试覆盖合法值、默认值、环境变量和归档回放。 |
| 运行环境影响 | 环境变量来自 .env 或宿主环境；不得在报告中泄露密钥。 |
| 架构组件 | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-data-001"></a>

## SWR-DATA-001

**标题**：多周期 XAUUSD 行情

系统应获取并标准化 XAUUSD 的 5m、15m、1h、4h 和 1d OHLCV，并保留来源、时间框架和时间戳。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/technical-analysis.md |
| 验证准则 | 数据层测试验证列、索引、周期、排序、空值和降级行为。 |
| 运行环境影响 | 依赖 TradingView/OANDA 网络接口和 UTC 时间语义。 |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |

<a id="swr-data-002"></a>

## SWR-DATA-002

**标题**：外部证据源

系统应获取或明确降级 DXY、收益率、新闻、日历和社交数据，并保存来源与失败原因。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/analyst-context.md |
| 验证准则 | 单元测试覆盖成功、确认空、超时、不可用和占位数据禁止升级为事实。 |
| 运行环境影响 | 外部供应商可用性不由软件控制；live smoke 与发布门禁分离。 |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |

<a id="swr-data-003"></a>

## SWR-DATA-003

**标题**：数据时效与 as-of

系统应为关键市场与外部事实计算 data-as-of、年龄和 observation mode，并阻止未来数据进入决策。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/report-trust.md |
| 验证准则 | 固定时间夹具覆盖新鲜、陈旧、闭市、未来事件和跨时区边界。 |
| 运行环境影响 | 所有内部比较使用带时区 UTC 时间。 |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-ana-001"></a>

## SWR-ANA-001

**标题**：技术与价格行为事实

系统应从 point-in-time 行情计算技术指标、PA/ICT、FVG、OB、流动性和多周期结构，并保留可复算来源。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/technical-analysis.md |
| 验证准则 | 确定性夹具覆盖正例、反例、边界、相同高低点和禁止未来数据。 |
| 运行环境影响 | pandas/numpy 版本和重采样语义属于配置基线。 |
| 架构组件 | [ARC-INDICATORS](SWE.2-architecture/software-architecture.md#arc-indicators)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-ana-002"></a>

## SWR-ANA-002

**标题**：交易计划几何

系统应验证方向、入场区、止损、目标顺序和风险收益几何，并拒绝不一致计划。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/records/reviews/financial/static-code-review.md |
| 验证准则 | 边界测试覆盖 BUY/SELL、目标乱序、止损穿越、零风险和舍入。 |
| 运行环境影响 | 所有价格采用 XAUUSD 报价单位，显示精度不改变验证数值。 |
| 架构组件 | [ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-ana-003"></a>

## SWR-ANA-003

**标题**：确定性风险和触发门禁

系统应在 Manager 授权前检查几何、时效、触发状态、观察模式和执行资格。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/management/audit-plan.md |
| 验证准则 | 未触发、陈旧、未授权和冲突证据场景必须降级为等待或观察。 |
| 运行环境影响 | 门禁不得依赖外部 LLM 可用性。 |
| 架构组件 | [ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-agt-001"></a>

## SWR-AGT-001

**标题**：规则 Agent 决策链

系统应在无 LLM 时完成 Analyst、Research、Debate、Trader、Risk 和 Manager 规则链并记录阶段结果。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/llm-agents.md |
| 验证准则 | Agent chain 测试验证阶段顺序、输入输出和 Manager 决定。 |
| 运行环境影响 | 规则链必须可离线执行。 |
| 架构组件 | [ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-llm-001"></a>

## SWR-LLM-001

**标题**：分阶段 LLM 决策链

启用 LLM 时，系统应按配置执行结构化阶段，并记录模型、输入、输出、耗时、重试和来源。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/llm-agents.md |
| 验证准则 | 假客户端测试覆盖阶段成功、解析失败、schema 失败和回退。 |
| 运行环境影响 | 依赖 OpenAI-compatible 第三方 API；真实调用不是离线发布门禁。 |
| 架构组件 | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-llm-002"></a>

## SWR-LLM-002

**标题**：LLM schema 与回退

LLM 输出只有在 JSON/schema/置信度策略通过时方可覆盖规则结果，失败时应保存原因并按模式回退。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/llm-agents.md |
| 验证准则 | 解析、schema、阈值和重试测试证明错误输出不能进入授权链。 |
| 运行环境影响 | hybrid 允许规则回退；llm 模式必须明确失败语义。 |
| 架构组件 | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-llm-003"></a>

## SWR-LLM-003

**标题**：LLM 主张证据资格

核心技术主张应引用结构化 fact_ids、关系和反证裁决，未通过资格验证的主张不得成为执行依据。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/report-trust.md |
| 验证准则 | claim-v2 测试覆盖完整、部分、未知、冲突和不连通事实关系。 |
| 运行环境影响 | 资格由确定性代码判定，不使用模型自评替代。 |
| 架构组件 | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-architecture/software-architecture.md#arc-agents) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-rep-001"></a>

## SWR-REP-001

**标题**：报告结构契约

系统应生成符合版本化 schema 的报告，并保持关键字段、类型和审计元数据完整。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.3-detailed-design/reference/examples/report-schema.md |
| 验证准则 | 样例导出和 schema 回归测试比较关键字段与类型。 |
| 运行环境影响 | 新字段保持向后兼容或提升 schema 版本。 |
| 架构组件 | [ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-rep-002"></a>

## SWR-REP-002

**标题**：事实注册与来源

报告中的关键数值和外部事实应进入唯一事实注册表，包含 fact_id、value、as_of、source 和 quality。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/report-trust.md |
| 验证准则 | 事实注册测试覆盖价格、PA、时效、日历、外部源和技术主张。 |
| 运行环境影响 | 缺来源事实不得标为 verified。 |
| 架构组件 | [ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-rep-003"></a>

## SWR-REP-003

**标题**：最终报告不变量门禁

报告归档和展示前应验证授权、几何、事实价格、时效、Manager 对齐和审计元数据。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/report-trust.md |
| 验证准则 | 违规夹具必须使报告降级并撤销执行资格；合法夹具保持通过。 |
| 运行环境影响 | 门禁为离线确定性组件。 |
| 架构组件 | [ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-rep-004"></a>

## SWR-REP-004

**标题**：报告可靠度

系统应使用可解释的确定性分项计算报告可靠度，并与模型 confidence 分离展示。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/report-trust.md |
| 验证准则 | 可靠度测试覆盖缺失、陈旧、来源多样性、schema 和不变量状态。 |
| 运行环境影响 | 公式版本随报告保存。 |
| 架构组件 | [ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-arc-001"></a>

## SWR-ARC-001

**标题**：运行归档

系统应归档运行配置、manifest、报告、分析、数据摘要和状态，并可列举、加载和验证。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.3-detailed-design/reference/run-archive-schema.md |
| 验证准则 | 归档测试覆盖成功、失败、原子写入、索引、传输和裁剪。 |
| 运行环境影响 | 文件系统需支持项目数据目录写入。 |
| 架构组件 | [ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-arc-002"></a>

## SWR-ARC-002

**标题**：归档兼容与回放

系统应检测归档 schema 兼容性，并在不重新调用外部数据或 LLM 的情况下加载可兼容历史报告。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | compatibility / P1 / agreed |
| 来源 | docs/aspice/SWE.3-detailed-design/reference/run-archive-schema.md |
| 验证准则 | 兼容夹具测试覆盖旧版本、缺失字段、不可兼容和完整回放。 |
| 运行环境影响 | 历史归档可能来自不同 Git SHA 和依赖版本。 |
| 架构组件 | [ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-bt-001"></a>

## SWR-BT-001

**标题**：Point-in-time 规则回测

系统应按时间截点运行规则 baseline、宏观 overlay 和执行仿真，不使用截点后的数据。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/backtesting.md |
| 验证准则 | 固定 OHLCV 和 DXY 夹具验证截点、交易顺序、成本和指标。 |
| 运行环境影响 | 当前结果只代表规则 baseline，不代表完整 LLM 表现。 |
| 架构组件 | [ARC-BACKTEST](SWE.2-architecture/software-architecture.md#arc-backtest)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](SWE.5-integration-testing.md#vm-backtest) |

<a id="swr-ui-001"></a>

## SWR-UI-001

**标题**：Streamlit 报告界面

系统应展示机构报告、短线策略、决策链和回测/配置页面，并复用同一会话报告。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/records/reviews/gui/streamlit-acceptance-2026-07-08.md |
| 验证准则 | UI helper 测试与人工验收覆盖导航、缓存、等待和主要组件。 |
| 运行环境影响 | 应用必须使用 run_app.py 启动。 |
| 架构组件 | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) |

<a id="swr-ui-002"></a>

## SWR-UI-002

**标题**：决策审计展示

界面应展示 agent_trace、stage source、LLM I/O、可靠度、不变量和未授权原因，不得把观察计划标为执行。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/report-trust.md |
| 验证准则 | UI helper 和人工场景验证授权状态、来源、拒绝原因和观察措辞。 |
| 运行环境影响 | UI 只消费已通过门禁的报告状态。 |
| 架构组件 | [ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) |

<a id="swr-cfg-001"></a>

## SWR-CFG-001

**标题**：配置与密钥边界

系统应从环境加载配置，不将密钥写入源码、日志、报告、归档或版本库。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | security / P0 / agreed |
| 来源 | docs/operations/setup.md |
| 验证准则 | 配置测试和秘密扫描验证默认禁用、URL 脱敏和受控示例。 |
| 运行环境影响 | .env 为本地非配置项，.env.example 为受控模板。 |
| 架构组件 | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-CONFIG](SWE.6-validation-testing.md#vm-config) |

<a id="swr-nfr-001"></a>

## SWR-NFR-001

**标题**：外部失败可恢复

外部数据或 LLM 失败时，系统应给出明确失败/降级状态，不得伪造事实或静默提升占位数据。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/management/audit-plan.md |
| 验证准则 | 故障注入覆盖超时、空结果、无效 JSON、HTTP 错误和部分数据。 |
| 运行环境影响 | 网络和供应商健康不作为软件本身通过的唯一依据。 |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |

<a id="swr-nfr-002"></a>

## SWR-NFR-002

**标题**：可观测与可审计

系统应记录运行 ID、配置、阶段、来源、耗时、错误、模型 I/O 摘要、数据 as-of 和验证状态。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | maintainability / P1 / agreed |
| 来源 | docs/management/audit-plan.md |
| 验证准则 | 审计摘要和进度测试验证字段完整、稳定和可归档。 |
| 运行环境影响 | 日志不得包含密钥或未脱敏 URL。 |
| 架构组件 | [ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-nfr-003"></a>

## SWR-NFR-003

**标题**：离线发布门禁

每个相关变更应执行 unit、regression、文档/追溯一致性和静态编译检查，并保存结果。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | maintainability / P1 / agreed |
| 来源 | docs/aspice/governance/verification-strategy.md |
| 验证准则 | GitHub Actions 对源码、文档、测试和配置变更运行质量工作流。 |
| 运行环境影响 | 离线门禁不调用付费 LLM、MT5 或 live external API。 |
| 架构组件 | [ARC-TOOLS](SWE.2-architecture/software-architecture.md#arc-tools) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace)、[VM-STATIC](SWE.6-validation-testing.md#vm-static) |

<a id="swr-nfr-004"></a>

## SWR-NFR-004

**标题**：可复现配置基线

发布基线应标识源码引用、直接与传递依赖、配置模板、schema、测试选择和验证结果。

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | compatibility / P1 / agreed |
| 来源 | docs/aspice/configuration-management.md |
| 验证准则 | 配置校验确认清单路径存在、锁文件精确固定且 SBOM 与锁一致。 |
| 运行环境影响 | 不同平台的可选依赖应显式标注。 |
| 架构组件 | [ARC-TOOLS](SWE.2-architecture/software-architecture.md#arc-tools)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-CONFIG](SWE.6-validation-testing.md#vm-config)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace) |
