# ARC-LLM — LLM 传输、上下文和策略

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./README.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/README.md#arc-llm)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/llm/__init__.py](#unit-598812089b) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/analyst.py](#unit-f5cb9d3f8c) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/client.py](#unit-d7fd07af44) | 8 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/context.py](#unit-6c3fd6c2e5) | 6 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/format_io.py](#unit-deb0d517c6) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/narrative_output.py](#unit-fbf77b94fb) | 11 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/prompts.py](#unit-a605fcb3a9) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/router.py](#unit-6568b95afa) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/stage_policy.py](#unit-e488978a91) | 8 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-598812089b"></a>

### UNIT-598812089B

**模块**：`src/llm/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-598812089B |
| 源码 | [src/llm/__init__.py](../../../src/llm/__init__.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-f5cb9d3f8c"></a>

### UNIT-F5CB9D3F8C

**模块**：`src/llm/analyst.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F5CB9D3F8C |
| 源码 | [src/llm/analyst.py](../../../src/llm/analyst.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/analyst.py` 的职责，通过 `validate_llm_payload`、`run_llm_analysis`、`apply_llm_to_report` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py) |
| 验证状态 | selected |

#### 函数导航

[_error_result](#fun-2e761b537c) · [_disabled_result](#fun-7a3c5fbb90) · [_client_from_config](#fun-b472cd2d40) · [_parse_result](#fun-05d603b92f) · [validate_llm_payload](#fun-7722d6583b) · [run_llm_analysis](#fun-c0808d1fd3) · [apply_llm_to_report](#fun-307482df32)

<a id="fun-2e761b537c"></a>

#### FUN-2E761B537C

| 设计项 | 说明 |
|---|---|
| 函数 | `_error_result` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L32` |
| 签名 | `_error_result(report: dict[str, Any], error: str)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`error`（str）：错误信息或异常对象 |
| 返回 | 返回 `LLMAnalysis` 类型结果 |
| 职责 | 生成`error_result`结果；返回 `LLMAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `deepcopy` → `report.get` → `sections.items` → `LLMAnalysis`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | deepcopy、report.get、sections.items、LLMAnalysis |
| 复杂度 / 风险 | 分支 1；跨度 15 行；低 |
| 测试 / 验证 | [tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py) · 直接动态测试 |

<a id="fun-7a3c5fbb90"></a>

#### FUN-7A3C5FBB90

| 设计项 | 说明 |
|---|---|
| 函数 | `_disabled_result` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L49` |
| 签名 | `_disabled_result(reason: str='LLM 未启用')` |
| 参数 | `reason`（str）：判定或拒绝原因；默认值 `'LLM 未启用'` |
| 返回 | 返回 `LLMAnalysis` 类型结果 |
| 职责 | 生成`disabled_result`结果；返回 `LLMAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `LLMAnalysis`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | LLMAnalysis |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b472cd2d40"></a>

#### FUN-B472CD2D40

| 设计项 | 说明 |
|---|---|
| 函数 | `_client_from_config` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L53` |
| 签名 | `_client_from_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 根据配置构建`client`；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `llm_configured` → `LLMClientError` → `client_for_stage`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | LLMClientError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm_configured、LLMClientError、client_for_stage |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-05d603b92f"></a>

#### FUN-05D603B92F

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_result` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L59` |
| 签名 | `_parse_result(data: dict[str, Any], *, model: str, provider: str)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`model`（str）：模型名称或模型对象<br>`provider`（str）：由 `provider` 表示的文本或标识 |
| 返回 | 返回 `LLMAnalysis` 类型结果 |
| 职责 | 解析结果；返回 `LLMAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `data.get` → `isinstance` → `max` → `min` → `LLMAnalysis` → `json.dumps`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、data.get、isinstance、float、max、min、LLMAnalysis、json.dumps |
| 复杂度 / 风险 | 分支 3；跨度 28 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7722d6583b"></a>

#### FUN-7722D6583B

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_llm_payload` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L89` |
| 签名 | `validate_llm_payload(data: dict[str, Any], report: dict[str, Any], *, facts: dict[str, Any] \| None=None, mode: str \| None=None, threshold: float \| None=None, model: str \| None=None, provider: str \| None=None)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`report`（dict[str, Any]）：分析报告<br>`facts`（dict[str, Any] \| None）：结构化事实集合；默认值 `None`<br>`mode`（str \| None）：运行或分析模式；默认值 `None`<br>`threshold`（float \| None）：由调用方提供的 `threshold` 输入对象；默认值 `None`<br>`model`（str \| None）：模型名称或模型对象；默认值 `None`<br>`provider`（str \| None）：由调用方提供的 `provider` 输入对象；默认值 `None` |
| 返回 | 返回 `LLMAnalysis` 类型结果 |
| 职责 | 验证LLM 阶段载荷；返回 `LLMAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_narrative_facts_for_llm` → `_parse_result` → `validate_and_merge_llm_sections` → `data.get` → `report.get` → `validate_llm_top_level_fields` → `field_reasons.items` → `next`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_narrative_facts_for_llm、_parse_result、validate_and_merge_llm_sections、data.get、report.get、validate_llm_top_level_fields、field_reasons.items、next、iter、rejected.values、setattr |
| 复杂度 / 风险 | 分支 4；跨度 39 行；中 |
| 测试 / 验证 | [tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py) · 直接动态测试 |

<a id="fun-c0808d1fd3"></a>

#### FUN-C0808D1FD3

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_analysis` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L130` |
| 签名 | `run_llm_analysis(ctx: MarketContext, debate: ResearchDebate, decision: ManagerDecision, report: dict[str, Any])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`decision`（ManagerDecision）：最终或阶段决策<br>`report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `LLMAnalysis` 类型结果 |
| 职责 | 执行`llm_analysis`；返回 `LLMAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `llm_narrative_enabled` → `_disabled_result` → `_client_from_config` → `build_llm_context` → `build_messages` → `log.info` → `run_llm_stage` → `_error_result`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm_narrative_enabled、_disabled_result、_client_from_config、build_llm_context、build_messages、log.info、run_llm_stage、_error_result、build_narrative_facts_for_llm、validate_llm_payload、report.setdefault、context.get、result.top_level_audit.get、items、log.warning、len、str、log.exception |
| 复杂度 / 风险 | 分支 6；跨度 58 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-307482df32"></a>

#### FUN-307482DF32

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_llm_to_report` |
| 源码位置 | [src/llm/analyst.py](../../../src/llm/analyst.py) · `L190` |
| 签名 | `apply_llm_to_report(report: dict[str, Any], llm: LLMAnalysis)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`llm`（LLMAnalysis）：由调用方提供的 `llm` 输入对象 |
| 返回 | 无返回值（None） |
| 职责 | 应用`llm_report`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `llm.to_dict` → `setdefault` → `report.setdefault` → `getattr` → `get` → `report.get` → `top_audit.get` → `llm.action_plan.replace`；包含 12 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm.to_dict、setdefault、report.setdefault、getattr、get、report.get、top_audit.get、llm.action_plan.replace、conclusion.get |
| 复杂度 / 风险 | 分支 12；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py) · 直接动态测试 |

<a id="unit-d7fd07af44"></a>

### UNIT-D7FD07AF44

**模块**：`src/llm/client.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D7FD07AF44 |
| 源码 | [src/llm/client.py](../../../src/llm/client.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/client.py` 的职责，通过 `LLMClientError`、`LLMClient` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_source_labels.py](../../../tests/unit/test_source_labels.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [LLMClient.chat_stream](#fun-b2c894bd12) | 生成`chat_stream`文本；可能影响外部接口；返回 `Iterator[str]` 类型结果。 | 外部接口 I/O | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) |

#### 函数导航

[LLMClient.__init__](#fun-184ed552df) · [LLMClient.timeout](#fun-b3cf019763) · [LLMClient._request_timeout](#fun-6281d0133f) · [LLMClient._headers](#fun-870c1d436c) · [LLMClient._parse_sse_line](#fun-c5e317f9c8) · [LLMClient.chat_stream](#fun-b2c894bd12) · [LLMClient.chat](#fun-feaf06c7c1) · [LLMClient.chat_json](#fun-cc950a51e1)

<a id="fun-184ed552df"></a>

#### FUN-184ED552DF

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.__init__` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L24` |
| 签名 | `LLMClient.__init__(self, *, api_key: str, base_url: str, model: str, timeout: int \| float \| None=None, connect_timeout: float \| None=None, read_timeout: float \| None=None)` |
| 参数 | `api_key`（str）：索引键<br>`base_url`（str）：外部资源地址<br>`model`（str）：模型名称或模型对象<br>`timeout`（int \| float \| None）：超时秒数；默认值 `None`<br>`connect_timeout`（float \| None）：超时秒数；默认值 `None`<br>`read_timeout`（float \| None）：超时秒数；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `base_url.rstrip` → `min`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | base_url.rstrip、float、min |
| 复杂度 / 风险 | 分支 4；跨度 28 行；低 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-b3cf019763"></a>

#### FUN-B3CF019763

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.timeout` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L54` |
| 签名 | `LLMClient.timeout(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`timeout`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_source_labels.py](../../../tests/unit/test_source_labels.py) · 直接动态测试 |

<a id="fun-6281d0133f"></a>

#### FUN-6281D0133F

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._request_timeout` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L58` |
| 签名 | `LLMClient._request_timeout(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[float, float]` 类型结果 |
| 职责 | 构建`request_timeout`；返回 `tuple[float, float]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py) · 直接动态测试 |

<a id="fun-870c1d436c"></a>

#### FUN-870C1D436C

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._headers` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L61` |
| 签名 | `LLMClient._headers(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`headers`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c5e317f9c8"></a>

#### FUN-C5E317F9C8

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._parse_sse_line` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L67` |
| 签名 | `LLMClient._parse_sse_line(self, line: str)` |
| 参数 | `line`（str）：由 `line` 表示的文本或标识 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 解析`sse_line`；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `line.strip` → `line.startswith` → `strip` → `json.loads` → `get` → `delta.get` → `isinstance`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | line.strip、line.startswith、strip、json.loads、get、delta.get、isinstance |
| 复杂度 / 风险 | 分支 5；跨度 19 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b2c894bd12"></a>

#### FUN-B2C894BD12

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.chat_stream` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L87` |
| 签名 | `LLMClient.chat_stream(self, messages: list[dict[str, str]], *, temperature: float=0.3, response_format: dict[str, str] \| None=None)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`temperature`（float）：模型采样温度；默认值 `0.3`<br>`response_format`（dict[str, str] \| None）：由 `response_format` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `Iterator[str]` 类型结果 |
| 职责 | 生成`chat_stream`文本；可能影响外部接口；返回 `Iterator[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `log.debug` → `requests.post` → `self._headers` → `self._request_timeout` → `LLMClientError` → `resp.iter_lines` → `raw.decode` → `isinstance`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `Iterator[str]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | LLMClientError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.debug、requests.post、self._headers、self._request_timeout、LLMClientError、resp.iter_lines、raw.decode、isinstance、str、self._parse_sse_line |
| 复杂度 / 风险 | 分支 8；跨度 57 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) · 直接动态测试 |

<a id="fun-feaf06c7c1"></a>

#### FUN-FEAF06C7C1

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.chat` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L145` |
| 签名 | `LLMClient.chat(self, messages: list[dict[str, str]], *, temperature: float=0.3, response_format: dict[str, str] \| None=None)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`temperature`（float）：模型采样温度；默认值 `0.3`<br>`response_format`（dict[str, str] \| None）：由 `response_format` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`chat`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.chat_stream` → `strip` → `join` → `LLMClientError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | LLMClientError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、self.chat_stream、strip、join、LLMClientError |
| 复杂度 / 风险 | 分支 1；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cc950a51e1"></a>

#### FUN-CC950A51E1

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.chat_json` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L164` |
| 签名 | `LLMClient.chat_json(self, messages: list[dict[str, str]], *, temperature: float=0.2)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`temperature`（float）：模型采样温度；默认值 `0.2` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`chat_json`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.chat` → `json.loads` → `LLMClientError` → `isinstance`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | LLMClientError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self.chat、json.loads、LLMClientError、isinstance |
| 复杂度 / 风险 | 分支 2；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-6c3fd6c2e5"></a>

### UNIT-6C3FD6C2E5

**模块**：`src/llm/context.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6C3FD6C2E5 |
| 源码 | [src/llm/context.py](../../../src/llm/context.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/context.py` 的职责，通过 `estimate_payload_size`、`build_llm_context` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_llm_context_compact.py](../../../tests/unit/test_llm_context_compact.py)、[tests/unit/test_llm_context_fact_refs.py](../../../tests/unit/test_llm_context_fact_refs.py) |
| 验证状态 | selected |

#### 函数导航

[_slim_external](#fun-a5b3114ea5) · [_slim_narrative_technical_context](#fun-311efc4821) · [_levels_as_fact_refs](#fun-8860117010) · [_slim_narrative_facts](#fun-8566c1a15c) · [estimate_payload_size](#fun-b49d34199c) · [build_llm_context](#fun-4d78ddfbc7)

<a id="fun-a5b3114ea5"></a>

#### FUN-A5B3114EA5

| 设计项 | 说明 |
|---|---|
| 函数 | `_slim_external` |
| 源码位置 | [src/llm/context.py](../../../src/llm/context.py) · `L28` |
| 签名 | `_slim_external(external: dict[str, Any], derived: dict[str, Any] \| None=None)` |
| 参数 | `external`（dict[str, Any]）：由 `external` 表示的键值映射<br>`derived`（dict[str, Any] \| None）：由 `derived` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`slim_external`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `derived.get` → `external.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | derived.get、external.get |
| 复杂度 / 风险 | 分支 2；跨度 15 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-311efc4821"></a>

#### FUN-311EFC4821

| 设计项 | 说明 |
|---|---|
| 函数 | `_slim_narrative_technical_context` |
| 源码位置 | [src/llm/context.py](../../../src/llm/context.py) · `L45` |
| 签名 | `_slim_narrative_technical_context(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`slim_narrative_technical_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_technical_context` → `full.get` → `isinstance`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_technical_context、full.get、isinstance |
| 复杂度 / 风险 | 分支 2；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8860117010"></a>

#### FUN-8860117010

| 设计项 | 说明 |
|---|---|
| 函数 | `_levels_as_fact_refs` |
| 源码位置 | [src/llm/context.py](../../../src/llm/context.py) · `L61` |
| 签名 | `_levels_as_fact_refs(levels: list[dict[str, Any]], registry: dict[str, Any])` |
| 参数 | `levels`（list[dict[str, Any]]）：候选价格水平集合<br>`registry`（dict[str, Any]）：事实或证据登记映射 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`levels_as_fact_refs`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get` → `fact_lookup` → `out.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | row.get、fact_lookup、float、out.append |
| 复杂度 / 风险 | 分支 3；跨度 15 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8566c1a15c"></a>

#### FUN-8566C1A15C

| 设计项 | 说明 |
|---|---|
| 函数 | `_slim_narrative_facts` |
| 源码位置 | [src/llm/context.py](../../../src/llm/context.py) · `L78` |
| 签名 | `_slim_narrative_facts(facts: dict[str, Any], registry: dict[str, Any])` |
| 参数 | `facts`（dict[str, Any]）：结构化事实集合<br>`registry`（dict[str, Any]）：事实或证据登记映射 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`slim_narrative_facts`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_levels_as_fact_refs` → `slim.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | dict、_levels_as_fact_refs、slim.get |
| 复杂度 / 风险 | 分支 2；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b49d34199c"></a>

#### FUN-B49D34199C

| 设计项 | 说明 |
|---|---|
| 函数 | `estimate_payload_size` |
| 源码位置 | [src/llm/context.py](../../../src/llm/context.py) · `L89` |
| 签名 | `estimate_payload_size(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `dict[str, int]` 类型结果 |
| 职责 | 估算`payload_size`；返回 `dict[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `json.dumps` → `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.dumps、len、round |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_context_compact.py](../../../tests/unit/test_llm_context_compact.py) · 直接动态测试 |

<a id="fun-4d78ddfbc7"></a>

#### FUN-4D78DDFBC7

| 设计项 | 说明 |
|---|---|
| 函数 | `build_llm_context` |
| 源码位置 | [src/llm/context.py](../../../src/llm/context.py) · `L95` |
| 签名 | `build_llm_context(ctx: MarketContext, debate: ResearchDebate, decision: ManagerDecision, report: dict[str, Any])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`debate`（ResearchDebate）：多角色辩论结果<br>`decision`（ManagerDecision）：最终或阶段决策<br>`report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`llm_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `s.get` → `get` → `_slim_narrative_technical_context` → `_slim_external` → `ctx.external.to_dict` → `decision.to_dict` → `fact_ids_for_signal`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、s.get、get、_slim_narrative_technical_context、_slim_external、ctx.external.to_dict、decision.to_dict、fact_ids_for_signal、build_narrative_facts_for_llm、_slim_narrative_facts、registry.get、compact_fact_index、estimate_payload_size |
| 复杂度 / 风险 | 分支 1；跨度 83 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_llm_context_compact.py](../../../tests/unit/test_llm_context_compact.py)、[tests/unit/test_llm_context_fact_refs.py](../../../tests/unit/test_llm_context_fact_refs.py) · 直接动态测试 |

<a id="unit-deb0d517c6"></a>

### UNIT-DEB0D517C6

**模块**：`src/llm/format_io.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DEB0D517C6 |
| 源码 | [src/llm/format_io.py](../../../src/llm/format_io.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/format_io.py` 的职责，通过 `format_llm_output`、`format_messages`、`messages_to_dict` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[format_llm_output](#fun-9200a4bf77) · [format_messages](#fun-0d23896651) · [messages_to_dict](#fun-c67d97c1fe)

<a id="fun-9200a4bf77"></a>

#### FUN-9200A4BF77

| 设计项 | 说明 |
|---|---|
| 函数 | `format_llm_output` |
| 源码位置 | [src/llm/format_io.py](../../../src/llm/format_io.py) · `L9` |
| 签名 | `format_llm_output(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`llm_output`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `text.strip` → `json.dumps` → `json.loads`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | text.strip、json.dumps、json.loads |
| 复杂度 / 风险 | 分支 2；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0d23896651"></a>

#### FUN-0D23896651

| 设计项 | 说明 |
|---|---|
| 函数 | `format_messages` |
| 源码位置 | [src/llm/format_io.py](../../../src/llm/format_io.py) · `L20` |
| 签名 | `format_messages(messages: list[dict[str, str]], *, max_chars: int=12000)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`max_chars`（int）：由 `max_chars` 表示的数值参数；默认值 `12000` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化LLM 消息集合；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `msg.get` → `strip` → `lines.append` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | msg.get、strip、lines.append、join、len |
| 复杂度 / 风险 | 分支 2；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c67d97c1fe"></a>

#### FUN-C67D97C1FE

| 设计项 | 说明 |
|---|---|
| 函数 | `messages_to_dict` |
| 源码位置 | [src/llm/format_io.py](../../../src/llm/format_io.py) · `L32` |
| 签名 | `messages_to_dict(messages: list[dict[str, str]])` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`messages_to_dict`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `m.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | m.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-fbf77b94fb"></a>

### UNIT-FBF77B94FB

**模块**：`src/llm/narrative_output.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FBF77B94FB |
| 源码 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/narrative_output.py` 的职责，通过 `format_llm_narrative` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_narrative_output.py](../../../tests/unit/test_narrative_output.py) |
| 验证状态 | selected |

#### 函数导航

[_try_parse_json](#fun-5605d6120b) · [_pct](#fun-8d01609c7d) · [_lines_to_html](#fun-80154bbc17) · [_fmt_evidence](#fun-2145bad99e) · [_fmt_debate](#fun-1e02af4dd5) · [_fmt_narrative](#fun-76a10bccd6) · [_fmt_generic](#fun-ac5a907908) · [_fmt_analyst_report](#fun-6dab1399aa) · [_fmt_analyst_team](#fun-ebf3493e57) · [_fmt_context](#fun-8d05235fca) · [format_llm_narrative](#fun-3b28d5a15c)

<a id="fun-5605d6120b"></a>

#### FUN-5605D6120B

| 设计项 | 说明 |
|---|---|
| 函数 | `_try_parse_json` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L19` |
| 签名 | `_try_parse_json(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 解析`try_json`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `text.strip` → `text.find` → `text.rfind` → `attempts.append` → `json.loads` → `isinstance` → `re.sub`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | text.strip、text.find、text.rfind、attempts.append、json.loads、isinstance、re.sub |
| 复杂度 / 风险 | 分支 7；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8d01609c7d"></a>

#### FUN-8D01609C7D

| 设计项 | 说明 |
|---|---|
| 函数 | `_pct` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L43` |
| 签名 | `_pct(v: Any)` |
| 参数 | `v`（Any）：由调用方提供的 `v` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`pct`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、max、min |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-80154bbc17"></a>

#### FUN-80154BBC17

| 设计项 | 说明 |
|---|---|
| 函数 | `_lines_to_html` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L51` |
| 签名 | `_lines_to_html(lines: list[str])` |
| 参数 | `lines`（list[str]）：由 `lines` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`lines_to_html`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `escape`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、escape |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2145bad99e"></a>

#### FUN-2145BAD99E

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_evidence` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L57` |
| 签名 | `_fmt_evidence(direction: str, data: dict[str, Any])` |
| 参数 | `direction`（str）：交易方向<br>`data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_evidence`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `data.get` → `_pct` → `isinstance` → `row.get` → `_CATEGORY_CN.get` → `bullets.append` → `escape`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、data.get、_pct、isinstance、row.get、_CATEGORY_CN.get、bullets.append、escape、parts.append、_lines_to_html、join |
| 复杂度 / 风险 | 分支 7；跨度 25 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1e02af4dd5"></a>

#### FUN-1E02AF4DD5

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_debate` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L84` |
| 签名 | `_fmt_debate(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_debate`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_BIAS_CN.get` → `lower` → `data.get` → `_pct` → `strip` → `isinstance` → `escape` → `parts.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _BIAS_CN.get、lower、str、data.get、_pct、strip、isinstance、escape、parts.append、_lines_to_html、join |
| 复杂度 / 风险 | 分支 3；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-76a10bccd6"></a>

#### FUN-76A10BCCD6

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_narrative` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L100` |
| 签名 | `_fmt_narrative(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_narrative`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `data.get` → `parts.append` → `escape` → `ln.strip` → `v.splitlines` → `_lines_to_html` → `isinstance`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、data.get、parts.append、escape、ln.strip、v.splitlines、_lines_to_html、isinstance、_pct、join |
| 复杂度 / 风险 | 分支 7；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ac5a907908"></a>

#### FUN-AC5A907908

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_generic` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L122` |
| 签名 | `_fmt_generic(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_generic`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.items` → `isinstance` → `strip` → `lines.append` → `_lines_to_html`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.items、isinstance、strip、str、lines.append、_lines_to_html |
| 复杂度 / 风险 | 分支 4；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6dab1399aa"></a>

#### FUN-6DAB1399AA

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_analyst_report` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L135` |
| 签名 | `_fmt_analyst_report(title: str, data: dict[str, Any])` |
| 参数 | `title`（str）：由 `title` 表示的文本或标识<br>`data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_analyst_report`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_BIAS_CN.get` → `lower` → `data.get` → `strip` → `_pct` → `isinstance` → `row.get` → `_CATEGORY_CN.get`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _BIAS_CN.get、lower、str、data.get、strip、_pct、isinstance、row.get、_CATEGORY_CN.get、bullets.append、escape、parts.append、_lines_to_html、join |
| 复杂度 / 风险 | 分支 7；跨度 27 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ebf3493e57"></a>

#### FUN-EBF3493E57

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_analyst_team` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L172` |
| 签名 | `_fmt_analyst_team(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_analyst_team`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `labels.items` → `data.get` → `isinstance` → `_BIAS_CN.get` → `lower` → `report.get` → `strip` → `_pct`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | labels.items、data.get、isinstance、_BIAS_CN.get、lower、str、report.get、strip、_pct、len、parts.append、escape、join |
| 复杂度 / 风险 | 分支 4；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8d05235fca"></a>

#### FUN-8D05235FCA

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_context` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L196` |
| 签名 | `_fmt_context(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_context`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.get` → `escape` → `isinstance` → `join` → `parts.append` → `strip` → `ext.get` → `p.get`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.get、escape、str、int、isinstance、join、parts.append、strip、ext.get、len、p.get |
| 复杂度 / 风险 | 分支 6；跨度 43 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3b28d5a15c"></a>

#### FUN-3B28D5A15C

| 设计项 | 说明 |
|---|---|
| 函数 | `format_llm_narrative` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L241` |
| 签名 | `format_llm_narrative(stage: str, raw: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`llm_narrative`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `raw.strip` → `_try_parse_json` → `escape` → `_fmt_evidence` → `_fmt_debate` → `_fmt_analyst_team` → `_fmt_context` → `_fmt_analyst_report`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | raw.strip、_try_parse_json、escape、len、_fmt_evidence、_fmt_debate、_fmt_analyst_team、_fmt_context、_fmt_analyst_report、_fmt_narrative、_fmt_generic |
| 复杂度 / 风险 | 分支 10；跨度 29 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_output.py](../../../tests/unit/test_narrative_output.py) · 直接动态测试 |

<a id="unit-a605fcb3a9"></a>

### UNIT-A605FCB3A9

**模块**：`src/llm/prompts.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A605FCB3A9 |
| 源码 | [src/llm/prompts.py](../../../src/llm/prompts.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/prompts.py` 的职责，通过 `build_messages` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[_observation_hint](#fun-ec14c06c57) · [build_messages](#fun-b5e78a9a6d)

<a id="fun-ec14c06c57"></a>

#### FUN-EC14C06C57

| 设计项 | 说明 |
|---|---|
| 函数 | `_observation_hint` |
| 源码位置 | [src/llm/prompts.py](../../../src/llm/prompts.py) · `L63` |
| 签名 | `_observation_hint(context: dict[str, Any])` |
| 参数 | `context`（dict[str, Any]）：运行上下文 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`observation_hint`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `context.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | context.get |
| 复杂度 / 风险 | 分支 1；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b5e78a9a6d"></a>

#### FUN-B5E78A9A6D

| 设计项 | 说明 |
|---|---|
| 函数 | `build_messages` |
| 源码位置 | [src/llm/prompts.py](../../../src/llm/prompts.py) · `L74` |
| 签名 | `build_messages(context: dict[str, Any])` |
| 参数 | `context`（dict[str, Any]）：运行上下文 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 构建LLM 消息集合；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_observation_hint` → `json.dumps`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _observation_hint、json.dumps |
| 复杂度 / 风险 | 分支 0；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-6568b95afa"></a>

### UNIT-6568B95AFA

**模块**：`src/llm/router.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6568B95AFA |
| 源码 | [src/llm/router.py](../../../src/llm/router.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/router.py` 的职责，通过 `client_for_model`、`get_fast_client`、`get_strong_client`、`get_debate_client`、`client_for_stage`、`routing_meta`、`llm_configured` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[client_for_model](#fun-1b26737be4) · [get_fast_client](#fun-c1648afe95) · [get_strong_client](#fun-b6cefe1540) · [get_debate_client](#fun-99cb06f377) · [client_for_stage](#fun-4719de86ff) · [routing_meta](#fun-dc9786297e) · [llm_configured](#fun-32ab5acbe0)

<a id="fun-1b26737be4"></a>

#### FUN-1B26737BE4

| 设计项 | 说明 |
|---|---|
| 函数 | `client_for_model` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L19` |
| 签名 | `client_for_model(model: str)` |
| 参数 | `model`（str）：模型名称或模型对象 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 生成`client_for_model`结果；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `LLMClient`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | LLMClient |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c1648afe95"></a>

#### FUN-C1648AFE95

| 设计项 | 说明 |
|---|---|
| 函数 | `get_fast_client` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L30` |
| 签名 | `get_fast_client()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 获取`fast_client`；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_model`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_model |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py) · 直接动态测试 |

<a id="fun-b6cefe1540"></a>

#### FUN-B6CEFE1540

| 设计项 | 说明 |
|---|---|
| 函数 | `get_strong_client` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L34` |
| 签名 | `get_strong_client()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 获取`strong_client`；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `client_for_model`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | client_for_model |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py) · 直接动态测试 |

<a id="fun-99cb06f377"></a>

#### FUN-99CB06F377

| 设计项 | 说明 |
|---|---|
| 函数 | `get_debate_client` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L38` |
| 签名 | `get_debate_client()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 获取`debate_client`；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_fast_client` → `get_strong_client`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_fast_client、get_strong_client |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py) · 直接动态测试 |

<a id="fun-4719de86ff"></a>

#### FUN-4719DE86FF

| 设计项 | 说明 |
|---|---|
| 函数 | `client_for_stage` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L45` |
| 签名 | `client_for_stage(stage: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 生成`client_for_stage`结果；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_stage_policy` → `get_fast_client` → `client_for_model` → `get_debate_client` → `get_strong_client`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_stage_policy、get_fast_client、client_for_model、get_debate_client、get_strong_client |
| 复杂度 / 风险 | 分支 3；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-dc9786297e"></a>

#### FUN-DC9786297E

| 设计项 | 说明 |
|---|---|
| 函数 | `routing_meta` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L57` |
| 签名 | `routing_meta()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 构建`routing_meta`；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_routing_strategy`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_routing_strategy |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-32ab5acbe0"></a>

#### FUN-32AB5ACBE0

| 设计项 | 说明 |
|---|---|
| 函数 | `llm_configured` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L62` |
| 签名 | `llm_configured()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_configured`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-e488978a91"></a>

### UNIT-E488978A91

**模块**：`src/llm/stage_policy.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E488978A91 |
| 源码 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | 实现“LLM 传输、上下文和策略”组件中 `src/llm/stage_policy.py` 的职责，通过 `StagePolicy`、`get_stage_policy`、`estimate_messages_size`、`estimate_text_size`、`apply_input_budget`、`build_routing_strategy` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 8 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

[StagePolicy.to_dict](#fun-8a092a53c7) · [_default_attempts](#fun-16718e4e98) · [_policies](#fun-500b8f3420) · [get_stage_policy](#fun-1d1021888e) · [estimate_messages_size](#fun-931519418f) · [estimate_text_size](#fun-288812bac3) · [apply_input_budget](#fun-639af5aafb) · [build_routing_strategy](#fun-e3b03c5e15)

<a id="fun-8a092a53c7"></a>

#### FUN-8A092A53C7

| 设计项 | 说明 |
|---|---|
| 函数 | `StagePolicy.to_dict` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L39` |
| 签名 | `StagePolicy.to_dict(self)` |
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

<a id="fun-16718e4e98"></a>

#### FUN-16718E4E98

| 设计项 | 说明 |
|---|---|
| 函数 | `_default_attempts` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L43` |
| 签名 | `_default_attempts()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`default_attempts`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、int |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-500b8f3420"></a>

#### FUN-500B8F3420

| 设计项 | 说明 |
|---|---|
| 函数 | `_policies` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L48` |
| 签名 | `_policies()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, StagePolicy]` 类型结果 |
| 职责 | 构建`policies`；返回 `dict[str, StagePolicy]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_default_attempts` → `StagePolicy`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, StagePolicy]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _default_attempts、int、StagePolicy |
| 复杂度 / 风险 | 分支 0；跨度 41 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1d1021888e"></a>

#### FUN-1D1021888E

| 设计项 | 说明 |
|---|---|
| 函数 | `get_stage_policy` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L91` |
| 签名 | `get_stage_policy(stage: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `StagePolicy` 类型结果 |
| 职责 | 获取`stage_policy`；返回 `StagePolicy` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_policies` → `_default_attempts` → `StagePolicy`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `StagePolicy` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _policies、_default_attempts、StagePolicy、int |
| 复杂度 / 风险 | 分支 1；跨度 14 行；中 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="fun-931519418f"></a>

#### FUN-931519418F

| 设计项 | 说明 |
|---|---|
| 函数 | `estimate_messages_size` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L107` |
| 签名 | `estimate_messages_size(messages: list[dict[str, str]])` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列 |
| 返回 | 返回 `dict[str, int]` 类型结果 |
| 职责 | 估算`messages_size`；返回 `dict[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `m.get` → `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、len、str、m.get、int、round |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-288812bac3"></a>

#### FUN-288812BAC3

| 设计项 | 说明 |
|---|---|
| 函数 | `estimate_text_size` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L115` |
| 签名 | `estimate_text_size(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `dict[str, int]` 类型结果 |
| 职责 | 估算`text_size`；返回 `dict[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、int、round |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-639af5aafb"></a>

#### FUN-639AF5AAFB

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_input_budget` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L123` |
| 签名 | `apply_input_budget(messages: list[dict[str, str]], policy: StagePolicy)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`policy`（StagePolicy）：由调用方提供的 `policy` 输入对象 |
| 返回 | 返回 `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]` 类型结果 |
| 职责 | 应用`input_budget`；返回 `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `estimate_messages_size` → `enumerate` → `m.get` → `range` → `max` → `get` → `meta.update`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | estimate_messages_size、dict、enumerate、m.get、list、range、len、max、str、get、meta.update |
| 复杂度 / 风险 | 分支 5；跨度 54 行；中 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="fun-e3b03c5e15"></a>

#### FUN-E3B03C5E15

| 设计项 | 说明 |
|---|---|
| 函数 | `build_routing_strategy` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L179` |
| 签名 | `build_routing_strategy()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`routing_strategy`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `p.to_dict` → `items` → `_policies`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | p.to_dict、items、_policies |
| 复杂度 / 风险 | 分支 1；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |
