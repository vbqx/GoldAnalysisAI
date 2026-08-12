# ARC-CORE — Advice pipeline orchestration

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-core)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/__init__.py](#unit-b141e8a708) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/config.py](#unit-f43788fe2b) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/__init__.py](#unit-21570b9deb) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/orchestrator.py](#unit-aa59bf5421) | 2 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/orchestrator_hooks.py](#unit-d0bec20560) | 4 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/parallel.py](#unit-d85010dca2) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/progress.py](#unit-0dc607ab64) | 31 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/run_config.py](#unit-4bd152d87b) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/run_context.py](#unit-338f795d63) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/types.py](#unit-d5eb6e2a98) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/log.py](#unit-a91501b8ca) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/pipeline.py](#unit-ba3f06e87a) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-b141e8a708"></a>

### UNIT-B141E8A708

**模块**：`src/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B141E8A708 |
| 源码 | [src/__init__.py](../../../src/__init__.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-f43788fe2b"></a>

### UNIT-F43788FE2B

**模块**：`src/config.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F43788FE2B |
| 源码 | [src/config.py](../../../src/config.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/config.py` 的职责，通过 `short_model_name`、`llm_provider_extra_payload` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_config.py](../../../tests/unit/test_llm_config.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) |
| 验证状态 | selected |

#### 函数导航

[_load_dotenv](#fun-f4d8ffcbf2) · [short_model_name](#fun-9eb4bec26a) · [llm_provider_extra_payload](#fun-55232b8fbe)

<a id="fun-f4d8ffcbf2"></a>

#### FUN-F4D8FFCBF2

| 设计项 | 说明 |
|---|---|
| 函数 | `_load_dotenv` |
| 源码位置 | [src/config.py](../../../src/config.py) · `L9` |
| 签名 | `_load_dotenv()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 加载.env 环境变量；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `resolve` → `Path` → `env_path.exists` → `splitlines` → `env_path.read_text` → `line.strip` → `line.startswith` → `line.split`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | resolve、Path、env_path.exists、splitlines、env_path.read_text、line.strip、line.startswith、line.split、os.environ.setdefault、key.strip、value.strip |
| 复杂度 / 风险 | 分支 3；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9eb4bec26a"></a>

#### FUN-9EB4BEC26A

| 设计项 | 说明 |
|---|---|
| 函数 | `short_model_name` |
| 源码位置 | [src/config.py](../../../src/config.py) · `L104` |
| 签名 | `short_model_name(model: str)` |
| 参数 | `model`（str）：模型名称或模型对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`short_model_name`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `model.split`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | model.split |
| 复杂度 / 风险 | 分支 1；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-55232b8fbe"></a>

#### FUN-55232B8FBE

| 设计项 | 说明 |
|---|---|
| 函数 | `llm_provider_extra_payload` |
| 源码位置 | [src/config.py](../../../src/config.py) · `L108` |
| 签名 | `llm_provider_extra_payload(*, model: str \| None=None)` |
| 参数 | `model`（str \| None）：模型名称或模型对象；默认值 `None` |
| 返回 | 返回 `dict[str, object]` 类型结果 |
| 职责 | 构建`llm_provider_extra_payload`；返回 `dict[str, object]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `os.getenv`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, object]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、os.getenv |
| 复杂度 / 风险 | 分支 3；跨度 12 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_config.py](../../../tests/unit/test_llm_config.py) · 直接动态测试 |

<a id="unit-21570b9deb"></a>

### UNIT-21570B9DEB

**模块**：`src/core/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-21570B9DEB |
| 源码 | [src/core/__init__.py](../../../src/core/__init__.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-aa59bf5421"></a>

### UNIT-AA59BF5421

**模块**：`src/core/orchestrator.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-AA59BF5421 |
| 源码 | [src/core/orchestrator.py](../../../src/core/orchestrator.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/orchestrator.py` 的职责，通过 `run_advice_pipeline`、`run_trade_agent_pipeline` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_advice_pipeline](#fun-0b6e09d42e) | 执行`advice_pipeline`；可能影响外部接口、共享状态；返回 `tuple[dict, dict, dict]` 类型结果。 | 外部接口 I/O；共享状态变更 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) |
| [run_trade_agent_pipeline](#fun-67d665990e) | 执行交易分析 Agent 完整流水线；返回 `tuple[dict, dict, dict]` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[run_advice_pipeline](#fun-0b6e09d42e) · [run_trade_agent_pipeline](#fun-67d665990e)

<a id="fun-0b6e09d42e"></a>

#### FUN-0B6E09D42E

| 设计项 | 说明 |
|---|---|
| 函数 | `run_advice_pipeline` |
| 源码位置 | [src/core/orchestrator.py](../../../src/core/orchestrator.py) · `L27` |
| 签名 | `run_advice_pipeline()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[dict, dict, dict]` 类型结果 |
| 职责 | 执行`advice_pipeline`；可能影响外部接口、共享状态；返回 `tuple[dict, dict, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `begin_pipeline_run` → `get_progress` → `fetch_market_data` → `publish_external_snapshot` → `prog.start` → `run_parallel` → `enrich` → `raw.items`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[dict, dict, dict]` 类型结果；可观察变化限于外部接口、共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O；共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | begin_pipeline_run、get_progress、fetch_market_data、publish_external_snapshot、prog.start、run_parallel、enrich、raw.items、prog.done、analyze_timeframe、assemble_market_context、log.info、build_advice_packet、normalized、get_run_config、enhance_advice、log.warning、prog.stage_io、json.dumps、ctx.to_dict |
| 复杂度 / 风险 | 分支 4；跨度 80 行；高 |
| 测试 / 验证 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) · 直接动态测试 |

<a id="fun-67d665990e"></a>

#### FUN-67D665990E

| 设计项 | 说明 |
|---|---|
| 函数 | `run_trade_agent_pipeline` |
| 源码位置 | [src/core/orchestrator.py](../../../src/core/orchestrator.py) · `L110` |
| 签名 | `run_trade_agent_pipeline()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[dict, dict, dict]` 类型结果 |
| 职责 | 执行交易分析 Agent 完整流水线；返回 `tuple[dict, dict, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_advice_pipeline`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict, dict, dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_advice_pipeline |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-d0bec20560"></a>

### UNIT-D0BEC20560

**模块**：`src/core/orchestrator_hooks.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D0BEC20560 |
| 源码 | [src/core/orchestrator_hooks.py](../../../src/core/orchestrator_hooks.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/orchestrator_hooks.py` 的职责，通过 `begin_pipeline_run`、`fetch_market_data`、`publish_external_snapshot`、`finalize_pipeline_archive` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 4 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [begin_pipeline_run](#fun-dd1340f890) | 执行`begin_pipeline`；返回 `tuple[str, float]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |
| [fetch_market_data](#fun-06f77b71cb) | 获取`market_data`；可能影响外部接口；返回 `DataFetchResult` 类型结果。 | 外部接口 I/O | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |
| [finalize_pipeline_archive](#fun-e9ab4f388f) | 归档`finalize_pipeline`；无返回值（None）。 | 未检测到直接副作用 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |

#### 函数导航

[begin_pipeline_run](#fun-dd1340f890) · [fetch_market_data](#fun-06f77b71cb) · [publish_external_snapshot](#fun-d2656c49ea) · [finalize_pipeline_archive](#fun-e9ab4f388f)

<a id="fun-dd1340f890"></a>

#### FUN-DD1340F890

| 设计项 | 说明 |
|---|---|
| 函数 | `begin_pipeline_run` |
| 源码位置 | [src/core/orchestrator_hooks.py](../../../src/core/orchestrator_hooks.py) · `L15` |
| 签名 | `begin_pipeline_run()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[str, float]` 类型结果 |
| 职责 | 执行`begin_pipeline`；返回 `tuple[str, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `allocate_run_id` → `set_current_run_id` → `log.info` → `time.perf_counter`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | allocate_run_id、set_current_run_id、log.info、time.perf_counter |
| 复杂度 / 风险 | 分支 0；跨度 7 行；高 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="fun-06f77b71cb"></a>

#### FUN-06F77B71CB

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_market_data` |
| 源码位置 | [src/core/orchestrator_hooks.py](../../../src/core/orchestrator_hooks.py) · `L24` |
| 签名 | `fetch_market_data()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `DataFetchResult` 类型结果 |
| 职责 | 获取`market_data`；可能影响外部接口；返回 `DataFetchResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_all_data`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `DataFetchResult` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_all_data |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="fun-d2656c49ea"></a>

#### FUN-D2656C49EA

| 设计项 | 说明 |
|---|---|
| 函数 | `publish_external_snapshot` |
| 源码位置 | [src/core/orchestrator_hooks.py](../../../src/core/orchestrator_hooks.py) · `L28` |
| 签名 | `publish_external_snapshot(fetched: DataFetchResult, prog: Any)` |
| 参数 | `fetched`（DataFetchResult）：数据获取结果<br>`prog`（Any）：由调用方提供的 `prog` 输入对象 |
| 返回 | 无返回值（None） |
| 职责 | 发布`external_snapshot`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `prog.set_external_snapshot` → `external_snapshot_from_fetch`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | prog.set_external_snapshot、external_snapshot_from_fetch |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="fun-e9ab4f388f"></a>

#### FUN-E9AB4F388F

| 设计项 | 说明 |
|---|---|
| 函数 | `finalize_pipeline_archive` |
| 源码位置 | [src/core/orchestrator_hooks.py](../../../src/core/orchestrator_hooks.py) · `L34` |
| 签名 | `finalize_pipeline_archive(run_id: str, *, fetched: DataFetchResult, report: dict[str, Any], enriched: dict, analyses: dict, elapsed_s: float, run_config: RunConfig \| None=None)` |
| 参数 | `run_id`（str）：对象标识<br>`fetched`（DataFetchResult）：数据获取结果<br>`report`（dict[str, Any]）：分析报告<br>`enriched`（dict）：已补充指标的行情数据<br>`analyses`（dict）：各时间框架分析结果<br>`elapsed_s`（float）：由 `elapsed_s` 表示的数值参数<br>`run_config`（RunConfig \| None）：运行配置；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 归档`finalize_pipeline`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `normalized` → `get_run_config` → `archive_run`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | normalized、get_run_config、archive_run |
| 复杂度 / 风险 | 分支 0；跨度 20 行；高 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="unit-d85010dca2"></a>

### UNIT-D85010DCA2

**模块**：`src/core/parallel.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D85010DCA2 |
| 源码 | [src/core/parallel.py](../../../src/core/parallel.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/parallel.py` 的职责，通过 `ParallelTaskError`、`run_parallel` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_parallel.py](../../../tests/unit/test_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[ParallelTaskError.__init__](#fun-121ea3a282) · [run_parallel](#fun-f68413bb73) · [run_parallel._run](#fun-554230efc2)

<a id="fun-121ea3a282"></a>

#### FUN-121EA3A282

| 设计项 | 说明 |
|---|---|
| 函数 | `ParallelTaskError.__init__` |
| 源码位置 | [src/core/parallel.py](../../../src/core/parallel.py) · `L20` |
| 签名 | `ParallelTaskError.__init__(self, errors: dict[str, BaseException])` |
| 参数 | `errors`（dict[str, BaseException]）：由 `errors` 表示的键值映射 |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `sorted` → `__init__` → `super`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、sorted、__init__、super |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f68413bb73"></a>

#### FUN-F68413BB73

| 设计项 | 说明 |
|---|---|
| 函数 | `run_parallel` |
| 源码位置 | [src/core/parallel.py](../../../src/core/parallel.py) · `L26` |
| 签名 | `run_parallel(tasks: list[tuple[str, Callable[[], T]]], *, max_workers: int, label: str='', raise_on_error: bool=False)` |
| 参数 | `tasks`（list[tuple[str, Callable[[], T]]]）：调用方提供的回调函数<br>`max_workers`（int）：由 `max_workers` 表示的数值参数<br>`label`（str）：展示或分类标签；默认值 `''`<br>`raise_on_error`（bool）：错误信息或异常对象；默认值 `False` |
| 返回 | 返回 `dict[str, T]` 类型结果 |
| 职责 | 执行`parallel`；返回 `dict[str, T]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `fn` → `worker_ctx.run` → `ThreadPoolExecutor` → `pool.submit` → `contextvars.copy_context` → `as_completed`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, T]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ParallelTaskError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、len、fn、worker_ctx.run、ThreadPoolExecutor、pool.submit、contextvars.copy_context、as_completed、future.result、log.warning、ParallelTaskError |
| 复杂度 / 风险 | 分支 7；跨度 49 行；中 |
| 测试 / 验证 | [tests/unit/test_parallel.py](../../../tests/unit/test_parallel.py) · 直接动态测试 |

<a id="fun-554230efc2"></a>

#### FUN-554230EFC2

| 设计项 | 说明 |
|---|---|
| 函数 | `run_parallel._run` |
| 源码位置 | [src/core/parallel.py](../../../src/core/parallel.py) · `L46` |
| 签名 | `run_parallel._run(name: str, fn: Callable[[], T], worker_ctx: contextvars.Context)` |
| 参数 | `name`（str）：对象名称<br>`fn`（Callable[[], T]）：调用方提供的回调函数<br>`worker_ctx`（contextvars.Context）：运行上下文 |
| 返回 | 返回 `tuple[str, T \| None, BaseException \| None]` 类型结果 |
| 职责 | 执行当前处理流程；返回 `tuple[str, T \| None, BaseException \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `worker_ctx.run`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, T \| None, BaseException \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | worker_ctx.run |
| 复杂度 / 风险 | 分支 1；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-0dc607ab64"></a>

### UNIT-0DC607AB64

**模块**：`src/core/progress.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0DC607AB64 |
| 源码 | [src/core/progress.py](../../../src/core/progress.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/progress.py` 的职责，通过 `PipelineProgressStep`、`PipelineProgressState`、`LLMIORecord`、`ProgressReporter`、`NoOpProgressReporter`、`get_progress`、`set_progress`、`reset_progress` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 31 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [PipelineProgressState.to_dict](#fun-e6e1bb921a) | 将当前对象转换为可序列化字典；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |

#### 函数导航

[PipelineProgressState.to_dict](#fun-e6e1bb921a) · [LLMIORecord.to_dict](#fun-15a8181c39) · [ProgressReporter.__init__](#fun-cb609da8dc) · [ProgressReporter.set_external_snapshot](#fun-71a259922f) · [ProgressReporter.start](#fun-ef0ac17bf3) · [ProgressReporter.start_sibling](#fun-a57d337b7d) · [ProgressReporter.update](#fun-f4408a209b) · [ProgressReporter.done](#fun-5e62a87f3a) · [ProgressReporter.fail](#fun-59b596d460) · [ProgressReporter.skip](#fun-1f365c723b) · [ProgressReporter.snapshot](#fun-40fa2599e6) · [ProgressReporter.llm_io_snapshot](#fun-0cb129ff59) · [ProgressReporter.stage_io](#fun-2b8326fbcd) · [ProgressReporter.llm_begin](#fun-776ea31038) · [ProgressReporter.llm_note_attempt](#fun-326c939089) · [ProgressReporter.run_llm_stream](#fun-5665b88765) · [ProgressReporter.llm_end](#fun-7ac82003df) · [ProgressReporter._new_llm_record](#fun-c39210a2c9) · [ProgressReporter._apply_telemetry](#fun-b1d16223b8) · [ProgressReporter._find_llm](#fun-46d50ce2f3) · [ProgressReporter._on_llm_begin](#fun-e72e9180d4) · [ProgressReporter._on_llm_chunk](#fun-f3e1b56237) · [ProgressReporter._on_llm_end](#fun-2246070cd9) · [ProgressReporter._find](#fun-56d0f4ca20) · [ProgressReporter._finish_all_running](#fun-473e5d3fd6) · [ProgressReporter._finish_running](#fun-d1368ea00b) · [ProgressReporter._elapsed_since_step_start](#fun-592ed31999) · [ProgressReporter._on_change](#fun-5a6a8e27cf) · [get_progress](#fun-ec9d010cf8) · [set_progress](#fun-6b37902476) · [reset_progress](#fun-f2934a14dd)

<a id="fun-e6e1bb921a"></a>

#### FUN-E6E1BB921A

| 设计项 | 说明 |
|---|---|
| 函数 | `PipelineProgressState.to_dict` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L29` |
| 签名 | `PipelineProgressState.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 11 行；高 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-15a8181c39"></a>

#### FUN-15A8181C39

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMIORecord.to_dict` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L66` |
| 签名 | `LLMIORecord.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list |
| 复杂度 / 风险 | 分支 0；跨度 23 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-cb609da8dc"></a>

#### FUN-CB609DA8DC

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.__init__` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L105` |
| 签名 | `ProgressReporter.__init__(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `PipelineProgressState` → `threading.RLock`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | PipelineProgressState、threading.RLock |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-71a259922f"></a>

#### FUN-71A259922F

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.set_external_snapshot` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L111` |
| 签名 | `ProgressReporter.set_external_snapshot(self, data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 无返回值（None） |
| 职责 | 执行`set_external_snapshot`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._on_change`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._on_change |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="fun-ef0ac17bf3"></a>

#### FUN-EF0AC17BF3

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.start` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L115` |
| 签名 | `ProgressReporter.start(self, step_id: str, label: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`label`（str）：展示或分类标签<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 启动当前任务；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._finish_all_running` → `PipelineProgressStep` → `time.perf_counter` → `self.state.steps.append` → `self._on_change`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._finish_all_running、PipelineProgressStep、time.perf_counter、self.state.steps.append、self._on_change |
| 复杂度 / 风险 | 分支 0；跨度 7 行；中 |
| 测试 / 验证 | [tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="fun-a57d337b7d"></a>

#### FUN-A57D337B7D

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.start_sibling` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L123` |
| 签名 | `ProgressReporter.start_sibling(self, step_id: str, label: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`label`（str）：展示或分类标签<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 启动`sibling`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `PipelineProgressStep` → `time.perf_counter` → `self.state.steps.append` → `self._on_change`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | PipelineProgressStep、time.perf_counter、self.state.steps.append、self._on_change |
| 复杂度 / 风险 | 分支 0；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py) · 直接动态测试 |

<a id="fun-f4408a209b"></a>

#### FUN-F4408A209B

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.update` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L131` |
| 签名 | `ProgressReporter.update(self, step_id: str, *, detail: str \| None=None, label: str \| None=None)` |
| 参数 | `step_id`（str）：对象标识<br>`detail`（str \| None）：详细说明文本；默认值 `None`<br>`label`（str \| None）：展示或分类标签；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 更新当前状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._find` → `self._on_change`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._find、self._on_change |
| 复杂度 / 风险 | 分支 3；跨度 9 行；中 |
| 测试 / 验证 | [tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py) · 直接动态测试 |

<a id="fun-5e62a87f3a"></a>

#### FUN-5E62A87F3A

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.done` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L141` |
| 签名 | `ProgressReporter.done(self, step_id: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 执行`done`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._find` → `self._elapsed_since_step_start` → `self._on_change`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._find、self._elapsed_since_step_start、self._on_change |
| 复杂度 / 风险 | 分支 2；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-59b596d460"></a>

#### FUN-59B596D460

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.fail` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L151` |
| 签名 | `ProgressReporter.fail(self, step_id: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 执行`fail`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._find` → `self._elapsed_since_step_start` → `self._on_change`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._find、self._elapsed_since_step_start、self._on_change |
| 复杂度 / 风险 | 分支 1；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="fun-1f365c723b"></a>

#### FUN-1F365C723B

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.skip` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L160` |
| 签名 | `ProgressReporter.skip(self, step_id: str, label: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`label`（str）：展示或分类标签<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 执行`skip`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self.state.steps.append` → `PipelineProgressStep` → `self._on_change`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self.state.steps.append、PipelineProgressStep、self._on_change |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py) · 直接动态测试 |

<a id="fun-40fa2599e6"></a>

#### FUN-40FA2599E6

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.snapshot` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L166` |
| 签名 | `ProgressReporter.snapshot(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`snapshot`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.state.to_dict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self.state.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="fun-0cb129ff59"></a>

#### FUN-0CB129FF59

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.llm_io_snapshot` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L169` |
| 签名 | `ProgressReporter.llm_io_snapshot(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`llm_io_snapshot`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `r.to_dict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | r.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-2b8326fbcd"></a>

#### FUN-2B8326FBCD

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.stage_io` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L173` |
| 签名 | `ProgressReporter.stage_io(self, stage: str, *, input_text: str, output_text: str, latency_ms: int \| None=None, label: str \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`input_text`（str）：输入文本<br>`output_text`（str）：输入文本<br>`latency_ms`（int \| None）：延迟毫秒数；默认值 `None`<br>`label`（str \| None）：展示或分类标签；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行阶段输入输出遥测处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `STAGE_LABELS.get` → `self.llm_io.append` → `LLMIORecord`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | STAGE_LABELS.get、self.llm_io.append、LLMIORecord |
| 复杂度 / 风险 | 分支 0；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-776ea31038"></a>

#### FUN-776EA31038

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.llm_begin` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L197` |
| 签名 | `ProgressReporter.llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], *, telemetry: dict[str, Any] \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`model`（str）：模型名称或模型对象<br>`messages`（list[dict[str, str]]）：消息序列<br>`telemetry`（dict[str, Any] \| None）：遥测记录；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`llm_begin`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `STAGE_LABELS.get` → `self._find_llm` → `tel.get` → `self._apply_telemetry` → `self.llm_io.append` → `self._new_llm_record` → `self._on_llm_begin`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | STAGE_LABELS.get、self._find_llm、bool、tel.get、list、self._apply_telemetry、self.llm_io.append、self._new_llm_record、self._on_llm_begin |
| 复杂度 / 风险 | 分支 2；跨度 29 行；中 |
| 测试 / 验证 | [tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-326c939089"></a>

#### FUN-326C939089

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.llm_note_attempt` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L227` |
| 签名 | `ProgressReporter.llm_note_attempt(self, stage: str, *, attempt: int, reason: str, error: str \| None=None, latency_ms: int \| None=None, usage: dict[str, int] \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`attempt`（int）：由 `attempt` 表示的数值参数<br>`reason`（str）：判定或拒绝原因<br>`error`（str \| None）：错误信息或异常对象；默认值 `None`<br>`latency_ms`（int \| None）：延迟毫秒数；默认值 `None`<br>`usage`（dict[str, int] \| None）：由 `usage` 表示的键值映射；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`llm_note_attempt`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._find_llm` → `rec.attempts.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._find_llm、dict、rec.attempts.append |
| 复杂度 / 风险 | 分支 2；跨度 24 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5665b88765"></a>

#### FUN-5665B88765

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.run_llm_stream` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L252` |
| 签名 | `ProgressReporter.run_llm_stream(self, stage: str, chunk_iter)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`chunk_iter`（实现约定类型）：由调用方提供的 `chunk_iter` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 执行LLM 流式响应；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parts.append` → `self._on_llm_chunk` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | parts.append、self._on_llm_chunk、join |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7ac82003df"></a>

#### FUN-7AC82003DF

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter.llm_end` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L260` |
| 签名 | `ProgressReporter.llm_end(self, stage: str, output: str, *, error: str \| None=None, latency_ms: int \| None=None, telemetry: dict[str, Any] \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`output`（str）：输出对象或输出路径<br>`error`（str \| None）：错误信息或异常对象；默认值 `None`<br>`latency_ms`（int \| None）：延迟毫秒数；默认值 `None`<br>`telemetry`（dict[str, Any] \| None）：遥测记录；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`llm_end`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._find_llm` → `self._apply_telemetry` → `telemetry.get` → `estimate_text_size` → `self._on_llm_end`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._find_llm、self._apply_telemetry、telemetry.get、estimate_text_size、self._on_llm_end |
| 复杂度 / 风险 | 分支 3；跨度 25 行；中 |
| 测试 / 验证 | [tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-c39210a2c9"></a>

#### FUN-C39210A2C9

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._new_llm_record` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L286` |
| 签名 | `ProgressReporter._new_llm_record(self, stage: str, label: str, model: str, messages: list[dict[str, str]], tel: dict[str, Any])` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`label`（str）：展示或分类标签<br>`model`（str）：模型名称或模型对象<br>`messages`（list[dict[str, str]]）：消息序列<br>`tel`（dict[str, Any]）：由 `tel` 表示的键值映射 |
| 返回 | 返回 `LLMIORecord` 类型结果 |
| 职责 | 生成`new_llm_record`结果；返回 `LLMIORecord` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `LLMIORecord` → `self._apply_telemetry`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMIORecord` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | LLMIORecord、list、self._apply_telemetry |
| 复杂度 / 风险 | 分支 0；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b1d16223b8"></a>

#### FUN-B1D16223B8

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._apply_telemetry` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L299` |
| 签名 | `ProgressReporter._apply_telemetry(rec: LLMIORecord, tel: dict[str, Any])` |
| 参数 | `rec`（LLMIORecord）：由调用方提供的 `rec` 输入对象<br>`tel`（dict[str, Any]）：由 `tel` 表示的键值映射 |
| 返回 | 无返回值（None） |
| 职责 | 应用`telemetry`；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、int |
| 复杂度 / 风险 | 分支 11；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-46d50ce2f3"></a>

#### FUN-46D50CE2F3

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._find_llm` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L323` |
| 签名 | `ProgressReporter._find_llm(self, stage: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `LLMIORecord \| None` 类型结果 |
| 职责 | 查找`llm`；返回 `LLMIORecord \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `reversed`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMIORecord \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | reversed |
| 复杂度 / 风险 | 分支 2；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e72e9180d4"></a>

#### FUN-E72E9180D4

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._on_llm_begin` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L329` |
| 签名 | `ProgressReporter._on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`model`（str）：模型名称或模型对象<br>`messages`（list[dict[str, str]]）：消息序列<br>`label`（str）：展示或分类标签 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_llm_begin`处理；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f3e1b56237"></a>

#### FUN-F3E1B56237

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._on_llm_chunk` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L332` |
| 签名 | `ProgressReporter._on_llm_chunk(self, stage: str, chunk: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`chunk`（str）：由 `chunk` 表示的文本或标识 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_llm_chunk`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._find_llm`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._find_llm |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | [tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-2246070cd9"></a>

#### FUN-2246070CD9

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._on_llm_end` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L338` |
| 签名 | `ProgressReporter._on_llm_end(self, stage: str, output: str, *, error: str \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`output`（str）：输出对象或输出路径<br>`error`（str \| None）：错误信息或异常对象；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_llm_end`处理；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-56d0f4ca20"></a>

#### FUN-56D0F4CA20

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._find` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L341` |
| 签名 | `ProgressReporter._find(self, step_id: str)` |
| 参数 | `step_id`（str）：对象标识 |
| 返回 | 返回 `PipelineProgressStep \| None` 类型结果 |
| 职责 | 查找当前对象；返回 `PipelineProgressStep \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `reversed`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `PipelineProgressStep \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | reversed |
| 复杂度 / 风险 | 分支 2；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-473e5d3fd6"></a>

#### FUN-473E5D3FD6

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._finish_all_running` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L347` |
| 签名 | `ProgressReporter._finish_all_running(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`finish_all_running`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._elapsed_since_step_start`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._elapsed_since_step_start |
| 复杂度 / 风险 | 分支 2；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d1368ea00b"></a>

#### FUN-D1368EA00B

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._finish_running` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L353` |
| 签名 | `ProgressReporter._finish_running(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`finish_running`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `reversed` → `self._elapsed_since_step_start`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | reversed、self._elapsed_since_step_start |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-592ed31999"></a>

#### FUN-592ED31999

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._elapsed_since_step_start` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L360` |
| 签名 | `ProgressReporter._elapsed_since_step_start(self, step: PipelineProgressStep)` |
| 参数 | `step`（PipelineProgressStep）：由调用方提供的 `step` 输入对象 |
| 返回 | 返回 `int \| None` 类型结果 |
| 职责 | 启动`elapsed_since_step`；返回 `int \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `time.perf_counter`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、time.perf_counter |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5a6a8e27cf"></a>

#### FUN-5A6A8E27CF

| 设计项 | 说明 |
|---|---|
| 函数 | `ProgressReporter._on_change` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L365` |
| 签名 | `ProgressReporter._on_change(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_change`处理；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ec9d010cf8"></a>

#### FUN-EC9D010CF8

| 设计项 | 说明 |
|---|---|
| 函数 | `get_progress` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L376` |
| 签名 | `get_progress()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ProgressReporter` 类型结果 |
| 职责 | 获取`progress`；可能影响共享状态；返回 `ProgressReporter` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_progress_ctx.get`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ProgressReporter` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _progress_ctx.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6b37902476"></a>

#### FUN-6B37902476

| 设计项 | 说明 |
|---|---|
| 函数 | `set_progress` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L380` |
| 签名 | `set_progress(reporter: ProgressReporter \| None)` |
| 参数 | `reporter`（ProgressReporter \| None）：由调用方提供的 `reporter` 输入对象 |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 生成`set_progress`结果；可能影响共享状态；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `_progress_ctx.set`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _progress_ctx.set |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="fun-f2934a14dd"></a>

#### FUN-F2934A14DD

| 设计项 | 说明 |
|---|---|
| 函数 | `reset_progress` |
| 源码位置 | [src/core/progress.py](../../../src/core/progress.py) · `L384` |
| 签名 | `reset_progress(token)` |
| 参数 | `token`（实现约定类型）：标记或认证令牌 |
| 返回 | 无返回值（None） |
| 职责 | 重置`progress`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_progress_ctx.reset`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _progress_ctx.reset |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="unit-4bd152d87b"></a>

### UNIT-4BD152D87B

**模块**：`src/core/run_config.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4BD152D87B |
| 源码 | [src/core/run_config.py](../../../src/core/run_config.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/run_config.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-338f795d63"></a>

### UNIT-338F795D63

**模块**：`src/core/run_context.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-338F795D63 |
| 源码 | [src/core/run_context.py](../../../src/core/run_context.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/run_context.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-d5eb6e2a98"></a>

### UNIT-D5EB6E2A98

**模块**：`src/core/types.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D5EB6E2A98 |
| 源码 | [src/core/types.py](../../../src/core/types.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/core/types.py` 的职责，通过 `EvidenceItem`、`HeadlineItem`、`CalendarEvent`、`MacroQuote`、`ExternalFactors`、`MarketContext`、`LLMStageTrace` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py) |
| 验证状态 | selected |

#### 函数导航

[HeadlineItem.to_dict](#fun-1f2e0f588a) · [CalendarEvent.to_dict](#fun-5a0e6a3977) · [CalendarEvent.display](#fun-4654e9b6a5) · [MacroQuote.to_dict](#fun-0b81375e45) · [ExternalFactors.to_dict](#fun-b52c340615) · [MarketContext.to_dict](#fun-6449e7e08e) · [LLMStageTrace.to_dict](#fun-a2365082b2)

<a id="fun-1f2e0f588a"></a>

#### FUN-1F2E0F588A

| 设计项 | 说明 |
|---|---|
| 函数 | `HeadlineItem.to_dict` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L37` |
| 签名 | `HeadlineItem.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-5a0e6a3977"></a>

#### FUN-5A0E6A3977

| 设计项 | 说明 |
|---|---|
| 函数 | `CalendarEvent.to_dict` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L50` |
| 签名 | `CalendarEvent.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-4654e9b6a5"></a>

#### FUN-4654E9B6A5

| 设计项 | 说明 |
|---|---|
| 函数 | `CalendarEvent.display` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L53` |
| 签名 | `CalendarEvent.display(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`display`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0b81375e45"></a>

#### FUN-0B81375E45

| 设计项 | 说明 |
|---|---|
| 函数 | `MacroQuote.to_dict` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L69` |
| 签名 | `MacroQuote.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-b52c340615"></a>

#### FUN-B52C340615

| 设计项 | 说明 |
|---|---|
| 函数 | `ExternalFactors.to_dict` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L86` |
| 签名 | `ExternalFactors.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `h.to_dict` → `c.to_dict` → `m.to_dict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | h.to_dict、c.to_dict、m.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-6449e7e08e"></a>

#### FUN-6449E7E08E

| 设计项 | 说明 |
|---|---|
| 函数 | `MarketContext.to_dict` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L122` |
| 签名 | `MarketContext.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.external.to_dict` → `self.analyses.keys`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self.external.to_dict、list、self.analyses.keys |
| 复杂度 / 风险 | 分支 0；跨度 10 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-a2365082b2"></a>

#### FUN-A2365082B2

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMStageTrace.to_dict` |
| 源码位置 | [src/core/types.py](../../../src/core/types.py) · `L154` |
| 签名 | `LLMStageTrace.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="unit-a91501b8ca"></a>

### UNIT-A91501B8CA

**模块**：`src/log.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A91501B8CA |
| 源码 | [src/log.py](../../../src/log.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/log.py` 的职责，通过 `setup_logging`、`get_logger` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[setup_logging](#fun-286f9adbe7) · [get_logger](#fun-02cd3d28ec)

<a id="fun-286f9adbe7"></a>

#### FUN-286F9ADBE7

| 设计项 | 说明 |
|---|---|
| 函数 | `setup_logging` |
| 源码位置 | [src/log.py](../../../src/log.py) · `L17` |
| 签名 | `setup_logging(*, level: str \| None=None, log_file: str \| None=None)` |
| 参数 | `level`（str \| None）：候选价格水平；默认值 `None`<br>`log_file`（str \| None）：由调用方提供的 `log_file` 输入对象；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`setup_logging`处理；可能影响文件系统、全局状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `getattr` → `logging.getLogger` → `root.setLevel` → `logging.StreamHandler` → `hasattr` → `sys.stderr.reconfigure` → `console.setFormatter`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 无返回值（None）；可观察变化限于文件系统、全局状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写；全局状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、getattr、logging.getLogger、root.setLevel、logging.StreamHandler、hasattr、sys.stderr.reconfigure、console.setFormatter、logging.Formatter、root.addHandler、Path、path.parent.mkdir、RotatingFileHandler、file_handler.setFormatter、setLevel、debug |
| 复杂度 / 风险 | 分支 5；跨度 43 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-02cd3d28ec"></a>

#### FUN-02CD3D28EC

| 设计项 | 说明 |
|---|---|
| 函数 | `get_logger` |
| 源码位置 | [src/log.py](../../../src/log.py) · `L62` |
| 签名 | `get_logger(name: str)` |
| 参数 | `name`（str）：对象名称 |
| 返回 | 返回 `logging.Logger` 类型结果 |
| 职责 | 获取`logger`；返回 `logging.Logger` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `setup_logging` → `logging.getLogger`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `logging.Logger` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | setup_logging、logging.getLogger |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-ba3f06e87a"></a>

### UNIT-BA3F06E87A

**模块**：`src/pipeline.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-BA3F06E87A |
| 源码 | [src/pipeline.py](../../../src/pipeline.py) |
| 架构组件 | ARC-CORE — Advice pipeline orchestration |
| 职责 | 实现“Advice pipeline orchestration”组件中 `src/pipeline.py` 的职责，通过 `run_analysis` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) |
| 验证状态 | selected |

#### 函数导航

[run_analysis](#fun-33aef245ba)

<a id="fun-33aef245ba"></a>

#### FUN-33AEF245BA

| 设计项 | 说明 |
|---|---|
| 函数 | `run_analysis` |
| 源码位置 | [src/pipeline.py](../../../src/pipeline.py) · `L11` |
| 签名 | `run_analysis()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[dict, dict, dict]` 类型结果 |
| 职责 | 执行`analysis`；返回 `tuple[dict, dict, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `log.debug` → `run_advice_pipeline`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict, dict, dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.debug、run_advice_pipeline |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |
