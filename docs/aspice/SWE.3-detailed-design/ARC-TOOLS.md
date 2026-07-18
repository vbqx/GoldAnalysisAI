# ARC-TOOLS — 开发、审核与运维工具

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-tools)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [scripts/chart_compare_test.py](#unit-670f7f7454) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/check_aspice_assets.py](#unit-de82d6e44b) | 23 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/check_mt5_connection.py](#unit-d4b396b36e) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/close_fixed_issues.py](#unit-9572f90802) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/compare_pa_5m_tv.py](#unit-b4a1accfa2) | 1 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/compare_pa_tv.py](#unit-8e5050cae9) | 2 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/create_system_test_issues.py](#unit-eefb367071) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/estimate_llm_tokens.py](#unit-3fa67ae3bf) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/export_sample_report.py](#unit-2781538ff5) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/generate_aspice_readable_docs.py](#unit-44da65110b) | 23 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/generate_aspice_software_evidence.py](#unit-70ee096332) | 23 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/inspect_archive.py](#unit-37e036c51b) | 6 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/regression_test.py](#unit-ebde8e6443) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/replay_llm_narrative.py](#unit-3960e281ab) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/run_pipeline_test.py](#unit-d538889607) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/show_utf8.py](#unit-8f71f01664) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/test_live_fetch.py](#unit-c913c2495c) | 2 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/test_llm_json_fix.py](#unit-76c5f6645c) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |

<a id="unit-670f7f7454"></a>

### UNIT-670F7F7454

**模块**：`scripts/chart_compare_test.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-670F7F7454 |
| 源码 | [scripts/chart_compare_test.py](../../../scripts/chart_compare_test.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/chart_compare_test.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-de82d6e44b"></a>

### UNIT-DE82D6E44B

**模块**：`scripts/check_aspice_assets.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DE82D6E44B |
| 源码 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/check_aspice_assets.py` 的职责，通过 `stable_id`、`read_yaml`、`rel`、`source_files`、`document_files`、`document_classification`、`document_title`、`markdown_anchors` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 23 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[stable_id](#fun-be28bb75d8) · [read_yaml](#fun-04a944fece) · [rel](#fun-6d47944494) · [source_files](#fun-6175ef47cc) · [document_files](#fun-7b527c5c90) · [document_classification](#fun-5ae4fdb3fc) · [document_title](#fun-64eed0d566) · [markdown_anchors](#fun-3f6353d53b) · [markdown_files](#fun-383eefc7a5) · [validate_markdown_links](#fun-d254cae005) · [build_document_register](#fun-fc561d92db) · [component_for](#fun-3c97caee46) · [module_doc](#fun-f9f01026c2) · [build_units](#fun-d410be7a27) · [build_trace_rows](#fun-2ceb1f60f7) · [dependency_outputs](#fun-beae13cf69) · [csv_text](#fun-c861d95e3c) · [process_index](#fun-cee22c60cc) · [expected_outputs](#fun-e18bb2dfa3) · [validate_model](#fun-3c81471a20) · [write_outputs](#fun-f855325a7a) · [check_outputs](#fun-e57502a017) · [main](#fun-4aa307b1b4)

<a id="fun-be28bb75d8"></a>

#### FUN-BE28BB75D8

| 设计项 | 说明 |
|---|---|
| 函数 | `stable_id` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L68` |
| 签名 | `stable_id(prefix: str, value: str)` |
| 参数 | `prefix`（str）：由 `prefix` 表示的文本或标识<br>`value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成稳定标识文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `hexdigest` → `hashlib.sha1` → `value.encode`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、hexdigest、hashlib.sha1、value.encode |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-04a944fece"></a>

#### FUN-04A944FECE

| 设计项 | 说明 |
|---|---|
| 函数 | `read_yaml` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L73` |
| 签名 | `read_yaml(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 读取YAML 数据；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `yaml.safe_load` → `path.read_text` → `isinstance` → `ValueError` → `path.relative_to`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | yaml.safe_load、path.read_text、isinstance、ValueError、path.relative_to |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6d47944494"></a>

#### FUN-6D47944494

| 设计项 | 说明 |
|---|---|
| 函数 | `rel` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L80` |
| 签名 | `rel(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成仓库相对路径文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `as_posix` → `path.relative_to`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | as_posix、path.relative_to |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../../tests/unit/test_report_reliability.py) · 直接动态测试 |

<a id="fun-6175ef47cc"></a>

#### FUN-6175EF47CC

| 设计项 | 说明 |
|---|---|
| 函数 | `source_files` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L84` |
| 签名 | `source_files()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[Path]` 类型结果 |
| 职责 | 构建受审源码文件清单；返回 `list[Path]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `ROOT.rglob` → `any` → `path.relative_to` → `casefold` → `rel`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[Path]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、ROOT.rglob、any、path.relative_to、casefold、rel |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7b527c5c90"></a>

#### FUN-7B527C5C90

| 设计项 | 说明 |
|---|---|
| 函数 | `document_files` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L95` |
| 签名 | `document_files()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[Path]` 类型结果 |
| 职责 | 构建受控文档清单；返回 `list[Path]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rglob` → `path.is_file` → `paths.update` → `path.exists` → `ROOT.glob` → `sorted` → `casefold` → `rel`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[Path]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rglob、path.is_file、paths.update、path.exists、ROOT.glob、sorted、casefold、rel |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5ae4fdb3fc"></a>

#### FUN-5AE4FDB3FC

| 设计项 | 说明 |
|---|---|
| 函数 | `document_classification` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L104` |
| 签名 | `document_classification(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `tuple[str, str, str, str]` 类型结果 |
| 职责 | 构建`document_classification`；返回 `tuple[str, str, str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rel` → `path_str.startswith` → `path.suffix.lower`；包含 29 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str, str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rel、path_str.startswith、path.suffix.lower |
| 复杂度 / 风险 | 分支 29；跨度 71 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-64eed0d566"></a>

#### FUN-64EED0D566

| 设计项 | 说明 |
|---|---|
| 函数 | `document_title` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L177` |
| 签名 | `document_title(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`document_title`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `path.exists` → `path.suffix.lower` → `path.read_text` → `re.search` → `strip` → `match.group` → `replace` → `path.stem.replace`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | path.exists、path.suffix.lower、path.read_text、re.search、strip、match.group、replace、path.stem.replace |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3f6353d53b"></a>

#### FUN-3F6353D53B

| 设计项 | 说明 |
|---|---|
| 函数 | `markdown_anchors` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L186` |
| 签名 | `markdown_anchors(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `set[str]` 类型结果 |
| 职责 | 构建`markdown_anchors`；返回 `set[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `path.read_text` → `match.group` → `EXPLICIT_ANCHOR_RE.finditer` → `defaultdict` → `HEADING_RE.finditer` → `lower` → `strip` → `re.sub`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `set[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | path.read_text、match.group、EXPLICIT_ANCHOR_RE.finditer、defaultdict、HEADING_RE.finditer、lower、strip、re.sub、anchors.add |
| 复杂度 / 风险 | 分支 3；跨度 15 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-383eefc7a5"></a>

#### FUN-383EEFC7A5

| 设计项 | 说明 |
|---|---|
| 函数 | `markdown_files` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L203` |
| 签名 | `markdown_files()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[Path]` 类型结果 |
| 职责 | 构建`markdown_files`；返回 `list[Path]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `ROOT.rglob` → `any` → `path.relative_to`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[Path]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、ROOT.rglob、any、path.relative_to |
| 复杂度 / 风险 | 分支 0；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d254cae005"></a>

#### FUN-D254CAE005

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_markdown_links` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L212` |
| 签名 | `validate_markdown_links()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 验证`markdown_links`；可能影响共享状态；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `markdown_files` → `source.read_text` → `MARKDOWN_LINK_RE.finditer` → `strip` → `split` → `match.group` → `raw_target.startswith` → `raw_target.partition`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | markdown_files、source.read_text、MARKDOWN_LINK_RE.finditer、strip、split、match.group、raw_target.startswith、raw_target.partition、resolve、unquote、text.count、match.start、target.is_relative_to、errors.append、rel、target.exists、target.suffix.lower、anchor_cache.setdefault、markdown_anchors |
| 复杂度 / 风险 | 分支 8；跨度 27 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fc561d92db"></a>

#### FUN-FC561D92DB

| 设计项 | 说明 |
|---|---|
| 函数 | `build_document_register` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L241` |
| 签名 | `build_document_register()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 构建文档登记表；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `document_files` → `document_classification` → `rows.append` → `stable_id` → `rel` → `document_title`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | document_files、document_classification、rows.append、stable_id、rel、document_title |
| 复杂度 / 风险 | 分支 3；跨度 20 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3c97caee46"></a>

#### FUN-3C97CAEE46

| 设计项 | 说明 |
|---|---|
| 函数 | `component_for` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L263` |
| 签名 | `component_for(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成源码所属架构组件文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rel` → `value.startswith`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rel、value.startswith |
| 复杂度 / 风险 | 分支 10；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f9f01026c2"></a>

#### FUN-F9F01026C2

| 设计项 | 说明 |
|---|---|
| 函数 | `module_doc` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L288` |
| 签名 | `module_doc(tree: ast.AST, component_name: str, source_path: str)` |
| 参数 | `tree`（ast.AST）：由调用方提供的 `tree` 输入对象<br>`component_name`（str）：对象名称<br>`source_path`（str）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成模块职责说明文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ast.get_docstring` → `rstrip` → `doc.splitlines` → `re.search` → `getattr` → `isinstance` → `node.name.startswith` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ast.get_docstring、rstrip、doc.splitlines、re.search、getattr、isinstance、node.name.startswith、join |
| 复杂度 / 风险 | 分支 2；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d410be7a27"></a>

#### FUN-D410BE7A27

| 设计项 | 说明 |
|---|---|
| 函数 | `build_units` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L302` |
| 签名 | `build_units(arch: dict[str, Any])` |
| 参数 | `arch`（dict[str, Any]）：软件架构模型 |
| 返回 | 返回 `tuple[list[dict[str, str]], list[dict[str, str]]]` 类型结果 |
| 职责 | 构建软件单元清单；返回 `tuple[list[dict[str, str]], list[dict[str, str]]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `source_files` → `rel` → `component_for` → `ast.parse` → `path.read_text` → `stable_id` → `join` → `units.append`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict[str, str]], list[dict[str, str]]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | source_files、rel、component_for、ast.parse、path.read_text、stable_id、join、units.append、module_doc、ast.walk、ast.iter_child_nodes、isinstance、parents.get、owners.append、reversed、functions.append、str、node.name.startswith、sorted、int |
| 复杂度 / 风险 | 分支 8；跨度 57 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2ceb1f60f7"></a>

#### FUN-2CEB1F60F7

| 设计项 | 说明 |
|---|---|
| 函数 | `build_trace_rows` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L361` |
| 签名 | `build_trace_rows(reqs: dict[str, Any], units: list[dict[str, str]])` |
| 参数 | `reqs`（dict[str, Any]）：由 `reqs` 表示的键值映射<br>`units`（list[dict[str, str]]）：由 `units` 表示的输入集合 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 构建追溯记录；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `defaultdict` → `append` → `sorted` → `rows.append` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | defaultdict、append、sorted、rows.append、join |
| 复杂度 / 风险 | 分支 2；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-beae13cf69"></a>

#### FUN-BEAE13CF69

| 设计项 | 说明 |
|---|---|
| 函数 | `dependency_outputs` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L382` |
| 签名 | `dependency_outputs(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `tuple[str, str]` 类型结果 |
| 职责 | 构建依赖锁与 SBOM 产物；返回 `tuple[str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `report.get` → `lower` → `get` → `item.get` → `archive.get` → `hashes.get` → `lock_lines.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、report.get、lower、get、item.get、archive.get、hashes.get、lock_lines.append、replace、name.lower、components.append、join、json.dumps |
| 复杂度 / 风险 | 分支 3；跨度 35 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c861d95e3c"></a>

#### FUN-C861D95E3C

| 设计项 | 说明 |
|---|---|
| 函数 | `csv_text` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L419` |
| 签名 | `csv_text(rows: list[dict[str, str]])` |
| 参数 | `rows`（list[dict[str, str]]）：记录行集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成CSV 文本文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ValueError` → `io.StringIO` → `csv.DictWriter` → `writer.writeheader` → `writer.writerows` → `buffer.getvalue`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ValueError、io.StringIO、csv.DictWriter、list、writer.writeheader、writer.writerows、buffer.getvalue |
| 复杂度 / 风险 | 分支 1；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cee22c60cc"></a>

#### FUN-CEE22C60CC

| 设计项 | 说明 |
|---|---|
| 函数 | `process_index` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L429` |
| 签名 | `process_index(rows: list[dict[str, str]])` |
| 参数 | `rows`（list[dict[str, str]]）：记录行集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成ASPICE 过程文档索引文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `defaultdict` → `append` → `sorted` → `lines.extend` → `startswith` → `removeprefix` → `lines.append` → `join`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | defaultdict、append、sorted、lines.extend、startswith、removeprefix、lines.append、join |
| 复杂度 / 风险 | 分支 5；跨度 24 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e18bb2dfa3"></a>

#### FUN-E18BB2DFA3

| 设计项 | 说明 |
|---|---|
| 函数 | `expected_outputs` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L455` |
| 签名 | `expected_outputs()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[Path, str]` 类型结果 |
| 职责 | 构建预期生成产物；返回 `dict[Path, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `read_yaml` → `build_document_register` → `build_units` → `build_trace_rows` → `PIP_REPORT_PATH.exists` → `report_path.exists` → `ValueError` → `json.loads`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[Path, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | read_yaml、build_document_register、build_units、build_trace_rows、PIP_REPORT_PATH.exists、report_path.exists、ValueError、json.loads、report_path.read_text、dependency_outputs、csv_text、process_index、json.dumps |
| 复杂度 / 风险 | 分支 3；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3c81471a20"></a>

#### FUN-3C81471A20

| 设计项 | 说明 |
|---|---|
| 函数 | `validate_model` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L480` |
| 签名 | `validate_model(*, allow_generated_missing: bool=False)` |
| 参数 | `allow_generated_missing`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 验证ASPICE 数据模型；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `read_yaml` → `reqs.get` → `arch.get` → `ver.get` → `errors.append` → `req_map.items` → `req.get` → `get`；包含 26 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | read_yaml、reqs.get、arch.get、ver.get、len、errors.append、req_map.items、req.get、get、reverse_ver.get、arch_map.items、component.get、arch_map.values、item.get、any、reverse_ver.items、cm.get、item_path.exists |
| 复杂度 / 风险 | 分支 26；跨度 64 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f855325a7a"></a>

#### FUN-F855325A7A

| 设计项 | 说明 |
|---|---|
| 函数 | `write_outputs` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L546` |
| 签名 | `write_outputs(outputs: dict[Path, str])` |
| 参数 | `outputs`（dict[Path, str]）：由 `outputs` 表示的键值映射 |
| 返回 | 无返回值（None） |
| 职责 | 写入生成产物；可能影响文件系统；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `ASPICE.mkdir` → `outputs.items` → `path.parent.mkdir` → `path.write_text`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 无返回值（None）；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ASPICE.mkdir、outputs.items、path.parent.mkdir、path.write_text |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e57502a017"></a>

#### FUN-E57502A017

| 设计项 | 说明 |
|---|---|
| 函数 | `check_outputs` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L553` |
| 签名 | `check_outputs(outputs: dict[Path, str])` |
| 参数 | `outputs`（dict[Path, str]）：由 `outputs` 表示的键值映射 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 检查生成产物；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `outputs.items` → `path.exists` → `errors.append` → `rel` → `path.read_text` → `build_document_register` → `document_files` → `sorted`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | outputs.items、path.exists、errors.append、rel、path.read_text、build_document_register、document_files、sorted、exists、errors.extend、validate_markdown_links |
| 复杂度 / 风险 | 分支 5；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4aa307b1b4"></a>

#### FUN-4AA307B1B4

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/check_aspice_assets.py](../../../scripts/check_aspice_assets.py) · `L578` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/check_aspice_assets.py` 的主流程；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_mutually_exclusive_group` → `group.add_argument` → `parser.parse_args` → `validate_model` → `expected_outputs` → `print` → `join`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_mutually_exclusive_group、group.add_argument、parser.parse_args、validate_model、expected_outputs、print、join、write_outputs、len、errors.extend、check_outputs、build_units、read_yaml、document_files |
| 复杂度 / 风险 | 分支 3；跨度 27 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-d4b396b36e"></a>

### UNIT-D4B396B36E

**模块**：`scripts/check_mt5_connection.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D4B396B36E |
| 源码 | [scripts/check_mt5_connection.py](../../../scripts/check_mt5_connection.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/check_mt5_connection.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[main](#fun-8efe0f5793)

<a id="fun-8efe0f5793"></a>

#### FUN-8EFE0F5793

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/check_mt5_connection.py](../../../scripts/check_mt5_connection.py) · `L19` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/check_mt5_connection.py` 的主流程；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `MT5Config` → `get_mt5_provider` → `print` → `provider.account_info` → `info.get` → `provider.shutdown`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | MT5Config、get_mt5_provider、print、provider.account_info、info.get、provider.shutdown |
| 复杂度 / 风险 | 分支 2；跨度 27 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-9572f90802"></a>

### UNIT-9572F90802

**模块**：`scripts/close_fixed_issues.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9572F90802 |
| 源码 | [scripts/close_fixed_issues.py](../../../scripts/close_fixed_issues.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/close_fixed_issues.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-b4a1accfa2"></a>

### UNIT-B4A1ACCFA2

**模块**：`scripts/compare_pa_5m_tv.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B4A1ACCFA2 |
| 源码 | [scripts/compare_pa_5m_tv.py](../../../scripts/compare_pa_5m_tv.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/compare_pa_5m_tv.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [main](#fun-406938ab22) | 执行 `scripts/compare_pa_5m_tv.py` 的主流程；可能影响外部接口；无返回值（None）。 | 外部接口 I/O | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |

#### 函数导航

[main](#fun-406938ab22)

<a id="fun-406938ab22"></a>

#### FUN-406938AB22

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/compare_pa_5m_tv.py](../../../scripts/compare_pa_5m_tv.py) · `L26` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行 `scripts/compare_pa_5m_tv.py` 的主流程；可能影响外部接口；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_all_data` → `enrich` → `fetched.raw.items` → `print` → `analyze_dgt_price_action` → `build_price_action_summaries` → `vp.get` → `lvl.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 无返回值（None）；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_all_data、enrich、fetched.raw.items、float、print、analyze_dgt_price_action、build_price_action_summaries、vp.get、lvl.get、analyze_timeframe、round |
| 复杂度 / 风险 | 分支 4；跨度 29 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-8e5050cae9"></a>

### UNIT-8E5050CAE9

**模块**：`scripts/compare_pa_tv.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8E5050CAE9 |
| 源码 | [scripts/compare_pa_tv.py](../../../scripts/compare_pa_tv.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/compare_pa_tv.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [main](#fun-d24395608c) | 执行 `scripts/compare_pa_tv.py` 的主流程；可能影响外部接口；无返回值（None）。 | 外部接口 I/O | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |

#### 函数导航

[_delta](#fun-818471ea1d) · [main](#fun-d24395608c)

<a id="fun-818471ea1d"></a>

#### FUN-818471EA1D

| 设计项 | 说明 |
|---|---|
| 函数 | `_delta` |
| 源码位置 | [scripts/compare_pa_tv.py](../../../scripts/compare_pa_tv.py) · `L26` |
| 签名 | `_delta(ours: float \| None, tv: float)` |
| 参数 | `ours`（float \| None）：由调用方提供的 `ours` 输入对象<br>`tv`（float）：由 `tv` 表示的数值参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成差值文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d24395608c"></a>

#### FUN-D24395608C

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/compare_pa_tv.py](../../../scripts/compare_pa_tv.py) · `L32` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行 `scripts/compare_pa_tv.py` 的主流程；可能影响外部接口；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_all_data` → `enrich` → `fetched.raw.items` → `print` → `df15.tail` → `analyze_dgt_price_action` → `_delta` → `build_volume_profile`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 无返回值（None）；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_all_data、enrich、fetched.raw.items、float、print、df15.tail、analyze_dgt_price_action、_delta、build_volume_profile、len、build_price_action_summaries、get、pa.get、vp.get、abs、x.get、analyze_timeframe、generate_trading_signals、sentiment_score |
| 复杂度 / 风险 | 分支 7；跨度 81 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-eefb367071"></a>

### UNIT-EEFB367071

**模块**：`scripts/create_system_test_issues.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EEFB367071 |
| 源码 | [scripts/create_system_test_issues.py](../../../scripts/create_system_test_issues.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/create_system_test_issues.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3fa67ae3bf"></a>

### UNIT-3FA67AE3BF

**模块**：`scripts/estimate_llm_tokens.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3FA67AE3BF |
| 源码 | [scripts/estimate_llm_tokens.py](../../../scripts/estimate_llm_tokens.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/estimate_llm_tokens.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_sys](#fun-85a3e4b3a3) · [_est](#fun-487ef18d78) · [main](#fun-7143a40322)

<a id="fun-85a3e4b3a3"></a>

#### FUN-85A3E4B3A3

| 设计项 | 说明 |
|---|---|
| 函数 | `_sys` |
| 源码位置 | [scripts/estimate_llm_tokens.py](../../../scripts/estimate_llm_tokens.py) · `L39` |
| 签名 | `_sys(mod: str)` |
| 参数 | `mod`（str）：由 `mod` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`sys`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `importlib.import_module`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、importlib.import_module |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-487ef18d78"></a>

#### FUN-487EF18D78

| 设计项 | 说明 |
|---|---|
| 函数 | `_est` |
| 源码位置 | [scripts/estimate_llm_tokens.py](../../../scripts/estimate_llm_tokens.py) · `L43` |
| 签名 | `_est(chars: int)` |
| 参数 | `chars`（int）：由 `chars` 表示的数值参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`est`；返回 `int` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7143a40322"></a>

#### FUN-7143A40322

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/estimate_llm_tokens.py](../../../scripts/estimate_llm_tokens.py) · `L47` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/estimate_llm_tokens.py` 的主流程；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_sample_context` → `run_analyst_team` → `run_bullish_researcher` → `run_bearish_researcher` → `run_debate` → `compute_trading_signals` → `run_trader_agent` → `run_risk_team`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _sample_context、run_analyst_team、run_bullish_researcher、run_bearish_researcher、run_debate、compute_trading_signals、run_trader_agent、run_risk_team、len、run_manager、build_report、_sys、technical_analyst_payload、fundamentals_analyst_payload、news_analyst_payload、sentiment_analyst_payload、research_payload、debate_payload、trader_payload、risk_payload |
| 复杂度 / 风险 | 分支 1；跨度 57 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-2781538ff5"></a>

### UNIT-2781538FF5

**模块**：`scripts/export_sample_report.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2781538FF5 |
| 源码 | [scripts/export_sample_report.py](../../../scripts/export_sample_report.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Export a脱敏 sample report JSON for docs/aspice/SWE.3-detailed-design/reference/examples/ (no network)。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) |
| 验证状态 | selected |

#### 函数导航

[_sanitize](#fun-a27c77a1d3) · [_sample_context](#fun-b0ffdeb50d) · [main](#fun-8b24cef8e4)

<a id="fun-a27c77a1d3"></a>

#### FUN-A27C77A1D3

| 设计项 | 说明 |
|---|---|
| 函数 | `_sanitize` |
| 源码位置 | [scripts/export_sample_report.py](../../../scripts/export_sample_report.py) · `L43` |
| 签名 | `_sanitize(obj)` |
| 参数 | `obj`（实现约定类型）：由调用方提供的 `obj` 输入对象 |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 生成可序列化安全值结果；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `math.isnan` → `math.isinf` → `round` → `abs` → `_sanitize` → `obj.items`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、math.isnan、math.isinf、round、abs、_sanitize、obj.items |
| 复杂度 / 风险 | 分支 5；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b0ffdeb50d"></a>

#### FUN-B0FFDEB50D

| 设计项 | 说明 |
|---|---|
| 函数 | `_sample_context` |
| 源码位置 | [scripts/export_sample_report.py](../../../scripts/export_sample_report.py) · `L55` |
| 签名 | `_sample_context()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `MarketContext` 类型结果 |
| 职责 | 生成`sample_context`结果；返回 `MarketContext` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.date_range` → `pd.Series` → `to_numpy` → `range` → `pd.DataFrame` → `enrich` → `analyze_timeframe` → `round`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `MarketContext` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.date_range、pd.Series、to_numpy、range、pd.DataFrame、enrich、analyze_timeframe、round、float、ExternalFactors、HeadlineItem、MacroQuote、MarketContext |
| 复杂度 / 风险 | 分支 0；跨度 61 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="fun-8b24cef8e4"></a>

#### FUN-8B24CEF8E4

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/export_sample_report.py](../../../scripts/export_sample_report.py) · `L118` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/export_sample_report.py` 的主流程；可能影响文件系统；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_sample_context` → `AgentPipelineMeta` → `run_analyst_team` → `run_bullish_researcher` → `run_bearish_researcher` → `run_debate` → `compute_trading_signals` → `run_trader_agent`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `int` 类型结果；可观察变化限于文件系统 |
| 显式异常 | RuntimeError |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _sample_context、AgentPipelineMeta、run_analyst_team、run_bullish_researcher、run_bearish_researcher、run_debate、compute_trading_signals、run_trader_agent、run_risk_team、len、run_manager、build_report、get、report.get、isinstance、math.isnan、RuntimeError、pipeline_meta.to_dict、m.to_dict、build_rule_narrative_sections |
| 复杂度 / 风险 | 分支 1；跨度 60 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-44da65110b"></a>

### UNIT-44DA65110B

**模块**：`scripts/generate_aspice_readable_docs.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-44DA65110B |
| 源码 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/generate_aspice_readable_docs.py` 的职责，通过 `expected_outputs`、`main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 23 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_yaml](#fun-8e0ae30e6f) · [_csv](#fun-b8135ddcb1) · [_cell](#fun-211336c6ae) · [_list](#fun-36e6a8909a) · [_anchor](#fun-0ad419ab09) · [_req_links](#fun-2631f769a2) · [_arch_links](#fun-532ec35635) · [_measure_links](#fun-a9d2621b2a) · [_test_links](#fun-0aee39f96b) · [_table](#fun-84d7ee0257) · [_front](#fun-6a04465af3) · [_requirements_doc](#fun-1839614189) · [_architecture_diagrams](#fun-c0e8b72578) · [_architecture_doc](#fun-73cd1d7b70) · [_design_outputs](#fun-cccb5498f5) · [_unit_section](#fun-4e2eb68af0) · [_unit_verification_doc](#fun-34bbf83058) · [_integration_doc](#fun-be2fd65386) · [_qualification_doc](#fun-2336ffb14c) · [_configuration_doc](#fun-009efeb3d5) · [_traceability_doc](#fun-48fe08d05f) · [expected_outputs](#fun-a614f5b1a4) · [main](#fun-1ea9f2053e)

<a id="fun-8e0ae30e6f"></a>

#### FUN-8E0AE30E6F

| 设计项 | 说明 |
|---|---|
| 函数 | `_yaml` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L27` |
| 签名 | `_yaml(name: str)` |
| 参数 | `name`（str）：对象名称 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建YAML 数据；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `yaml.safe_load` → `read_text` → `isinstance` → `ValueError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | yaml.safe_load、read_text、isinstance、ValueError |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b8135ddcb1"></a>

#### FUN-B8135DDCB1

| 设计项 | 说明 |
|---|---|
| 函数 | `_csv` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L34` |
| 签名 | `_csv(name: str)` |
| 参数 | `name`（str）：对象名称 |
| 返回 | 返回 `list[dict[str, str]]` 类型结果 |
| 职责 | 构建CSV 数据；返回 `list[dict[str, str]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `open` → `csv.DictReader`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, str]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | open、list、csv.DictReader |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-211336c6ae"></a>

#### FUN-211336C6AE

| 设计项 | 说明 |
|---|---|
| 函数 | `_cell` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L39` |
| 签名 | `_cell(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`cell`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `join` → `strip` → `replace` → `text.replace`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、join、str、strip、replace、text.replace |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-36e6a8909a"></a>

#### FUN-36E6A8909A

| 设计项 | 说明 |
|---|---|
| 函数 | `_list` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L48` |
| 签名 | `_list(value: str)` |
| 参数 | `value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`list`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `value.split`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、value.split |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0ad419ab09"></a>

#### FUN-0AD419AB09

| 设计项 | 说明 |
|---|---|
| 函数 | `_anchor` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L52` |
| 签名 | `_anchor(value: str)` |
| 参数 | `value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成Markdown 锚点文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `replace` → `value.lower`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | replace、value.lower |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2631f769a2"></a>

#### FUN-2631F769A2

| 设计项 | 说明 |
|---|---|
| 函数 | `_req_links` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L56` |
| 签名 | `_req_links(values: list[str] \| str, prefix: str='')` |
| 参数 | `values`（list[str] \| str）：待处理值集合<br>`prefix`（str）：由 `prefix` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`req_links`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values.split` → `isinstance` → `join` → `_anchor`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | values.split、isinstance、join、_anchor |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-532ec35635"></a>

#### FUN-532EC35635

| 设计项 | 说明 |
|---|---|
| 函数 | `_arch_links` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L61` |
| 签名 | `_arch_links(values: list[str] \| str, prefix: str='')` |
| 参数 | `values`（list[str] \| str）：待处理值集合<br>`prefix`（str）：由 `prefix` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`arch_links`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values.split` → `isinstance` → `join` → `_anchor`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | values.split、isinstance、join、_anchor |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a9d2621b2a"></a>

#### FUN-A9D2621B2A

| 设计项 | 说明 |
|---|---|
| 函数 | `_measure_links` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L66` |
| 签名 | `_measure_links(values: list[str] \| str, prefix: str='')` |
| 参数 | `values`（list[str] \| str）：待处理值集合<br>`prefix`（str）：由 `prefix` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`measure_links`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `values.split` → `isinstance` → `item.startswith` → `rendered.append` → `_anchor` → `join`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | values.split、isinstance、item.startswith、rendered.append、_anchor、join |
| 复杂度 / 风险 | 分支 5；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0aee39f96b"></a>

#### FUN-0AEE39F96B

| 设计项 | 说明 |
|---|---|
| 函数 | `_test_links` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L77` |
| 签名 | `_test_links(value: list[str] \| str, root_prefix: str='../../')` |
| 参数 | `value`（list[str] \| str）：待处理值<br>`root_prefix`（str）：由 `root_prefix` 表示的文本或标识；默认值 `'../../'` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`test_links`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `value.split` → `isinstance` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | value.split、isinstance、join |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-84d7ee0257"></a>

#### FUN-84D7EE0257

| 设计项 | 说明 |
|---|---|
| 函数 | `_table` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L82` |
| 签名 | `_table(headers: list[str], rows: list[list[object]])` |
| 参数 | `headers`（list[str]）：表头或 HTTP 头字段<br>`rows`（list[list[object]]）：记录行集合 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`table`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `lines.extend` → `_cell`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、lines.extend、_cell |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6a04465af3"></a>

#### FUN-6A04465AF3

| 设计项 | 说明 |
|---|---|
| 函数 | `_front` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L91` |
| 签名 | `_front(title: str, process: str, purpose: str)` |
| 参数 | `title`（str）：由 `title` 表示的文本或标识<br>`process`（str）：由 `process` 表示的文本或标识<br>`purpose`（str）：由 `purpose` 表示的文本或标识 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`front`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1839614189"></a>

#### FUN-1839614189

| 设计项 | 说明 |
|---|---|
| 函数 | `_requirements_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L107` |
| 签名 | `_requirements_doc(reqs: dict[str, Any])` |
| 参数 | `reqs`（dict[str, Any]）：由 `reqs` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`requirements_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_front` → `defaultdict` → `_table` → `sorted` → `lower` → `_anchor` → `_arch_links` → `_measure_links`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _front、len、defaultdict、_table、sorted、lower、_anchor、_arch_links、_measure_links、join |
| 复杂度 / 风险 | 分支 2；跨度 42 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c0e8b72578"></a>

#### FUN-C0E8B72578

| 设计项 | 说明 |
|---|---|
| 函数 | `_architecture_diagrams` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L151` |
| 签名 | `_architecture_diagrams()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`architecture_diagrams`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 133 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-73cd1d7b70"></a>

#### FUN-73CD1D7B70

| 设计项 | 说明 |
|---|---|
| 函数 | `_architecture_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L286` |
| 签名 | `_architecture_doc(arch: dict[str, Any], units: list[dict[str, str]])` |
| 参数 | `arch`（dict[str, Any]）：软件架构模型<br>`units`（list[dict[str, str]]）：由 `units` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`architecture_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `defaultdict` → `append` → `_front` → `_table` → `_architecture_diagrams` → `_anchor` → `join` → `enumerate`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | defaultdict、append、_front、_table、len、_architecture_diagrams、_anchor、join、enumerate、_req_links、interface_kind_names.get |
| 复杂度 / 风险 | 分支 5；跨度 65 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cccb5498f5"></a>

#### FUN-CCCB5498F5

| 设计项 | 说明 |
|---|---|
| 函数 | `_design_outputs` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L353` |
| 签名 | `_design_outputs(arch: dict[str, Any], units: list[dict[str, str]], functions: list[dict[str, str]], verification: dict[str, dict[str, str]])` |
| 参数 | `arch`（dict[str, Any]）：软件架构模型<br>`units`（list[dict[str, str]]）：由 `units` 表示的输入集合<br>`functions`（list[dict[str, str]]）：由 `functions` 表示的输入集合<br>`verification`（dict[str, dict[str, str]]）：验证证据或验证配置 |
| 返回 | 返回 `dict[Path, str]` 类型结果 |
| 职责 | 构建`design_outputs`；返回 `dict[Path, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `defaultdict` → `append` → `_front` → `sorted` → `casefold` → `sum` → `component_rows.append` → `_req_links`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[Path, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | defaultdict、append、_front、len、sorted、casefold、sum、component_rows.append、_req_links、_anchor、_table、_measure_links、_unit_section、int、join |
| 复杂度 / 风险 | 分支 4；跨度 91 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4e2eb68af0"></a>

#### FUN-4E2EB68AF0

| 设计项 | 说明 |
|---|---|
| 函数 | `_unit_section` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L446` |
| 签名 | `_unit_section(unit: dict[str, str], functions: list[dict[str, str]], verification: dict[str, str], component_name: str, *, root_prefix: str='../../', aspice_prefix: str='')` |
| 参数 | `unit`（dict[str, str]）：由 `unit` 表示的键值映射<br>`functions`（list[dict[str, str]]）：由 `functions` 表示的输入集合<br>`verification`（dict[str, str]）：验证证据或验证配置<br>`component_name`（str）：对象名称<br>`root_prefix`（str）：由 `root_prefix` 表示的文本或标识；默认值 `'../../'`<br>`aspice_prefix`（str）：由 `aspice_prefix` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`unit_section`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_anchor` → `_table` → `_req_links` → `_measure_links` → `_test_links` → `lines.append` → `join` → `get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _anchor、_table、_req_links、_measure_links、_test_links、lines.append、join、get、replace、_list |
| 复杂度 / 风险 | 分支 4；跨度 85 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-34bbf83058"></a>

#### FUN-34BBF83058

| 设计项 | 说明 |
|---|---|
| 函数 | `_unit_verification_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L533` |
| 签名 | `_unit_verification_doc(arch: dict[str, Any], rows: list[dict[str, str]])` |
| 参数 | `arch`（dict[str, Any]）：软件架构模型<br>`rows`（list[dict[str, str]]）：记录行集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`unit_verification_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `defaultdict` → `append` → `sum` → `_front` → `_table` → `_anchor` → `_measure_links` → `_test_links`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | defaultdict、append、sum、int、_front、len、_table、_anchor、_measure_links、_test_links、sorted、casefold、join |
| 复杂度 / 风险 | 分支 2；跨度 24 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-be2fd65386"></a>

#### FUN-BE2FD65386

| 设计项 | 说明 |
|---|---|
| 函数 | `_integration_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L559` |
| 签名 | `_integration_doc(plan: dict[str, Any], measures: dict[str, Any])` |
| 参数 | `plan`（dict[str, Any]）：由 `plan` 表示的键值映射<br>`measures`（dict[str, Any]）：由 `measures` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`integration_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_front` → `defaultdict` → `append` → `measure_items.setdefault` → `measure_items.items` → `join` → `_anchor` → `enumerate`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _front、defaultdict、append、measure_items.setdefault、measure_items.items、join、_anchor、enumerate、_table、_req_links、_test_links、_measure_links |
| 复杂度 / 风险 | 分支 7；跨度 34 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2336ffb14c"></a>

#### FUN-2336FFB14C

| 设计项 | 说明 |
|---|---|
| 函数 | `_qualification_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L595` |
| 签名 | `_qualification_doc(measures: dict[str, Any], coverage: list[dict[str, str]])` |
| 参数 | `measures`（dict[str, Any]）：由 `measures` 表示的键值映射<br>`coverage`（list[dict[str, str]]）：由 `coverage` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`qualification_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `_front` → `_table` → `policy.items` → `_anchor` → `_req_links` → `_arch_links` → `_measure_links`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、_front、_table、policy.items、_anchor、len、_req_links、_arch_links、_measure_links、join |
| 复杂度 / 风险 | 分支 1；跨度 24 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-009efeb3d5"></a>

#### FUN-009EFEB3D5

| 设计项 | 说明 |
|---|---|
| 函数 | `_configuration_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L621` |
| 签名 | `_configuration_doc(cm: dict[str, Any])` |
| 参数 | `cm`（dict[str, Any]）：由 `cm` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`configuration_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `json.loads` → `read_text` → `sbom.get` → `_front` → `_table` → `items` → `item.get` → `join`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.loads、read_text、sbom.get、_front、_table、items、len、item.get、join |
| 复杂度 / 风险 | 分支 0；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-48fe08d05f"></a>

#### FUN-48FE08D05F

| 设计项 | 说明 |
|---|---|
| 函数 | `_traceability_doc` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L639` |
| 签名 | `_traceability_doc(reqs: dict[str, Any], coverage: list[dict[str, str]])` |
| 参数 | `reqs`（dict[str, Any]）：由 `reqs` 表示的键值映射<br>`coverage`（list[dict[str, str]]）：由 `coverage` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`traceability_doc`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_front` → `_table` → `_req_links` → `_arch_links` → `_measure_links` → `join`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _front、_table、_req_links、_arch_links、_measure_links、join |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a614f5b1a4"></a>

#### FUN-A614F5B1A4

| 设计项 | 说明 |
|---|---|
| 函数 | `expected_outputs` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L649` |
| 签名 | `expected_outputs()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[Path, str]` 类型结果 |
| 职责 | 构建预期生成产物；返回 `dict[Path, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_yaml` → `_csv` → `_design_outputs`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[Path, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _yaml、_csv、_design_outputs |
| 复杂度 / 风险 | 分支 0；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1ea9f2053e"></a>

#### FUN-1EA9F2053E

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/generate_aspice_readable_docs.py](../../../scripts/generate_aspice_readable_docs.py) · `L664` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/generate_aspice_readable_docs.py` 的主流程；可能影响文件系统；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_mutually_exclusive_group` → `mode.add_argument` → `parser.parse_args` → `expected_outputs` → `outputs.items` → `path.parent.mkdir` → `path.write_text`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `int` 类型结果；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_mutually_exclusive_group、mode.add_argument、parser.parse_args、expected_outputs、outputs.items、path.parent.mkdir、path.write_text、path.exists、errors.append、as_posix、path.relative_to、path.read_text、print、join、len |
| 复杂度 / 风险 | 分支 5；跨度 22 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-70ee096332"></a>

### UNIT-70EE096332

**模块**：`scripts/generate_aspice_software_evidence.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-70EE096332 |
| 源码 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/generate_aspice_software_evidence.py` 的职责，通过 `expected_outputs`、`main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 23 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_rel](#fun-39773424a2) · [_stable_id](#fun-dd062cff6e) · [_source_files](#fun-bed0de409d) · [_test_corpus](#fun-86730c4fbc) · [_token_references](#fun-d937d4a0bb) · [_component_for](#fun-c81b19f40e) · [_qualname](#fun-6e9b981dfb) · [_call_name](#fun-97fbbac4cf) · [_argument_nodes](#fun-721b31ee97) · [_argument_purpose](#fun-9031bdaadf) · [_parameter_contract](#fun-20592a303d) · [_precondition_contract](#fun-88961fc4af) · [_postcondition_contract](#fun-addd854580) · [_return_contract](#fun-da094680ba) · [_target_label](#fun-5aa8fa151c) · [_inferred_purpose](#fun-ba8bdd7096) · [_chinese_responsibility](#fun-3857213e2a) · [_algorithm_summary](#fun-825228f28a) · [_node_contract](#fun-df98642acc) · [_risk](#fun-966d638362) · [_csv](#fun-840dd814ad) · [expected_outputs](#fun-6b5f339e4d) · [main](#fun-9c060dbc51)

<a id="fun-39773424a2"></a>

#### FUN-39773424A2

| 设计项 | 说明 |
|---|---|
| 函数 | `_rel` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L41` |
| 签名 | `_rel(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成仓库相对路径文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `as_posix` → `path.relative_to`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | as_posix、path.relative_to |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-dd062cff6e"></a>

#### FUN-DD062CFF6E

| 设计项 | 说明 |
|---|---|
| 函数 | `_stable_id` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L45` |
| 签名 | `_stable_id(prefix: str, value: str)` |
| 参数 | `prefix`（str）：由 `prefix` 表示的文本或标识<br>`value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成稳定标识文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `hexdigest` → `hashlib.sha1` → `value.encode`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、hexdigest、hashlib.sha1、value.encode |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-bed0de409d"></a>

#### FUN-BED0DE409D

| 设计项 | 说明 |
|---|---|
| 函数 | `_source_files` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L50` |
| 签名 | `_source_files()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[Path]` 类型结果 |
| 职责 | 构建受审源码文件清单；返回 `list[Path]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sorted` → `ROOT.rglob` → `any` → `path.relative_to` → `casefold` → `_rel`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[Path]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sorted、ROOT.rglob、any、path.relative_to、casefold、_rel |
| 复杂度 / 风险 | 分支 0；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-86730c4fbc"></a>

#### FUN-86730C4FBC

| 设计项 | 说明 |
|---|---|
| 函数 | `_test_corpus` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L61` |
| 签名 | `_test_corpus()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`test_corpus`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_rel` → `path.read_text` → `sorted` → `rglob` → `casefold`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _rel、path.read_text、sorted、rglob、casefold |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d937d4a0bb"></a>

#### FUN-D937D4A0BB

| 设计项 | 说明 |
|---|---|
| 函数 | `_token_references` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L71` |
| 签名 | `_token_references(token: str, corpus: dict[str, str])` |
| 参数 | `token`（str）：标记或认证令牌<br>`corpus`（dict[str, str]）：由 `corpus` 表示的键值映射 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`token_references`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `re.compile` → `re.escape` → `corpus.items` → `pattern.search`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | re.compile、re.escape、corpus.items、pattern.search |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c81b19f40e"></a>

#### FUN-C81B19F40E

| 设计项 | 说明 |
|---|---|
| 函数 | `_component_for` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L76` |
| 签名 | `_component_for(path: str)` |
| 参数 | `path`（str）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成源码所属架构组件文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `path.startswith`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | path.startswith |
| 复杂度 / 风险 | 分支 3；跨度 17 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6e9b981dfb"></a>

#### FUN-6E9B981DFB

| 设计项 | 说明 |
|---|---|
| 函数 | `_qualname` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L95` |
| 签名 | `_qualname(node: ast.FunctionDef \| ast.AsyncFunctionDef, parents: dict[ast.AST, ast.AST])` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点<br>`parents`（dict[ast.AST, ast.AST]）：由 `parents` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`qualname`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parents.get` → `isinstance` → `owners.append` → `join` → `reversed`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | parents.get、isinstance、owners.append、join、reversed |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-97fbbac4cf"></a>

#### FUN-97FBBAC4CF

| 设计项 | 说明 |
|---|---|
| 函数 | `_call_name` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L105` |
| 签名 | `_call_name(call: ast.Call)` |
| 参数 | `call`（ast.Call）：由调用方提供的 `call` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`call_name`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `parts.append` → `join` → `reversed`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、parts.append、join、reversed |
| 复杂度 / 风险 | 分支 2；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-721b31ee97"></a>

#### FUN-721B31EE97

| 设计项 | 说明 |
|---|---|
| 函数 | `_argument_nodes` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L212` |
| 签名 | `_argument_nodes(node: ast.FunctionDef \| ast.AsyncFunctionDef)` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点 |
| 返回 | 返回 `list[ast.arg]` 类型结果 |
| 职责 | 构建`argument_nodes`；返回 `list[ast.arg]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[ast.arg]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9031bdaadf"></a>

#### FUN-9031BDAADF

| 设计项 | 说明 |
|---|---|
| 函数 | `_argument_purpose` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L216` |
| 签名 | `_argument_purpose(name: str, annotation: str)` |
| 参数 | `name`（str）：对象名称<br>`annotation`（str）：由 `annotation` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`argument_purpose`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `name.split` → `name.endswith` → `name.startswith` → `any`；包含 14 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | name.split、name.endswith、name.startswith、any |
| 复杂度 / 风险 | 分支 14；跨度 31 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-20592a303d"></a>

#### FUN-20592A303D

| 设计项 | 说明 |
|---|---|
| 函数 | `_parameter_contract` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L249` |
| 签名 | `_parameter_contract(node: ast.FunctionDef \| ast.AsyncFunctionDef)` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`parameter_contract`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `zip` → `defaults.update` → `_argument_nodes` → `ast.unparse` → `_argument_purpose` → `parts.append` → `join`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | zip、len、defaults.update、_argument_nodes、ast.unparse、_argument_purpose、parts.append、join |
| 复杂度 / 风险 | 分支 7；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-88961fc4af"></a>

#### FUN-88961FC4AF

| 设计项 | 说明 |
|---|---|
| 函数 | `_precondition_contract` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L273` |
| 签名 | `_precondition_contract(parameter_contract: str, effects: list[str])` |
| 参数 | `parameter_contract`（str）：由 `parameter_contract` 表示的文本或标识<br>`effects`（list[str]）：由 `effects` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`precondition_contract`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `clauses.insert` → `clauses.append` → `join`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | clauses.insert、clauses.append、join |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-addd854580"></a>

#### FUN-ADDD854580

| 设计项 | 说明 |
|---|---|
| 函数 | `_postcondition_contract` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L286` |
| 签名 | `_postcondition_contract(return_contract: str, effects: list[str])` |
| 参数 | `return_contract`（str）：由 `return_contract` 表示的文本或标识<br>`effects`（list[str]）：由 `effects` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`postcondition_contract`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `clauses.append` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | clauses.append、join |
| 复杂度 / 风险 | 分支 1；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-da094680ba"></a>

#### FUN-DA094680BA

| 设计项 | 说明 |
|---|---|
| 函数 | `_return_contract` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L296` |
| 签名 | `_return_contract(node: ast.FunctionDef \| ast.AsyncFunctionDef)` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`return_contract`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ast.unparse` → `any` → `isinstance` → `ast.walk`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ast.unparse、any、isinstance、ast.walk |
| 复杂度 / 风险 | 分支 3；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5aa8fa151c"></a>

#### FUN-5AA8FA151C

| 设计项 | 说明 |
|---|---|
| 函数 | `_target_label` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L304` |
| 签名 | `_target_label(tokens: list[str])` |
| 参数 | `tokens`（list[str]）：由 `tokens` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`target_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `TARGET_LABELS.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、TARGET_LABELS.get |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ba8bdd7096"></a>

#### FUN-BA8BDD7096

| 设计项 | 说明 |
|---|---|
| 函数 | `_inferred_purpose` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L309` |
| 签名 | `_inferred_purpose(node: ast.FunctionDef \| ast.AsyncFunctionDef, return_contract: str, source_path: str)` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点<br>`return_contract`（str）：由 `return_contract` 表示的文本或标识<br>`source_path`（str）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`inferred_purpose`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `node.name.strip` → `re.split` → `tokens.index` → `_target_label` → `any` → `next` → `enumerate` → `token.lower`；包含 16 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | node.name.strip、re.split、tokens.index、_target_label、any、next、enumerate、token.lower、lower、ACTION_ONLY_TARGETS.get、return_contract.startswith |
| 复杂度 / 风险 | 分支 16；跨度 41 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3857213e2a"></a>

#### FUN-3857213E2A

| 设计项 | 说明 |
|---|---|
| 函数 | `_chinese_responsibility` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L352` |
| 签名 | `_chinese_responsibility(node: ast.FunctionDef \| ast.AsyncFunctionDef, calls: list[str], effects: list[str], return_contract: str, source_path: str)` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点<br>`calls`（list[str]）：由 `calls` 表示的输入集合<br>`effects`（list[str]）：由 `effects` 表示的输入集合<br>`return_contract`（str）：由 `return_contract` 表示的文本或标识<br>`source_path`（str）：文件或目录路径 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`chinese_responsibility`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ast.get_docstring` → `rstrip` → `doc.splitlines` → `re.match` → `_inferred_purpose` → `details.append` → `join`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ast.get_docstring、rstrip、doc.splitlines、re.match、_inferred_purpose、details.append、join |
| 复杂度 / 风险 | 分支 3；跨度 19 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-825228f28a"></a>

#### FUN-825228F28A

| 设计项 | 说明 |
|---|---|
| 函数 | `_algorithm_summary` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L373` |
| 签名 | `_algorithm_summary(calls: list[str], branches: int)` |
| 参数 | `calls`（list[str]）：由 `calls` 表示的输入集合<br>`branches`（int）：由 `branches` 表示的数值参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`algorithm_summary`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join |
| 复杂度 / 风险 | 分支 2；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-df98642acc"></a>

#### FUN-DF98642ACC

| 设计项 | 说明 |
|---|---|
| 函数 | `_node_contract` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L388` |
| 签名 | `_node_contract(node: ast.FunctionDef \| ast.AsyncFunctionDef, source_path: str)` |
| 参数 | `node`（ast.FunctionDef \| ast.AsyncFunctionDef）：AST 或结构节点<br>`source_path`（str）：文件或目录路径 |
| 返回 | 返回 `dict[str, str \| int]` 类型结果 |
| 职责 | 构建`node_contract`；返回 `dict[str, str \| int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ast.unparse` → `_return_contract` → `sorted` → `ast.walk` → `isinstance` → `getattr` → `dict.fromkeys` → `_call_name`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str \| int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ast.unparse、_return_contract、sorted、ast.walk、isinstance、getattr、list、dict.fromkeys、_call_name、sum、lower、join、re.search、effects.append、any、_chinese_responsibility、max、_parameter_contract、_algorithm_summary、_precondition_contract |
| 复杂度 / 风险 | 分支 7；跨度 50 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-966d638362"></a>

#### FUN-966D638362

| 设计项 | 说明 |
|---|---|
| 函数 | `_risk` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L440` |
| 签名 | `_risk(path: str, name: str, contract: dict[str, str \| int])` |
| 参数 | `path`（str）：文件或目录路径<br>`name`（str）：对象名称<br>`contract`（dict[str, str \| int]）：由 `contract` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成风险结果文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `re.search` → `startswith` → `name.split`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | re.search、str、int、startswith、name.split |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-840dd814ad"></a>

#### FUN-840DD814AD

| 设计项 | 说明 |
|---|---|
| 函数 | `_csv` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L450` |
| 签名 | `_csv(rows: list[dict[str, object]])` |
| 参数 | `rows`（list[dict[str, object]]）：记录行集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成CSV 数据文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `io.StringIO` → `csv.DictWriter` → `writer.writeheader` → `writer.writerows` → `buffer.getvalue`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | io.StringIO、csv.DictWriter、list、writer.writeheader、writer.writerows、buffer.getvalue |
| 复杂度 / 风险 | 分支 0；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6b5f339e4d"></a>

#### FUN-6B5F339E4D

| 设计项 | 说明 |
|---|---|
| 函数 | `expected_outputs` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L458` |
| 签名 | `expected_outputs()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[dict[Path, str], dict[str, int]]` 类型结果 |
| 职责 | 构建预期生成产物；返回 `tuple[dict[Path, str], dict[str, int]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `yaml.safe_load` → `ARCH_PATH.read_text` → `REQ_PATH.read_text` → `RESULT_PATH.read_text` → `_test_corpus` → `defaultdict` → `_source_files` → `_rel`；包含 18 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[Path, str], dict[str, int]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | yaml.safe_load、ARCH_PATH.read_text、REQ_PATH.read_text、RESULT_PATH.read_text、_test_corpus、defaultdict、_source_files、_rel、_stable_id、_component_for、ast.parse、source.read_text、ast.walk、ast.iter_child_nodes、replace、path.removesuffix、update、_token_references、isinstance、_qualname |
| 复杂度 / 风险 | 分支 18；跨度 141 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9c060dbc51"></a>

#### FUN-9C060DBC51

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/generate_aspice_software_evidence.py](../../../scripts/generate_aspice_software_evidence.py) · `L601` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/generate_aspice_software_evidence.py` 的主流程；可能影响文件系统；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_mutually_exclusive_group` → `mode.add_argument` → `parser.parse_args` → `expected_outputs` → `outputs.items` → `path.write_text` → `path.exists`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `int` 类型结果；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_mutually_exclusive_group、mode.add_argument、parser.parse_args、expected_outputs、outputs.items、path.write_text、path.exists、errors.append、_rel、path.read_text、print、join |
| 复杂度 / 风险 | 分支 7；跨度 26 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-37e036c51b"></a>

### UNIT-37E036C51B

**模块**：`scripts/inspect_archive.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-37E036C51B |
| 源码 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/inspect_archive.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_cmd_list](#fun-000d721083) · [_cmd_inspect](#fun-747a7a71ca) · [_cmd_validate](#fun-63ae1e91d4) · [_cmd_export](#fun-e505b92782) · [_cmd_import](#fun-ca79779a11) · [main](#fun-80a2a844ca)

<a id="fun-000d721083"></a>

#### FUN-000D721083

| 设计项 | 说明 |
|---|---|
| 函数 | `_cmd_list` |
| 源码位置 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) · `L16` |
| 签名 | `_cmd_list(args: argparse.Namespace)` |
| 参数 | `args`（argparse.Namespace）：由调用方提供的 `args` 输入对象 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`cmd_list`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `list_archives` → `print` → `archive_label`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list_archives、print、archive_label |
| 复杂度 / 风险 | 分支 2；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-747a7a71ca"></a>

#### FUN-747A7A71CA

| 设计项 | 说明 |
|---|---|
| 函数 | `_cmd_inspect` |
| 源码位置 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) · `L28` |
| 签名 | `_cmd_inspect(args: argparse.Namespace)` |
| 参数 | `args`（argparse.Namespace）：由调用方提供的 `args` 输入对象 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`cmd_inspect`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `inspect_run_archive` → `print` → `json.dumps`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | inspect_run_archive、print、json.dumps |
| 复杂度 / 风险 | 分支 1；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-63ae1e91d4"></a>

#### FUN-63AE1E91D4

| 设计项 | 说明 |
|---|---|
| 函数 | `_cmd_validate` |
| 源码位置 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) · `L44` |
| 签名 | `_cmd_validate(args: argparse.Namespace)` |
| 参数 | `args`（argparse.Namespace）：由调用方提供的 `args` 输入对象 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 验证`cmd`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `normalized` → `RunConfig` → `load_replay_bundle` → `print` → `json.dumps` → `get` → `report.get` → `sorted`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | normalized、RunConfig、load_replay_bundle、print、json.dumps、get、report.get、sorted、enriched.keys、analyses.keys、bool |
| 复杂度 / 风险 | 分支 0；跨度 21 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e505b92782"></a>

#### FUN-E505B92782

| 设计项 | 说明 |
|---|---|
| 函数 | `_cmd_export` |
| 源码位置 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) · `L67` |
| 签名 | `_cmd_export(args: argparse.Namespace)` |
| 参数 | `args`（argparse.Namespace）：由调用方提供的 `args` 输入对象 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 导出`cmd`；可能影响文件系统；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `export_archive_zip` → `Path` → `out.write_bytes` → `print`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `int` 类型结果；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | export_archive_zip、Path、out.write_bytes、print、len |
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ca79779a11"></a>

#### FUN-CA79779A11

| 设计项 | 说明 |
|---|---|
| 函数 | `_cmd_import` |
| 源码位置 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) · `L77` |
| 签名 | `_cmd_import(args: argparse.Namespace)` |
| 参数 | `args`（argparse.Namespace）：由调用方提供的 `args` 输入对象 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 导入`cmd`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `read_bytes` → `Path` → `import_archive_zip` → `print`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | read_bytes、Path、import_archive_zip、print |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-80a2a844ca"></a>

#### FUN-80A2A844CA

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/inspect_archive.py](../../../scripts/inspect_archive.py) · `L86` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/inspect_archive.py` 的主流程；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_subparsers` → `sub.add_parser` → `list_p.add_argument` → `list_p.set_defaults` → `inspect_p.add_argument` → `inspect_p.set_defaults` → `validate_p.add_argument`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_subparsers、sub.add_parser、list_p.add_argument、list_p.set_defaults、inspect_p.add_argument、inspect_p.set_defaults、validate_p.add_argument、validate_p.set_defaults、export_p.add_argument、export_p.set_defaults、import_p.add_argument、import_p.set_defaults、parser.parse_args、args.func |
| 复杂度 / 风险 | 分支 0；跨度 29 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-ebde8e6443"></a>

### UNIT-EBDE8E6443

**模块**：`scripts/regression_test.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EBDE8E6443 |
| 源码 | [scripts/regression_test.py](../../../scripts/regression_test.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/regression_test.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3960e281ab"></a>

### UNIT-3960E281AB

**模块**：`scripts/replay_llm_narrative.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3960E281AB |
| 源码 | [scripts/replay_llm_narrative.py](../../../scripts/replay_llm_narrative.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/replay_llm_narrative.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py)、[tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py) |
| 验证状态 | selected |

#### 函数导航

[_load_json](#fun-2a9ad18e99) · [_load_llm_payload](#fun-0b702bf5f4) · [_print_audit](#fun-89b0c24609) · [main](#fun-06a7e09133)

<a id="fun-2a9ad18e99"></a>

#### FUN-2A9AD18E99

| 设计项 | 说明 |
|---|---|
| 函数 | `_load_json` |
| 源码位置 | [scripts/replay_llm_narrative.py](../../../scripts/replay_llm_narrative.py) · `L18` |
| 签名 | `_load_json(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 加载JSON 数据；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `json.loads` → `path.read_text`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.loads、path.read_text |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0b702bf5f4"></a>

#### FUN-0B702BF5F4

| 设计项 | 说明 |
|---|---|
| 函数 | `_load_llm_payload` |
| 源码位置 | [scripts/replay_llm_narrative.py](../../../scripts/replay_llm_narrative.py) · `L22` |
| 签名 | `_load_llm_payload(report: dict, llm_path: Path \| None)` |
| 参数 | `report`（dict）：分析报告<br>`llm_path`（Path \| None）：文件或目录路径 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 加载LLM 阶段载荷；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_load_json` → `isinstance` → `SystemExit` → `report.get` → `llm.get` → `json.loads`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | SystemExit |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _load_json、isinstance、SystemExit、report.get、llm.get、json.loads |
| 复杂度 / 风险 | 分支 3；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-89b0c24609"></a>

#### FUN-89B0C24609

| 设计项 | 说明 |
|---|---|
| 函数 | `_print_audit` |
| 源码位置 | [scripts/replay_llm_narrative.py](../../../scripts/replay_llm_narrative.py) · `L37` |
| 签名 | `_print_audit(result)` |
| 参数 | `result`（实现约定类型）：处理结果 |
| 返回 | 无返回值（None） |
| 职责 | 执行`print_audit`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `print` → `get` → `section.get` → `audit.get` → `top.get` → `items` → `sum`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | print、get、section.get、audit.get、top.get、items、sum、len |
| 复杂度 / 风险 | 分支 6；跨度 27 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-06a7e09133"></a>

#### FUN-06A7E09133

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/replay_llm_narrative.py](../../../scripts/replay_llm_narrative.py) · `L66` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行 `scripts/replay_llm_narrative.py` 的主流程；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_argument` → `parser.parse_args` → `_load_json` → `report.get` → `build_rule_narrative_sections` → `_load_llm_payload` → `validate_llm_payload`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_argument、parser.parse_args、_load_json、report.get、build_rule_narrative_sections、_load_llm_payload、validate_llm_payload、_print_audit、apply_llm_to_report、print |
| 复杂度 / 风险 | 分支 2；跨度 32 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-d538889607"></a>

### UNIT-D538889607

**模块**：`scripts/run_pipeline_test.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D538889607 |
| 源码 | [scripts/run_pipeline_test.py](../../../scripts/run_pipeline_test.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/run_pipeline_test.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-8f71f01664"></a>

### UNIT-8F71F01664

**模块**：`scripts/show_utf8.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8F71F01664 |
| 源码 | [scripts/show_utf8.py](../../../scripts/show_utf8.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/show_utf8.py` 的职责，通过 `parse_args`、`main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[parse_args](#fun-fdec2f3b6b) · [main](#fun-9302f1289e)

<a id="fun-fdec2f3b6b"></a>

#### FUN-FDEC2F3B6B

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_args` |
| 源码位置 | [scripts/show_utf8.py](../../../scripts/show_utf8.py) · `L16` |
| 签名 | `parse_args()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `argparse.Namespace` 类型结果 |
| 职责 | 解析命令行参数；返回 `argparse.Namespace` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_argument` → `parser.parse_args`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `argparse.Namespace` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_argument、parser.parse_args |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9302f1289e"></a>

#### FUN-9302F1289E

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/show_utf8.py](../../../scripts/show_utf8.py) · `L24` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/show_utf8.py` 的主流程；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sys.stdout.reconfigure` → `parse_args` → `Path` → `path.read_text` → `text.splitlines` → `max` → `min` → `range`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sys.stdout.reconfigure、parse_args、Path、path.read_text、text.splitlines、max、min、len、range、print |
| 复杂度 / 风险 | 分支 1；跨度 11 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-c913c2495c"></a>

### UNIT-C913C2495C

**模块**：`scripts/test_live_fetch.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C913C2495C |
| 源码 | [scripts/test_live_fetch.py](../../../scripts/test_live_fetch.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/test_live_fetch.py` 的职责，通过 `main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [main](#fun-9c22b2b4e5) | 执行 `scripts/test_live_fetch.py` 的主流程；可能影响外部接口；返回 `int` 类型结果。 | 外部接口 I/O | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |

#### 函数导航

[_block](#fun-2e85c86a01) · [main](#fun-9c22b2b4e5)

<a id="fun-2e85c86a01"></a>

#### FUN-2E85C86A01

| 设计项 | 说明 |
|---|---|
| 函数 | `_block` |
| 源码位置 | [scripts/test_live_fetch.py](../../../scripts/test_live_fetch.py) · `L20` |
| 签名 | `_block(title: str, body: object)` |
| 参数 | `title`（str）：由 `title` 表示的文本或标识<br>`body`（object）：由调用方提供的 `body` 输入对象 |
| 返回 | 无返回值（None） |
| 职责 | 执行`block`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `print` → `isinstance` → `json.dumps`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | print、isinstance、json.dumps |
| 复杂度 / 风险 | 分支 1；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9c22b2b4e5"></a>

#### FUN-9C22B2B4E5

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [scripts/test_live_fetch.py](../../../scripts/test_live_fetch.py) · `L30` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `scripts/test_live_fetch.py` 的主流程；可能影响外部接口；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `print` → `fetch_dxy_impact` → `_block` → `fetch_jin10_bundle` → `fetch_jin10_quote` → `fetch_jin10_kline` → `fetch_social_sentiment` → `merge_external`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `int` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | print、fetch_dxy_impact、_block、fetch_jin10_bundle、len、fetch_jin10_quote、fetch_jin10_kline、fetch_social_sentiment、merge_external、fetch_external、NewsDataSource、FundamentalsDataSource、SocialDataSource、sum、dxy_refs.get、bool、social_refs.get |
| 复杂度 / 风险 | 分支 1；跨度 72 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-76c5f6645c"></a>

### UNIT-76C5F6645C

**模块**：`scripts/test_llm_json_fix.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-76C5F6645C |
| 源码 | [scripts/test_llm_json_fix.py](../../../scripts/test_llm_json_fix.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | 实现“开发、审核与运维工具”组件中 `scripts/test_llm_json_fix.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-NFR-003](../SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](../SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。
