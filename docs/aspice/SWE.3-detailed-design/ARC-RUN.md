# ARC-RUN — 运行上下文与归档

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-run)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/run/__init__.py](#unit-3d26d1ec62) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/__init__.py](#unit-6c61c7bbf5) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/compat.py](#unit-2f300feed2) | 9 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/completion.py](#unit-af0b99f0b7) | 3 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/index.py](#unit-969bf3943a) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/prune.py](#unit-038535558b) | 2 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/schema.py](#unit-ea2375efd1) | 5 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/store.py](#unit-d3d34bc712) | 40 | 15 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/transfer.py](#unit-3365be69b6) | 2 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/config.py](#unit-e124606847) | 11 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/context.py](#unit-8a8bc190aa) | 6 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/pipeline_run.py](#unit-7df4993ab3) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-3d26d1ec62"></a>

### UNIT-3D26D1EC62

**模块**：`src/run/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3D26D1EC62 |
| 源码 | [src/run/__init__.py](../../../src/run/__init__.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-6c61c7bbf5"></a>

### UNIT-6C61C7BBF5

**模块**：`src/run/archive/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6C61C7BBF5 |
| 源码 | [src/run/archive/__init__.py](../../../src/run/archive/__init__.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-2f300feed2"></a>

### UNIT-2F300FEED2

**模块**：`src/run/archive/compat.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F300FEED2 |
| 源码 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/compat.py` 的职责，通过 `synthesize_manifest_from_legacy`、`load_manifest`、`inspect_archive`、`normalize_report`、`migrate_fetch_payload`、`migrate_analyses_payload`、`migrate_frame_payload`、`upgrade_manifest_if_needed` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 9 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [inspect_archive](#fun-8186a770f5) | 归档`inspect`；可能影响外部接口；返回 `ArchiveInspection` 类型结果。 | 外部接口 I/O | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) |

#### 函数导航

[_read_json](#fun-1bfdad92bb) · [synthesize_manifest_from_legacy](#fun-9b86f7a9e8) · [load_manifest](#fun-4abec90c24) · [inspect_archive](#fun-8186a770f5) · [normalize_report](#fun-6792cfea90) · [migrate_fetch_payload](#fun-e54bdf4478) · [migrate_analyses_payload](#fun-47ef0675a6) · [migrate_frame_payload](#fun-8a37d9c11c) · [upgrade_manifest_if_needed](#fun-5bc6d37ce9)

<a id="fun-1bfdad92bb"></a>

#### FUN-1BFDAD92BB

| 设计项 | 说明 |
|---|---|
| 函数 | `_read_json` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L37` |
| 签名 | `_read_json(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 读取JSON 数据；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `json.loads` → `path.read_text`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.loads、path.read_text |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9b86f7a9e8"></a>

#### FUN-9B86F7A9E8

| 设计项 | 说明 |
|---|---|
| 函数 | `synthesize_manifest_from_legacy` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L41` |
| 签名 | `synthesize_manifest_from_legacy(run_id: str, directory: Path)` |
| 参数 | `run_id`（str）：对象标识<br>`directory`（Path）：由调用方提供的 `directory` 输入对象 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 根据`legacy`构建`synthesize_manifest`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_read_json` → `meta_path.is_file` → `meta.get` → `build_manifest` → `isinstance`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _read_json、meta_path.is_file、int、meta.get、build_manifest、str、isinstance |
| 复杂度 / 风险 | 分支 2；跨度 19 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="fun-4abec90c24"></a>

#### FUN-4ABEC90C24

| 设计项 | 说明 |
|---|---|
| 函数 | `load_manifest` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L62` |
| 签名 | `load_manifest(run_id: str, directory: Path)` |
| 参数 | `run_id`（str）：对象标识<br>`directory`（Path）：由调用方提供的 `directory` 输入对象 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 加载归档清单；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `manifest_path.is_file` → `_read_json` → `isinstance` → `ValueError` → `manifest.setdefault` → `is_file` → `log.info` → `synthesize_manifest_from_legacy`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | FileNotFoundError；ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | manifest_path.is_file、_read_json、isinstance、ValueError、manifest.setdefault、is_file、log.info、synthesize_manifest_from_legacy、FileNotFoundError |
| 复杂度 / 风险 | 分支 3；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8186a770f5"></a>

#### FUN-8186A770F5

| 设计项 | 说明 |
|---|---|
| 函数 | `inspect_archive` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L76` |
| 签名 | `inspect_archive(run_id: str, directory: Path)` |
| 参数 | `run_id`（str）：对象标识<br>`directory`（Path）：由调用方提供的 `directory` 输入对象 |
| 返回 | 返回 `ArchiveInspection` 类型结果 |
| 职责 | 归档`inspect`；可能影响外部接口；返回 `ArchiveInspection` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `load_manifest` → `ArchiveInspection` → `manifest.get` → `warnings.append` → `errors.append` → `get` → `artifacts.get` → `report_path.is_file`；包含 22 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ArchiveInspection` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_manifest、ArchiveInspection、str、int、manifest.get、warnings.append、errors.append、get、artifacts.get、report_path.is_file、is_file、enriched_dir.is_dir、any、enriched_dir.glob、analyses_path.is_file、fetch_path.is_file、replay.get、_read_json、isinstance、pipeline_replay_errors |
| 复杂度 / 风险 | 分支 22；跨度 108 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="fun-6792cfea90"></a>

#### FUN-6792CFEA90

| 设计项 | 说明 |
|---|---|
| 函数 | `normalize_report` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L186` |
| 签名 | `normalize_report(report: Any, *, contract_version: int=REPORT_CONTRACT_VERSION)` |
| 参数 | `report`（Any）：分析报告<br>`contract_version`（int）：由 `contract_version` 表示的数值参数；默认值 `REPORT_CONTRACT_VERSION` |
| 返回 | 返回 `tuple[dict[str, Any], list[str]]` 类型结果 |
| 职责 | 标准化报告；返回 `tuple[dict[str, Any], list[str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `warnings.append` → `REPORT_TOP_LEVEL_DEFAULTS.items` → `default` → `callable` → `normalized.get` → `sections.get` → `normalized.setdefault`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any], list[str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、warnings.append、dict、REPORT_TOP_LEVEL_DEFAULTS.items、default、callable、normalized.get、sections.get、normalized.setdefault、meta.setdefault |
| 复杂度 / 风险 | 分支 9；跨度 38 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="fun-e54bdf4478"></a>

#### FUN-E54BDF4478

| 设计项 | 说明 |
|---|---|
| 函数 | `migrate_fetch_payload` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L226` |
| 签名 | `migrate_fetch_payload(raw: Any)` |
| 参数 | `raw`（Any）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 获取`migrate_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `unwrap_artifact` → `isinstance` → `ValueError` → `log.warning`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | unwrap_artifact、isinstance、ValueError、log.warning |
| 复杂度 / 风险 | 分支 3；跨度 10 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="fun-47ef0675a6"></a>

#### FUN-47EF0675A6

| 设计项 | 说明 |
|---|---|
| 函数 | `migrate_analyses_payload` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L238` |
| 签名 | `migrate_analyses_payload(raw: Any)` |
| 参数 | `raw`（Any）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`migrate_analyses_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `unwrap_artifact` → `isinstance` → `log.warning`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | unwrap_artifact、isinstance、log.warning |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8a37d9c11c"></a>

#### FUN-8A37D9C11C

| 设计项 | 说明 |
|---|---|
| 函数 | `migrate_frame_payload` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L247` |
| 签名 | `migrate_frame_payload(raw: Any)` |
| 参数 | `raw`（Any）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`migrate_frame_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `unwrap_artifact` → `isinstance` → `ValueError` → `log.warning`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | unwrap_artifact、isinstance、ValueError、log.warning |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5bc6d37ce9"></a>

#### FUN-5BC6D37CE9

| 设计项 | 说明 |
|---|---|
| 函数 | `upgrade_manifest_if_needed` |
| 源码位置 | [src/run/archive/compat.py](../../../src/run/archive/compat.py) · `L256` |
| 签名 | `upgrade_manifest_if_needed(manifest: dict[str, Any], run_id: str, directory: Path)` |
| 参数 | `manifest`（dict[str, Any]）：由 `manifest` 表示的键值映射<br>`run_id`（str）：对象标识<br>`directory`（Path）：由调用方提供的 `directory` 输入对象 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`upgrade_manifest_if_needed`；可能影响文件系统；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `manifest.get` → `upgraded.get` → `path.is_file` → `path.write_text` → `json.dumps` → `log.info`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、manifest.get、dict、upgraded.get、path.is_file、path.write_text、json.dumps、log.info |
| 复杂度 / 风险 | 分支 3；跨度 19 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="unit-af0b99f0b7"></a>

### UNIT-AF0B99F0B7

**模块**：`src/run/archive/completion.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-AF0B99F0B7 |
| 源码 | [src/run/archive/completion.py](../../../src/run/archive/completion.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/completion.py` 的职责，通过 `generation_step_statuses`、`pipeline_replay_errors`、`assert_pipeline_replay_ready` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 3 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [pipeline_replay_errors](#fun-d7f6e6e3b1) | 构建`pipeline_replay_errors`；返回 `list[str]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) |
| [assert_pipeline_replay_ready](#fun-0bb8a53ce4) | 执行`assert_pipeline_replay_ready`处理；无返回值（None）。 | 未检测到直接副作用 | — |

#### 函数导航

[generation_step_statuses](#fun-57dfc7a96b) · [pipeline_replay_errors](#fun-d7f6e6e3b1) · [assert_pipeline_replay_ready](#fun-0bb8a53ce4)

<a id="fun-57dfc7a96b"></a>

#### FUN-57DFC7A96B

| 设计项 | 说明 |
|---|---|
| 函数 | `generation_step_statuses` |
| 源码位置 | [src/run/archive/completion.py](../../../src/run/archive/completion.py) · `L35` |
| 签名 | `generation_step_statuses(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`generation_step_statuses`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `isinstance` → `strip` → `row.get` → `lower`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get、isinstance、strip、str、row.get、lower |
| 复杂度 / 风险 | 分支 4；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d7f6e6e3b1"></a>

#### FUN-D7F6E6E3B1

| 设计项 | 说明 |
|---|---|
| 函数 | `pipeline_replay_errors` |
| 源码位置 | [src/run/archive/completion.py](../../../src/run/archive/completion.py) · `L50` |
| 签名 | `pipeline_replay_errors(report: dict[str, Any], manifest: dict[str, Any] \| None=None)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`manifest`（dict[str, Any] \| None）：由 `manifest` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`pipeline_replay_errors`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `lower` → `strip` → `summary.get` → `errors.append` → `generation_step_statuses` → `step_map.get`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、lower、strip、str、summary.get、errors.append、generation_step_statuses、step_map.get |
| 复杂度 / 风险 | 分支 6；跨度 26 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="fun-0bb8a53ce4"></a>

#### FUN-0BB8A53CE4

| 设计项 | 说明 |
|---|---|
| 函数 | `assert_pipeline_replay_ready` |
| 源码位置 | [src/run/archive/completion.py](../../../src/run/archive/completion.py) · `L78` |
| 签名 | `assert_pipeline_replay_ready(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 执行`assert_pipeline_replay_ready`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `pipeline_replay_errors` → `ValueError` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pipeline_replay_errors、ValueError、join |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-969bf3943a"></a>

### UNIT-969BF3943A

**模块**：`src/run/archive/index.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-969BF3943A |
| 源码 | [src/run/archive/index.py](../../../src/run/archive/index.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/index.py` 的职责，通过 `index_path`、`load_index`、`save_index`、`upsert_index_entry`、`remove_index_entries`、`list_index_entries`、`rebuild_index_from_disk` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

[index_path](#fun-9a9d39921e) · [load_index](#fun-0ecea1344b) · [save_index](#fun-c4f5638491) · [upsert_index_entry](#fun-081a82e5e4) · [remove_index_entries](#fun-2f44aef037) · [list_index_entries](#fun-5115315dfe) · [rebuild_index_from_disk](#fun-9b663ef8e0)

<a id="fun-9a9d39921e"></a>

#### FUN-9A9D39921E

| 设计项 | 说明 |
|---|---|
| 函数 | `index_path` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L19` |
| 签名 | `index_path(root: Path)` |
| 参数 | `root`（Path）：项目根目录 |
| 返回 | 返回 `Path` 类型结果 |
| 职责 | 生成`index_path`结果；返回 `Path` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Path` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0ecea1344b"></a>

#### FUN-0ECEA1344B

| 设计项 | 说明 |
|---|---|
| 函数 | `load_index` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L23` |
| 签名 | `load_index(root: Path)` |
| 参数 | `root`（Path）：项目根目录 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 加载索引；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `index_path` → `path.is_file` → `json.loads` → `path.read_text` → `isinstance` → `payload.setdefault`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | index_path、path.is_file、json.loads、path.read_text、isinstance、payload.setdefault |
| 复杂度 / 风险 | 分支 3；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c4f5638491"></a>

#### FUN-C4F5638491

| 设计项 | 说明 |
|---|---|
| 函数 | `save_index` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L37` |
| 签名 | `save_index(root: Path, index: dict[str, Any])` |
| 参数 | `root`（Path）：项目根目录<br>`index`（dict[str, Any]）：由 `index` 表示的键值映射 |
| 返回 | 无返回值（None） |
| 职责 | 保存索引；可能影响文件系统；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `root.mkdir` → `isoformat` → `datetime.now` → `write_text` → `index_path` → `json.dumps`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 无返回值（None）；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | root.mkdir、isoformat、datetime.now、write_text、index_path、json.dumps |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-081a82e5e4"></a>

#### FUN-081A82E5E4

| 设计项 | 说明 |
|---|---|
| 函数 | `upsert_index_entry` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L48` |
| 签名 | `upsert_index_entry(root: Path, entry: dict[str, Any])` |
| 参数 | `root`（Path）：项目根目录<br>`entry`（dict[str, Any]）：入场价格或入场记录 |
| 返回 | 无返回值（None） |
| 职责 | 执行`upsert_index_entry`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `load_index` → `index.get` → `entry.get` → `row.get` → `runs.append` → `runs.sort` → `save_index`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_index、list、index.get、str、entry.get、row.get、runs.append、runs.sort、save_index |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2f44aef037"></a>

#### FUN-2F44AEF037

| 设计项 | 说明 |
|---|---|
| 函数 | `remove_index_entries` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L59` |
| 签名 | `remove_index_entries(root: Path, run_ids: set[str])` |
| 参数 | `root`（Path）：项目根目录<br>`run_ids`（set[str]）：由 `run_ids` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 移除`index_entries`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `load_index` → `index.get` → `row.get` → `save_index`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_index、index.get、str、row.get、save_index |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5115315dfe"></a>

#### FUN-5115315DFE

| 设计项 | 说明 |
|---|---|
| 函数 | `list_index_entries` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L68` |
| 签名 | `list_index_entries(root: Path, *, limit: int=100)` |
| 参数 | `root`（Path）：项目根目录<br>`limit`（int）：返回或处理数量上限；默认值 `100` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`list_index_entries`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `load_index` → `index.get` → `runs.sort` → `row.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_index、list、index.get、runs.sort、str、row.get |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) · 直接动态测试 |

<a id="fun-9b663ef8e0"></a>

#### FUN-9B663EF8E0

| 设计项 | 说明 |
|---|---|
| 函数 | `rebuild_index_from_disk` |
| 源码位置 | [src/run/archive/index.py](../../../src/run/archive/index.py) · `L75` |
| 签名 | `rebuild_index_from_disk(root: Path, rows: list[dict[str, Any]])` |
| 参数 | `root`（Path）：项目根目录<br>`rows`（list[dict[str, Any]]）：记录行集合 |
| 返回 | 无返回值（None） |
| 职责 | 根据`disk`构建`rebuild_index`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `load_index` → `sorted` → `row.get` → `save_index`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_index、sorted、str、row.get、save_index |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) · 直接动态测试 |

<a id="unit-038535558b"></a>

### UNIT-038535558B

**模块**：`src/run/archive/prune.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-038535558B |
| 源码 | [src/run/archive/prune.py](../../../src/run/archive/prune.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/prune.py` 的职责，通过 `prune_archives` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [prune_archives](#fun-a1476b11ab) | 构建`prune_archives`；返回 `list[str]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) |

#### 函数导航

[_dir_size_bytes](#fun-f03125cdf0) · [prune_archives](#fun-a1476b11ab)

<a id="fun-f03125cdf0"></a>

#### FUN-F03125CDF0

| 设计项 | 说明 |
|---|---|
| 函数 | `_dir_size_bytes` |
| 源码位置 | [src/run/archive/prune.py](../../../src/run/archive/prune.py) · `L16` |
| 签名 | `_dir_size_bytes(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`dir_size_bytes`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `path.rglob` → `child.is_file` → `child.stat`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | path.rglob、child.is_file、child.stat |
| 复杂度 / 风险 | 分支 3；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a1476b11ab"></a>

#### FUN-A1476B11AB

| 设计项 | 说明 |
|---|---|
| 函数 | `prune_archives` |
| 源码位置 | [src/run/archive/prune.py](../../../src/run/archive/prune.py) · `L27` |
| 签名 | `prune_archives(root: Path, rows: list[dict[str, Any]], *, max_count: int \| None=None, max_mb: int \| None=None)` |
| 参数 | `root`（Path）：项目根目录<br>`rows`（list[dict[str, Any]]）：记录行集合<br>`max_count`（int \| None）：数量或处理上限；默认值 `None`<br>`max_mb`（int \| None）：由调用方提供的 `max_mb` 输入对象；默认值 `None` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`prune_archives`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `row.get` → `to_remove.append` → `folder.is_dir` → `_dir_size_bytes` → `ordered.pop` → `victim.get` → `sizes.get`；包含 15 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、str、row.get、len、to_remove.append、folder.is_dir、_dir_size_bytes、ordered.pop、victim.get、sizes.get、dict.fromkeys、shutil.rmtree、removed.append、log.info、log.warning、remove_index_entries、set |
| 复杂度 / 风险 | 分支 15；跨度 57 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) · 直接动态测试 |

<a id="unit-ea2375efd1"></a>

### UNIT-EA2375EFD1

**模块**：`src/run/archive/schema.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EA2375EFD1 |
| 源码 | [src/run/archive/schema.py](../../../src/run/archive/schema.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/schema.py` 的职责，通过 `CompatibilityLevel`、`ArchiveInspection`、`app_build_version`、`artifact_envelope`、`unwrap_artifact`、`build_manifest` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 5 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [ArchiveInspection.loadable](#fun-4d1e837774) | 判断`loadable`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |

#### 函数导航

[ArchiveInspection.loadable](#fun-4d1e837774) · [app_build_version](#fun-0fd63f4847) · [artifact_envelope](#fun-350588b114) · [unwrap_artifact](#fun-9ed5b56457) · [build_manifest](#fun-a7f6be3e0f)

<a id="fun-4d1e837774"></a>

#### FUN-4D1E837774

| 设计项 | 说明 |
|---|---|
| 函数 | `ArchiveInspection.loadable` |
| 源码位置 | [src/run/archive/schema.py](../../../src/run/archive/schema.py) · `L84` |
| 签名 | `ArchiveInspection.loadable(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`loadable`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-0fd63f4847"></a>

#### FUN-0FD63F4847

| 设计项 | 说明 |
|---|---|
| 函数 | `app_build_version` |
| 源码位置 | [src/run/archive/schema.py](../../../src/run/archive/schema.py) · `L88` |
| 签名 | `app_build_version()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 构建`app_version`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rsplit` → `__file__.replace` → `strip` → `subprocess.check_output`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rsplit、__file__.replace、strip、subprocess.check_output |
| 复杂度 / 风险 | 分支 2；跨度 16 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-350588b114"></a>

#### FUN-350588B114

| 设计项 | 说明 |
|---|---|
| 函数 | `artifact_envelope` |
| 源码位置 | [src/run/archive/schema.py](../../../src/run/archive/schema.py) · `L106` |
| 签名 | `artifact_envelope(*, kind: str, artifact_version: int, payload: Any)` |
| 参数 | `kind`（str）：类别标识<br>`artifact_version`（int）：由 `artifact_version` 表示的数值参数<br>`payload`（Any）：结构化载荷 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`artifact_envelope`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-9ed5b56457"></a>

#### FUN-9ED5B56457

| 设计项 | 说明 |
|---|---|
| 函数 | `unwrap_artifact` |
| 源码位置 | [src/run/archive/schema.py](../../../src/run/archive/schema.py) · `L114` |
| 签名 | `unwrap_artifact(raw: Any, *, kind: str, default_version: int)` |
| 参数 | `raw`（Any）：尚未标准化的原始输入<br>`kind`（str）：类别标识<br>`default_version`（int）：由 `default_version` 表示的数值参数 |
| 返回 | 返回 `tuple[int, Any]` 类型结果 |
| 职责 | 构建`unwrap_artifact`；返回 `tuple[int, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `raw.get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[int, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、raw.get、int |
| 复杂度 / 风险 | 分支 5；跨度 17 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py) · 直接动态测试 |

<a id="fun-a7f6be3e0f"></a>

#### FUN-A7F6BE3E0F

| 设计项 | 说明 |
|---|---|
| 函数 | `build_manifest` |
| 源码位置 | [src/run/archive/schema.py](../../../src/run/archive/schema.py) · `L133` |
| 签名 | `build_manifest(*, run_id: str, saved_at: str \| None=None, run_config: dict[str, Any] \| None=None, summary: dict[str, Any] \| None=None, legacy: dict[str, Any] \| None=None)` |
| 参数 | `run_id`（str）：对象标识<br>`saved_at`（str \| None）：事件或数据时间；默认值 `None`<br>`run_config`（dict[str, Any] \| None）：运行配置；默认值 `None`<br>`summary`（dict[str, Any] \| None）：摘要内容；默认值 `None`<br>`legacy`（dict[str, Any] \| None）：由 `legacy` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建归档清单；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isoformat` → `datetime.now` → `app_build_version`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isoformat、datetime.now、app_build_version |
| 复杂度 / 风险 | 分支 0；跨度 50 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-d3d34bc712"></a>

### UNIT-D3D34BC712

**模块**：`src/run/archive/store.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D3D34BC712 |
| 源码 | [src/run/archive/store.py](../../../src/run/archive/store.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/store.py` 的职责，通过 `archives_root`、`run_dir`、`allocate_run_id`、`inspect_run_archive`、`list_archives`、`archives_exist`、`archive_label`、`encode_analysis` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 40 / 15 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [archives_root](#fun-1c86ff94a1) | 生成`archives_root`结果；返回 `Path` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| [inspect_run_archive](#fun-ed26b4ee99) | 执行`inspect_archive`；返回 `Any` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| [_archive_row_from_path](#fun-c1c36bd8f4) | 根据`path`构建`archive_row`；返回 `dict[str, Any] \| None` 类型结果。 | 未检测到直接副作用 | — |
| [_scan_archives](#fun-1ecbdf7dbe) | 构建`scan_archives`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | — |
| [list_archives](#fun-9e74461596) | 构建`list_archives`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| [archives_exist](#fun-02080aaef3) | 判断`archives_exist`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| [archive_label](#fun-a95b39bc72) | 归档`label`；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| [_encode_order_block](#fun-37471cb30f) | 编码订单块；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | — |
| [_decode_order_block](#fun-aef3d9744a) | 解码订单块；返回 `OrderBlock` 类型结果。 | 未检测到直接副作用 | — |
| [load_fetch](#fun-76805b2fc9) | 加载`fetch`；可能影响外部接口；返回 `DataFetchResult` 类型结果。 | 外部接口 I/O | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| [load_archive_meta](#fun-2c07f0c57c) | 加载`archive_meta`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | — |
| [load_archive_5m_bars](#fun-57bbeb8ec6) | 加载`archive_5m_bars`；返回 `pd.DataFrame` 类型结果。 | 未检测到直接副作用 | — |
| [_persist_archive_folder](#fun-70ced3edba) | 归档`persist_folder`；可能影响文件系统、外部接口；返回 `Path` 类型结果。 | 外部接口 I/O；文件系统读写 | — |
| [archive_failure_run](#fun-b471df422d) | 归档`failure_run`；可能影响共享状态；返回 `Path \| None` 类型结果。 | 共享状态变更 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) |
| [archive_run](#fun-7d1305aec2) | 归档`run`；返回 `Path` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |

#### 函数导航

[archives_root](#fun-1c86ff94a1) · [run_dir](#fun-5374bbe5e8) · [_sanitize_json](#fun-4433fa9140) · [allocate_run_id](#fun-681db272f7) · [inspect_run_archive](#fun-ed26b4ee99) · [_archive_row_from_path](#fun-c1c36bd8f4) · [_scan_archives](#fun-1ecbdf7dbe) · [list_archives](#fun-9e74461596) · [archives_exist](#fun-02080aaef3) · [archive_label](#fun-a95b39bc72) · [_ts_to_str](#fun-9ae985d283) · [_ts_from_str](#fun-85ef9fd874) · [_encode_order_block](#fun-37471cb30f) · [_decode_order_block](#fun-aef3d9744a) · [_encode_fvg](#fun-b2731107dd) · [_decode_fvg](#fun-55b5b5693e) · [_encode_structure_event](#fun-0b04667d7d) · [_decode_structure_event](#fun-5ade499def) · [_encode_liquidity](#fun-57b7676118) · [_decode_liquidity](#fun-ad119574f9) · [encode_analysis](#fun-4982e87c7f) · [decode_analysis](#fun-6c9f997021) · [_frame_to_json](#fun-789e3f37fa) · [_frame_from_json](#fun-8a5c077425) · [_external_to_json](#fun-ff14e13c2d) · [_external_from_json](#fun-a2a4e2c638) · [_fetch_payload](#fun-31c24783fe) · [load_fetch](#fun-76805b2fc9) · [load_enriched](#fun-a0b5f157c2) · [load_analyses](#fun-e23a10f8ee) · [load_archive_meta](#fun-2c07f0c57c) · [load_report](#fun-426b01b9bc) · [load_bundle](#fun-d5f0d013d7) · [load_archive_5m_bars](#fun-57bbeb8ec6) · [_failure_payload](#fun-5b44894270) · [_stub_failure_report](#fun-8665b343fa) · [_persist_archive_folder](#fun-70ced3edba) · [archive_failure_run](#fun-b471df422d) · [load_forensic_bundle](#fun-4dda0d21b3) · [archive_run](#fun-7d1305aec2)

<a id="fun-1c86ff94a1"></a>

#### FUN-1C86FF94A1

| 设计项 | 说明 |
|---|---|
| 函数 | `archives_root` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L58` |
| 签名 | `archives_root()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Path` 类型结果 |
| 职责 | 生成`archives_root`结果；返回 `Path` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Path` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-5374bbe5e8"></a>

#### FUN-5374BBE5E8

| 设计项 | 说明 |
|---|---|
| 函数 | `run_dir` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L62` |
| 签名 | `run_dir(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `Path` 类型结果 |
| 职责 | 执行`dir`；返回 `Path` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `archives_root`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Path` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | archives_root |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-4433fa9140"></a>

#### FUN-4433FA9140

| 设计项 | 说明 |
|---|---|
| 函数 | `_sanitize_json` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L66` |
| 签名 | `_sanitize_json(obj: Any)` |
| 参数 | `obj`（Any）：由调用方提供的 `obj` 输入对象 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`sanitize_json`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `math.isnan` → `math.isinf` → `round` → `abs` → `_sanitize_json` → `obj.items`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、math.isnan、math.isinf、round、abs、_sanitize_json、obj.items |
| 复杂度 / 风险 | 分支 5；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-681db272f7"></a>

#### FUN-681DB272F7

| 设计项 | 说明 |
|---|---|
| 函数 | `allocate_run_id` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L78` |
| 签名 | `allocate_run_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 执行`allocate_id`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strftime` → `datetime.now` → `exists` → `run_dir`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strftime、datetime.now、exists、run_dir |
| 复杂度 / 风险 | 分支 1；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-ed26b4ee99"></a>

#### FUN-ED26B4EE99

| 设计项 | 说明 |
|---|---|
| 函数 | `inspect_run_archive` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L88` |
| 签名 | `inspect_run_archive(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 执行`inspect_archive`；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `inspect_archive` → `run_dir`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | inspect_archive、run_dir |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-c1c36bd8f4"></a>

#### FUN-C1C36BD8F4

| 设计项 | 说明 |
|---|---|
| 函数 | `_archive_row_from_path` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L92` |
| 签名 | `_archive_row_from_path(run_id: str, path: Path)` |
| 参数 | `run_id`（str）：对象标识<br>`path`（Path）：文件或目录路径 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 根据`path`构建`archive_row`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `path.is_dir` → `is_file` → `inspect_archive` → `manifest.get` → `summary.get` → `meta_path.is_file` → `json.loads` → `meta_path.read_text`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | path.is_dir、is_file、inspect_archive、manifest.get、summary.get、str、meta_path.is_file、json.loads、meta_path.read_text、row.setdefault、legacy_meta.get |
| 复杂度 / 风险 | 分支 5；跨度 36 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1ecbdf7dbe"></a>

#### FUN-1ECBDF7DBE

| 设计项 | 说明 |
|---|---|
| 函数 | `_scan_archives` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L130` |
| 签名 | `_scan_archives(*, limit: int=100)` |
| 参数 | `limit`（int）：返回或处理数量上限；默认值 `100` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`scan_archives`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `archives_root` → `root.is_dir` → `root.iterdir` → `path.is_dir` → `_archive_row_from_path` → `rows.append` → `rows.sort` → `row.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | archives_root、root.is_dir、root.iterdir、path.is_dir、_archive_row_from_path、rows.append、rows.sort、str、row.get |
| 复杂度 / 风险 | 分支 4；跨度 13 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9e74461596"></a>

#### FUN-9E74461596

| 设计项 | 说明 |
|---|---|
| 函数 | `list_archives` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L145` |
| 签名 | `list_archives(*, limit: int=100)` |
| 参数 | `limit`（int）：返回或处理数量上限；默认值 `100` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`list_archives`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `archives_root` → `root.is_dir` → `list_index_entries` → `_scan_archives` → `max` → `rebuild_index_from_disk`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | archives_root、root.is_dir、list_index_entries、_scan_archives、max、rebuild_index_from_disk |
| 复杂度 / 风险 | 分支 3；跨度 11 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-02080aaef3"></a>

#### FUN-02080AAEF3

| 设计项 | 说明 |
|---|---|
| 函数 | `archives_exist` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L158` |
| 签名 | `archives_exist()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`archives_exist`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `list_archives`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、list_archives |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-a95b39bc72"></a>

#### FUN-A95B39BC72

| 设计项 | 说明 |
|---|---|
| 函数 | `archive_label` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L162` |
| 签名 | `archive_label(meta: dict[str, Any])` |
| 参数 | `meta`（dict[str, Any]）：审计或处理元数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 归档`label`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `format_utc8` → `get` → `isinstance` → `bars.get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、meta.get、format_utc8、get、float、isinstance、bars.get |
| 复杂度 / 风险 | 分支 5；跨度 20 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-9ae985d283"></a>

#### FUN-9AE985D283

| 设计项 | 说明 |
|---|---|
| 函数 | `_ts_to_str` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L184` |
| 签名 | `_ts_to_str(value: Any)` |
| 参数 | `value`（Any）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`ts_to_str`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isoformat` → `pd.Timestamp`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isoformat、pd.Timestamp |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-85ef9fd874"></a>

#### FUN-85EF9FD874

| 设计项 | 说明 |
|---|---|
| 函数 | `_ts_from_str` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L188` |
| 签名 | `_ts_from_str(value: str \| None)` |
| 参数 | `value`（str \| None）：待处理值 |
| 返回 | 返回 `pd.Timestamp \| None` 类型结果 |
| 职责 | 根据`str`构建`ts`；返回 `pd.Timestamp \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.Timestamp`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Timestamp \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.Timestamp |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-37471cb30f"></a>

#### FUN-37471CB30F

| 设计项 | 说明 |
|---|---|
| 函数 | `_encode_order_block` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L194` |
| 签名 | `_encode_order_block(row: OrderBlock)` |
| 参数 | `row`（OrderBlock）：当前记录行 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 编码订单块；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_ts_to_str`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _ts_to_str |
| 复杂度 / 风险 | 分支 0；跨度 8 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-aef3d9744a"></a>

#### FUN-AEF3D9744A

| 设计项 | 说明 |
|---|---|
| 函数 | `_decode_order_block` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L204` |
| 签名 | `_decode_order_block(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `OrderBlock` 类型结果 |
| 职责 | 解码订单块；返回 `OrderBlock` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `OrderBlock` → `_ts_from_str` → `payload.get` → `pd.Timestamp.utcnow`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `OrderBlock` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | OrderBlock、float、_ts_from_str、payload.get、pd.Timestamp.utcnow、str |
| 复杂度 / 风险 | 分支 0；跨度 8 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b2731107dd"></a>

#### FUN-B2731107DD

| 设计项 | 说明 |
|---|---|
| 函数 | `_encode_fvg` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L214` |
| 签名 | `_encode_fvg(row: FairValueGap)` |
| 参数 | `row`（FairValueGap）：当前记录行 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 编码公允价值缺口；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_ts_to_str`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _ts_to_str |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-55b5b5693e"></a>

#### FUN-55B5B5693E

| 设计项 | 说明 |
|---|---|
| 函数 | `_decode_fvg` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L224` |
| 签名 | `_decode_fvg(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `FairValueGap` 类型结果 |
| 职责 | 解码公允价值缺口；返回 `FairValueGap` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `FairValueGap` → `_ts_from_str` → `payload.get` → `pd.Timestamp.utcnow`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `FairValueGap` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | FairValueGap、float、_ts_from_str、payload.get、pd.Timestamp.utcnow、str |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0b04667d7d"></a>

#### FUN-0B04667D7D

| 设计项 | 说明 |
|---|---|
| 函数 | `_encode_structure_event` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L234` |
| 签名 | `_encode_structure_event(row: StructureEvent)` |
| 参数 | `row`（StructureEvent）：当前记录行 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 编码市场结构事件；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_ts_to_str`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _ts_to_str |
| 复杂度 / 风险 | 分支 1；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5ade499def"></a>

#### FUN-5ADE499DEF

| 设计项 | 说明 |
|---|---|
| 函数 | `_decode_structure_event` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L245` |
| 签名 | `_decode_structure_event(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `StructureEvent` 类型结果 |
| 职责 | 解码市场结构事件；返回 `StructureEvent` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `StructureEvent` → `_ts_from_str` → `payload.get` → `pd.Timestamp.utcnow`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `StructureEvent` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | StructureEvent、float、_ts_from_str、payload.get、pd.Timestamp.utcnow |
| 复杂度 / 风险 | 分支 0；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-57b7676118"></a>

#### FUN-57B7676118

| 设计项 | 说明 |
|---|---|
| 函数 | `_encode_liquidity` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L256` |
| 签名 | `_encode_liquidity(row: LiquidityZone)` |
| 参数 | `row`（LiquidityZone）：当前记录行 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 编码流动性结构；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ad119574f9"></a>

#### FUN-AD119574F9

| 设计项 | 说明 |
|---|---|
| 函数 | `_decode_liquidity` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L266` |
| 签名 | `_decode_liquidity(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `LiquidityZone` 类型结果 |
| 职责 | 解码流动性结构；返回 `LiquidityZone` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `LiquidityZone` → `payload.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LiquidityZone` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | LiquidityZone、float、str、payload.get、bool |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4982e87c7f"></a>

#### FUN-4982E87C7F

| 设计项 | 说明 |
|---|---|
| 函数 | `encode_analysis` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L276` |
| 签名 | `encode_analysis(analysis: TimeframeAnalysis)` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 编码`analysis`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_encode_order_block` → `_encode_fvg` → `_encode_liquidity` → `_encode_structure_event`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _encode_order_block、_encode_fvg、_encode_liquidity、_encode_structure_event |
| 复杂度 / 风险 | 分支 0；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-6c9f997021"></a>

#### FUN-6C9F997021

| 设计项 | 说明 |
|---|---|
| 函数 | `decode_analysis` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L299` |
| 签名 | `decode_analysis(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `TimeframeAnalysis` 类型结果 |
| 职责 | 解码`analysis`；返回 `TimeframeAnalysis` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `TimeframeAnalysis` → `payload.get` → `_decode_order_block` → `isinstance` → `_decode_fvg` → `_decode_liquidity` → `_decode_structure_event`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `TimeframeAnalysis` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | TimeframeAnalysis、str、payload.get、_decode_order_block、isinstance、_decode_fvg、_decode_liquidity、_decode_structure_event |
| 复杂度 / 风险 | 分支 0；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-789e3f37fa"></a>

#### FUN-789E3F37FA

| 设计项 | 说明 |
|---|---|
| 函数 | `_frame_to_json` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L322` |
| 签名 | `_frame_to_json(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`frame_to_json`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `getattr` → `out.index.tz_convert` → `ts.isoformat` → `pd.to_datetime` → `values.tolist` → `out.where` → `pd.notna`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、getattr、out.index.tz_convert、ts.isoformat、pd.to_datetime、str、values.tolist、out.where、pd.notna |
| 复杂度 / 风险 | 分支 1；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8a5c077425"></a>

#### FUN-8A5C077425

| 设计项 | 说明 |
|---|---|
| 函数 | `_frame_from_json` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L334` |
| 签名 | `_frame_from_json(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 根据JSON 数据构建数据表；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.DataFrame` → `pd.to_datetime`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.DataFrame、pd.to_datetime |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ff14e13c2d"></a>

#### FUN-FF14E13C2D

| 设计项 | 说明 |
|---|---|
| 函数 | `_external_to_json` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L340` |
| 签名 | `_external_to_json(external: ExternalFactors)` |
| 参数 | `external`（ExternalFactors）：由调用方提供的 `external` 输入对象 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`external_to_json`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.to_dict` → `event.to_dict` → `quote.to_dict`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、item.to_dict、event.to_dict、quote.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a2a4e2c638"></a>

#### FUN-A2A4E2C638

| 设计项 | 说明 |
|---|---|
| 函数 | `_external_from_json` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L355` |
| 签名 | `_external_from_json(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 根据JSON 数据构建外部数据快照；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `payload.get` → `ExternalFactors` → `HeadlineItem` → `row.get` → `isinstance` → `CalendarEvent` → `MacroQuote`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | payload.get、ExternalFactors、str、HeadlineItem、row.get、isinstance、CalendarEvent、float、MacroQuote |
| 复杂度 / 风险 | 分支 0；跨度 47 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-31c24783fe"></a>

#### FUN-31C24783FE

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_payload` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L404` |
| 签名 | `_fetch_payload(fetched: DataFetchResult)` |
| 参数 | `fetched`（DataFetchResult）：数据获取结果 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 获取结构化载荷；可能影响文件系统；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_frame_to_json` → `fetched.raw.items` → `_external_to_json` → `artifact_envelope`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _frame_to_json、fetched.raw.items、_external_to_json、artifact_envelope |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-76805b2fc9"></a>

#### FUN-76805B2FC9

| 设计项 | 说明 |
|---|---|
| 函数 | `load_fetch` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L414` |
| 签名 | `load_fetch(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `DataFetchResult` 类型结果 |
| 职责 | 加载`fetch`；可能影响外部接口；返回 `DataFetchResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `load_manifest` → `get` → `manifest.get` → `path.is_file` → `FileNotFoundError` → `migrate_fetch_payload` → `json.loads`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `DataFetchResult` 类型结果；可观察变化限于外部接口 |
| 显式异常 | FileNotFoundError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、load_manifest、str、get、manifest.get、path.is_file、FileNotFoundError、migrate_fetch_payload、json.loads、path.read_text、payload.get、_frame_from_json、migrate_frame_payload、raw_payload.items、_external_from_json、DataFetchResult |
| 复杂度 / 风险 | 分支 1；跨度 16 行；高 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-a0b5f157c2"></a>

#### FUN-A0B5F157C2

| 设计项 | 说明 |
|---|---|
| 函数 | `load_enriched` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L432` |
| 签名 | `load_enriched(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `dict[str, pd.DataFrame]` 类型结果 |
| 职责 | 加载`enriched`；返回 `dict[str, pd.DataFrame]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `load_manifest` → `get` → `manifest.get` → `enriched_spec.get` → `enriched_dir.is_dir` → `FileNotFoundError` → `sorted`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, pd.DataFrame]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | FileNotFoundError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、load_manifest、get、manifest.get、str、enriched_spec.get、enriched_dir.is_dir、FileNotFoundError、sorted、enriched_dir.glob、json.loads、path.read_text、migrate_frame_payload、_frame_from_json |
| 复杂度 / 风险 | 分支 3；跨度 15 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e23a10f8ee"></a>

#### FUN-E23A10F8EE

| 设计项 | 说明 |
|---|---|
| 函数 | `load_analyses` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L449` |
| 签名 | `load_analyses(run_id: str, enriched: dict[str, pd.DataFrame])` |
| 参数 | `run_id`（str）：对象标识<br>`enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据 |
| 返回 | 返回 `dict[str, TimeframeAnalysis]` 类型结果 |
| 职责 | 加载`analyses`；返回 `dict[str, TimeframeAnalysis]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `load_manifest` → `get` → `manifest.get` → `path.is_file` → `json.loads` → `path.read_text` → `migrate_analyses_payload`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, TimeframeAnalysis]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、load_manifest、str、get、manifest.get、path.is_file、json.loads、path.read_text、migrate_analyses_payload、decode_analysis、payload.items、isinstance、log.warning、analyze_timeframe、enriched.items |
| 复杂度 / 风险 | 分支 1；跨度 17 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-2c07f0c57c"></a>

#### FUN-2C07F0C57C

| 设计项 | 说明 |
|---|---|
| 函数 | `load_archive_meta` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L468` |
| 签名 | `load_archive_meta(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 加载`archive_meta`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `upgrade_manifest_if_needed` → `load_manifest` → `meta_path.is_file` → `json.loads` → `meta_path.read_text`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、upgrade_manifest_if_needed、load_manifest、meta_path.is_file、json.loads、meta_path.read_text |
| 复杂度 / 风险 | 分支 1；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-426b01b9bc"></a>

#### FUN-426B01B9BC

| 设计项 | 说明 |
|---|---|
| 函数 | `load_report` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L479` |
| 签名 | `load_report(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 加载报告；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `load_manifest` → `get` → `manifest.get` → `path.is_file` → `FileNotFoundError` → `json.loads` → `path.read_text`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | FileNotFoundError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、load_manifest、str、get、manifest.get、path.is_file、FileNotFoundError、json.loads、path.read_text |
| 复杂度 / 风险 | 分支 1；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-d5f0d013d7"></a>

#### FUN-D5F0D013D7

| 设计项 | 说明 |
|---|---|
| 函数 | `load_bundle` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L489` |
| 签名 | `load_bundle(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]` 类型结果 |
| 职责 | 加载`bundle`；返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `inspect_archive` → `ValueError` → `join` → `upgrade_manifest_if_needed` → `load_report` → `get` → `manifest.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、inspect_archive、ValueError、join、upgrade_manifest_if_needed、list、load_report、int、get、manifest.get、normalize_report、load_warnings.extend、load_enriched、load_analyses、report.setdefault、log.warning |
| 复杂度 / 风险 | 分支 2；跨度 39 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-57bbeb8ec6"></a>

#### FUN-57BBEB8EC6

| 设计项 | 说明 |
|---|---|
| 函数 | `load_archive_5m_bars` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L530` |
| 签名 | `load_archive_5m_bars(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 加载`archive_5m_bars`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `load_fetch` → `FileNotFoundError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | FileNotFoundError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_fetch、FileNotFoundError |
| 复杂度 / 风险 | 分支 1；跨度 6 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5b44894270"></a>

#### FUN-5B44894270

| 设计项 | 说明 |
|---|---|
| 函数 | `_failure_payload` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L538` |
| 签名 | `_failure_payload(reason: str, *, step: str \| None=None)` |
| 参数 | `reason`（str）：判定或拒绝原因<br>`step`（str \| None）：由调用方提供的 `step` 输入对象；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`failure_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isoformat` → `datetime.now`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isoformat、datetime.now |
| 复杂度 / 风险 | 分支 0；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8665b343fa"></a>

#### FUN-8665B343FA

| 设计项 | 说明 |
|---|---|
| 函数 | `_stub_failure_report` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L546` |
| 签名 | `_stub_failure_report(*, run_config: RunConfig, reason: str, generation_steps: list[dict] \| None=None, llm_io: list[dict] \| None=None, current_price: float \| None=None)` |
| 参数 | `run_config`（RunConfig）：运行配置<br>`reason`（str）：判定或拒绝原因<br>`generation_steps`（list[dict] \| None）：执行步骤集合；默认值 `None`<br>`llm_io`（list[dict] \| None）：由 `llm_io` 表示的输入集合；默认值 `None`<br>`current_price`（float \| None）：当前市场价格；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`stub_failure_report`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_config.normalized` → `format_utc8` → `isoformat` → `datetime.now` → `cfg.to_dict` → `cfg.fingerprint`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_config.normalized、format_utc8、isoformat、datetime.now、cfg.to_dict、cfg.fingerprint |
| 复杂度 / 风险 | 分支 1；跨度 26 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-70ced3edba"></a>

#### FUN-70CED3EDBA

| 设计项 | 说明 |
|---|---|
| 函数 | `_persist_archive_folder` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L574` |
| 签名 | `_persist_archive_folder(run_id: str, *, run_config: RunConfig, summary: dict[str, Any], report: dict[str, Any], fetched: DataFetchResult \| None=None, enriched: dict[str, pd.DataFrame] \| None=None, analyses: dict[str, TimeframeAnalysis] \| None=None, failure: dict[str, Any] \| None=None)` |
| 参数 | `run_id`（str）：对象标识<br>`run_config`（RunConfig）：运行配置<br>`summary`（dict[str, Any]）：摘要内容<br>`report`（dict[str, Any]）：分析报告<br>`fetched`（DataFetchResult \| None）：数据获取结果；默认值 `None`<br>`enriched`（dict[str, pd.DataFrame] \| None）：已补充指标的行情数据；默认值 `None`<br>`analyses`（dict[str, TimeframeAnalysis] \| None）：各时间框架分析结果；默认值 `None`<br>`failure`（dict[str, Any] \| None）：由 `failure` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `Path` 类型结果 |
| 职责 | 归档`persist_folder`；可能影响文件系统、外部接口；返回 `Path` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `target.mkdir` → `isoformat` → `datetime.now` → `run_config.normalized` → `write_text` → `json.dumps` → `_fetch_payload`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `Path` 类型结果；可观察变化限于文件系统、外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O；文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、target.mkdir、isoformat、datetime.now、run_config.normalized、write_text、json.dumps、_fetch_payload、_sanitize_json、encode_analysis、analyses.items、artifact_envelope、enriched_dir.mkdir、enriched.items、_frame_to_json、str、summary.get、build_manifest、cfg.to_dict、cfg.fingerprint |
| 复杂度 / 风险 | 分支 5；跨度 102 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b471df422d"></a>

#### FUN-B471DF422D

| 设计项 | 说明 |
|---|---|
| 函数 | `archive_failure_run` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L678` |
| 签名 | `archive_failure_run(run_id: str, reason: str, *, run_config: RunConfig, elapsed_s: float, fetched: DataFetchResult \| None=None, enriched: dict[str, pd.DataFrame] \| None=None, analyses: dict[str, TimeframeAnalysis] \| None=None, report: dict[str, Any] \| None=None, failure_step: str \| None=None)` |
| 参数 | `run_id`（str）：对象标识<br>`reason`（str）：判定或拒绝原因<br>`run_config`（RunConfig）：运行配置<br>`elapsed_s`（float）：由 `elapsed_s` 表示的数值参数<br>`fetched`（DataFetchResult \| None）：数据获取结果；默认值 `None`<br>`enriched`（dict[str, pd.DataFrame] \| None）：已补充指标的行情数据；默认值 `None`<br>`analyses`（dict[str, TimeframeAnalysis] \| None）：各时间框架分析结果；默认值 `None`<br>`report`（dict[str, Any] \| None）：分析报告；默认值 `None`<br>`failure_step`（str \| None）：由调用方提供的 `failure_step` 输入对象；默认值 `None` |
| 返回 | 返回 `Path \| None` 类型结果 |
| 职责 | 归档`failure_run`；可能影响共享状态；返回 `Path \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `target.exists` → `load_archive_meta` → `existing.get` → `get_progress` → `prog.snapshot` → `prog.llm_io_snapshot` → `s.get`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Path \| None` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、target.exists、load_archive_meta、str、existing.get、get_progress、prog.snapshot、prog.llm_io_snapshot、s.get、fetched.raw.get、float、_stub_failure_report、report.setdefault、get、report.get、round、_persist_archive_folder、_failure_payload |
| 复杂度 / 风险 | 分支 11；跨度 70 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) · 直接动态测试 |

<a id="fun-4dda0d21b3"></a>

#### FUN-4DDA0D21B3

| 设计项 | 说明 |
|---|---|
| 函数 | `load_forensic_bundle` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L750` |
| 签名 | `load_forensic_bundle(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]` 类型结果 |
| 职责 | 加载`forensic_bundle`；返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `directory.is_dir` → `FileNotFoundError` → `inspect_archive` → `upgrade_manifest_if_needed` → `manifest.get` → `load_report` → `get`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | FileNotFoundError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、directory.is_dir、FileNotFoundError、inspect_archive、upgrade_manifest_if_needed、manifest.get、load_report、int、get、normalize_report、failure_path.is_file、json.loads、failure_path.read_text、str、failure.get、isinstance、RunConfig.from_dict、_stub_failure_report、list、load_enriched |
| 复杂度 / 风险 | 分支 9；跨度 57 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) · 直接动态测试 |

<a id="fun-7d1305aec2"></a>

#### FUN-7D1305AEC2

| 设计项 | 说明 |
|---|---|
| 函数 | `archive_run` |
| 源码位置 | [src/run/archive/store.py](../../../src/run/archive/store.py) · `L809` |
| 签名 | `archive_run(run_id: str, *, fetched: DataFetchResult, report: dict[str, Any], enriched: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], run_config: RunConfig, elapsed_s: float)` |
| 参数 | `run_id`（str）：对象标识<br>`fetched`（DataFetchResult）：数据获取结果<br>`report`（dict[str, Any]）：分析报告<br>`enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据<br>`analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果<br>`run_config`（RunConfig）：运行配置<br>`elapsed_s`（float）：由 `elapsed_s` 表示的数值参数 |
| 返回 | 返回 `Path` 类型结果 |
| 职责 | 归档`run`；返回 `Path` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_config.normalized` → `report.get` → `meta.get` → `assert_pipeline_replay_ready` → `get` → `round` → `_persist_archive_folder`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Path` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_config.normalized、report.get、str、meta.get、assert_pipeline_replay_ready、get、round、_persist_archive_folder |
| 复杂度 / 风险 | 分支 1；跨度 32 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="unit-3365be69b6"></a>

### UNIT-3365BE69B6

**模块**：`src/run/archive/transfer.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3365BE69B6 |
| 源码 | [src/run/archive/transfer.py](../../../src/run/archive/transfer.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/archive/transfer.py` 的职责，通过 `export_archive_zip`、`import_archive_zip` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [export_archive_zip](#fun-8992fe197d) | 导出运行归档压缩包；返回 `bytes` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) |
| [import_archive_zip](#fun-41bb437461) | 导入运行归档压缩包；可能影响文件系统；返回 `str` 类型结果。 | 文件系统读写 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) |

#### 函数导航

[export_archive_zip](#fun-8992fe197d) · [import_archive_zip](#fun-41bb437461)

<a id="fun-8992fe197d"></a>

#### FUN-8992FE197D

| 设计项 | 说明 |
|---|---|
| 函数 | `export_archive_zip` |
| 源码位置 | [src/run/archive/transfer.py](../../../src/run/archive/transfer.py) · `L22` |
| 签名 | `export_archive_zip(run_id: str)` |
| 参数 | `run_id`（str）：对象标识 |
| 返回 | 返回 `bytes` 类型结果 |
| 职责 | 导出运行归档压缩包；返回 `bytes` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_dir` → `directory.is_dir` → `FileNotFoundError` → `io.BytesIO` → `zipfile.ZipFile` → `sorted` → `directory.rglob` → `path.is_file`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bytes` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | FileNotFoundError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_dir、directory.is_dir、FileNotFoundError、io.BytesIO、zipfile.ZipFile、sorted、directory.rglob、path.is_file、as_posix、path.relative_to、zf.write、zf.writestr、json.dumps、buf.getvalue |
| 复杂度 / 风险 | 分支 3；跨度 21 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) · 直接动态测试 |

<a id="fun-41bb437461"></a>

#### FUN-41BB437461

| 设计项 | 说明 |
|---|---|
| 函数 | `import_archive_zip` |
| 源码位置 | [src/run/archive/transfer.py](../../../src/run/archive/transfer.py) · `L45` |
| 签名 | `import_archive_zip(data: bytes, *, run_id: str \| None=None, overwrite: bool=False)` |
| 参数 | `data`（bytes）：输入数据<br>`run_id`（str \| None）：对象标识；默认值 `None`<br>`overwrite`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 导入运行归档压缩包；可能影响文件系统；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `archives_root` → `root.mkdir` → `zipfile.ZipFile` → `io.BytesIO` → `zf.namelist` → `json.loads` → `decode` → `zf.read`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `str` 类型结果；可观察变化限于文件系统 |
| 显式异常 | FileExistsError；ValueError |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | archives_root、root.mkdir、zipfile.ZipFile、io.BytesIO、zf.namelist、json.loads、decode、zf.read、name.split、name.endswith、ValueError、str、bundle_meta.get、len、next、iter、run_dir、target.exists、FileExistsError、target.mkdir |
| 复杂度 / 风险 | 分支 10；跨度 50 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py) · 直接动态测试 |

<a id="unit-e124606847"></a>

### UNIT-E124606847

**模块**：`src/run/config.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E124606847 |
| 源码 | [src/run/config.py](../../../src/run/config.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/config.py` 的职责，通过 `RunConfig`、`coerce_run_config`、`run_config_widget_state`、`is_advanced_run_config`、`default_panel_run_config`、`run_config_from_env`、`run_config_for_mode`、`apply_run_config` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[RunConfig.normalized](#fun-b62302b4ee) · [RunConfig.to_dict](#fun-f162ed7246) · [RunConfig.fingerprint](#fun-64a2707a8e) · [RunConfig.from_dict](#fun-b640f9deec) · [coerce_run_config](#fun-f263af19a6) · [run_config_widget_state](#fun-bb1b3b8b1f) · [is_advanced_run_config](#fun-6f8a6a5aa4) · [default_panel_run_config](#fun-3913f92b96) · [run_config_from_env](#fun-168d3dbada) · [run_config_for_mode](#fun-529864dac4) · [apply_run_config](#fun-4a55d80b54)

<a id="fun-b62302b4ee"></a>

#### FUN-B62302B4EE

| 设计项 | 说明 |
|---|---|
| 函数 | `RunConfig.normalized` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L49` |
| 签名 | `RunConfig.normalized(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `'RunConfig'` 类型结果 |
| 职责 | 生成`normalized`结果；返回 `'RunConfig'` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `RunConfig` → `ANALYST_ONLY_ALIASES.get` → `lower`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `'RunConfig'` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、RunConfig、ANALYST_ONLY_ALIASES.get、lower、bool |
| 复杂度 / 风险 | 分支 4；跨度 40 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

<a id="fun-f162ed7246"></a>

#### FUN-F162ED7246

| 设计项 | 说明 |
|---|---|
| 函数 | `RunConfig.to_dict` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L90` |
| 签名 | `RunConfig.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, object]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, object]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict` → `self.normalized`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, object]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict、self.normalized |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-64a2707a8e"></a>

#### FUN-64A2707A8E

| 设计项 | 说明 |
|---|---|
| 函数 | `RunConfig.fingerprint` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L93` |
| 签名 | `RunConfig.fingerprint(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fingerprint`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.normalized` → `json.dumps` → `hexdigest` → `hashlib.sha256` → `raw.encode` → `cfg.to_dict`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self.normalized、json.dumps、hexdigest、hashlib.sha256、raw.encode、cfg.to_dict |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

<a id="fun-b640f9deec"></a>

#### FUN-B640F9DEEC

| 设计项 | 说明 |
|---|---|
| 函数 | `RunConfig.from_dict` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L102` |
| 签名 | `RunConfig.from_dict(cls, data: dict[str, Any] \| None)` |
| 参数 | `data`（dict[str, Any] \| None）：输入数据 |
| 返回 | 返回 `'RunConfig'` 类型结果 |
| 职责 | 根据`dict`构建`当前对象`；返回 `'RunConfig'` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `RunConfig` → `fields` → `data.items` → `normalized` → `cls`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `'RunConfig'` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | RunConfig、fields、data.items、normalized、cls |
| 复杂度 / 风险 | 分支 1；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f263af19a6"></a>

#### FUN-F263AF19A6

| 设计项 | 说明 |
|---|---|
| 函数 | `coerce_run_config` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L110` |
| 签名 | `coerce_run_config(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `RunConfig \| None` 类型结果 |
| 职责 | 执行`coerce_config`；返回 `RunConfig \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `value.normalized` → `RunConfig.from_dict`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、value.normalized、RunConfig.from_dict |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-bb1b3b8b1f"></a>

#### FUN-BB1B3B8B1F

| 设计项 | 说明 |
|---|---|
| 函数 | `run_config_widget_state` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L126` |
| 签名 | `run_config_widget_state(config: RunConfig)` |
| 参数 | `config`（RunConfig）：运行配置 |
| 返回 | 返回 `dict[str, object]` 类型结果 |
| 职责 | 执行`config_widget_state`；返回 `dict[str, object]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `config.normalized` → `run_config_for_mode` → `cfg.fingerprint` → `preset.fingerprint` → `_MODE_UI_LABELS.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, object]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | config.normalized、run_config_for_mode、cfg.fingerprint、preset.fingerprint、bool、_MODE_UI_LABELS.get |
| 复杂度 / 风险 | 分支 2；跨度 33 行；中 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-6f8a6a5aa4"></a>

#### FUN-6F8A6A5AA4

| 设计项 | 说明 |
|---|---|
| 函数 | `is_advanced_run_config` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L161` |
| 签名 | `is_advanced_run_config(config: RunConfig)` |
| 参数 | `config`（RunConfig）：运行配置 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`advanced_run_config`；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `config.normalized` → `run_config_for_mode` → `cfg.fingerprint` → `preset.fingerprint`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | config.normalized、run_config_for_mode、cfg.fingerprint、preset.fingerprint |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-3913f92b96"></a>

#### FUN-3913F92B96

| 设计项 | 说明 |
|---|---|
| 函数 | `default_panel_run_config` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L167` |
| 签名 | `default_panel_run_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `RunConfig` 类型结果 |
| 职责 | 执行`default_panel_config`；返回 `RunConfig` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_config_for_mode`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_config_for_mode |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-168d3dbada"></a>

#### FUN-168D3DBADA

| 设计项 | 说明 |
|---|---|
| 函数 | `run_config_from_env` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L172` |
| 签名 | `run_config_from_env()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `RunConfig` 类型结果 |
| 职责 | 根据`env`构建运行配置；返回 `RunConfig` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `normalized` → `RunConfig`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | normalized、RunConfig |
| 复杂度 / 风险 | 分支 0；跨度 17 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-529864dac4"></a>

#### FUN-529864DAC4

| 设计项 | 说明 |
|---|---|
| 函数 | `run_config_for_mode` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L191` |
| 签名 | `run_config_for_mode(mode: AgentMode, *, llm_enabled: bool=True, llm_analyst_only: str='')` |
| 参数 | `mode`（AgentMode）：运行或分析模式<br>`llm_enabled`（bool）：控制对应行为是否启用的布尔值；默认值 `True`<br>`llm_analyst_only`（str）：由 `llm_analyst_only` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `RunConfig` 类型结果 |
| 职责 | 执行`config_mode`；返回 `RunConfig` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `normalized` → `RunConfig`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | normalized、RunConfig |
| 复杂度 / 风险 | 分支 1；跨度 17 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-4a55d80b54"></a>

#### FUN-4A55D80B54

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_run_config` |
| 源码位置 | [src/run/config.py](../../../src/run/config.py) · `L210` |
| 签名 | `apply_run_config(run_config: RunConfig)` |
| 参数 | `run_config`（RunConfig）：运行配置 |
| 返回 | 无返回值（None） |
| 职责 | 应用运行配置；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `set_run_config` → `run_config.normalized`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set_run_config、run_config.normalized |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="unit-8a8bc190aa"></a>

### UNIT-8A8BC190AA

**模块**：`src/run/context.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8A8BC190AA |
| 源码 | [src/run/context.py](../../../src/run/context.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/context.py` 的职责，通过 `set_run_config`、`reset_run_config`、`get_run_config`、`run_config_scope`、`agent_mode`、`llm_narrative_enabled` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) |
| 验证状态 | selected |

#### 函数导航

[set_run_config](#fun-2ed9157cf0) · [reset_run_config](#fun-68bfb62aad) · [get_run_config](#fun-30b017175d) · [run_config_scope](#fun-d24ed90856) · [agent_mode](#fun-7d87b82d39) · [llm_narrative_enabled](#fun-9f09ace833)

<a id="fun-2ed9157cf0"></a>

#### FUN-2ED9157CF0

| 设计项 | 说明 |
|---|---|
| 函数 | `set_run_config` |
| 源码位置 | [src/run/context.py](../../../src/run/context.py) · `L14` |
| 签名 | `set_run_config(config: RunConfig)` |
| 参数 | `config`（RunConfig）：运行配置 |
| 返回 | 返回 `Token` 类型结果 |
| 职责 | 执行`set_config`；返回 `Token` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_run_config.set` → `config.normalized`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Token` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _run_config.set、config.normalized |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-68bfb62aad"></a>

#### FUN-68BFB62AAD

| 设计项 | 说明 |
|---|---|
| 函数 | `reset_run_config` |
| 源码位置 | [src/run/context.py](../../../src/run/context.py) · `L19` |
| 签名 | `reset_run_config(token: Token)` |
| 参数 | `token`（Token）：标记或认证令牌 |
| 返回 | 无返回值（None） |
| 职责 | 重置运行配置；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_run_config.reset`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _run_config.reset |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-30b017175d"></a>

#### FUN-30B017175D

| 设计项 | 说明 |
|---|---|
| 函数 | `get_run_config` |
| 源码位置 | [src/run/context.py](../../../src/run/context.py) · `L23` |
| 签名 | `get_run_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `RunConfig` 类型结果 |
| 职责 | 获取运行配置；返回 `RunConfig` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_run_config.get` → `run_config_from_env`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _run_config.get、run_config_from_env |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-d24ed90856"></a>

#### FUN-D24ED90856

| 设计项 | 说明 |
|---|---|
| 函数 | `run_config_scope` |
| 源码位置 | [src/run/context.py](../../../src/run/context.py) · `L31` |
| 签名 | `run_config_scope(config: RunConfig)` |
| 参数 | `config`（RunConfig）：运行配置 |
| 返回 | 返回 `Iterator[RunConfig]` 类型结果 |
| 职责 | 执行`config_scope`；返回 `Iterator[RunConfig]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `set_run_config` → `config.normalized` → `reset_run_config`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Iterator[RunConfig]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set_run_config、config.normalized、reset_run_config |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-7d87b82d39"></a>

#### FUN-7D87B82D39

| 设计项 | 说明 |
|---|---|
| 函数 | `agent_mode` |
| 源码位置 | [src/run/context.py](../../../src/run/context.py) · `L40` |
| 签名 | `agent_mode()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`agent_mode`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_audit_summary.py](../../../tests/unit/test_audit_summary.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_trade_stages.py](../../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

<a id="fun-9f09ace833"></a>

#### FUN-9F09ACE833

| 设计项 | 说明 |
|---|---|
| 函数 | `llm_narrative_enabled` |
| 源码位置 | [src/run/context.py](../../../src/run/context.py) · `L44` |
| 签名 | `llm_narrative_enabled()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_narrative_enabled`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_run_config`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_run_config、bool |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-7df4993ab3"></a>

### UNIT-7DF4993AB3

**模块**：`src/run/pipeline_run.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7DF4993AB3 |
| 源码 | [src/run/pipeline_run.py](../../../src/run/pipeline_run.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | 实现“运行上下文与归档”组件中 `src/run/pipeline_run.py` 的职责，通过 `set_current_run_id`、`get_current_run_id` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](../SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](../SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](../SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](../SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[set_current_run_id](#fun-018351c88a) · [get_current_run_id](#fun-7ab49a40bf)

<a id="fun-018351c88a"></a>

#### FUN-018351C88A

| 设计项 | 说明 |
|---|---|
| 函数 | `set_current_run_id` |
| 源码位置 | [src/run/pipeline_run.py](../../../src/run/pipeline_run.py) · `L10` |
| 签名 | `set_current_run_id(run_id: str \| None)` |
| 参数 | `run_id`（str \| None）：对象标识 |
| 返回 | 无返回值（None） |
| 职责 | 执行`set_current_id`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_current_run_id.set`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _current_run_id.set |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7ab49a40bf"></a>

#### FUN-7AB49A40BF

| 设计项 | 说明 |
|---|---|
| 函数 | `get_current_run_id` |
| 源码位置 | [src/run/pipeline_run.py](../../../src/run/pipeline_run.py) · `L14` |
| 签名 | `get_current_run_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 获取`current_run_id`；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_current_run_id.get`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _current_run_id.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |
