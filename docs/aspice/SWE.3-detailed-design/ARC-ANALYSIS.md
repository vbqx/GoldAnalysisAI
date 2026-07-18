# ARC-ANALYSIS — 事实、结构、信号与报告门禁

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-analysis)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/analysis/__init__.py](#unit-cf43fe46e5) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/audit_summary.py](#unit-9f95d55376) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/chart_sr_filters.py](#unit-271badecbe) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/chart_zone_filters.py](#unit-070aa8511c) | 8 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/claim_eligibility.py](#unit-67d22a7c31) | 14 | 14 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/data_freshness.py](#unit-3549e9d9b7) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/dgt_price_action.py](#unit-7dfc57faf9) | 10 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/display_labels.py](#unit-3b1598dc1b) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/fact_registry.py](#unit-60e70e7439) | 16 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/field_glossary.py](#unit-c37864f306) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/ict_pa.py](#unit-3962aaac44) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/level_validator.py](#unit-a9ae5e6696) | 7 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/luxalgo_smc.py](#unit-2f7fedba6f) | 15 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/narrative_combine.py](#unit-4f106aec16) | 15 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/narrative_facts.py](#unit-b5b5d80eb7) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/narrative_sections.py](#unit-0d14c54b60) | 28 | 4 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/plan_signals.py](#unit-406cec1297) | 20 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/price_action_facts.py](#unit-daf97d09e5) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/proximity.py](#unit-ce01c0290c) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_engine.py](#unit-dad8a91ff9) | 44 | 8 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_facts.py](#unit-cd6da8c4a3) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_invariant_gate.py](#unit-1aecfa1072) | 4 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_invariants.py](#unit-70bd327d9d) | 13 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_reliability.py](#unit-07e7315842) | 11 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/risk_gates.py](#unit-0cc0e8d72a) | 6 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/signal_geometry.py](#unit-84723142fa) | 3 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/signal_identity.py](#unit-c8f58d21e1) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/technical_context.py](#unit-7faaa8edca) | 17 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/tf_snapshot.py](#unit-ebf42549f9) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-cf43fe46e5"></a>

### UNIT-CF43FE46E5

**模块**：`src/analysis/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CF43FE46E5 |
| 源码 | [src/analysis/__init__.py](../../../src/analysis/__init__.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-9f95d55376"></a>

### UNIT-9F95D55376

**模块**：`src/analysis/audit_summary.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9F95D55376 |
| 源码 | [src/analysis/audit_summary.py](../../../src/analysis/audit_summary.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/audit_summary.py` 的职责，通过 `build_audit_summary` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) |
| 验证状态 | selected |

#### 函数导航

[_hash_payload](#fun-18bf7fc28a) · [_llm_usage_summary](#fun-3041827ff4) · [build_audit_summary](#fun-5b705f2cac)

<a id="fun-18bf7fc28a"></a>

#### FUN-18BF7FC28A

| 设计项 | 说明 |
|---|---|
| 函数 | `_hash_payload` |
| 源码位置 | [src/analysis/audit_summary.py](../../../src/analysis/audit_summary.py) · `L10` |
| 签名 | `_hash_payload(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`hash_payload`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `json.dumps` → `hexdigest` → `hashlib.sha256` → `raw.encode`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.dumps、hexdigest、hashlib.sha256、raw.encode |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3041827ff4"></a>

#### FUN-3041827FF4

| 设计项 | 说明 |
|---|---|
| 函数 | `_llm_usage_summary` |
| 源码位置 | [src/analysis/audit_summary.py](../../../src/analysis/audit_summary.py) · `L15` |
| 签名 | `_llm_usage_summary(llm_io: list[dict[str, Any]])` |
| 参数 | `llm_io`（list[dict[str, Any]]）：由 `llm_io` 表示的输入集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`llm_usage_summary`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `r.get` → `sum` → `a.get` → `retry_reasons.append` → `round` → `any`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | r.get、sum、int、a.get、retry_reasons.append、len、round、any |
| 复杂度 / 风险 | 分支 5；跨度 32 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5b705f2cac"></a>

#### FUN-5B705F2CAC

| 设计项 | 说明 |
|---|---|
| 函数 | `build_audit_summary` |
| 源码位置 | [src/analysis/audit_summary.py](../../../src/analysis/audit_summary.py) · `L49` |
| 签名 | `build_audit_summary(report: dict[str, Any], *, decision: Any \| None=None, stage_meta: dict[str, Any] \| None=None)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`decision`（Any \| None）：最终或阶段决策；默认值 `None`<br>`stage_meta`（dict[str, Any] \| None）：审计或处理元数据；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`audit_summary`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `next` → `s.get` → `meta.get` → `row.get` → `get` → `val.get` → `narrative_audit.items`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、next、s.get、meta.get、row.get、get、val.get、narrative_audit.items、isinstance、decision.to_dict、hasattr、decision_dict.get、_hash_payload、top_audit.get、_llm_usage_summary、v.get |
| 复杂度 / 风险 | 分支 1；跨度 59 行；中 |
| 测试 / 验证 | [tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="unit-271badecbe"></a>

### UNIT-271BADECBE

**模块**：`src/analysis/chart_sr_filters.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-271BADECBE |
| 源码 | [src/analysis/chart_sr_filters.py](../../../src/analysis/chart_sr_filters.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/chart_sr_filters.py` 的职责，通过 `visible_sr_price_lines` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) |
| 验证状态 | selected |

#### 函数导航

[_fmt_price](#fun-615e3b9de5) · [_short_chart_title](#fun-cbd491e1bc) · [_merge_nearby](#fun-fbc037e567) · [visible_sr_price_lines](#fun-449394678b)

<a id="fun-615e3b9de5"></a>

#### FUN-615E3B9DE5

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_price` |
| 源码位置 | [src/analysis/chart_sr_filters.py](../../../src/analysis/chart_sr_filters.py) · `L22` |
| 签名 | `_fmt_price(price: float)` |
| 参数 | `price`（float）：当前或待评估价格 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成价格显示值文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `abs`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、abs、str、int |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cbd491e1bc"></a>

#### FUN-CBD491E1BC

| 设计项 | 说明 |
|---|---|
| 函数 | `_short_chart_title` |
| 源码位置 | [src/analysis/chart_sr_filters.py](../../../src/analysis/chart_sr_filters.py) · `L29` |
| 签名 | `_short_chart_title(lvl: SrLevel)` |
| 参数 | `lvl`（SrLevel）：由调用方提供的 `lvl` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`short_chart_title`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `replace`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、replace、len |
| 复杂度 / 风险 | 分支 3；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fbc037e567"></a>

#### FUN-FBC037E567

| 设计项 | 说明 |
|---|---|
| 函数 | `_merge_nearby` |
| 源码位置 | [src/analysis/chart_sr_filters.py](../../../src/analysis/chart_sr_filters.py) · `L47` |
| 签名 | `_merge_nearby(levels: list[SrLevel])` |
| 参数 | `levels`（list[SrLevel]）：候选价格水平集合 |
| 返回 | 返回 `list[SrLevel]` 类型结果 |
| 职责 | 合并`nearby`；返回 `list[SrLevel]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `_KIND_PRIORITY.get` → `enumerate` → `abs` → `kept.append`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[SrLevel]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、_KIND_PRIORITY.get、enumerate、abs、kept.append |
| 复杂度 / 风险 | 分支 6；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-449394678b"></a>

#### FUN-449394678B

| 设计项 | 说明 |
|---|---|
| 函数 | `visible_sr_price_lines` |
| 源码位置 | [src/analysis/chart_sr_filters.py](../../../src/analysis/chart_sr_filters.py) · `L69` |
| 签名 | `visible_sr_price_lines(sr_levels: list[SrLevel] \| list[dict[str, Any]], plot_df: pd.DataFrame, *, max_lines: int=_MAX_CHART_LINES, current_price: float \| None=None)` |
| 参数 | `sr_levels`（list[SrLevel] \| list[dict[str, Any]]）：候选价格水平集合<br>`plot_df`（pd.DataFrame）：输入数据表<br>`max_lines`（int）：由 `max_lines` 表示的数值参数；默认值 `_MAX_CHART_LINES`<br>`current_price`（float \| None）：当前市场价格；默认值 `None` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`visible_sr_price_lines`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `min` → `max` → `isinstance` → `parsed.append` → `SrLevel` → `row.get` → `pd.Timestamp` → `_merge_nearby`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、min、max、isinstance、parsed.append、SrLevel、row.get、pd.Timestamp、str、_merge_nearby、visible.sort、_KIND_PRIORITY.get、abs、len、picked.extend、sorted、_SR_COLORS.get、lines.append、colors.get、_fmt_price |
| 复杂度 / 风险 | 分支 8；跨度 69 行；中 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="unit-070aa8511c"></a>

### UNIT-070AA8511C

**模块**：`src/analysis/chart_zone_filters.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-070AA8511C |
| 源码 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/chart_zone_filters.py` 的职责，通过 `chart_plot_df`、`chart_price_bounds`、`zone_overlaps_chart_range`、`visible_order_blocks`、`visible_active_fvgs`、`visible_zone_snapshots`、`visible_zones_for_chart` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [visible_order_blocks](#fun-f8e5f51975) | 构建`visible_order_blocks`；返回 `list[OrderBlock]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |

#### 函数导航

[chart_plot_df](#fun-5916a45360) · [chart_price_bounds](#fun-77a17f101c) · [zone_overlaps_chart_range](#fun-2b036568fa) · [_align_ts](#fun-feca409ef6) · [visible_order_blocks](#fun-f8e5f51975) · [visible_active_fvgs](#fun-52b596d6f3) · [visible_zone_snapshots](#fun-75356974bc) · [visible_zones_for_chart](#fun-19453dd010)

<a id="fun-5916a45360"></a>

#### FUN-5916A45360

| 设计项 | 说明 |
|---|---|
| 函数 | `chart_plot_df` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L18` |
| 签名 | `chart_plot_df(df: pd.DataFrame, bars: int)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`bars`（int）：K 线记录集合 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 构建`chart_plot_df`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `copy` → `df.tail` → `max`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | copy、df.tail、max |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-77a17f101c"></a>

#### FUN-77A17F101C

| 设计项 | 说明 |
|---|---|
| 函数 | `chart_price_bounds` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L22` |
| 签名 | `chart_price_bounds(plot_df: pd.DataFrame)` |
| 参数 | `plot_df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `tuple[float, float]` 类型结果 |
| 职责 | 构建`chart_price_bounds`；返回 `tuple[float, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `min` → `max`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、min、max |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2b036568fa"></a>

#### FUN-2B036568FA

| 设计项 | 说明 |
|---|---|
| 函数 | `zone_overlaps_chart_range` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L26` |
| 签名 | `zone_overlaps_chart_range(low: float, high: float, plot_df: pd.DataFrame)` |
| 参数 | `low`（float）：最低价序列或下界<br>`high`（float）：最高价序列或上界<br>`plot_df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`zone_overlaps_chart_range`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `chart_price_bounds`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | chart_price_bounds |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-feca409ef6"></a>

#### FUN-FECA409EF6

| 设计项 | 说明 |
|---|---|
| 函数 | `_align_ts` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L33` |
| 签名 | `_align_ts(ts: pd.Timestamp, ref_index: pd.DatetimeIndex)` |
| 参数 | `ts`（pd.Timestamp）：由调用方提供的 `ts` 输入对象<br>`ref_index`（pd.DatetimeIndex）：由调用方提供的 `ref_index` 输入对象 |
| 返回 | 返回 `pd.Timestamp` 类型结果 |
| 职责 | 生成`align_ts`结果；返回 `pd.Timestamp` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.Timestamp` → `t.tz_localize` → `t.tz_convert`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Timestamp` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.Timestamp、t.tz_localize、t.tz_convert |
| 复杂度 / 风险 | 分支 3；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f8e5f51975"></a>

#### FUN-F8E5F51975

| 设计项 | 说明 |
|---|---|
| 函数 | `visible_order_blocks` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L44` |
| 签名 | `visible_order_blocks(analysis: TimeframeAnalysis, plot_df: pd.DataFrame, *, max_zones: int=MAX_OB_ZONES)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`plot_df`（pd.DataFrame）：输入数据表<br>`max_zones`（int）：价格区域集合；默认值 `MAX_OB_ZONES` |
| 返回 | 返回 `list[OrderBlock]` 类型结果 |
| 职责 | 构建`visible_order_blocks`；返回 `list[OrderBlock]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `plot_df.index.max` → `_align_ts` → `zone_overlaps_chart_range` → `visible.sort`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[OrderBlock]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | plot_df.index.max、_align_ts、zone_overlaps_chart_range、float、visible.sort |
| 复杂度 / 风险 | 分支 0；跨度 15 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-52b596d6f3"></a>

#### FUN-52B596D6F3

| 设计项 | 说明 |
|---|---|
| 函数 | `visible_active_fvgs` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L61` |
| 签名 | `visible_active_fvgs(analysis: TimeframeAnalysis, plot_df: pd.DataFrame, *, max_zones: int=MAX_FVG_ZONES)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`plot_df`（pd.DataFrame）：输入数据表<br>`max_zones`（int）：价格区域集合；默认值 `MAX_FVG_ZONES` |
| 返回 | 返回 `list[FairValueGap]` 类型结果 |
| 职责 | 构建`visible_active_fvgs`；返回 `list[FairValueGap]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `plot_df.index.max` → `_align_ts` → `zone_overlaps_chart_range` → `visible.sort`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[FairValueGap]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | plot_df.index.max、_align_ts、zone_overlaps_chart_range、float、visible.sort |
| 复杂度 / 风险 | 分支 0；跨度 15 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-75356974bc"></a>

#### FUN-75356974BC

| 设计项 | 说明 |
|---|---|
| 函数 | `visible_zone_snapshots` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L78` |
| 签名 | `visible_zone_snapshots(analysis: TimeframeAnalysis, plot_df: pd.DataFrame, *, ob_limit: int=MAX_OB_ZONES, fvg_limit: int=MAX_FVG_ZONES)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`plot_df`（pd.DataFrame）：输入数据表<br>`ob_limit`（int）：返回或处理数量上限；默认值 `MAX_OB_ZONES`<br>`fvg_limit`（int）：返回或处理数量上限；默认值 `MAX_FVG_ZONES` |
| 返回 | 返回 `tuple[list[dict[str, object]], list[dict[str, object]]]` 类型结果 |
| 职责 | 构建`visible_zone_snapshots`；返回 `tuple[list[dict[str, object]], list[dict[str, object]]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `visible_order_blocks` → `visible_active_fvgs`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict[str, object]], list[dict[str, object]]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | visible_order_blocks、visible_active_fvgs |
| 复杂度 / 风险 | 分支 0；跨度 17 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-19453dd010"></a>

#### FUN-19453DD010

| 设计项 | 说明 |
|---|---|
| 函数 | `visible_zones_for_chart` |
| 源码位置 | [src/analysis/chart_zone_filters.py](../../../src/analysis/chart_zone_filters.py) · `L97` |
| 签名 | `visible_zones_for_chart(analysis: TimeframeAnalysis, df: pd.DataFrame, *, bars: int, ob_limit: int=MAX_OB_ZONES, fvg_limit: int=MAX_FVG_ZONES)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`df`（pd.DataFrame）：输入数据表<br>`bars`（int）：K 线记录集合<br>`ob_limit`（int）：返回或处理数量上限；默认值 `MAX_OB_ZONES`<br>`fvg_limit`（int）：返回或处理数量上限；默认值 `MAX_FVG_ZONES` |
| 返回 | 返回 `tuple[list[dict[str, object]], list[dict[str, object]]]` 类型结果 |
| 职责 | 构建`visible_zones_for_chart`；返回 `tuple[list[dict[str, object]], list[dict[str, object]]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `chart_plot_df` → `visible_zone_snapshots`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict[str, object]], list[dict[str, object]]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | chart_plot_df、visible_zone_snapshots |
| 复杂度 / 风险 | 分支 0；跨度 10 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-67d22a7c31"></a>

### UNIT-67D22A7C31

**模块**：`src/analysis/claim_eligibility.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-67D22A7C31 |
| 源码 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/claim_eligibility.py` 的职责，通过 `ClaimAudit`、`technical_claim_fact_catalog`、`adjudicate_level_proposal_claim`、`claim_allows_execution_authorization` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 14 / 14 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [ClaimAudit.to_dict](#fun-43c4b237b7) | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| [ClaimAudit.allows_execution_authorization](#fun-039e702d1a) | 判断`allows_execution_authorization`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py) |
| [_overlap_amount](#fun-103fa43ff4) | 计算`overlap_amount`；返回 `float` 类型结果。 | 未检测到直接副作用 | — |
| [_zones_near](#fun-49e61c75ae) | 判断`zones_near`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_reaction_index](#fun-ee4367894d) | 构建`reaction_index`；返回 `dict[str, dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [_collect_fvgs](#fun-ead4b05709) | 收集`fvgs`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [technical_claim_fact_catalog](#fun-8edd654d1e) | 构建`technical_claim_fact_catalog`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [_fact_entity_for_ids](#fun-ae9b1e87f2) | 构建`fact_entity_for_ids`；返回 `dict[str, Any] \| None` 类型结果。 | 未检测到直接副作用 | — |
| [_fact_direction_supports_trade](#fun-4fb8932cb6) | 判断`fact_direction_supports_trade`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_relationship_holds](#fun-a094dfd75f) | 判断`relationship_holds`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_aligned_fvgs](#fun-582a749531) | 构建`aligned_fvgs`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [_counter_fvgs](#fun-aff197d9f4) | 构建`counter_fvgs`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [adjudicate_level_proposal_claim](#fun-d280cc6eb5) | 生成`adjudicate_level_proposal_claim`结果；返回 `ClaimAudit` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py) |
| [claim_allows_execution_authorization](#fun-972700d46f) | 判断`claim_allows_execution_authorization`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py) |

#### 函数导航

[ClaimAudit.to_dict](#fun-43c4b237b7) · [ClaimAudit.allows_execution_authorization](#fun-039e702d1a) · [_overlap_amount](#fun-103fa43ff4) · [_zones_near](#fun-49e61c75ae) · [_reaction_index](#fun-ee4367894d) · [_collect_fvgs](#fun-ead4b05709) · [technical_claim_fact_catalog](#fun-8edd654d1e) · [_fact_entity_for_ids](#fun-ae9b1e87f2) · [_fact_direction_supports_trade](#fun-4fb8932cb6) · [_relationship_holds](#fun-a094dfd75f) · [_aligned_fvgs](#fun-582a749531) · [_counter_fvgs](#fun-aff197d9f4) · [adjudicate_level_proposal_claim](#fun-d280cc6eb5) · [claim_allows_execution_authorization](#fun-972700d46f)

<a id="fun-43c4b237b7"></a>

#### FUN-43C4B237B7

| 设计项 | 说明 |
|---|---|
| 函数 | `ClaimAudit.to_dict` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L44` |
| 签名 | `ClaimAudit.to_dict(self)` |
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
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-039e702d1a"></a>

#### FUN-039E702D1A

| 设计项 | 说明 |
|---|---|
| 函数 | `ClaimAudit.allows_execution_authorization` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L48` |
| 签名 | `ClaimAudit.allows_execution_authorization(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`allows_execution_authorization`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py) · 直接动态测试 |

<a id="fun-103fa43ff4"></a>

#### FUN-103FA43FF4

| 设计项 | 说明 |
|---|---|
| 函数 | `_overlap_amount` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L52` |
| 签名 | `_overlap_amount(a_lo: float, a_hi: float, b_lo: float, b_hi: float)` |
| 参数 | `a_lo`（float）：由 `a_lo` 表示的数值参数<br>`a_hi`（float）：由 `a_hi` 表示的数值参数<br>`b_lo`（float）：由 `b_lo` 表示的数值参数<br>`b_hi`（float）：由 `b_hi` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`overlap_amount`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min |
| 复杂度 / 风险 | 分支 0；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-49e61c75ae"></a>

#### FUN-49E61C75AE

| 设计项 | 说明 |
|---|---|
| 函数 | `_zones_near` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L58` |
| 签名 | `_zones_near(a_lo: float, a_hi: float, b_lo: float, b_hi: float, *, tol: float)` |
| 参数 | `a_lo`（float）：由 `a_lo` 表示的数值参数<br>`a_hi`（float）：由 `a_hi` 表示的数值参数<br>`b_lo`（float）：由 `b_lo` 表示的数值参数<br>`b_hi`（float）：由 `b_hi` 表示的数值参数<br>`tol`（float）：由 `tol` 表示的数值参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`zones_near`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_overlap_amount` → `max` → `min`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _overlap_amount、max、min |
| 复杂度 / 风险 | 分支 3；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ee4367894d"></a>

#### FUN-EE4367894D

| 设计项 | 说明 |
|---|---|
| 函数 | `_reaction_index` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L69` |
| 签名 | `_reaction_index(reactions: list[dict[str, Any]] \| None)` |
| 参数 | `reactions`（list[dict[str, Any]] \| None）：由 `reactions` 表示的输入集合 |
| 返回 | 返回 `dict[str, dict[str, Any]]` 类型结果 |
| 职责 | 构建`reaction_index`；返回 `dict[str, dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `row.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、row.get |
| 复杂度 / 风险 | 分支 2；跨度 7 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ead4b05709"></a>

#### FUN-EAD4B05709

| 设计项 | 说明 |
|---|---|
| 函数 | `_collect_fvgs` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L78` |
| 签名 | `_collect_fvgs(analyses: dict[str, TimeframeAnalysis])` |
| 参数 | `analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 收集`fvgs`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `analyses.items` → `enumerate` → `isinstance` → `abs` → `rows.append` → `round`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | analyses.items、float、enumerate、isinstance、abs、rows.append、round |
| 复杂度 / 风险 | 分支 6；跨度 25 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8edd654d1e"></a>

#### FUN-8EDD654D1E

| 设计项 | 说明 |
|---|---|
| 函数 | `technical_claim_fact_catalog` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L105` |
| 签名 | `technical_claim_fact_catalog(ctx: MarketContext, *, price_action: dict[str, Any] \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`price_action`（dict[str, Any] \| None）：价格行为分析结果；默认值 `None` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`technical_claim_fact_catalog`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.analyses.items` → `enumerate` → `isinstance` → `sorted` → `rows.append` → `build_price_action_summaries` → `pa_blocks.items` → `block.get`；包含 16 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ctx.analyses.items、enumerate、isinstance、sorted、float、rows.append、str、build_price_action_summaries、pa_blocks.items、block.get、profile.get、level.get、lower |
| 复杂度 / 风险 | 分支 16；跨度 92 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ae9b1e87f2"></a>

#### FUN-AE9B1E87F2

| 设计项 | 说明 |
|---|---|
| 函数 | `_fact_entity_for_ids` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L199` |
| 签名 | `_fact_entity_for_ids(fact_ids: list[str], catalog: list[dict[str, Any]])` |
| 参数 | `fact_ids`（list[str]）：由 `fact_ids` 表示的输入集合<br>`catalog`（list[dict[str, Any]]）：由 `catalog` 表示的输入集合 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 构建`fact_entity_for_ids`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `row.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、row.get |
| 复杂度 / 风险 | 分支 3；跨度 11 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4fb8932cb6"></a>

#### FUN-4FB8932CB6

| 设计项 | 说明 |
|---|---|
| 函数 | `_fact_direction_supports_trade` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L212` |
| 签名 | `_fact_direction_supports_trade(fact: dict[str, Any], direction: str)` |
| 参数 | `fact`（dict[str, Any]）：由 `fact` 表示的键值映射<br>`direction`（str）：交易方向 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`fact_direction_supports_trade`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `fact.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、fact.get |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a094dfd75f"></a>

#### FUN-A094DFD75F

| 设计项 | 说明 |
|---|---|
| 函数 | `_relationship_holds` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L218` |
| 签名 | `_relationship_holds(relation_type: str, left: dict[str, Any], right: dict[str, Any])` |
| 参数 | `relation_type`（str）：由 `relation_type` 表示的文本或标识<br>`left`（dict[str, Any]）：由 `left` 表示的键值映射<br>`right`（dict[str, Any]）：由 `right` 表示的键值映射 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`relationship_holds`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `_zones_near` → `left.get` → `right.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、max、min、_zones_near、str、left.get、right.get |
| 复杂度 / 风险 | 分支 3；跨度 32 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-582a749531"></a>

#### FUN-582A749531

| 设计项 | 说明 |
|---|---|
| 函数 | `_aligned_fvgs` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L252` |
| 签名 | `_aligned_fvgs(*, direction: str, entry_low: float, entry_high: float, zones: list[dict[str, Any]])` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`zones`（list[dict[str, Any]]）：价格区域集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`aligned_fvgs`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_zones_near`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _zones_near |
| 复杂度 / 风险 | 分支 1；跨度 14 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-aff197d9f4"></a>

#### FUN-AFF197D9F4

| 设计项 | 说明 |
|---|---|
| 函数 | `_counter_fvgs` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L268` |
| 签名 | `_counter_fvgs(*, direction: str, entry_low: float, entry_high: float, zones: list[dict[str, Any]])` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`zones`（list[dict[str, Any]]）：价格区域集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`counter_fvgs`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_zones_near`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _zones_near |
| 复杂度 / 风险 | 分支 1；跨度 14 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d280cc6eb5"></a>

#### FUN-D280CC6EB5

| 设计项 | 说明 |
|---|---|
| 函数 | `adjudicate_level_proposal_claim` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L284` |
| 签名 | `adjudicate_level_proposal_claim(proposal: LevelProposal, ctx: MarketContext, *, level_reactions: list[dict[str, Any]] \| None=None)` |
| 参数 | `proposal`（LevelProposal）：候选交易方案<br>`ctx`（MarketContext）：运行上下文<br>`level_reactions`（list[dict[str, Any]] \| None）：由 `level_reactions` 表示的输入集合；默认值 `None` |
| 返回 | 返回 `ClaimAudit` 类型结果 |
| 职责 | 生成`adjudicate_level_proposal_claim`结果；返回 `ClaimAudit` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_reaction_index` → `strip` → `technical_claim_fact_catalog` → `_collect_fvgs` → `_aligned_fvgs` → `_counter_fvgs` → `fact_ids.extend` → `ClaimAudit`；包含 33 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ClaimAudit` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _reaction_index、strip、str、technical_claim_fact_catalog、_collect_fvgs、_aligned_fvgs、_counter_fvgs、fact_ids.extend、len、bool、ClaimAudit、fact_ids.append、reasons.append、reaction.get、sorted、isinstance、row.get、set、issubset、counterevidence.append |
| 复杂度 / 风险 | 分支 33；跨度 274 行；高 |
| 测试 / 验证 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py) · 直接动态测试 |

<a id="fun-972700d46f"></a>

#### FUN-972700D46F

| 设计项 | 说明 |
|---|---|
| 函数 | `claim_allows_execution_authorization` |
| 源码位置 | [src/analysis/claim_eligibility.py](../../../src/analysis/claim_eligibility.py) · `L560` |
| 签名 | `claim_allows_execution_authorization(signal_or_meta: dict[str, Any] \| None)` |
| 参数 | `signal_or_meta`（dict[str, Any] \| None）：审计或处理元数据 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`claim_allows_execution_authorization`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `signal_or_meta.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | signal_or_meta.get |
| 复杂度 / 风险 | 分支 2；跨度 9 行；高 |
| 测试 / 验证 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py) · 直接动态测试 |

<a id="unit-3549e9d9b7"></a>

### UNIT-3549E9D9B7

**模块**：`src/analysis/data_freshness.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3549E9D9B7 |
| 源码 | [src/analysis/data_freshness.py](../../../src/analysis/data_freshness.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/data_freshness.py` 的职责，通过 `build_data_as_of` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_data_freshness.py](../../../tests/unit/test_data_freshness.py) |
| 验证状态 | selected |

#### 函数导航

[_bar_timestamp](#fun-2b7eb34519) · [build_data_as_of](#fun-4734af977b)

<a id="fun-2b7eb34519"></a>

#### FUN-2B7EB34519

| 设计项 | 说明 |
|---|---|
| 函数 | `_bar_timestamp` |
| 源码位置 | [src/analysis/data_freshness.py](../../../src/analysis/data_freshness.py) · `L18` |
| 签名 | `_bar_timestamp(df: pd.DataFrame \| None)` |
| 参数 | `df`（pd.DataFrame \| None）：输入数据表 |
| 返回 | 返回 `datetime \| None` 类型结果 |
| 职责 | 生成`bar_timestamp`结果；返回 `datetime \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `ts.tz_localize` → `ts.to_pydatetime`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `datetime \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、ts.tz_localize、ts.to_pydatetime |
| 复杂度 / 风险 | 分支 3；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4734af977b"></a>

#### FUN-4734AF977B

| 设计项 | 说明 |
|---|---|
| 函数 | `build_data_as_of` |
| 源码位置 | [src/analysis/data_freshness.py](../../../src/analysis/data_freshness.py) · `L29` |
| 签名 | `build_data_as_of(raw: dict[str, pd.DataFrame], *, now: datetime \| None=None)` |
| 参数 | `raw`（dict[str, pd.DataFrame]）：尚未标准化的原始输入<br>`now`（datetime \| None）：由调用方提供的 `now` 输入对象；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`data_as_of`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `datetime.now` → `raw.get` → `_bar_timestamp` → `last_bar.replace` → `total_seconds` → `now.weekday` → `warnings.append` → `last_bar.strftime`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | datetime.now、raw.get、_bar_timestamp、last_bar.replace、total_seconds、now.weekday、warnings.append、last_bar.strftime、now.strftime、round、log.info、len |
| 复杂度 / 风险 | 分支 9；跨度 50 行；中 |
| 测试 / 验证 | [tests/unit/test_data_freshness.py](../../../tests/unit/test_data_freshness.py) · 直接动态测试 |

<a id="unit-7dfc57faf9"></a>

### UNIT-7DFC57FAF9

**模块**：`src/analysis/dgt_price_action.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7DFC57FAF9 |
| 源码 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/dgt_price_action.py` 的职责，通过 `SrLevel`、`VolumeProfileResult`、`DgtPriceActionResult`、`build_volume_profile`、`analyze_dgt_price_action`、`dgt_result_to_dict` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 10 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) |
| 验证状态 | selected |

#### 函数导航

[_nz_volume](#fun-a1eb4c5f6a) · [_volume_usable](#fun-8c5d73d5c1) · [_atr](#fun-62894b9526) · [_consecutive_sr](#fun-90d19bf962) · [_spike_and_volatility_levels](#fun-fbf2e7c9de) · [_volume_portion](#fun-16616bf5e6) · [build_volume_profile](#fun-998848a755) · [_dedupe_sr_levels](#fun-692ece3baf) · [analyze_dgt_price_action](#fun-b29e79e520) · [dgt_result_to_dict](#fun-39cf1265fc)

<a id="fun-a1eb4c5f6a"></a>

#### FUN-A1EB4C5F6A

| 设计项 | 说明 |
|---|---|
| 函数 | `_nz_volume` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L63` |
| 签名 | `_nz_volume(series: pd.Series)` |
| 参数 | `series`（pd.Series）：由调用方提供的 `series` 输入对象 |
| 返回 | 返回 `pd.Series` 类型结果 |
| 职责 | 生成`nz_volume`结果；返回 `pd.Series` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `astype` → `series.fillna`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Series` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | astype、series.fillna |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8c5d73d5c1"></a>

#### FUN-8C5D73D5C1

| 设计项 | 说明 |
|---|---|
| 函数 | `_volume_usable` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L67` |
| 签名 | `_volume_usable(vol: pd.Series, *, min_ratio: float=0.05)` |
| 参数 | `vol`（pd.Series）：由调用方提供的 `vol` 输入对象<br>`min_ratio`（float）：由 `min_ratio` 表示的数值参数；默认值 `0.05` |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`volume_usable`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、sum、len |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-62894b9526"></a>

#### FUN-62894B9526

| 设计项 | 说明 |
|---|---|
| 函数 | `_atr` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L73` |
| 签名 | `_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int)` |
| 参数 | `high`（pd.Series）：最高价序列或上界<br>`low`（pd.Series）：最低价序列或下界<br>`close`（pd.Series）：由调用方提供的 `close` 输入对象<br>`length`（int）：由 `length` 表示的数值参数 |
| 返回 | 返回 `pd.Series` 类型结果 |
| 职责 | 生成`atr`结果；返回 `pd.Series` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `close.shift` → `max` → `pd.concat` → `abs` → `mean` → `tr.rolling`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Series` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | close.shift、max、pd.concat、abs、mean、tr.rolling |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-90d19bf962"></a>

#### FUN-90D19BF962

| 设计项 | 说明 |
|---|---|
| 函数 | `_consecutive_sr` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L82` |
| 签名 | `_consecutive_sr(window: pd.DataFrame, vol_ma: pd.Series, *, use_volume: bool)` |
| 参数 | `window`（pd.DataFrame）：由调用方提供的 `window` 输入对象<br>`vol_ma`（pd.Series）：由调用方提供的 `vol_ma` 输入对象<br>`use_volume`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `list[SrLevel]` 类型结果 |
| 职责 | 构建`consecutive_sr`；返回 `list[SrLevel]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `astype` → `_nz_volume` → `v.shift` → `c.shift` → `range` → `levels.append` → `SrLevel` → `round`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[SrLevel]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、astype、_nz_volume、v.shift、c.shift、range、bool、float、levels.append、SrLevel、round、slice_l.min、slice_h.max |
| 复杂度 / 风险 | 分支 5；跨度 68 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fbf2e7c9de"></a>

#### FUN-FBF2E7C9DE

| 设计项 | 说明 |
|---|---|
| 函数 | `_spike_and_volatility_levels` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L152` |
| 签名 | `_spike_and_volatility_levels(window: pd.DataFrame, vol_ma: pd.Series)` |
| 参数 | `window`（pd.DataFrame）：由调用方提供的 `window` 输入对象<br>`vol_ma`（pd.Series）：由调用方提供的 `vol_ma` 输入对象 |
| 返回 | 返回 `tuple[list[SrLevel], int, int]` 类型结果 |
| 职责 | 构建`spike_and_volatility_levels`；返回 `tuple[list[SrLevel], int, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `astype` → `_nz_volume` → `_atr` → `range` → `levels.append` → `SrLevel` → `round`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[SrLevel], int, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | astype、_nz_volume、_atr、range、len、float、bool、levels.append、SrLevel、round |
| 复杂度 / 风险 | 分支 9；跨度 56 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-16616bf5e6"></a>

#### FUN-16616BF5E6

| 设计项 | 说明 |
|---|---|
| 函数 | `_volume_portion` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L210` |
| 签名 | `_volume_portion(bar_low: float, bar_high: float, row_low: float, row_high: float)` |
| 参数 | `bar_low`（float）：最低价序列或下界<br>`bar_high`（float）：最高价序列或上界<br>`row_low`（float）：最低价序列或下界<br>`row_high`（float）：最高价序列或上界 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`volume_portion`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max |
| 复杂度 / 风险 | 分支 3；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-998848a755"></a>

#### FUN-998848A755

| 设计项 | 说明 |
|---|---|
| 函数 | `build_volume_profile` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L226` |
| 签名 | `build_volume_profile(bars: pd.DataFrame, *, num_rows: int=PROFILE_ROWS, value_area_pct: float=VALUE_AREA_PCT, sd_thresh: float=SUPPLY_DEMAND_THRESH)` |
| 参数 | `bars`（pd.DataFrame）：K 线记录集合<br>`num_rows`（int）：记录行集合；默认值 `PROFILE_ROWS`<br>`value_area_pct`（float）：百分比数值；默认值 `VALUE_AREA_PCT`<br>`sd_thresh`（float）：由 `sd_thresh` 表示的数值参数；默认值 `SUPPLY_DEMAND_THRESH` |
| 返回 | 返回 `VolumeProfileResult` 类型结果 |
| 职责 | 构建`volume_profile`；返回 `VolumeProfileResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `VolumeProfileResult` → `_nz_volume` → `_volume_usable` → `v.sum` → `min` → `max` → `np.isfinite` → `np.zeros`；包含 20 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `VolumeProfileResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | VolumeProfileResult、_nz_volume、_volume_usable、float、v.sum、min、max、np.isfinite、np.zeros、bars.iterrows、int、range、_volume_portion、totals.max、totals.argmax、round、totals.sum、sd_zones.append |
| 复杂度 / 风险 | 分支 20；跨度 92 行；中 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="fun-692ece3baf"></a>

#### FUN-692ECE3BAF

| 设计项 | 说明 |
|---|---|
| 函数 | `_dedupe_sr_levels` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L320` |
| 签名 | `_dedupe_sr_levels(levels: list[SrLevel], *, tolerance: float=0.35)` |
| 参数 | `levels`（list[SrLevel]）：候选价格水平集合<br>`tolerance`（float）：数值比较容差；默认值 `0.35` |
| 返回 | 返回 `list[SrLevel]` 类型结果 |
| 职责 | 去重`sr_levels`；返回 `list[SrLevel]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `enumerate` → `abs` → `kept.append`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[SrLevel]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、enumerate、abs、kept.append |
| 复杂度 / 风险 | 分支 5；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b29e79e520"></a>

#### FUN-B29E79E520

| 设计项 | 说明 |
|---|---|
| 函数 | `analyze_dgt_price_action` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L342` |
| 签名 | `analyze_dgt_price_action(df: pd.DataFrame, timeframe: str, *, lookback: int=DEFAULT_LOOKBACK, profile_bars: pd.DataFrame \| None=None)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`timeframe`（str）：行情时间框架<br>`lookback`（int）：由 `lookback` 表示的数值参数；默认值 `DEFAULT_LOOKBACK`<br>`profile_bars`（pd.DataFrame \| None）：K 线记录集合；默认值 `None` |
| 返回 | 返回 `DgtPriceActionResult` 类型结果 |
| 职责 | 生成`analyze_dgt_price_action`结果；返回 `DgtPriceActionResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `DgtPriceActionResult` → `copy` → `df.tail` → `_nz_volume` → `_volume_usable` → `mean` → `vol.rolling` → `sr.extend`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `DgtPriceActionResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | DgtPriceActionResult、copy、df.tail、_nz_volume、_volume_usable、mean、vol.rolling、sr.extend、_consecutive_sr、_spike_and_volatility_levels、_dedupe_sr_levels、build_volume_profile、len |
| 复杂度 / 风险 | 分支 2；跨度 42 行；中 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="fun-39cf1265fc"></a>

#### FUN-39CF1265FC

| 设计项 | 说明 |
|---|---|
| 函数 | `dgt_result_to_dict` |
| 源码位置 | [src/analysis/dgt_price_action.py](../../../src/analysis/dgt_price_action.py) · `L386` |
| 签名 | `dgt_result_to_dict(result: DgtPriceActionResult, *, lookback_requested: int \| None=None, lookback_mode: str \| None=None)` |
| 参数 | `result`（DgtPriceActionResult）：处理结果<br>`lookback_requested`（int \| None）：由调用方提供的 `lookback_requested` 输入对象；默认值 `None`<br>`lookback_mode`（str \| None）：运行或分析模式；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`dgt_result_to_dict`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lvl.time.isoformat`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lvl.time.isoformat |
| 复杂度 / 风险 | 分支 2；跨度 37 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-3b1598dc1b"></a>

### UNIT-3B1598DC1B

**模块**：`src/analysis/display_labels.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3B1598DC1B |
| 源码 | [src/analysis/display_labels.py](../../../src/analysis/display_labels.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/display_labels.py` 的职责，通过 `liquidity_label` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[liquidity_label](#fun-f519f9a949)

<a id="fun-f519f9a949"></a>

#### FUN-F519F9A949

| 设计项 | 说明 |
|---|---|
| 函数 | `liquidity_label` |
| 源码位置 | [src/analysis/display_labels.py](../../../src/analysis/display_labels.py) · `L22` |
| 签名 | `liquidity_label(zone: LiquidityZone)` |
| 参数 | `zone`（LiquidityZone）：由调用方提供的 `zone` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`liquidity_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 2；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-60e70e7439"></a>

### UNIT-60E70E7439

**模块**：`src/analysis/fact_registry.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-60E70E7439 |
| 源码 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/fact_registry.py` 的职责，通过 `calendar_state`、`build_fact_registry`、`allowed_prices`、`fact_lookup`、`fact_ids_for_signal`、`compact_fact_index` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 16 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py)、[tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_llm_context_fact_refs.py](../../../tests/unit/test_llm_context_fact_refs.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[_as_of_utc](#fun-0574dfe158) · [_register_numeric](#fun-0a56af7ead) · [_register_text](#fun-9127544e40) · [_pa_fact_id](#fun-760701887e) · [calendar_state](#fun-7a197e3612) · [_calendar_state](#fun-b21844f1e5) · [_register_timeframes](#fun-98305ca234) · [_register_price_action](#fun-87b173149d) · [_register_technical_claim_facts](#fun-0da621fc3d) · [_register_freshness](#fun-e744014446) · [_register_external](#fun-0d88ff54f8) · [build_fact_registry](#fun-afac55bb24) · [allowed_prices](#fun-f1860a0ed6) · [fact_lookup](#fun-cbacfa1e82) · [fact_ids_for_signal](#fun-e14834ae01) · [compact_fact_index](#fun-91752c5a3c)

<a id="fun-0574dfe158"></a>

#### FUN-0574DFE158

| 设计项 | 说明 |
|---|---|
| 函数 | `_as_of_utc` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L11` |
| 签名 | `_as_of_utc(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`as_of_utc`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `as_of.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get、as_of.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0a56af7ead"></a>

#### FUN-0A56AF7EAD

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_numeric` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L16` |
| 签名 | `_register_numeric(facts: dict[str, dict[str, Any]], *, fact_id: str, value: Any, source: str, timeframe: str \| None=None, quality: str='verified', as_of: str \| None=None, refs: dict[str, Any] \| None=None)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`fact_id`（str）：对象标识<br>`value`（Any）：待处理值<br>`source`（str）：数据或证据来源<br>`timeframe`（str \| None）：行情时间框架；默认值 `None`<br>`quality`（str）：由 `quality` 表示的文本或标识；默认值 `'verified'`<br>`as_of`（str \| None）：数据截止时间；默认值 `None`<br>`refs`（dict[str, Any] \| None）：由 `refs` 表示的键值映射；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_numeric`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、get |
| 复杂度 / 风险 | 分支 4；跨度 34 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9127544e40"></a>

#### FUN-9127544E40

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_text` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L52` |
| 签名 | `_register_text(facts: dict[str, dict[str, Any]], *, fact_id: str, value: Any, source: str, timeframe: str \| None=None, quality: str='verified', as_of: str \| None=None, refs: dict[str, Any] \| None=None)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`fact_id`（str）：对象标识<br>`value`（Any）：待处理值<br>`source`（str）：数据或证据来源<br>`timeframe`（str \| None）：行情时间框架；默认值 `None`<br>`quality`（str）：由 `quality` 表示的文本或标识；默认值 `'verified'`<br>`as_of`（str \| None）：数据截止时间；默认值 `None`<br>`refs`（dict[str, Any] \| None）：由 `refs` 表示的键值映射；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_text`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、get |
| 复杂度 / 风险 | 分支 3；跨度 31 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-760701887e"></a>

#### FUN-760701887E

| 设计项 | 说明 |
|---|---|
| 函数 | `_pa_fact_id` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L85` |
| 签名 | `_pa_fact_id(tf: str, suffix: str)` |
| 参数 | `tf`（str）：时间框架简称<br>`suffix`（str）：由 `suffix` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`pa_fact_id`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7a197e3612"></a>

#### FUN-7A197E3612

| 设计项 | 说明 |
|---|---|
| 函数 | `calendar_state` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L91` |
| 签名 | `calendar_state(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成经济日历状态文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_calendar_state`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _calendar_state |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py) · 直接动态测试 |

<a id="fun-b21844f1e5"></a>

#### FUN-B21844F1E5

| 设计项 | 说明 |
|---|---|
| 函数 | `_calendar_state` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L96` |
| 签名 | `_calendar_state(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成经济日历状态文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `lower` → `external.get` → `any` → `strip`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、lower、str、external.get、any、strip |
| 复杂度 / 风险 | 分支 5；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-98305ca234"></a>

#### FUN-98305CA234

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_timeframes` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L116` |
| 签名 | `_register_timeframes(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str \| None, source: str)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`report`（dict[str, Any]）：分析报告<br>`as_of`（str \| None）：数据截止时间<br>`source`（str）：数据或证据来源 |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_timeframes`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `items` → `report.get` → `isinstance` → `_register_numeric` → `info.get` → `_register_text` → `enumerate` → `ob.get`；包含 15 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | items、report.get、isinstance、_register_numeric、info.get、_register_text、enumerate、ob.get、float、abs、fvg.get、round |
| 复杂度 / 风险 | 分支 15；跨度 66 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-87b173149d"></a>

#### FUN-87B173149D

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_price_action` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L184` |
| 签名 | `_register_price_action(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str \| None)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`report`（dict[str, Any]）：分析报告<br>`as_of`（str \| None）：数据截止时间 |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_price_action`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `items` → `report.get` → `get` → `_register_numeric` → `_pa_fact_id` → `vp.get` → `enumerate` → `lvl.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | items、report.get、get、_register_numeric、_pa_fact_id、vp.get、enumerate、lvl.get、str |
| 复杂度 / 风险 | 分支 3；跨度 29 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0da621fc3d"></a>

#### FUN-0DA621FC3D

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_technical_claim_facts` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L215` |
| 签名 | `_register_technical_claim_facts(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str \| None)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`report`（dict[str, Any]）：分析报告<br>`as_of`（str \| None）：数据截止时间 |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_technical_claim_facts`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `isinstance` → `entity.get` → `strip` → `fid.endswith` → `_register_numeric`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、isinstance、entity.get、strip、str、fid.endswith、_register_numeric |
| 复杂度 / 风险 | 分支 9；跨度 43 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e744014446"></a>

#### FUN-E744014446

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_freshness` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L260` |
| 签名 | `_register_freshness(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str \| None, source: str)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`report`（dict[str, Any]）：分析报告<br>`as_of`（str \| None）：数据截止时间<br>`source`（str）：数据或证据来源 |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_freshness`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `_register_text` → `data_as_of.get` → `lower` → `_register_numeric` → `stats.get` → `bars.items`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get、_register_text、data_as_of.get、lower、str、bool、_register_numeric、stats.get、bars.items |
| 复杂度 / 风险 | 分支 4；跨度 42 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0d88ff54f8"></a>

#### FUN-0D88FF54F8

| 设计项 | 说明 |
|---|---|
| 函数 | `_register_external` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L304` |
| 签名 | `_register_external(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str \| None)` |
| 参数 | `facts`（dict[str, dict[str, Any]]）：结构化事实集合<br>`report`（dict[str, Any]）：分析报告<br>`as_of`（str \| None）：数据截止时间 |
| 返回 | 无返回值（None） |
| 职责 | 执行`register_external`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `_calendar_state` → `_register_text` → `enumerate` → `external.get` → `isinstance` → `row.get` → `headline.get`；包含 12 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、_calendar_state、_register_text、enumerate、external.get、isinstance、row.get、headline.get、str、quote.get、_register_numeric、cross.get |
| 复杂度 / 风险 | 分支 12；跨度 83 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-afac55bb24"></a>

#### FUN-AFAC55BB24

| 设计项 | 说明 |
|---|---|
| 函数 | `build_fact_registry` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L389` |
| 签名 | `build_fact_registry(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`fact_registry`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_as_of_utc` → `get` → `report.get` → `_register_numeric` → `metrics.get` → `enumerate` → `row.get` → `_register_timeframes`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _as_of_utc、str、get、report.get、_register_numeric、metrics.get、enumerate、row.get、_register_timeframes、_register_price_action、_register_technical_claim_facts、sig.get、sentiment.get、_register_freshness、_register_external、facts.items、float、append、price_index.setdefault、len |
| 复杂度 / 风险 | 分支 9；跨度 85 行；中 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py)、[tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_llm_context_fact_refs.py](../../../tests/unit/test_llm_context_fact_refs.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) · 直接动态测试 |

<a id="fun-f1860a0ed6"></a>

#### FUN-F1860A0ED6

| 设计项 | 说明 |
|---|---|
| 函数 | `allowed_prices` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L476` |
| 签名 | `allowed_prices(registry: dict[str, Any])` |
| 参数 | `registry`（dict[str, Any]）：事实或证据登记映射 |
| 返回 | 返回 `set[float]` 类型结果 |
| 职责 | 构建`allowed_prices`；返回 `set[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values` → `registry.get` → `row.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `set[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、values、registry.get、row.get |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py) · 直接动态测试 |

<a id="fun-cbacfa1e82"></a>

#### FUN-CBACFA1E82

| 设计项 | 说明 |
|---|---|
| 函数 | `fact_lookup` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L484` |
| 签名 | `fact_lookup(registry: dict[str, Any], price: float, *, tolerance: float=0.51)` |
| 参数 | `registry`（dict[str, Any]）：事实或证据登记映射<br>`price`（float）：当前或待评估价格<br>`tolerance`（float）：数值比较容差；默认值 `0.51` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`fact_lookup`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values` → `registry.get` → `row.get` → `abs` → `matches.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | values、registry.get、row.get、abs、float、matches.append、str |
| 复杂度 / 风险 | 分支 3；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py) · 直接动态测试 |

<a id="fun-e14834ae01"></a>

#### FUN-E14834AE01

| 设计项 | 说明 |
|---|---|
| 函数 | `fact_ids_for_signal` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L495` |
| 签名 | `fact_ids_for_signal(sig: dict[str, Any], registry: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号<br>`registry`（dict[str, Any]）：事实或证据登记映射 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`fact_ids_for_signal`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get` → `registry.get` → `mapping.items` → `range` → `tp_ids.append`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、sig.get、registry.get、mapping.items、range、len、tp_ids.append |
| 复杂度 / 风险 | 分支 5；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py) · 直接动态测试 |

<a id="fun-91752c5a3c"></a>

#### FUN-91752C5A3C

| 设计项 | 说明 |
|---|---|
| 函数 | `compact_fact_index` |
| 源码位置 | [src/analysis/fact_registry.py](../../../src/analysis/fact_registry.py) · `L518` |
| 签名 | `compact_fact_index(registry: dict[str, Any], *, limit: int=120)` |
| 参数 | `registry`（dict[str, Any]）：事实或证据登记映射<br>`limit`（int）：返回或处理数量上限；默认值 `120` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`compact_fact_index`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values` → `registry.get` → `rows.sort` → `r.get` → `row.get` → `out.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、values、registry.get、rows.sort、str、r.get、row.get、out.append |
| 复杂度 / 风险 | 分支 2；跨度 19 行；中 |
| 测试 / 验证 | [tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py) · 直接动态测试 |

<a id="unit-c37864f306"></a>

### UNIT-C37864F306

**模块**：`src/analysis/field_glossary.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C37864F306 |
| 源码 | [src/analysis/field_glossary.py](../../../src/analysis/field_glossary.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/field_glossary.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3962aaac44"></a>

### UNIT-3962AAAC44

**模块**：`src/analysis/ict_pa.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3962AAAC44 |
| 源码 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/ict_pa.py` 的职责，通过 `SwingPoint`、`OrderBlock`、`FairValueGap`、`LiquidityZone`、`StructureEvent`、`TimeframeAnalysis`、`analyze_timeframe`、`sentiment_score` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_coherence.py](../../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_plan_signals.py](../../../tests/unit/test_plan_signals.py)、[tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_tf_snapshot.py](../../../tests/unit/test_tf_snapshot.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[_premium_discount](#fun-9d252e677d) · [_volume_signal](#fun-655f9ec66c) · [_last_numeric](#fun-51492ca837) · [_swing_liquidity](#fun-b620f510c7) · [_latest_structure_labels](#fun-dd99d46e1a) · [analyze_timeframe](#fun-caebe97b43) · [sentiment_score](#fun-2279759b7f)

<a id="fun-9d252e677d"></a>

#### FUN-9D252E677D

| 设计项 | 说明 |
|---|---|
| 函数 | `_premium_discount` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L80` |
| 签名 | `_premium_discount(swing_high: float \| None, swing_low: float \| None, price: float)` |
| 参数 | `swing_high`（float \| None）：摆动高点价格<br>`swing_low`（float \| None）：摆动低点价格<br>`price`（float）：当前或待评估价格 |
| 返回 | 返回 `tuple[str, float \| None]` 类型结果 |
| 职责 | 构建`premium_discount`；返回 `tuple[str, float \| None]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, float \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-655f9ec66c"></a>

#### FUN-655F9EC66C

| 设计项 | 说明 |
|---|---|
| 函数 | `_volume_signal` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L93` |
| 签名 | `_volume_signal(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`volume_signal`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `astype` → `mean`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、astype、float、mean |
| 复杂度 / 风险 | 分支 4；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-51492ca837"></a>

#### FUN-51492CA837

| 设计项 | 说明 |
|---|---|
| 函数 | `_last_numeric` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L109` |
| 签名 | `_last_numeric(df: pd.DataFrame, column: str)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`column`（str）：由 `column` 表示的文本或标识 |
| 返回 | 返回 `float \| None` 类型结果 |
| 职责 | 计算`last_numeric`；返回 `float \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.isna`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.isna、float |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b620f510c7"></a>

#### FUN-B620F510C7

| 设计项 | 说明 |
|---|---|
| 函数 | `_swing_liquidity` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L118` |
| 签名 | `_swing_liquidity(swing_high: float \| None, swing_low: float \| None)` |
| 参数 | `swing_high`（float \| None）：摆动高点价格<br>`swing_low`（float \| None）：摆动低点价格 |
| 返回 | 返回 `list[LiquidityZone]` 类型结果 |
| 职责 | 构建`swing_liquidity`；返回 `list[LiquidityZone]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `zones.append` → `LiquidityZone`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[LiquidityZone]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | zones.append、LiquidityZone、float |
| 复杂度 / 风险 | 分支 2；跨度 25 行；低 |
| 测试 / 验证 | [tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py) · 直接动态测试 |

<a id="fun-dd99d46e1a"></a>

#### FUN-DD99D46E1A

| 设计项 | 说明 |
|---|---|
| 函数 | `_latest_structure_labels` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L145` |
| 签名 | `_latest_structure_labels(events: list[StructureEvent], *, scope: Literal['internal', 'swing'] \| None=None)` |
| 参数 | `events`（list[StructureEvent]）：事件集合<br>`scope`（Literal['internal', 'swing'] \| None）：由调用方提供的 `scope` 输入对象；默认值 `None` |
| 返回 | 返回 `tuple[str, str]` 类型结果 |
| 职责 | 构建`latest_structure_labels`；返回 `tuple[str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `reversed`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | reversed |
| 复杂度 / 风险 | 分支 3；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-caebe97b43"></a>

#### FUN-CAEBE97B43

| 设计项 | 说明 |
|---|---|
| 函数 | `analyze_timeframe` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L161` |
| 签名 | `analyze_timeframe(df: pd.DataFrame, timeframe: str)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`timeframe`（str）：行情时间框架 |
| 返回 | 返回 `TimeframeAnalysis` 类型结果 |
| 职责 | 生成`analyze_timeframe`结果；返回 `TimeframeAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `analyze_luxalgo` → `_latest_structure_labels` → `_last_numeric` → `max` → `min` → `_premium_discount` → `_swing_liquidity` → `TimeframeAnalysis`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `TimeframeAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | analyze_luxalgo、_latest_structure_labels、float、len、_last_numeric、max、min、_premium_discount、_swing_liquidity、TimeframeAnalysis、_volume_signal |
| 复杂度 / 风险 | 分支 4；跨度 43 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="fun-2279759b7f"></a>

#### FUN-2279759B7F

| 设计项 | 说明 |
|---|---|
| 函数 | `sentiment_score` |
| 源码位置 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) · `L206` |
| 签名 | `sentiment_score(analyses: dict[str, TimeframeAnalysis])` |
| 参数 | `analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果 |
| 返回 | 返回 `dict[str, float]` 类型结果 |
| 职责 | 评分`sentiment`；返回 `dict[str, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `weights.items` → `round`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | weights.items、round |
| 复杂度 / 风险 | 分支 4；跨度 22 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-a9ae5e6696"></a>

### UNIT-A9AE5E6696

**模块**：`src/analysis/level_validator.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A9AE5E6696 |
| 源码 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/level_validator.py` 的职责，通过 `validate_llm_levels` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [validate_llm_levels](#fun-89da4d6e6e) | 验证`llm_levels`；返回 `tuple[list[TradingSignal], list[dict[str, Any]]]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py) |

#### 函数导航

[_location_error](#fun-3964465d91) · [_llm_signal_name](#fun-4bc8ff4d21) · [_tp_ladder_error](#fun-153aabf750) · [_geometry_error](#fun-fcbb9c053e) · [_position_size](#fun-a872921e36) · [validate_llm_levels](#fun-89da4d6e6e) · [_grade_force](#fun-fe20142b1a)

<a id="fun-3964465d91"></a>

#### FUN-3964465D91

| 设计项 | 说明 |
|---|---|
| 函数 | `_location_error` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L22` |
| 签名 | `_location_error(ctx: MarketContext, proposal: LevelProposal)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`proposal`（LevelProposal）：候选交易方案 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`location_error`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 2；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4bc8ff4d21"></a>

#### FUN-4BC8FF4D21

| 设计项 | 说明 |
|---|---|
| 函数 | `_llm_signal_name` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L37` |
| 签名 | `_llm_signal_name(proposal: LevelProposal)` |
| 参数 | `proposal`（LevelProposal）：候选交易方案 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`llm_signal_name`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、str |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-153aabf750"></a>

#### FUN-153AABF750

| 设计项 | 说明 |
|---|---|
| 函数 | `_tp_ladder_error` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L45` |
| 签名 | `_tp_ladder_error(proposal: LevelProposal)` |
| 参数 | `proposal`（LevelProposal）：候选交易方案 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`tp_ladder_error`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `any` → `zip`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、any、zip |
| 复杂度 / 风险 | 分支 8；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fcbb9c053e"></a>

#### FUN-FCBB9C053E

| 设计项 | 说明 |
|---|---|
| 函数 | `_geometry_error` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L65` |
| 签名 | `_geometry_error(proposal: LevelProposal)` |
| 参数 | `proposal`（LevelProposal）：候选交易方案 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`geometry_error`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_tp_ladder_error`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _tp_ladder_error |
| 复杂度 / 风险 | 分支 8；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a872921e36"></a>

#### FUN-A872921E36

| 设计项 | 说明 |
|---|---|
| 函数 | `_position_size` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L86` |
| 签名 | `_position_size(confidence: float, grade: str, *, eligibility: str)` |
| 参数 | `confidence`（float）：由 `confidence` 表示的数值参数<br>`grade`（str）：由 `grade` 表示的文本或标识<br>`eligibility`（str）：由 `eligibility` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`position_size`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-89da4d6e6e"></a>

#### FUN-89DA4D6E6E

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_llm_levels` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L96` |
| 签名 | `validate_llm_levels(ctx: MarketContext, proposals: list[LevelProposal], *, level_reactions: list[dict[str, Any]] \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`proposals`（list[LevelProposal]）：由 `proposals` 表示的输入集合<br>`level_reactions`（list[dict[str, Any]] \| None）：由 `level_reactions` 表示的输入集合；默认值 `None` |
| 返回 | 返回 `tuple[list[TradingSignal], list[dict[str, Any]]]` 类型结果 |
| 职责 | 验证`llm_levels`；返回 `tuple[list[TradingSignal], list[dict[str, Any]]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `log.info` → `sentiment_score` → `enumerate` → `adjudicate_level_proposal_claim` → `proposal.to_dict` → `join` → `audit.append` → `claim.to_dict`；包含 21 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[TradingSignal], list[dict[str, Any]]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.info、len、sentiment_score、enumerate、adjudicate_level_proposal_claim、list、dict、proposal.to_dict、join、audit.append、claim.to_dict、_geometry_error、_stop_breached、_location_error、setup_type.startswith、dict.fromkeys、_llm_signal_name、_setup_status_and_score、reasons.append、reasons.extend |
| 复杂度 / 风险 | 分支 21；跨度 197 行；高 |
| 测试 / 验证 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py) · 直接动态测试 |

<a id="fun-fe20142b1a"></a>

#### FUN-FE20142B1A

| 设计项 | 说明 |
|---|---|
| 函数 | `_grade_force` |
| 源码位置 | [src/analysis/level_validator.py](../../../src/analysis/level_validator.py) · `L295` |
| 签名 | `_grade_force(score: float)` |
| 参数 | `score`（float）：评分值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`grade_force`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-2f7fedba6f"></a>

### UNIT-2F7FEDBA6F

**模块**：`src/analysis/luxalgo_smc.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F7FEDBA6F |
| 源码 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/luxalgo_smc.py` 的职责，通过 `LuxAlgoResult`、`analyze_luxalgo` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 15 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_store_order_block](#fun-2052af2dde) | 生成`store_order_block`结果；返回 `OrderBlock \| None` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py) |
| [analyze_luxalgo](#fun-08ff07c7e5) | 生成`analyze_luxalgo`结果；返回 `LuxAlgoResult` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py) |

#### 函数导航

[_true_range](#fun-80471dd12f) · [_atr_series](#fun-f820754950) · [_leg_at_bar](#fun-fc6a52d232) · [_parsed_bar](#fun-0a1736195c) · [_fvg_threshold](#fun-8b8bd0c1c0) · [_store_order_block](#fun-2052af2dde) · [_mitigate_obs](#fun-31c7de2cd6) · [_mitigate_fvgs](#fun-a130bd9445) · [_crossover](#fun-603728af0a) · [_crossunder](#fun-0fd674f4f8) · [_internal_confluence_bars](#fun-d33565e210) · [_append_structure_event](#fun-d317d1876f) · [_update_structure_pivots](#fun-5978222f4d) · [_push_ob](#fun-64ef8badda) · [analyze_luxalgo](#fun-08ff07c7e5)

<a id="fun-80471dd12f"></a>

#### FUN-80471DD12F

| 设计项 | 说明 |
|---|---|
| 函数 | `_true_range` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L71` |
| 签名 | `_true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray)` |
| 参数 | `high`（np.ndarray）：最高价序列或上界<br>`low`（np.ndarray）：最低价序列或下界<br>`close`（np.ndarray）：由调用方提供的 `close` 输入对象 |
| 返回 | 返回 `np.ndarray` 类型结果 |
| 职责 | 生成`true_range`结果；返回 `np.ndarray` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `np.empty` → `range` → `max` → `abs`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `np.ndarray` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、np.empty、range、max、abs |
| 复杂度 / 风险 | 分支 1；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f820754950"></a>

#### FUN-F820754950

| 设计项 | 说明 |
|---|---|
| 函数 | `_atr_series` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L80` |
| 签名 | `_atr_series(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int)` |
| 参数 | `high`（np.ndarray）：最高价序列或上界<br>`low`（np.ndarray）：最低价序列或下界<br>`close`（np.ndarray）：由调用方提供的 `close` 输入对象<br>`period`（int）：计算周期长度 |
| 返回 | 返回 `np.ndarray` 类型结果 |
| 职责 | 生成`atr_series`结果；返回 `np.ndarray` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_true_range` → `np.full` → `range` → `np.mean`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `np.ndarray` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _true_range、np.full、len、range、float、np.mean |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fc6a52d232"></a>

#### FUN-FC6A52D232

| 设计项 | 说明 |
|---|---|
| 函数 | `_leg_at_bar` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L90` |
| 签名 | `_leg_at_bar(highs: np.ndarray, lows: np.ndarray, i: int, size: int, prev_leg: int)` |
| 参数 | `highs`（np.ndarray）：由调用方提供的 `highs` 输入对象<br>`lows`（np.ndarray）：由调用方提供的 `lows` 输入对象<br>`i`（int）：由 `i` 表示的数值参数<br>`size`（int）：由 `size` 表示的数值参数<br>`prev_leg`（int）：由 `prev_leg` 表示的数值参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`leg_at_bar`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `np.max` → `np.min`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、np.max、np.min |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0a1736195c"></a>

#### FUN-0A1736195C

| 设计项 | 说明 |
|---|---|
| 函数 | `_parsed_bar` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L103` |
| 签名 | `_parsed_bar(high: float, low: float, vol: float)` |
| 参数 | `high`（float）：最高价序列或上界<br>`low`（float）：最低价序列或下界<br>`vol`（float）：由 `vol` 表示的数值参数 |
| 返回 | 返回 `tuple[float, float]` 类型结果 |
| 职责 | 构建`parsed_bar`；返回 `tuple[float, float]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8b8bd0c1c0"></a>

#### FUN-8B8BD0C1C0

| 设计项 | 说明 |
|---|---|
| 函数 | `_fvg_threshold` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L109` |
| 签名 | `_fvg_threshold(cum_abs_delta: float, bar_index: int)` |
| 参数 | `cum_abs_delta`（float）：由 `cum_abs_delta` 表示的数值参数<br>`bar_index`（int）：由 `bar_index` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`fvg_threshold`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2052af2dde"></a>

#### FUN-2052AF2DDE

| 设计项 | 说明 |
|---|---|
| 函数 | `_store_order_block` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L115` |
| 签名 | `_store_order_block(parsed_highs: list[float], parsed_lows: list[float], times: list[pd.Timestamp], pivot_index: int, current_index: int, bias: Literal['bullish', 'bearish'])` |
| 参数 | `parsed_highs`（list[float]）：由 `parsed_highs` 表示的输入集合<br>`parsed_lows`（list[float]）：由 `parsed_lows` 表示的输入集合<br>`times`（list[pd.Timestamp]）：由 `times` 表示的输入集合<br>`pivot_index`（int）：由 `pivot_index` 表示的数值参数<br>`current_index`（int）：由 `current_index` 表示的数值参数<br>`bias`（Literal['bullish', 'bearish']）：由调用方提供的 `bias` 输入对象 |
| 返回 | 返回 `OrderBlock \| None` 类型结果 |
| 职责 | 生成`store_order_block`结果；返回 `OrderBlock \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `np.argmax` → `np.argmin` → `OrderBlock`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `OrderBlock \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、np.argmax、np.argmin、OrderBlock、float |
| 复杂度 / 风险 | 分支 4；跨度 28 行；高 |
| 测试 / 验证 | [tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py) · 直接动态测试 |

<a id="fun-31c7de2cd6"></a>

#### FUN-31C7DE2CD6

| 设计项 | 说明 |
|---|---|
| 函数 | `_mitigate_obs` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L145` |
| 签名 | `_mitigate_obs(obs: list[OrderBlock], high: float, low: float)` |
| 参数 | `obs`（list[OrderBlock]）：由 `obs` 表示的输入集合<br>`high`（float）：最高价序列或上界<br>`low`（float）：最低价序列或下界 |
| 返回 | 返回 `list[OrderBlock]` 类型结果 |
| 职责 | 构建`mitigate_obs`；返回 `list[OrderBlock]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `kept.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[OrderBlock]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | kept.append |
| 复杂度 / 风险 | 分支 3；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a130bd9445"></a>

#### FUN-A130BD9445

| 设计项 | 说明 |
|---|---|
| 函数 | `_mitigate_fvgs` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L160` |
| 签名 | `_mitigate_fvgs(fvgs: list[FairValueGap], high: float, low: float)` |
| 参数 | `fvgs`（list[FairValueGap]）：由 `fvgs` 表示的输入集合<br>`high`（float）：最高价序列或上界<br>`low`（float）：最低价序列或下界 |
| 返回 | 返回 `list[FairValueGap]` 类型结果 |
| 职责 | 构建`mitigate_fvgs`；返回 `list[FairValueGap]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `kept.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[FairValueGap]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | kept.append |
| 复杂度 / 风险 | 分支 3；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-603728af0a"></a>

#### FUN-603728AF0A

| 设计项 | 说明 |
|---|---|
| 函数 | `_crossover` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L175` |
| 签名 | `_crossover(close_prev: float, close_curr: float, level: float)` |
| 参数 | `close_prev`（float）：由 `close_prev` 表示的数值参数<br>`close_curr`（float）：由 `close_curr` 表示的数值参数<br>`level`（float）：候选价格水平 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`crossover`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0fd674f4f8"></a>

#### FUN-0FD674F4F8

| 设计项 | 说明 |
|---|---|
| 函数 | `_crossunder` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L179` |
| 签名 | `_crossunder(close_prev: float, close_curr: float, level: float)` |
| 参数 | `close_prev`（float）：由 `close_prev` 表示的数值参数<br>`close_curr`（float）：由 `close_curr` 表示的数值参数<br>`level`（float）：候选价格水平 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`crossunder`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d33565e210"></a>

#### FUN-D33565E210

| 设计项 | 说明 |
|---|---|
| 函数 | `_internal_confluence_bars` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L183` |
| 签名 | `_internal_confluence_bars(open_: float, high: float, low: float, close: float)` |
| 参数 | `open_`（float）：由 `open_` 表示的数值参数<br>`high`（float）：最高价序列或上界<br>`low`（float）：最低价序列或下界<br>`close`（float）：由 `close` 表示的数值参数 |
| 返回 | 返回 `tuple[bool, bool]` 类型结果 |
| 职责 | 判断`internal_confluence_bars`条件是否成立；返回 `tuple[bool, bool]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[bool, bool]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min |
| 复杂度 / 风险 | 分支 0；跨度 11 行；低 |
| 测试 / 验证 | [tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py) · 直接动态测试 |

<a id="fun-d317d1876f"></a>

#### FUN-D317D1876F

| 设计项 | 说明 |
|---|---|
| 函数 | `_append_structure_event` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L196` |
| 签名 | `_append_structure_event(events: list[StructureEvent], *, tag: Literal['BOS', 'CHoCH'], direction: Literal['bullish', 'bearish'], level: float, bar_time: pd.Timestamp, pivot_time: pd.Timestamp \| None, scope: Literal['internal', 'swing'])` |
| 参数 | `events`（list[StructureEvent]）：事件集合<br>`tag`（Literal['BOS', 'CHoCH']）：由调用方提供的 `tag` 输入对象<br>`direction`（Literal['bullish', 'bearish']）：交易方向<br>`level`（float）：候选价格水平<br>`bar_time`（pd.Timestamp）：事件或数据时间<br>`pivot_time`（pd.Timestamp \| None）：事件或数据时间<br>`scope`（Literal['internal', 'swing']）：由调用方提供的 `scope` 输入对象 |
| 返回 | 无返回值（None） |
| 职责 | 追加市场结构事件；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `events.append` → `StructureEvent`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | events.append、StructureEvent |
| 复杂度 / 风险 | 分支 0；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5978222f4d"></a>

#### FUN-5978222F4D

| 设计项 | 说明 |
|---|---|
| 函数 | `_update_structure_pivots` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L218` |
| 签名 | `_update_structure_pivots(*, size: int, leg_prev: int, leg_curr: int, highs: np.ndarray, lows: np.ndarray, index: pd.DatetimeIndex, i: int, pivot_high: _Pivot, pivot_low: _Pivot, trailing: _Trailing \| None, swings: list[SwingPoint], equal_mode: bool, atr_measure: float, equal_prev_low: _Pivot, equal_prev_high: _Pivot, liquidity: list[LiquidityZone])` |
| 参数 | `size`（int）：由 `size` 表示的数值参数<br>`leg_prev`（int）：由 `leg_prev` 表示的数值参数<br>`leg_curr`（int）：由 `leg_curr` 表示的数值参数<br>`highs`（np.ndarray）：由调用方提供的 `highs` 输入对象<br>`lows`（np.ndarray）：由调用方提供的 `lows` 输入对象<br>`index`（pd.DatetimeIndex）：由调用方提供的 `index` 输入对象<br>`i`（int）：由 `i` 表示的数值参数<br>`pivot_high`（_Pivot）：最高价序列或上界<br>`pivot_low`（_Pivot）：最低价序列或下界<br>`trailing`（_Trailing \| None）：由调用方提供的 `trailing` 输入对象<br>`swings`（list[SwingPoint]）：由 `swings` 表示的输入集合<br>`equal_mode`（bool）：运行或分析模式<br>`atr_measure`（float）：由 `atr_measure` 表示的数值参数<br>`equal_prev_low`（_Pivot）：最低价序列或下界<br>`equal_prev_high`（_Pivot）：最高价序列或上界<br>`liquidity`（list[LiquidityZone]）：由 `liquidity` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 更新`structure_pivots`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `abs` → `swings.append` → `SwingPoint`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、abs、swings.append、SwingPoint |
| 复杂度 / 风险 | 分支 11；跨度 67 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-64ef8badda"></a>

#### FUN-64EF8BADDA

| 设计项 | 说明 |
|---|---|
| 函数 | `_push_ob` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L287` |
| 签名 | `_push_ob(blocks: list[OrderBlock], ob: OrderBlock \| None)` |
| 参数 | `blocks`（list[OrderBlock]）：由 `blocks` 表示的输入集合<br>`ob`（OrderBlock \| None）：由调用方提供的 `ob` 输入对象 |
| 返回 | 无返回值（None） |
| 职责 | 执行`push_ob`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `blocks.pop` → `blocks.insert`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、blocks.pop、blocks.insert |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-08ff07c7e5"></a>

#### FUN-08FF07C7E5

| 设计项 | 说明 |
|---|---|
| 函数 | `analyze_luxalgo` |
| 源码位置 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) · `L295` |
| 签名 | `analyze_luxalgo(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `LuxAlgoResult` 类型结果 |
| 职责 | 生成`analyze_luxalgo`结果；返回 `LuxAlgoResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `LuxAlgoResult` → `astype` → `_atr_series` → `_Pivot` → `_Trailing` → `range` → `np.isnan` → `_parsed_bar`；包含 29 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LuxAlgoResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、LuxAlgoResult、astype、_atr_series、_Pivot、_Trailing、range、float、np.isnan、_parsed_bar、parsed_highs.append、parsed_lows.append、times.append、abs、_leg_at_bar、max、np.mean、_update_structure_pivots、_fvg_threshold、fvgs.insert |
| 复杂度 / 风险 | 分支 29；跨度 294 行；高 |
| 测试 / 验证 | [tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py) · 直接动态测试 |

<a id="unit-4f106aec16"></a>

### UNIT-4F106AEC16

**模块**：`src/analysis/narrative_combine.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4F106AEC16 |
| 源码 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/narrative_combine.py` 的职责，通过 `pa_block`、`value_zone_position`、`nearest_pa_sr`、`zone_midpoint`、`resonance_note`、`entry_resonance_text`、`pa_trend_label`、`liquidity_pa_side_text` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 15 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py) |
| 验证状态 | selected |

#### 函数导航

[_fmt](#fun-891202ded4) · [pa_block](#fun-39e6ed0f5b) · [value_zone_position](#fun-411453936c) · [nearest_pa_sr](#fun-98c0107c91) · [zone_midpoint](#fun-9f20c3627c) · [resonance_note](#fun-e61095f39d) · [entry_resonance_text](#fun-9e35377646) · [pa_trend_label](#fun-6d4b2fe2bb) · [liquidity_pa_side_text](#fun-761ec7d9af) · [tf_pa_structure_levels](#fun-59652b92db) · [tf_pa_condition](#fun-0917f96ed2) · [tf_pa_invalidation](#fun-8f862d6445) · [liquidity_side_text](#fun-36832f1f03) · [tf_pa_context_line](#fun-75dd4e0160) · [build_pa_llm_summary](#fun-8a883dd45a)

<a id="fun-891202ded4"></a>

#### FUN-891202DED4

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L29` |
| 签名 | `_fmt(value: Any)` |
| 参数 | `value`（Any）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `number.is_integer` → `rstrip`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、number.is_integer、rstrip |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-39e6ed0f5b"></a>

#### FUN-39E6ED0F5B

| 设计项 | 说明 |
|---|---|
| 函数 | `pa_block` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L37` |
| 签名 | `pa_block(report: dict[str, Any], tf: str)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`tf`（str）：时间框架简称 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`pa_block`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-411453936c"></a>

#### FUN-411453936C

| 设计项 | 说明 |
|---|---|
| 函数 | `value_zone_position` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L41` |
| 签名 | `value_zone_position(price: float \| None, vp: dict[str, Any])` |
| 参数 | `price`（float \| None）：当前或待评估价格<br>`vp`（dict[str, Any]）：由 `vp` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`value_zone_position`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `vp.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | vp.get、float |
| 复杂度 / 风险 | 分支 4；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-98c0107c91"></a>

#### FUN-98C0107C91

| 设计项 | 说明 |
|---|---|
| 函数 | `nearest_pa_sr` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L54` |
| 签名 | `nearest_pa_sr(sr_levels: list[dict[str, Any]], price: float \| None, direction: str, *, limit: int=3)` |
| 参数 | `sr_levels`（list[dict[str, Any]]）：候选价格水平集合<br>`price`（float \| None）：当前或待评估价格<br>`direction`（str）：交易方向<br>`limit`（int）：返回或处理数量上限；默认值 `3` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建最近价格行为支撑阻力；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lvl.get` → `parsed.sort` → `round` → `seen.add` → `out.append` → `_fmt`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lvl.get、float、parsed.sort、set、round、seen.add、str、out.append、_fmt、len |
| 复杂度 / 风险 | 分支 5；跨度 32 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9f20c3627c"></a>

#### FUN-9F20C3627C

| 设计项 | 说明 |
|---|---|
| 函数 | `zone_midpoint` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L88` |
| 签名 | `zone_midpoint(zone: str \| None)` |
| 参数 | `zone`（str \| None）：由调用方提供的 `zone` 输入对象 |
| 返回 | 返回 `float \| None` 类型结果 |
| 职责 | 计算`zone_midpoint`；返回 `float \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `split` → `zone.replace`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | split、zone.replace、float |
| 复杂度 / 风险 | 分支 2；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e61095f39d"></a>

#### FUN-E61095F39D

| 设计项 | 说明 |
|---|---|
| 函数 | `resonance_note` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L98` |
| 签名 | `resonance_note(smc_zone: str \| None, pa_prices: list[float], *, tolerance: float=RESONANCE_TOLERANCE)` |
| 参数 | `smc_zone`（str \| None）：由调用方提供的 `smc_zone` 输入对象<br>`pa_prices`（list[float]）：由 `pa_prices` 表示的输入集合<br>`tolerance`（float）：数值比较容差；默认值 `RESONANCE_TOLERANCE` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`resonance_note`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `zone_midpoint` → `abs`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | zone_midpoint、abs |
| 复杂度 / 风险 | 分支 3；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9e35377646"></a>

#### FUN-9E35377646

| 设计项 | 说明 |
|---|---|
| 函数 | `entry_resonance_text` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L113` |
| 签名 | `entry_resonance_text(signal: dict[str, Any], pa_block_5m: dict[str, Any], *, tolerance: float=RESONANCE_TOLERANCE)` |
| 参数 | `signal`（dict[str, Any]）：当前交易信号<br>`pa_block_5m`（dict[str, Any]）：由 `pa_block_5m` 表示的键值映射<br>`tolerance`（float）：数值比较容差；默认值 `RESONANCE_TOLERANCE` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`entry_resonance_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `signal.get` → `pa_block_5m.get` → `vp.get` → `abs` → `notes.append` → `x.get` → `join` → `dict.fromkeys`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | signal.get、float、pa_block_5m.get、vp.get、abs、notes.append、x.get、join、dict.fromkeys |
| 复杂度 / 风险 | 分支 6；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py) · 直接动态测试 |

<a id="fun-6d4b2fe2bb"></a>

#### FUN-6D4B2FE2BB

| 设计项 | 说明 |
|---|---|
| 函数 | `pa_trend_label` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L139` |
| 签名 | `pa_trend_label(price: float \| None, vp: dict[str, Any])` |
| 参数 | `price`（float \| None）：当前或待评估价格<br>`vp`（dict[str, Any]）：由 `vp` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`pa_trend_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `value_zone_position`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | value_zone_position |
| 复杂度 / 风险 | 分支 3；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-761ec7d9af"></a>

#### FUN-761EC7D9AF

| 设计项 | 说明 |
|---|---|
| 函数 | `liquidity_pa_side_text` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L151` |
| 签名 | `liquidity_pa_side_text(side_label: str, pa_labels: list[str])` |
| 参数 | `side_label`（str）：展示或分类标签<br>`pa_labels`（list[str]）：由 `pa_labels` 表示的输入集合 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`liquidity_pa_side_text`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join |
| 复杂度 / 风险 | 分支 1；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-59652b92db"></a>

#### FUN-59652B92DB

| 设计项 | 说明 |
|---|---|
| 函数 | `tf_pa_structure_levels` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L157` |
| 签名 | `tf_pa_structure_levels(pa_tf: dict[str, Any], price: float \| None, *, tf: str)` |
| 参数 | `pa_tf`（dict[str, Any]）：时间框架简称<br>`price`（float \| None）：当前或待评估价格<br>`tf`（str）：时间框架简称 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`tf_pa_structure_levels`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pa_tf.get` → `vp.get` → `levels.append` → `_fmt` → `nearest_pa_sr` → `join`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pa_tf.get、vp.get、levels.append、_fmt、nearest_pa_sr、len、join |
| 复杂度 / 风险 | 分支 4；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0917f96ed2"></a>

#### FUN-0917F96ED2

| 设计项 | 说明 |
|---|---|
| 函数 | `tf_pa_condition` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L182` |
| 签名 | `tf_pa_condition(tf: str, *, trend: str, vp: dict[str, Any])` |
| 参数 | `tf`（str）：时间框架简称<br>`trend`（str）：由 `trend` 表示的文本或标识<br>`vp`（dict[str, Any]）：由 `vp` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`tf_pa_condition`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8f862d6445"></a>

#### FUN-8F862D6445

| 设计项 | 说明 |
|---|---|
| 函数 | `tf_pa_invalidation` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L192` |
| 签名 | `tf_pa_invalidation(trend: str, vp: dict[str, Any])` |
| 参数 | `trend`（str）：由 `trend` 表示的文本或标识<br>`vp`（dict[str, Any]）：由 `vp` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`tf_pa_invalidation`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `vp.get` → `_fmt`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | vp.get、_fmt |
| 复杂度 / 风险 | 分支 3；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-36832f1f03"></a>

#### FUN-36832F1F03

| 设计项 | 说明 |
|---|---|
| 函数 | `liquidity_side_text` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L203` |
| 签名 | `liquidity_side_text(side_label: str, smc_rows: list[dict[str, Any]], pa_labels: list[str])` |
| 参数 | `side_label`（str）：展示或分类标签<br>`smc_rows`（list[dict[str, Any]]）：记录行集合<br>`pa_labels`（list[str]）：由 `pa_labels` 表示的输入集合 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`liquidity_side_text`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parts.append` → `join` → `_fmt`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | parts.append、join、_fmt |
| 复杂度 / 风险 | 分支 3；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-75dd4e0160"></a>

#### FUN-75DD4E0160

| 设计项 | 说明 |
|---|---|
| 函数 | `tf_pa_context_line` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L218` |
| 签名 | `tf_pa_context_line(tf: str, vp: dict[str, Any], price: float \| None)` |
| 参数 | `tf`（str）：时间框架简称<br>`vp`（dict[str, Any]）：由 `vp` 表示的键值映射<br>`price`（float \| None）：当前或待评估价格 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`tf_pa_context_line`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `vp.get` → `value_zone_position` → `_fmt`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | vp.get、value_zone_position、_fmt |
| 复杂度 / 风险 | 分支 3；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8a883dd45a"></a>

#### FUN-8A883DD45A

| 设计项 | 说明 |
|---|---|
| 函数 | `build_pa_llm_summary` |
| 源码位置 | [src/analysis/narrative_combine.py](../../../src/analysis/narrative_combine.py) · `L231` |
| 签名 | `build_pa_llm_summary(price_action: dict[str, Any], *, price: float \| None)` |
| 参数 | `price_action`（dict[str, Any]）：价格行为分析结果<br>`price`（float \| None）：当前或待评估价格 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`pa_llm_summary`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `price_action.items` → `isinstance` → `block.get` → `vp.get` → `value_zone_position` → `nearest_pa_sr`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | price_action.items、isinstance、block.get、vp.get、value_zone_position、nearest_pa_sr、len |
| 复杂度 / 风险 | 分支 6；跨度 41 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py) · 直接动态测试 |

<a id="unit-b5b5d80eb7"></a>

### UNIT-B5B5D80EB7

**模块**：`src/analysis/narrative_facts.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B5B5D80EB7 |
| 源码 | [src/analysis/narrative_facts.py](../../../src/analysis/narrative_facts.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/narrative_facts.py` 的职责，通过 `build_narrative_facts_for_llm` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py) |
| 验证状态 | selected |

#### 函数导航

[build_narrative_facts_for_llm](#fun-5441c0b28d)

<a id="fun-5441c0b28d"></a>

#### FUN-5441C0B28D

| 设计项 | 说明 |
|---|---|
| 函数 | `build_narrative_facts_for_llm` |
| 源码位置 | [src/analysis/narrative_facts.py](../../../src/analysis/narrative_facts.py) · `L15` |
| 签名 | `build_narrative_facts_for_llm(report: dict[str, Any], *, ctx: MarketContext \| None=None, technical_context: dict[str, Any] \| None=None, event_limit: int \| None=None, compact_for_llm: bool=True)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`ctx`（MarketContext \| None）：运行上下文；默认值 `None`<br>`technical_context`（dict[str, Any] \| None）：运行上下文；默认值 `None`<br>`event_limit`（int \| None）：返回或处理数量上限；默认值 `None`<br>`compact_for_llm`（bool）：控制对应行为是否启用的布尔值；默认值 `True` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`narrative_facts_llm`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_technical_context` → `build_narrative_facts`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_technical_context、build_narrative_facts |
| 复杂度 / 风险 | 分支 3；跨度 16 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py) · 直接动态测试 |

<a id="unit-0d14c54b60"></a>

### UNIT-0D14C54B60

**模块**：`src/analysis/narrative_sections.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0D14C54B60 |
| 源码 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/narrative_sections.py` 的职责，通过 `build_rule_narrative_sections`、`section_to_bullets`、`overview_bullets_from_sections`、`build_narrative_facts`、`validate_and_merge_llm_sections`、`narrative_price_tolerance`、`validate_llm_top_level_fields`、`validate_llm_top_level` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 28 / 4 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_narrative_top_level.py](../../../tests/unit/test_narrative_top_level.py)、[tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_overview_volume_context](#fun-9b4186d596) | 构建`overview_volume_context`；可能影响外部接口；返回 `tuple[dict[str, Any], str]` 类型结果。 | 外部接口 I/O | — |
| [_liquidity_pa_context](#fun-76ad3fd71d) | 构建`liquidity_pa_context`；可能影响外部接口；返回 `tuple[dict[str, Any], str]` 类型结果。 | 外部接口 I/O | — |
| [build_narrative_facts](#fun-6ee7e2523c) | 构建`narrative_facts`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py) |
| [_execution_authorized](#fun-25aeefe31c) | 判断`execution_authorized`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[_fmt](#fun-cafae2be89) · [_section](#fun-77b59ff6c0) · [_intraday_pa_block](#fun-28571ac483) · [_overview_volume_context](#fun-9b4186d596) · [_liquidity_pa_context](#fun-76ad3fd71d) · [build_rule_narrative_sections](#fun-d63e7f97de) · [section_to_bullets](#fun-7fbc737860) · [overview_bullets_from_sections](#fun-becbd2f758) · [build_narrative_facts](#fun-6ee7e2523c) · [build_narrative_facts.add_context](#fun-0717bfae8a) · [build_narrative_facts.add_execution](#fun-287fb686ea) · [validate_and_merge_llm_sections](#fun-f0ff3fb2e4) · [_confidence](#fun-58e4660f21) · [_coerce_string_list](#fun-e6ef29ff95) · [_capped_section_lists](#fun-ca4fa260dd) · [_section_visible_lines](#fun-3a8882518c) · [_normalize_llm_section](#fun-75bc1eba00) · [_validate_section](#fun-5c22fbf976) · [_expected_bias](#fun-21729c6d78) · [narrative_price_tolerance](#fun-74a552c2a1) · [_price_tolerance](#fun-ea3075165b) · [_unapproved_prices](#fun-ee96ece754) · [_unapproved_calendar_claims](#fun-6cde98503a) · [_executable_wording_on_wait](#fun-870e7671a1) · [_direction_conflict](#fun-b4dcb46a68) · [_execution_authorized](#fun-25aeefe31c) · [validate_llm_top_level_fields](#fun-d7185cbde0) · [validate_llm_top_level](#fun-5260c4fffe)

<a id="fun-cafae2be89"></a>

#### FUN-CAFAE2BE89

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L36` |
| 签名 | `_fmt(value: Any)` |
| 参数 | `value`（Any）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `number.is_integer` → `rstrip`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、number.is_integer、rstrip |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-77b59ff6c0"></a>

#### FUN-77B59FF6C0

| 设计项 | 说明 |
|---|---|
| 函数 | `_section` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L44` |
| 签名 | `_section(summary: str, *, context: list[str] \| None=None, levels: list[str] \| None=None, conditions: list[str] \| None=None, invalidation: str='')` |
| 参数 | `summary`（str）：摘要内容<br>`context`（list[str] \| None）：运行上下文；默认值 `None`<br>`levels`（list[str] \| None）：候选价格水平集合；默认值 `None`<br>`conditions`（list[str] \| None）：由 `conditions` 表示的输入集合；默认值 `None`<br>`invalidation`（str）：由 `invalidation` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建文档章节；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `summary.strip` → `invalidation.strip`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | summary.strip、invalidation.strip |
| 复杂度 / 风险 | 分支 0；跨度 19 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-28571ac483"></a>

#### FUN-28571AC483

| 设计项 | 说明 |
|---|---|
| 函数 | `_intraday_pa_block` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L65` |
| 签名 | `_intraday_pa_block(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`intraday_pa_block`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9b4186d596"></a>

#### FUN-9B4186D596

| 设计项 | 说明 |
|---|---|
| 函数 | `_overview_volume_context` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L70` |
| 签名 | `_overview_volume_context(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `tuple[dict[str, Any], str]` 类型结果 |
| 职责 | 构建`overview_volume_context`；可能影响外部接口；返回 `tuple[dict[str, Any], str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_intraday_pa_block` → `get` → `session.get` → `pa_block` → `block.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[dict[str, Any], str]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _intraday_pa_block、get、session.get、pa_block、block.get |
| 复杂度 / 风险 | 分支 3；跨度 10 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-76ad3fd71d"></a>

#### FUN-76AD3FD71D

| 设计项 | 说明 |
|---|---|
| 函数 | `_liquidity_pa_context` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L82` |
| 签名 | `_liquidity_pa_context(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `tuple[dict[str, Any], str]` 类型结果 |
| 职责 | 构建`liquidity_pa_context`；可能影响外部接口；返回 `tuple[dict[str, Any], str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_intraday_pa_block` → `session.get` → `get` → `pa_block` → `block.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[dict[str, Any], str]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _intraday_pa_block、session.get、get、pa_block、block.get |
| 复杂度 / 风险 | 分支 3；跨度 10 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d63e7f97de"></a>

#### FUN-D63E7F97DE

| 设计项 | 说明 |
|---|---|
| 函数 | `build_rule_narrative_sections` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L94` |
| 签名 | `build_rule_narrative_sections(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, dict[str, Any]]` 类型结果 |
| 职责 | 构建`rule_narrative_sections`；返回 `dict[str, dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `metrics.get` → `s.get` → `next` → `pa_trend_label` → `get` → `pa_block` → `max`；包含 17 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、metrics.get、s.get、next、pa_trend_label、get、pa_block、max、set、len、_overview_volume_context、pa_overview.get、_fmt、vp_overview.get、overview_levels.append、primary.get、entry_resonance_text、value_zone_position、str、conclusion.get |
| 复杂度 / 风险 | 分支 17；跨度 109 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py) · 直接动态测试 |

<a id="fun-7fbc737860"></a>

#### FUN-7FBC737860

| 设计项 | 说明 |
|---|---|
| 函数 | `section_to_bullets` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L205` |
| 签名 | `section_to_bullets(section: dict[str, Any])` |
| 参数 | `section`（dict[str, Any]）：由 `section` 表示的键值映射 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`section_to_bullets`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `section.get` → `rows.append` → `rows.extend` → `row.strip`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | section.get、rows.append、str、rows.extend、row.strip |
| 复杂度 / 风险 | 分支 2；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-becbd2f758"></a>

#### FUN-BECBD2F758

| 设计项 | 说明 |
|---|---|
| 函数 | `overview_bullets_from_sections` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L218` |
| 签名 | `overview_bullets_from_sections(sections: dict[str, dict[str, Any]])` |
| 参数 | `sections`（dict[str, dict[str, Any]]）：由 `sections` 表示的键值映射 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 根据`sections`构建`overview_bullets`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `section_to_bullets` → `sections.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | section_to_bullets、sections.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6ee7e2523c"></a>

#### FUN-6EE7E2523C

| 设计项 | 说明 |
|---|---|
| 函数 | `build_narrative_facts` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L223` |
| 签名 | `build_narrative_facts(report: dict[str, Any], technical_context: dict[str, Any], *, compact_for_llm: bool=False)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`technical_context`（dict[str, Any]）：运行上下文<br>`compact_for_llm`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`narrative_facts`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `context_levels.append` → `authorized_execution_levels.append` → `report.get` → `add_context` → `metrics.get` → `enumerate` → `row.get`；包含 27 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、context_levels.append、authorized_execution_levels.append、report.get、add_context、metrics.get、enumerate、row.get、str、items、info.get、s.get、bool、get、signal.get、add_execution、vp.get、lvl.get、technical_context.get |
| 复杂度 / 风险 | 分支 27；跨度 165 行；高 |
| 测试 / 验证 | [tests/unit/test_narrative_combine.py](../../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py) · 直接动态测试 |

<a id="fun-0717bfae8a"></a>

#### FUN-0717BFAE8A

| 设计项 | 说明 |
|---|---|
| 函数 | `build_narrative_facts.add_context` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L233` |
| 签名 | `build_narrative_facts.add_context(level_id: str, value: Any, source: str, *, timeframe: str \| None=None, kind: str='level')` |
| 参数 | `level_id`（str）：对象标识<br>`value`（Any）：待处理值<br>`source`（str）：数据或证据来源<br>`timeframe`（str \| None）：行情时间框架；默认值 `None`<br>`kind`（str）：类别标识；默认值 `'level'` |
| 返回 | 无返回值（None） |
| 职责 | 添加上下文；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `context_levels.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、context_levels.append |
| 复杂度 / 风险 | 分支 2；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-287fb686ea"></a>

#### FUN-287FB686EA

| 设计项 | 说明 |
|---|---|
| 函数 | `build_narrative_facts.add_execution` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L244` |
| 签名 | `build_narrative_facts.add_execution(level_id: str, value: Any, source: str, *, signal_id: str, kind: str='execution')` |
| 参数 | `level_id`（str）：对象标识<br>`value`（Any）：待处理值<br>`source`（str）：数据或证据来源<br>`signal_id`（str）：对象标识<br>`kind`（str）：类别标识；默认值 `'execution'` |
| 返回 | 无返回值（None） |
| 职责 | 添加`execution`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `authorized_execution_levels.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、authorized_execution_levels.append |
| 复杂度 / 风险 | 分支 2；跨度 16 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f0ff3fb2e4"></a>

#### FUN-F0FF3FB2E4

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_and_merge_llm_sections` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L390` |
| 签名 | `validate_and_merge_llm_sections(raw_sections: Any, *, rule_sections: dict[str, dict[str, Any]], facts: dict[str, Any], mode: str, threshold: float)` |
| 参数 | `raw_sections`（Any）：由调用方提供的 `raw_sections` 输入对象<br>`rule_sections`（dict[str, dict[str, Any]]）：由 `rule_sections` 表示的键值映射<br>`facts`（dict[str, Any]）：结构化事实集合<br>`mode`（str）：运行或分析模式<br>`threshold`（float）：由 `threshold` 表示的数值参数 |
| 返回 | 返回 `tuple[dict[str, dict[str, Any]], dict[str, Any]]` 类型结果 |
| 职责 | 验证`and_merge_llm_sections`；返回 `tuple[dict[str, dict[str, Any]], dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `facts.get` → `_expected_bias` → `isinstance` → `common.get` → `strip` → `supplied.get` → `_validate_section`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, dict[str, Any]], dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、facts.get、_expected_bias、isinstance、str、common.get、strip、supplied.get、_validate_section、_confidence、_normalize_llm_section、deepcopy、rule_sections.get、_section |
| 复杂度 / 风险 | 分支 4；跨度 48 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py) · 直接动态测试 |

<a id="fun-58e4660f21"></a>

#### FUN-58E4660F21

| 设计项 | 说明 |
|---|---|
| 函数 | `_confidence` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L440` |
| 签名 | `_confidence(value: Any)` |
| 参数 | `value`（Any）：待处理值 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算置信度；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、float、get |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e6ef29ff95"></a>

#### FUN-E6EF29FF95

| 设计项 | 说明 |
|---|---|
| 函数 | `_coerce_string_list` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L447` |
| 签名 | `_coerce_string_list(value: Any)` |
| 参数 | `value`（Any）：待处理值 |
| 返回 | 返回 `list[str] \| None` 类型结果 |
| 职责 | 构建`coerce_string_list`；返回 `list[str] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `value.strip` → `item.strip` → `out.append`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、value.strip、item.strip、out.append、str |
| 复杂度 / 风险 | 分支 9；跨度 25 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ca4fa260dd"></a>

#### FUN-CA4FA260DD

| 设计项 | 说明 |
|---|---|
| 函数 | `_capped_section_lists` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L474` |
| 签名 | `_capped_section_lists(value: dict[str, Any])` |
| 参数 | `value`（dict[str, Any]）：待处理值 |
| 返回 | 返回 `dict[str, list[str]]` 类型结果 |
| 职责 | 构建`capped_section_lists`；返回 `dict[str, list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_SECTION_LIST_CAPS.items` → `_coerce_string_list` → `value.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _SECTION_LIST_CAPS.items、_coerce_string_list、value.get |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3a8882518c"></a>

#### FUN-3A8882518C

| 设计项 | 说明 |
|---|---|
| 函数 | `_section_visible_lines` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L484` |
| 签名 | `_section_visible_lines(value: dict[str, Any])` |
| 参数 | `value`（dict[str, Any]）：待处理值 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`section_visible_lines`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_capped_section_lists` → `strip` → `value.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _capped_section_lists、strip、str、value.get、len |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-75bc1eba00"></a>

#### FUN-75BC1EBA00

| 设计项 | 说明 |
|---|---|
| 函数 | `_normalize_llm_section` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L492` |
| 签名 | `_normalize_llm_section(value: dict[str, Any])` |
| 参数 | `value`（dict[str, Any]）：待处理值 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 标准化`llm_section`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_capped_section_lists` → `strip` → `_confidence`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _capped_section_lists、strip、str、_confidence |
| 复杂度 / 风险 | 分支 0；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5c22fbf976"></a>

#### FUN-5C22FBF976

| 设计项 | 说明 |
|---|---|
| 函数 | `_validate_section` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L506` |
| 签名 | `_validate_section(value: Any, *, allowed: set[float], expected_bias: str, calendar_state: str='', allowed_calendar_times: set[str] \| None=None)` |
| 参数 | `value`（Any）：待处理值<br>`allowed`（set[float]）：由 `allowed` 表示的输入集合<br>`expected_bias`（str）：由 `expected_bias` 表示的文本或标识<br>`calendar_state`（str）：状态对象；默认值 `''`<br>`allowed_calendar_times`（set[str] \| None）：由 `allowed_calendar_times` 表示的输入集合；默认值 `None` |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 验证文档章节；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `value.get` → `strip` → `_coerce_string_list` → `_section_visible_lines` → `join` → `_NUMBER_RE.findall` → `any`；包含 13 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、str、value.get、strip、_coerce_string_list、_section_visible_lines、join、_NUMBER_RE.findall、float、any、abs、narrative_price_tolerance、_unapproved_calendar_claims、set |
| 复杂度 / 风险 | 分支 13；跨度 55 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-21729c6d78"></a>

#### FUN-21729C6D78

| 设计项 | 说明 |
|---|---|
| 函数 | `_expected_bias` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L563` |
| 签名 | `_expected_bias(facts: dict[str, Any])` |
| 参数 | `facts`（dict[str, Any]）：结构化事实集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`expected_bias`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `facts.get` → `common.get` → `lower` → `signal.get` → `decision.get` → `sentiment.get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | facts.get、common.get、lower、str、signal.get、decision.get、float、sentiment.get |
| 复杂度 / 风险 | 分支 5；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-74a552c2a1"></a>

#### FUN-74A552C2A1

| 设计项 | 说明 |
|---|---|
| 函数 | `narrative_price_tolerance` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L581` |
| 签名 | `narrative_price_tolerance(token: str, reference: float)` |
| 参数 | `token`（str）：标记或认证令牌<br>`reference`（float）：由 `reference` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`narrative_price_tolerance`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `token.split` → `frac.rstrip`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | token.split、frac.rstrip、len |
| 复杂度 / 风险 | 分支 3；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ea3075165b"></a>

#### FUN-EA3075165B

| 设计项 | 说明 |
|---|---|
| 函数 | `_price_tolerance` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L602` |
| 签名 | `_price_tolerance(reference: float)` |
| 参数 | `reference`（float）：由 `reference` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`price_tolerance`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `abs`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、abs |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ee96ece754"></a>

#### FUN-EE96ECE754

| 设计项 | 说明 |
|---|---|
| 函数 | `_unapproved_prices` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L607` |
| 签名 | `_unapproved_prices(text: str, allowed: set[float])` |
| 参数 | `text`（str）：输入文本<br>`allowed`（set[float]）：由 `allowed` 表示的输入集合 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`unapproved_prices`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_NUMBER_RE.findall` → `any` → `abs` → `narrative_price_tolerance`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _NUMBER_RE.findall、float、any、abs、narrative_price_tolerance |
| 复杂度 / 风险 | 分支 4；跨度 13 行；低 |
| 测试 / 验证 | [tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py) · 直接动态测试 |

<a id="fun-6cde98503a"></a>

#### FUN-6CDE98503A

| 设计项 | 说明 |
|---|---|
| 函数 | `_unapproved_calendar_claims` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L629` |
| 签名 | `_unapproved_calendar_claims(text: str, *, calendar_state: str, allowed_times: set[str])` |
| 参数 | `text`（str）：输入文本<br>`calendar_state`（str）：状态对象<br>`allowed_times`（set[str]）：由 `allowed_times` 表示的输入集合 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`unapproved_calendar_claims`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `text.strip` → `_CALENDAR_CLAIM_RE.finditer` → `strip` → `match.group` → `any` → `t.endswith` → `clock.endswith`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | text.strip、_CALENDAR_CLAIM_RE.finditer、strip、match.group、any、t.endswith、clock.endswith |
| 复杂度 / 风险 | 分支 6；跨度 24 行；低 |
| 测试 / 验证 | [tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py) · 直接动态测试 |

<a id="fun-870e7671a1"></a>

#### FUN-870E7671A1

| 设计项 | 说明 |
|---|---|
| 函数 | `_executable_wording_on_wait` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L687` |
| 签名 | `_executable_wording_on_wait(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`executable_wording_on_wait`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `any` → `re.search`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | any、re.search |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b4dcb46a68"></a>

#### FUN-B4DCB46A68

| 设计项 | 说明 |
|---|---|
| 函数 | `_direction_conflict` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L693` |
| 签名 | `_direction_conflict(text: str, expected_bias: str)` |
| 参数 | `text`（str）：输入文本<br>`expected_bias`（str）：由 `expected_bias` 表示的文本或标识 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 生成`direction_conflict`文本；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `any`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | any |
| 复杂度 / 风险 | 分支 2；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-25aeefe31c"></a>

#### FUN-25AEEFE31C

| 设计项 | 说明 |
|---|---|
| 函数 | `_execution_authorized` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L705` |
| 签名 | `_execution_authorized(facts: dict[str, Any])` |
| 参数 | `facts`（dict[str, Any]）：结构化事实集合 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`execution_authorized`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `facts.get` → `common.get` → `decision.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | facts.get、common.get、str、decision.get |
| 复杂度 / 风险 | 分支 2；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d7185cbde0"></a>

#### FUN-D7185CBDE0

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_llm_top_level_fields` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L716` |
| 签名 | `validate_llm_top_level_fields(llm: dict[str, Any], *, facts: dict[str, Any])` |
| 参数 | `llm`（dict[str, Any]）：由 `llm` 表示的键值映射<br>`facts`（dict[str, Any]）：结构化事实集合 |
| 返回 | 返回 `dict[str, str \| None]` 类型结果 |
| 职责 | 验证`llm_top_level_fields`；返回 `dict[str, str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `facts.get` → `_execution_authorized` → `_expected_bias` → `get` → `decision.get` → `common.get` → `strip`；包含 14 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、facts.get、_execution_authorized、_expected_bias、get、str、decision.get、common.get、strip、llm.get、any、value.strip、fields.values、sum、value.count、fields.items、text.strip、_unapproved_prices、_unapproved_calendar_claims |
| 复杂度 / 风险 | 分支 14；跨度 71 行；中 |
| 测试 / 验证 | [tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py)、[tests/unit/test_narrative_top_level.py](../../../tests/unit/test_narrative_top_level.py) · 直接动态测试 |

<a id="fun-5260c4fffe"></a>

#### FUN-5260C4FFFE

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_llm_top_level` |
| 源码位置 | [src/analysis/narrative_sections.py](../../../src/analysis/narrative_sections.py) · `L789` |
| 签名 | `validate_llm_top_level(llm: dict[str, Any], *, facts: dict[str, Any])` |
| 参数 | `llm`（dict[str, Any]）：由 `llm` 表示的键值映射<br>`facts`（dict[str, Any]）：结构化事实集合 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 验证`llm_top_level`；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `validate_llm_top_level_fields` → `field_reasons.values`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | validate_llm_top_level_fields、field_reasons.values |
| 复杂度 / 风险 | 分支 2；跨度 11 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_top_level.py](../../../tests/unit/test_narrative_top_level.py) · 直接动态测试 |

<a id="unit-406cec1297"></a>

### UNIT-406CEC1297

**模块**：`src/analysis/plan_signals.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-406CEC1297 |
| 源码 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/plan_signals.py` 的职责，通过 `pa_usable`、`build_rule_pa_block`、`smc_filter_adjustment`、`val_sweep_confirmed`、`build_pa_short_aggressive`、`build_pa_short_conservative`、`build_pa_long_sweep` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 20 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_plan_signal_targets.py](../../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_plan_signals.py](../../../tests/unit/test_plan_signals.py) |
| 验证状态 | selected |

#### 函数导航

[pa_usable](#fun-df2b309e7a) · [_rule_sr_level](#fun-edbd519580) · [build_rule_pa_block](#fun-a04f67d803) · [_atr](#fun-d4e38583ee) · [_zone_band](#fun-7820ca9cf2) · [_nearest_pa_sr](#fun-b2869caf10) · [_vah_zone](#fun-0cc973c97b) · [_resistance_zone](#fun-0924b3ca47) · [_val_zone](#fun-2dc7daba92) · [_support_zone](#fun-05d58d82e1) · [_sell_targets](#fun-ce8413dcd6) · [_buy_targets](#fun-e65ed5c0aa) · [_smc_zones](#fun-88ad48e01b) · [_zone_overlaps_entry](#fun-e5ee860a8a) · [_structure_shifted](#fun-9a867fc2bd) · [smc_filter_adjustment](#fun-cd33dcdad5) · [val_sweep_confirmed](#fun-9cd2c897d0) · [build_pa_short_aggressive](#fun-8f66092349) · [build_pa_short_conservative](#fun-f24046f4b0) · [build_pa_long_sweep](#fun-c5a6f97a5f)

<a id="fun-df2b309e7a"></a>

#### FUN-DF2B309E7A

| 设计项 | 说明 |
|---|---|
| 函数 | `pa_usable` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L30` |
| 签名 | `pa_usable(price_action: dict[str, Any] \| None)` |
| 参数 | `price_action`（dict[str, Any] \| None）：价格行为分析结果 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`pa_usable`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `price_action.get` → `block.get` → `vp.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | price_action.get、block.get、vp.get、bool |
| 复杂度 / 风险 | 分支 2；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-edbd519580"></a>

#### FUN-EDBD519580

| 设计项 | 说明 |
|---|---|
| 函数 | `_rule_sr_level` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L41` |
| 签名 | `_rule_sr_level(price: float, direction: str, label: str)` |
| 参数 | `price`（float）：当前或待评估价格<br>`direction`（str）：交易方向<br>`label`（str）：展示或分类标签 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`rule_sr_level`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a04f67d803"></a>

#### FUN-A04F67D803

| 设计项 | 说明 |
|---|---|
| 函数 | `build_rule_pa_block` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L51` |
| 签名 | `build_rule_pa_block(*, price: float, swing_high: float, swing_low: float, analysis_5m: TimeframeAnalysis, price_action: dict[str, Any] \| None=None, metrics: dict[str, Any] \| None=None)` |
| 参数 | `price`（float）：当前或待评估价格<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`price_action`（dict[str, Any] \| None）：价格行为分析结果；默认值 `None`<br>`metrics`（dict[str, Any] \| None）：由 `metrics` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`rule_pa_block`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `pa5.get` → `existing_vp.get` → `metrics.get` → `vp.get` → `round` → `min` → `max`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、pa5.get、existing_vp.get、metrics.get、vp.get、float、round、min、max、list、any、lvl.get、abs、sr_levels.append、_rule_sr_level、bool |
| 复杂度 / 风险 | 分支 10；跨度 74 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d4e38583ee"></a>

#### FUN-D4E38583EE

| 设计项 | 说明 |
|---|---|
| 函数 | `_atr` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L127` |
| 签名 | `_atr(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` |
| 参数 | `analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`atr`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7820ca9cf2"></a>

#### FUN-7820CA9CF2

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_band` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L131` |
| 签名 | `_zone_band(center: float, atr: float, *, ratio: float=0.2)` |
| 参数 | `center`（float）：由 `center` 表示的数值参数<br>`atr`（float）：平均真实波幅<br>`ratio`（float）：由 `ratio` 表示的数值参数；默认值 `0.2` |
| 返回 | 返回 `tuple[float, float]` 类型结果 |
| 职责 | 构建`zone_band`；返回 `tuple[float, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、round |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b2869caf10"></a>

#### FUN-B2869CAF10

| 设计项 | 说明 |
|---|---|
| 函数 | `_nearest_pa_sr` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L136` |
| 签名 | `_nearest_pa_sr(sr_levels: list[dict[str, Any]], price: float, direction: str)` |
| 参数 | `sr_levels`（list[dict[str, Any]]）：候选价格水平集合<br>`price`（float）：当前或待评估价格<br>`direction`（str）：交易方向 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 构建最近价格行为支撑阻力；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lvl.get` → `parsed.sort`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lvl.get、float、parsed.sort |
| 复杂度 / 风险 | 分支 2；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0cc973c97b"></a>

#### FUN-0CC973C97B

| 设计项 | 说明 |
|---|---|
| 函数 | `_vah_zone` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L156` |
| 签名 | `_vah_zone(vp: dict[str, Any], atr: float)` |
| 参数 | `vp`（dict[str, Any]）：由 `vp` 表示的键值映射<br>`atr`（float）：平均真实波幅 |
| 返回 | 返回 `_PaZone \| None` 类型结果 |
| 职责 | 生成`vah_zone`结果；返回 `_PaZone \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `vp.get` → `_zone_band` → `_PaZone`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `_PaZone \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | vp.get、_zone_band、float、_PaZone |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0924b3ca47"></a>

#### FUN-0924B3CA47

| 设计项 | 说明 |
|---|---|
| 函数 | `_resistance_zone` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L164` |
| 签名 | `_resistance_zone(sr: dict[str, Any], atr: float)` |
| 参数 | `sr`（dict[str, Any]）：由 `sr` 表示的键值映射<br>`atr`（float）：平均真实波幅 |
| 返回 | 返回 `_PaZone` 类型结果 |
| 职责 | 生成`resistance_zone`结果；返回 `_PaZone` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_zone_band` → `sr.get` → `_PaZone`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `_PaZone` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_zone_band、str、sr.get、_PaZone |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2dc7daba92"></a>

#### FUN-2DC7DABA92

| 设计项 | 说明 |
|---|---|
| 函数 | `_val_zone` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L171` |
| 签名 | `_val_zone(vp: dict[str, Any], atr: float)` |
| 参数 | `vp`（dict[str, Any]）：由 `vp` 表示的键值映射<br>`atr`（float）：平均真实波幅 |
| 返回 | 返回 `_PaZone \| None` 类型结果 |
| 职责 | 生成`val_zone`结果；返回 `_PaZone \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `vp.get` → `_zone_band` → `_PaZone`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `_PaZone \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | vp.get、_zone_band、float、_PaZone |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-05d58d82e1"></a>

#### FUN-05D58D82E1

| 设计项 | 说明 |
|---|---|
| 函数 | `_support_zone` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L179` |
| 签名 | `_support_zone(sr: dict[str, Any], atr: float)` |
| 参数 | `sr`（dict[str, Any]）：由 `sr` 表示的键值映射<br>`atr`（float）：平均真实波幅 |
| 返回 | 返回 `_PaZone` 类型结果 |
| 职责 | 生成`support_zone`结果；返回 `_PaZone` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_zone_band` → `sr.get` → `_PaZone` → `round` → `max`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `_PaZone` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_zone_band、str、sr.get、_PaZone、round、max |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ce8413dcd6"></a>

#### FUN-CE8413DCD6

| 设计项 | 说明 |
|---|---|
| 函数 | `_sell_targets` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L186` |
| 签名 | `_sell_targets(entry_low: float, entry_high: float, *, poc: float \| None, val: float \| None, swing_low: float)` |
| 参数 | `entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`poc`（float \| None）：由调用方提供的 `poc` 输入对象<br>`val`（float \| None）：由调用方提供的 `val` 输入对象<br>`swing_low`（float）：摆动低点价格 |
| 返回 | 返回 `tuple[float, float, float] \| None` 类型结果 |
| 职责 | 构建`sell_targets`；返回 `tuple[float, float, float] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `round` → `candidates.append` → `normalize_take_profits`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float, float] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、round、float、candidates.append、normalize_take_profits、len |
| 复杂度 / 风险 | 分支 6；跨度 39 行；低 |
| 测试 / 验证 | [tests/unit/test_plan_signal_targets.py](../../../tests/unit/test_plan_signal_targets.py) · 直接动态测试 |

<a id="fun-e65ed5c0aa"></a>

#### FUN-E65ED5C0AA

| 设计项 | 说明 |
|---|---|
| 函数 | `_buy_targets` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L227` |
| 签名 | `_buy_targets(entry_low: float, entry_high: float, *, price: float, poc: float \| None, vah: float \| None, swing_high: float, swing_low: float)` |
| 参数 | `entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`price`（float）：当前或待评估价格<br>`poc`（float \| None）：由调用方提供的 `poc` 输入对象<br>`vah`（float \| None）：由调用方提供的 `vah` 输入对象<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格 |
| 返回 | 返回 `tuple[float, float, float]` 类型结果 |
| 职责 | 构建`buy_targets`；返回 `tuple[float, float, float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `candidates.append` → `normalize_take_profits` → `ordered.append` → `max`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float、candidates.append、normalize_take_profits、len、ordered.append、max |
| 复杂度 / 风险 | 分支 6；跨度 37 行；低 |
| 测试 / 验证 | [tests/unit/test_plan_signal_targets.py](../../../tests/unit/test_plan_signal_targets.py) · 直接动态测试 |

<a id="fun-88ad48e01b"></a>

#### FUN-88AD48E01B

| 设计项 | 说明 |
|---|---|
| 函数 | `_smc_zones` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L266` |
| 签名 | `_smc_zones(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` |
| 参数 | `analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析 |
| 返回 | 返回 `list[tuple[float, float, str]]` 类型结果 |
| 职责 | 构建`smc_zones`；返回 `list[tuple[float, float, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `zones.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[tuple[float, float, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | zones.append |
| 复杂度 / 风险 | 分支 3；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e5ee860a8a"></a>

#### FUN-E5EE860A8A

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_overlaps_entry` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L276` |
| 签名 | `_zone_overlaps_entry(zone_low: float, zone_high: float, entry_low: float, entry_high: float, *, tolerance: float=RESONANCE_TOLERANCE)` |
| 参数 | `zone_low`（float）：最低价序列或下界<br>`zone_high`（float）：最高价序列或上界<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`tolerance`（float）：数值比较容差；默认值 `RESONANCE_TOLERANCE` |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`zone_overlaps_entry`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `abs`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | abs |
| 复杂度 / 风险 | 分支 1；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9a867fc2bd"></a>

#### FUN-9A867FC2BD

| 设计项 | 说明 |
|---|---|
| 函数 | `_structure_shifted` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L291` |
| 签名 | `_structure_shifted(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, *, direction: str)` |
| 参数 | `analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析<br>`direction`（str）：交易方向 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`structure_shifted`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `direction.lower` → `any` → `lower` → `upper`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | direction.lower、any、lower、upper |
| 复杂度 / 风险 | 分支 0；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cd33dcdad5"></a>

#### FUN-CD33DCDAD5

| 设计项 | 说明 |
|---|---|
| 函数 | `smc_filter_adjustment` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L306` |
| 签名 | `smc_filter_adjustment(*, direction: str, entry_low: float, entry_high: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析 |
| 返回 | 返回 `_SmcFilter` 类型结果 |
| 职责 | 筛选`smc_adjustment`；返回 `_SmcFilter` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `join` → `sorted` → `reasons.append` → `_smc_zones` → `_zone_overlaps_entry` → `_SmcFilter`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `_SmcFilter` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、join、sorted、reasons.append、_smc_zones、_zone_overlaps_entry、_SmcFilter |
| 复杂度 / 风险 | 分支 8；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_plan_signals.py](../../../tests/unit/test_plan_signals.py) · 直接动态测试 |

<a id="fun-9cd2c897d0"></a>

#### FUN-9CD2C897D0

| 设计项 | 说明 |
|---|---|
| 函数 | `val_sweep_confirmed` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L352` |
| 签名 | `val_sweep_confirmed(*, price: float, val: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` |
| 参数 | `price`（float）：当前或待评估价格<br>`val`（float）：由 `val` 表示的数值参数<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析 |
| 返回 | 返回 `tuple[bool, list[str]]` 类型结果 |
| 职责 | 判断`val_sweep_confirmed`条件是否成立；返回 `tuple[bool, list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_atr` → `max` → `_structure_shifted` → `reasons.append`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[bool, list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _atr、max、float、_structure_shifted、reasons.append |
| 复杂度 / 风险 | 分支 5；跨度 30 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8f66092349"></a>

#### FUN-8F66092349

| 设计项 | 说明 |
|---|---|
| 函数 | `build_pa_short_aggressive` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L384` |
| 签名 | `build_pa_short_aggressive(*, price: float, pa_block: dict[str, Any], swing_low: float, atr: float)` |
| 参数 | `price`（float）：当前或待评估价格<br>`pa_block`（dict[str, Any]）：由 `pa_block` 表示的键值映射<br>`swing_low`（float）：摆动低点价格<br>`atr`（float）：平均真实波幅 |
| 返回 | 返回 `tuple[_PaZone, float, list[float]] \| None` 类型结果 |
| 职责 | 构建`pa_short_aggressive`；返回 `tuple[_PaZone, float, list[float]] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_nearest_pa_sr` → `pa_block.get` → `_resistance_zone` → `_sell_targets` → `vp.get` → `max` → `round`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[_PaZone, float, list[float]] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _nearest_pa_sr、pa_block.get、_resistance_zone、float、_sell_targets、vp.get、max、round、list |
| 复杂度 / 风险 | 分支 3；跨度 26 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f24046f4b0"></a>

#### FUN-F24046F4B0

| 设计项 | 说明 |
|---|---|
| 函数 | `build_pa_short_conservative` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L412` |
| 签名 | `build_pa_short_conservative(*, price: float, pa_block: dict[str, Any], swing_low: float, atr: float)` |
| 参数 | `price`（float）：当前或待评估价格<br>`pa_block`（dict[str, Any]）：由 `pa_block` 表示的键值映射<br>`swing_low`（float）：摆动低点价格<br>`atr`（float）：平均真实波幅 |
| 返回 | 返回 `tuple[_PaZone, float, list[float]] \| None` 类型结果 |
| 职责 | 构建`pa_short_conservative`；返回 `tuple[_PaZone, float, list[float]] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pa_block.get` → `_vah_zone` → `_nearest_pa_sr` → `_resistance_zone` → `_sell_targets` → `vp.get` → `max` → `round`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[_PaZone, float, list[float]] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pa_block.get、_vah_zone、_nearest_pa_sr、_resistance_zone、_sell_targets、vp.get、max、round、list |
| 复杂度 / 风险 | 分支 3；跨度 26 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c5a6f97a5f"></a>

#### FUN-C5A6F97A5F

| 设计项 | 说明 |
|---|---|
| 函数 | `build_pa_long_sweep` |
| 源码位置 | [src/analysis/plan_signals.py](../../../src/analysis/plan_signals.py) · `L440` |
| 签名 | `build_pa_long_sweep(*, price: float, pa_block: dict[str, Any], swing_high: float, swing_low: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` |
| 参数 | `price`（float）：当前或待评估价格<br>`pa_block`（dict[str, Any]）：由 `pa_block` 表示的键值映射<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析 |
| 返回 | 返回 `tuple[_PaZone, float, list[float], bool, list[str]] \| None` 类型结果 |
| 职责 | 构建`pa_long_sweep`；返回 `tuple[_PaZone, float, list[float], bool, list[str]] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pa_block.get` → `_atr` → `vp.get` → `max` → `round` → `_PaZone` → `val_sweep_confirmed` → `_nearest_pa_sr`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[_PaZone, float, list[float], bool, list[str]] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pa_block.get、_atr、vp.get、max、round、float、_PaZone、val_sweep_confirmed、_nearest_pa_sr、_support_zone、list、_buy_targets |
| 复杂度 / 风险 | 分支 2；跨度 52 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-daf97d09e5"></a>

### UNIT-DAF97D09E5

**模块**：`src/analysis/price_action_facts.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAF97D09E5 |
| 源码 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/price_action_facts.py` 的职责，通过 `build_session_price_action_block`、`build_price_action_summaries`、`chart_sr_levels` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) |
| 验证状态 | selected |

#### 函数导航

[_ltf_covers_window](#fun-c06b90a09b) · [_align_timestamp](#fun-bce4e6db5f) · [_bars_for_latest_session_day](#fun-cf1adc9362) · [_session_matches_daily](#fun-a13f4e6eec) · [build_session_price_action_block](#fun-6da9739c93) · [build_price_action_summaries](#fun-c677f127b2) · [chart_sr_levels](#fun-edaa738364)

<a id="fun-c06b90a09b"></a>

#### FUN-C06B90A09B

| 设计项 | 说明 |
|---|---|
| 函数 | `_ltf_covers_window` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L24` |
| 签名 | `_ltf_covers_window(ltf_slice: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp, *, min_frac: float=_LTF_COVER_FRAC)` |
| 参数 | `ltf_slice`（pd.DataFrame）：由调用方提供的 `ltf_slice` 输入对象<br>`start`（pd.Timestamp）：由调用方提供的 `start` 输入对象<br>`end`（pd.Timestamp）：由调用方提供的 `end` 输入对象<br>`min_frac`（float）：由 `min_frac` 表示的数值参数；默认值 `_LTF_COVER_FRAC` |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`ltf_covers_window`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `total_seconds` → `pd.Timestamp` → `max` → `min`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | total_seconds、pd.Timestamp、max、min |
| 复杂度 / 风险 | 分支 3；跨度 19 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-bce4e6db5f"></a>

#### FUN-BCE4E6DB5F

| 设计项 | 说明 |
|---|---|
| 函数 | `_align_timestamp` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L45` |
| 签名 | `_align_timestamp(ts: pd.Timestamp, ref: pd.DatetimeIndex)` |
| 参数 | `ts`（pd.Timestamp）：由调用方提供的 `ts` 输入对象<br>`ref`（pd.DatetimeIndex）：由调用方提供的 `ref` 输入对象 |
| 返回 | 返回 `pd.Timestamp` 类型结果 |
| 职责 | 生成`align_timestamp`结果；返回 `pd.Timestamp` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.Timestamp` → `tz_convert` → `ts.tz_localize` → `ts.tz_convert` → `tz_localize`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Timestamp` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.Timestamp、tz_convert、ts.tz_localize、ts.tz_convert、tz_localize |
| 复杂度 / 风险 | 分支 3；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cf1adc9362"></a>

#### FUN-CF1ADC9362

| 设计项 | 说明 |
|---|---|
| 函数 | `_bars_for_latest_session_day` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L56` |
| 签名 | `_bars_for_latest_session_day(df_5m: pd.DataFrame, df_1d: pd.DataFrame)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`df_1d`（pd.DataFrame）：由调用方提供的 `df_1d` 输入对象 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 构建`bars_for_latest_session_day`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `_align_timestamp` → `min` → `pd.Timedelta`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、_align_timestamp、min、pd.Timedelta |
| 复杂度 / 风险 | 分支 2；跨度 15 行；低 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="fun-a13f4e6eec"></a>

#### FUN-A13F4E6EEC

| 设计项 | 说明 |
|---|---|
| 函数 | `_session_matches_daily` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L73` |
| 签名 | `_session_matches_daily(df_session: pd.DataFrame, daily_row: pd.Series, *, tol: float)` |
| 参数 | `df_session`（pd.DataFrame）：会话对象<br>`daily_row`（pd.Series）：当前记录行<br>`tol`（float）：由 `tol` 表示的数值参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`session_matches_daily`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `abs`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、max、min、abs |
| 复杂度 / 风险 | 分支 1；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6da9739c93"></a>

#### FUN-6DA9739C93

| 设计项 | 说明 |
|---|---|
| 函数 | `build_session_price_action_block` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L86` |
| 签名 | `build_session_price_action_block(df_5m: pd.DataFrame \| None, df_1d: pd.DataFrame \| None)` |
| 参数 | `df_5m`（pd.DataFrame \| None）：5 分钟 OHLCV 数据表<br>`df_1d`（pd.DataFrame \| None）：由调用方提供的 `df_1d` 输入对象 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 构建`session_price_action_block`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_bars_for_latest_session_day` → `_session_matches_daily` → `analyze_dgt_price_action` → `dgt_result_to_dict`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _bars_for_latest_session_day、_session_matches_daily、len、analyze_dgt_price_action、dgt_result_to_dict |
| 复杂度 / 风险 | 分支 4；跨度 22 行；中 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="fun-c677f127b2"></a>

#### FUN-C677F127B2

| 设计项 | 说明 |
|---|---|
| 函数 | `build_price_action_summaries` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L110` |
| 签名 | `build_price_action_summaries(data: dict[str, pd.DataFrame], *, lookback: int=DEFAULT_LOOKBACK)` |
| 参数 | `data`（dict[str, pd.DataFrame]）：输入数据<br>`lookback`（int）：由 `lookback` 表示的数值参数；默认值 `DEFAULT_LOOKBACK` |
| 返回 | 返回 `dict[str, dict[str, Any]]` 类型结果 |
| 职责 | 构建`price_action_summaries`；返回 `dict[str, dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `data.get` → `df.tail` → `_ltf_covers_window` → `analyze_dgt_price_action` → `dgt_result_to_dict` → `build_session_price_action_block`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | data.get、df.tail、_ltf_covers_window、analyze_dgt_price_action、dgt_result_to_dict、build_session_price_action_block |
| 复杂度 / 风险 | 分支 5；跨度 39 行；中 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="fun-edaa738364"></a>

#### FUN-EDAA738364

| 设计项 | 说明 |
|---|---|
| 函数 | `chart_sr_levels` |
| 源码位置 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) · `L151` |
| 签名 | `chart_sr_levels(report: dict[str, Any], timeframe: str='5m')` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`timeframe`（str）：行情时间框架；默认值 `'5m'` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`chart_sr_levels`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `pa.get` → `block.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、pa.get、list、block.get |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_dgt_price_action.py](../../../tests/unit/test_dgt_price_action.py) · 直接动态测试 |

<a id="unit-ce01c0290c"></a>

### UNIT-CE01C0290C

**模块**：`src/analysis/proximity.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CE01C0290C |
| 源码 | [src/analysis/proximity.py](../../../src/analysis/proximity.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/proximity.py` 的职责，通过 `proximity_threshold`、`zone_near_price`、`level_near_price` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_proximity.py](../../../tests/unit/test_proximity.py) |
| 验证状态 | selected |

#### 函数导航

[proximity_threshold](#fun-575ce11369) · [zone_near_price](#fun-914f4d90ea) · [level_near_price](#fun-8793f9d1f1)

<a id="fun-575ce11369"></a>

#### FUN-575CE11369

| 设计项 | 说明 |
|---|---|
| 函数 | `proximity_threshold` |
| 源码位置 | [src/analysis/proximity.py](../../../src/analysis/proximity.py) · `L12` |
| 签名 | `proximity_threshold(price: float, atr: float \| None, *, atr_mult: float=1.0, pct: float=PCT_FALLBACK)` |
| 参数 | `price`（float）：当前或待评估价格<br>`atr`（float \| None）：平均真实波幅<br>`atr_mult`（float）：由 `atr_mult` 表示的数值参数；默认值 `1.0`<br>`pct`（float）：由 `pct` 表示的数值参数；默认值 `PCT_FALLBACK` |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`proximity_threshold`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-914f4d90ea"></a>

#### FUN-914F4D90EA

| 设计项 | 说明 |
|---|---|
| 函数 | `zone_near_price` |
| 源码位置 | [src/analysis/proximity.py](../../../src/analysis/proximity.py) · `L22` |
| 签名 | `zone_near_price(price: float, low: float, high: float, atr: float \| None, *, atr_mult: float=1.0, pct: float=PCT_FALLBACK)` |
| 参数 | `price`（float）：当前或待评估价格<br>`low`（float）：最低价序列或下界<br>`high`（float）：最高价序列或上界<br>`atr`（float \| None）：平均真实波幅<br>`atr_mult`（float）：由 `atr_mult` 表示的数值参数；默认值 `1.0`<br>`pct`（float）：由 `pct` 表示的数值参数；默认值 `PCT_FALLBACK` |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`zone_near_price`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `min` → `max` → `abs` → `proximity_threshold`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | min、max、abs、proximity_threshold |
| 复杂度 / 风险 | 分支 1；跨度 15 行；中 |
| 测试 / 验证 | [tests/unit/test_proximity.py](../../../tests/unit/test_proximity.py) · 直接动态测试 |

<a id="fun-8793f9d1f1"></a>

#### FUN-8793F9D1F1

| 设计项 | 说明 |
|---|---|
| 函数 | `level_near_price` |
| 源码位置 | [src/analysis/proximity.py](../../../src/analysis/proximity.py) · `L39` |
| 签名 | `level_near_price(level: float, price: float, atr: float \| None, *, atr_mult: float=1.0, pct: float=PCT_FALLBACK)` |
| 参数 | `level`（float）：候选价格水平<br>`price`（float）：当前或待评估价格<br>`atr`（float \| None）：平均真实波幅<br>`atr_mult`（float）：由 `atr_mult` 表示的数值参数；默认值 `1.0`<br>`pct`（float）：由 `pct` 表示的数值参数；默认值 `PCT_FALLBACK` |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`level_near_price`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `abs` → `proximity_threshold`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | abs、proximity_threshold |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_proximity.py](../../../tests/unit/test_proximity.py) · 直接动态测试 |

<a id="unit-dad8a91ff9"></a>

### UNIT-DAD8A91FF9

**模块**：`src/analysis/report_engine.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAD8A91FF9 |
| 源码 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/report_engine.py` 的职责，通过 `TradingSignal`、`compute_trading_signals`、`generate_trading_signals`、`trend_projections`、`build_conclusion`、`invalidation_rules`、`parse_risk_events_calendar`、`build_calendar_events` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 44 / 8 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_backtest_simulator.py](../../../tests/unit/test_backtest_simulator.py)、[tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py)、[tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_plan_signals.py](../../../tests/unit/test_plan_signals.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_generate_pa_signals](#fun-3121795202) | 构建`generate_pa_signals`；返回 `list[TradingSignal]` 类型结果。 | 未检测到直接副作用 | — |
| [authorized_position_scale](#fun-b8f52e3dc7) | 计算`authorized_position_scale`；返回 `float` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py) |
| [format_authorized_position_size](#fun-a43ced947f) | 格式化`authorized_position_size`；返回 `str` 类型结果。 | 未检测到直接副作用 | — |
| [_format_trader_veto_lines](#fun-4c3a66bdae) | 格式化`trader_veto_lines`；返回 `list[str]` 类型结果。 | 未检测到直接副作用 | — |
| [apply_manager_authorization](#fun-5d6d01887f) | 应用`manager_authorization`；无返回值（None）。 | 未检测到直接副作用 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) |
| [apply_manager_authorization._attach_rejection](#fun-91b63c3cae) | 执行`attach_rejection`处理；无返回值（None）。 | 未检测到直接副作用 | — |
| [apply_manager_authorization._clear_auth_meta](#fun-6d5b47fa9d) | 执行`clear_auth_meta`处理；无返回值（None）。 | 未检测到直接副作用 | — |
| [_authorized_primary_signal](#fun-358a1e0942) | 构建`authorized_primary_signal`；返回 `dict[str, Any] \| None` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[_compute_risk_reward](#fun-46bd20a480) · [_risk_reward_ratio](#fun-dcc89b25ee) · [_grade](#fun-15ed1e142c) · [_zone_relation](#fun-79027dc513) · [_stop_breached](#fun-4edf24baf8) · [_setup_status_and_score](#fun-216988a705) · [compute_trading_signals](#fun-db79153948) · [_apply_smc_filter_score](#fun-c46ab92251) · [_finalize_pa_plan_meta](#fun-b29ba1665b) · [generate_trading_signals](#fun-7b436508b0) · [_generate_pa_signals](#fun-3121795202) · [trend_projections](#fun-570c5667b7) · [build_conclusion](#fun-e3c1c289a1) · [invalidation_rules](#fun-a5ab9c9398) · [parse_risk_events_calendar](#fun-5fd97aa52d) · [build_calendar_events](#fun-fddea7563f) · [calendar_rows_from_external](#fun-c04ff0655e) · [_build_context_levels](#fun-3196d79811) · [build_key_levels](#fun-6ab88c4476) · [build_resistance_support](#fun-0e716fdbd6) · [_signal_value](#fun-666ae14d42) · [_assign_signal_roles](#fun-5dd9e47b1e) · [build_strategy_plans](#fun-a1e1bc8771) · [authorized_position_scale](#fun-b8f52e3dc7) · [format_authorized_position_size](#fun-a43ced947f) · [_normalize_signal_dict_take_profits](#fun-34dce71c07) · [_review_field](#fun-e8ad3336d7) · [_format_risk_veto_lines](#fun-be4a18b71c) · [_format_trader_veto_lines](#fun-4c3a66bdae) · [_format_level_validation_lines](#fun-15ccc085e1) · [build_signal_rejection_notes](#fun-3539753867) · [build_signal_rejection_reason](#fun-3bf762bd92) · [_signal_to_dict](#fun-442599ada0) · [_assign_signal_ids](#fun-9883fd47f5) · [_signal_execution_ready](#fun-435783f2d2) · [apply_manager_authorization](#fun-5d6d01887f) · [apply_manager_authorization._attach_rejection](#fun-91b63c3cae) · [apply_manager_authorization._clear_auth_meta](#fun-6d5b47fa9d) · [_authorized_primary_signal](#fun-358a1e0942) · [_format_entry_zone](#fun-26766e75ae) · [build_final_decision_meta](#fun-f903e47206) · [align_conclusion_with_manager_decision](#fun-db059d9e58) · [build_path_summary](#fun-cc7188b273) · [build_report](#fun-65d3afa4f8)

<a id="fun-46bd20a480"></a>

#### FUN-46BD20A480

| 设计项 | 说明 |
|---|---|
| 函数 | `_compute_risk_reward` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L78` |
| 签名 | `_compute_risk_reward(*, direction: str, entry_low: float, entry_high: float, stop_loss: float, take_profits: list[float])` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`stop_loss`（float）：止损价格<br>`take_profits`（list[float]）：止盈目标集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 计算风险收益比；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 4；跨度 24 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-dcc89b25ee"></a>

#### FUN-DCC89B25EE

| 设计项 | 说明 |
|---|---|
| 函数 | `_risk_reward_ratio` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L104` |
| 签名 | `_risk_reward_ratio(*, direction: str, entry_low: float, entry_high: float, stop_loss: float, take_profits: list[float])` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`stop_loss`（float）：止损价格<br>`take_profits`（list[float]）：止盈目标集合 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`risk_reward_ratio`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 21 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-15ed1e142c"></a>

#### FUN-15ED1E142C

| 设计项 | 说明 |
|---|---|
| 函数 | `_grade` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L127` |
| 签名 | `_grade(score: float)` |
| 参数 | `score`（float）：评分值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`grade`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-79027dc513"></a>

#### FUN-79027DC513

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_relation` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L137` |
| 签名 | `_zone_relation(*, price: float, direction: str, entry_low: float, entry_high: float)` |
| 参数 | `price`（float）：当前或待评估价格<br>`direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界 |
| 返回 | 返回 `tuple[str, float]` 类型结果 |
| 职责 | 构建`zone_relation`；返回 `tuple[str, float]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 5；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4edf24baf8"></a>

#### FUN-4EDF24BAF8

| 设计项 | 说明 |
|---|---|
| 函数 | `_stop_breached` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L157` |
| 签名 | `_stop_breached(*, price: float, direction: str, stop_loss: float)` |
| 参数 | `price`（float）：当前或待评估价格<br>`direction`（str）：交易方向<br>`stop_loss`（float）：止损价格 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 停止`breached`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-216988a705"></a>

#### FUN-216988A705

| 设计项 | 说明 |
|---|---|
| 函数 | `_setup_status_and_score` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L164` |
| 签名 | `_setup_status_and_score(*, name: str, direction: str, theme: str, setup_type: str, price: float, entry_low: float, entry_high: float, stop_loss: float, take_profits: list[float], sentiment: dict[str, float], trigger_confirmed: bool=False)` |
| 参数 | `name`（str）：对象名称<br>`direction`（str）：交易方向<br>`theme`（str）：由 `theme` 表示的文本或标识<br>`setup_type`（str）：由 `setup_type` 表示的文本或标识<br>`price`（float）：当前或待评估价格<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`stop_loss`（float）：止损价格<br>`take_profits`（list[float]）：止盈目标集合<br>`sentiment`（dict[str, float]）：市场情绪结果<br>`trigger_confirmed`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `tuple[str, bool, str, float, str, list[str]]` 类型结果 |
| 职责 | 评分`setup_status_and`；返回 `tuple[str, bool, str, float, str, list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_zone_relation` → `_risk_reward_ratio` → `_stop_breached` → `sentiment.get` → `min` → `reasons.append` → `round` → `_grade`；包含 18 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, bool, str, float, str, list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _zone_relation、_risk_reward_ratio、_stop_breached、sentiment.get、min、reasons.append、round、_grade |
| 复杂度 / 风险 | 分支 18；跨度 91 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-db79153948"></a>

#### FUN-DB79153948

| 设计项 | 说明 |
|---|---|
| 函数 | `compute_trading_signals` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L257` |
| 签名 | `compute_trading_signals(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `list[TradingSignal]` 类型结果 |
| 职责 | 计算`trading_signals`；返回 `list[TradingSignal]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment_score` → `analyses.get` → `build_price_action_summaries` → `generate_trading_signals`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[TradingSignal]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment_score、analyses.get、build_price_action_summaries、generate_trading_signals |
| 复杂度 / 风险 | 分支 2；跨度 22 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="fun-c46ab92251"></a>

#### FUN-C46AB92251

| 设计项 | 说明 |
|---|---|
| 函数 | `_apply_smc_filter_score` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L281` |
| 签名 | `_apply_smc_filter_score(*, direction: str, entry_low: float, entry_high: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, score: float, reasons: list[str])` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析<br>`score`（float）：评分值<br>`reasons`（list[str]）：由 `reasons` 表示的输入集合 |
| 返回 | 返回 `tuple[float, str, list[str]]` 类型结果 |
| 职责 | 应用`smc_filter_score`；返回 `tuple[float, str, list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `smc_filter_adjustment` → `max` → `min` → `round` → `reasons.extend` → `_grade`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, str, list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | smc_filter_adjustment、max、min、round、reasons.extend、_grade |
| 复杂度 / 风险 | 分支 0；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b29ba1665b"></a>

#### FUN-B29BA1665B

| 设计项 | 说明 |
|---|---|
| 函数 | `_finalize_pa_plan_meta` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L303` |
| 签名 | `_finalize_pa_plan_meta(*, rule_fallback: bool, setup_type: str, zone_label: str, score: float, grade: str, reasons: list[str], short_note: str \| None=None)` |
| 参数 | `rule_fallback`（bool）：控制对应行为是否启用的布尔值<br>`setup_type`（str）：由 `setup_type` 表示的文本或标识<br>`zone_label`（str）：展示或分类标签<br>`score`（float）：评分值<br>`grade`（str）：由 `grade` 表示的文本或标识<br>`reasons`（list[str]）：由 `reasons` 表示的输入集合<br>`short_note`（str \| None）：由调用方提供的 `short_note` 输入对象；默认值 `None` |
| 返回 | 返回 `tuple[str, str, float, str, list[str]]` 类型结果 |
| 职责 | 构建`finalize_pa_plan_meta`；返回 `tuple[str, str, float, str, list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `round` → `_grade`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str, float, str, list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、round、_grade |
| 复杂度 / 风险 | 分支 2；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7b436508b0"></a>

#### FUN-7B436508B0

| 设计项 | 说明 |
|---|---|
| 函数 | `generate_trading_signals` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L325` |
| 签名 | `generate_trading_signals(price: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, swing_high: float, swing_low: float, sentiment: dict[str, float], *, price_action: dict[str, Any] \| None=None, metrics: dict[str, Any] \| None=None)` |
| 参数 | `price`（float）：当前或待评估价格<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`sentiment`（dict[str, float]）：市场情绪结果<br>`price_action`（dict[str, Any] \| None）：价格行为分析结果；默认值 `None`<br>`metrics`（dict[str, Any] \| None）：由 `metrics` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `list[TradingSignal]` 类型结果 |
| 职责 | 构建`generate_trading_signals`；返回 `list[TradingSignal]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pa_usable` → `_generate_pa_signals` → `build_rule_pa_block`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[TradingSignal]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pa_usable、_generate_pa_signals、build_rule_pa_block |
| 复杂度 / 风险 | 分支 2；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_plan_signals.py](../../../tests/unit/test_plan_signals.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="fun-3121795202"></a>

#### FUN-3121795202

| 设计项 | 说明 |
|---|---|
| 函数 | `_generate_pa_signals` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L371` |
| 签名 | `_generate_pa_signals(price: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, swing_high: float, swing_low: float, sentiment: dict[str, float], *, price_action: dict[str, Any], rule_fallback: bool=False)` |
| 参数 | `price`（float）：当前或待评估价格<br>`analysis_5m`（TimeframeAnalysis）：5 分钟周期分析<br>`analysis_15m`（TimeframeAnalysis）：15 分钟周期分析<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`sentiment`（dict[str, float]）：市场情绪结果<br>`price_action`（dict[str, Any]）：价格行为分析结果<br>`rule_fallback`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `list[TradingSignal]` 类型结果 |
| 职责 | 构建`generate_pa_signals`；返回 `list[TradingSignal]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment.get` → `price_action.get` → `build_pa_short_aggressive` → `_compute_risk_reward` → `_setup_status_and_score` → `_apply_smc_filter_score` → `_finalize_pa_plan_meta` → `signals.append`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[TradingSignal]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、sentiment.get、price_action.get、build_pa_short_aggressive、_compute_risk_reward、_setup_status_and_score、_apply_smc_filter_score、_finalize_pa_plan_meta、signals.append、TradingSignal、build_pa_short_conservative、max、build_pa_long_sweep、reasons.extend、min、round、_grade、reasons.append |
| 复杂度 / 风险 | 分支 8；跨度 237 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-570c5667b7"></a>

#### FUN-570C5667B7

| 设计项 | 说明 |
|---|---|
| 函数 | `trend_projections` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L610` |
| 签名 | `trend_projections(price: float, swing_high: float, swing_low: float, sentiment: dict[str, float])` |
| 参数 | `price`（float）：当前或待评估价格<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`sentiment`（dict[str, float]）：市场情绪结果 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`trend_projections`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `sentiment.get` → `round`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、sentiment.get、round |
| 复杂度 / 风险 | 分支 3；跨度 118 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py) · 直接动态测试 |

<a id="fun-e3c1c289a1"></a>

#### FUN-E3C1C289A1

| 设计项 | 说明 |
|---|---|
| 函数 | `build_conclusion` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L730` |
| 签名 | `build_conclusion(sentiment: dict[str, float], primary_trend: str, signals: list[TradingSignal])` |
| 参数 | `sentiment`（dict[str, float]）：市场情绪结果<br>`primary_trend`（str）：由 `primary_trend` 表示的文本或标识<br>`signals`（list[TradingSignal]）：交易信号集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`conclusion`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment.get` → `max` → `next`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment.get、max、next |
| 复杂度 / 风险 | 分支 11；跨度 73 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py) · 直接动态测试 |

<a id="fun-a5ab9c9398"></a>

#### FUN-A5AB9C9398

| 设计项 | 说明 |
|---|---|
| 函数 | `invalidation_rules` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L805` |
| 签名 | `invalidation_rules(analysis_15m: TimeframeAnalysis, swing_high: float, signals: list[TradingSignal])` |
| 参数 | `analysis_15m`（TimeframeAnalysis）：15 分钟周期分析<br>`swing_high`（float）：摆动高点价格<br>`signals`（list[TradingSignal]）：交易信号集合 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`invalidation_rules`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `round` → `rules.insert`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、round、rules.insert |
| 复杂度 / 风险 | 分支 5；跨度 22 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5fd97aa52d"></a>

#### FUN-5FD97AA52D

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_risk_events_calendar` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L829` |
| 签名 | `parse_risk_events_calendar(risk_events: str)` |
| 参数 | `risk_events`（str）：事件集合 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 解析`risk_events_calendar`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `risk_events.split` → `part.strip` → `_CAL_EVENT_RE.match` → `strip` → `m.group` → `body.lower` → `startswith` → `body.upper`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | risk_events.split、part.strip、_CAL_EVENT_RE.match、strip、m.group、body.lower、startswith、body.upper、events.append |
| 复杂度 / 风险 | 分支 5；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fddea7563f"></a>

#### FUN-FDDEA7563F

| 设计项 | 说明 |
|---|---|
| 函数 | `build_calendar_events` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L854` |
| 签名 | `build_calendar_events()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 构建`calendar_events`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py) · 直接动态测试 |

<a id="fun-c04ff0655e"></a>

#### FUN-C04FF0655E

| 设计项 | 说明 |
|---|---|
| 函数 | `calendar_rows_from_external` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L864` |
| 签名 | `calendar_rows_from_external(*, calendar_events: list[Any] \| None=None, risk_events: str='—')` |
| 参数 | `calendar_events`（list[Any] \| None）：事件集合；默认值 `None`<br>`risk_events`（str）：事件集合；默认值 `'—'` |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 根据外部数据快照构建`calendar_rows`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `hasattr` → `getattr` → `isinstance` → `event.get` → `body.strip` → `region.lower` → `body.lower` → `startswith`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | hasattr、str、getattr、isinstance、event.get、body.strip、region.lower、body.lower、startswith、body.upper、rows.append、parse_risk_events_calendar |
| 复杂度 / 风险 | 分支 7；跨度 33 行；中 |
| 测试 / 验证 | [tests/unit/test_calendar_empty.py](../../../tests/unit/test_calendar_empty.py) · 直接动态测试 |

<a id="fun-3196d79811"></a>

#### FUN-3196D79811

| 设计项 | 说明 |
|---|---|
| 函数 | `_build_context_levels` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L899` |
| 签名 | `_build_context_levels(price: float, swing_high: float, swing_low: float, swing_tf: str, swing_atr: float \| None)` |
| 参数 | `price`（float）：当前或待评估价格<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`swing_tf`（str）：时间框架简称<br>`swing_atr`（float \| None）：平均真实波幅 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`context_levels`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `swing_tf.upper` → `level_near_price` → `levels.append` → `round`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | swing_tf.upper、level_near_price、levels.append、round |
| 复杂度 / 风险 | 分支 2；跨度 33 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6ab88c4476"></a>

#### FUN-6AB88C4476

| 设计项 | 说明 |
|---|---|
| 函数 | `build_key_levels` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L934` |
| 签名 | `build_key_levels(price: float, metrics: dict, swing_high: float, swing_low: float, fib: list[dict], signals: list[TradingSignal], *, swing_tf: str='4h', swing_atr: float \| None=None)` |
| 参数 | `price`（float）：当前或待评估价格<br>`metrics`（dict）：由 `metrics` 表示的键值映射<br>`swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格<br>`fib`（list[dict]）：由 `fib` 表示的输入集合<br>`signals`（list[TradingSignal]）：交易信号集合<br>`swing_tf`（str）：时间框架简称；默认值 `'4h'`<br>`swing_atr`（float \| None）：平均真实波幅；默认值 `None` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建关键价格水平；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `metrics.get` → `levels.append` → `zone_near_price` → `swing_tf.upper` → `sorted` → `x.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | metrics.get、levels.append、len、zone_near_price、swing_tf.upper、sorted、x.get |
| 复杂度 / 风险 | 分支 4；跨度 43 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0e716fdbd6"></a>

#### FUN-0E716FDBD6

| 设计项 | 说明 |
|---|---|
| 函数 | `build_resistance_support` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L979` |
| 签名 | `build_resistance_support(key_levels: list[dict], liquidity: list[dict])` |
| 参数 | `key_levels`（list[dict]）：候选价格水平集合<br>`liquidity`（list[dict]）：由 `liquidity` 表示的输入集合 |
| 返回 | 返回 `tuple[list[str], list[str]]` 类型结果 |
| 职责 | 构建`resistance_support`；返回 `tuple[list[str], list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lv.get` → `resist.append` → `support.append` → `item.get`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[str], list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lv.get、resist.append、support.append、item.get |
| 复杂度 / 风险 | 分支 6；跨度 25 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-666ae14d42"></a>

#### FUN-666AE14D42

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_value` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1006` |
| 签名 | `_signal_value(signal: TradingSignal \| dict[str, Any], key: str, default: Any=None)` |
| 参数 | `signal`（TradingSignal \| dict[str, Any]）：当前交易信号<br>`key`（str）：索引键<br>`default`（Any）：由调用方提供的 `default` 输入对象；默认值 `None` |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成信号数值结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `signal.get` → `getattr`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、signal.get、getattr |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5dd9e47b1e"></a>

#### FUN-5DD9E47B1E

| 设计项 | 说明 |
|---|---|
| 函数 | `_assign_signal_roles` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1012` |
| 签名 | `_assign_signal_roles(signals: list[TradingSignal], sentiment: dict[str, float])` |
| 参数 | `signals`（list[TradingSignal]）：交易信号集合<br>`sentiment`（dict[str, float]）：市场情绪结果 |
| 返回 | 无返回值（None） |
| 职责 | 执行`assign_signal_roles`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment.get |
| 复杂度 / 风险 | 分支 3；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a1e1bc8771"></a>

#### FUN-A1E1BC8771

| 设计项 | 说明 |
|---|---|
| 函数 | `build_strategy_plans` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1024` |
| 签名 | `build_strategy_plans(signals: list[TradingSignal \| dict[str, Any]])` |
| 参数 | `signals`（list[TradingSignal \| dict[str, Any]]）：交易信号集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`strategy_plans`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_signal_value` → `enumerate` → `plans.append` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _signal_value、enumerate、plans.append、len、join、str |
| 复杂度 / 风险 | 分支 2；跨度 16 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py) · 直接动态测试 |

<a id="fun-b8f52e3dc7"></a>

#### FUN-B8F52E3DC7

| 设计项 | 说明 |
|---|---|
| 函数 | `authorized_position_scale` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1042` |
| 签名 | `authorized_position_scale(reviews: list, decision)` |
| 参数 | `reviews`（list）：风险或评审结果集合<br>`decision`（实现约定类型）：最终或阶段决策 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`authorized_position_scale`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `selected.intersection` → `min`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、float、set、selected.intersection、min |
| 复杂度 / 风险 | 分支 3；跨度 13 行；高 |
| 测试 / 验证 | [tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py) · 直接动态测试 |

<a id="fun-a43ced947f"></a>

#### FUN-A43CED947F

| 设计项 | 说明 |
|---|---|
| 函数 | `format_authorized_position_size` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1057` |
| 签名 | `format_authorized_position_size(scale: float, action: str)` |
| 参数 | `scale`（float）：由 `scale` 表示的数值参数<br>`action`（str）：由 `action` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`authorized_position_size`；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 4；跨度 11 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-34dce71c07"></a>

#### FUN-34DCE71C07

| 设计项 | 说明 |
|---|---|
| 函数 | `_normalize_signal_dict_take_profits` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1070` |
| 签名 | `_normalize_signal_dict_take_profits(sig: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 无返回值（None） |
| 职责 | 标准化`signal_dict_take_profits`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get` → `normalize_signal_take_profits`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get、normalize_signal_take_profits |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e8ad3336d7"></a>

#### FUN-E8AD3336D7

| 设计项 | 说明 |
|---|---|
| 函数 | `_review_field` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1086` |
| 签名 | `_review_field(review: object, name: str, default: object=None)` |
| 参数 | `review`（object）：由调用方提供的 `review` 输入对象<br>`name`（str）：对象名称<br>`default`（object）：由调用方提供的 `default` 输入对象；默认值 `None` |
| 返回 | 返回 `object` 类型结果 |
| 职责 | 生成`review_field`结果；返回 `object` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `review.get` → `getattr`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `object` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、review.get、getattr |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-be4a18b71c"></a>

#### FUN-BE4A18B71C

| 设计项 | 说明 |
|---|---|
| 函数 | `_format_risk_veto_lines` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1092` |
| 签名 | `_format_risk_veto_lines(risk_reviews: list \| None, *, candidate_index: int \| None)` |
| 参数 | `risk_reviews`（list \| None）：风险评审集合<br>`candidate_index`（int \| None）：由调用方提供的 `candidate_index` 输入对象 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 格式化`risk_veto_lines`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_review_field` → `_RISK_PROFILE_CN.get` → `strip` → `join` → `lines.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、_review_field、_RISK_PROFILE_CN.get、bool、list、strip、float、join、lines.append |
| 复杂度 / 风险 | 分支 7；跨度 32 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4c3a66bdae"></a>

#### FUN-4C3A66BDAE

| 设计项 | 说明 |
|---|---|
| 函数 | `_format_trader_veto_lines` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1126` |
| 签名 | `_format_trader_veto_lines(proposal: object \| None, *, candidate_index: int \| None)` |
| 参数 | `proposal`（object \| None）：候选交易方案<br>`candidate_index`（int \| None）：由调用方提供的 `candidate_index` 输入对象 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 格式化`trader_veto_lines`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `proposal.get` → `getattr` → `lines.append` → `strip` → `join`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、list、proposal.get、str、getattr、lines.append、strip、join |
| 复杂度 / 风险 | 分支 5；跨度 26 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-15ccc085e1"></a>

#### FUN-15CCC085E1

| 设计项 | 说明 |
|---|---|
| 函数 | `_format_level_validation_lines` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1154` |
| 签名 | `_format_level_validation_lines(validated_plans: list[dict[str, Any]] \| None, sig: dict[str, Any])` |
| 参数 | `validated_plans`（list[dict[str, Any]] \| None）：已通过校验的交易计划集合<br>`sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 格式化`level_validation_lines`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get` → `row.get` → `upper` → `prop.get` → `strip` → `abs` → `lines.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、sig.get、row.get、upper、prop.get、strip、bool、abs、float、lines.append |
| 复杂度 / 风险 | 分支 7；跨度 26 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3539753867"></a>

#### FUN-3539753867

| 设计项 | 说明 |
|---|---|
| 函数 | `build_signal_rejection_notes` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1182` |
| 签名 | `build_signal_rejection_notes(sig: dict[str, Any], *, decision_action: str, observation_mode: bool=False, primary_name: str \| None=None, primary_sig: dict[str, Any] \| None=None, decision_summary: str='', decision_confidence: float \| None=None, risk_reviews: list \| None=None, candidate_index: int \| None=None, proposal: object \| None=None, validated_plans: list[dict[str, Any]] \| None=None)` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号<br>`decision_action`（str）：由 `decision_action` 表示的文本或标识<br>`observation_mode`（bool）：观察模式开关或策略；默认值 `False`<br>`primary_name`（str \| None）：对象名称；默认值 `None`<br>`primary_sig`（dict[str, Any] \| None）：待评估交易信号；默认值 `None`<br>`decision_summary`（str）：摘要内容；默认值 `''`<br>`decision_confidence`（float \| None）：由调用方提供的 `decision_confidence` 输入对象；默认值 `None`<br>`risk_reviews`（list \| None）：风险评审集合；默认值 `None`<br>`candidate_index`（int \| None）：由调用方提供的 `candidate_index` 输入对象；默认值 `None`<br>`proposal`（object \| None）：候选交易方案；默认值 `None`<br>`validated_plans`（list[dict[str, Any]] \| None）：已通过校验的交易计划集合；默认值 `None` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`signal_rejection_notes`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parts.append` → `strip` → `parts.extend` → `_format_risk_veto_lines` → `_format_trader_veto_lines` → `_format_level_validation_lines` → `sig.get` → `primary_sig.get`；包含 18 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | parts.append、str、strip、float、parts.extend、_format_risk_veto_lines、_format_trader_veto_lines、_format_level_validation_lines、sig.get、primary_sig.get、upper、set、seen.add、ordered.append |
| 复杂度 / 风险 | 分支 18；跨度 80 行；中 |
| 测试 / 验证 | [tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py) · 直接动态测试 |

<a id="fun-3bf762bd92"></a>

#### FUN-3BF762BD92

| 设计项 | 说明 |
|---|---|
| 函数 | `build_signal_rejection_reason` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1264` |
| 签名 | `build_signal_rejection_reason(sig: dict[str, Any], *, decision_action: str, observation_mode: bool=False, primary_name: str \| None=None, primary_sig: dict[str, Any] \| None=None, decision_summary: str='', decision_confidence: float \| None=None, risk_reviews: list \| None=None, candidate_index: int \| None=None, proposal: object \| None=None, validated_plans: list[dict[str, Any]] \| None=None)` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号<br>`decision_action`（str）：由 `decision_action` 表示的文本或标识<br>`observation_mode`（bool）：观察模式开关或策略；默认值 `False`<br>`primary_name`（str \| None）：对象名称；默认值 `None`<br>`primary_sig`（dict[str, Any] \| None）：待评估交易信号；默认值 `None`<br>`decision_summary`（str）：摘要内容；默认值 `''`<br>`decision_confidence`（float \| None）：由调用方提供的 `decision_confidence` 输入对象；默认值 `None`<br>`risk_reviews`（list \| None）：风险评审集合；默认值 `None`<br>`candidate_index`（int \| None）：由调用方提供的 `candidate_index` 输入对象；默认值 `None`<br>`proposal`（object \| None）：候选交易方案；默认值 `None`<br>`validated_plans`（list[dict[str, Any]] \| None）：已通过校验的交易计划集合；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 构建`signal_rejection_reason`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_signal_rejection_notes` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_signal_rejection_notes、join |
| 复杂度 / 风险 | 分支 1；跨度 29 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-442599ada0"></a>

#### FUN-442599ADA0

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_to_dict` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1295` |
| 签名 | `_signal_to_dict(signal: TradingSignal)` |
| 参数 | `signal`（TradingSignal）：当前交易信号 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`signal_to_dict`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict` → `_normalize_signal_dict_take_profits` → `stable_signal_id`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict、_normalize_signal_dict_take_profits、stable_signal_id |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9883fd47f5"></a>

#### FUN-9883FD47F5

| 设计项 | 说明 |
|---|---|
| 函数 | `_assign_signal_ids` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1302` |
| 签名 | `_assign_signal_ids(sig_dicts: list[dict[str, Any]])` |
| 参数 | `sig_dicts`（list[dict[str, Any]]）：由 `sig_dicts` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 执行`assign_signal_ids`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get` → `stable_signal_id`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get、stable_signal_id |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-435783f2d2"></a>

#### FUN-435783F2D2

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_execution_ready` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1307` |
| 签名 | `_signal_execution_ready(sig: dict[str, Any] \| None)` |
| 参数 | `sig`（dict[str, Any] \| None）：待评估交易信号 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`signal_execution_ready`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get、bool |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5d6d01887f"></a>

#### FUN-5D6D01887F

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_manager_authorization` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1316` |
| 签名 | `apply_manager_authorization(report: dict, decision, risk_reviews: list, *, proposal: object \| None=None)` |
| 参数 | `report`（dict）：分析报告<br>`decision`（实现约定类型）：最终或阶段决策<br>`risk_reviews`（list）：风险评审集合<br>`proposal`（object \| None）：候选交易方案；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 应用`manager_authorization`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `_assign_signal_ids` → `report.setdefault` → `meta.get` → `getattr` → `strip` → `ManagerDecision` → `authorized_position_scale`；包含 21 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、report.get、_assign_signal_ids、report.setdefault、meta.get、str、getattr、strip、ManagerDecision、set、authorized_position_scale、build_signal_rejection_notes、bool、join、decision.to_dict、hasattr、dict、enumerate、_normalize_signal_dict_take_profits、_attach_rejection |
| 复杂度 / 风险 | 分支 21；跨度 162 行；高 |
| 测试 / 验证 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../../tests/unit/test_rule_chain_stability.py) · 直接动态测试 |

<a id="fun-91b63c3cae"></a>

#### FUN-91B63C3CAE

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_manager_authorization._attach_rejection` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1353` |
| 签名 | `apply_manager_authorization._attach_rejection(sig: dict[str, Any], *, idx: int, primary_name: str \| None=None, primary_sig: dict \| None=None)` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号<br>`idx`（int）：由 `idx` 表示的数值参数<br>`primary_name`（str \| None）：对象名称；默认值 `None`<br>`primary_sig`（dict \| None）：待评估交易信号；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`attach_rejection`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `build_signal_rejection_notes` → `meta.get` → `getattr` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_signal_rejection_notes、bool、meta.get、str、getattr、join |
| 复杂度 / 风险 | 分支 1；跨度 22 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6d5b47fa9d"></a>

#### FUN-6D5B47FA9D

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_manager_authorization._clear_auth_meta` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1376` |
| 签名 | `apply_manager_authorization._clear_auth_meta(*, plan_authorized: bool=False)` |
| 参数 | `plan_authorized`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 无返回值（None） |
| 职责 | 执行`clear_auth_meta`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `decision.to_dict` → `hasattr`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | decision.to_dict、hasattr、dict |
| 复杂度 / 风险 | 分支 1；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-358a1e0942"></a>

#### FUN-358A1E0942

| 设计项 | 说明 |
|---|---|
| 函数 | `_authorized_primary_signal` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1488` |
| 签名 | `_authorized_primary_signal(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 构建`authorized_primary_signal`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `next` → `report.get` → `s.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | next、report.get、s.get |
| 复杂度 / 风险 | 分支 0；跨度 5 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-26766e75ae"></a>

#### FUN-26766E75AE

| 设计项 | 说明 |
|---|---|
| 函数 | `_format_entry_zone` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1495` |
| 签名 | `_format_entry_zone(signal: dict[str, Any])` |
| 参数 | `signal`（dict[str, Any]）：当前交易信号 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`entry_zone`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `signal.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | signal.get、float |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f903e47206"></a>

#### FUN-F903E47206

| 设计项 | 说明 |
|---|---|
| 函数 | `build_final_decision_meta` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1502` |
| 签名 | `build_final_decision_meta(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`final_decision_meta`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `lower` → `decision.get` → `strip` → `_authorized_primary_signal` → `_MANAGER_ACTION_CN.get` → `get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、lower、str、decision.get、bool、strip、_authorized_primary_signal、_MANAGER_ACTION_CN.get、get、primary.get、_format_entry_zone |
| 复杂度 / 风险 | 分支 5；跨度 47 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-db059d9e58"></a>

#### FUN-DB059D9E58

| 设计项 | 说明 |
|---|---|
| 函数 | `align_conclusion_with_manager_decision` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1551` |
| 签名 | `align_conclusion_with_manager_decision(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 执行`align_conclusion_with_manager_decision`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.setdefault` → `meta.get` → `lower` → `decision.get` → `strip` → `build_final_decision_meta` → `get` → `_MANAGER_ACTION_CN.get`；包含 14 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.setdefault、meta.get、lower、str、decision.get、bool、strip、build_final_decision_meta、get、_MANAGER_ACTION_CN.get、_authorized_primary_signal、primary.get、_format_entry_zone、conclusion.get |
| 复杂度 / 风险 | 分支 14；跨度 75 行；中 |
| 测试 / 验证 | [tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_manager_authorization.py](../../../tests/unit/test_manager_authorization.py) · 直接动态测试 |

<a id="fun-cc7188b273"></a>

#### FUN-CC7188B273

| 设计项 | 说明 |
|---|---|
| 函数 | `build_path_summary` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1628` |
| 签名 | `build_path_summary(projections: list[dict])` |
| 参数 | `projections`（list[dict]）：由 `projections` 表示的输入集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`path_summary`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `enumerate` → `p.get` → `join` → `out.append`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | enumerate、p.get、join、out.append |
| 复杂度 / 风险 | 分支 1；跨度 14 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-65d3afa4f8"></a>

#### FUN-65D3AFA4F8

| 设计项 | 说明 |
|---|---|
| 函数 | `build_report` |
| 源码位置 | [src/analysis/report_engine.py](../../../src/analysis/report_engine.py) · `L1644` |
| 签名 | `build_report(data: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], *, signals: list[TradingSignal] \| None=None)` |
| 参数 | `data`（dict[str, pd.DataFrame]）：输入数据<br>`analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果<br>`signals`（list[TradingSignal] \| None）：交易信号集合；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建报告；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `daily_metrics` → `sentiment_score` → `analyses.get` → `fibonacci_levels` → `build_price_action_summaries` → `generate_trading_signals` → `_assign_signal_roles` → `build_conclusion`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | daily_metrics、sentiment_score、analyses.get、fibonacci_levels、build_price_action_summaries、generate_trading_signals、_assign_signal_roles、build_conclusion、build_tf_summaries、build_liquidity_entries、_build_context_levels、max、trend_projections、build_path_summary、build_key_levels、build_resistance_support、log.info、len、sentiment.get、indicator_snapshot |
| 复杂度 / 风险 | 分支 11；跨度 139 行；中 |
| 测试 / 验证 | [tests/unit/test_evidence_provenance.py](../../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="unit-cd6da8c4a3"></a>

### UNIT-CD6DA8C4A3

**模块**：`src/analysis/report_facts.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CD6DA8C4A3 |
| 源码 | [src/analysis/report_facts.py](../../../src/analysis/report_facts.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/report_facts.py` 的职责，通过 `build_tf_summaries`、`build_liquidity_entries` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py) |
| 验证状态 | selected |

#### 函数导航

[build_tf_summaries](#fun-7f2a7da4e4) · [_strong_weak_context_entries](#fun-6ed8e3091f) · [build_liquidity_entries](#fun-c657924e3f)

<a id="fun-7f2a7da4e4"></a>

#### FUN-7F2A7DA4E4

| 设计项 | 说明 |
|---|---|
| 函数 | `build_tf_summaries` |
| 源码位置 | [src/analysis/report_facts.py](../../../src/analysis/report_facts.py) · `L19` |
| 签名 | `build_tf_summaries(data: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], *, price: float)` |
| 参数 | `data`（dict[str, pd.DataFrame]）：输入数据<br>`analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果<br>`price`（float）：当前或待评估价格 |
| 返回 | 返回 `dict[str, dict[str, Any]]` 类型结果 |
| 职责 | 构建`tf_summaries`；返回 `dict[str, dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_tf_snapshot` → `ema_relation`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_tf_snapshot、ema_relation |
| 复杂度 / 风险 | 分支 2；跨度 16 行；中 |
| 测试 / 验证 | [tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py) · 直接动态测试 |

<a id="fun-6ed8e3091f"></a>

#### FUN-6ED8E3091F

| 设计项 | 说明 |
|---|---|
| 函数 | `_strong_weak_context_entries` |
| 源码位置 | [src/analysis/report_facts.py](../../../src/analysis/report_facts.py) · `L37` |
| 签名 | `_strong_weak_context_entries(analysis: TimeframeAnalysis, *, price: float, swing_atr: float \| None)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`price`（float）：当前或待评估价格<br>`swing_atr`（float \| None）：平均真实波幅 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`strong_weak_context_entries`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_tf_snapshot` → `panel.get` → `level_near_price` → `entries.append` → `round`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_tf_snapshot、panel.get、level_near_price、float、entries.append、round |
| 复杂度 / 风险 | 分支 3；跨度 29 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c657924e3f"></a>

#### FUN-C657924E3F

| 设计项 | 说明 |
|---|---|
| 函数 | `build_liquidity_entries` |
| 源码位置 | [src/analysis/report_facts.py](../../../src/analysis/report_facts.py) · `L68` |
| 签名 | `build_liquidity_entries(analyses: dict[str, TimeframeAnalysis], *, price: float, swing_tf: str, swing_atr: float \| None)` |
| 参数 | `analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果<br>`price`（float）：当前或待评估价格<br>`swing_tf`（str）：时间框架简称<br>`swing_atr`（float \| None）：平均真实波幅 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`liquidity_entries`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `analyses.get` → `round` → `seen.add` → `entries.append` → `liquidity_label` → `entries.extend` → `_strong_weak_context_entries` → `entries.sort`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、analyses.get、round、float、seen.add、entries.append、liquidity_label、entries.extend、_strong_weak_context_entries、entries.sort、abs |
| 复杂度 / 风险 | 分支 7；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py) · 直接动态测试 |

<a id="unit-1aecfa1072"></a>

### UNIT-1AECFA1072

**模块**：`src/analysis/report_invariant_gate.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1AECFA1072 |
| 源码 | [src/analysis/report_invariant_gate.py](../../../src/analysis/report_invariant_gate.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/report_invariant_gate.py` 的职责，通过 `apply_report_invariant_gate` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 4 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [apply_report_invariant_gate](#fun-2e93cd50fc) | 应用`report_invariant_gate`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py) |

#### 函数导航

[_revoke_execution](#fun-bf2c9119ea) · [_sanitize_llm_fields](#fun-b1bed5ecad) · [_sanitize_conclusion](#fun-0d8ba6c403) · [apply_report_invariant_gate](#fun-2e93cd50fc)

<a id="fun-bf2c9119ea"></a>

#### FUN-BF2C9119EA

| 设计项 | 说明 |
|---|---|
| 函数 | `_revoke_execution` |
| 源码位置 | [src/analysis/report_invariant_gate.py](../../../src/analysis/report_invariant_gate.py) · `L24` |
| 签名 | `_revoke_execution(report: dict[str, Any], remediations: list[str])` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`remediations`（list[str]）：由 `remediations` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 执行`revoke_execution`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.setdefault` → `report.get` → `remediations.append`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.setdefault、report.get、remediations.append |
| 复杂度 / 风险 | 分支 1；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b1bed5ecad"></a>

#### FUN-B1BED5ECAD

| 设计项 | 说明 |
|---|---|
| 函数 | `_sanitize_llm_fields` |
| 源码位置 | [src/analysis/report_invariant_gate.py](../../../src/analysis/report_invariant_gate.py) · `L42` |
| 签名 | `_sanitize_llm_fields(report: dict[str, Any], violations: list[dict[str, str]], remediations: list[str])` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`violations`（list[dict[str, str]]）：由 `violations` 表示的输入集合<br>`remediations`（list[str]）：由 `remediations` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 执行`sanitize_llm_fields`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.setdefault` → `row.get` → `code.startswith` → `strip` → `llm.get` → `remediations.append` → `_executable_wording_on_wait`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.setdefault、str、row.get、code.startswith、strip、llm.get、remediations.append、_executable_wording_on_wait |
| 复杂度 / 风险 | 分支 5；跨度 15 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0d8ba6c403"></a>

#### FUN-0D8BA6C403

| 设计项 | 说明 |
|---|---|
| 函数 | `_sanitize_conclusion` |
| 源码位置 | [src/analysis/report_invariant_gate.py](../../../src/analysis/report_invariant_gate.py) · `L59` |
| 签名 | `_sanitize_conclusion(report: dict[str, Any], remediations: list[str])` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`remediations`（list[str]）：由 `remediations` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 执行`sanitize_conclusion`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.setdefault` → `conclusion.get` → `_executable_wording_on_wait` → `remediations.append` → `get` → `report.get` → `conclusion.pop`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.setdefault、str、conclusion.get、_executable_wording_on_wait、remediations.append、get、report.get、conclusion.pop |
| 复杂度 / 风险 | 分支 2；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2e93cd50fc"></a>

#### FUN-2E93CD50FC

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_report_invariant_gate` |
| 源码位置 | [src/analysis/report_invariant_gate.py](../../../src/analysis/report_invariant_gate.py) · `L71` |
| 签名 | `apply_report_invariant_gate(report: dict[str, Any], invariants: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`invariants`（dict[str, Any]）：由 `invariants` 表示的键值映射 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 应用`report_invariant_gate`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.setdefault` → `invariants.get` → `v.get` → `meta.setdefault` → `_revoke_execution` → `_sanitize_llm_fields` → `_sanitize_conclusion` → `align_conclusion_with_manager_decision`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.setdefault、list、invariants.get、str、v.get、meta.setdefault、_revoke_execution、_sanitize_llm_fields、_sanitize_conclusion、align_conclusion_with_manager_decision、build_final_decision_meta、sorted |
| 复杂度 / 风险 | 分支 2；跨度 34 行；高 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py) · 直接动态测试 |

<a id="unit-70bd327d9d"></a>

### UNIT-70BD327D9D

**模块**：`src/analysis/report_invariants.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-70BD327D9D |
| 源码 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/report_invariants.py` 的职责，通过 `validate_report_invariants` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 13 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_plan_signal_targets.py](../../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_authorized_signals_for_geometry](#fun-574f6bf2c5) | 构建`authorized_signals_for_geometry`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [_check_authorization_narrative](#fun-070be1843c) | 检查`authorization_narrative`；返回 `list[dict[str, str]]` 类型结果。 | 未检测到直接副作用 | — |
| [validate_report_invariants](#fun-8b2af809d8) | 验证报告不变量；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_plan_signal_targets.py](../../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) |

#### 函数导航

[_violation](#fun-c9004b2dc1) · [_manager_wait](#fun-39a8495c0f) · [_observation_mode](#fun-f9403871be) · [_normalize_direction](#fun-6461023713) · [_authorized_signals_for_geometry](#fun-574f6bf2c5) · [_check_signal_geometry](#fun-eb10a8bba7) · [_llm_top_level_active](#fun-202a49097f) · [_check_authorization_narrative](#fun-070be1843c) · [_check_manager_alignment](#fun-f9e30a657b) · [_check_fact_prices](#fun-5a7430694e) · [_check_freshness_language](#fun-26dad09727) · [_check_audit_metadata](#fun-cb762c7ebb) · [validate_report_invariants](#fun-8b2af809d8)

<a id="fun-c9004b2dc1"></a>

#### FUN-C9004B2DC1

| 设计项 | 说明 |
|---|---|
| 函数 | `_violation` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L19` |
| 签名 | `_violation(code: str, field: str, message: str)` |
| 参数 | `code`（str）：由 `code` 表示的文本或标识<br>`field`（str）：由 `field` 表示的文本或标识<br>`message`（str）：由 `message` 表示的文本或标识 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`violation`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-39a8495c0f"></a>

#### FUN-39A8495C0F

| 设计项 | 说明 |
|---|---|
| 函数 | `_manager_wait` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L23` |
| 签名 | `_manager_wait(meta: dict[str, Any])` |
| 参数 | `meta`（dict[str, Any]）：审计或处理元数据 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`manager_wait`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `decision.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | meta.get、str、decision.get |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f9403871be"></a>

#### FUN-F9403871BE

| 设计项 | 说明 |
|---|---|
| 函数 | `_observation_mode` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L31` |
| 签名 | `_observation_mode(meta: dict[str, Any])` |
| 参数 | `meta`（dict[str, Any]）：审计或处理元数据 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`observation_mode`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、meta.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6461023713"></a>

#### FUN-6461023713

| 设计项 | 说明 |
|---|---|
| 函数 | `_normalize_direction` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L35` |
| 签名 | `_normalize_direction(raw: str)` |
| 参数 | `raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 标准化`direction`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `upper`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、upper |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-574f6bf2c5"></a>

#### FUN-574F6BF2C5

| 设计项 | 说明 |
|---|---|
| 函数 | `_authorized_signals_for_geometry` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L44` |
| 签名 | `_authorized_signals_for_geometry(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`authorized_signals_for_geometry`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `s.get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、report.get、str、meta.get、s.get |
| 复杂度 / 风险 | 分支 5；跨度 22 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-eb10a8bba7"></a>

#### FUN-EB10A8BBA7

| 设计项 | 说明 |
|---|---|
| 函数 | `_check_signal_geometry` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L68` |
| 签名 | `_check_signal_geometry(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 检查交易信号价格几何；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `enumerate` → `_authorized_signals_for_geometry` → `sig.get` → `_normalize_direction` → `LevelProposal` → `out.append`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、get、report.get、enumerate、_authorized_signals_for_geometry、str、sig.get、_normalize_direction、LevelProposal、out.append、_violation、_geometry_error、_tp_ladder_error |
| 复杂度 / 风险 | 分支 5；跨度 28 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-202a49097f"></a>

#### FUN-202A49097F

| 设计项 | 说明 |
|---|---|
| 函数 | `_llm_top_level_active` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L98` |
| 签名 | `_llm_top_level_active(llm: dict[str, Any])` |
| 参数 | `llm`（dict[str, Any]）：由 `llm` 表示的键值映射 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_top_level_active`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `llm.get` → `any` → `strip`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、llm.get、any、strip、str |
| 复杂度 / 风险 | 分支 1；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-070be1843c"></a>

#### FUN-070BE1843C

| 设计项 | 说明 |
|---|---|
| 函数 | `_check_authorization_narrative` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L108` |
| 签名 | `_check_authorization_narrative(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 检查`authorization_narrative`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `_llm_top_level_active` → `build_narrative_facts_for_llm` → `validate_llm_top_level_fields` → `field_reasons.items` → `out.append` → `_violation` → `_manager_wait`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、_llm_top_level_active、build_narrative_facts_for_llm、validate_llm_top_level_fields、field_reasons.items、out.append、_violation、_manager_wait、_observation_mode、strip、str、llm.get、_executable_wording_on_wait、get |
| 复杂度 / 风险 | 分支 6；跨度 21 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f9e30a657b"></a>

#### FUN-F9E30A657B

| 设计项 | 说明 |
|---|---|
| 函数 | `_check_manager_alignment` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L131` |
| 签名 | `_check_manager_alignment(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 检查`manager_alignment`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `final.get` → `get` → `out.append` → `_violation` → `conclusion.get` → `_authorized_signals_for_geometry`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、str、final.get、get、out.append、_violation、conclusion.get、_authorized_signals_for_geometry、sig.get、strip |
| 复杂度 / 风险 | 分支 6；跨度 34 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5a7430694e"></a>

#### FUN-5A7430694E

| 设计项 | 说明 |
|---|---|
| 函数 | `_check_fact_prices` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L167` |
| 签名 | `_check_fact_prices(report: dict[str, Any], registry: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`registry`（dict[str, Any]）：事实或证据登记映射 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 检查`fact_prices`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `allowed_prices` → `report.get` → `join` → `llm.get` → `re.findall` → `any` → `abs` → `narrative_price_tolerance`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | allowed_prices、report.get、join、str、llm.get、re.findall、float、any、abs、narrative_price_tolerance、out.append、_violation |
| 复杂度 / 风险 | 分支 5；跨度 26 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-26dad09727"></a>

#### FUN-26DAD09727

| 设计项 | 说明 |
|---|---|
| 函数 | `_check_freshness_language` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L195` |
| 签名 | `_check_freshness_language(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 检查`freshness_language`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `as_of.get` → `join` → `llm.get` → `any` → `blob.lower` → `out.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、as_of.get、join、str、llm.get、any、blob.lower、out.append、_violation |
| 复杂度 / 风险 | 分支 2；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cb762c7ebb"></a>

#### FUN-CB762C7EBB

| 设计项 | 说明 |
|---|---|
| 函数 | `_check_audit_metadata` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L209` |
| 签名 | `_check_audit_metadata(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 检查`audit_metadata`；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `get` → `out.append` → `_violation` → `registry.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、get、out.append、_violation、registry.get |
| 复杂度 / 风险 | 分支 2；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8b2af809d8"></a>

#### FUN-8B2AF809D8

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_report_invariants` |
| 源码位置 | [src/analysis/report_invariants.py](../../../src/analysis/report_invariants.py) · `L227` |
| 签名 | `validate_report_invariants(report: dict[str, Any], *, registry: dict[str, Any] \| None=None)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`registry`（dict[str, Any] \| None）：事实或证据登记映射；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 验证报告不变量；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_fact_registry` → `violations.extend` → `_check_signal_geometry` → `_check_authorization_narrative` → `_check_manager_alignment` → `_check_fact_prices` → `_check_freshness_language` → `_check_audit_metadata`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_fact_registry、violations.extend、_check_signal_geometry、_check_authorization_narrative、_check_manager_alignment、_check_fact_prices、_check_freshness_language、_check_audit_metadata、len |
| 复杂度 / 风险 | 分支 0；跨度 19 行；高 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_plan_signal_targets.py](../../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) · 直接动态测试 |

<a id="unit-07e7315842"></a>

### UNIT-07E7315842

**模块**：`src/analysis/report_reliability.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-07E7315842 |
| 源码 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/report_reliability.py` 的职责，通过 `compute_report_reliability` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[_clamp](#fun-c44555ff7c) · [_normalize_source](#fun-276b3e529b) · [_collect_item_sources](#fun-ac8525df31) · [_data_quality](#fun-feb3154c03) · [_freshness_quality](#fun-a8d6008a74) · [_evidence_coverage](#fun-64e7649c32) · [_source_diversity](#fun-f6a742357c) · [_cross_timeframe_agreement](#fun-c83d50260f) · [_bull_bear_separation](#fun-fb32931ed7) · [_schema_quality](#fun-4e2b9ea344) · [compute_report_reliability](#fun-3daba6ffad)

<a id="fun-c44555ff7c"></a>

#### FUN-C44555FF7C

| 设计项 | 说明 |
|---|---|
| 函数 | `_clamp` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L23` |
| 签名 | `_clamp(value: float)` |
| 参数 | `value`（float）：待处理值 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`clamp`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-276b3e529b"></a>

#### FUN-276B3E529B

| 设计项 | 说明 |
|---|---|
| 函数 | `_normalize_source` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L27` |
| 签名 | `_normalize_source(raw: str)` |
| 参数 | `raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 标准化`source`；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `text.startswith` → `text.split`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、str、text.startswith、text.split |
| 复杂度 / 风险 | 分支 4；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ac8525df31"></a>

#### FUN-AC8525DF31

| 设计项 | 说明 |
|---|---|
| 函数 | `_collect_item_sources` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L37` |
| 签名 | `_collect_item_sources(item: dict[str, Any])` |
| 参数 | `item`（dict[str, Any]）：当前处理条目 |
| 返回 | 返回 `set[str]` 类型结果 |
| 职责 | 收集`item_sources`；返回 `set[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.get` → `_normalize_source` → `refs.get` → `sources.add`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `set[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | item.get、set、_normalize_source、str、refs.get、sources.add |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-feb3154c03"></a>

#### FUN-FEB3154C03

| 设计项 | 说明 |
|---|---|
| 函数 | `_data_quality` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L47` |
| 签名 | `_data_quality(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`data_quality`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `as_of.get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get、as_of.get |
| 复杂度 / 风险 | 分支 5；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a8d6008a74"></a>

#### FUN-A8D6008A74

| 设计项 | 说明 |
|---|---|
| 函数 | `_freshness_quality` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L63` |
| 签名 | `_freshness_quality(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`freshness_quality`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `_data_quality`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、_data_quality |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-64e7649c32"></a>

#### FUN-64E7649C32

| 设计项 | 说明 |
|---|---|
| 函数 | `_evidence_coverage` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L70` |
| 签名 | `_evidence_coverage(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`evidence_coverage`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `trace.get` → `sum` → `get` → `team.get` → `debate.get` → `min` → `_clamp`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、trace.get、sum、get、team.get、len、debate.get、min、_clamp |
| 复杂度 / 风险 | 分支 0；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f6a742357c"></a>

#### FUN-F6A742357C

| 设计项 | 说明 |
|---|---|
| 函数 | `_source_diversity` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L82` |
| 签名 | `_source_diversity(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`source_diversity`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `get` → `trace.get` → `isinstance` → `block.get` → `sources.update` → `_collect_item_sources` → `_clamp`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、report.get、get、trace.get、isinstance、block.get、sources.update、_collect_item_sources、_clamp、len |
| 复杂度 / 风险 | 分支 5；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c83d50260f"></a>

#### FUN-C83D50260F

| 设计项 | 说明 |
|---|---|
| 函数 | `_cross_timeframe_agreement` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L96` |
| 签名 | `_cross_timeframe_agreement(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`cross_timeframe_agreement`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `info.get` → `tfs.values` → `isinstance` → `sum` → `max` → `_clamp`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、str、info.get、tfs.values、isinstance、sum、max、len、_clamp |
| 复杂度 / 风险 | 分支 1；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fb32931ed7"></a>

#### FUN-FB32931ED7

| 设计项 | 说明 |
|---|---|
| 函数 | `_bull_bear_separation` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L107` |
| 签名 | `_bull_bear_separation(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`bull_bear_separation`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `trace.get` → `get` → `debate.get` → `_clamp` → `abs`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、trace.get、float、get、debate.get、_clamp、abs |
| 复杂度 / 风险 | 分支 0；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4e2b9ea344"></a>

#### FUN-4E2B9EA344

| 设计项 | 说明 |
|---|---|
| 函数 | `_schema_quality` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L115` |
| 签名 | `_schema_quality(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`schema_quality`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `inv.get` → `_clamp`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get、inv.get、int、_clamp |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3daba6ffad"></a>

#### FUN-3DABA6FFAD

| 设计项 | 说明 |
|---|---|
| 函数 | `compute_report_reliability` |
| 源码位置 | [src/analysis/report_reliability.py](../../../src/analysis/report_reliability.py) · `L125` |
| 签名 | `compute_report_reliability(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 计算报告可靠度；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `_data_quality` → `_freshness_quality` → `_evidence_coverage` → `_source_diversity` → `_cross_timeframe_agreement` → `_bull_bear_separation` → `_schema_quality`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、_data_quality、_freshness_quality、_evidence_coverage、_source_diversity、_cross_timeframe_agreement、_bull_bear_separation、_schema_quality、sum、report.get、_clamp、float、llm.get |
| 复杂度 / 风险 | 分支 0；跨度 31 行；中 |
| 测试 / 验证 | [tests/integration/test_offline_report_contract.py](../../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) · 直接动态测试 |

<a id="unit-0cc0e8d72a"></a>

### UNIT-0CC0E8D72A

**模块**：`src/analysis/risk_gates.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0CC0E8D72A |
| 源码 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/risk_gates.py` 的职责，通过 `signal_trigger_ready`、`validate_signal_geometry`、`apply_risk_gates` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_risk_gates.py](../../../tests/unit/test_risk_gates.py)、[tests/unit/test_risk_gates_trigger.py](../../../tests/unit/test_risk_gates_trigger.py) |
| 验证状态 | selected |

#### 函数导航

[_signal_dict](#fun-8340a338d8) · [_entry_mid](#fun-6ea0957492) · [_risk_reward](#fun-e7212ec1e1) · [signal_trigger_ready](#fun-03ea7fde9d) · [validate_signal_geometry](#fun-8e3c0f41d3) · [apply_risk_gates](#fun-df12984213)

<a id="fun-8340a338d8"></a>

#### FUN-8340A338D8

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_dict` |
| 源码位置 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) · `L18` |
| 签名 | `_signal_dict(sig: Any)` |
| 参数 | `sig`（Any）：待评估交易信号 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`signal_dict`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `is_dataclass` → `asdict`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、is_dataclass、asdict |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6ea0957492"></a>

#### FUN-6EA0957492

| 设计项 | 说明 |
|---|---|
| 函数 | `_entry_mid` |
| 源码位置 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) · `L26` |
| 签名 | `_entry_mid(sig: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`entry_mid`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、sig.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e7212ec1e1"></a>

#### FUN-E7212EC1E1

| 设计项 | 说明 |
|---|---|
| 函数 | `_risk_reward` |
| 源码位置 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) · `L30` |
| 签名 | `_risk_reward(sig: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算风险收益比；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `sig.get` → `upper` → `_entry_mid` → `min`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、str、sig.get、upper、_entry_mid、float、min |
| 复杂度 / 风险 | 分支 3；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-03ea7fde9d"></a>

#### FUN-03EA7FDE9D

| 设计项 | 说明 |
|---|---|
| 函数 | `signal_trigger_ready` |
| 源码位置 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) · `L50` |
| 签名 | `signal_trigger_ready(sig: Any)` |
| 参数 | `sig`（Any）：待评估交易信号 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`signal_trigger_ready`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_signal_dict` → `row.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _signal_dict、row.get、bool |
| 复杂度 / 风险 | 分支 1；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_risk_gates_trigger.py](../../../tests/unit/test_risk_gates_trigger.py) · 直接动态测试 |

<a id="fun-8e3c0f41d3"></a>

#### FUN-8E3C0F41D3

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_signal_geometry` |
| 源码位置 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) · `L58` |
| 签名 | `validate_signal_geometry(sig: Any, *, current_price: float)` |
| 参数 | `sig`（Any）：待评估交易信号<br>`current_price`（float）：当前市场价格 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 验证交易信号价格几何；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_signal_dict` → `row.get` → `lower` → `upper` → `_entry_mid` → `normalize_take_profits` → `_risk_reward` → `abs`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _signal_dict、row.get、lower、str、upper、_entry_mid、float、normalize_take_profits、_risk_reward、abs |
| 复杂度 / 风险 | 分支 10；跨度 44 行；中 |
| 测试 / 验证 | [tests/unit/test_risk_gates.py](../../../tests/unit/test_risk_gates.py) · 直接动态测试 |

<a id="fun-df12984213"></a>

#### FUN-DF12984213

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_risk_gates` |
| 源码位置 | [src/analysis/risk_gates.py](../../../src/analysis/risk_gates.py) · `L104` |
| 签名 | `apply_risk_gates(reviews: list, proposal, signals: list[Any], *, current_price: float, data_as_of: dict[str, Any] \| None=None, observation_mode: bool=False)` |
| 参数 | `reviews`（list）：风险或评审结果集合<br>`proposal`（实现约定类型）：候选交易方案<br>`signals`（list[Any]）：交易信号集合<br>`current_price`（float）：当前市场价格<br>`data_as_of`（dict[str, Any] \| None）：数据截止时间；默认值 `None`<br>`observation_mode`（bool）：观察模式开关或策略；默认值 `False` |
| 返回 | 返回 `list` 类型结果 |
| 职责 | 应用`risk_gates`；返回 `list` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `as_of.get` → `global_block.append` → `notes.extend` → `log.warning` → `join` → `isinstance` → `notes.append` → `seen.add`；包含 12 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | as_of.get、global_block.append、float、list、notes.extend、log.warning、join、set、isinstance、len、notes.append、seen.add、validate_signal_geometry、kept.append、signal_trigger_ready、awaiting_trigger.append、gated.append、RiskReview |
| 复杂度 / 风险 | 分支 12；跨度 77 行；中 |
| 测试 / 验证 | [tests/unit/test_risk_gates.py](../../../tests/unit/test_risk_gates.py)、[tests/unit/test_risk_gates_trigger.py](../../../tests/unit/test_risk_gates_trigger.py) · 直接动态测试 |

<a id="unit-84723142fa"></a>

### UNIT-84723142FA

**模块**：`src/analysis/signal_geometry.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-84723142FA |
| 源码 | [src/analysis/signal_geometry.py](../../../src/analysis/signal_geometry.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/signal_geometry.py` 的职责，通过 `normalize_take_profits`、`normalize_signal_take_profits` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_signal_geometry.py](../../../tests/unit/test_signal_geometry.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_dedupe_preserve_order](#fun-35226fd4cc) | 去重`preserve_order`；返回 `list[float]` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[_dedupe_preserve_order](#fun-35226fd4cc) · [normalize_take_profits](#fun-2abed7854b) · [normalize_signal_take_profits](#fun-f4b66c6737)

<a id="fun-35226fd4cc"></a>

#### FUN-35226FD4CC

| 设计项 | 说明 |
|---|---|
| 函数 | `_dedupe_preserve_order` |
| 源码位置 | [src/analysis/signal_geometry.py](../../../src/analysis/signal_geometry.py) · `L8` |
| 签名 | `_dedupe_preserve_order(levels: list[float])` |
| 参数 | `levels`（list[float]）：候选价格水平集合 |
| 返回 | 返回 `list[float]` 类型结果 |
| 职责 | 去重`preserve_order`；返回 `list[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `out.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | out.append |
| 复杂度 / 风险 | 分支 2；跨度 6 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2abed7854b"></a>

#### FUN-2ABED7854B

| 设计项 | 说明 |
|---|---|
| 函数 | `normalize_take_profits` |
| 源码位置 | [src/analysis/signal_geometry.py](../../../src/analysis/signal_geometry.py) · `L16` |
| 签名 | `normalize_take_profits(*, direction: str, entry_low: float, entry_high: float, take_profits: list[float], theme: str='')` |
| 参数 | `direction`（str）：交易方向<br>`entry_low`（float）：入场区间下界<br>`entry_high`（float）：入场区间上界<br>`take_profits`（list[float]）：止盈目标集合<br>`theme`（str）：由 `theme` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `list[float]` 类型结果 |
| 职责 | 标准化`take_profits`；返回 `list[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `raw.strip` → `cleaned.append` → `round` → `_dedupe_preserve_order` → `sorted`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、lower、raw.strip、cleaned.append、round、_dedupe_preserve_order、sorted |
| 复杂度 / 风险 | 分支 4；跨度 25 行；中 |
| 测试 / 验证 | [tests/unit/test_signal_geometry.py](../../../tests/unit/test_signal_geometry.py) · 直接动态测试 |

<a id="fun-f4b66c6737"></a>

#### FUN-F4B66C6737

| 设计项 | 说明 |
|---|---|
| 函数 | `normalize_signal_take_profits` |
| 源码位置 | [src/analysis/signal_geometry.py](../../../src/analysis/signal_geometry.py) · `L43` |
| 签名 | `normalize_signal_take_profits(signal: dict[str, Any])` |
| 参数 | `signal`（dict[str, Any]）：当前交易信号 |
| 返回 | 返回 `list[float]` 类型结果 |
| 职责 | 标准化`signal_take_profits`；返回 `list[float]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `signal.get` → `normalize_take_profits`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | signal.get、normalize_take_profits、str、float |
| 复杂度 / 风险 | 分支 1；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-c8f58d21e1"></a>

### UNIT-C8F58D21E1

**模块**：`src/analysis/signal_identity.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C8F58D21E1 |
| 源码 | [src/analysis/signal_identity.py](../../../src/analysis/signal_identity.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/signal_identity.py` 的职责，通过 `stable_signal_id` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_signal_identity.py](../../../tests/unit/test_signal_identity.py) |
| 验证状态 | selected |

#### 函数导航

[stable_signal_id](#fun-515303b30d)

<a id="fun-515303b30d"></a>

#### FUN-515303B30D

| 设计项 | 说明 |
|---|---|
| 函数 | `stable_signal_id` |
| 源码位置 | [src/analysis/signal_identity.py](../../../src/analysis/signal_identity.py) · `L10` |
| 签名 | `stable_signal_id(signal: dict[str, Any])` |
| 参数 | `signal`（dict[str, Any]）：当前交易信号 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stable_signal_id`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `signal.get` → `round` → `json.dumps` → `hexdigest` → `hashlib.sha256` → `raw.encode`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、str、signal.get、round、float、json.dumps、hexdigest、hashlib.sha256、raw.encode |
| 复杂度 / 风险 | 分支 0；跨度 16 行；中 |
| 测试 / 验证 | [tests/unit/test_signal_identity.py](../../../tests/unit/test_signal_identity.py) · 直接动态测试 |

<a id="unit-7faaa8edca"></a>

### UNIT-7FAAA8EDCA

**模块**：`src/analysis/technical_context.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7FAAA8EDCA |
| 源码 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/technical_context.py` 的职责，通过 `distance_pct`、`primary_analysis`、`fibonacci_context`、`support_resistance_context`、`indicator_snapshot`、`structure_narrative`、`timeframe_context`、`technical_quality` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 17 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py) |
| 验证状态 | selected |

#### 函数导航

[distance_pct](#fun-86bf8dedc0) · [primary_analysis](#fun-a9814ca00a) · [fibonacci_context](#fun-e2f42619c2) · [support_resistance_context](#fun-e5355cc1ae) · [support_resistance_context.add_level](#fun-67805426ec) · [support_resistance_context.add_zone](#fun-ab952e6029) · [indicator_snapshot](#fun-41bb47141e) · [structure_narrative](#fun-ab37ca5fb2) · [timeframe_context](#fun-8894db4de1) · [technical_quality](#fun-8313bc01b7) · [build_technical_context](#fun-9091131d8f) · [_ready_indicators](#fun-303ba8669b) · [_nonzero_volume_ratio](#fun-42e28caea1) · [_rank_ict_events](#fun-be25278d2d) · [_level_kind](#fun-4a23106463) · [_zone_kind](#fun-41c768d621) · [_dedupe_levels](#fun-c48fb80201)

<a id="fun-86bf8dedc0"></a>

#### FUN-86BF8DEDC0

| 设计项 | 说明 |
|---|---|
| 函数 | `distance_pct` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L27` |
| 签名 | `distance_pct(price: float, level: float)` |
| 参数 | `price`（float）：当前或待评估价格<br>`level`（float）：候选价格水平 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`distance_pct`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a9814ca00a"></a>

#### FUN-A9814CA00A

| 设计项 | 说明 |
|---|---|
| 函数 | `primary_analysis` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L33` |
| 签名 | `primary_analysis(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `TimeframeAnalysis \| None` 类型结果 |
| 职责 | 生成`primary_analysis`结果；返回 `TimeframeAnalysis \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.analyses.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `TimeframeAnalysis \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ctx.analyses.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e2f42619c2"></a>

#### FUN-E2F42619C2

| 设计项 | 说明 |
|---|---|
| 函数 | `fibonacci_context` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L37` |
| 签名 | `fibonacci_context(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`fibonacci_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `primary_analysis` → `ctx.metrics.get` → `fibonacci_levels` → `sorted` → `round` → `distance_pct` → `abs`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | primary_analysis、ctx.metrics.get、fibonacci_levels、float、sorted、round、distance_pct、abs |
| 复杂度 / 风险 | 分支 2；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e5355cc1ae"></a>

#### FUN-E5355CC1AE

| 设计项 | 说明 |
|---|---|
| 函数 | `support_resistance_context` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L62` |
| 签名 | `support_resistance_context(ctx: MarketContext, *, limit: int=12)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`limit`（int）：返回或处理数量上限；默认值 `12` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`support_resistance_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_level_kind` → `levels.append` → `round` → `distance_pct` → `_zone_kind` → `add_level` → `metrics.get` → `primary_analysis`；包含 14 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _level_kind、levels.append、round、float、distance_pct、_zone_kind、add_level、metrics.get、primary_analysis、fibonacci_context、fib.get、row.get、TF_WEIGHT.items、ctx.analyses.get、max、getattr、liquidity_label、add_zone、_dedupe_levels、sorted |
| 复杂度 / 风险 | 分支 14；跨度 127 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-67805426ec"></a>

#### FUN-67805426EC

| 设计项 | 说明 |
|---|---|
| 函数 | `support_resistance_context.add_level` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L66` |
| 签名 | `support_resistance_context.add_level(*, price: float \| None, kind: str \| None, label: str, source: str, timeframe: str \| None=None, strength: float=0.4)` |
| 参数 | `price`（float \| None）：当前或待评估价格<br>`kind`（str \| None）：类别标识<br>`label`（str）：展示或分类标签<br>`source`（str）：数据或证据来源<br>`timeframe`（str \| None）：行情时间框架；默认值 `None`<br>`strength`（float）：由 `strength` 表示的数值参数；默认值 `0.4` |
| 返回 | 无返回值（None） |
| 职责 | 添加`level`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_level_kind` → `levels.append` → `round` → `distance_pct`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _level_kind、levels.append、round、float、distance_pct |
| 复杂度 / 风险 | 分支 1；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ab952e6029"></a>

#### FUN-AB952E6029

| 设计项 | 说明 |
|---|---|
| 函数 | `support_resistance_context.add_zone` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L90` |
| 签名 | `support_resistance_context.add_zone(*, low: float, high: float, preferred_kind: str, label: str, source: str, timeframe: str \| None, strength: float)` |
| 参数 | `low`（float）：最低价序列或下界<br>`high`（float）：最高价序列或上界<br>`preferred_kind`（str）：类别标识<br>`label`（str）：展示或分类标签<br>`source`（str）：数据或证据来源<br>`timeframe`（str \| None）：行情时间框架<br>`strength`（float）：由 `strength` 表示的数值参数 |
| 返回 | 无返回值（None） |
| 职责 | 添加`zone`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_zone_kind` → `levels.append` → `round` → `distance_pct`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_zone_kind、levels.append、round、distance_pct |
| 复杂度 / 风险 | 分支 0；跨度 25 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-41bb47141e"></a>

#### FUN-41BB47141E

| 设计项 | 说明 |
|---|---|
| 函数 | `indicator_snapshot` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L191` |
| 签名 | `indicator_snapshot(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建指标快照；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.enriched.get` → `_nonzero_volume_ratio` → `ema_relation` → `indicator_values` → `_ready_indicators` → `round`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ctx.enriched.get、_nonzero_volume_ratio、len、ema_relation、indicator_values、_ready_indicators、round |
| 复杂度 / 风险 | 分支 2；跨度 16 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py) · 直接动态测试 |

<a id="fun-ab37ca5fb2"></a>

#### FUN-AB37CA5FB2

| 设计项 | 说明 |
|---|---|
| 函数 | `structure_narrative` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L209` |
| 签名 | `structure_narrative(analysis: TimeframeAnalysis, *, max_events: int=2)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`max_events`（int）：事件集合；默认值 `2` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`structure_narrative`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `trend_map.get` → `pd_map.get` → `_latest_structure_labels` → `parts.append` → `join` → `reversed`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | trend_map.get、pd_map.get、_latest_structure_labels、parts.append、list、join、reversed |
| 复杂度 / 风险 | 分支 9；跨度 34 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-8894db4de1"></a>

#### FUN-8894DB4DE1

| 设计项 | 说明 |
|---|---|
| 函数 | `timeframe_context` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L245` |
| 签名 | `timeframe_context(tf: str, analysis: TimeframeAnalysis, *, price: float, event_limit: int=8, ob_limit: int=5, fvg_limit: int=5, liquidity_limit: int=6)` |
| 参数 | `tf`（str）：时间框架简称<br>`analysis`（TimeframeAnalysis）：当前分析结果<br>`price`（float）：当前或待评估价格<br>`event_limit`（int）：返回或处理数量上限；默认值 `8`<br>`ob_limit`（int）：返回或处理数量上限；默认值 `5`<br>`fvg_limit`（int）：返回或处理数量上限；默认值 `5`<br>`liquidity_limit`（int）：返回或处理数量上限；默认值 `6` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`timeframe_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `build_tf_snapshot` → `structure_narrative` → `_rank_ict_events` → `liquidity_label` → `round` → `distance_pct`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | build_tf_snapshot、structure_narrative、_rank_ict_events、liquidity_label、round、distance_pct |
| 复杂度 / 风险 | 分支 2；跨度 55 行；中 |
| 测试 / 验证 | [tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py) · 直接动态测试 |

<a id="fun-8313bc01b7"></a>

#### FUN-8313BC01B7

| 设计项 | 说明 |
|---|---|
| 函数 | `technical_quality` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L302` |
| 签名 | `technical_quality(ctx: MarketContext, indicators: dict[str, Any] \| None=None)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`indicators`（dict[str, Any] \| None）：由 `indicators` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`technical_quality`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `indicator_snapshot` → `ctx.enriched.get` → `min` → `scores.append` → `warnings.append` → `get` → `indicators.get` → `ready.intersection`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | indicator_snapshot、len、ctx.enriched.get、min、scores.append、warnings.append、set、get、indicators.get、ready.intersection、float、sum、ctx.analyses.values、support_resistance_context、sr.get、round |
| 复杂度 / 风险 | 分支 7；跨度 47 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9091131d8f"></a>

#### FUN-9091131D8F

| 设计项 | 说明 |
|---|---|
| 函数 | `build_technical_context` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L351` |
| 签名 | `build_technical_context(ctx: MarketContext, *, event_limit: int=8)` |
| 参数 | `ctx`（MarketContext）：运行上下文<br>`event_limit`（int）：返回或处理数量上限；默认值 `8` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`technical_context`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `indicator_snapshot` → `build_tf_snapshot` → `ctx.derived.get` → `sentiment_score` → `ctx.context_stats.get` → `technical_quality` → `fibonacci_context` → `support_resistance_context`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | indicator_snapshot、build_tf_snapshot、ctx.derived.get、sentiment_score、ctx.context_stats.get、technical_quality、fibonacci_context、support_resistance_context、build_price_action_summaries、timeframe_context |
| 复杂度 / 风险 | 分支 0；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py) · 直接动态测试 |

<a id="fun-303ba8669b"></a>

#### FUN-303BA8669B

| 设计项 | 说明 |
|---|---|
| 函数 | `_ready_indicators` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L381` |
| 签名 | `_ready_indicators(row: pd.Series)` |
| 参数 | `row`（pd.Series）：当前记录行 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`ready_indicators`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.notna`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.notna |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-42e28caea1"></a>

#### FUN-42E28CAEA1

| 设计项 | 说明 |
|---|---|
| 函数 | `_nonzero_volume_ratio` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L385` |
| 签名 | `_nonzero_volume_ratio(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`nonzero_volume_ratio`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `astype` → `sum`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | astype、float、sum、len |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-be25278d2d"></a>

#### FUN-BE25278D2D

| 设计项 | 说明 |
|---|---|
| 函数 | `_rank_ict_events` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L392` |
| 签名 | `_rank_ict_events(analysis: TimeframeAnalysis, *, limit: int)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`limit`（int）：返回或处理数量上限 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`rank_ict_events`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `priority.get` → `lower`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、priority.get、lower、str |
| 复杂度 / 风险 | 分支 0；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4a23106463"></a>

#### FUN-4A23106463

| 设计项 | 说明 |
|---|---|
| 函数 | `_level_kind` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L410` |
| 签名 | `_level_kind(price: float, level: float)` |
| 参数 | `price`（float）：当前或待评估价格<br>`level`（float）：候选价格水平 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`level_kind`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-41c768d621"></a>

#### FUN-41C768D621

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_kind` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L418` |
| 签名 | `_zone_kind(price: float, low: float, high: float, preferred: str)` |
| 参数 | `price`（float）：当前或待评估价格<br>`low`（float）：最低价序列或下界<br>`high`（float）：最高价序列或上界<br>`preferred`（str）：由 `preferred` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`zone_kind`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 3；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c48fb80201"></a>

#### FUN-C48FB80201

| 设计项 | 说明 |
|---|---|
| 函数 | `_dedupe_levels` |
| 源码位置 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) · `L428` |
| 签名 | `_dedupe_levels(levels: list[dict[str, Any]])` |
| 参数 | `levels`（list[dict[str, Any]]）：候选价格水平集合 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 去重`levels`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `best.get` → `best.values`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、round、float、best.get、list、best.values |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-ebf42549f9"></a>

### UNIT-EBF42549F9

**模块**：`src/analysis/tf_snapshot.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EBF42549F9 |
| 源码 | [src/analysis/tf_snapshot.py](../../../src/analysis/tf_snapshot.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 实现“事实、结构、信号与报告门禁”组件中 `src/analysis/tf_snapshot.py` 的职责，通过 `build_tf_snapshot` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](../SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](../SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](../SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](../SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_tf_snapshot.py](../../../tests/unit/test_tf_snapshot.py) |
| 验证状态 | selected |

#### 函数导航

[_newest_events](#fun-7354a02bce) · [_serialize_event](#fun-a7616824f7) · [_strong_weak_high_low](#fun-6dedb23061) · [build_tf_snapshot](#fun-c91f12310a)

<a id="fun-7354a02bce"></a>

#### FUN-7354A02BCE

| 设计项 | 说明 |
|---|---|
| 函数 | `_newest_events` |
| 源码位置 | [src/analysis/tf_snapshot.py](../../../src/analysis/tf_snapshot.py) · `L12` |
| 签名 | `_newest_events(events: list[StructureEvent], *, kind: str, limit: int=SNAPSHOT_LIMIT)` |
| 参数 | `events`（list[StructureEvent]）：事件集合<br>`kind`（str）：类别标识<br>`limit`（int）：返回或处理数量上限；默认值 `SNAPSHOT_LIMIT` |
| 返回 | 返回 `list[StructureEvent]` 类型结果 |
| 职责 | 构建`newest_events`；返回 `list[StructureEvent]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `matched.sort`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[StructureEvent]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | matched.sort |
| 复杂度 / 风险 | 分支 0；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a7616824f7"></a>

#### FUN-A7616824F7

| 设计项 | 说明 |
|---|---|
| 函数 | `_serialize_event` |
| 源码位置 | [src/analysis/tf_snapshot.py](../../../src/analysis/tf_snapshot.py) · `L23` |
| 签名 | `_serialize_event(event: StructureEvent)` |
| 参数 | `event`（StructureEvent）：事件对象 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 序列化`event`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | round、float |
| 复杂度 / 风险 | 分支 2；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6dedb23061"></a>

#### FUN-6DEDB23061

| 设计项 | 说明 |
|---|---|
| 函数 | `_strong_weak_high_low` |
| 源码位置 | [src/analysis/tf_snapshot.py](../../../src/analysis/tf_snapshot.py) · `L35` |
| 签名 | `_strong_weak_high_low(trend: str, swing_high: float \| None, swing_low: float \| None)` |
| 参数 | `trend`（str）：由 `trend` 表示的文本或标识<br>`swing_high`（float \| None）：摆动高点价格<br>`swing_low`（float \| None）：摆动低点价格 |
| 返回 | 返回 `dict[str, float \| None]` 类型结果 |
| 职责 | 构建`strong_weak_high_low`；返回 `dict[str, float \| None]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, float \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 2；跨度 25 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c91f12310a"></a>

#### FUN-C91F12310A

| 设计项 | 说明 |
|---|---|
| 函数 | `build_tf_snapshot` |
| 源码位置 | [src/analysis/tf_snapshot.py](../../../src/analysis/tf_snapshot.py) · `L62` |
| 签名 | `build_tf_snapshot(analysis: TimeframeAnalysis)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`tf_snapshot`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_newest_events` → `_strong_weak_high_low` → `_serialize_event`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _newest_events、_strong_weak_high_low、_serialize_event |
| 复杂度 / 风险 | 分支 0；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_tf_snapshot.py](../../../tests/unit/test_tf_snapshot.py) · 直接动态测试 |
