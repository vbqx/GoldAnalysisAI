# ARC-VIZ — Human-review presentation

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-viz)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/viz/__init__.py](#unit-3ec85337ca) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/advice_view.py](#unit-2e19dca37c) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/external_data_view.py](#unit-8b3827f5ec) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/generation_state.py](#unit-e27519993b) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/generation_worker.py](#unit-4c9db5733a) | 16 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/llm_process_view.py](#unit-4756f86a84) | 6 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/page_layout.py](#unit-d8ab5e90b4) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/pipeline_progress.py](#unit-87ec9bc982) | 20 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/replay_loader.py](#unit-a63d87a7bb) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/run_config_panel.py](#unit-ee18de86b2) | 9 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/session_keys.py](#unit-6fa4e87f8a) | 5 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/streamlit_common.py](#unit-202db41fe0) | 20 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |

<a id="unit-3ec85337ca"></a>

### UNIT-3EC85337CA

**模块**：`src/viz/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3EC85337CA |
| 源码 | [src/viz/__init__.py](../../../src/viz/__init__.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-2e19dca37c"></a>

### UNIT-2E19DCA37C

**模块**：`src/viz/advice_view.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2E19DCA37C |
| 源码 | [src/viz/advice_view.py](../../../src/viz/advice_view.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/advice_view.py` 的职责，通过 `render_advice_report` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[_list](#fun-c4deaf62cb) · [render_advice_report](#fun-26e9639f08)

<a id="fun-c4deaf62cb"></a>

#### FUN-C4DEAF62CB

| 设计项 | 说明 |
|---|---|
| 函数 | `_list` |
| 源码位置 | [src/viz/advice_view.py](../../../src/viz/advice_view.py) · `L39` |
| 签名 | `_list(items: list[Any], *, css: str='bullet-list')` |
| 参数 | `items`（list[Any]）：输入项集合<br>`css`（str）：由 `css` 表示的文本或标识；默认值 `'bullet-list'` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`list`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `html.escape`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、html.escape、str |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-26e9639f08"></a>

#### FUN-26E9639F08

| 设计项 | 说明 |
|---|---|
| 函数 | `render_advice_report` |
| 源码位置 | [src/viz/advice_view.py](../../../src/viz/advice_view.py) · `L43` |
| 签名 | `render_advice_report(report: dict[str, Any], data: dict, analyses: dict)` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`data`（dict）：输入数据<br>`analyses`（dict）：各时间框架分析结果 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`advice_report`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `advice.get` → `get` → `_BIAS_CN.get` → `_CONFIDENCE_CN.get` → `_DECISION_CN.get` → `html.escape` → `st.markdown`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、str、advice.get、get、_BIAS_CN.get、_CONFIDENCE_CN.get、_DECISION_CN.get、html.escape、float、st.markdown、isinstance、setup.get、zone.get、st.columns、_list、list、join、st.info、alt.get、st.expander |
| 复杂度 / 风险 | 分支 4；跨度 95 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-8b3827f5ec"></a>

### UNIT-8B3827F5EC

**模块**：`src/viz/external_data_view.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8B3827F5EC |
| 源码 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/external_data_view.py` 的职责，通过 `external_snapshot_from_fetch`、`external_payload_from_report`、`render_external_data_content`、`render_external_data_page` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |
| 验证状态 | selected |

#### 函数导航

[_source_tags](#fun-0a1b4eddd8) · [external_snapshot_from_fetch](#fun-1e2febd33e) · [external_payload_from_report](#fun-73c9145028) · [_render_headline_list](#fun-75474c9286) · [_render_calendar_rows](#fun-15a26b9540) · [render_external_data_content](#fun-6cdbb0b77d) · [render_external_data_page](#fun-6b50c51729)

<a id="fun-0a1b4eddd8"></a>

#### FUN-0A1B4EDDD8

| 设计项 | 说明 |
|---|---|
| 函数 | `_source_tags` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L14` |
| 签名 | `_source_tags(sources: list[str])` |
| 参数 | `sources`（list[str]）：由 `sources` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`source_tags`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `html.escape`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、html.escape、str |
| 复杂度 / 风险 | 分支 0；跨度 6 行；低 |
| 测试 / 验证 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py) · 直接动态测试 |

<a id="fun-1e2febd33e"></a>

#### FUN-1E2FEBD33E

| 设计项 | 说明 |
|---|---|
| 函数 | `external_snapshot_from_fetch` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L22` |
| 签名 | `external_snapshot_from_fetch(fetched: DataFetchResult)` |
| 参数 | `fetched`（DataFetchResult）：数据获取结果 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 根据`fetch`构建`external_snapshot`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `event.to_dict` → `h.to_dict` → `m.to_dict`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | event.to_dict、list、h.to_dict、m.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 20 行；中 |
| 测试 / 验证 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="fun-73c9145028"></a>

#### FUN-73C9145028

| 设计项 | 说明 |
|---|---|
| 函数 | `external_payload_from_report` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L44` |
| 签名 | `external_payload_from_report(report: dict, data: dict \| None=None)` |
| 参数 | `report`（dict）：分析报告<br>`data`（dict \| None）：输入数据；默认值 `None` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 根据报告构建`external_payload`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `ext.get` → `data.items` → `ext.setdefault` → `get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | dict、report.get、list、ext.get、len、data.items、ext.setdefault、get |
| 复杂度 / 风险 | 分支 2；跨度 14 行；中 |
| 测试 / 验证 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py) · 直接动态测试 |

<a id="fun-75474c9286"></a>

#### FUN-75474C9286

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_headline_list` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L60` |
| 签名 | `_render_headline_list(items: list[dict], *, empty: str)` |
| 参数 | `items`（list[dict]）：输入项集合<br>`empty`（str）：由 `empty` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`headline_list`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `html.escape` → `h.get` → `rows.append` → `join`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | html.escape、str、h.get、rows.append、join |
| 复杂度 / 风险 | 分支 4；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-15a26b9540"></a>

#### FUN-15A26B9540

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_calendar_rows` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L74` |
| 签名 | `_render_calendar_rows(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`calendar_rows`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `payload.get` → `join` → `html.escape` → `e.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | payload.get、join、html.escape、str、e.get |
| 复杂度 / 风险 | 分支 4；跨度 17 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6cdbb0b77d"></a>

#### FUN-6CDBB0B77D

| 设计项 | 说明 |
|---|---|
| 函数 | `render_external_data_content` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L93` |
| 签名 | `render_external_data_content(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`external_data_content`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `payload.get` → `_source_tags` → `isinstance` → `_render_headline_list` → `join` → `html.escape` → `_render_calendar_rows` → `p.get`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | payload.get、_source_tags、isinstance、_render_headline_list、join、html.escape、str、_render_calendar_rows、p.get、sorted、bars.items、m.get、derived_bits.append、st.markdown |
| 复杂度 / 风险 | 分支 11；跨度 94 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6b50c51729"></a>

#### FUN-6B50C51729

| 设计项 | 说明 |
|---|---|
| 函数 | `render_external_data_page` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L189` |
| 签名 | `render_external_data_page(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`external_data_page`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `payload.get` → `render_page_hero` → `render_external_data_content`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | payload.get、render_page_hero、render_external_data_content |
| 复杂度 / 风险 | 分支 1；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-e27519993b"></a>

### UNIT-E27519993B

**模块**：`src/viz/generation_state.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E27519993B |
| 源码 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/generation_state.py` 的职责，通过 `GenerationJob`、`purge_expired`、`access_job`、`get_job`、`create_job`、`drop_job`、`update_live` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[GenerationJob.key](#fun-91dd83b0a6) · [purge_expired](#fun-a28f3ce7db) · [access_job](#fun-fab2a1bb76) · [get_job](#fun-bcb1df87b1) · [create_job](#fun-e4ee868b95) · [drop_job](#fun-0d53c85f3b) · [update_live](#fun-5614348eb6)

<a id="fun-91dd83b0a6"></a>

#### FUN-91DD83B0A6

| 设计项 | 说明 |
|---|---|
| 函数 | `GenerationJob.key` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L24` |
| 签名 | `GenerationJob.key(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`key`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

<a id="fun-a28f3ce7db"></a>

#### FUN-A28F3CE7DB

| 设计项 | 说明 |
|---|---|
| 函数 | `purge_expired` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L32` |
| 签名 | `purge_expired()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`purge_expired`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `time.monotonic` → `_STORE.items` → `_STORE.pop`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | time.monotonic、_STORE.items、_STORE.pop |
| 复杂度 / 风险 | 分支 1；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fab2a1bb76"></a>

#### FUN-FAB2A1BB76

| 设计项 | 说明 |
|---|---|
| 函数 | `access_job` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L40` |
| 签名 | `access_job(job_key: str)` |
| 参数 | `job_key`（str）：索引键 |
| 返回 | 返回 `GenerationJob \| None` 类型结果 |
| 职责 | 生成`access_job`结果；返回 `GenerationJob \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `purge_expired` → `_STORE.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `GenerationJob \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | purge_expired、_STORE.get |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-bcb1df87b1"></a>

#### FUN-BCB1DF87B1

| 设计项 | 说明 |
|---|---|
| 函数 | `get_job` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L46` |
| 签名 | `get_job(job_key: str, *, session_id: str)` |
| 参数 | `job_key`（str）：索引键<br>`session_id`（str）：对象标识 |
| 返回 | 返回 `GenerationJob \| None` 类型结果 |
| 职责 | 获取`job`；返回 `GenerationJob \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `purge_expired` → `_STORE.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `GenerationJob \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | purge_expired、_STORE.get |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-e4ee868b95"></a>

#### FUN-E4EE868B95

| 设计项 | 说明 |
|---|---|
| 函数 | `create_job` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L55` |
| 签名 | `create_job(session_id: str, generation_id: str)` |
| 参数 | `session_id`（str）：对象标识<br>`generation_id`（str）：对象标识 |
| 返回 | 返回 `GenerationJob` 类型结果 |
| 职责 | 创建`job`；返回 `GenerationJob` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `purge_expired` → `GenerationJob`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `GenerationJob` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | purge_expired、GenerationJob |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-0d53c85f3b"></a>

#### FUN-0D53C85F3B

| 设计项 | 说明 |
|---|---|
| 函数 | `drop_job` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L63` |
| 签名 | `drop_job(job_key: str, *, session_id: str)` |
| 参数 | `job_key`（str）：索引键<br>`session_id`（str）：对象标识 |
| 返回 | 无返回值（None） |
| 职责 | 执行`drop_job`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_STORE.get` → `_STORE.pop`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _STORE.get、_STORE.pop |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5614348eb6"></a>

#### FUN-5614348EB6

| 设计项 | 说明 |
|---|---|
| 函数 | `update_live` |
| 源码位置 | [src/viz/generation_state.py](../../../src/viz/generation_state.py) · `L70` |
| 签名 | `update_live(job_key: str, snapshot: dict[str, Any])` |
| 参数 | `job_key`（str）：索引键<br>`snapshot`（dict[str, Any]）：由 `snapshot` 表示的键值映射 |
| 返回 | 无返回值（None） |
| 职责 | 更新`live`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_STORE.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _STORE.get |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py) · 直接动态测试 |

<a id="unit-4c9db5733a"></a>

### UNIT-4C9DB5733A

**模块**：`src/viz/generation_worker.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4C9DB5733A |
| 源码 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/generation_worker.py` 的职责，通过 `compact_llm_io_for_live`、`ModuleSyncProgressReporter`、`format_generation_error`、`start_generation` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 16 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[_is_streaming_llm_record](#fun-2029e693a6) · [compact_llm_io_for_live](#fun-52fe00a287) · [ModuleSyncProgressReporter.__init__](#fun-2fae0caf3c) · [ModuleSyncProgressReporter._sync](#fun-309bcf8879) · [ModuleSyncProgressReporter._headline_from_steps](#fun-a85c4e4bb0) · [ModuleSyncProgressReporter._on_change](#fun-16cab352ce) · [ModuleSyncProgressReporter._on_llm_chunk](#fun-db5d7a17a9) · [ModuleSyncProgressReporter.llm_begin](#fun-328cc0f106) · [ModuleSyncProgressReporter.llm_end](#fun-b1681a5a0b) · [ModuleSyncProgressReporter.fail](#fun-40bbcb7294) · [ModuleSyncProgressReporter.done](#fun-00ca768fe8) · [ModuleSyncProgressReporter.update](#fun-f475f6a25b) · [ModuleSyncProgressReporter.stage_io](#fun-b77c2c5b77) · [format_generation_error](#fun-4adbbae6f8) · [start_generation](#fun-de0806140c) · [start_generation.worker](#fun-eadc84cc44)

<a id="fun-2029e693a6"></a>

#### FUN-2029E693A6

| 设计项 | 说明 |
|---|---|
| 函数 | `_is_streaming_llm_record` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L24` |
| 签名 | `_is_streaming_llm_record(rec: dict)` |
| 参数 | `rec`（dict）：由 `rec` 表示的键值映射 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断流式 LLM 调用记录；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rec.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rec.get |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-52fe00a287"></a>

#### FUN-52FE00A287

| 设计项 | 说明 |
|---|---|
| 函数 | `compact_llm_io_for_live` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L32` |
| 签名 | `compact_llm_io_for_live(records: list[dict])` |
| 参数 | `records`（list[dict]）：结构化记录集合 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 构建`compact_llm_io_for_live`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_is_streaming_llm_record` → `rec.get` → `msg.get` → `trimmed_msgs.append` → `compacted.append`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _is_streaming_llm_record、rec.get、len、str、msg.get、trimmed_msgs.append、compacted.append |
| 复杂度 / 风险 | 分支 5；跨度 39 行；中 |
| 测试 / 验证 | [tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py) · 直接动态测试 |

<a id="fun-2fae0caf3c"></a>

#### FUN-2FAE0CAF3C

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.__init__` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L76` |
| 签名 | `ModuleSyncProgressReporter.__init__(self, job_key: str)` |
| 参数 | `job_key`（str）：索引键 |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `__init__` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | __init__、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-309bcf8879"></a>

#### FUN-309BCF8879

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter._sync` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L82` |
| 签名 | `ModuleSyncProgressReporter._sync(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`sync`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `access_job` → `prev.get` → `self.snapshot` → `compact_llm_io_for_live` → `self.llm_io_snapshot` → `self._headline_from_steps` → `update_live`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | access_job、prev.get、self.snapshot、compact_llm_io_for_live、self.llm_io_snapshot、self._headline_from_steps、update_live |
| 复杂度 / 风险 | 分支 1；跨度 15 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a85c4e4bb0"></a>

#### FUN-A85C4E4BB0

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter._headline_from_steps` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L99` |
| 签名 | `ModuleSyncProgressReporter._headline_from_steps(steps: list[dict])` |
| 参数 | `steps`（list[dict]）：执行步骤集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 根据`steps`构建`headline`；可能影响共享状态；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pipeline_progress_headline`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pipeline_progress_headline |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-16cab352ce"></a>

#### FUN-16CAB352CE

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter._on_change` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L104` |
| 签名 | `ModuleSyncProgressReporter._on_change(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_change`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._sync`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._sync |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-db5d7a17a9"></a>

#### FUN-DB5D7A17A9

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter._on_llm_chunk` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L107` |
| 签名 | `ModuleSyncProgressReporter._on_llm_chunk(self, stage: str, chunk: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`chunk`（str）：由 `chunk` 表示的文本或标识 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_llm_chunk`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_on_llm_chunk` → `super` → `time.monotonic` → `self._sync`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _on_llm_chunk、super、time.monotonic、self._sync |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | [tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-328cc0f106"></a>

#### FUN-328CC0F106

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.llm_begin` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L114` |
| 签名 | `ModuleSyncProgressReporter.llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], *, telemetry: dict \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`model`（str）：模型名称或模型对象<br>`messages`（list[dict[str, str]]）：消息序列<br>`telemetry`（dict \| None）：遥测记录；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`llm_begin`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `llm_begin` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm_begin、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 10 行；中 |
| 测试 / 验证 | [tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-b1681a5a0b"></a>

#### FUN-B1681A5A0B

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.llm_end` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L125` |
| 签名 | `ModuleSyncProgressReporter.llm_end(self, stage: str, output: str, *, error: str \| None=None, latency_ms: int \| None=None, telemetry: dict \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`output`（str）：输出对象或输出路径<br>`error`（str \| None）：错误信息或异常对象；默认值 `None`<br>`latency_ms`（int \| None）：延迟毫秒数；默认值 `None`<br>`telemetry`（dict \| None）：遥测记录；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`llm_end`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `llm_end` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm_end、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 11 行；中 |
| 测试 / 验证 | [tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="fun-40bbcb7294"></a>

#### FUN-40BBCB7294

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.fail` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L137` |
| 签名 | `ModuleSyncProgressReporter.fail(self, step_id: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 执行`fail`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `fail` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fail、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="fun-00ca768fe8"></a>

#### FUN-00CA768FE8

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.done` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L141` |
| 签名 | `ModuleSyncProgressReporter.done(self, step_id: str, detail: str='')` |
| 参数 | `step_id`（str）：对象标识<br>`detail`（str）：详细说明文本；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 执行`done`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `done` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | done、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-f475f6a25b"></a>

#### FUN-F475F6A25B

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.update` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L145` |
| 签名 | `ModuleSyncProgressReporter.update(self, step_id: str, *, detail: str \| None=None, label: str \| None=None)` |
| 参数 | `step_id`（str）：对象标识<br>`detail`（str \| None）：详细说明文本；默认值 `None`<br>`label`（str \| None）：展示或分类标签；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 更新当前状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `update` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | update、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py) · 直接动态测试 |

<a id="fun-b77c2c5b77"></a>

#### FUN-B77C2C5B77

| 设计项 | 说明 |
|---|---|
| 函数 | `ModuleSyncProgressReporter.stage_io` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L149` |
| 签名 | `ModuleSyncProgressReporter.stage_io(self, stage: str, *, input_text: str, output_text: str, latency_ms: int \| None=None, label: str \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`input_text`（str）：输入文本<br>`output_text`（str）：输入文本<br>`latency_ms`（int \| None）：延迟毫秒数；默认值 `None`<br>`label`（str \| None）：展示或分类标签；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行阶段输入输出遥测处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `stage_io` → `super` → `self._sync`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | stage_io、super、self._sync |
| 复杂度 / 风险 | 分支 0；跨度 17 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4adbbae6f8"></a>

#### FUN-4ADBBAE6F8

| 设计项 | 说明 |
|---|---|
| 函数 | `format_generation_error` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L168` |
| 签名 | `format_generation_error(exc: BaseException)` |
| 参数 | `exc`（BaseException）：由调用方提供的 `exc` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`generation_error`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `strip` → `getattr` → `type` → `raw.replace`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、strip、str、getattr、type、raw.replace |
| 复杂度 / 风险 | 分支 5；跨度 20 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |

<a id="fun-de0806140c"></a>

#### FUN-DE0806140C

| 设计项 | 说明 |
|---|---|
| 函数 | `start_generation` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L190` |
| 签名 | `start_generation(job_key: str, run_config: RunConfig, *, session_id: str)` |
| 参数 | `job_key`（str）：索引键<br>`run_config`（RunConfig）：运行配置<br>`session_id`（str）：对象标识 |
| 返回 | 无返回值（None） |
| 职责 | 启动`generation`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `get_job` → `create_job` → `job_key.split` → `job.thread.is_alive` → `access_job` → `load_replay_bundle` → `log.info` → `log.exception`；包含 12 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_job、create_job、job_key.split、job.thread.is_alive、access_job、load_replay_bundle、log.info、log.exception、ModuleSyncProgressReporter、set_run_config、run_config.normalized、set_progress、time.perf_counter、clear_cache、run_analysis、setdefault、run_config.to_dict、run_config.fingerprint、get_current_run_id、archive_failure_run |
| 复杂度 / 风险 | 分支 12；跨度 73 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |

<a id="fun-eadc84cc44"></a>

#### FUN-EADC84CC44

| 设计项 | 说明 |
|---|---|
| 函数 | `start_generation.worker` |
| 源码位置 | [src/viz/generation_worker.py](../../../src/viz/generation_worker.py) · `L217` |
| 签名 | `start_generation.worker()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`worker`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `ModuleSyncProgressReporter` → `set_run_config` → `run_config.normalized` → `set_progress` → `access_job` → `time.perf_counter` → `clear_cache` → `run_analysis`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ModuleSyncProgressReporter、set_run_config、run_config.normalized、set_progress、access_job、time.perf_counter、clear_cache、run_analysis、setdefault、run_config.to_dict、run_config.fingerprint、log.info、log.exception、get_current_run_id、archive_failure_run、format_generation_error、reset_progress、reset_run_config、set_current_run_id |
| 复杂度 / 风险 | 分支 5；跨度 42 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py) · 直接动态测试 |

<a id="unit-4756f86a84"></a>

### UNIT-4756F86A84

**模块**：`src/viz/llm_process_view.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4756F86A84 |
| 源码 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/llm_process_view.py` 的职责，通过 `render_llm_process_page` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_llm_process_view.py](../../../tests/unit/test_llm_process_view.py) |
| 验证状态 | selected |

#### 函数导航

[_meta](#fun-75eb5f61b5) · [_llm_records](#fun-ac8e431b3e) · [_rule_stage_records](#fun-dee902878c) · [_llm_stage_records](#fun-81f59692e6) · [_render_advisor_trace](#fun-ba70001f5d) · [render_llm_process_page](#fun-f2c66853de)

<a id="fun-75eb5f61b5"></a>

#### FUN-75EB5F61B5

| 设计项 | 说明 |
|---|---|
| 函数 | `_meta` |
| 源码位置 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) · `L13` |
| 签名 | `_meta(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 构建`meta`；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ac8e431b3e"></a>

#### FUN-AC8E431B3E

| 设计项 | 说明 |
|---|---|
| 函数 | `_llm_records` |
| 源码位置 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) · `L17` |
| 签名 | `_llm_records(meta: dict)` |
| 参数 | `meta`（dict）：审计或处理元数据 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 构建`llm_records`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、meta.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-dee902878c"></a>

#### FUN-DEE902878C

| 设计项 | 说明 |
|---|---|
| 函数 | `_rule_stage_records` |
| 源码位置 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) · `L21` |
| 签名 | `_rule_stage_records(records: list[dict])` |
| 参数 | `records`（list[dict]）：结构化记录集合 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 构建`rule_stage_records`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | row.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-81f59692e6"></a>

#### FUN-81F59692E6

| 设计项 | 说明 |
|---|---|
| 函数 | `_llm_stage_records` |
| 源码位置 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) · `L25` |
| 签名 | `_llm_stage_records(records: list[dict])` |
| 参数 | `records`（list[dict]）：结构化记录集合 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 构建`llm_stage_records`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `row.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | row.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ba70001f5d"></a>

#### FUN-BA70001F5D

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_advisor_trace` |
| 源码位置 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) · `L29` |
| 签名 | `_render_advisor_trace(trace: dict \| None)` |
| 参数 | `trace`（dict \| None）：Agent 或流水线追踪记录 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`advisor_trace`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.caption` → `st.columns` → `metric` → `trace.get` → `st.error` → `st.warning` → `isinstance` → `st.json`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.caption、st.columns、metric、trace.get、int、st.error、str、st.warning、isinstance、st.json、st.expander |
| 复杂度 / 风险 | 分支 5；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f2c66853de"></a>

#### FUN-F2C66853DE

| 设计项 | 说明 |
|---|---|
| 函数 | `render_llm_process_page` |
| 源码位置 | [src/viz/llm_process_view.py](../../../src/viz/llm_process_view.py) · `L51` |
| 签名 | `render_llm_process_page(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_process_page`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_meta` → `report.get` → `meta.get` → `_llm_records` → `render_page_hero` → `st.success` → `advice.get` → `get`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _meta、report.get、str、meta.get、_llm_records、render_page_hero、st.success、advice.get、get、st.warning、st.info、st.tabs、render_progress_steps、st.caption、_llm_stage_records、render_llm_io_history、_rule_stage_records、st.markdown、st.code、json.dumps |
| 复杂度 / 风险 | 分支 6；跨度 79 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_process_view.py](../../../tests/unit/test_llm_process_view.py) · 直接动态测试 |

<a id="unit-d8ab5e90b4"></a>

### UNIT-D8AB5E90B4

**模块**：`src/viz/page_layout.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D8AB5E90B4 |
| 源码 | [src/viz/page_layout.py](../../../src/viz/page_layout.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/page_layout.py` 的职责，通过 `render_page_hero` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[render_page_hero](#fun-0e7ecec1bd)

<a id="fun-0e7ecec1bd"></a>

#### FUN-0E7ECEC1BD

| 设计项 | 说明 |
|---|---|
| 函数 | `render_page_hero` |
| 源码位置 | [src/viz/page_layout.py](../../../src/viz/page_layout.py) · `L8` |
| 签名 | `render_page_hero(title: str, subtitle: str='')` |
| 参数 | `title`（str）：由 `title` 表示的文本或标识<br>`subtitle`（str）：由 `subtitle` 表示的文本或标识；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`page_hero`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown |
| 复杂度 / 风险 | 分支 1；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-87ec9bc982"></a>

### UNIT-87EC9BC982

**模块**：`src/viz/pipeline_progress.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-87EC9BC982 |
| 源码 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/pipeline_progress.py` 的职责，通过 `format_latency_ms`、`pipeline_progress_headline`、`render_progress_steps`、`is_streaming_llm_record`、`partition_llm_records_for_live`、`render_live_llm_status_lightweight`、`render_live_llm_streams`、`render_llm_io_history` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 20 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [pipeline_progress_headline](#fun-0b8c70cae4) | 生成`pipeline_progress_headline`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py) |

#### 函数导航

[format_latency_ms](#fun-2a3f14c75d) · [pipeline_progress_headline](#fun-0b8c70cae4) · [_format_step](#fun-c1629a4de1) · [render_progress_steps](#fun-311ae39ba2) · [_render_llm_io_text](#fun-ad1fa5e595) · [_render_llm_output_panel](#fun-7dcbcf149d) · [is_streaming_llm_record](#fun-17c606facf) · [partition_llm_records_for_live](#fun-d82430a62e) · [render_live_llm_status_lightweight](#fun-4d69bae96d) · [render_live_llm_streams](#fun-c7365fb901) · [_filter_llm_io_records](#fun-c8f614ea56) · [render_llm_io_history](#fun-fa5a1c7f41) · [StreamlitProgressReporter.__init__](#fun-0d15b0afcc) · [StreamlitProgressReporter._paint](#fun-cf6dff11c9) · [StreamlitProgressReporter._on_change](#fun-518e29c44c) · [StreamlitProgressReporter._on_llm_begin](#fun-25b5bbb645) · [StreamlitProgressReporter.run_llm_stream](#fun-4d2f1f7990) · [StreamlitProgressReporter.run_llm_stream._gen](#fun-f822a4e8cf) · [StreamlitProgressReporter._on_llm_end](#fun-85e51e2ba9) · [StreamlitProgressReporter.complete](#fun-a18a4822f2)

<a id="fun-2a3f14c75d"></a>

#### FUN-2A3F14C75D

| 设计项 | 说明 |
|---|---|
| 函数 | `format_latency_ms` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L12` |
| 签名 | `format_latency_ms(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`latency_ms`；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int |
| 复杂度 / 风险 | 分支 2；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0b8c70cae4"></a>

#### FUN-0B8C70CAE4

| 设计项 | 说明 |
|---|---|
| 函数 | `pipeline_progress_headline` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L28` |
| 签名 | `pipeline_progress_headline(steps: list[dict] \| None)` |
| 参数 | `steps`（list[dict] \| None）：执行步骤集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`pipeline_progress_headline`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `s.get` → `step.get` → `strip` → `parts.append` → `join` → `last.get`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | s.get、str、step.get、strip、parts.append、join、last.get |
| 复杂度 / 风险 | 分支 7；跨度 21 行；高 |
| 测试 / 验证 | [tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py) · 直接动态测试 |

<a id="fun-c1629a4de1"></a>

#### FUN-C1629A4DE1

| 设计项 | 说明 |
|---|---|
| 函数 | `_format_step` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L51` |
| 签名 | `_format_step(step: PipelineProgressStep)` |
| 参数 | `step`（PipelineProgressStep）：由调用方提供的 `step` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`step`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_STATUS_ICONS.get`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _STATUS_ICONS.get |
| 复杂度 / 风险 | 分支 6；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-311ae39ba2"></a>

#### FUN-311AE39BA2

| 设计项 | 说明 |
|---|---|
| 函数 | `render_progress_steps` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L67` |
| 签名 | `render_progress_steps(steps: list[dict], *, title: str='生成步骤')` |
| 参数 | `steps`（list[dict]）：执行步骤集合<br>`title`（str）：由 `title` 表示的文本或标识；默认值 `'生成步骤'` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`progress_steps`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown` → `PipelineProgressStep` → `raw.get` → `_format_step`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown、PipelineProgressStep、raw.get、_format_step |
| 复杂度 / 风险 | 分支 3；跨度 14 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ad1fa5e595"></a>

#### FUN-AD1FA5E595

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_llm_io_text` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L83` |
| 签名 | `_render_llm_io_text(*, label: str, key: str, text: str, height: int=360)` |
| 参数 | `label`（str）：展示或分类标签<br>`key`（str）：索引键<br>`text`（str）：输入文本<br>`height`（int）：由 `height` 表示的数值参数；默认值 `360` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_io_text`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown` → `st.text_area`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown、st.text_area |
| 复杂度 / 风险 | 分支 1；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7dcbcf149d"></a>

#### FUN-7DCBCF149D

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_llm_output_panel` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L96` |
| 签名 | `_render_llm_output_panel(*, stage: str, output: str, error: str \| None=None, json_height: int=320, widget_key: str \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`output`（str）：输出对象或输出路径<br>`error`（str \| None）：错误信息或异常对象；默认值 `None`<br>`json_height`（int）：由 `json_height` 表示的数值参数；默认值 `320`<br>`widget_key`（str \| None）：索引键；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_output_panel`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.error` → `st.caption` → `_render_llm_io_text` → `format_llm_output`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.error、st.caption、_render_llm_io_text、format_llm_output、len |
| 复杂度 / 风险 | 分支 2；跨度 21 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-17c606facf"></a>

#### FUN-17C606FACF

| 设计项 | 说明 |
|---|---|
| 函数 | `is_streaming_llm_record` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L119` |
| 签名 | `is_streaming_llm_record(rec: dict)` |
| 参数 | `rec`（dict）：由 `rec` 表示的键值映射 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断流式 LLM 调用记录；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rec.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rec.get |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py) · 直接动态测试 |

<a id="fun-d82430a62e"></a>

#### FUN-D82430A62E

| 设计项 | 说明 |
|---|---|
| 函数 | `partition_llm_records_for_live` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L128` |
| 签名 | `partition_llm_records_for_live(records: list[dict])` |
| 参数 | `records`（list[dict]）：结构化记录集合 |
| 返回 | 返回 `tuple[list[dict], list[dict]]` 类型结果 |
| 职责 | 构建`partition_llm_records_for_live`；返回 `tuple[list[dict], list[dict]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_filter_llm_io_records` → `is_streaming_llm_record`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict], list[dict]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _filter_llm_io_records、is_streaming_llm_record |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py) · 直接动态测试 |

<a id="fun-4d69bae96d"></a>

#### FUN-4D69BAE96D

| 设计项 | 说明 |
|---|---|
| 函数 | `render_live_llm_status_lightweight` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L136` |
| 签名 | `render_live_llm_status_lightweight(live: dict)` |
| 参数 | `live`（dict）：由 `live` 表示的键值映射 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`live_llm_status_lightweight`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `live.get` → `partition_llm_records_for_live` → `st.markdown` → `rec.get` → `st.caption`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | live.get、partition_llm_records_for_live、st.markdown、rec.get、len、str、st.caption |
| 复杂度 / 风险 | 分支 5；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c7365fb901"></a>

#### FUN-C7365FB901

| 设计项 | 说明 |
|---|---|
| 函数 | `render_live_llm_streams` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L156` |
| 签名 | `render_live_llm_streams(active: list[dict])` |
| 参数 | `active`（list[dict]）：由 `active` 表示的输入集合 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`live_llm_streams`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown` → `enumerate` → `rec.get` → `st.container` → `st.caption` → `_render_llm_io_text` → `format_messages` → `format_llm_output`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown、enumerate、rec.get、st.container、st.caption、_render_llm_io_text、format_messages、len、format_llm_output |
| 复杂度 / 风险 | 分支 5；跨度 34 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c8f614ea56"></a>

#### FUN-C8F614EA56

| 设计项 | 说明 |
|---|---|
| 函数 | `_filter_llm_io_records` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L192` |
| 签名 | `_filter_llm_io_records(records: list[dict])` |
| 参数 | `records`（list[dict]）：结构化记录集合 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 筛选LLM 输入输出记录；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `any` → `r.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | any、r.get |
| 复杂度 / 风险 | 分支 1；跨度 17 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fa5a1c7f41"></a>

#### FUN-FA5A1C7F41

| 设计项 | 说明 |
|---|---|
| 函数 | `render_llm_io_history` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L211` |
| 签名 | `render_llm_io_history(records: list[dict], *, title: str='智能体 I/O', expand_last: bool=False)` |
| 参数 | `records`（list[dict]）：结构化记录集合<br>`title`（str）：由 `title` 表示的文本或标识；默认值 `'智能体 I/O'`<br>`expand_last`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_io_history`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_filter_llm_io_records` → `st.caption` → `st.markdown` → `enumerate` → `rec.get` → `format_latency_ms` → `st.expander` → `_render_llm_io_text`；包含 13 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _filter_llm_io_records、st.caption、st.markdown、enumerate、rec.get、format_latency_ms、str、st.expander、len、_render_llm_io_text、format_messages、st.error、format_llm_output、format_llm_narrative |
| 复杂度 / 风险 | 分支 13；跨度 48 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0d15b0afcc"></a>

#### FUN-0D15B0AFCC

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter.__init__` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L264` |
| 签名 | `StreamlitProgressReporter.__init__(self, *, progress_slot=None, llm_slot=None)` |
| 参数 | `progress_slot`（实现约定类型）：由调用方提供的 `progress_slot` 输入对象；默认值 `None`<br>`llm_slot`（实现约定类型）：由调用方提供的 `llm_slot` 输入对象；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `__init__` → `super` → `st.empty` → `self._paint`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | __init__、super、st.empty、self._paint |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cf6dff11c9"></a>

#### FUN-CF6DFF11C9

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter._paint` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L272` |
| 签名 | `StreamlitProgressReporter._paint(self, headline: str)` |
| 参数 | `headline`（str）：由 `headline` 表示的文本或标识 |
| 返回 | 无返回值（None） |
| 职责 | 执行`paint`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_format_step` → `join` → `self._slot.info`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _format_step、join、self._slot.info |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-518e29c44c"></a>

#### FUN-518E29C44C

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter._on_change` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L277` |
| 签名 | `StreamlitProgressReporter._on_change(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_change`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `next` → `reversed` → `self._paint`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | next、reversed、self._paint |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-25b5bbb645"></a>

#### FUN-25B5BBB645

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter._on_llm_begin` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L289` |
| 签名 | `StreamlitProgressReporter._on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`model`（str）：模型名称或模型对象<br>`messages`（list[dict[str, str]]）：消息序列<br>`label`（str）：展示或分类标签 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_llm_begin`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown` → `st.expander` → `expander.caption` → `expander.text_area` → `format_messages` → `expander.empty` → `output_box.markdown`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown、st.expander、expander.caption、expander.text_area、format_messages、expander.empty、output_box.markdown |
| 复杂度 / 风险 | 分支 2；跨度 21 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4d2f1f7990"></a>

#### FUN-4D2F1F7990

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter.run_llm_stream` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L311` |
| 签名 | `StreamlitProgressReporter.run_llm_stream(self, stage: str, chunk_iter)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`chunk_iter`（实现约定类型）：由调用方提供的 `chunk_iter` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 执行LLM 流式响应；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self._llm_blocks.get` → `run_llm_stream` → `super` → `st.write_stream` → `_gen`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._llm_blocks.get、run_llm_stream、super、st.write_stream、_gen |
| 复杂度 / 风险 | 分支 2；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f822a4e8cf"></a>

#### FUN-F822A4E8CF

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter.run_llm_stream._gen` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L316` |
| 签名 | `StreamlitProgressReporter.run_llm_stream._gen()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（隐式 None） |
| 职责 | 执行`gen`处理；无返回值（隐式 None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（隐式 None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-85e51e2ba9"></a>

#### FUN-85E51E2BA9

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter._on_llm_end` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L325` |
| 签名 | `StreamlitProgressReporter._on_llm_end(self, stage: str, output: str, *, error: str \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`output`（str）：输出对象或输出路径<br>`error`（str \| None）：错误信息或异常对象；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_llm_end`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._llm_blocks.get` → `self._find_llm` → `format_latency_ms` → `markdown` → `error` → `container` → `_render_llm_output_panel`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._llm_blocks.get、self._find_llm、format_latency_ms、markdown、error、container、_render_llm_output_panel |
| 复杂度 / 风险 | 分支 7；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a18a4822f2"></a>

#### FUN-A18A4822F2

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter.complete` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L348` |
| 签名 | `StreamlitProgressReporter.complete(self, *, ok: bool=True)` |
| 参数 | `ok`（bool）：控制对应行为是否启用的布尔值；默认值 `True` |
| 返回 | 无返回值（None） |
| 职责 | 执行`complete`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._slot.success` → `next` → `reversed` → `self._paint` → `self._slot.error`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._slot.success、next、reversed、self._paint、self._slot.error |
| 复杂度 / 风险 | 分支 3；跨度 11 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="unit-a63d87a7bb"></a>

### UNIT-A63D87A7BB

**模块**：`src/viz/replay_loader.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A63D87A7BB |
| 源码 | [src/viz/replay_loader.py](../../../src/viz/replay_loader.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/replay_loader.py` 的职责，通过 `load_replay_bundle` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) |
| 验证状态 | selected |

#### 函数导航

[_upgrade_to_advice_v2](#fun-52c23750b5) · [load_replay_bundle](#fun-2838d79653)

<a id="fun-52c23750b5"></a>

#### FUN-52C23750B5

| 设计项 | 说明 |
|---|---|
| 函数 | `_upgrade_to_advice_v2` |
| 源码位置 | [src/viz/replay_loader.py](../../../src/viz/replay_loader.py) · `L14` |
| 签名 | `_upgrade_to_advice_v2(run_id: str, bundle: tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]])` |
| 参数 | `run_id`（str）：对象标识<br>`bundle`（tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]）：由 `bundle` 表示的键值映射 |
| 返回 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果 |
| 职责 | 构建`upgrade_to_advice_v2`；返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `load_fetch` → `ExternalFactors` → `get` → `replay_warnings.append` → `assemble_market_context` → `pd.Timestamp` → `parsed.tz_localize`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、load_fetch、ExternalFactors、str、get、replay_warnings.append、assemble_market_context、pd.Timestamp、parsed.tz_localize、parsed.to_pydatetime、build_advice_packet、build_advice_report、update |
| 复杂度 / 风险 | 分支 4；跨度 45 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2838d79653"></a>

#### FUN-2838D79653

| 设计项 | 说明 |
|---|---|
| 函数 | `load_replay_bundle` |
| 源码位置 | [src/viz/replay_loader.py](../../../src/viz/replay_loader.py) · `L61` |
| 签名 | `load_replay_bundle(run_config: RunConfig)` |
| 参数 | `run_config`（RunConfig）：运行配置 |
| 返回 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果 |
| 职责 | 加载`replay_bundle`；返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_config.normalized` → `ValueError` → `inspect_run_archive` → `join` → `_upgrade_to_advice_v2` → `load_bundle` → `load_forensic_bundle`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_config.normalized、ValueError、inspect_run_archive、join、_upgrade_to_advice_v2、load_bundle、load_forensic_bundle |
| 复杂度 / 风险 | 分支 7；跨度 27 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |

<a id="unit-ee18de86b2"></a>

### UNIT-EE18DE86B2

**模块**：`src/viz/run_config_panel.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EE18DE86B2 |
| 源码 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/run_config_panel.py` 的职责，通过 `mode_label_to_value`、`mode_value_to_label`、`selected_run_config`、`render_sidebar_replay`、`render_run_config_panel` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 9 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) |
| 验证状态 | selected |

#### 函数导航

[mode_label_to_value](#fun-6478ef0ef9) · [mode_value_to_label](#fun-9df4825093) · [_seed](#fun-560a47b85b) · [_ensure_default_replay_run_id](#fun-dfbacecc76) · [selected_run_config](#fun-4712d21b11) · [_on_open_replay_config](#fun-d6653fc459) · [render_sidebar_replay](#fun-8d7f136545) · [_render_replay_controls](#fun-fea885853a) · [render_run_config_panel](#fun-de6787dacc)

<a id="fun-6478ef0ef9"></a>

#### FUN-6478EF0EF9

| 设计项 | 说明 |
|---|---|
| 函数 | `mode_label_to_value` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L21` |
| 签名 | `mode_label_to_value(label: str)` |
| 参数 | `label`（str）：展示或分类标签 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`mode_label_to_value`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_LABEL_TO_MODE.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _LABEL_TO_MODE.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9df4825093"></a>

#### FUN-9DF4825093

| 设计项 | 说明 |
|---|---|
| 函数 | `mode_value_to_label` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L25` |
| 签名 | `mode_value_to_label(value: str)` |
| 参数 | `value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`mode_value_to_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_MODE_TO_LABEL.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _MODE_TO_LABEL.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-560a47b85b"></a>

#### FUN-560A47B85B

| 设计项 | 说明 |
|---|---|
| 函数 | `_seed` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L29` |
| 签名 | `_seed()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`seed`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `items` → `run_config_widget_state` → `default_panel_run_config`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、bool、str、items、run_config_widget_state、default_panel_run_config |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-dfbacecc76"></a>

#### FUN-DFBACECC76

| 设计项 | 说明 |
|---|---|
| 函数 | `_ensure_default_replay_run_id` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L42` |
| 签名 | `_ensure_default_replay_run_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 确保`default_replay_run_id`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `list_archives` → `row.get` → `st.session_state.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list_archives、str、row.get、st.session_state.get |
| 复杂度 / 风险 | 分支 2；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4712d21b11"></a>

#### FUN-4712D21B11

| 设计项 | 说明 |
|---|---|
| 函数 | `selected_run_config` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L54` |
| 签名 | `selected_run_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `RunConfig` 类型结果 |
| 职责 | 执行`selected_config`；可能影响共享状态；返回 `RunConfig` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `strip` → `normalized` → `RunConfig` → `mode_label_to_value`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、strip、str、normalized、RunConfig、mode_label_to_value |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

<a id="fun-d6653fc459"></a>

#### FUN-D6653FC459

| 设计项 | 说明 |
|---|---|
| 函数 | `_on_open_replay_config` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L63` |
| 签名 | `_on_open_replay_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 打开`on_replay_config`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.pop`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.pop |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8d7f136545"></a>

#### FUN-8D7F136545

| 设计项 | 说明 |
|---|---|
| 函数 | `render_sidebar_replay` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L72` |
| 签名 | `render_sidebar_replay()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`sidebar_replay`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.sidebar.markdown` → `list_archives` → `st.sidebar.caption` → `st.sidebar.button`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.sidebar.markdown、list_archives、st.sidebar.caption、len、st.sidebar.button |
| 复杂度 / 风险 | 分支 1；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fea885853a"></a>

#### FUN-FEA885853A

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_replay_controls` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L85` |
| 签名 | `_render_replay_controls()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`replay_controls`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `list_archives` → `st.checkbox` → `st.session_state.get` → `st.info` → `_ensure_default_replay_run_id` → `archive_label` → `st.selectbox` → `labels.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list_archives、st.checkbox、st.session_state.get、st.info、_ensure_default_replay_run_id、archive_label、st.selectbox、list、labels.get |
| 复杂度 / 风险 | 分支 2；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-de6787dacc"></a>

#### FUN-DE6787DACC

| 设计项 | 说明 |
|---|---|
| 函数 | `render_run_config_panel` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L105` |
| 签名 | `render_run_config_panel()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`run_config_panel`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_seed` → `render_page_hero` → `st.radio` → `mode_label_to_value` → `st.session_state.get` → `st.caption` → `_render_replay_controls` → `st.button`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _seed、render_page_hero、st.radio、list、mode_label_to_value、str、st.session_state.get、st.caption、_render_replay_controls、st.button、selected_run_config、st.rerun、st.stop |
| 复杂度 / 风险 | 分支 2；跨度 20 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-6fa4e87f8a"></a>

### UNIT-6FA4E87F8A

**模块**：`src/viz/session_keys.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6FA4E87F8A |
| 源码 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/session_keys.py` 的职责，通过 `session_id`、`generation_id`、`job_key`、`rotate_generation_id`、`invalidate_report_cache` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 5 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[session_id](#fun-0eec7855b3) · [generation_id](#fun-ba937173ed) · [job_key](#fun-4d0107c2b8) · [rotate_generation_id](#fun-47ff82aecf) · [invalidate_report_cache](#fun-35b294ebf2)

<a id="fun-0eec7855b3"></a>

#### FUN-0EEC7855B3

| 设计项 | 说明 |
|---|---|
| 函数 | `session_id` |
| 源码位置 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) · `L23` |
| 签名 | `session_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`session_id`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `uuid.uuid4`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、uuid.uuid4 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-ba937173ed"></a>

#### FUN-BA937173ED

| 设计项 | 说明 |
|---|---|
| 函数 | `generation_id` |
| 源码位置 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) · `L29` |
| 签名 | `generation_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成生成任务标识文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `uuid.uuid4`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、uuid.uuid4 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4d0107c2b8"></a>

#### FUN-4D0107C2B8

| 设计项 | 说明 |
|---|---|
| 函数 | `job_key` |
| 源码位置 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) · `L35` |
| 签名 | `job_key()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`job_key`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `session_id` → `generation_id`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | session_id、generation_id |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-47ff82aecf"></a>

#### FUN-47FF82AECF

| 设计项 | 说明 |
|---|---|
| 函数 | `rotate_generation_id` |
| 源码位置 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) · `L39` |
| 签名 | `rotate_generation_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`rotate_generation_id`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `uuid.uuid4`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、uuid.uuid4 |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-35b294ebf2"></a>

#### FUN-35B294EBF2

| 设计项 | 说明 |
|---|---|
| 函数 | `invalidate_report_cache` |
| 源码位置 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) · `L45` |
| 签名 | `invalidate_report_cache()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`invalidate_report_cache`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `job_key` → `drop_job` → `session_id` → `rotate_generation_id` → `st.session_state.pop`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | job_key、drop_job、session_id、rotate_generation_id、st.session_state.pop |
| 复杂度 / 风险 | 分支 0；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-202db41fe0"></a>

### UNIT-202DB41FE0

**模块**：`src/viz/streamlit_common.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-202DB41FE0 |
| 源码 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) |
| 架构组件 | ARC-VIZ — Human-review presentation |
| 职责 | 实现“Human-review presentation”组件中 `src/viz/streamlit_common.py` 的职责，通过 `bootstrap_env`、`missing_runtime_dependencies`、`render_runtime_dependency_banner`、`page_setup`、`init_page`、`render_sidebar_refresh_button`、`render_sidebar_header`、`render_sidebar_footer` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ADV-002](../SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](../SWE.1-software-requirements.md#swr-adv-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 20 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[_session_id](#fun-2fd5708c36) · [_generation_id](#fun-b7dfde89b4) · [_job_key](#fun-675c7168fc) · [bootstrap_env](#fun-4bd443c8f3) · [missing_runtime_dependencies](#fun-cd1e50e1de) · [render_runtime_dependency_banner](#fun-86e5501024) · [page_setup](#fun-d2be30af9f) · [init_page](#fun-aff4dbd771) · [_on_request_reconfigure](#fun-4a59a3158d) · [render_sidebar_refresh_button](#fun-4a02ec5564) · [render_sidebar_header](#fun-e229df7619) · [render_sidebar_footer](#fun-943d58e197) · [_resolve_confirmed_run_config](#fun-460dffdb7c) · [_render_waiting_ui](#fun-9a85354a87) · [_render_waiting_ui._live_poll](#fun-19d89f3693) · [_render_external_waiting](#fun-db56a44e6c) · [_render_external_waiting._poll](#fun-4cb4b42e37) · [ensure_external_data](#fun-cd1636a5b5) · [ensure_report](#fun-2543fa4f8f) · [_store_report_bundle](#fun-2268bf01ca)

<a id="fun-2fd5708c36"></a>

#### FUN-2FD5708C36

| 设计项 | 说明 |
|---|---|
| 函数 | `_session_id` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L57` |
| 签名 | `_session_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`session_id`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `uuid.uuid4`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、uuid.uuid4 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b7dfde89b4"></a>

#### FUN-B7DFDE89B4

| 设计项 | 说明 |
|---|---|
| 函数 | `_generation_id` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L63` |
| 签名 | `_generation_id()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成生成任务标识文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `uuid.uuid4`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、uuid.uuid4 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-675c7168fc"></a>

#### FUN-675C7168FC

| 设计项 | 说明 |
|---|---|
| 函数 | `_job_key` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L69` |
| 签名 | `_job_key()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`job_key`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_session_id` → `_generation_id`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _session_id、_generation_id |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4bd443c8f3"></a>

#### FUN-4BD443C8F3

| 设计项 | 说明 |
|---|---|
| 函数 | `bootstrap_env` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L73` |
| 签名 | `bootstrap_env()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`bootstrap_env`处理；可能影响文件系统、共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `resolve` → `Path` → `env_path.exists` → `splitlines` → `env_path.read_text` → `line.strip` → `line.startswith` → `line.split`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 无返回值（None）；可观察变化限于文件系统、共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写；共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | resolve、Path、env_path.exists、splitlines、env_path.read_text、line.strip、line.startswith、line.split、key.strip、val.strip、os.environ.get、os.environ.setdefault、winreg.OpenKey、winreg.QueryValueEx、strip、server.split、winreg.CloseKey |
| 复杂度 / 风险 | 分支 8；跨度 32 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cd1e50e1de"></a>

#### FUN-CD1E50E1DE

| 设计项 | 说明 |
|---|---|
| 函数 | `missing_runtime_dependencies` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L107` |
| 签名 | `missing_runtime_dependencies()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`missing_runtime_dependencies`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `missing.append`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | missing.append |
| 复杂度 / 风险 | 分支 1；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-86e5501024"></a>

#### FUN-86E5501024

| 设计项 | 说明 |
|---|---|
| 函数 | `render_runtime_dependency_banner` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L117` |
| 签名 | `render_runtime_dependency_banner()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`runtime_dependency_banner`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `missing_runtime_dependencies` → `st.error` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | missing_runtime_dependencies、st.error、join |
| 复杂度 / 风险 | 分支 1；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d2be30af9f"></a>

#### FUN-D2BE30AF9F

| 设计项 | 说明 |
|---|---|
| 函数 | `page_setup` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L129` |
| 签名 | `page_setup()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`page_setup`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `bootstrap_env` → `setup_logging` → `st.markdown`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bootstrap_env、setup_logging、st.markdown |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-aff4dbd771"></a>

#### FUN-AFF4DBD771

| 设计项 | 说明 |
|---|---|
| 函数 | `init_page` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L137` |
| 签名 | `init_page(*, title_suffix: str='')` |
| 参数 | `title_suffix`（str）：由 `title_suffix` 表示的文本或标识；默认值 `''` |
| 返回 | 无返回值（None） |
| 职责 | 初始化`page`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `bootstrap_env` → `setup_logging` → `st.set_page_config` → `st.markdown`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bootstrap_env、setup_logging、st.set_page_config、st.markdown |
| 复杂度 / 风险 | 分支 1；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4a59a3158d"></a>

#### FUN-4A59A3158D

| 设计项 | 说明 |
|---|---|
| 函数 | `_on_request_reconfigure` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L149` |
| 签名 | `_on_request_reconfigure()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_request_reconfigure`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `log.info` → `st.session_state.pop`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.info、st.session_state.pop |
| 复杂度 / 风险 | 分支 0；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4a02ec5564"></a>

#### FUN-4A02EC5564

| 设计项 | 说明 |
|---|---|
| 函数 | `render_sidebar_refresh_button` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L158` |
| 签名 | `render_sidebar_refresh_button()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`sidebar_refresh_button`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.sidebar.button`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.sidebar.button |
| 复杂度 / 风险 | 分支 0；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e229df7619"></a>

#### FUN-E229DF7619

| 设计项 | 说明 |
|---|---|
| 函数 | `render_sidebar_header` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L167` |
| 签名 | `render_sidebar_header()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`sidebar_header`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.sidebar.markdown` → `st.sidebar.caption` → `short_model_name` → `render_sidebar_replay` → `render_sidebar_refresh_button`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.sidebar.markdown、st.sidebar.caption、short_model_name、render_sidebar_replay、render_sidebar_refresh_button |
| 复杂度 / 风险 | 分支 1；跨度 15 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-943d58e197"></a>

#### FUN-943D58E197

| 设计项 | 说明 |
|---|---|
| 函数 | `render_sidebar_footer` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L184` |
| 签名 | `render_sidebar_footer(data: dict \| None=None)` |
| 参数 | `data`（dict \| None）：输入数据；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`sidebar_footer`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `coerce_run_config` → `st.session_state.get` → `mode_value_to_label` → `st.sidebar.caption` → `active_config.fingerprint` → `st.sidebar.expander` → `st.table` → `indicator_table_rows`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | coerce_run_config、st.session_state.get、mode_value_to_label、st.sidebar.caption、active_config.fingerprint、st.sidebar.expander、st.table、indicator_table_rows、indicator_snapshot |
| 复杂度 / 风险 | 分支 2；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-460dffdb7c"></a>

#### FUN-460DFFDB7C

| 设计项 | 说明 |
|---|---|
| 函数 | `_resolve_confirmed_run_config` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L197` |
| 签名 | `_resolve_confirmed_run_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `RunConfig \| None` 类型结果 |
| 职责 | 解析并选择`confirmed_run_config`；可能影响共享状态；返回 `RunConfig \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `coerce_run_config` → `st.session_state.get`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig \| None` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | coerce_run_config、st.session_state.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9a85354a87"></a>

#### FUN-9A85354A87

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_waiting_ui` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L201` |
| 签名 | `_render_waiting_ui(job_key_str: str, *, show_generation_ui: bool)` |
| 参数 | `job_key_str`（str）：由 `job_key_str` 表示的文本或标识<br>`show_generation_ui`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`waiting_ui`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `render_page_hero` → `st.empty` → `st.fragment` → `timedelta` → `get_job` → `_session_id` → `live.get` → `steps_slot.container`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | render_page_hero、st.empty、st.fragment、timedelta、get_job、_session_id、live.get、steps_slot.container、render_progress_steps、pipeline_progress_headline、st.caption、llm_slot.container、render_live_llm_status_lightweight、st.rerun、log.exception、st.warning、_live_poll |
| 复杂度 / 风险 | 分支 6；跨度 37 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-19d89f3693"></a>

#### FUN-19D89F3693

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_waiting_ui._live_poll` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L217` |
| 签名 | `_render_waiting_ui._live_poll()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`live_poll`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.fragment` → `timedelta` → `get_job` → `_session_id` → `live.get` → `steps_slot.container` → `render_progress_steps` → `pipeline_progress_headline`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.fragment、timedelta、get_job、_session_id、live.get、steps_slot.container、render_progress_steps、pipeline_progress_headline、st.caption、llm_slot.container、render_live_llm_status_lightweight、st.rerun、log.exception、st.warning |
| 复杂度 / 风险 | 分支 5；跨度 19 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-db56a44e6c"></a>

#### FUN-DB56A44E6C

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_external_waiting` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L240` |
| 签名 | `_render_external_waiting(job_key_str: str)` |
| 参数 | `job_key_str`（str）：由 `job_key_str` 表示的文本或标识 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`external_waiting`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `render_page_hero` → `st.empty` → `st.fragment` → `timedelta` → `get_job` → `_session_id` → `live.get` → `st.rerun`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | render_page_hero、st.empty、st.fragment、timedelta、get_job、_session_id、live.get、st.rerun、steps_slot.container、render_progress_steps、pipeline_progress_headline、st.info、llm_slot.container、render_live_llm_status_lightweight、log.exception、st.warning、_poll |
| 复杂度 / 风险 | 分支 5；跨度 37 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4cb4b42e37"></a>

#### FUN-4CB4B42E37

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_external_waiting._poll` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L255` |
| 签名 | `_render_external_waiting._poll()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`poll`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.fragment` → `timedelta` → `get_job` → `_session_id` → `live.get` → `st.rerun` → `steps_slot.container` → `render_progress_steps`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.fragment、timedelta、get_job、_session_id、live.get、st.rerun、steps_slot.container、render_progress_steps、pipeline_progress_headline、st.info、llm_slot.container、render_live_llm_status_lightweight、log.exception、st.warning |
| 复杂度 / 风险 | 分支 5；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cd1636a5b5"></a>

#### FUN-CD1636A5B5

| 设计项 | 说明 |
|---|---|
| 函数 | `ensure_external_data` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L279` |
| 签名 | `ensure_external_data()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 确保`external_data`；可能影响共享状态；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `purge_expired` → `st.session_state.pop` → `invalidate_report_cache` → `st.session_state.get` → `render_run_config_panel` → `_resolve_confirmed_run_config` → `run_config.fingerprint` → `_job_key`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | purge_expired、st.session_state.pop、invalidate_report_cache、st.session_state.get、render_run_config_panel、_resolve_confirmed_run_config、run_config.fingerprint、_job_key、load_replay_bundle、st.error、st.stop、external_payload_from_report、_generation_id、get_job、_session_id、log.exception、format_generation_error、job.live.get、start_generation、_render_external_waiting |
| 复杂度 / 风险 | 分支 10；跨度 56 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2543fa4f8f"></a>

#### FUN-2543FA4F8F

| 设计项 | 说明 |
|---|---|
| 函数 | `ensure_report` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L337` |
| 签名 | `ensure_report(*, show_generation_ui: bool=True)` |
| 参数 | `show_generation_ui`（bool）：控制对应行为是否启用的布尔值；默认值 `True` |
| 返回 | 返回 `tuple[dict, dict, dict]` 类型结果 |
| 职责 | 确保报告；可能影响共享状态；返回 `tuple[dict, dict, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `purge_expired` → `st.session_state.pop` → `invalidate_report_cache` → `st.session_state.get` → `render_run_config_panel` → `_resolve_confirmed_run_config` → `run_config.fingerprint` → `_job_key`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict, dict, dict]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | purge_expired、st.session_state.pop、invalidate_report_cache、st.session_state.get、render_run_config_panel、_resolve_confirmed_run_config、run_config.fingerprint、_job_key、_generation_id、get_job、_session_id、job.live.get、log.exception、st.markdown、render_progress_steps、st.error、format_generation_error、st.caption、st.stop、start_generation |
| 复杂度 / 风险 | 分支 8；跨度 49 行；中 |
| 测试 / 验证 | [tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-2268bf01ca"></a>

#### FUN-2268BF01CA

| 设计项 | 说明 |
|---|---|
| 函数 | `_store_report_bundle` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L388` |
| 签名 | `_store_report_bundle(job_key_str: str, bundle: tuple[dict, dict, dict], run_config_fingerprint: str)` |
| 参数 | `job_key_str`（str）：由 `job_key_str` 表示的文本或标识<br>`bundle`（tuple[dict, dict, dict]）：由 `bundle` 表示的键值映射<br>`run_config_fingerprint`（str）：由 `run_config_fingerprint` 表示的文本或标识 |
| 返回 | 返回 `tuple[dict, dict, dict]` 类型结果 |
| 职责 | 构建`store_report_bundle`；返回 `tuple[dict, dict, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `drop_job` → `_session_id` → `_generation_id`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict, dict, dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | drop_job、_session_id、_generation_id |
| 复杂度 / 风险 | 分支 0；跨度 10 行；低 |
| 测试 / 验证 | [tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |
