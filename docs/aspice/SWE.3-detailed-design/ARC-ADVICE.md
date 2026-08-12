# ARC-ADVICE — Human-review advice engine

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-advice)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/advice/__init__.py](#unit-928784da94) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/advice/audit.py](#unit-f6d48540e6) | 1 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/advice/engine.py](#unit-56f8ff3b61) | 15 | 15 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/advice/llm.py](#unit-ba683051ba) | 5 | 5 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/advice/report.py](#unit-acc548aba0) | 2 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/advice/types.py](#unit-d41345d767) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-928784da94"></a>

### UNIT-928784DA94

**模块**：`src/advice/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-928784DA94 |
| 源码 | [src/advice/__init__.py](../../../src/advice/__init__.py) |
| 架构组件 | ARC-ADVICE — Human-review advice engine |
| 职责 | 实现“Human-review advice engine”组件中 `src/advice/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ADV-001](../SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](../SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-f6d48540e6"></a>

### UNIT-F6D48540E6

**模块**：`src/advice/audit.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F6D48540E6 |
| 源码 | [src/advice/audit.py](../../../src/advice/audit.py) |
| 架构组件 | ARC-ADVICE — Human-review advice engine |
| 职责 | 实现“Human-review advice engine”组件中 `src/advice/audit.py` 的职责，通过 `audit_advice` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ADV-001](../SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](../SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [audit_advice](#fun-c3bb71e51c) | 生成`audit_advice`结果；返回 `AdviceAudit` 类型结果。 | 未检测到直接副作用 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |

#### 函数导航

[audit_advice](#fun-c3bb71e51c)

<a id="fun-c3bb71e51c"></a>

#### FUN-C3BB71E51C

| 设计项 | 说明 |
|---|---|
| 函数 | `audit_advice` |
| 源码位置 | [src/advice/audit.py](../../../src/advice/audit.py) · `L8` |
| 签名 | `audit_advice(packet: AdvicePacket)` |
| 参数 | `packet`（AdvicePacket）：由调用方提供的 `packet` 输入对象 |
| 返回 | 返回 `AdviceAudit` 类型结果 |
| 职责 | 生成`audit_advice`结果；返回 `AdviceAudit` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `violations.append` → `warnings.append` → `AdviceAudit` → `any` → `max` → `sorted` → `join`；包含 18 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AdviceAudit` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | violations.append、warnings.append、AdviceAudit、any、max、sorted、set、join |
| 复杂度 / 风险 | 分支 18；跨度 49 行；高 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) · 直接动态测试 |

<a id="unit-56f8ff3b61"></a>

### UNIT-56F8FF3B61

**模块**：`src/advice/engine.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-56F8FF3B61 |
| 源码 | [src/advice/engine.py](../../../src/advice/engine.py) |
| 架构组件 | ARC-ADVICE — Human-review advice engine |
| 职责 | 实现“Human-review advice engine”组件中 `src/advice/engine.py` 的职责，通过 `build_advice_packet` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ADV-001](../SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](../SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 15 / 15 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_bias](#fun-1f215990ac) | 构建`bias`；返回 `tuple[str, str, list[str]]` 类型结果。 | 未检测到直接副作用 | — |
| [_trend_cn](#fun-01c7dd3b96) | 生成`trend_cn`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | — |
| [_level_bounds](#fun-777cd0539b) | 构建`level_bounds`；返回 `tuple[float, float]` 类型结果。 | 未检测到直接副作用 | — |
| [_source_family](#fun-1452f32fb1) | 生成`source_family`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | — |
| [_evidence_id](#fun-51fa733f1a) | 生成`evidence_id`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | — |
| [_cluster_levels](#fun-617accc6a0) | 构建`cluster_levels`；返回 `list[list[dict[str, Any]]]` 类型结果。 | 未检测到直接副作用 | — |
| [_cluster_rank](#fun-b8c6253015) | 构建`cluster_rank`；返回 `tuple[int, float, float]` 类型结果。 | 未检测到直接副作用 | — |
| [_pick_cluster](#fun-38f9bc2124) | 构建`pick_cluster`；返回 `list[dict[str, Any]] \| None` 类型结果。 | 未检测到直接副作用 | — |
| [_zone_from_cluster](#fun-a9180d19b6) | 根据`cluster`构建`zone`；返回 `AttentionZone` 类型结果。 | 未检测到直接副作用 | — |
| [_target_prices](#fun-b96b4d78f2) | 构建`target_prices`；返回 `list[float]` 类型结果。 | 未检测到直接副作用 | — |
| [_rr](#fun-65829e56d4) | 构建`rr`；返回 `list[float]` 类型结果。 | 未检测到直接副作用 | — |
| [_human_checklist](#fun-324d833370) | 构建`human_checklist`；返回 `list[str]` 类型结果。 | 未检测到直接副作用 | — |
| [_risks](#fun-31108e0f15) | 构建`risks`；返回 `list[str]` 类型结果。 | 未检测到直接副作用 | — |
| [_no_setup_packet](#fun-5de4f49a87) | 生成`no_setup_packet`结果；返回 `AdvicePacket` 类型结果。 | 未检测到直接副作用 | — |
| [build_advice_packet](#fun-8b9a1cc80c) | 构建`advice_packet`；返回 `AdvicePacket` 类型结果。 | 未检测到直接副作用 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |

#### 函数导航

[_bias](#fun-1f215990ac) · [_trend_cn](#fun-01c7dd3b96) · [_level_bounds](#fun-777cd0539b) · [_source_family](#fun-1452f32fb1) · [_evidence_id](#fun-51fa733f1a) · [_cluster_levels](#fun-617accc6a0) · [_cluster_rank](#fun-b8c6253015) · [_pick_cluster](#fun-38f9bc2124) · [_zone_from_cluster](#fun-a9180d19b6) · [_target_prices](#fun-b96b4d78f2) · [_rr](#fun-65829e56d4) · [_human_checklist](#fun-324d833370) · [_risks](#fun-31108e0f15) · [_no_setup_packet](#fun-5de4f49a87) · [build_advice_packet](#fun-8b9a1cc80c)

<a id="fun-1f215990ac"></a>

#### FUN-1F215990AC

| 设计项 | 说明 |
|---|---|
| 函数 | `_bias` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L28` |
| 签名 | `_bias(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `tuple[str, str, list[str]]` 类型结果 |
| 职责 | 构建`bias`；返回 `tuple[str, str, list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `ctx.analyses.get` → `_trend_cn`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str, list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、ctx.analyses.get、_trend_cn |
| 复杂度 / 风险 | 分支 5；跨度 19 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-01c7dd3b96"></a>

#### FUN-01C7DD3B96

| 设计项 | 说明 |
|---|---|
| 函数 | `_trend_cn` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L49` |
| 签名 | `_trend_cn(value: str)` |
| 参数 | `value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`trend_cn`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-777cd0539b"></a>

#### FUN-777CD0539B

| 设计项 | 说明 |
|---|---|
| 函数 | `_level_bounds` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L53` |
| 签名 | `_level_bounds(row: dict[str, Any])` |
| 参数 | `row`（dict[str, Any]）：当前记录行 |
| 返回 | 返回 `tuple[float, float]` 类型结果 |
| 职责 | 构建`level_bounds`；返回 `tuple[float, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get` → `min` → `max`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、row.get、min、max |
| 复杂度 / 风险 | 分支 2；跨度 5 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1452f32fb1"></a>

#### FUN-1452F32FB1

| 设计项 | 说明 |
|---|---|
| 函数 | `_source_family` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L60` |
| 签名 | `_source_family(row: dict[str, Any])` |
| 参数 | `row`（dict[str, Any]）：当前记录行 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`source_family`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get` → `source.split`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、row.get、source.split |
| 复杂度 / 风险 | 分支 0；跨度 3 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-51fa733f1a"></a>

#### FUN-51FA733F1A

| 设计项 | 说明 |
|---|---|
| 函数 | `_evidence_id` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L65` |
| 签名 | `_evidence_id(row: dict[str, Any], index: int)` |
| 参数 | `row`（dict[str, Any]）：当前记录行<br>`index`（int）：由 `index` 表示的数值参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`evidence_id`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get` → `_source_family`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、row.get、_source_family、float |
| 复杂度 / 风险 | 分支 0；跨度 5 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-617accc6a0"></a>

#### FUN-617ACCC6A0

| 设计项 | 说明 |
|---|---|
| 函数 | `_cluster_levels` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L72` |
| 签名 | `_cluster_levels(rows: list[dict[str, Any]], *, tolerance: float)` |
| 参数 | `rows`（list[dict[str, Any]]）：记录行集合<br>`tolerance`（float）：数值比较容差 |
| 返回 | 返回 `list[list[dict[str, Any]]]` 类型结果 |
| 职责 | 构建`cluster_levels`；返回 `list[list[dict[str, Any]]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `item.get` → `row.get` → `next` → `abs` → `sum` → `x.get` → `clusters.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[list[dict[str, Any]]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、float、item.get、row.get、next、abs、sum、x.get、len、clusters.append、matched.append |
| 复杂度 / 风险 | 分支 2；跨度 22 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b8c6253015"></a>

#### FUN-B8C6253015

| 设计项 | 说明 |
|---|---|
| 函数 | `_cluster_rank` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L96` |
| 签名 | `_cluster_rank(cluster: list[dict[str, Any]], price: float)` |
| 参数 | `cluster`（list[dict[str, Any]]）：由 `cluster` 表示的输入集合<br>`price`（float）：当前或待评估价格 |
| 返回 | 返回 `tuple[int, float, float]` 类型结果 |
| 职责 | 构建`cluster_rank`；返回 `tuple[int, float, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_source_family` → `row.get` → `sum` → `abs`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[int, float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _source_family、str、row.get、sum、float、len、abs |
| 复杂度 / 风险 | 分支 0；跨度 7 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-38f9bc2124"></a>

#### FUN-38F9BC2124

| 设计项 | 说明 |
|---|---|
| 函数 | `_pick_cluster` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L105` |
| 签名 | `_pick_cluster(rows: list[dict[str, Any]], *, direction: str, price: float, tolerance: float, max_distance: float)` |
| 参数 | `rows`（list[dict[str, Any]]）：记录行集合<br>`direction`（str）：交易方向<br>`price`（float）：当前或待评估价格<br>`tolerance`（float）：数值比较容差<br>`max_distance`（float）：由 `max_distance` 表示的数值参数 |
| 返回 | 返回 `list[dict[str, Any]] \| None` 类型结果 |
| 职责 | 构建`pick_cluster`；返回 `list[dict[str, Any]] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_level_bounds` → `eligible.append` → `_cluster_levels` → `_source_family` → `row.get` → `max` → `_cluster_rank`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _level_bounds、eligible.append、_cluster_levels、len、_source_family、str、row.get、max、_cluster_rank |
| 复杂度 / 风险 | 分支 4；跨度 26 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a9180d19b6"></a>

#### FUN-A9180D19B6

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_from_cluster` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L133` |
| 签名 | `_zone_from_cluster(cluster: list[dict[str, Any]])` |
| 参数 | `cluster`（list[dict[str, Any]]）：由 `cluster` 表示的输入集合 |
| 返回 | 返回 `AttentionZone` 类型结果 |
| 职责 | 根据`cluster`构建`zone`；返回 `AttentionZone` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_level_bounds` → `min` → `max` → `row.get` → `labels.append` → `AttentionZone` → `round` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AttentionZone` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _level_bounds、min、max、str、row.get、labels.append、AttentionZone、round、join |
| 复杂度 / 风险 | 分支 2；跨度 10 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b96b4d78f2"></a>

#### FUN-B96B4D78F2

| 设计项 | 说明 |
|---|---|
| 函数 | `_target_prices` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L145` |
| 签名 | `_target_prices(rows: list[dict[str, Any]], *, direction: str, zone: AttentionZone, tolerance: float)` |
| 参数 | `rows`（list[dict[str, Any]]）：记录行集合<br>`direction`（str）：交易方向<br>`zone`（AttentionZone）：由调用方提供的 `zone` 输入对象<br>`tolerance`（float）：数值比较容差 |
| 返回 | 返回 `list[float]` 类型结果 |
| 职责 | 构建`target_prices`；返回 `list[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_cluster_levels` → `sum` → `row.get` → `candidates.append` → `sorted` → `round`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _cluster_levels、sum、float、row.get、len、candidates.append、sorted、set、round |
| 复杂度 / 风险 | 分支 3；跨度 16 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-65829e56d4"></a>

#### FUN-65829E56D4

| 设计项 | 说明 |
|---|---|
| 函数 | `_rr` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L163` |
| 签名 | `_rr(direction: str, zone: AttentionZone, invalidation: float, targets: list[float])` |
| 参数 | `direction`（str）：交易方向<br>`zone`（AttentionZone）：由调用方提供的 `zone` 输入对象<br>`invalidation`（float）：由 `invalidation` 表示的数值参数<br>`targets`（list[float]）：由 `targets` 表示的输入集合 |
| 返回 | 返回 `list[float]` 类型结果 |
| 职责 | 构建`rr`；返回 `list[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `max`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、max |
| 复杂度 / 风险 | 分支 3；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-324d833370"></a>

#### FUN-324D833370

| 设计项 | 说明 |
|---|---|
| 函数 | `_human_checklist` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L174` |
| 签名 | `_human_checklist(direction: str, zone: AttentionZone)` |
| 参数 | `direction`（str）：交易方向<br>`zone`（AttentionZone）：由调用方提供的 `zone` 输入对象 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`human_checklist`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 13 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-31108e0f15"></a>

#### FUN-31108E0F15

| 设计项 | 说明 |
|---|---|
| 函数 | `_risks` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L189` |
| 签名 | `_risks(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`risks`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `risks.append` → `ctx.analyses.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、risks.append、ctx.analyses.get、str |
| 复杂度 / 风险 | 分支 3；跨度 11 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5de4f49a87"></a>

#### FUN-5DE4F49A87

| 设计项 | 说明 |
|---|---|
| 函数 | `_no_setup_packet` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L202` |
| 签名 | `_no_setup_packet(*, decision: str, bias: str, confidence: str, price: float, context: list[str], summary: str, risks: list[str], uncertainties: list[str], evidence: list[AdviceEvidence])` |
| 参数 | `decision`（str）：最终或阶段决策<br>`bias`（str）：由 `bias` 表示的文本或标识<br>`confidence`（str）：由 `confidence` 表示的文本或标识<br>`price`（float）：当前或待评估价格<br>`context`（list[str]）：运行上下文<br>`summary`（str）：摘要内容<br>`risks`（list[str]）：由 `risks` 表示的输入集合<br>`uncertainties`（list[str]）：由 `uncertainties` 表示的输入集合<br>`evidence`（list[AdviceEvidence]）：由 `evidence` 表示的输入集合 |
| 返回 | 返回 `AdvicePacket` 类型结果 |
| 职责 | 生成`no_setup_packet`结果；返回 `AdvicePacket` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `AdvicePacket` → `round` → `replace` → `audit_advice`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AdvicePacket` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | AdvicePacket、round、replace、audit_advice |
| 复杂度 / 风险 | 分支 0；跨度 27 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8b9a1cc80c"></a>

#### FUN-8B9A1CC80C

| 设计项 | 说明 |
|---|---|
| 函数 | `build_advice_packet` |
| 源码位置 | [src/advice/engine.py](../../../src/advice/engine.py) · `L231` |
| 签名 | `build_advice_packet(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `AdvicePacket` 类型结果 |
| 职责 | 构建`advice_packet`；返回 `AdvicePacket` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_bias` → `AdviceEvidence` → `_TF_CN.get` → `_trend_cn` → `ctx.analyses.get` → `_risks` → `build_data_as_of` → `ctx.derived.get`；包含 17 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `AdvicePacket` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_bias、AdviceEvidence、_TF_CN.get、_trend_cn、ctx.analyses.get、_risks、build_data_as_of、ctx.derived.get、freshness.get、_no_setup_packet、list、support_resistance_context、getattr、max、_pick_cluster、_zone_from_cluster、_target_prices、round、enumerate |
| 复杂度 / 风险 | 分支 17；跨度 168 行；高 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) · 直接动态测试 |

<a id="unit-ba683051ba"></a>

### UNIT-BA683051BA

**模块**：`src/advice/llm.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-BA683051BA |
| 源码 | [src/advice/llm.py](../../../src/advice/llm.py) |
| 架构组件 | ARC-ADVICE — Human-review advice engine |
| 职责 | 实现“Human-review advice engine”组件中 `src/advice/llm.py` 的职责，通过 `enhance_advice` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ADV-001](../SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](../SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 5 / 5 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_strings](#fun-aa090923df) | 构建`strings`；返回 `list[str]` 类型结果。 | 未检测到直接副作用 | — |
| [_parse](#fun-590c9e4d9e) | 解析输入内容；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |
| [_allowed_prices](#fun-f2b5b5b5e2) | 构建`allowed_prices`；返回 `list[float]` 类型结果。 | 未检测到直接副作用 | — |
| [_assert_no_new_prices](#fun-0a13c3956f) | 执行`assert_no_new_prices`处理；无返回值（None）。 | 未检测到直接副作用 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |
| [enhance_advice](#fun-592b6da4fa) | 构建`enhance_advice`；返回 `tuple[AdvicePacket, LLMStageTrace \| None]` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[_strings](#fun-aa090923df) · [_parse](#fun-590c9e4d9e) · [_allowed_prices](#fun-f2b5b5b5e2) · [_assert_no_new_prices](#fun-0a13c3956f) · [enhance_advice](#fun-592b6da4fa)

<a id="fun-aa090923df"></a>

#### FUN-AA090923DF

| 设计项 | 说明 |
|---|---|
| 函数 | `_strings` |
| 源码位置 | [src/advice/llm.py](../../../src/advice/llm.py) · `L34` |
| 签名 | `_strings(value: Any, *, limit: int, field: str)` |
| 参数 | `value`（Any）：待处理值<br>`limit`（int）：返回或处理数量上限<br>`field`（str）：由 `field` 表示的文本或标识 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`strings`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `ValueError` → `strip`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、ValueError、strip、str、len |
| 复杂度 / 风险 | 分支 3；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-590c9e4d9e"></a>

#### FUN-590C9E4D9E

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse` |
| 源码位置 | [src/advice/llm.py](../../../src/advice/llm.py) · `L45` |
| 签名 | `_parse(data: dict[str, Any], *, has_setup: bool)` |
| 参数 | `data`（dict[str, Any]）：输入数据<br>`has_setup`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 解析输入内容；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `data.get` → `ValueError` → `_strings`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、data.get、ValueError、_strings |
| 复杂度 / 风险 | 分支 3；跨度 19 行；高 |
| 测试 / 验证 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) · 直接动态测试 |

<a id="fun-f2b5b5b5e2"></a>

#### FUN-F2B5B5B5E2

| 设计项 | 说明 |
|---|---|
| 函数 | `_allowed_prices` |
| 源码位置 | [src/advice/llm.py](../../../src/advice/llm.py) · `L66` |
| 签名 | `_allowed_prices(packet: AdvicePacket)` |
| 参数 | `packet`（AdvicePacket）：由调用方提供的 `packet` 输入对象 |
| 返回 | 返回 `list[float]` 类型结果 |
| 职责 | 构建`allowed_prices`；返回 `list[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values.extend`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | values.extend |
| 复杂度 / 风险 | 分支 1；跨度 13 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0a13c3956f"></a>

#### FUN-0A13C3956F

| 设计项 | 说明 |
|---|---|
| 函数 | `_assert_no_new_prices` |
| 源码位置 | [src/advice/llm.py](../../../src/advice/llm.py) · `L81` |
| 签名 | `_assert_no_new_prices(payload: dict[str, Any], allowed: list[float])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷<br>`allowed`（list[float]）：由 `allowed` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 执行`assert_no_new_prices`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `json.dumps` → `raw.replace` → `re.findall` → `any` → `abs` → `ValueError` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.dumps、float、raw.replace、re.findall、any、abs、ValueError、join |
| 复杂度 / 风险 | 分支 1；跨度 7 行；高 |
| 测试 / 验证 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) · 直接动态测试 |

<a id="fun-592b6da4fa"></a>

#### FUN-592B6DA4FA

| 设计项 | 说明 |
|---|---|
| 函数 | `enhance_advice` |
| 源码位置 | [src/advice/llm.py](../../../src/advice/llm.py) · `L90` |
| 签名 | `enhance_advice(packet: AdvicePacket)` |
| 参数 | `packet`（AdvicePacket）：由调用方提供的 `packet` 输入对象 |
| 返回 | 返回 `tuple[AdvicePacket, LLMStageTrace \| None]` 类型结果 |
| 职责 | 构建`enhance_advice`；返回 `tuple[AdvicePacket, LLMStageTrace \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `llm_configured` → `client_for_stage` → `json.dumps` → `packet.to_dict` → `run_llm_stage` → `_parse` → `_assert_no_new_prices` → `_allowed_prices`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[AdvicePacket, LLMStageTrace \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm_configured、client_for_stage、json.dumps、packet.to_dict、run_llm_stage、_parse、_assert_no_new_prices、_allowed_prices、replace、audit_advice、ValueError、join |
| 复杂度 / 风险 | 分支 4；跨度 43 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-acc548aba0"></a>

### UNIT-ACC548ABA0

**模块**：`src/advice/report.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-ACC548ABA0 |
| 源码 | [src/advice/report.py](../../../src/advice/report.py) |
| 架构组件 | ARC-ADVICE — Human-review advice engine |
| 职责 | 实现“Human-review advice engine”组件中 `src/advice/report.py` 的职责，通过 `build_advice_report` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ADV-001](../SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](../SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_external_context](#fun-063288e260) | 构建`external_context`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | — |
| [build_advice_report](#fun-fc0343e620) | 构建`advice_report`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) |

#### 函数导航

[_external_context](#fun-063288e260) · [build_advice_report](#fun-fc0343e620)

<a id="fun-063288e260"></a>

#### FUN-063288E260

| 设计项 | 说明 |
|---|---|
| 函数 | `_external_context` |
| 源码位置 | [src/advice/report.py](../../../src/advice/report.py) · `L15` |
| 签名 | `_external_context(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`external_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.to_dict`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | row.to_dict、list |
| 复杂度 / 风险 | 分支 0；跨度 11 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fc0343e620"></a>

#### FUN-FC0343E620

| 设计项 | 说明 |
|---|---|
| 函数 | `build_advice_report` |
| 源码位置 | [src/advice/report.py](../../../src/advice/report.py) · `L28` |
| 签名 | `build_advice_report(ctx: MarketContext, advice: AdvicePacket, *, run_id: str, run_config: dict[str, Any])` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`advice`（AdvicePacket）：由调用方提供的 `advice` 输入对象<br>`run_id`（str）：对象标识<br>`run_config`（dict[str, Any]）：运行配置 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`advice_report`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_data_as_of` → `ctx.derived.get` → `timeframe_context` → `ctx.analyses.get` → `format_utc8` → `isoformat` → `datetime.now` → `advice.to_dict`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_data_as_of、ctx.derived.get、timeframe_context、ctx.analyses.get、format_utc8、isoformat、datetime.now、dict、advice.to_dict、support_resistance_context、_external_context |
| 复杂度 / 风险 | 分支 0；跨度 34 行；高 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py) · 直接动态测试 |

<a id="unit-d41345d767"></a>

### UNIT-D41345D767

**模块**：`src/advice/types.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D41345D767 |
| 源码 | [src/advice/types.py](../../../src/advice/types.py) |
| 架构组件 | ARC-ADVICE — Human-review advice engine |
| 职责 | 实现“Human-review advice engine”组件中 `src/advice/types.py` 的职责，通过 `AdviceEvidence`、`AttentionZone`、`AdviceSetup`、`AlternativeScenario`、`AdviceAudit`、`AdvicePacket` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ADV-001](../SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](../SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

[AdvicePacket.to_dict](#fun-08df603ff8)

<a id="fun-08df603ff8"></a>

#### FUN-08DF603FF8

| 设计项 | 说明 |
|---|---|
| 函数 | `AdvicePacket.to_dict` |
| 源码位置 | [src/advice/types.py](../../../src/advice/types.py) · `L75` |
| 签名 | `AdvicePacket.to_dict(self)` |
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
