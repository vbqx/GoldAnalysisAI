# ARC-AGENTS — 规则/LLM Agent 编排

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./README.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/README.md#arc-agents)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/agents/__init__.py](#unit-818fcec908) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/__init__.py](#unit-b6c46ef660) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/base.py](#unit-8110cb5da5) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/evidence_ids.py](#unit-87b2f0bba3) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/evidence_provenance.py](#unit-5e6c877f3b) | 11 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/fundamentals.py](#unit-52003276aa) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/news.py](#unit-3628b84ddf) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/news_bias.py](#unit-b6597d0c34) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/sentiment.py](#unit-8f2897b88a) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/structure_zones.py](#unit-3363ad337f) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/technical.py](#unit-8d8fc5eaa1) | 9 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/bearish.py](#unit-8933374b3e) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/bullish.py](#unit-6008a95748) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/debate.py](#unit-34bf03f815) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/factory.py](#unit-f23db48d75) | 20 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/__init__.py](#unit-1606bdc6e2) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/base.py](#unit-3eeb009803) | 5 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/payload.py](#unit-3a49bda3a6) | 25 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/schemas.py](#unit-9b539edeb6) | 18 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/__init__.py](#unit-7226a2379a) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/__init__.py](#unit-1df6497ce4) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/_common.py](#unit-73b0811649) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/fundamentals.py](#unit-fcd3d48fde) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/news.py](#unit-25115c1d6f) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/sentiment.py](#unit-2bf1b61e7e) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/technical.py](#unit-a3445b9493) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/bearish.py](#unit-2ccd7c4dcb) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/bullish.py](#unit-12bf07eb04) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/debate.py](#unit-3970799e39) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/levels.py](#unit-4fbc2b73a8) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/manager.py](#unit-5ed826be60) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/risk.py](#unit-9038f74287) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/trader.py](#unit-a996419c04) | 2 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/manager.py](#unit-cc665640c2) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/risk.py](#unit-c1468c2396) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/trader.py](#unit-6340c2c541) | 1 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-818fcec908"></a>

### UNIT-818FCEC908

**模块**：`src/agents/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-818FCEC908 |
| 源码 | [src/agents/__init__.py](../../../src/agents/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-b6c46ef660"></a>

### UNIT-B6C46EF660

**模块**：`src/agents/analysts/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B6C46EF660 |
| 源码 | [src/agents/analysts/__init__.py](../../../src/agents/analysts/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/__init__.py` 的职责，通过 `run_analyst_team` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_analyst_team](#fun-00321f2b4a)

<a id="fun-00321f2b4a"></a>

#### FUN-00321F2B4A

| 设计项 | 说明 |
|---|---|
| 函数 | `run_analyst_team` |
| 源码位置 | [src/agents/analysts/__init__.py](../../../src/agents/analysts/__init__.py) · `L20` |
| 签名 | `run_analyst_team(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `AnalystTeam` 类型结果 |
| 职责 | 执行分析师团队结果；返回 `AnalystTeam` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `AnalystTeam` → `run_technical_analyst` → `run_fundamentals_analyst` → `run_news_analyst` → `run_sentiment_analyst`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystTeam` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | AnalystTeam、run_technical_analyst、run_fundamentals_analyst、run_news_analyst、run_sentiment_analyst |
| 复杂度 / 风险 | 分支 0；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="unit-8110cb5da5"></a>

### UNIT-8110CB5DA5

**模块**：`src/agents/analysts/base.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8110CB5DA5 |
| 源码 | [src/agents/analysts/base.py](../../../src/agents/analysts/base.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/base.py` 的职责，通过 `confidence_from_items`、`build_report`、`items_for_direction` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) |
| 验证状态 | selected |

#### 函数导航

[confidence_from_items](#fun-c3439bfbe3) · [build_report](#fun-cc65b2503a) · [items_for_direction](#fun-7ef67bfe39)

<a id="fun-c3439bfbe3"></a>

#### FUN-C3439BFBE3

| 设计项 | 说明 |
|---|---|
| 函数 | `confidence_from_items` |
| 源码位置 | [src/agents/analysts/base.py](../../../src/agents/analysts/base.py) · `L11` |
| 签名 | `confidence_from_items(items: list[EvidenceItem])` |
| 参数 | `items`（list[EvidenceItem]）：输入项集合 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 根据`items`计算置信度；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `min` → `sum`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | min、sum、len |
| 复杂度 / 风险 | 分支 1；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cc65b2503a"></a>

#### FUN-CC65B2503A

| 设计项 | 说明 |
|---|---|
| 函数 | `build_report` |
| 源码位置 | [src/agents/analysts/base.py](../../../src/agents/analysts/base.py) · `L17` |
| 签名 | `build_report(*, agent: str, items: list[EvidenceItem], bias: Bias, summary: str \| None=None)` |
| 参数 | `agent`（str）：Agent 实例或标识<br>`items`（list[EvidenceItem]）：输入项集合<br>`bias`（Bias）：由调用方提供的 `bias` 输入对象<br>`summary`（str \| None）：摘要内容；默认值 `None` |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 构建报告；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `confidence_from_items` → `AnalystReport` → `assign_evidence_ids`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystReport` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | confidence_from_items、len、AnalystReport、assign_evidence_ids |
| 复杂度 / 风险 | 分支 2；跨度 20 行；中 |
| 测试 / 验证 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="fun-7ef67bfe39"></a>

#### FUN-7EF67BFE39

| 设计项 | 说明 |
|---|---|
| 函数 | `items_for_direction` |
| 源码位置 | [src/agents/analysts/base.py](../../../src/agents/analysts/base.py) · `L39` |
| 签名 | `items_for_direction(team_reports: list[AnalystReport], direction: Bias)` |
| 参数 | `team_reports`（list[AnalystReport]）：由 `team_reports` 表示的输入集合<br>`direction`（Bias）：交易方向 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`items_for_direction`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.agent.replace` → `merged.append` → `EvidenceItem` → `min` → `max` → `merged.sort`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.agent.replace、merged.append、EvidenceItem、min、max、merged.sort |
| 复杂度 / 风险 | 分支 3；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py) · 直接动态测试 |

<a id="unit-87b2f0bba3"></a>

### UNIT-87B2F0BBA3

**模块**：`src/agents/analysts/evidence_ids.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-87B2F0BBA3 |
| 源码 | [src/agents/analysts/evidence_ids.py](../../../src/agents/analysts/evidence_ids.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/evidence_ids.py` 的职责，通过 `assign_evidence_ids` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[assign_evidence_ids](#fun-736ecac34c)

<a id="fun-736ecac34c"></a>

#### FUN-736ECAC34C

| 设计项 | 说明 |
|---|---|
| 函数 | `assign_evidence_ids` |
| 源码位置 | [src/agents/analysts/evidence_ids.py](../../../src/agents/analysts/evidence_ids.py) · `L8` |
| 签名 | `assign_evidence_ids(agent: str, items: list[EvidenceItem])` |
| 参数 | `agent`（str）：Agent 实例或标识<br>`items`（list[EvidenceItem]）：输入项集合 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`assign_evidence_ids`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `enumerate` → `strip` → `out.append` → `EvidenceItem`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | enumerate、strip、out.append、EvidenceItem、dict |
| 复杂度 / 风险 | 分支 1；跨度 16 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-5e6c877f3b"></a>

### UNIT-5E6C877F3B

**模块**：`src/agents/analysts/evidence_provenance.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5E6C877F3B |
| 源码 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/evidence_provenance.py` 的职责，通过 `analyst_evidence_ids`、`evidence_registry`、`is_new_structure_id`、`dedupe_evidence_items`、`parse_research_items`、`build_research_provenance_meta`、`blend_research_confidence`、`build_debate_provenance_meta` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py) |
| 验证状态 | selected |

#### 函数导航

[analyst_evidence_ids](#fun-89a55043e0) · [evidence_registry](#fun-c2ce034d09) · [is_new_structure_id](#fun-bc6ab45103) · [_allowed_id](#fun-5138cc692a) · [dedupe_evidence_items](#fun-aea352184d) · [_restore_refs](#fun-dfee2688c2) · [parse_research_items](#fun-43d1351553) · [build_research_provenance_meta](#fun-87a0b32a1c) · [blend_research_confidence](#fun-94884173fc) · [build_debate_provenance_meta](#fun-d72e36ce1e) · [blend_debate_consensus](#fun-1e35c05ea3)

<a id="fun-89a55043e0"></a>

#### FUN-89A55043E0

| 设计项 | 说明 |
|---|---|
| 函数 | `analyst_evidence_ids` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L10` |
| 签名 | `analyst_evidence_ids(team: AnalystTeam)` |
| 参数 | `team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `set[str]` 类型结果 |
| 职责 | 构建`analyst_evidence_ids`；返回 `set[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `strip` → `ids.add`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `set[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、getattr、strip、ids.add |
| 复杂度 / 风险 | 分支 3；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c2ce034d09"></a>

#### FUN-C2CE034D09

| 设计项 | 说明 |
|---|---|
| 函数 | `evidence_registry` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L20` |
| 签名 | `evidence_registry(team: AnalystTeam)` |
| 参数 | `team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `dict[str, EvidenceItem]` 类型结果 |
| 职责 | 构建`evidence_registry`；返回 `dict[str, EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `strip`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、strip |
| 复杂度 / 风险 | 分支 3；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py) · 直接动态测试 |

<a id="fun-bc6ab45103"></a>

#### FUN-BC6AB45103

| 设计项 | 说明 |
|---|---|
| 函数 | `is_new_structure_id` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L30` |
| 签名 | `is_new_structure_id(evidence_id: str, agent: str)` |
| 参数 | `evidence_id`（str）：对象标识<br>`agent`（str）：Agent 实例或标识 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`new_structure_id`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5138cc692a"></a>

#### FUN-5138CC692A

| 设计项 | 说明 |
|---|---|
| 函数 | `_allowed_id` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L35` |
| 签名 | `_allowed_id(evidence_id: str, *, agent: str, allowed_ids: set[str])` |
| 参数 | `evidence_id`（str）：对象标识<br>`agent`（str）：Agent 实例或标识<br>`allowed_ids`（set[str]）：由 `allowed_ids` 表示的输入集合 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`allowed_id`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `evidence_id.strip`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | evidence_id.strip |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-aea352184d"></a>

#### FUN-AEA352184D

| 设计项 | 说明 |
|---|---|
| 函数 | `dedupe_evidence_items` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L42` |
| 签名 | `dedupe_evidence_items(items: list[EvidenceItem])` |
| 参数 | `items`（list[EvidenceItem]）：输入项集合 |
| 返回 | 返回 `tuple[list[EvidenceItem], int]` 类型结果 |
| 职责 | 去重证据条目；返回 `tuple[list[EvidenceItem], int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `best.get` → `max` → `sorted` → `best.values`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[EvidenceItem], int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、best.get、max、len、sorted、best.values |
| 复杂度 / 风险 | 分支 3；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py) · 直接动态测试 |

<a id="fun-dfee2688c2"></a>

#### FUN-DFEE2688C2

| 设计项 | 说明 |
|---|---|
| 函数 | `_restore_refs` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L57` |
| 签名 | `_restore_refs(item: EvidenceItem, registry: dict[str, EvidenceItem])` |
| 参数 | `item`（EvidenceItem）：当前处理条目<br>`registry`（dict[str, EvidenceItem]）：事实或证据登记映射 |
| 返回 | 返回 `EvidenceItem` 类型结果 |
| 职责 | 生成`restore_refs`结果；返回 `EvidenceItem` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `registry.get` → `merged_refs.update` → `item.refs.items` → `merged_refs.get` → `upstream.refs.get` → `merged_refs.setdefault` → `EvidenceItem`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `EvidenceItem` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、registry.get、dict、merged_refs.update、item.refs.items、merged_refs.get、upstream.refs.get、merged_refs.setdefault、EvidenceItem |
| 复杂度 / 风险 | 分支 2；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-43d1351553"></a>

#### FUN-43D1351553

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_research_items` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L77` |
| 签名 | `parse_research_items(rows: list[dict[str, Any]], *, agent: str, direction: Bias, allowed_ids: set[str], registry: dict[str, EvidenceItem], item_refs_fn)` |
| 参数 | `rows`（list[dict[str, Any]]）：记录行集合<br>`agent`（str）：Agent 实例或标识<br>`direction`（Bias）：交易方向<br>`allowed_ids`（set[str]）：由 `allowed_ids` 表示的输入集合<br>`registry`（dict[str, EvidenceItem]）：事实或证据登记映射<br>`item_refs_fn`（实现约定类型）：由调用方提供的 `item_refs_fn` 输入对象 |
| 返回 | 返回 `tuple[list[EvidenceItem], int]` 类型结果 |
| 职责 | 解析研究证据条目；返回 `tuple[list[EvidenceItem], int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `enumerate` → `isinstance` → `strip` → `row.get` → `ValueError` → `_allowed_id` → `item_refs_fn` → `max`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[EvidenceItem], int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | enumerate、isinstance、strip、str、row.get、ValueError、_allowed_id、item_refs_fn、float、max、min、EvidenceItem、_restore_refs、parsed.append、dedupe_evidence_items |
| 复杂度 / 风险 | 分支 7；跨度 46 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-87a0b32a1c"></a>

#### FUN-87A0B32A1C

| 设计项 | 说明 |
|---|---|
| 函数 | `build_research_provenance_meta` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L125` |
| 签名 | `build_research_provenance_meta(items: list[EvidenceItem], *, allowed_ids: set[str], model_confidence: float, dedupe_dropped: int=0)` |
| 参数 | `items`（list[EvidenceItem]）：输入项集合<br>`allowed_ids`（set[str]）：由 `allowed_ids` 表示的输入集合<br>`model_confidence`（float）：由 `model_confidence` 表示的数值参数<br>`dedupe_dropped`（int）：由 `dedupe_dropped` 表示的数值参数；默认值 `0` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`research_provenance_meta`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `sum` → `i.refs.get` → `min` → `max`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、sum、len、str、i.refs.get、min、max |
| 复杂度 / 风险 | 分支 1；跨度 32 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-94884173fc"></a>

#### FUN-94884173FC

| 设计项 | 说明 |
|---|---|
| 函数 | `blend_research_confidence` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L159` |
| 签名 | `blend_research_confidence(model_confidence: float, meta: dict[str, Any])` |
| 参数 | `model_confidence`（float）：由 `model_confidence` 表示的数值参数<br>`meta`（dict[str, Any]）：审计或处理元数据 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`blend_research_confidence`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、meta.get、max、min |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d72e36ce1e"></a>

#### FUN-D72E36CE1E

| 设计项 | 说明 |
|---|---|
| 函数 | `build_debate_provenance_meta` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L164` |
| 签名 | `build_debate_provenance_meta(bullish: list[EvidenceItem], bearish: list[EvidenceItem], *, model_consensus_strength: float)` |
| 参数 | `bullish`（list[EvidenceItem]）：看多证据或计数<br>`bearish`（list[EvidenceItem]）：看空证据或计数<br>`model_consensus_strength`（float）：由 `model_consensus_strength` 表示的数值参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`debate_provenance_meta`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `min` → `max` → `round` → `sorted`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、min、max、round、sorted |
| 复杂度 / 风险 | 分支 0；跨度 24 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1e35c05ea3"></a>

#### FUN-1E35C05EA3

| 设计项 | 说明 |
|---|---|
| 函数 | `blend_debate_consensus` |
| 源码位置 | [src/agents/analysts/evidence_provenance.py](../../../src/agents/analysts/evidence_provenance.py) · `L190` |
| 签名 | `blend_debate_consensus(model_strength: float, meta: dict[str, Any])` |
| 参数 | `model_strength`（float）：由 `model_strength` 表示的数值参数<br>`meta`（dict[str, Any]）：审计或处理元数据 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`blend_debate_consensus`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、meta.get、max、min |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-52003276aa"></a>

### UNIT-52003276AA

**模块**：`src/agents/analysts/fundamentals.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-52003276AA |
| 源码 | [src/agents/analysts/fundamentals.py](../../../src/agents/analysts/fundamentals.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/fundamentals.py` 的职责，通过 `run_fundamentals_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_bias_from_quotes](#fun-39f851dead) · [_macro_context_evidence](#fun-d0b578d7f2) · [run_fundamentals_analyst](#fun-2dc8e34e80)

<a id="fun-39f851dead"></a>

#### FUN-39F851DEAD

| 设计项 | 说明 |
|---|---|
| 函数 | `_bias_from_quotes` |
| 源码位置 | [src/agents/analysts/fundamentals.py](../../../src/agents/analysts/fundamentals.py) · `L11` |
| 签名 | `_bias_from_quotes(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `Bias` 类型结果 |
| 职责 | 根据`quotes`构建`bias`；返回 `Bias` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `votes.get` → `any`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Bias` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | votes.get、any |
| 复杂度 / 风险 | 分支 5；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d0b578d7f2"></a>

#### FUN-D0B578D7F2

| 设计项 | 说明 |
|---|---|
| 函数 | `_macro_context_evidence` |
| 源码位置 | [src/agents/analysts/fundamentals.py](../../../src/agents/analysts/fundamentals.py) · `L27` |
| 签名 | `_macro_context_evidence(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`macro_context_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `ev.display` → `items.append` → `EvidenceItem` → `min` → `ctx.derived.get` → `strip` → `countdown.get`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、ev.display、items.append、EvidenceItem、len、min、ctx.derived.get、strip、countdown.get、err.lower |
| 复杂度 / 风险 | 分支 6；跨度 64 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2dc8e34e80"></a>

#### FUN-2DC8E34E80

| 设计项 | 说明 |
|---|---|
| 函数 | `run_fundamentals_analyst` |
| 源码位置 | [src/agents/analysts/fundamentals.py](../../../src/agents/analysts/fundamentals.py) · `L93` |
| 签名 | `run_fundamentals_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 执行基本面分析 Agent；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `external_macro_evidence` → `_macro_context_evidence` → `_bias_from_quotes` → `any` → `i.refs.get` → `get` → `ctx.context_stats.get` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystReport` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | external_macro_evidence、_macro_context_evidence、_bias_from_quotes、any、i.refs.get、get、ctx.context_stats.get、join、build_report |
| 复杂度 / 风险 | 分支 1；跨度 15 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="unit-3628b84ddf"></a>

### UNIT-3628B84DDF

**模块**：`src/agents/analysts/news.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3628B84DDF |
| 源码 | [src/agents/analysts/news.py](../../../src/agents/analysts/news.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/news.py` 的职责，通过 `run_news_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_news_context_evidence](#fun-215c3fb37a) · [run_news_analyst](#fun-b07796dbd7)

<a id="fun-215c3fb37a"></a>

#### FUN-215C3FB37A

| 设计项 | 说明 |
|---|---|
| 函数 | `_news_context_evidence` |
| 源码位置 | [src/agents/analysts/news.py](../../../src/agents/analysts/news.py) · `L12` |
| 签名 | `_news_context_evidence(ctx: MarketContext, *, is_live: bool)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`is_live`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`news_context_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `items.append` → `EvidenceItem` → `min` → `ctx.derived.get` → `topic.get` → `err.lower` → `join`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、items.append、EvidenceItem、len、min、ctx.derived.get、topic.get、str、int、err.lower、join |
| 复杂度 / 风险 | 分支 7；跨度 63 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b07796dbd7"></a>

#### FUN-B07796DBD7

| 设计项 | 说明 |
|---|---|
| 函数 | `run_news_analyst` |
| 源码位置 | [src/agents/analysts/news.py](../../../src/agents/analysts/news.py) · `L77` |
| 签名 | `run_news_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 执行新闻分析 Agent；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `any` → `external_to_evidence` → `_news_context_evidence` → `infer_news_bias` → `sum` → `build_report`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystReport` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | any、external_to_evidence、_news_context_evidence、infer_news_bias、len、sum、build_report |
| 复杂度 / 风险 | 分支 2；跨度 22 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="unit-b6597d0c34"></a>

### UNIT-B6597D0C34

**模块**：`src/agents/analysts/news_bias.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B6597D0C34 |
| 源码 | [src/agents/analysts/news_bias.py](../../../src/agents/analysts/news_bias.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/news_bias.py` 的职责，通过 `infer_news_bias` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[infer_news_bias](#fun-8413383608)

<a id="fun-8413383608"></a>

#### FUN-8413383608

| 设计项 | 说明 |
|---|---|
| 函数 | `infer_news_bias` |
| 源码位置 | [src/agents/analysts/news_bias.py](../../../src/agents/analysts/news_bias.py) · `L37` |
| 签名 | `infer_news_bias(headlines: list[HeadlineItem], calendar: list[CalendarEvent], *, risk_text: str='')` |
| 参数 | `headlines`（list[HeadlineItem]）：由 `headlines` 表示的输入集合<br>`calendar`（list[CalendarEvent]）：由 `calendar` 表示的输入集合<br>`risk_text`（str）：输入文本；默认值 `''` |
| 返回 | 返回 `Bias` 类型结果 |
| 职责 | 生成`infer_news_bias`结果；返回 `Bias` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `join` → `sum` → `k.lower`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Bias` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、join、sum、k.lower |
| 复杂度 / 风险 | 分支 4；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-8f2897b88a"></a>

### UNIT-8F2897B88A

**模块**：`src/agents/analysts/sentiment.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8F2897B88A |
| 源码 | [src/agents/analysts/sentiment.py](../../../src/agents/analysts/sentiment.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/sentiment.py` 的职责，通过 `run_sentiment_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_social_note](#fun-853c57015e) · [_social_bias_delta](#fun-e569d3f536) · [_sentiment_context_evidence](#fun-00db5653b2) · [run_sentiment_analyst](#fun-8e5ddab513)

<a id="fun-853c57015e"></a>

#### FUN-853C57015E

| 设计项 | 说明 |
|---|---|
| 函数 | `_social_note` |
| 源码位置 | [src/agents/analysts/sentiment.py](../../../src/agents/analysts/sentiment.py) · `L12` |
| 签名 | `_social_note(ext, post_count: int)` |
| 参数 | `ext`（实现约定类型）：由调用方提供的 `ext` 输入对象<br>`post_count`（int）：数量或处理上限 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`social_note`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、len |
| 复杂度 / 风险 | 分支 4；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e569d3f536"></a>

#### FUN-E569D3F536

| 设计项 | 说明 |
|---|---|
| 函数 | `_social_bias_delta` |
| 源码位置 | [src/agents/analysts/sentiment.py](../../../src/agents/analysts/sentiment.py) · `L23` |
| 签名 | `_social_bias_delta(posts: list[dict])` |
| 参数 | `posts`（list[dict]）：由 `posts` 表示的输入集合 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`social_bias_delta`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `post.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、post.get |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-00db5653b2"></a>

#### FUN-00DB5653B2

| 设计项 | 说明 |
|---|---|
| 函数 | `_sentiment_context_evidence` |
| 源码位置 | [src/agents/analysts/sentiment.py](../../../src/agents/analysts/sentiment.py) · `L33` |
| 签名 | `_sentiment_context_evidence(ctx: MarketContext, vote: dict[str, float])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`vote`（dict[str, float]）：由 `vote` 表示的键值映射 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`sentiment_context_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.analyses.items` → `trends.values` → `join` → `sorted` → `trends.items` → `items.append` → `EvidenceItem` → `post.get`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ctx.analyses.items、len、set、trends.values、join、sorted、trends.items、items.append、EvidenceItem、str、post.get、kind_counts.get、int、min、max、round、_social_bias_delta、abs、err.lower |
| 复杂度 / 风险 | 分支 9；跨度 68 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8e5ddab513"></a>

#### FUN-8E5DDAB513

| 设计项 | 说明 |
|---|---|
| 函数 | `run_sentiment_analyst` |
| 源码位置 | [src/agents/analysts/sentiment.py](../../../src/agents/analysts/sentiment.py) · `L103` |
| 签名 | `run_sentiment_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 执行情绪分析 Agent；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment_score` → `EvidenceItem` → `max` → `items.extend` → `_sentiment_context_evidence` → `post.get` → `items.append` → `min`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystReport` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment_score、EvidenceItem、max、items.extend、_sentiment_context_evidence、str、post.get、items.append、min、abs、any、_social_bias_delta、_social_note、len、build_report |
| 复杂度 / 风险 | 分支 9；跨度 57 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="unit-3363ad337f"></a>

### UNIT-3363AD337F

**模块**：`src/agents/analysts/structure_zones.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3363AD337F |
| 源码 | [src/agents/analysts/structure_zones.py](../../../src/agents/analysts/structure_zones.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/structure_zones.py` 的职责，通过 `ict_zone_evidence` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[ict_zone_evidence](#fun-6eec9deabd)

<a id="fun-6eec9deabd"></a>

#### FUN-6EEC9DEABD

| 设计项 | 说明 |
|---|---|
| 函数 | `ict_zone_evidence` |
| 源码位置 | [src/agents/analysts/structure_zones.py](../../../src/agents/analysts/structure_zones.py) · `L11` |
| 签名 | `ict_zone_evidence(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`ict_zone_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_TF_ZONE_WEIGHT.items` → `ctx.analyses.get` → `seen.add` → `items.append` → `EvidenceItem` → `round`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、_TF_ZONE_WEIGHT.items、ctx.analyses.get、float、seen.add、items.append、EvidenceItem、round |
| 复杂度 / 风险 | 分支 7；跨度 49 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-8d8fc5eaa1"></a>

### UNIT-8D8FC5EAA1

**模块**：`src/agents/analysts/technical.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8D8FC5EAA1 |
| 源码 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/analysts/technical.py` 的职责，通过 `run_technical_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 9 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_technical_analyst](#fun-10ecc215f3) | 执行技术分析 Agent；可能影响外部接口；返回 `AnalystReport` 类型结果。 | 外部接口 I/O | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |

#### 函数导航

[_structure_bias](#fun-6bf4e07518) · [_ict_context_evidence](#fun-a800d7efb0) · [_fibonacci_evidence](#fun-047ed2fce9) · [_indicator_evidence](#fun-30c0262d6e) · [_quality_evidence](#fun-efb2eb527e) · [_support_resistance_evidence](#fun-0adaa6f91a) · [_level_price_text](#fun-699a6c41bf) · [_pa_evidence](#fun-5e5145e5af) · [run_technical_analyst](#fun-10ecc215f3)

<a id="fun-6bf4e07518"></a>

#### FUN-6BF4E07518

| 设计项 | 说明 |
|---|---|
| 函数 | `_structure_bias` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L19` |
| 签名 | `_structure_bias(analyses: dict[str, TimeframeAnalysis])` |
| 参数 | `analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果 |
| 返回 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果 |
| 职责 | 构建`structure_bias`；返回 `tuple[Bias, list[EvidenceItem]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `TF_WEIGHT.items` → `analyses.get` → `items.append` → `EvidenceItem`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | TF_WEIGHT.items、analyses.get、items.append、EvidenceItem |
| 复杂度 / 风险 | 分支 8；跨度 51 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a800d7efb0"></a>

#### FUN-A800D7EFB0

| 设计项 | 说明 |
|---|---|
| 函数 | `_ict_context_evidence` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L72` |
| 签名 | `_ict_context_evidence(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果 |
| 职责 | 构建`ict_context_evidence`；返回 `tuple[Bias, list[EvidenceItem]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `TF_WEIGHT.items` → `ctx.analyses.get` → `get` → `round` → `items.append` → `EvidenceItem` → `sorted` → `abs`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | TF_WEIGHT.items、ctx.analyses.get、get、round、items.append、EvidenceItem、sorted、abs、distance_pct、float、max、getattr |
| 复杂度 / 风险 | 分支 10；跨度 75 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-047ed2fce9"></a>

#### FUN-047ED2FCE9

| 设计项 | 说明 |
|---|---|
| 函数 | `_fibonacci_evidence` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L149` |
| 签名 | `_fibonacci_evidence(technical_ctx: dict, price: float)` |
| 参数 | `technical_ctx`（dict）：运行上下文<br>`price`（float）：当前或待评估价格 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`fibonacci_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `technical_ctx.get` → `fib.get` → `row.get` → `distance_pct` → `items.append` → `EvidenceItem` → `round`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | technical_ctx.get、fib.get、float、row.get、distance_pct、items.append、EvidenceItem、round |
| 复杂度 / 风险 | 分支 2；跨度 28 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-30c0262d6e"></a>

#### FUN-30C0262D6E

| 设计项 | 说明 |
|---|---|
| 函数 | `_indicator_evidence` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L179` |
| 签名 | `_indicator_evidence(technical_ctx: dict)` |
| 参数 | `technical_ctx`（dict）：运行上下文 |
| 返回 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果 |
| 职责 | 构建`indicator_evidence`；返回 `tuple[Bias, list[EvidenceItem]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `technical_ctx.get` → `TF_WEIGHT.items` → `indicators.get` → `row.get` → `values.get` → `items.append` → `EvidenceItem` → `max`；包含 13 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | technical_ctx.get、TF_WEIGHT.items、indicators.get、row.get、values.get、items.append、EvidenceItem、max、float、round |
| 复杂度 / 风险 | 分支 13；跨度 83 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-efb2eb527e"></a>

#### FUN-EFB2EB527E

| 设计项 | 说明 |
|---|---|
| 函数 | `_quality_evidence` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L264` |
| 签名 | `_quality_evidence(technical_ctx: dict)` |
| 参数 | `technical_ctx`（dict）：运行上下文 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`quality_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `technical_ctx.get` → `quality.get` → `EvidenceItem` → `join` → `max` → `min`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | technical_ctx.get、float、quality.get、EvidenceItem、join、max、min |
| 复杂度 / 风险 | 分支 2；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0adaa6f91a"></a>

#### FUN-0ADAA6F91A

| 设计项 | 说明 |
|---|---|
| 函数 | `_support_resistance_evidence` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L280` |
| 签名 | `_support_resistance_evidence(technical_ctx: dict)` |
| 参数 | `technical_ctx`（dict）：运行上下文 |
| 返回 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果 |
| 职责 | 构建`support_resistance_evidence`；返回 `tuple[Bias, list[EvidenceItem]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `technical_ctx.get` → `sr.get` → `level.get` → `_level_price_text` → `min` → `max` → `abs` → `items.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[Bias, list[EvidenceItem]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | technical_ctx.get、sr.get、float、level.get、_level_price_text、min、max、abs、items.append、EvidenceItem |
| 复杂度 / 风险 | 分支 7；跨度 49 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-699a6c41bf"></a>

#### FUN-699A6C41BF

| 设计项 | 说明 |
|---|---|
| 函数 | `_level_price_text` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L331` |
| 签名 | `_level_price_text(level: dict)` |
| 参数 | `level`（dict）：候选价格水平 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`level_price_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `level.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、level.get |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5e5145e5af"></a>

#### FUN-5E5145E5AF

| 设计项 | 说明 |
|---|---|
| 函数 | `_pa_evidence` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L337` |
| 签名 | `_pa_evidence(technical_ctx: dict)` |
| 参数 | `technical_ctx`（dict）：运行上下文 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`pa_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `technical_ctx.get` → `pa.get` → `block.get` → `vp.get` → `items.append` → `EvidenceItem` → `lvl.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | technical_ctx.get、pa.get、block.get、vp.get、items.append、EvidenceItem、float、lvl.get |
| 复杂度 / 风险 | 分支 4；跨度 35 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-10ecc215f3"></a>

#### FUN-10ECC215F3

| 设计项 | 说明 |
|---|---|
| 函数 | `run_technical_analyst` |
| 源码位置 | [src/agents/analysts/technical.py](../../../src/agents/analysts/technical.py) · `L374` |
| 签名 | `run_technical_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 执行技术分析 Agent；可能影响外部接口；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_technical_context` → `fetch_evidence` → `MarketDataSource` → `_structure_bias` → `_ict_context_evidence` → `_fibonacci_evidence` → `_indicator_evidence` → `_support_resistance_evidence`；包含 14 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `AnalystReport` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_technical_context、fetch_evidence、MarketDataSource、_structure_bias、_ict_context_evidence、_fibonacci_evidence、_indicator_evidence、_support_resistance_evidence、_quality_evidence、_pa_evidence、ctx.enriched.get、ema_relation、sum、relations.values、relations.items、ema_items.append、EvidenceItem、sentiment_score、ict_zone_evidence、biases.append |
| 复杂度 / 风险 | 分支 14；跨度 105 行；高 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="unit-8933374b3e"></a>

### UNIT-8933374B3E

**模块**：`src/agents/bearish.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8933374B3E |
| 源码 | [src/agents/bearish.py](../../../src/agents/bearish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/bearish.py` 的职责，通过 `run_bearish_researcher` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) |
| 验证状态 | selected |

#### 函数导航

[_structure_items](#fun-c2054ace2c) · [run_bearish_researcher](#fun-63515361b0)

<a id="fun-c2054ace2c"></a>

#### FUN-C2054ACE2C

| 设计项 | 说明 |
|---|---|
| 函数 | `_structure_items` |
| 源码位置 | [src/agents/bearish.py](../../../src/agents/bearish.py) · `L12` |
| 签名 | `_structure_items(analyses: dict[str, TimeframeAnalysis])` |
| 参数 | `analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建结构条目集合；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_TF_WEIGHT.items` → `items.append` → `EvidenceItem`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _TF_WEIGHT.items、items.append、EvidenceItem |
| 复杂度 / 风险 | 分支 11；跨度 66 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-63515361b0"></a>

#### FUN-63515361B0

| 设计项 | 说明 |
|---|---|
| 函数 | `run_bearish_researcher` |
| 源码位置 | [src/agents/bearish.py](../../../src/agents/bearish.py) · `L80` |
| 签名 | `run_bearish_researcher(ctx: MarketContext, team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `AgentEvidence` 类型结果 |
| 职责 | 执行`bearish_researcher`；返回 `AgentEvidence` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_structure_items` → `items_for_direction` → `sum` → `max` → `AgentEvidence` → `min`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AgentEvidence` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _structure_items、items_for_direction、sum、max、len、AgentEvidence、min |
| 复杂度 / 风险 | 分支 2；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="unit-6008a95748"></a>

### UNIT-6008A95748

**模块**：`src/agents/bullish.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6008A95748 |
| 源码 | [src/agents/bullish.py](../../../src/agents/bullish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/bullish.py` 的职责，通过 `run_bullish_researcher` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) |
| 验证状态 | selected |

#### 函数导航

[_structure_items](#fun-3bd84eeb0a) · [run_bullish_researcher](#fun-87ec3ef32e)

<a id="fun-3bd84eeb0a"></a>

#### FUN-3BD84EEB0A

| 设计项 | 说明 |
|---|---|
| 函数 | `_structure_items` |
| 源码位置 | [src/agents/bullish.py](../../../src/agents/bullish.py) · `L12` |
| 签名 | `_structure_items(analyses: dict[str, TimeframeAnalysis])` |
| 参数 | `analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建结构条目集合；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_TF_WEIGHT.items` → `items.append` → `EvidenceItem`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _TF_WEIGHT.items、items.append、EvidenceItem |
| 复杂度 / 风险 | 分支 9；跨度 56 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-87ec3ef32e"></a>

#### FUN-87EC3EF32E

| 设计项 | 说明 |
|---|---|
| 函数 | `run_bullish_researcher` |
| 源码位置 | [src/agents/bullish.py](../../../src/agents/bullish.py) · `L70` |
| 签名 | `run_bullish_researcher(ctx: MarketContext, team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `AgentEvidence` 类型结果 |
| 职责 | 执行`bullish_researcher`；返回 `AgentEvidence` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_structure_items` → `items_for_direction` → `sum` → `max` → `AgentEvidence` → `min`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AgentEvidence` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _structure_items、items_for_direction、sum、max、len、AgentEvidence、min |
| 复杂度 / 风险 | 分支 2；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="unit-34bf03f815"></a>

### UNIT-34BF03F815

**模块**：`src/agents/debate.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-34BF03F815 |
| 源码 | [src/agents/debate.py](../../../src/agents/debate.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/debate.py` 的职责，通过 `run_debate` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_debate_coherence.py](../../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) |
| 验证状态 | selected |

#### 函数导航

[run_debate](#fun-29aa7948ff)

<a id="fun-29aa7948ff"></a>

#### FUN-29AA7948FF

| 设计项 | 说明 |
|---|---|
| 函数 | `run_debate` |
| 源码位置 | [src/agents/debate.py](../../../src/agents/debate.py) · `L16` |
| 签名 | `run_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses, team: AnalystTeam \| None=None, ctx: MarketContext \| None=None)` |
| 参数 | `bullish`（AgentEvidence）：看多证据或计数<br>`bearish`（AgentEvidence）：看空证据或计数<br>`analyses`（实现约定类型）：各时间框架分析结果<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None`<br>`ctx`（MarketContext \| None）：运行上下文；默认值 `None` |
| 返回 | 返回 `ResearchDebate` 类型结果 |
| 职责 | 执行`debate`；返回 `ResearchDebate` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `sentiment_score` → `sentiment.get` → `notes.append` → `get` → `getattr` → `strip` → `row.get`；包含 13 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ResearchDebate` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、len、sentiment_score、sentiment.get、notes.append、get、getattr、strip、row.get、abs、min、ResearchDebate |
| 复杂度 / 风险 | 分支 13；跨度 74 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_debate_coherence.py](../../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="unit-f23db48d75"></a>

### UNIT-F23DB48D75

**模块**：`src/agents/factory.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F23DB48D75 |
| 源码 | [src/agents/factory.py](../../../src/agents/factory.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/factory.py` 的职责，通过 `run_analyst_team`、`run_bullish`、`run_bearish`、`research_uses_parallel_llm`、`run_research_team`、`run_debate`、`run_level_proposer`、`run_trader` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 20 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_coherence.py](../../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_trader](#fun-c68a4cf1f3) | 执行`trader`；可能影响共享状态；返回实现分支产生的结果（源码未标注类型）。 | 共享状态变更 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |

#### 函数导航

[_use_llm_stage](#fun-5766bc355b) · [_pick_evidence](#fun-8bd56770da) · [_pick_analyst_report](#fun-69649a77ae) · [_analyst_team_aggregate_source](#fun-61f26f47e9) · [_use_llm_analyst](#fun-590a53a74c) · [_needs_rule_baseline](#fun-c7c1e6f330) · [_llm_stage_ok](#fun-27167e88c9) · [_ensure_rule_baseline](#fun-3e86d74ceb) · [run_analyst_team](#fun-e8a54418d1) · [run_bullish](#fun-7a4ecb2fc6) · [run_bearish](#fun-5113cb3027) · [research_uses_parallel_llm](#fun-91a30f1f5d) · [run_research_team](#fun-70aa2e8b05) · [_pick_debate](#fun-4f354a267b) · [run_debate](#fun-7599e6282b) · [run_level_proposer](#fun-682ee70c11) · [run_trader](#fun-c68a4cf1f3) · [run_risk](#fun-bab0b34f57) · [run_risk._gate](#fun-d6ed0e37d5) · [run_manager](#fun-60d80a7b70)

<a id="fun-5766bc355b"></a>

#### FUN-5766BC355B

| 设计项 | 说明 |
|---|---|
| 函数 | `_use_llm_stage` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L60` |
| 签名 | `_use_llm_stage(stage_enabled: bool)` |
| 参数 | `stage_enabled`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`use_llm_stage`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config` → `llm_configured` → `log.warning`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config、llm_configured、log.warning |
| 复杂度 / 风险 | 分支 3；跨度 9 行；低 |
| 测试 / 验证 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="fun-8bd56770da"></a>

#### FUN-8BD56770DA

| 设计项 | 说明 |
|---|---|
| 函数 | `_pick_evidence` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L71` |
| 签名 | `_pick_evidence(stage: str, rule_result: AgentEvidence, llm_result: AgentEvidence \| None, trace, pipeline: AgentPipelineMeta)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`rule_result`（AgentEvidence）：处理结果<br>`llm_result`（AgentEvidence \| None）：处理结果<br>`trace`（实现约定类型）：Agent 或流水线追踪记录<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果 |
| 返回 | 返回 `AgentEvidence` 类型结果 |
| 职责 | 生成`pick_evidence`结果；返回 `AgentEvidence` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config` → `pipeline.record` → `StageMeta`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AgentEvidence` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config、pipeline.record、StageMeta |
| 复杂度 / 风险 | 分支 5；跨度 30 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-69649a77ae"></a>

#### FUN-69649A77AE

| 设计项 | 说明 |
|---|---|
| 函数 | `_pick_analyst_report` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L103` |
| 签名 | `_pick_analyst_report(stage: str, rule_result: AnalystReport, llm_result: AnalystReport \| None, trace, pipeline: AgentPipelineMeta)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`rule_result`（AnalystReport）：处理结果<br>`llm_result`（AnalystReport \| None）：处理结果<br>`trace`（实现约定类型）：Agent 或流水线追踪记录<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果 |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 生成`pick_analyst_report`结果；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config` → `_use_llm_stage` → `pipeline.record` → `StageMeta`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystReport` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config、_use_llm_stage、pipeline.record、StageMeta |
| 复杂度 / 风险 | 分支 6；跨度 32 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-61f26f47e9"></a>

#### FUN-61F26F47E9

| 设计项 | 说明 |
|---|---|
| 函数 | `_analyst_team_aggregate_source` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L137` |
| 签名 | `_analyst_team_aggregate_source(llm_picked: int, total: int=4)` |
| 参数 | `llm_picked`（int）：由 `llm_picked` 表示的数值参数<br>`total`（int）：由 `total` 表示的数值参数；默认值 `4` |
| 返回 | 返回 `StageSource` 类型结果 |
| 职责 | 聚合`analyst_team_source`；返回 `StageSource` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `StageSource` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-590a53a74c"></a>

#### FUN-590A53A74C

| 设计项 | 说明 |
|---|---|
| 函数 | `_use_llm_analyst` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L145` |
| 签名 | `_use_llm_analyst(stage: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`use_llm_analyst`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c7c1e6f330"></a>

#### FUN-C7C1E6F330

| 设计项 | 说明 |
|---|---|
| 函数 | `_needs_rule_baseline` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L149` |
| 签名 | `_needs_rule_baseline()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`needs_rule_baseline`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-27167e88c9"></a>

#### FUN-27167E88C9

| 设计项 | 说明 |
|---|---|
| 函数 | `_llm_stage_ok` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L154` |
| 签名 | `_llm_stage_ok(llm_result, trace)` |
| 参数 | `llm_result`（实现约定类型）：处理结果<br>`trace`（实现约定类型）：Agent 或流水线追踪记录 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_stage_ok`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3e86d74ceb"></a>

#### FUN-3E86D74CEB

| 设计项 | 说明 |
|---|---|
| 函数 | `_ensure_rule_baseline` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L158` |
| 签名 | `_ensure_rule_baseline(rule_result, llm_result, trace, compute_rule)` |
| 参数 | `rule_result`（实现约定类型）：处理结果<br>`llm_result`（实现约定类型）：处理结果<br>`trace`（实现约定类型）：Agent 或流水线追踪记录<br>`compute_rule`（实现约定类型）：由调用方提供的 `compute_rule` 输入对象 |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 确保`rule_baseline`；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config` → `_llm_stage_ok` → `compute_rule`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config、_llm_stage_ok、compute_rule |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e8a54418d1"></a>

#### FUN-E8A54418D1

| 设计项 | 说明 |
|---|---|
| 函数 | `run_analyst_team` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L167` |
| 签名 | `run_analyst_team(ctx: MarketContext, pipeline: AgentPipelineMeta)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果 |
| 返回 | 返回 `AnalystTeam` 类型结果 |
| 职责 | 执行分析师团队结果；可能影响共享状态；返回 `AnalystTeam` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_progress` → `prog.update` → `time.perf_counter` → `_use_llm_stage` → `get_run_config` → `rule_analyst_team` → `_needs_rule_baseline` → `analyst_team_input_payload`；包含 22 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystTeam` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_progress、prog.update、time.perf_counter、_use_llm_stage、get_run_config、rule_analyst_team、_needs_rule_baseline、analyst_team_input_payload、int、prog.stage_io、json.dumps、rule_team.to_dict、pipeline.record、StageMeta、_use_llm_analyst、llm_tasks.append、len、run_parallel、fn、min |
| 复杂度 / 风险 | 分支 22；跨度 113 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="fun-7a4ecb2fc6"></a>

#### FUN-7A4ECB2FC6

| 设计项 | 说明 |
|---|---|
| 函数 | `run_bullish` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L282` |
| 签名 | `run_bullish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `AgentEvidence` 类型结果 |
| 职责 | 执行`bullish`；可能影响共享状态；返回 `AgentEvidence` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_use_llm_stage` → `get_run_config` → `rule_bullish` → `_needs_rule_baseline` → `update` → `get_progress` → `pipeline.record` → `StageMeta`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AgentEvidence` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _use_llm_stage、get_run_config、rule_bullish、_needs_rule_baseline、update、get_progress、pipeline.record、StageMeta、run_llm_bullish、_ensure_rule_baseline、_pick_evidence |
| 复杂度 / 风险 | 分支 3；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5113cb3027"></a>

#### FUN-5113CB3027

| 设计项 | 说明 |
|---|---|
| 函数 | `run_bearish` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L302` |
| 签名 | `run_bearish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `AgentEvidence` 类型结果 |
| 职责 | 执行`bearish`；可能影响共享状态；返回 `AgentEvidence` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_use_llm_stage` → `get_run_config` → `rule_bearish` → `_needs_rule_baseline` → `update` → `get_progress` → `pipeline.record` → `StageMeta`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AgentEvidence` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _use_llm_stage、get_run_config、rule_bearish、_needs_rule_baseline、update、get_progress、pipeline.record、StageMeta、run_llm_bearish、_ensure_rule_baseline、_pick_evidence |
| 复杂度 / 风险 | 分支 3；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-91a30f1f5d"></a>

#### FUN-91A30F1F5D

| 设计项 | 说明 |
|---|---|
| 函数 | `research_uses_parallel_llm` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L322` |
| 签名 | `research_uses_parallel_llm()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`research_uses_parallel_llm`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_use_llm_stage` → `get_run_config`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _use_llm_stage、get_run_config |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="fun-70aa2e8b05"></a>

#### FUN-70AA2E8B05

| 设计项 | 说明 |
|---|---|
| 函数 | `run_research_team` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L332` |
| 签名 | `run_research_team(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `tuple[AgentEvidence, AgentEvidence]` 类型结果 |
| 职责 | 执行`research_team`；返回 `tuple[AgentEvidence, AgentEvidence]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_use_llm_stage` → `get_run_config` → `rule_bullish` → `_needs_rule_baseline` → `rule_bearish` → `run_parallel` → `run_llm_bullish` → `run_llm_bearish`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AgentEvidence, AgentEvidence]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | RuntimeError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _use_llm_stage、get_run_config、rule_bullish、_needs_rule_baseline、rule_bearish、run_parallel、run_llm_bullish、run_llm_bearish、results.get、_ensure_rule_baseline、pipeline.record、StageMeta、_pick_evidence、RuntimeError |
| 复杂度 / 风险 | 分支 5；跨度 45 行；中 |
| 测试 / 验证 | [tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="fun-4f354a267b"></a>

#### FUN-4F354A267B

| 设计项 | 说明 |
|---|---|
| 函数 | `_pick_debate` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L379` |
| 签名 | `_pick_debate(rule_result: ResearchDebate, llm_result: ResearchDebate \| None, trace, pipeline: AgentPipelineMeta)` |
| 参数 | `rule_result`（ResearchDebate）：处理结果<br>`llm_result`（ResearchDebate \| None）：处理结果<br>`trace`（实现约定类型）：Agent 或流水线追踪记录<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果 |
| 返回 | 返回 `ResearchDebate` 类型结果 |
| 职责 | 生成`pick_debate`结果；返回 `ResearchDebate` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config` → `pipeline.record` → `StageMeta`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ResearchDebate` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config、pipeline.record、StageMeta |
| 复杂度 / 风险 | 分支 5；跨度 27 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7599e6282b"></a>

#### FUN-7599E6282B

| 设计项 | 说明 |
|---|---|
| 函数 | `run_debate` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L408` |
| 签名 | `run_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses, pipeline: AgentPipelineMeta, team: AnalystTeam, ctx: MarketContext)` |
| 参数 | `bullish`（AgentEvidence）：看多证据或计数<br>`bearish`（AgentEvidence）：看空证据或计数<br>`analyses`（实现约定类型）：各时间框架分析结果<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`team`（AnalystTeam）：分析团队结果<br>`ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `ResearchDebate` 类型结果 |
| 职责 | 执行`debate`；可能影响共享状态；返回 `ResearchDebate` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_use_llm_stage` → `get_run_config` → `update` → `get_progress` → `rule_debate` → `pipeline.record` → `StageMeta` → `_needs_rule_baseline`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ResearchDebate` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _use_llm_stage、get_run_config、update、get_progress、rule_debate、pipeline.record、StageMeta、_needs_rule_baseline、run_parallel、run_llm_debate、_pick_debate |
| 复杂度 / 风险 | 分支 3；跨度 34 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_debate_coherence.py](../../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-682ee70c11"></a>

#### FUN-682EE70C11

| 设计项 | 说明 |
|---|---|
| 函数 | `run_level_proposer` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L444` |
| 签名 | `run_level_proposer(ctx: MarketContext, team: AnalystTeam, debate: ResearchDebate, pipeline: AgentPipelineMeta, rule_signals: list[TradingSignal])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam）：分析团队结果<br>`debate`（ResearchDebate）：多角色辩论结果<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`rule_signals`（list[TradingSignal]）：交易信号集合 |
| 返回 | 返回 `list[LevelProposal]` 类型结果 |
| 职责 | 执行`level_proposer`；可能影响共享状态；返回 `list[LevelProposal]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_use_llm_stage` → `get_run_config` → `log.info` → `pipeline.record` → `StageMeta` → `update` → `get_progress` → `run_llm_level_proposer`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[LevelProposal]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _use_llm_stage、get_run_config、log.info、pipeline.record、StageMeta、update、get_progress、run_llm_level_proposer、len、log.warning |
| 复杂度 / 风险 | 分支 2；跨度 25 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-c68a4cf1f3"></a>

#### FUN-C68A4CF1F3

| 设计项 | 说明 |
|---|---|
| 函数 | `run_trader` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L471` |
| 签名 | `run_trader(ctx: MarketContext, debate: ResearchDebate, pipeline: AgentPipelineMeta, signals: list[TradingSignal], team: AnalystTeam \| None=None, *, observation_mode: bool=False)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`signals`（list[TradingSignal]）：交易信号集合<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None`<br>`observation_mode`（bool）：观察模式开关或策略；默认值 `False` |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 执行`trader`；可能影响共享状态；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `rule_trader` → `_use_llm_stage` → `get_run_config` → `update` → `get_progress` → `pipeline.record` → `StageMeta` → `run_llm_trader`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rule_trader、_use_llm_stage、get_run_config、update、get_progress、pipeline.record、StageMeta、run_llm_trader |
| 复杂度 / 风险 | 分支 4；跨度 33 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-bab0b34f57"></a>

#### FUN-BAB0B34F57

| 设计项 | 说明 |
|---|---|
| 函数 | `run_risk` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L506` |
| 签名 | `run_risk(proposal: TransactionProposal, signals: list, pipeline: AgentPipelineMeta, *, current_price: float=0.0, data_as_of: dict \| None=None, observation_mode: bool=False)` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`signals`（list）：交易信号集合<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果<br>`current_price`（float）：当前市场价格；默认值 `0.0`<br>`data_as_of`（dict \| None）：数据截止时间；默认值 `None`<br>`observation_mode`（bool）：观察模式开关或策略；默认值 `False` |
| 返回 | 返回 `list[RiskReview]` 类型结果 |
| 职责 | 执行风险结果；可能影响共享状态；返回 `list[RiskReview]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `apply_risk_gates` → `rule_risk` → `_use_llm_stage` → `get_run_config` → `update` → `get_progress` → `pipeline.record` → `StageMeta`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[RiskReview]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | apply_risk_gates、rule_risk、len、_use_llm_stage、get_run_config、update、get_progress、pipeline.record、StageMeta、run_llm_risk、_gate |
| 复杂度 / 风险 | 分支 4；跨度 56 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-d6ed0e37d5"></a>

#### FUN-D6ED0E37D5

| 设计项 | 说明 |
|---|---|
| 函数 | `run_risk._gate` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L515` |
| 签名 | `run_risk._gate(reviews: list[RiskReview])` |
| 参数 | `reviews`（list[RiskReview]）：风险或评审结果集合 |
| 返回 | 返回 `list[RiskReview]` 类型结果 |
| 职责 | 构建`gate`；返回 `list[RiskReview]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `apply_risk_gates`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[RiskReview]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | apply_risk_gates |
| 复杂度 / 风险 | 分支 0；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-60d80a7b70"></a>

#### FUN-60D80A7B70

| 设计项 | 说明 |
|---|---|
| 函数 | `run_manager` |
| 源码位置 | [src/agents/factory.py](../../../src/agents/factory.py) · `L564` |
| 签名 | `run_manager(proposal: TransactionProposal, reviews: list[RiskReview], pipeline: AgentPipelineMeta)` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`reviews`（list[RiskReview]）：风险或评审结果集合<br>`pipeline`（AgentPipelineMeta）：流水线对象或结果 |
| 返回 | 返回 `ManagerDecision` 类型结果 |
| 职责 | 执行管理 Agent 决策；可能影响共享状态；返回 `ManagerDecision` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rule_manager` → `_use_llm_stage` → `get_run_config` → `update` → `get_progress` → `pipeline.record` → `StageMeta` → `run_llm_manager`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ManagerDecision` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rule_manager、_use_llm_stage、get_run_config、update、get_progress、pipeline.record、StageMeta、run_llm_manager |
| 复杂度 / 风险 | 分支 4；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) · 直接动态测试 |

<a id="unit-1606bdc6e2"></a>

### UNIT-1606BDC6E2

**模块**：`src/agents/llm/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1606BDC6E2 |
| 源码 | [src/agents/llm/__init__.py](../../../src/agents/llm/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3eeb009803"></a>

### UNIT-3EEB009803

**模块**：`src/agents/llm/base.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3EEB009803 |
| 源码 | [src/agents/llm/base.py](../../../src/agents/llm/base.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/base.py` 的职责，通过 `stream_llm_json`、`run_llm_stage` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 5 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_llm_json.py](../../../tests/unit/test_llm_json.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_llm_stage](#fun-ddb9984fe6) | 执行`llm_stage`；可能影响共享状态；返回 `tuple[T \| None, LLMStageTrace]` 类型结果。 | 共享状态变更 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) |

#### 函数导航

[_backoff_seconds](#fun-e3963880ea) · [_parse_llm_json](#fun-b6641135ba) · [_stream_once](#fun-6474c56d9a) · [stream_llm_json](#fun-79e9f3d3c1) · [run_llm_stage](#fun-ddb9984fe6)

<a id="fun-e3963880ea"></a>

#### FUN-E3963880EA

| 设计项 | 说明 |
|---|---|
| 函数 | `_backoff_seconds` |
| 源码位置 | [src/agents/llm/base.py](../../../src/agents/llm/base.py) · `L30` |
| 签名 | `_backoff_seconds(attempt: int)` |
| 参数 | `attempt`（int）：由 `attempt` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`backoff_seconds`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b6641135ba"></a>

#### FUN-B6641135BA

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_llm_json` |
| 源码位置 | [src/agents/llm/base.py](../../../src/agents/llm/base.py) · `L36` |
| 签名 | `_parse_llm_json(raw: str)` |
| 参数 | `raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 解析`llm_json`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `raw.strip` → `json.JSONDecodeError` → `text.find` → `text.rfind` → `attempts.append` → `re.sub` → `json.loads` → `isinstance`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError；json.JSONDecodeError；last_err |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | raw.strip、json.JSONDecodeError、text.find、text.rfind、attempts.append、list、re.sub、json.loads、isinstance、ValueError |
| 复杂度 / 风险 | 分支 6；跨度 27 行；低 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_llm_json.py](../../../tests/unit/test_llm_json.py) · 直接动态测试 |

<a id="fun-6474c56d9a"></a>

#### FUN-6474C56D9A

| 设计项 | 说明 |
|---|---|
| 函数 | `_stream_once` |
| 源码位置 | [src/agents/llm/base.py](../../../src/agents/llm/base.py) · `L65` |
| 签名 | `_stream_once(client: LLMClient, messages: list[dict[str, str]], *, stage: str, temperature: float)` |
| 参数 | `client`（LLMClient）：外部服务客户端<br>`messages`（list[dict[str, str]]）：消息序列<br>`stage`（str）：流水线或 Agent 阶段标识<br>`temperature`（float）：模型采样温度 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stream_once`文本；可能影响共享状态；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_progress` → `prog.run_llm_stream` → `client.chat_stream`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_progress、prog.run_llm_stream、client.chat_stream |
| 复杂度 / 风险 | 分支 0；跨度 17 行；低 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) · 直接动态测试 |

<a id="fun-79e9f3d3c1"></a>

#### FUN-79E9F3D3C1

| 设计项 | 说明 |
|---|---|
| 函数 | `stream_llm_json` |
| 源码位置 | [src/agents/llm/base.py](../../../src/agents/llm/base.py) · `L84` |
| 签名 | `stream_llm_json(client: LLMClient, messages: list[dict[str, str]], *, stage: str, temperature: float=0.2, max_attempts: int \| None=None)` |
| 参数 | `client`（LLMClient）：外部服务客户端<br>`messages`（list[dict[str, str]]）：消息序列<br>`stage`（str）：流水线或 Agent 阶段标识<br>`temperature`（float）：模型采样温度；默认值 `0.2`<br>`max_attempts`（int \| None）：由调用方提供的 `max_attempts` 输入对象；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stream_llm_json`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_stage_policy` → `max` → `range` → `min` → `_stream_once` → `_backoff_seconds` → `log.warning` → `time.sleep`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | last_exc |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_stage_policy、max、int、range、min、_stream_once、_backoff_seconds、log.warning、time.sleep |
| 复杂度 / 风险 | 分支 5；跨度 39 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) · 直接动态测试 |

<a id="fun-ddb9984fe6"></a>

#### FUN-DDB9984FE6

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_stage` |
| 源码位置 | [src/agents/llm/base.py](../../../src/agents/llm/base.py) · `L125` |
| 签名 | `run_llm_stage(*, stage: str, model: str, client: LLMClient, messages: list[dict[str, str]], parse: Callable[[dict[str, Any]], T], temperature: float=0.2)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`model`（str）：模型名称或模型对象<br>`client`（LLMClient）：外部服务客户端<br>`messages`（list[dict[str, str]]）：消息序列<br>`parse`（Callable[[dict[str, Any]], T]）：调用方提供的回调函数<br>`temperature`（float）：模型采样温度；默认值 `0.2` |
| 返回 | 返回 `tuple[T \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_stage`；可能影响共享状态；返回 `tuple[T \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_stage_policy` → `build_routing_strategy` → `apply_input_budget` → `log.warning` → `budget_meta.get` → `get_progress` → `routing.get` → `prog.llm_begin`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[T \| None, LLMStageTrace]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_stage_policy、build_routing_strategy、apply_input_budget、log.warning、budget_meta.get、get_progress、routing.get、prog.llm_begin、time.perf_counter、range、min、_stream_once、_parse_llm_json、parse、int、estimate_text_size、prog.llm_end、log.info、LLMStageTrace、bool |
| 复杂度 / 风险 | 分支 9；跨度 189 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="unit-3a49bda3a6"></a>

### UNIT-3A49BDA3A6

**模块**：`src/agents/llm/payload.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3A49BDA3A6 |
| 源码 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/payload.py` 的职责，通过 `technical_level_reactions_payload`、`analyst_team_payload`、`analyst_team_summaries_payload`、`analyst_team_input_payload`、`market_payload`、`research_payload`、`technical_analyst_payload`、`fundamentals_analyst_payload` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 25 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_legacy_trader_payload](#fun-992d8a594f) | 构建`legacy_trader_payload`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | — |
| [trader_decision_payload](#fun-8ce195cdf3) | 构建`trader_decision_payload`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) |
| [trader_payload](#fun-aac9fbd67b) | 构建`trader_payload`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) |

#### 函数导航

[_tf_block](#fun-2aeed14a2e) · [_structure_vote](#fun-f3d598c89c) · [_timeframe_trends](#fun-eaa77ee71a) · [_event_risk_block](#fun-6d3cf52f12) · [technical_level_reactions_payload](#fun-c677217758) · [analyst_team_payload](#fun-6c3bfd3baa) · [analyst_team_summaries_payload](#fun-a152bbc0e8) · [analyst_team_input_payload](#fun-6749b95a24) · [_fibonacci_block](#fun-293475f5a3) · [market_payload](#fun-3c9a11e1b3) · [research_payload](#fun-fddf16b339) · [technical_analyst_payload](#fun-081944e744) · [fundamentals_analyst_payload](#fun-f93a6b184d) · [news_analyst_payload](#fun-3fc60de348) · [sentiment_analyst_payload](#fun-e83e383708) · [debate_payload](#fun-3e594bc0fa) · [evidence_payload](#fun-8646951a9c) · [_signal_payload](#fun-35a12d35f4) · [signal_list_payload](#fun-256c7b349e) · [_legacy_trader_payload](#fun-992d8a594f) · [trader_decision_payload](#fun-8ce195cdf3) · [trader_payload](#fun-aac9fbd67b) · [risk_payload](#fun-f44f676424) · [manager_payload](#fun-63914db325) · [level_proposer_payload](#fun-c4847806bf)

<a id="fun-2aeed14a2e"></a>

#### FUN-2AEED14A2E

| 设计项 | 说明 |
|---|---|
| 函数 | `_tf_block` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L34` |
| 签名 | `_tf_block(tf: str, analysis: TimeframeAnalysis, *, price: float)` |
| 参数 | `tf`（str）：时间框架简称<br>`analysis`（TimeframeAnalysis）：当前分析结果<br>`price`（float）：当前或待评估价格 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`tf_block`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `timeframe_context`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | timeframe_context |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f3d598c89c"></a>

#### FUN-F3D598C89C

| 设计项 | 说明 |
|---|---|
| 函数 | `_structure_vote` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L38` |
| 签名 | `_structure_vote(analyses)` |
| 参数 | `analyses`（实现约定类型）：各时间框架分析结果 |
| 返回 | 返回 `dict[str, float]` 类型结果 |
| 职责 | 构建`structure_vote`；返回 `dict[str, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment_score`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment_score |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-eaa77ee71a"></a>

#### FUN-EAA77EE71A

| 设计项 | 说明 |
|---|---|
| 函数 | `_timeframe_trends` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L42` |
| 签名 | `_timeframe_trends(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`timeframe_trends`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6d3cf52f12"></a>

#### FUN-6D3CF52F12

| 设计项 | 说明 |
|---|---|
| 函数 | `_event_risk_block` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L48` |
| 签名 | `_event_risk_block(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`event_risk_block`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.derived.get` → `min`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ctx.derived.get、min |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c677217758"></a>

#### FUN-C677217758

| 设计项 | 说明 |
|---|---|
| 函数 | `technical_level_reactions_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L57` |
| 签名 | `technical_level_reactions_payload(team: AnalystTeam)` |
| 参数 | `team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`technical_level_reactions_payload`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.refs.get` → `round` → `recovered.append` → `strip`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、item.refs.get、round、float、recovered.append、strip、str |
| 复杂度 / 风险 | 分支 5；跨度 28 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6c3bfd3baa"></a>

#### FUN-6C3BFD3BAA

| 设计项 | 说明 |
|---|---|
| 函数 | `analyst_team_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L87` |
| 签名 | `analyst_team_payload(team: AnalystTeam)` |
| 参数 | `team`（AnalystTeam）：分析团队结果 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`analyst_team_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `sorted`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、sorted、list |
| 复杂度 / 风险 | 分支 2；跨度 25 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a152bbc0e8"></a>

#### FUN-A152BBC0E8

| 设计项 | 说明 |
|---|---|
| 函数 | `analyst_team_summaries_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L114` |
| 签名 | `analyst_team_summaries_payload(team: AnalystTeam, *, top_items: int=0)` |
| 参数 | `team`（AnalystTeam）：分析团队结果<br>`top_items`（int）：输入项集合；默认值 `0` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`analyst_team_summaries_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `sorted`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、sorted |
| 复杂度 / 风险 | 分支 2；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6749b95a24"></a>

#### FUN-6749B95A24

| 设计项 | 说明 |
|---|---|
| 函数 | `analyst_team_input_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L139` |
| 签名 | `analyst_team_input_payload(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`analyst_team_input_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `technical_analyst_payload` → `fundamentals_analyst_payload` → `news_analyst_payload` → `sentiment_analyst_payload`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | technical_analyst_payload、fundamentals_analyst_payload、news_analyst_payload、sentiment_analyst_payload |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-293475f5a3"></a>

#### FUN-293475F5A3

| 设计项 | 说明 |
|---|---|
| 函数 | `_fibonacci_block` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L150` |
| 签名 | `_fibonacci_block(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`fibonacci_block`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fibonacci_context`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fibonacci_context |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3c9a11e1b3"></a>

#### FUN-3C9A11E1B3

| 设计项 | 说明 |
|---|---|
| 函数 | `market_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L155` |
| 签名 | `market_payload(ctx: MarketContext, team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`market_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.external.to_dict` → `_tf_block` → `analyst_team_payload`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ctx.external.to_dict、_tf_block、analyst_team_payload |
| 复杂度 / 风险 | 分支 1；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fddf16b339"></a>

#### FUN-FDDF16B339

| 设计项 | 说明 |
|---|---|
| 函数 | `research_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L176` |
| 签名 | `research_payload(ctx: MarketContext, team: AnalystTeam, direction: str)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam）：分析团队结果<br>`direction`（str）：交易方向 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`research_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `analyst_evidence_ids` → `market_payload` → `analyst_team_payload` → `_structure_vote` → `_timeframe_trends` → `_event_risk_block`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、analyst_evidence_ids、market_payload、analyst_team_payload、_structure_vote、_timeframe_trends、_event_risk_block |
| 复杂度 / 风险 | 分支 1；跨度 19 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-081944e744"></a>

#### FUN-081944E744

| 设计项 | 说明 |
|---|---|
| 函数 | `technical_analyst_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L197` |
| 签名 | `technical_analyst_payload(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`technical_analyst_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ema_relation` → `build_technical_context` → `base.get` → `build_pa_llm_summary` → `technical_claim_fact_catalog` → `ctx.derived.get` → `_fibonacci_block` → `ctx.context_stats.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ema_relation、build_technical_context、base.get、build_pa_llm_summary、technical_claim_fact_catalog、ctx.derived.get、_fibonacci_block、ctx.context_stats.get |
| 复杂度 / 风险 | 分支 3；跨度 30 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-f93a6b184d"></a>

#### FUN-F93A6B184D

| 设计项 | 说明 |
|---|---|
| 函数 | `fundamentals_analyst_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L229` |
| 签名 | `fundamentals_analyst_payload(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`fundamentals_analyst_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `m.to_dict` → `ctx.derived.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | m.to_dict、ctx.derived.get |
| 复杂度 / 风险 | 分支 1；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) · 直接动态测试 |

<a id="fun-3fc60de348"></a>

#### FUN-3FC60DE348

| 设计项 | 说明 |
|---|---|
| 函数 | `news_analyst_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L244` |
| 签名 | `news_analyst_payload(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`news_analyst_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ext.to_dict` → `ext_dict.get` → `ctx.derived.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ext.to_dict、ext_dict.get、ctx.derived.get、len |
| 复杂度 / 风险 | 分支 1；跨度 40 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-e83e383708"></a>

#### FUN-E83E383708

| 设计项 | 说明 |
|---|---|
| 函数 | `sentiment_analyst_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L286` |
| 签名 | `sentiment_analyst_payload(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`sentiment_analyst_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment_score`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment_score |
| 复杂度 / 风险 | 分支 0；跨度 12 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-3e594bc0fa"></a>

#### FUN-3E594BC0FA

| 设计项 | 说明 |
|---|---|
| 函数 | `debate_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L300` |
| 签名 | `debate_payload(bullish: AgentEvidence, bearish: AgentEvidence, analyses, *, ctx: MarketContext \| None=None, team: AnalystTeam \| None=None)` |
| 参数 | `bullish`（AgentEvidence）：看多证据或计数<br>`bearish`（AgentEvidence）：看空证据或计数<br>`analyses`（实现约定类型）：各时间框架分析结果<br>`ctx`（MarketContext \| None）：运行上下文；默认值 `None`<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`debate_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `evidence_payload` → `sentiment_score` → `_event_risk_block` → `ctx.derived.get` → `analyst_team_summaries_payload` → `getattr`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | evidence_payload、sentiment_score、_event_risk_block、ctx.derived.get、analyst_team_summaries_payload、getattr |
| 复杂度 / 风险 | 分支 4；跨度 38 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-8646951a9c"></a>

#### FUN-8646951A9C

| 设计项 | 说明 |
|---|---|
| 函数 | `evidence_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L340` |
| 签名 | `evidence_payload(evidence: AgentEvidence)` |
| 参数 | `evidence`（AgentEvidence）：由调用方提供的 `evidence` 输入对象 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`evidence_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted |
| 复杂度 / 风险 | 分支 0；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-35a12d35f4"></a>

#### FUN-35A12D35F4

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L361` |
| 签名 | `_signal_payload(signal: Any)` |
| 参数 | `signal`（Any）：当前交易信号 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`signal_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr |
| 复杂度 / 风险 | 分支 0；跨度 15 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-256c7b349e"></a>

#### FUN-256C7B349E

| 设计项 | 说明 |
|---|---|
| 函数 | `signal_list_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L378` |
| 签名 | `signal_list_payload(signals: list[Any])` |
| 参数 | `signals`（list[Any]）：交易信号集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`signal_list_payload`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_signal_payload` → `enumerate`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _signal_payload、enumerate |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-992d8a594f"></a>

#### FUN-992D8A594F

| 设计项 | 说明 |
|---|---|
| 函数 | `_legacy_trader_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L385` |
| 签名 | `_legacy_trader_payload(ctx: MarketContext, debate: ResearchDebate, signals: list[Any])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`signals`（list[Any]）：交易信号集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`legacy_trader_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `market_payload` → `signal_list_payload`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | market_payload、signal_list_payload |
| 复杂度 / 风险 | 分支 0；跨度 19 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8ce195cdf3"></a>

#### FUN-8CE195CDF3

| 设计项 | 说明 |
|---|---|
| 函数 | `trader_decision_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L406` |
| 签名 | `trader_decision_payload(ctx: MarketContext, debate: ResearchDebate, team: AnalystTeam, signals: list[Any])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`team`（AnalystTeam）：分析团队结果<br>`signals`（list[Any]）：交易信号集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`trader_decision_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `analyst_team_summaries_payload` → `_structure_vote` → `signal_list_payload`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | analyst_team_summaries_payload、_structure_vote、signal_list_payload |
| 复杂度 / 风险 | 分支 0；跨度 26 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-aac9fbd67b"></a>

#### FUN-AAC9FBD67B

| 设计项 | 说明 |
|---|---|
| 函数 | `trader_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L434` |
| 签名 | `trader_payload(ctx: MarketContext, debate: ResearchDebate, signals: list[Any], team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`signals`（list[Any]）：交易信号集合<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`trader_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `trader_decision_payload` → `_legacy_trader_payload`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | trader_decision_payload、_legacy_trader_payload |
| 复杂度 / 风险 | 分支 1；跨度 9 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-f44f676424"></a>

#### FUN-F44F676424

| 设计项 | 说明 |
|---|---|
| 函数 | `risk_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L445` |
| 签名 | `risk_payload(proposal: TransactionProposal, signal_count: int, *, signals: list[Any] \| None=None, current_price: float \| None=None, data_as_of: dict[str, Any] \| None=None)` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`signal_count`（int）：信号数量<br>`signals`（list[Any] \| None）：交易信号集合；默认值 `None`<br>`current_price`（float \| None）：当前市场价格；默认值 `None`<br>`data_as_of`（dict[str, Any] \| None）：数据截止时间；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`risk_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `sig.get` → `_signal_payload` → `row.get` → `round` → `selected.append` → `proposal.to_dict`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、isinstance、sig.get、_signal_payload、row.get、float、round、selected.append、proposal.to_dict |
| 复杂度 / 风险 | 分支 4；跨度 49 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-63914db325"></a>

#### FUN-63914DB325

| 设计项 | 说明 |
|---|---|
| 函数 | `manager_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L496` |
| 签名 | `manager_payload(proposal: TransactionProposal, reviews: list[RiskReview])` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`reviews`（list[RiskReview]）：风险或评审结果集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`manager_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `proposal.to_dict` → `r.to_dict`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | proposal.to_dict、r.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 15 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="fun-c4847806bf"></a>

#### FUN-C4847806BF

| 设计项 | 说明 |
|---|---|
| 函数 | `level_proposer_payload` |
| 源码位置 | [src/agents/llm/payload.py](../../../src/agents/llm/payload.py) · `L513` |
| 签名 | `level_proposer_payload(ctx: MarketContext, team: AnalystTeam, debate: ResearchDebate, rule_signals: list[Any])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam）：分析团队结果<br>`debate`（ResearchDebate）：多角色辩论结果<br>`rule_signals`（list[Any]）：交易信号集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`level_proposer_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_technical_context` → `technical_level_reactions_payload` → `technical_claim_fact_catalog` → `structure.get` → `analyst_team_payload` → `build_pa_llm_summary` → `_signal_payload` → `market_payload`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_technical_context、technical_level_reactions_payload、technical_claim_fact_catalog、structure.get、analyst_team_payload、build_pa_llm_summary、_signal_payload、market_payload |
| 复杂度 / 风险 | 分支 1；跨度 70 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py) · 直接动态测试 |

<a id="unit-9b539edeb6"></a>

### UNIT-9B539EDEB6

**模块**：`src/agents/llm/schemas.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9B539EDEB6 |
| 源码 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/schemas.py` 的职责，通过 `parse_analyst_report`、`parse_agent_evidence`、`parse_research_debate`、`parse_level_proposals`、`parse_transaction_proposal`、`parse_risk_reviews`、`parse_manager_decision` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 18 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[_item_refs](#fun-8ec477c06b) · [_clamp_strength](#fun-330aae4a56) · [_string_list](#fun-352076cbe7) · [_index_list](#fun-fefe6cd472) · [_float_field](#fun-d4331ef421) · [_parse_level_reactions](#fun-abc4913591) · [_level_reactions_from_items](#fun-16c25d76d9) · [_merge_level_reactions_into_items](#fun-1aa683b3a6) · [parse_analyst_report](#fun-bb1277c4f9) · [parse_agent_evidence](#fun-5a54aee754) · [parse_research_debate](#fun-c7499346d6) · [_compose_level_deduction_reason](#fun-3f721baec4) · [_level_deduction_quality](#fun-548d3233a2) · [parse_level_proposals](#fun-28618f8314) · [_validate_level_path_contract](#fun-866b1d79aa) · [parse_transaction_proposal](#fun-1cf0104153) · [parse_risk_reviews](#fun-616d649c39) · [parse_manager_decision](#fun-675d6fb6d6)

<a id="fun-8ec477c06b"></a>

#### FUN-8EC477C06B

| 设计项 | 说明 |
|---|---|
| 函数 | `_item_refs` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L33` |
| 签名 | `_item_refs(row: dict[str, Any], category: str)` |
| 参数 | `row`（dict[str, Any]）：当前记录行<br>`category`（str）：由 `category` 表示的文本或标识 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`item_refs`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get` → `isinstance` → `refs.get` → `_DEFAULT_ITEM_SOURCE.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | row.get、isinstance、refs.get、str、_DEFAULT_ITEM_SOURCE.get |
| 复杂度 / 风险 | 分支 4；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-330aae4a56"></a>

#### FUN-330AAE4A56

| 设计项 | 说明 |
|---|---|
| 函数 | `_clamp_strength` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L46` |
| 签名 | `_clamp_strength(v: Any)` |
| 参数 | `v`（Any）：由调用方提供的 `v` 输入对象 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`clamp_strength`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、max、min |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-352076cbe7"></a>

#### FUN-352076CBE7

| 设计项 | 说明 |
|---|---|
| 函数 | `_string_list` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L54` |
| 签名 | `_string_list(value: Any, *, fallback: list[str] \| None=None, limit: int=8)` |
| 参数 | `value`（Any）：待处理值<br>`fallback`（list[str] \| None）：由 `fallback` 表示的输入集合；默认值 `None`<br>`limit`（int）：返回或处理数量上限；默认值 `8` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`string_list`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `strip`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、strip、str |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fefe6cd472"></a>

#### FUN-FEFE6CD472

| 设计项 | 说明 |
|---|---|
| 函数 | `_index_list` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L64` |
| 签名 | `_index_list(value: Any, *, allowed: set[int])` |
| 参数 | `value`（Any）：待处理值<br>`allowed`（set[int]）：由 `allowed` 表示的输入集合 |
| 返回 | 返回 `list[int]` 类型结果 |
| 职责 | 构建`index_list`；返回 `list[int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `out.append`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、int、out.append |
| 复杂度 / 风险 | 分支 4；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d4331ef421"></a>

#### FUN-D4331EF421

| 设计项 | 说明 |
|---|---|
| 函数 | `_float_field` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L78` |
| 签名 | `_float_field(row: dict[str, Any], name: str)` |
| 参数 | `row`（dict[str, Any]）：当前记录行<br>`name`（str）：对象名称 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`float_field`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ValueError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、ValueError |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-abc4913591"></a>

#### FUN-ABC4913591

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_level_reactions` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L85` |
| 签名 | `_parse_level_reactions(data: dict[str, Any], *, agent: str)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`agent`（str）：Agent 实例或标识 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 解析`level_reactions`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.get` → `isinstance` → `enumerate` → `strip` → `row.get` → `round` → `lower` → `relation.get`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.get、isinstance、enumerate、strip、str、row.get、round、float、lower、relation.get、relationships.append、out.append、_clamp_strength、sorted、set |
| 复杂度 / 风险 | 分支 9；跨度 63 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-16c25d76d9"></a>

#### FUN-16C25D76D9

| 设计项 | 说明 |
|---|---|
| 函数 | `_level_reactions_from_items` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L150` |
| 签名 | `_level_reactions_from_items(items: list[EvidenceItem])` |
| 参数 | `items`（list[EvidenceItem]）：输入项集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 根据`items`构建`level_reactions`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.refs.get` → `round` → `recovered.append` → `strip`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | item.refs.get、round、float、recovered.append、strip、str、list |
| 复杂度 / 风险 | 分支 4；跨度 24 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1aa683b3a6"></a>

#### FUN-1AA683B3A6

| 设计项 | 说明 |
|---|---|
| 函数 | `_merge_level_reactions_into_items` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L176` |
| 签名 | `_merge_level_reactions_into_items(items: list[EvidenceItem], reactions: list[dict[str, Any]], *, agent: str)` |
| 参数 | `items`（list[EvidenceItem]）：输入项集合<br>`reactions`（list[dict[str, Any]]）：由 `reactions` 表示的输入集合<br>`agent`（str）：Agent 实例或标识 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 合并`level_reactions_into_items`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `enumerate` → `strip` → `row.get` → `merged.append` → `EvidenceItem` → `isinstance` → `existing_ids.add`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、enumerate、strip、str、row.get、merged.append、EvidenceItem、float、isinstance、existing_ids.add |
| 复杂度 / 风险 | 分支 6；跨度 41 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-bb1277c4f9"></a>

#### FUN-BB1277C4F9

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_analyst_report` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L219` |
| 签名 | `parse_analyst_report(data: dict[str, Any], *, agent: str)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`agent`（str）：Agent 实例或标识 |
| 返回 | 返回 `AnalystReport` 类型结果 |
| 职责 | 解析`analyst_report`；返回 `AnalystReport` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `data.get` → `isinstance` → `enumerate` → `strip` → `row.get` → `_item_refs` → `items.append`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AnalystReport` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、data.get、isinstance、enumerate、strip、row.get、_item_refs、items.append、EvidenceItem、_clamp_strength、_parse_level_reactions、_level_reactions_from_items、len、ValueError、_merge_level_reactions_into_items、AnalystReport |
| 复杂度 / 风险 | 分支 11；跨度 57 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) · 直接动态测试 |

<a id="fun-5a54aee754"></a>

#### FUN-5A54AEE754

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_agent_evidence` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L278` |
| 签名 | `parse_agent_evidence(data: dict[str, Any], *, agent: str, direction: Bias, allowed_evidence_ids: set[str] \| None=None, evidence_registry: dict[str, EvidenceItem] \| None=None)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`agent`（str）：Agent 实例或标识<br>`direction`（Bias）：交易方向<br>`allowed_evidence_ids`（set[str] \| None）：由 `allowed_evidence_ids` 表示的输入集合；默认值 `None`<br>`evidence_registry`（dict[str, EvidenceItem] \| None）：事实或证据登记映射；默认值 `None` |
| 返回 | 返回 `AgentEvidence` 类型结果 |
| 职责 | 解析`agent_evidence`；返回 `AgentEvidence` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.get` → `_clamp_strength` → `strip` → `isinstance` → `ValueError` → `parse_research_items` → `build_research_provenance_meta` → `blend_research_confidence`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AgentEvidence` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.get、_clamp_strength、strip、str、isinstance、ValueError、parse_research_items、build_research_provenance_meta、blend_research_confidence、enumerate、row.get、_item_refs、items.append、EvidenceItem、set、len、AgentEvidence |
| 复杂度 / 风险 | 分支 7；跨度 76 行；中 |
| 测试 / 验证 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py) · 直接动态测试 |

<a id="fun-c7499346d6"></a>

#### FUN-C7499346D6

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_research_debate` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L356` |
| 签名 | `parse_research_debate(data: dict[str, Any], *, bullish: AgentEvidence, bearish: AgentEvidence)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`bullish`（AgentEvidence）：看多证据或计数<br>`bearish`（AgentEvidence）：看空证据或计数 |
| 返回 | 返回 `ResearchDebate` 类型结果 |
| 职责 | 解析`research_debate`；返回 `ResearchDebate` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `data.get` → `_clamp_strength` → `build_debate_provenance_meta` → `blend_debate_consensus` → `round` → `isinstance` → `strip`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ResearchDebate` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、data.get、_clamp_strength、build_debate_provenance_meta、blend_debate_consensus、round、isinstance、strip、notes.append、ResearchDebate |
| 复杂度 / 风险 | 分支 4；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py) · 直接动态测试 |

<a id="fun-3f721baec4"></a>

#### FUN-3F721BAEC4

| 设计项 | 说明 |
|---|---|
| 函数 | `_compose_level_deduction_reason` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L405` |
| 签名 | `_compose_level_deduction_reason(*, anchor_level: str, expected_reaction: str, deduction: str, reason: str)` |
| 参数 | `anchor_level`（str）：候选价格水平<br>`expected_reaction`（str）：由 `expected_reaction` 表示的文本或标识<br>`deduction`（str）：由 `deduction` 表示的文本或标识<br>`reason`（str）：判定或拒绝原因 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`compose_level_deduction_reason`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parts.append` → `join`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | parts.append、join |
| 复杂度 / 风险 | 分支 5；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-548d3233a2"></a>

#### FUN-548D3233A2

| 设计项 | 说明 |
|---|---|
| 函数 | `_level_deduction_quality` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L425` |
| 签名 | `_level_deduction_quality(*, anchor_level: str, expected_reaction: str, deduction: str, reason: str, reaction_evidence_id: str)` |
| 参数 | `anchor_level`（str）：候选价格水平<br>`expected_reaction`（str）：由 `expected_reaction` 表示的文本或标识<br>`deduction`（str）：由 `deduction` 表示的文本或标识<br>`reason`（str）：判定或拒绝原因<br>`reaction_evidence_id`（str）：对象标识 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`level_deduction_quality`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、len |
| 复杂度 / 风险 | 分支 3；跨度 17 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-28618f8314"></a>

#### FUN-28618F8314

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_level_proposals` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L444` |
| 签名 | `parse_level_proposals(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `list[LevelProposal]` 类型结果 |
| 职责 | 解析`level_proposals`；返回 `list[LevelProposal]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.get` → `isinstance` → `ValueError` → `enumerate` → `upper` → `row.get` → `strip` → `_float_field`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[LevelProposal]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.get、isinstance、ValueError、enumerate、upper、str、row.get、strip、_float_field、take_profits.append、float、_compose_level_deduction_reason、_level_deduction_quality、proposals.append、LevelProposal、round、_clamp_strength、_validate_level_path_contract |
| 复杂度 / 风险 | 分支 11；跨度 86 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py) · 直接动态测试 |

<a id="fun-866b1d79aa"></a>

#### FUN-866B1D79AA

| 设计项 | 说明 |
|---|---|
| 函数 | `_validate_level_path_contract` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L532` |
| 签名 | `_validate_level_path_contract(proposals: list[LevelProposal])` |
| 参数 | `proposals`（list[LevelProposal]）：由 `proposals` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 验证`level_path_contract`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `ValueError` → `sorted`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、ValueError、sorted |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1cf0104153"></a>

#### FUN-1CF0104153

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_transaction_proposal` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L540` |
| 签名 | `parse_transaction_proposal(data: dict[str, Any], *, debate_bias: Bias, signal_count: int)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`debate_bias`（Bias）：由调用方提供的 `debate_bias` 输入对象<br>`signal_count`（int）：信号数量 |
| 返回 | 返回 `TransactionProposal` 类型结果 |
| 职责 | 解析`transaction_proposal`；返回 `TransactionProposal` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `data.get` → `range` → `max` → `_index_list` → `_string_list` → `TransactionProposal`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `TransactionProposal` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、data.get、set、range、max、_index_list、_string_list、TransactionProposal |
| 复杂度 / 风险 | 分支 2；跨度 25 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-616d649c39"></a>

#### FUN-616D649C39

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_risk_reviews` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L567` |
| 签名 | `parse_risk_reviews(data: dict[str, Any], *, proposal: TransactionProposal, signal_count: int)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`proposal`（TransactionProposal）：候选交易方案<br>`signal_count`（int）：信号数量 |
| 返回 | 返回 `list[RiskReview]` 类型结果 |
| 职责 | 解析`risk_reviews`；返回 `list[RiskReview]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.get` → `isinstance` → `ValueError` → `lower` → `row.get` → `_index_list` → `_clamp_strength` → `RiskReview`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[RiskReview]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.get、isinstance、ValueError、lower、str、row.get、_index_list、_clamp_strength、bool、RiskReview、_string_list、join |
| 复杂度 / 风险 | 分支 6；跨度 34 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-675d6fb6d6"></a>

#### FUN-675D6FB6D6

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_manager_decision` |
| 源码位置 | [src/agents/llm/schemas.py](../../../src/agents/llm/schemas.py) · `L603` |
| 签名 | `parse_manager_decision(data: dict[str, Any], *, proposal: TransactionProposal, reviews: list[RiskReview])` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`proposal`（TransactionProposal）：候选交易方案<br>`reviews`（list[RiskReview]）：风险或评审结果集合 |
| 返回 | 返回 `ManagerDecision` 类型结果 |
| 职责 | 解析`manager_decision`；返回 `ManagerDecision` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `data.get` → `_index_list` → `strip` → `intersection` → `min` → `ManagerDecision` → `_clamp_strength`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ManagerDecision` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、data.get、_index_list、strip、intersection、set、min、ManagerDecision、_clamp_strength |
| 复杂度 / 风险 | 分支 7；跨度 42 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="unit-7226a2379a"></a>

### UNIT-7226A2379A

**模块**：`src/agents/llm/stages/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7226A2379A |
| 源码 | [src/agents/llm/stages/__init__.py](../../../src/agents/llm/stages/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-1df6497ce4"></a>

### UNIT-1DF6497CE4

**模块**：`src/agents/llm/stages/analysts/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1DF6497CE4 |
| 源码 | [src/agents/llm/stages/analysts/__init__.py](../../../src/agents/llm/stages/analysts/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/analysts/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-73b0811649"></a>

### UNIT-73B0811649

**模块**：`src/agents/llm/stages/analysts/_common.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-73B0811649 |
| 源码 | [src/agents/llm/stages/analysts/_common.py](../../../src/agents/llm/stages/analysts/_common.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/analysts/_common.py` 的职责，通过 `run_specialist_llm` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[run_specialist_llm](#fun-55e3a906bd)

<a id="fun-55e3a906bd"></a>

#### FUN-55E3A906BD

| 设计项 | 说明 |
|---|---|
| 函数 | `run_specialist_llm` |
| 源码位置 | [src/agents/llm/stages/analysts/_common.py](../../../src/agents/llm/stages/analysts/_common.py) · `L23` |
| 签名 | `run_specialist_llm(ctx: MarketContext, *, stage: str, agent: str, system: str, payload_fn: Callable[[MarketContext], dict[str, Any]], user_prefix: str)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`stage`（str）：流水线或 Agent 阶段标识<br>`agent`（str）：Agent 实例或标识<br>`system`（str）：由 `system` 表示的文本或标识<br>`payload_fn`（Callable[[MarketContext], dict[str, Any]]）：调用方提供的回调函数<br>`user_prefix`（str）：由 `user_prefix` 表示的文本或标识 |
| 返回 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`specialist_llm`；返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `payload_fn` → `json.dumps` → `run_llm_stage` → `parse_analyst_report`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、payload_fn、json.dumps、run_llm_stage、parse_analyst_report |
| 复杂度 / 风险 | 分支 1；跨度 28 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-fcd3d48fde"></a>

### UNIT-FCD3D48FDE

**模块**：`src/agents/llm/stages/analysts/fundamentals.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FCD3D48FDE |
| 源码 | [src/agents/llm/stages/analysts/fundamentals.py](../../../src/agents/llm/stages/analysts/fundamentals.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/analysts/fundamentals.py` 的职责，通过 `run_llm_fundamentals_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_fundamentals_analyst](#fun-039cd9925f)

<a id="fun-039cd9925f"></a>

#### FUN-039CD9925F

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_fundamentals_analyst` |
| 源码位置 | [src/agents/llm/stages/analysts/fundamentals.py](../../../src/agents/llm/stages/analysts/fundamentals.py) · `L16` |
| 签名 | `run_llm_fundamentals_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_fundamentals_analyst`；返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_specialist_llm`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_specialist_llm |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) · 直接动态测试 |

<a id="unit-25115c1d6f"></a>

### UNIT-25115C1D6F

**模块**：`src/agents/llm/stages/analysts/news.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-25115C1D6F |
| 源码 | [src/agents/llm/stages/analysts/news.py](../../../src/agents/llm/stages/analysts/news.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/analysts/news.py` 的职责，通过 `run_llm_news_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_news_analyst](#fun-4e10e953f7)

<a id="fun-4e10e953f7"></a>

#### FUN-4E10E953F7

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_news_analyst` |
| 源码位置 | [src/agents/llm/stages/analysts/news.py](../../../src/agents/llm/stages/analysts/news.py) · `L20` |
| 签名 | `run_llm_news_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_news_analyst`；返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_specialist_llm`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_specialist_llm |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) · 直接动态测试 |

<a id="unit-2bf1b61e7e"></a>

### UNIT-2BF1B61E7E

**模块**：`src/agents/llm/stages/analysts/sentiment.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2BF1B61E7E |
| 源码 | [src/agents/llm/stages/analysts/sentiment.py](../../../src/agents/llm/stages/analysts/sentiment.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/analysts/sentiment.py` 的职责，通过 `run_llm_sentiment_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_sentiment_analyst](#fun-417df23078)

<a id="fun-417df23078"></a>

#### FUN-417DF23078

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_sentiment_analyst` |
| 源码位置 | [src/agents/llm/stages/analysts/sentiment.py](../../../src/agents/llm/stages/analysts/sentiment.py) · `L17` |
| 签名 | `run_llm_sentiment_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_sentiment_analyst`；返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_specialist_llm`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_specialist_llm |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) · 直接动态测试 |

<a id="unit-a3445b9493"></a>

### UNIT-A3445B9493

**模块**：`src/agents/llm/stages/analysts/technical.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A3445B9493 |
| 源码 | [src/agents/llm/stages/analysts/technical.py](../../../src/agents/llm/stages/analysts/technical.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/analysts/technical.py` 的职责，通过 `run_llm_technical_analyst` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_technical_analyst](#fun-c901472c03)

<a id="fun-c901472c03"></a>

#### FUN-C901472C03

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_technical_analyst` |
| 源码位置 | [src/agents/llm/stages/analysts/technical.py](../../../src/agents/llm/stages/analysts/technical.py) · `L61` |
| 签名 | `run_llm_technical_analyst(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_technical_analyst`；返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_specialist_llm`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AnalystReport \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_specialist_llm |
| 复杂度 / 风险 | 分支 0；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py) · 直接动态测试 |

<a id="unit-2ccd7c4dcb"></a>

### UNIT-2CCD7C4DCB

**模块**：`src/agents/llm/stages/bearish.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2CCD7C4DCB |
| 源码 | [src/agents/llm/stages/bearish.py](../../../src/agents/llm/stages/bearish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/bearish.py` 的职责，通过 `run_llm_bearish` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_bearish](#fun-1d081c3bb3)

<a id="fun-1d081c3bb3"></a>

#### FUN-1D081C3BB3

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_bearish` |
| 源码位置 | [src/agents/llm/stages/bearish.py](../../../src/agents/llm/stages/bearish.py) · `L34` |
| 签名 | `run_llm_bearish(ctx: MarketContext, team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `tuple[AgentEvidence \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_bearish`；返回 `tuple[AgentEvidence \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `research_payload` → `json.dumps` → `analyst_evidence_ids` → `evidence_registry` → `run_llm_stage` → `parse_agent_evidence`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AgentEvidence \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、research_payload、json.dumps、analyst_evidence_ids、evidence_registry、run_llm_stage、parse_agent_evidence |
| 复杂度 / 风险 | 分支 3；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="unit-12bf07eb04"></a>

### UNIT-12BF07EB04

**模块**：`src/agents/llm/stages/bullish.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-12BF07EB04 |
| 源码 | [src/agents/llm/stages/bullish.py](../../../src/agents/llm/stages/bullish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/bullish.py` 的职责，通过 `run_llm_bullish` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_bullish](#fun-9efeb32d2f)

<a id="fun-9efeb32d2f"></a>

#### FUN-9EFEB32D2F

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_bullish` |
| 源码位置 | [src/agents/llm/stages/bullish.py](../../../src/agents/llm/stages/bullish.py) · `L37` |
| 签名 | `run_llm_bullish(ctx: MarketContext, team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `tuple[AgentEvidence \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_bullish`；返回 `tuple[AgentEvidence \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `research_payload` → `json.dumps` → `analyst_evidence_ids` → `evidence_registry` → `run_llm_stage` → `parse_agent_evidence`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AgentEvidence \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、research_payload、json.dumps、analyst_evidence_ids、evidence_registry、run_llm_stage、parse_agent_evidence |
| 复杂度 / 风险 | 分支 3；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py) · 直接动态测试 |

<a id="unit-3970799e39"></a>

### UNIT-3970799E39

**模块**：`src/agents/llm/stages/debate.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3970799E39 |
| 源码 | [src/agents/llm/stages/debate.py](../../../src/agents/llm/stages/debate.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/debate.py` 的职责，通过 `run_llm_debate` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_debate](#fun-59f17fb960)

<a id="fun-59f17fb960"></a>

#### FUN-59F17FB960

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_debate` |
| 源码位置 | [src/agents/llm/stages/debate.py](../../../src/agents/llm/stages/debate.py) · `L29` |
| 签名 | `run_llm_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses, *, ctx: MarketContext \| None=None, team: AnalystTeam \| None=None)` |
| 参数 | `bullish`（AgentEvidence）：看多证据或计数<br>`bearish`（AgentEvidence）：看空证据或计数<br>`analyses`（实现约定类型）：各时间框架分析结果<br>`ctx`（MarketContext \| None）：运行上下文；默认值 `None`<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `tuple[ResearchDebate \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_debate`；返回 `tuple[ResearchDebate \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `debate_payload` → `json.dumps` → `run_llm_stage` → `parse_research_debate`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[ResearchDebate \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、debate_payload、json.dumps、run_llm_stage、parse_research_debate |
| 复杂度 / 风险 | 分支 1；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py) · 直接动态测试 |

<a id="unit-4fbc2b73a8"></a>

### UNIT-4FBC2B73A8

**模块**：`src/agents/llm/stages/levels.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4FBC2B73A8 |
| 源码 | [src/agents/llm/stages/levels.py](../../../src/agents/llm/stages/levels.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/levels.py` 的职责，通过 `run_llm_level_proposer` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_level_proposer](#fun-cbb3a88b74)

<a id="fun-cbb3a88b74"></a>

#### FUN-CBB3A88B74

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_level_proposer` |
| 源码位置 | [src/agents/llm/stages/levels.py](../../../src/agents/llm/stages/levels.py) · `L61` |
| 签名 | `run_llm_level_proposer(ctx: MarketContext, team: AnalystTeam, debate: ResearchDebate, rule_signals: list[object])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`team`（AnalystTeam）：分析团队结果<br>`debate`（ResearchDebate）：多角色辩论结果<br>`rule_signals`（list[object]）：交易信号集合 |
| 返回 | 返回 `tuple[list[LevelProposal] \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_level_proposer`；返回 `tuple[list[LevelProposal] \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `level_proposer_payload` → `log.info` → `payload.get` → `json.dumps` → `run_llm_stage` → `max` → `log.warning`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[LevelProposal] \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、level_proposer_payload、log.info、len、payload.get、json.dumps、run_llm_stage、max、log.warning |
| 复杂度 / 风险 | 分支 2；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="unit-5ed826be60"></a>

### UNIT-5ED826BE60

**模块**：`src/agents/llm/stages/manager.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5ED826BE60 |
| 源码 | [src/agents/llm/stages/manager.py](../../../src/agents/llm/stages/manager.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/manager.py` 的职责，通过 `run_llm_manager` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_manager](#fun-af30a97dcf)

<a id="fun-af30a97dcf"></a>

#### FUN-AF30A97DCF

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_manager` |
| 源码位置 | [src/agents/llm/stages/manager.py](../../../src/agents/llm/stages/manager.py) · `L27` |
| 签名 | `run_llm_manager(proposal: TransactionProposal, reviews: list[RiskReview])` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`reviews`（list[RiskReview]）：风险或评审结果集合 |
| 返回 | 返回 `tuple[ManagerDecision \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_manager`；返回 `tuple[ManagerDecision \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `manager_payload` → `json.dumps` → `run_llm_stage` → `parse_manager_decision`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[ManagerDecision \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、manager_payload、json.dumps、run_llm_stage、parse_manager_decision |
| 复杂度 / 风险 | 分支 1；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="unit-9038f74287"></a>

### UNIT-9038F74287

**模块**：`src/agents/llm/stages/risk.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9038F74287 |
| 源码 | [src/agents/llm/stages/risk.py](../../../src/agents/llm/stages/risk.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/risk.py` 的职责，通过 `run_llm_risk` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_risk](#fun-836a19ca04) · [run_llm_risk._parse](#fun-31f4ada410)

<a id="fun-836a19ca04"></a>

#### FUN-836A19CA04

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_risk` |
| 源码位置 | [src/agents/llm/stages/risk.py](../../../src/agents/llm/stages/risk.py) · `L28` |
| 签名 | `run_llm_risk(proposal: TransactionProposal, signal_count: int, *, signals: list[Any] \| None=None, current_price: float \| None=None, data_as_of: dict[str, Any] \| None=None)` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`signal_count`（int）：信号数量<br>`signals`（list[Any] \| None）：交易信号集合；默认值 `None`<br>`current_price`（float \| None）：当前市场价格；默认值 `None`<br>`data_as_of`（dict[str, Any] \| None）：数据截止时间；默认值 `None` |
| 返回 | 返回 `tuple[list[RiskReview] \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_risk`；返回 `tuple[list[RiskReview] \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `risk_payload` → `max` → `min` → `data.get` → `parse_risk_reviews` → `json.dumps` → `run_llm_stage`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[RiskReview] \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、risk_payload、max、min、float、data.get、parse_risk_reviews、json.dumps、run_llm_stage |
| 复杂度 / 风险 | 分支 2；跨度 43 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-31f4ada410"></a>

#### FUN-31F4ADA410

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_risk._parse` |
| 源码位置 | [src/agents/llm/stages/risk.py](../../../src/agents/llm/stages/risk.py) · `L46` |
| 签名 | `run_llm_risk._parse(data: dict)` |
| 参数 | `data`（dict）：输入数据 |
| 返回 | 返回 `list[RiskReview]` 类型结果 |
| 职责 | 解析输入内容；返回 `list[RiskReview]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `data.get` → `parse_risk_reviews`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[RiskReview]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、float、data.get、parse_risk_reviews |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-a996419c04"></a>

### UNIT-A996419C04

**模块**：`src/agents/llm/stages/trader.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A996419C04 |
| 源码 | [src/agents/llm/stages/trader.py](../../../src/agents/llm/stages/trader.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/llm/stages/trader.py` 的职责，通过 `run_llm_trader` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_llm_trader](#fun-ddd80e4bd9) | 执行`llm_trader`；返回 `tuple[TransactionProposal \| None, LLMStageTrace]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) |
| [run_llm_trader._parse](#fun-839ea81209) | 解析输入内容；返回 `TransactionProposal` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[run_llm_trader](#fun-ddd80e4bd9) · [run_llm_trader._parse](#fun-839ea81209)

<a id="fun-ddd80e4bd9"></a>

#### FUN-DDD80E4BD9

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_trader` |
| 源码位置 | [src/agents/llm/stages/trader.py](../../../src/agents/llm/stages/trader.py) · `L28` |
| 签名 | `run_llm_trader(ctx: MarketContext, debate: ResearchDebate, signals: list[TradingSignal], team: AnalystTeam \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`signals`（list[TradingSignal]）：交易信号集合<br>`team`（AnalystTeam \| None）：分析团队结果；默认值 `None` |
| 返回 | 返回 `tuple[TransactionProposal \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_trader`；返回 `tuple[TransactionProposal \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_stage` → `trader_payload` → `max` → `min` → `data.get` → `parse_transaction_proposal` → `json.dumps` → `run_llm_stage`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[TransactionProposal \| None, LLMStageTrace]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_stage、trader_payload、max、min、float、data.get、parse_transaction_proposal、len、json.dumps、run_llm_stage |
| 复杂度 / 风险 | 分支 2；跨度 39 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py) · 直接动态测试 |

<a id="fun-839ea81209"></a>

#### FUN-839EA81209

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_trader._parse` |
| 源码位置 | [src/agents/llm/stages/trader.py](../../../src/agents/llm/stages/trader.py) · `L38` |
| 签名 | `run_llm_trader._parse(data: dict)` |
| 参数 | `data`（dict）：输入数据 |
| 返回 | 返回 `TransactionProposal` 类型结果 |
| 职责 | 解析输入内容；返回 `TransactionProposal` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `data.get` → `parse_transaction_proposal`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `TransactionProposal` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、float、data.get、parse_transaction_proposal、len |
| 复杂度 / 风险 | 分支 1；跨度 10 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-cc665640c2"></a>

### UNIT-CC665640C2

**模块**：`src/agents/manager.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CC665640C2 |
| 源码 | [src/agents/manager.py](../../../src/agents/manager.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/manager.py` 的职责，通过 `run_manager` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) |
| 验证状态 | selected |

#### 函数导航

[_scale_for_indices](#fun-8c2914e178) · [_evidence_confidence](#fun-a6411be7ce) · [run_manager](#fun-f7395a9fd5)

<a id="fun-8c2914e178"></a>

#### FUN-8C2914E178

| 设计项 | 说明 |
|---|---|
| 函数 | `_scale_for_indices` |
| 源码位置 | [src/agents/manager.py](../../../src/agents/manager.py) · `L8` |
| 签名 | `_scale_for_indices(reviews: list[RiskReview], indices: list[int])` |
| 参数 | `reviews`（list[RiskReview]）：风险或评审结果集合<br>`indices`（list[int]）：由 `indices` 表示的输入集合 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`scale_for_indices`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `selected.intersection` → `min`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、selected.intersection、min |
| 复杂度 / 风险 | 分支 2；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a6411be7ce"></a>

#### FUN-A6411BE7CE

| 设计项 | 说明 |
|---|---|
| 函数 | `_evidence_confidence` |
| 源码位置 | [src/agents/manager.py](../../../src/agents/manager.py) · `L20` |
| 签名 | `_evidence_confidence(reviews: list[RiskReview], proposal: TransactionProposal, *, action: str)` |
| 参数 | `reviews`（list[RiskReview]）：风险或评审结果集合<br>`proposal`（TransactionProposal）：候选交易方案<br>`action`（str）：由 `action` 表示的文本或标识 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`evidence_confidence`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `get` → `round` → `min` → `max`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、get、round、min、max |
| 复杂度 / 风险 | 分支 3；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f7395a9fd5"></a>

#### FUN-F7395A9FD5

| 设计项 | 说明 |
|---|---|
| 函数 | `run_manager` |
| 源码位置 | [src/agents/manager.py](../../../src/agents/manager.py) · `L38` |
| 签名 | `run_manager(proposal: TransactionProposal, reviews: list[RiskReview])` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`reviews`（list[RiskReview]）：风险或评审结果集合 |
| 返回 | 返回 `ManagerDecision` 类型结果 |
| 职责 | 执行管理 Agent 决策；返回 `ManagerDecision` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `next` → `ManagerDecision` → `_scale_for_indices` → `_evidence_confidence`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ManagerDecision` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | next、ManagerDecision、_scale_for_indices、_evidence_confidence |
| 复杂度 / 风险 | 分支 4；跨度 52 行；中 |
| 测试 / 验证 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) · 直接动态测试 |

<a id="unit-c1468c2396"></a>

### UNIT-C1468C2396

**模块**：`src/agents/risk.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C1468C2396 |
| 源码 | [src/agents/risk.py](../../../src/agents/risk.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/risk.py` 的职责，通过 `run_risk_team` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) |
| 验证状态 | selected |

#### 函数导航

[_review](#fun-d7ba82b894) · [run_risk_team](#fun-f364bcfeae)

<a id="fun-d7ba82b894"></a>

#### FUN-D7BA82B894

| 设计项 | 说明 |
|---|---|
| 函数 | `_review` |
| 源码位置 | [src/agents/risk.py](../../../src/agents/risk.py) · `L11` |
| 签名 | `_review(profile: RiskProfile, proposal: TransactionProposal, signal_count: int)` |
| 参数 | `profile`（RiskProfile）：由调用方提供的 `profile` 输入对象<br>`proposal`（TransactionProposal）：候选交易方案<br>`signal_count`（int）：信号数量 |
| 返回 | 返回 `RiskReview` 类型结果 |
| 职责 | 生成`review`结果；返回 `RiskReview` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `RiskReview` → `notes.append`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RiskReview` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | RiskReview、notes.append |
| 复杂度 / 风险 | 分支 6；跨度 47 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f364bcfeae"></a>

#### FUN-F364BCFEAE

| 设计项 | 说明 |
|---|---|
| 函数 | `run_risk_team` |
| 源码位置 | [src/agents/risk.py](../../../src/agents/risk.py) · `L60` |
| 签名 | `run_risk_team(proposal: TransactionProposal, signal_count: int, *, signals: list[Any] \| None=None, current_price: float=0.0, data_as_of: dict[str, Any] \| None=None, observation_mode: bool=False)` |
| 参数 | `proposal`（TransactionProposal）：候选交易方案<br>`signal_count`（int）：信号数量<br>`signals`（list[Any] \| None）：交易信号集合；默认值 `None`<br>`current_price`（float）：当前市场价格；默认值 `0.0`<br>`data_as_of`（dict[str, Any] \| None）：数据截止时间；默认值 `None`<br>`observation_mode`（bool）：观察模式开关或策略；默认值 `False` |
| 返回 | 返回 `list[RiskReview]` 类型结果 |
| 职责 | 执行`risk_team`；返回 `list[RiskReview]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_review` → `apply_risk_gates`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[RiskReview]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _review、apply_risk_gates |
| 复杂度 / 风险 | 分支 1；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) · 直接动态测试 |

<a id="unit-6340c2c541"></a>

### UNIT-6340C2C541

**模块**：`src/agents/trader.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6340C2C541 |
| 源码 | [src/agents/trader.py](../../../src/agents/trader.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 实现“规则/LLM Agent 编排”组件中 `src/agents/trader.py` 的职责，通过 `run_trader_agent` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_trader_agent](#fun-fee6c661e8) | 执行`trader_agent`；返回 `tuple[TransactionProposal, list[TradingSignal]]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) |

#### 函数导航

[run_trader_agent](#fun-fee6c661e8)

<a id="fun-fee6c661e8"></a>

#### FUN-FEE6C661E8

| 设计项 | 说明 |
|---|---|
| 函数 | `run_trader_agent` |
| 源码位置 | [src/agents/trader.py](../../../src/agents/trader.py) · `L17` |
| 签名 | `run_trader_agent(ctx: MarketContext, debate: ResearchDebate, signals: list[TradingSignal])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`signals`（list[TradingSignal]）：交易信号集合 |
| 返回 | 返回 `tuple[TransactionProposal, list[TradingSignal]]` 类型结果 |
| 职责 | 执行`trader_agent`；返回 `tuple[TransactionProposal, list[TradingSignal]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `enumerate` → `getattr` → `sentiment_score` → `sentiment.get` → `rationale.append` → `TransactionProposal`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[TransactionProposal, list[TradingSignal]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | enumerate、getattr、sentiment_score、sentiment.get、rationale.append、TransactionProposal |
| 复杂度 / 风险 | 分支 10；跨度 93 行；高 |
| 测试 / 验证 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) · 直接动态测试 |
