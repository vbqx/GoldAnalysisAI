# ARC-VIZ — Streamlit 展示

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
| [src/viz/agent_trace_view.py](#unit-986f7077ab) | 8 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/archive_config_summary.py](#unit-6a590d74f1) | 2 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/charts.py](#unit-7301a06e0a) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/dashboard_components.py](#unit-c8a82e7519) | 38 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/decision_page.py](#unit-003f08decb) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/display_labels.py](#unit-9b624c52d7) | 10 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/external_data_view.py](#unit-8b3827f5ec) | 6 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/generation_state.py](#unit-e27519993b) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/generation_worker.py](#unit-4c9db5733a) | 16 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/lightweight_chart.py](#unit-abbedfd349) | 15 | 15 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/llm_meta.py](#unit-f5c8e9bf82) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/llm_view.py](#unit-e782e5b762) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/page_layout.py](#unit-d8ab5e90b4) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/pipeline_progress.py](#unit-87ec9bc982) | 19 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/replay_loader.py](#unit-a63d87a7bb) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/report_views.py](#unit-4e47421947) | 4 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/run_config_panel.py](#unit-ee18de86b2) | 20 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/session_keys.py](#unit-6fa4e87f8a) | 5 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/source_labels.py](#unit-f568ea7ece) | 8 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/streamlit_common.py](#unit-202db41fe0) | 20 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |

<a id="unit-3ec85337ca"></a>

### UNIT-3EC85337CA

**模块**：`src/viz/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3EC85337CA |
| 源码 | [src/viz/__init__.py](../../../src/viz/__init__.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-986f7077ab"></a>

### UNIT-986F7077AB

**模块**：`src/viz/agent_trace_view.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-986F7077AB |
| 源码 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/agent_trace_view.py` 的职责，通过 `render_agent_trace_panel`、`render_agent_trace_sidebar` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [render_agent_trace_panel](#fun-8765e21451) | 渲染`agent_trace_panel`；无返回值（None）。 | 未检测到直接副作用 | — |

#### 函数导航

[_badge_md](#fun-1b8f11eeeb) · [_stage_source_text](#fun-f0fee40c1c) · [_short_text](#fun-4971a29fae) · [_stage_card](#fun-c7d1fa8bc5) · [_render_stage_summary_grid](#fun-f93c1a5bee) · [_decision_flow_markdown](#fun-d0d9c7226c) · [render_agent_trace_panel](#fun-8765e21451) · [render_agent_trace_sidebar](#fun-1d4ae30fbd)

<a id="fun-1b8f11eeeb"></a>

#### FUN-1B8F11EEEB

| 设计项 | 说明 |
|---|---|
| 函数 | `_badge_md` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L26` |
| 签名 | `_badge_md(meta: dict)` |
| 参数 | `meta`（dict）：审计或处理元数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`badge_md`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `stage_meta_label` → `llm_was_invoked`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | stage_meta_label、llm_was_invoked |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f0fee40c1c"></a>

#### FUN-F0FEE40C1C

| 设计项 | 说明 |
|---|---|
| 函数 | `_stage_source_text` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L33` |
| 签名 | `_stage_source_text(stage_meta: dict, stage: str)` |
| 参数 | `stage_meta`（dict）：审计或处理元数据<br>`stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stage_source_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `stage_meta.get` → `stage_meta_label` → `meta.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | stage_meta.get、stage_meta_label、meta.get |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4971a29fae"></a>

#### FUN-4971A29FAE

| 设计项 | 说明 |
|---|---|
| 函数 | `_short_text` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L41` |
| 签名 | `_short_text(value: object, limit: int=72)` |
| 参数 | `value`（object）：待处理值<br>`limit`（int）：返回或处理数量上限；默认值 `72` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`short_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、len |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c7d1fa8bc5"></a>

#### FUN-C7D1FA8BC5

| 设计项 | 说明 |
|---|---|
| 函数 | `_stage_card` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L48` |
| 签名 | `_stage_card(stage: str, meta: dict, main: str, sub: str='')` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`meta`（dict）：审计或处理元数据<br>`main`（str）：由 `main` 表示的文本或标识<br>`sub`（str）：由 `sub` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stage_card`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `llm_was_invoked` → `STAGE_LABELS.get` → `html.escape` → `render_stage_meta_badge` → `_short_text`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | llm_was_invoked、STAGE_LABELS.get、html.escape、render_stage_meta_badge、_short_text |
| 复杂度 / 风险 | 分支 1；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f93c1a5bee"></a>

#### FUN-F93C1A5BEE

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_stage_summary_grid` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L60` |
| 签名 | `_render_stage_summary_grid(report: dict, trace: dict)` |
| 参数 | `report`（dict）：分析报告<br>`trace`（dict）：Agent 或流水线追踪记录 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`stage_summary_grid`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `trace.get` → `report.get` → `analyst_team.get` → `analyst_biases.append` → `STAGE_LABELS.get` → `label_bias` → `row.get` → `sum`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | trace.get、report.get、analyst_team.get、analyst_biases.append、STAGE_LABELS.get、label_bias、row.get、sum、len、_stage_card、stage_meta.get、join、debate.get、float、primary_signal.get、label_action、decision.get、label_trade_direction |
| 复杂度 / 风险 | 分支 3；跨度 48 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d0d9c7226c"></a>

#### FUN-D0D9C7226C

| 设计项 | 说明 |
|---|---|
| 函数 | `_decision_flow_markdown` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L110` |
| 签名 | `_decision_flow_markdown(report: dict, trace: dict)` |
| 参数 | `report`（dict）：分析报告<br>`trace`（dict）：Agent 或流水线追踪记录 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`decision_flow_markdown`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `trace.get` → `team.get` → `analyst_bits.append` → `label_bias` → `row.get` → `enumerate` → `signal_bits.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、trace.get、team.get、analyst_bits.append、label_bias、row.get、enumerate、signal_bits.append、sig.get、sum、len、_stage_source_text、float、debate.get、decision.get、join、meta.get、metrics.get、sentiment.get、label_trade_direction |
| 复杂度 / 风险 | 分支 3；跨度 78 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8765e21451"></a>

#### FUN-8765E21451

| 设计项 | 说明 |
|---|---|
| 函数 | `render_agent_trace_panel` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L190` |
| 签名 | `render_agent_trace_panel(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`agent_trace_panel`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `st.caption` → `trace.get` → `debate.get` → `sentiment.get` → `st.warning` → `st.markdown` → `_render_stage_summary_grid`；包含 45 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、st.caption、trace.get、debate.get、float、sentiment.get、st.warning、st.markdown、_render_stage_summary_grid、meta_report.get、reliability.get、get、invariants.get、join、str、v.get、st.info、st.columns、stage_meta.get、st.metric |
| 复杂度 / 风险 | 分支 45；跨度 266 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1d4ae30fbd"></a>

#### FUN-1D4AE30FBD

| 设计项 | 说明 |
|---|---|
| 函数 | `render_agent_trace_sidebar` |
| 源码位置 | [src/viz/agent_trace_view.py](../../../src/viz/agent_trace_view.py) · `L458` |
| 签名 | `render_agent_trace_sidebar(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`agent_trace_sidebar`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `render_agent_trace_panel`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | render_agent_trace_panel |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-6a590d74f1"></a>

### UNIT-6A590D74F1

**模块**：`src/viz/archive_config_summary.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6A590D74F1 |
| 源码 | [src/viz/archive_config_summary.py](../../../src/viz/archive_config_summary.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/archive_config_summary.py` 的职责，通过 `format_archived_run_config`、`pipeline_status_label` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [format_archived_run_config](#fun-e73bf3a018) | 格式化`archived_run_config`；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py) |
| [pipeline_status_label](#fun-acfcd5eef4) | 生成`pipeline_status_label`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py) |

#### 函数导航

[format_archived_run_config](#fun-e73bf3a018) · [pipeline_status_label](#fun-acfcd5eef4)

<a id="fun-e73bf3a018"></a>

#### FUN-E73BF3A018

| 设计项 | 说明 |
|---|---|
| 函数 | `format_archived_run_config` |
| 源码位置 | [src/viz/archive_config_summary.py](../../../src/viz/archive_config_summary.py) · `L8` |
| 签名 | `format_archived_run_config(run_config: dict[str, Any] \| None)` |
| 参数 | `run_config`（dict[str, Any] \| None）：运行配置 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`archived_run_config`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `cfg.get` → `stages.append` → `join` → `strip`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | cfg.get、stages.append、join、strip、str |
| 复杂度 / 风险 | 分支 5；跨度 22 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py) · 直接动态测试 |

<a id="fun-acfcd5eef4"></a>

#### FUN-ACFCD5EEF4

| 设计项 | 说明 |
|---|---|
| 函数 | `pipeline_status_label` |
| 源码位置 | [src/viz/archive_config_summary.py](../../../src/viz/archive_config_summary.py) · `L32` |
| 签名 | `pipeline_status_label(status: str \| None)` |
| 参数 | `status`（str \| None）：由调用方提供的 `status` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`pipeline_status_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `mapping.get` → `lower` → `strip`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | mapping.get、lower、strip、str |
| 复杂度 / 风险 | 分支 0；跨度 7 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_config_summary.py](../../../tests/unit/test_archive_config_summary.py) · 直接动态测试 |

<a id="unit-7301a06e0a"></a>

### UNIT-7301A06E0A

**模块**：`src/viz/charts.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7301A06E0A |
| 源码 | [src/viz/charts.py](../../../src/viz/charts.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/charts.py` 的职责，通过 `build_sentiment_donut`、`build_projection_chart` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) |
| 验证状态 | selected |

#### 函数导航

[build_sentiment_donut](#fun-508ae8715d) · [build_projection_chart](#fun-25d919a083)

<a id="fun-508ae8715d"></a>

#### FUN-508AE8715D

| 设计项 | 说明 |
|---|---|
| 函数 | `build_sentiment_donut` |
| 源码位置 | [src/viz/charts.py](../../../src/viz/charts.py) · `L10` |
| 签名 | `build_sentiment_donut(sentiment: dict[str, float])` |
| 参数 | `sentiment`（dict[str, float]）：市场情绪结果 |
| 返回 | 返回 `go.Figure` 类型结果 |
| 职责 | 构建`sentiment_donut`；返回 `go.Figure` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `go.Figure` → `go.Pie` → `fig.update_layout`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `go.Figure` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | go.Figure、go.Pie、dict、fig.update_layout |
| 复杂度 / 风险 | 分支 0；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-25d919a083"></a>

#### FUN-25D919A083

| 设计项 | 说明 |
|---|---|
| 函数 | `build_projection_chart` |
| 源码位置 | [src/viz/charts.py](../../../src/viz/charts.py) · `L36` |
| 签名 | `build_projection_chart(projections: list[dict])` |
| 参数 | `projections`（list[dict]）：由 `projections` 表示的输入集合 |
| 返回 | 返回 `go.Figure` 类型结果 |
| 职责 | 构建`projection_chart`；返回 `go.Figure` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `go.Figure` → `fig.add_trace` → `go.Scatter` → `fig.update_layout` → `fig.update_yaxes`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `go.Figure` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | go.Figure、fig.add_trace、go.Scatter、dict、fig.update_layout、fig.update_yaxes |
| 复杂度 / 风险 | 分支 1；跨度 24 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-c8a82e7519"></a>

### UNIT-C8A82E7519

**模块**：`src/viz/dashboard_components.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C8A82E7519 |
| 源码 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/dashboard_components.py` 的职责，通过 `render_external_data_panel`、`render_header`、`render_final_decision_banner`、`render_decision_summary`、`render_rejected_plan_details`、`render_primary_plan_focus`、`render_top_overview_row`、`render_tf_stack` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 38 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py) |
| 验证状态 | selected |

#### 函数导航

[_is_placeholder_source](#fun-86e2359125) · [_chg_class](#fun-0059ca3d67) · [_truncate](#fun-2d55219a60) · [_source_tags](#fun-550f755267) · [render_external_data_panel](#fun-85e277e655) · [render_header](#fun-64dfaecbb9) · [_fmt_price](#fun-725d5a8f44) · [_primary_signal](#fun-72ca74c7a9) · [_status_meta](#fun-389fe568ee) · [_direction_class](#fun-23bf7fa077) · [_signal_zone](#fun-0010bc2852) · [_signal_targets](#fun-d398c927e4) · [_first_text](#fun-133e6e54c6) · [render_final_decision_banner](#fun-e962207ce2) · [render_decision_summary](#fun-c819f0daf5) · [_display_plan_signals](#fun-937765293d) · [_confidence_text](#fun-d3d7244ace) · [_minify_plan_html](#fun-2f9b45e4cd) · [_render_plan_card](#fun-e6d39c08cf) · [render_rejected_plan_details](#fun-9c21a8d1a7) · [render_primary_plan_focus](#fun-3bfb666a67) · [render_top_overview_row](#fun-1308a20c4f) · [render_tf_stack](#fun-d69f968c9e) · [render_bottom_row](#fun-1fb9420507) · [_fmt_zone](#fun-2dd042625f) · [_fmt_event_list](#fun-eab2c95485) · [_fmt_prices](#fun-48fc0fd2b1) · [_fmt_strong_weak](#fun-6d789b868b) · [render_tf_panel](#fun-854dcce0eb) · [render_narrative_section](#fun-ce51fb1d21) · [_narrative_fallback_hint](#fun-18e3bf98ae) · [render_key_levels](#fun-1e810a3b0e) · [render_strategy_sections](#fun-b460f224ca) · [render_path_cards](#fun-60b752029b) · [render_calendar](#fun-f129f84b90) · [render_trading_plans](#fun-94c9558228) · [render_liquidity](#fun-5e89771732) · [render_footer](#fun-aaaaeceb82)

<a id="fun-86e2359125"></a>

#### FUN-86E2359125

| 设计项 | 说明 |
|---|---|
| 函数 | `_is_placeholder_source` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L23` |
| 签名 | `_is_placeholder_source(src: str)` |
| 参数 | `src`（str）：由 `src` 表示的文本或标识 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`placeholder_source`；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `src.endswith` → `src.lower`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | src.endswith、src.lower |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0059ca3d67"></a>

#### FUN-0059CA3D67

| 设计项 | 说明 |
|---|---|
| 函数 | `_chg_class` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L632` |
| 签名 | `_chg_class(change: float)` |
| 参数 | `change`（float）：由 `change` 表示的数值参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`chg_class`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2d55219a60"></a>

#### FUN-2D55219A60

| 设计项 | 说明 |
|---|---|
| 函数 | `_truncate` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L636` |
| 签名 | `_truncate(text: str, n: int)` |
| 参数 | `text`（str）：输入文本<br>`n`（int）：由 `n` 表示的数值参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`truncate`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、len |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-550f755267"></a>

#### FUN-550F755267

| 设计项 | 说明 |
|---|---|
| 函数 | `_source_tags` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L641` |
| 签名 | `_source_tags(sources: list[str])` |
| 参数 | `sources`（list[str]）：由 `sources` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`source_tags`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_is_placeholder_source` → `chips.append` → `_SOURCE_LABELS.get` → `html.escape` → `join`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _is_placeholder_source、chips.append、_SOURCE_LABELS.get、html.escape、join |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py) · 直接动态测试 |

<a id="fun-85e277e655"></a>

#### FUN-85E277E655

| 设计项 | 说明 |
|---|---|
| 函数 | `render_external_data_panel` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L654` |
| 签名 | `render_external_data_panel(ext: dict[str, Any])` |
| 参数 | `ext`（dict[str, Any]）：由 `ext` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`external_data_panel`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ext.get` → `_source_tags` → `isinstance` → `join` → `html.escape` → `e.get` → `parse_risk_events_calendar` → `p.get`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ext.get、_source_tags、isinstance、join、html.escape、str、e.get、parse_risk_events_calendar、p.get |
| 复杂度 / 风险 | 分支 8；跨度 62 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-64dfaecbb9"></a>

#### FUN-64DFAECBB9

| 设计项 | 说明 |
|---|---|
| 函数 | `render_header` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L718` |
| 签名 | `render_header(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`header`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_chg_class` → `metric_html.append` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _chg_class、metric_html.append、join |
| 复杂度 / 风险 | 分支 2；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-725d5a8f44"></a>

#### FUN-725D5A8F44

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_price` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L742` |
| 签名 | `_fmt_price(value: Any)` |
| 参数 | `value`（Any）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成价格显示值文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-72ca74c7a9"></a>

#### FUN-72CA74C7A9

| 设计项 | 说明 |
|---|---|
| 函数 | `_primary_signal` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L749` |
| 签名 | `_primary_signal(signals: list[dict[str, Any]])` |
| 参数 | `signals`（list[dict[str, Any]]）：交易信号集合 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 构建`primary_signal`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get |
| 复杂度 / 风险 | 分支 3；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-389fe568ee"></a>

#### FUN-389FE568EE

| 设计项 | 说明 |
|---|---|
| 函数 | `_status_meta` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L758` |
| 签名 | `_status_meta(status: str)` |
| 参数 | `status`（str）：由 `status` 表示的文本或标识 |
| 返回 | 返回 `tuple[str, str]` 类型结果 |
| 职责 | 构建`status_meta`；返回 `tuple[str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `status_map.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | status_map.get |
| 复杂度 / 风险 | 分支 0；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-23bf7fa077"></a>

#### FUN-23BF7FA077

| 设计项 | 说明 |
|---|---|
| 函数 | `_direction_class` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L769` |
| 签名 | `_direction_class(signal: dict[str, Any] \| None, conclusion: dict[str, Any])` |
| 参数 | `signal`（dict[str, Any] \| None）：当前交易信号<br>`conclusion`（dict[str, Any]）：由 `conclusion` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`direction_class`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `infer_trade_theme` → `signal.get` → `lower` → `conclusion.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | infer_trade_theme、str、signal.get、lower、conclusion.get |
| 复杂度 / 风险 | 分支 3；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0010bc2852"></a>

#### FUN-0010BC2852

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_zone` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L785` |
| 签名 | `_signal_zone(sig: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`signal_zone`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_fmt_price` → `sig.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _fmt_price、sig.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d398c927e4"></a>

#### FUN-D398C927E4

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_targets` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L789` |
| 签名 | `_signal_targets(sig: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`signal_targets`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get` → `join` → `_fmt_price`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get、join、_fmt_price |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-133e6e54c6"></a>

#### FUN-133E6E54C6

| 设计项 | 说明 |
|---|---|
| 函数 | `_first_text` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L796` |
| 签名 | `_first_text(items: list[Any], fallback: str='—')` |
| 参数 | `items`（list[Any]）：输入项集合<br>`fallback`（str）：由 `fallback` 表示的文本或标识；默认值 `'—'` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`first_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e962207ce2"></a>

#### FUN-E962207CE2

| 设计项 | 说明 |
|---|---|
| 函数 | `render_final_decision_banner` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L804` |
| 签名 | `render_final_decision_banner(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`final_decision_banner`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `build_final_decision_meta` → `final.get` → `lower` → `html.escape` → `label_action` → `plan.get`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、build_final_decision_meta、bool、final.get、lower、str、html.escape、label_action、plan.get、strip |
| 复杂度 / 风险 | 分支 9；跨度 54 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-c819f0daf5"></a>

#### FUN-C819F0DAF5

| 设计项 | 说明 |
|---|---|
| 函数 | `render_decision_summary` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L860` |
| 签名 | `render_decision_summary(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`decision_summary`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `_primary_signal` → `get` → `_status_meta` → `_direction_class` → `_fmt_price` → `metrics.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、bool、meta.get、_primary_signal、str、get、_status_meta、_direction_class、_fmt_price、metrics.get、float、html.escape、conclusion.get、label_action、execution_banner、list、_first_text、render_source_badge、stage_source |
| 复杂度 / 风险 | 分支 4；跨度 69 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-937765293d"></a>

#### FUN-937765293D

| 设计项 | 说明 |
|---|---|
| 函数 | `_display_plan_signals` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L931` |
| 签名 | `_display_plan_signals(signals: list[dict[str, Any]], *, limit: int=3)` |
| 参数 | `signals`（list[dict[str, Any]]）：交易信号集合<br>`limit`（int）：返回或处理数量上限；默认值 `3` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`display_plan_signals`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d3d7244ace"></a>

#### FUN-D3D7244ACE

| 设计项 | 说明 |
|---|---|
| 函数 | `_confidence_text` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L938` |
| 签名 | `_confidence_text(sig: dict[str, Any])` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`confidence_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get、float、str |
| 复杂度 / 风险 | 分支 3；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2f9b45e4cd"></a>

#### FUN-2F9B45E4CD

| 设计项 | 说明 |
|---|---|
| 函数 | `_minify_plan_html` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L948` |
| 签名 | `_minify_plan_html(markup: str)` |
| 参数 | `markup`（str）：由 `markup` 表示的文本或标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`minify_plan_html`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ln.strip` → `markup.splitlines` → `join`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ln.strip、markup.splitlines、join |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e6d39c08cf"></a>

#### FUN-E6D39C08CF

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_plan_card` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L954` |
| 签名 | `_render_plan_card(sig: dict[str, Any], *, plan_label: str, is_primary: bool=False, unauthorized: bool=False, rejected: bool=False)` |
| 参数 | `sig`（dict[str, Any]）：待评估交易信号<br>`plan_label`（str）：展示或分类标签<br>`is_primary`（bool）：控制对应行为是否启用的布尔值；默认值 `False`<br>`unauthorized`（bool）：控制对应行为是否启用的布尔值；默认值 `False`<br>`rejected`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`plan_card`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sig.get` → `infer_trade_theme` → `_status_meta` → `html.escape` → `join` → `strip` → `startswith` → `_confidence_text`；包含 16 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sig.get、infer_trade_theme、str、_status_meta、html.escape、join、strip、startswith、_confidence_text、_minify_plan_html、_signal_zone、_fmt_price、_signal_targets |
| 复杂度 / 风险 | 分支 16；跨度 90 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9c21a8d1a7"></a>

#### FUN-9C21A8D1A7

| 设计项 | 说明 |
|---|---|
| 函数 | `render_rejected_plan_details` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1046` |
| 签名 | `render_rejected_plan_details(signals: list[dict], *, meta: dict \| None=None, validated_plans: list[dict] \| None=None)` |
| 参数 | `signals`（list[dict]）：交易信号集合<br>`meta`（dict \| None）：审计或处理元数据；默认值 `None`<br>`validated_plans`（list[dict] \| None）：已通过校验的交易计划集合；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`rejected_plan_details`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `s.get` → `enumerate` → `cards.append` → `_render_plan_card` → `row.get` → `upper` → `prop.get` → `any`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | s.get、enumerate、cards.append、_render_plan_card、str、row.get、upper、prop.get、any、len、_minify_plan_html、join |
| 复杂度 / 风险 | 分支 8；跨度 58 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3bfb666a67"></a>

#### FUN-3BFB666A67

| 设计项 | 说明 |
|---|---|
| 函数 | `render_primary_plan_focus` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1106` |
| 签名 | `render_primary_plan_focus(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`primary_plan_focus`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_display_plan_signals` → `report.get` → `next` → `enumerate` → `sig.get` → `_render_plan_card`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _display_plan_signals、report.get、next、enumerate、sig.get、len、_render_plan_card |
| 复杂度 / 风险 | 分支 2；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1308a20c4f"></a>

#### FUN-1308A20C4F

| 设计项 | 说明 |
|---|---|
| 函数 | `render_top_overview_row` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1119` |
| 签名 | `render_top_overview_row(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`top_overview_row`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `stage_source` → `render_source_badge` → `join` → `html.escape` → `conclusion_display_lines`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、stage_source、render_source_badge、join、html.escape、conclusion_display_lines、str |
| 复杂度 / 风险 | 分支 0；跨度 27 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d69f968c9e"></a>

#### FUN-D69F968C9E

| 设计项 | 说明 |
|---|---|
| 函数 | `render_tf_stack` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1148` |
| 签名 | `render_tf_stack(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`tf_stack`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `render_tf_panel`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、render_tf_panel |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1fb9420507"></a>

#### FUN-1FB9420507

| 设计项 | 说明 |
|---|---|
| 函数 | `render_bottom_row` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1156` |
| 签名 | `render_bottom_row(report: dict[str, Any], conclusion: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告<br>`conclusion`（dict[str, Any]）：由 `conclusion` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`bottom_row`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `join` → `html.escape` → `p.get` → `conclusion.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、join、html.escape、str、p.get、list、conclusion.get |
| 复杂度 / 风险 | 分支 0；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-2dd042625f"></a>

#### FUN-2DD042625F

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_zone` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1186` |
| 签名 | `_fmt_zone(items: list[dict], direction: str \| None=None, *, limit: int=5)` |
| 参数 | `items`（list[dict]）：输入项集合<br>`direction`（str \| None）：交易方向；默认值 `None`<br>`limit`（int）：返回或处理数量上限；默认值 `5` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_zone`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `i.get` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | i.get、join |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-eab2c95485"></a>

#### FUN-EAB2C95485

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_event_list` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1193` |
| 签名 | `_fmt_event_list(items: list[dict])` |
| 参数 | `items`（list[dict]）：输入项集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_event_list`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `i.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、i.get |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-48fc0fd2b1"></a>

#### FUN-48FC0FD2B1

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_prices` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1199` |
| 签名 | `_fmt_prices(prices: list[float])` |
| 参数 | `prices`（list[float]）：由 `prices` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_prices`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6d789b868b"></a>

#### FUN-6D789B868B

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_strong_weak` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1205` |
| 签名 | `_fmt_strong_weak(info: dict[str, Any])` |
| 参数 | `info`（dict[str, Any]）：由 `info` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_strong_weak`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `info.get` → `parts.append` → `join`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | info.get、parts.append、join |
| 复杂度 / 风险 | 分支 5；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-854dcce0eb"></a>

#### FUN-854DCCE0EB

| 设计项 | 说明 |
|---|---|
| 函数 | `render_tf_panel` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1218` |
| 签名 | `render_tf_panel(tf: str, info: dict[str, Any], *, compact: bool=False)` |
| 参数 | `tf`（str）：时间框架简称<br>`info`（dict[str, Any]）：由 `info` 表示的键值映射<br>`compact`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`tf_panel`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `TF_LABELS.get` → `TREND_CN.get` → `pd_map.get` → `info.get` → `_fmt_event_list` → `_fmt_zone` → `_fmt_prices` → `_fmt_strong_weak`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | TF_LABELS.get、TREND_CN.get、pd_map.get、info.get、_fmt_event_list、_fmt_zone、_fmt_prices、_fmt_strong_weak、join、ema.items |
| 复杂度 / 风险 | 分支 4；跨度 47 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ce51fb1d21"></a>

#### FUN-CE51FB1D21

| 设计项 | 说明 |
|---|---|
| 函数 | `render_narrative_section` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1267` |
| 签名 | `render_narrative_section(section: dict[str, Any] \| None)` |
| 参数 | `section`（dict[str, Any] \| None）：由 `section` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`narrative_section`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `section.get` → `NARRATIVE_SOURCE_CN.get` → `strip` → `rows.append` → `join` → `html.escape` → `_narrative_fallback_hint`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、section.get、NARRATIVE_SOURCE_CN.get、strip、rows.append、join、html.escape、_narrative_fallback_hint |
| 复杂度 / 风险 | 分支 10；跨度 29 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-18e3bf98ae"></a>

#### FUN-18E3BF98AE

| 设计项 | 说明 |
|---|---|
| 函数 | `_narrative_fallback_hint` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1298` |
| 签名 | `_narrative_fallback_hint(section: dict[str, Any])` |
| 参数 | `section`（dict[str, Any]）：由 `section` 表示的键值映射 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`narrative_fallback_hint`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `section.get` → `humanize_narrative_fallback` → `strip` → `html.escape`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、section.get、humanize_narrative_fallback、strip、html.escape |
| 复杂度 / 风险 | 分支 2；跨度 7 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1e810a3b0e"></a>

#### FUN-1E810A3B0E

| 设计项 | 说明 |
|---|---|
| 函数 | `render_key_levels` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1307` |
| 签名 | `render_key_levels(levels: list[dict])` |
| 参数 | `levels`（list[dict]）：候选价格水平集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染关键价格水平；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lv.get` → `items.append` → `join`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lv.get、items.append、join |
| 复杂度 / 风险 | 分支 3；跨度 14 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b460f224ca"></a>

#### FUN-B460F224CA

| 设计项 | 说明 |
|---|---|
| 函数 | `render_strategy_sections` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1323` |
| 签名 | `render_strategy_sections(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`strategy_sections`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `report.get` → `render_trading_plans` → `title.split` → `parts.append`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、report.get、render_trading_plans、title.split、parts.append |
| 复杂度 / 风险 | 分支 1；跨度 14 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-60b752029b"></a>

#### FUN-60B752029B

| 设计项 | 说明 |
|---|---|
| 函数 | `render_path_cards` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1340` |
| 签名 | `render_path_cards(paths: list[dict])` |
| 参数 | `paths`（list[dict]）：由 `paths` 表示的输入集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`path_cards`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f129f84b90"></a>

#### FUN-F129F84B90

| 设计项 | 说明 |
|---|---|
| 函数 | `render_calendar` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1348` |
| 签名 | `render_calendar(events: list[dict])` |
| 参数 | `events`（list[dict]）：事件集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`calendar`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `html.escape` → `e.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、html.escape、str、e.get |
| 复杂度 / 风险 | 分支 1；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-94c9558228"></a>

#### FUN-94C9558228

| 设计项 | 说明 |
|---|---|
| 函数 | `render_trading_plans` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1358` |
| 签名 | `render_trading_plans(signals: list[dict], *, meta: dict \| None=None, include_primary: bool=True, validated_plans: list[dict] \| None=None)` |
| 参数 | `signals`（list[dict]）：交易信号集合<br>`meta`（dict \| None）：审计或处理元数据；默认值 `None`<br>`include_primary`（bool）：控制对应行为是否启用的布尔值；默认值 `True`<br>`validated_plans`（list[dict] \| None）：已通过校验的交易计划集合；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`trading_plans`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `s.get` → `_display_plan_signals` → `any` → `row.get` → `html.escape` → `execution_banner` → `enumerate`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、meta.get、s.get、_display_plan_signals、any、row.get、html.escape、execution_banner、enumerate、len、sig.get、cards.append、_render_plan_card、render_rejected_plan_details、join |
| 复杂度 / 风险 | 分支 6；跨度 43 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py) · 直接动态测试 |

<a id="fun-5e89771732"></a>

#### FUN-5E89771732

| 设计项 | 说明 |
|---|---|
| 函数 | `render_liquidity` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1403` |
| 签名 | `render_liquidity(items: list[dict])` |
| 参数 | `items`（list[dict]）：输入项集合 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染流动性结构；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `label_map.get` → `lines.append` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | label_map.get、lines.append、join |
| 复杂度 / 风险 | 分支 1；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-aaaaeceb82"></a>

#### FUN-AAAAECEB82

| 设计项 | 说明 |
|---|---|
| 函数 | `render_footer` |
| 源码位置 | [src/viz/dashboard_components.py](../../../src/viz/dashboard_components.py) · `L1417` |
| 签名 | `render_footer(report: dict[str, Any])` |
| 参数 | `report`（dict[str, Any]）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`footer`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、join |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="unit-003f08decb"></a>

### UNIT-003F08DECB

**模块**：`src/viz/decision_page.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-003F08DECB |
| 源码 | [src/viz/decision_page.py](../../../src/viz/decision_page.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/decision_page.py` 的职责，通过 `render_live_generation_panel`、`render_llm_decision_page` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py) |
| 验证状态 | selected |

#### 函数导航

[_render_generation_and_llm_io](#fun-77f3e3eb2d) · [render_live_generation_panel](#fun-4d76920cc8) · [render_llm_decision_page](#fun-0871294ede)

<a id="fun-77f3e3eb2d"></a>

#### FUN-77F3E3EB2D

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_generation_and_llm_io` |
| 源码位置 | [src/viz/decision_page.py](../../../src/viz/decision_page.py) · `L20` |
| 签名 | `_render_generation_and_llm_io(*, steps: list[dict], records: list[dict], stage_sources: dict \| None=None, expand_last: bool=False, empty_steps_msg: str='暂无生成步骤记录', empty_io_msg: str='暂无 LLM 调用记录', live_streaming: bool=False, show_steps: bool=True)` |
| 参数 | `steps`（list[dict]）：执行步骤集合<br>`records`（list[dict]）：结构化记录集合<br>`stage_sources`（dict \| None）：由 `stage_sources` 表示的键值映射；默认值 `None`<br>`expand_last`（bool）：控制对应行为是否启用的布尔值；默认值 `False`<br>`empty_steps_msg`（str）：由 `empty_steps_msg` 表示的文本或标识；默认值 `'暂无生成步骤记录'`<br>`empty_io_msg`（str）：由 `empty_io_msg` 表示的文本或标识；默认值 `'暂无 LLM 调用记录'`<br>`live_streaming`（bool）：控制对应行为是否启用的布尔值；默认值 `False`<br>`show_steps`（bool）：执行步骤集合；默认值 `True` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`generation_and_llm_io`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `render_progress_steps` → `st.info` → `st.divider` → `merge_llm_io_with_stage_sources` → `partition_llm_records_for_live` → `render_live_llm_streams` → `render_llm_io_history`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | render_progress_steps、st.info、st.divider、merge_llm_io_with_stage_sources、partition_llm_records_for_live、render_live_llm_streams、render_llm_io_history |
| 复杂度 / 风险 | 分支 10；跨度 47 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4d76920cc8"></a>

#### FUN-4D76920CC8

| 设计项 | 说明 |
|---|---|
| 函数 | `render_live_generation_panel` |
| 源码位置 | [src/viz/decision_page.py](../../../src/viz/decision_page.py) · `L69` |
| 签名 | `render_live_generation_panel(live: dict, *, show_steps: bool=True)` |
| 参数 | `live`（dict）：由 `live` 表示的键值映射<br>`show_steps`（bool）：执行步骤集合；默认值 `True` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`live_generation_panel`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `live.get` → `st.tabs` → `_render_generation_and_llm_io` → `st.info`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | live.get、st.tabs、_render_generation_and_llm_io、st.info |
| 复杂度 / 风险 | 分支 0；跨度 25 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0871294ede"></a>

#### FUN-0871294EDE

| 设计项 | 说明 |
|---|---|
| 函数 | `render_llm_decision_page` |
| 源码位置 | [src/viz/decision_page.py](../../../src/viz/decision_page.py) · `L96` |
| 签名 | `render_llm_decision_page(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_decision_page`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `render_page_hero` → `st.markdown` → `render_agent_source_banner` → `st.tabs` → `render_agent_trace_panel` → `render_llm_panel` → `report.get` → `_render_generation_and_llm_io`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | render_page_hero、st.markdown、render_agent_source_banner、st.tabs、render_agent_trace_panel、render_llm_panel、report.get、_render_generation_and_llm_io、meta.get |
| 复杂度 / 风险 | 分支 0；跨度 25 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-9b624c52d7"></a>

### UNIT-9B624C52D7

**模块**：`src/viz/display_labels.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9B624C52D7 |
| 源码 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/display_labels.py` 的职责，通过 `format_report_branding`、`humanize_narrative_fallback`、`label_bias`、`label_action`、`label_trade_direction`、`label_risk_profile`、`label_position_scale`、`infer_trade_theme` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 10 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [label_trade_direction](#fun-32cef2320f) | 生成`label_trade_direction`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) |
| [infer_trade_theme](#fun-9cdbf9137f) | 生成`infer_trade_theme`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) |

#### 函数导航

[format_report_branding](#fun-7d9904747d) · [humanize_narrative_fallback](#fun-c22c609a56) · [label_bias](#fun-49e5ad57e6) · [label_action](#fun-5a683dd3d4) · [label_trade_direction](#fun-32cef2320f) · [label_risk_profile](#fun-3c82dc7efd) · [label_position_scale](#fun-32db70ee85) · [infer_trade_theme](#fun-9cdbf9137f) · [execution_banner](#fun-1e94d60636) · [conclusion_display_lines](#fun-493ef2091a)

<a id="fun-7d9904747d"></a>

#### FUN-7D9904747D

| 设计项 | 说明 |
|---|---|
| 函数 | `format_report_branding` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L44` |
| 签名 | `format_report_branding(text: object)` |
| 参数 | `text`（object）：输入文本 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`report_branding`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `out.replace`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | str、out.replace |
| 复杂度 / 风险 | 分支 1；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-c22c609a56"></a>

#### FUN-C22C609A56

| 设计项 | 说明 |
|---|---|
| 函数 | `humanize_narrative_fallback` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L52` |
| 签名 | `humanize_narrative_fallback(reason: object)` |
| 参数 | `reason`（object）：判定或拒绝原因 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`humanize_narrative_fallback`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `raw.startswith` → `raw.removeprefix`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、raw.startswith、raw.removeprefix |
| 复杂度 / 风险 | 分支 2；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-49e5ad57e6"></a>

#### FUN-49E5AD57E6

| 设计项 | 说明 |
|---|---|
| 函数 | `label_bias` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L67` |
| 签名 | `label_bias(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`label_bias`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `BIAS_CN.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、str、BIAS_CN.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-5a683dd3d4"></a>

#### FUN-5A683DD3D4

| 设计项 | 说明 |
|---|---|
| 函数 | `label_action` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L72` |
| 签名 | `label_action(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`label_action`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `ACTION_CN.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、str、ACTION_CN.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-32cef2320f"></a>

#### FUN-32CEF2320F

| 设计项 | 说明 |
|---|---|
| 函数 | `label_trade_direction` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L77` |
| 签名 | `label_trade_direction(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`label_trade_direction`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `TRADE_DIRECTION_CN.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、str、TRADE_DIRECTION_CN.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；高 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-3c82dc7efd"></a>

#### FUN-3C82DC7EFD

| 设计项 | 说明 |
|---|---|
| 函数 | `label_risk_profile` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L82` |
| 签名 | `label_risk_profile(value: object)` |
| 参数 | `value`（object）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`label_risk_profile`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `RISK_PROFILE_CN.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、str、RISK_PROFILE_CN.get |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-32db70ee85"></a>

#### FUN-32DB70EE85

| 设计项 | 说明 |
|---|---|
| 函数 | `label_position_scale` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L87` |
| 签名 | `label_position_scale(scale: object)` |
| 参数 | `scale`（object）：由调用方提供的 `scale` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`label_position_scale`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 4；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9cdbf9137f"></a>

#### FUN-9CDBF9137F

| 设计项 | 说明 |
|---|---|
| 函数 | `infer_trade_theme` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L107` |
| 签名 | `infer_trade_theme(*, theme: str='', direction: str='', direction_cn: str='')` |
| 参数 | `theme`（str）：由 `theme` 表示的文本或标识；默认值 `''`<br>`direction`（str）：交易方向；默认值 `''`<br>`direction_cn`（str）：由 `direction_cn` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`infer_trade_theme`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `strip` → `raw.strip` → `any`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、strip、str、raw.strip、any |
| 复杂度 / 风险 | 分支 3；跨度 16 行；高 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-1e94d60636"></a>

#### FUN-1E94D60636

| 设计项 | 说明 |
|---|---|
| 函数 | `execution_banner` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L125` |
| 签名 | `execution_banner(meta: dict \| None)` |
| 参数 | `meta`（dict \| None）：审计或处理元数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`execution_banner`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `strip` → `trigger.get` → `parts.append` → `decision.get` → `join` → `lower`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | meta.get、strip、str、trigger.get、parts.append、decision.get、join、lower |
| 复杂度 / 风险 | 分支 7；跨度 27 行；中 |
| 测试 / 验证 | [tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="fun-493ef2091a"></a>

#### FUN-493EF2091A

| 设计项 | 说明 |
|---|---|
| 函数 | `conclusion_display_lines` |
| 源码位置 | [src/viz/display_labels.py](../../../src/viz/display_labels.py) · `L154` |
| 签名 | `conclusion_display_lines(conclusion: dict[str, Any] \| None)` |
| 参数 | `conclusion`（dict[str, Any] \| None）：由 `conclusion` 表示的键值映射 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`conclusion_display_lines`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `conclusion.get` → `lines.append` → `header.startswith` → `summary.rstrip`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、conclusion.get、lines.append、header.startswith、summary.rstrip |
| 复杂度 / 风险 | 分支 4；跨度 16 行；中 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../../tests/unit/test_display_labels.py) · 直接动态测试 |

<a id="unit-8b3827f5ec"></a>

### UNIT-8B3827F5EC

**模块**：`src/viz/external_data_view.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8B3827F5EC |
| 源码 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/external_data_view.py` 的职责，通过 `external_snapshot_from_fetch`、`external_payload_from_report`、`render_external_data_content`、`render_external_data_page` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |
| 验证状态 | selected |

#### 函数导航

[external_snapshot_from_fetch](#fun-1e2febd33e) · [external_payload_from_report](#fun-73c9145028) · [_render_headline_list](#fun-75474c9286) · [_render_calendar_rows](#fun-15a26b9540) · [render_external_data_content](#fun-6cdbb0b77d) · [render_external_data_page](#fun-6b50c51729)

<a id="fun-1e2febd33e"></a>

#### FUN-1E2FEBD33E

| 设计项 | 说明 |
|---|---|
| 函数 | `external_snapshot_from_fetch` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L16` |
| 签名 | `external_snapshot_from_fetch(fetched: DataFetchResult)` |
| 参数 | `fetched`（DataFetchResult）：数据获取结果 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 根据`fetch`构建`external_snapshot`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parse_risk_events_calendar` → `h.to_dict` → `m.to_dict`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | parse_risk_events_calendar、list、h.to_dict、m.to_dict |
| 复杂度 / 风险 | 分支 1；跨度 20 行；中 |
| 测试 / 验证 | [tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="fun-73c9145028"></a>

#### FUN-73C9145028

| 设计项 | 说明 |
|---|---|
| 函数 | `external_payload_from_report` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L38` |
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
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L54` |
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
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L68` |
| 签名 | `_render_calendar_rows(payload: dict[str, Any])` |
| 参数 | `payload`（dict[str, Any]）：结构化载荷 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`calendar_rows`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `payload.get` → `join` → `html.escape` → `e.get` → `parse_risk_events_calendar`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | payload.get、join、html.escape、str、e.get、parse_risk_events_calendar |
| 复杂度 / 风险 | 分支 5；跨度 24 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6cdbb0b77d"></a>

#### FUN-6CDBB0B77D

| 设计项 | 说明 |
|---|---|
| 函数 | `render_external_data_content` |
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L94` |
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
| 源码位置 | [src/viz/external_data_view.py](../../../src/viz/external_data_view.py) · `L190` |
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
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/generation_state.py` 的职责，通过 `GenerationJob`、`purge_expired`、`access_job`、`get_job`、`create_job`、`drop_job`、`update_live` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
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
| 测试 / 验证 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_narrative_sections.py](../../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../../tests/unit/test_replay_llm_narrative.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

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
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/generation_worker.py` 的职责，通过 `compact_llm_io_for_live`、`ModuleSyncProgressReporter`、`format_generation_error`、`start_generation` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 16 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py)、[tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_module_sync_telemetry.py](../../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../../tests/unit/test_progress.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py)、[tests/unit/test_risk_gates.py](../../../tests/unit/test_risk_gates.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
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
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

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
| 测试 / 验证 | [tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_report_invariants.py](../../../tests/unit/test_report_invariants.py) · 直接动态测试 |

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
| 测试 / 验证 | [tests/integration/test_pipeline.py](../../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_live_progress_ui.py](../../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

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
| 测试 / 验证 | [tests/regression/test_doc_pipeline_sync.py](../../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_golden_report_benchmark.py](../../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_risk_gates.py](../../../tests/unit/test_risk_gates.py) · 直接动态测试 |

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
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |

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

<a id="unit-abbedfd349"></a>

### UNIT-ABBEDFD349

**模块**：`src/viz/lightweight_chart.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-ABBEDFD349 |
| 源码 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/lightweight_chart.py` 的职责，通过 `build_lightweight_chart_html`、`chart_iframe_height` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 15 / 15 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_tf_short](#fun-092ce9f86b) | 生成`tf_short`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | — |
| [_zone_title](#fun-f95e2508fa) | 生成`zone_title`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [_align_ts](#fun-3733752cf4) | 生成`align_ts`结果；返回 `pd.Timestamp` 类型结果。 | 未检测到直接副作用 | — |
| [_to_unix](#fun-8e3f539bdd) | 计算`to_unix`；返回 `int` 类型结果。 | 未检测到直接副作用 | — |
| [_bar_delta](#fun-44a30a06ef) | 生成`bar_delta`结果；返回 `pd.Timedelta` 类型结果。 | 未检测到直接副作用 | — |
| [_zone_future_end](#fun-f4069a84ad) | 生成`zone_future_end`结果；返回 `pd.Timestamp` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [_zone_box_data](#fun-fa95eaff48) | 构建`zone_box_data`；返回 `list[dict[str, float \| int]]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [_ob_display_end_time](#fun-19260207ff) | 生成`ob_display_end_time`结果；返回 `pd.Timestamp` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [_append_zone_box](#fun-ff5b159787) | 追加`zone_box`；无返回值（None）。 | 未检测到直接副作用 | — |
| [_append_lux_fvg](#fun-3ce37e5cc0) | 追加`lux_fvg`；无返回值（None）。 | 未检测到直接副作用 | — |
| [_append_lux_ob](#fun-c590a6c0d5) | 追加`lux_ob`；无返回值（None）。 | 未检测到直接副作用 | — |
| [_serialize_overlays](#fun-af5e00ed83) | 序列化`overlays`；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [_build_projections](#fun-501852c2a0) | 构建`projections`；返回 `list[dict[str, Any]]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [build_lightweight_chart_html](#fun-540615a0fd) | 构建Lightweight Charts 交互图表 HTML；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| [chart_iframe_height](#fun-ac67fe2b86) | 计算`chart_iframe_height`；返回 `int` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) |

#### 函数导航

[_tf_short](#fun-092ce9f86b) · [_zone_title](#fun-f95e2508fa) · [_align_ts](#fun-3733752cf4) · [_to_unix](#fun-8e3f539bdd) · [_bar_delta](#fun-44a30a06ef) · [_zone_future_end](#fun-f4069a84ad) · [_zone_box_data](#fun-fa95eaff48) · [_ob_display_end_time](#fun-19260207ff) · [_append_zone_box](#fun-ff5b159787) · [_append_lux_fvg](#fun-3ce37e5cc0) · [_append_lux_ob](#fun-c590a6c0d5) · [_serialize_overlays](#fun-af5e00ed83) · [_build_projections](#fun-501852c2a0) · [build_lightweight_chart_html](#fun-540615a0fd) · [chart_iframe_height](#fun-ac67fe2b86)

<a id="fun-092ce9f86b"></a>

#### FUN-092CE9F86B

| 设计项 | 说明 |
|---|---|
| 函数 | `_tf_short` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L115` |
| 签名 | `_tf_short(timeframe: str)` |
| 参数 | `timeframe`（str）：行情时间框架 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`tf_short`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `TF_SHORT.get` → `timeframe.upper`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | TF_SHORT.get、timeframe.upper |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f95e2508fa"></a>

#### FUN-F95E2508FA

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_title` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L119` |
| 签名 | `_zone_title(kind: str, direction: str, low: float, high: float, *, half: str \| None=None, source_tf: str \| None=None)` |
| 参数 | `kind`（str）：类别标识<br>`direction`（str）：交易方向<br>`low`（float）：最低价序列或下界<br>`high`（float）：最高价序列或上界<br>`half`（str \| None）：由调用方提供的 `half` 输入对象；默认值 `None`<br>`source_tf`（str \| None）：时间框架简称；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`zone_title`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `_tf_short`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、round、_tf_short |
| 复杂度 / 风险 | 分支 5；跨度 21 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-3733752cf4"></a>

#### FUN-3733752CF4

| 设计项 | 说明 |
|---|---|
| 函数 | `_align_ts` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L142` |
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
| 复杂度 / 风险 | 分支 3；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8e3f539bdd"></a>

#### FUN-8E3F539BDD

| 设计项 | 说明 |
|---|---|
| 函数 | `_to_unix` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L153` |
| 签名 | `_to_unix(ts: pd.Timestamp)` |
| 参数 | `ts`（pd.Timestamp）：由调用方提供的 `ts` 输入对象 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`to_unix`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `timestamp` → `pd.Timestamp`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、timestamp、pd.Timestamp |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-44a30a06ef"></a>

#### FUN-44A30A06EF

| 设计项 | 说明 |
|---|---|
| 函数 | `_bar_delta` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L157` |
| 签名 | `_bar_delta(plot_df: pd.DataFrame)` |
| 参数 | `plot_df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `pd.Timedelta` 类型结果 |
| 职责 | 生成`bar_delta`结果；返回 `pd.Timedelta` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.Timedelta`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Timedelta` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、pd.Timedelta |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f4069a84ad"></a>

#### FUN-F4069A84AD

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_future_end` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L163` |
| 签名 | `_zone_future_end(plot_df: pd.DataFrame, start_time: pd.Timestamp)` |
| 参数 | `plot_df`（pd.DataFrame）：输入数据表<br>`start_time`（pd.Timestamp）：事件或数据时间 |
| 返回 | 返回 `pd.Timestamp` 类型结果 |
| 职责 | 生成`zone_future_end`结果；返回 `pd.Timestamp` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_bar_delta` → `max` → `_align_ts`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Timestamp` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _bar_delta、max、len、_align_ts |
| 复杂度 / 风险 | 分支 0；跨度 5 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-fa95eaff48"></a>

#### FUN-FA95EAFF48

| 设计项 | 说明 |
|---|---|
| 函数 | `_zone_box_data` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L170` |
| 签名 | `_zone_box_data(plot_df: pd.DataFrame, start_time: pd.Timestamp, high: float, *, end_time: pd.Timestamp \| None=None)` |
| 参数 | `plot_df`（pd.DataFrame）：输入数据表<br>`start_time`（pd.Timestamp）：事件或数据时间<br>`high`（float）：最高价序列或上界<br>`end_time`（pd.Timestamp \| None）：事件或数据时间；默认值 `None` |
| 返回 | 返回 `list[dict[str, float \| int]]` 类型结果 |
| 职责 | 构建`zone_box_data`；返回 `list[dict[str, float \| int]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_align_ts` → `_zone_future_end` → `round` → `_to_unix`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, float \| int]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _align_ts、_zone_future_end、round、_to_unix |
| 复杂度 / 风险 | 分支 2；跨度 21 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-19260207ff"></a>

#### FUN-19260207FF

| 设计项 | 说明 |
|---|---|
| 函数 | `_ob_display_end_time` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L193` |
| 签名 | `_ob_display_end_time(plot_df: pd.DataFrame)` |
| 参数 | `plot_df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `pd.Timestamp` 类型结果 |
| 职责 | 生成`ob_display_end_time`结果；返回 `pd.Timestamp` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_zone_future_end`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.Timestamp` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _zone_future_end |
| 复杂度 / 风险 | 分支 0；跨度 3 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-ff5b159787"></a>

#### FUN-FF5B159787

| 设计项 | 说明 |
|---|---|
| 函数 | `_append_zone_box` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L198` |
| 签名 | `_append_zone_box(zones: list[dict[str, Any]], *, kind: str, direction: str, low: float, high: float, start_time: pd.Timestamp, plot_df: pd.DataFrame, source_tf: str, colors: dict[str, str], title: str \| None=None, show_label: bool=True, end_time: pd.Timestamp \| None=None)` |
| 参数 | `zones`（list[dict[str, Any]]）：价格区域集合<br>`kind`（str）：类别标识<br>`direction`（str）：交易方向<br>`low`（float）：最低价序列或下界<br>`high`（float）：最高价序列或上界<br>`start_time`（pd.Timestamp）：事件或数据时间<br>`plot_df`（pd.DataFrame）：输入数据表<br>`source_tf`（str）：时间框架简称<br>`colors`（dict[str, str]）：由 `colors` 表示的键值映射<br>`title`（str \| None）：由调用方提供的 `title` 输入对象；默认值 `None`<br>`show_label`（bool）：展示或分类标签；默认值 `True`<br>`end_time`（pd.Timestamp \| None）：事件或数据时间；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 追加`zone_box`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `zones.append` → `round` → `_zone_box_data`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | zones.append、round、_zone_box_data |
| 复杂度 / 风险 | 分支 2；跨度 29 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3ce37e5cc0"></a>

#### FUN-3CE37E5CC0

| 设计项 | 说明 |
|---|---|
| 函数 | `_append_lux_fvg` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L229` |
| 签名 | `_append_lux_fvg(zones: list[dict[str, Any]], fvg, plot_df: pd.DataFrame, source_tf: str)` |
| 参数 | `zones`（list[dict[str, Any]]）：价格区域集合<br>`fvg`（实现约定类型）：由调用方提供的 `fvg` 输入对象<br>`plot_df`（pd.DataFrame）：输入数据表<br>`source_tf`（str）：时间框架简称 |
| 返回 | 无返回值（None） |
| 职责 | 追加`lux_fvg`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_zone_future_end` → `_zone_title` → `_append_zone_box`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_zone_future_end、_zone_title、_append_zone_box |
| 复杂度 / 风险 | 分支 1；跨度 40 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c590a6c0d5"></a>

#### FUN-C590A6C0D5

| 设计项 | 说明 |
|---|---|
| 函数 | `_append_lux_ob` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L271` |
| 签名 | `_append_lux_ob(zones: list[dict[str, Any]], ob, plot_df: pd.DataFrame, source_tf: str, *, end_time: pd.Timestamp)` |
| 参数 | `zones`（list[dict[str, Any]]）：价格区域集合<br>`ob`（实现约定类型）：由调用方提供的 `ob` 输入对象<br>`plot_df`（pd.DataFrame）：输入数据表<br>`source_tf`（str）：时间框架简称<br>`end_time`（pd.Timestamp）：事件或数据时间 |
| 返回 | 无返回值（None） |
| 职责 | 追加`lux_ob`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_append_zone_box` → `_zone_title`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _append_zone_box、_zone_title |
| 复杂度 / 风险 | 分支 1；跨度 22 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-af5e00ed83"></a>

#### FUN-AF5E00ED83

| 设计项 | 说明 |
|---|---|
| 函数 | `_serialize_overlays` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L295` |
| 签名 | `_serialize_overlays(analysis: TimeframeAnalysis, report: dict[str, Any], plot_df: pd.DataFrame, *, timeframe: str='1h', include_projections: bool=True, variant: str='main')` |
| 参数 | `analysis`（TimeframeAnalysis）：当前分析结果<br>`report`（dict[str, Any]）：分析报告<br>`plot_df`（pd.DataFrame）：输入数据表<br>`timeframe`（str）：行情时间框架；默认值 `'1h'`<br>`include_projections`（bool）：控制对应行为是否启用的布尔值；默认值 `True`<br>`variant`（str）：由 `variant` 表示的文本或标识；默认值 `'main'` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 序列化`overlays`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `visible_active_fvgs` → `_append_lux_fvg` → `visible_order_blocks` → `_ob_display_end_time` → `_append_lux_ob` → `chart_sr_levels` → `price_lines.extend` → `visible_sr_price_lines`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | visible_active_fvgs、_append_lux_fvg、visible_order_blocks、_ob_display_end_time、_append_lux_ob、chart_sr_levels、price_lines.extend、visible_sr_price_lines、float、_build_projections |
| 复杂度 / 风险 | 分支 6；跨度 46 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-501852c2a0"></a>

#### FUN-501852C2A0

| 设计项 | 说明 |
|---|---|
| 函数 | `_build_projections` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L343` |
| 签名 | `_build_projections(plot_df: pd.DataFrame, report: dict[str, Any] \| None, *, timeframe: str='5m')` |
| 参数 | `plot_df`（pd.DataFrame）：输入数据表<br>`report`（dict[str, Any] \| None）：分析报告<br>`timeframe`（str）：行情时间框架；默认值 `'5m'` |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`projections`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_PROJECTION_STEP_GAP.get` → `pd.Timedelta` → `enumerate` → `points.append` → `_to_unix` → `round` → `lines.append`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _PROJECTION_STEP_GAP.get、pd.Timedelta、enumerate、points.append、_to_unix、round、float、len、lines.append |
| 复杂度 / 风险 | 分支 5；跨度 27 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-540615a0fd"></a>

#### FUN-540615A0FD

| 设计项 | 说明 |
|---|---|
| 函数 | `build_lightweight_chart_html` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L372` |
| 签名 | `build_lightweight_chart_html(df: pd.DataFrame, analysis: TimeframeAnalysis \| None=None, report: dict[str, Any] \| None=None, *, timeframe: str='1h', symbol: str='XAUUSD', symbol_name: str='黄金/美元', exchange: str='OANDA', height: int \| None=None, bars: int \| None=None, variant: str='main', watermark: str \| None=None, show_projections: bool \| None=None)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`analysis`（TimeframeAnalysis \| None）：当前分析结果；默认值 `None`<br>`report`（dict[str, Any] \| None）：分析报告；默认值 `None`<br>`timeframe`（str）：行情时间框架；默认值 `'1h'`<br>`symbol`（str）：交易品种代码；默认值 `'XAUUSD'`<br>`symbol_name`（str）：对象名称；默认值 `'黄金/美元'`<br>`exchange`（str）：由 `exchange` 表示的文本或标识；默认值 `'OANDA'`<br>`height`（int \| None）：由调用方提供的 `height` 输入对象；默认值 `None`<br>`bars`（int \| None）：K 线记录集合；默认值 `None`<br>`variant`（str）：由 `variant` 表示的文本或标识；默认值 `'main'`<br>`watermark`（str \| None）：由调用方提供的 `watermark` 输入对象；默认值 `None`<br>`show_projections`（bool \| None）：由调用方提供的 `show_projections` 输入对象；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 构建Lightweight Charts 交互图表 HTML；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `CHART_VARIANTS.get` → `preset.get` → `copy` → `df.tail` → `TF_LABELS.get` → `get` → `plot_df.iterrows` → `_to_unix`；包含 42 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | CHART_VARIANTS.get、int、bool、preset.get、float、copy、df.tail、len、TF_LABELS.get、get、plot_df.iterrows、_to_unix、candles.append、round、row.get、volumes.append、LINE_COLORS.items、pd.notna、points.append、_serialize_overlays |
| 复杂度 / 风险 | 分支 42；跨度 478 行；高 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="fun-ac67fe2b86"></a>

#### FUN-AC67FE2B86

| 设计项 | 说明 |
|---|---|
| 函数 | `chart_iframe_height` |
| 源码位置 | [src/viz/lightweight_chart.py](../../../src/viz/lightweight_chart.py) · `L852` |
| 签名 | `chart_iframe_height(variant: str='main', height: int \| None=None)` |
| 参数 | `variant`（str）：由 `variant` 表示的文本或标识；默认值 `'main'`<br>`height`（int \| None）：由调用方提供的 `height` 输入对象；默认值 `None` |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`chart_iframe_height`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `CHART_VARIANTS.get` → `preset.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | CHART_VARIANTS.get、int、preset.get |
| 复杂度 / 风险 | 分支 3；跨度 9 行；高 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="unit-f5c8e9bf82"></a>

### UNIT-F5C8E9BF82

**模块**：`src/viz/llm_meta.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F5C8E9BF82 |
| 源码 | [src/viz/llm_meta.py](../../../src/viz/llm_meta.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/llm_meta.py` 的职责，通过 `format_latency_ms`、`dedupe_llm_io_records`、`merge_llm_io_with_stage_sources`、`stage_llm_caption` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[format_latency_ms](#fun-58b0856420) · [dedupe_llm_io_records](#fun-2eacce73e8) · [merge_llm_io_with_stage_sources](#fun-cfe09c603f) · [stage_llm_caption](#fun-f3a683bcda)

<a id="fun-58b0856420"></a>

#### FUN-58B0856420

| 设计项 | 说明 |
|---|---|
| 函数 | `format_latency_ms` |
| 源码位置 | [src/viz/llm_meta.py](../../../src/viz/llm_meta.py) · `L8` |
| 签名 | `format_latency_ms(ms: int \| None)` |
| 参数 | `ms`（int \| None）：由调用方提供的 `ms` 输入对象 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`latency_ms`；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 2；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2eacce73e8"></a>

#### FUN-2EACCE73E8

| 设计项 | 说明 |
|---|---|
| 函数 | `dedupe_llm_io_records` |
| 源码位置 | [src/viz/llm_meta.py](../../../src/viz/llm_meta.py) · `L16` |
| 签名 | `dedupe_llm_io_records(records: list[dict])` |
| 参数 | `records`（list[dict]）：结构化记录集合 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 去重LLM 输入输出记录；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rec.get` → `order.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rec.get、order.append |
| 复杂度 / 风险 | 分支 2；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cfe09c603f"></a>

#### FUN-CFE09C603F

| 设计项 | 说明 |
|---|---|
| 函数 | `merge_llm_io_with_stage_sources` |
| 源码位置 | [src/viz/llm_meta.py](../../../src/viz/llm_meta.py) · `L28` |
| 签名 | `merge_llm_io_with_stage_sources(records: list[dict], stage_sources: dict)` |
| 参数 | `records`（list[dict]）：结构化记录集合<br>`stage_sources`（dict）：由 `stage_sources` 表示的键值映射 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 合并`llm_io_with_stage_sources`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `dedupe_llm_io_records` → `rec.get` → `get` → `stage_sources.get` → `trace.get` → `merged.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | dedupe_llm_io_records、rec.get、get、stage_sources.get、dict、trace.get、merged.append |
| 复杂度 / 风险 | 分支 3；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f3a683bcda"></a>

#### FUN-F3A683BCDA

| 设计项 | 说明 |
|---|---|
| 函数 | `stage_llm_caption` |
| 源码位置 | [src/viz/llm_meta.py](../../../src/viz/llm_meta.py) · `L43` |
| 签名 | `stage_llm_caption(stage_sources: dict, stage: str)` |
| 参数 | `stage_sources`（dict）：由 `stage_sources` 表示的键值映射<br>`stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stage_llm_caption`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `stage_sources.get` → `short_model_name` → `trace.get` → `format_latency_ms`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、stage_sources.get、short_model_name、trace.get、format_latency_ms |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-e782e5b762"></a>

### UNIT-E782E5B762

**模块**：`src/viz/llm_view.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E782E5B762 |
| 源码 | [src/viz/llm_view.py](../../../src/viz/llm_view.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/llm_view.py` 的职责，通过 `render_llm_panel`、`render_llm_sidebar` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[render_llm_panel](#fun-2bb63dcf3d) · [render_llm_sidebar](#fun-d200c30db1)

<a id="fun-2bb63dcf3d"></a>

#### FUN-2BB63DCF3D

| 设计项 | 说明 |
|---|---|
| 函数 | `render_llm_panel` |
| 源码位置 | [src/viz/llm_view.py](../../../src/viz/llm_view.py) · `L10` |
| 签名 | `render_llm_panel(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_panel`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `st.caption` → `llm.get` → `st.error` → `meta.get` → `get` → `strip` → `reliability.get`；包含 17 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、st.caption、llm.get、st.error、bool、meta.get、get、strip、str、reliability.get、st.info、st.markdown、st.write、action_plan.split、line.strip、top_audit.get、st.columns |
| 复杂度 / 风险 | 分支 17；跨度 66 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d200c30db1"></a>

#### FUN-D200C30DB1

| 设计项 | 说明 |
|---|---|
| 函数 | `render_llm_sidebar` |
| 源码位置 | [src/viz/llm_view.py](../../../src/viz/llm_view.py) · `L78` |
| 签名 | `render_llm_sidebar(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_sidebar`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `render_llm_panel`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | render_llm_panel |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-d8ab5e90b4"></a>

### UNIT-D8AB5E90B4

**模块**：`src/viz/page_layout.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D8AB5E90B4 |
| 源码 | [src/viz/page_layout.py](../../../src/viz/page_layout.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/page_layout.py` 的职责，通过 `render_page_hero` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py) |
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
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py) · 直接动态测试 |

<a id="unit-87ec9bc982"></a>

### UNIT-87EC9BC982

**模块**：`src/viz/pipeline_progress.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-87EC9BC982 |
| 源码 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/pipeline_progress.py` 的职责，通过 `pipeline_progress_headline`、`render_progress_steps`、`is_streaming_llm_record`、`partition_llm_records_for_live`、`render_live_llm_status_lightweight`、`render_live_llm_streams`、`render_llm_io_history`、`StreamlitProgressReporter` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 19 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [pipeline_progress_headline](#fun-0b8c70cae4) | 生成`pipeline_progress_headline`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py) |

#### 函数导航

[pipeline_progress_headline](#fun-0b8c70cae4) · [_format_step](#fun-c1629a4de1) · [render_progress_steps](#fun-311ae39ba2) · [_render_llm_io_text](#fun-ad1fa5e595) · [_render_llm_output_panel](#fun-7dcbcf149d) · [is_streaming_llm_record](#fun-17c606facf) · [partition_llm_records_for_live](#fun-d82430a62e) · [render_live_llm_status_lightweight](#fun-4d69bae96d) · [render_live_llm_streams](#fun-c7365fb901) · [_filter_llm_io_records](#fun-c8f614ea56) · [render_llm_io_history](#fun-fa5a1c7f41) · [StreamlitProgressReporter.__init__](#fun-0d15b0afcc) · [StreamlitProgressReporter._paint](#fun-cf6dff11c9) · [StreamlitProgressReporter._on_change](#fun-518e29c44c) · [StreamlitProgressReporter._on_llm_begin](#fun-25b5bbb645) · [StreamlitProgressReporter.run_llm_stream](#fun-4d2f1f7990) · [StreamlitProgressReporter.run_llm_stream._gen](#fun-f822a4e8cf) · [StreamlitProgressReporter._on_llm_end](#fun-85e51e2ba9) · [StreamlitProgressReporter.complete](#fun-a18a4822f2)

<a id="fun-0b8c70cae4"></a>

#### FUN-0B8C70CAE4

| 设计项 | 说明 |
|---|---|
| 函数 | `pipeline_progress_headline` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L21` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L44` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L60` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L76` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L89` |
| 签名 | `_render_llm_output_panel(*, stage: str, output: str, error: str \| None=None, json_height: int=320, widget_key: str \| None=None)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`output`（str）：输出对象或输出路径<br>`error`（str \| None）：错误信息或异常对象；默认值 `None`<br>`json_height`（int）：由 `json_height` 表示的数值参数；默认值 `320`<br>`widget_key`（str \| None）：索引键；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`llm_output_panel`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.error` → `st.caption` → `_render_llm_io_text` → `format_llm_output` → `st.markdown` → `format_llm_narrative`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.error、st.caption、_render_llm_io_text、format_llm_output、len、st.markdown、format_llm_narrative |
| 复杂度 / 风险 | 分支 2；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-17c606facf"></a>

#### FUN-17C606FACF

| 设计项 | 说明 |
|---|---|
| 函数 | `is_streaming_llm_record` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L113` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L122` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L130` |
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
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py) · 直接动态测试 |

<a id="fun-c7365fb901"></a>

#### FUN-C7365FB901

| 设计项 | 说明 |
|---|---|
| 函数 | `render_live_llm_streams` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L150` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L186` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L205` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L258` |
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
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-cf6dff11c9"></a>

#### FUN-CF6DFF11C9

| 设计项 | 说明 |
|---|---|
| 函数 | `StreamlitProgressReporter._paint` |
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L266` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L271` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L283` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L305` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L310` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L319` |
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
| 源码位置 | [src/viz/pipeline_progress.py](../../../src/viz/pipeline_progress.py) · `L342` |
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
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_report_invariant_gate.py](../../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="unit-a63d87a7bb"></a>

### UNIT-A63D87A7BB

**模块**：`src/viz/replay_loader.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A63D87A7BB |
| 源码 | [src/viz/replay_loader.py](../../../src/viz/replay_loader.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/replay_loader.py` 的职责，通过 `load_replay_bundle` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) |
| 验证状态 | selected |

#### 函数导航

[load_replay_bundle](#fun-2838d79653)

<a id="fun-2838d79653"></a>

#### FUN-2838D79653

| 设计项 | 说明 |
|---|---|
| 函数 | `load_replay_bundle` |
| 源码位置 | [src/viz/replay_loader.py](../../../src/viz/replay_loader.py) · `L14` |
| 签名 | `load_replay_bundle(run_config: RunConfig)` |
| 参数 | `run_config`（RunConfig）：运行配置 |
| 返回 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果 |
| 职责 | 加载`replay_bundle`；返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `run_config.normalized` → `ValueError` → `inspect_run_archive` → `join` → `load_bundle` → `load_forensic_bundle`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | run_config.normalized、ValueError、inspect_run_archive、join、load_bundle、load_forensic_bundle |
| 复杂度 / 风险 | 分支 5；跨度 21 行；中 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |

<a id="unit-4e47421947"></a>

### UNIT-4E47421947

**模块**：`src/viz/report_views.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4E47421947 |
| 源码 | [src/viz/report_views.py](../../../src/viz/report_views.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/report_views.py` 的职责，通过 `render_institutional_report`、`render_strategy_map` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 4 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [render_institutional_report](#fun-c6d32e207c) | 渲染`institutional_report`；无返回值（None）。 | 未检测到直接副作用 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) |

#### 函数导航

[_embed_chart](#fun-6a488ebc85) · [_top_text_panel](#fun-d4c3b6faa5) · [render_institutional_report](#fun-c6d32e207c) · [render_strategy_map](#fun-3c8ba1f22e)

<a id="fun-6a488ebc85"></a>

#### FUN-6A488EBC85

| 设计项 | 说明 |
|---|---|
| 函数 | `_embed_chart` |
| 源码位置 | [src/viz/report_views.py](../../../src/viz/report_views.py) · `L31` |
| 签名 | `_embed_chart(data, analysis, report, tf, *, variant: str='main', watermark=None, projections=True, show_title: bool=True, iframe_height: int \| None=None, chart_height: int \| None=None)` |
| 参数 | `data`（实现约定类型）：输入数据<br>`analysis`（实现约定类型）：当前分析结果<br>`report`（实现约定类型）：分析报告<br>`tf`（实现约定类型）：时间框架简称<br>`variant`（str）：由 `variant` 表示的文本或标识；默认值 `'main'`<br>`watermark`（实现约定类型）：由调用方提供的 `watermark` 输入对象；默认值 `None`<br>`projections`（实现约定类型）：由调用方提供的 `projections` 输入对象；默认值 `True`<br>`show_title`（bool）：控制对应行为是否启用的布尔值；默认值 `True`<br>`iframe_height`（int \| None）：由调用方提供的 `iframe_height` 输入对象；默认值 `None`<br>`chart_height`（int \| None）：由调用方提供的 `chart_height` 输入对象；默认值 `None` |
| 返回 | 无返回值（隐式 None） |
| 职责 | 执行`embed_chart`处理；无返回值（隐式 None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown` → `get` → `chart_iframe_height` → `max` → `st.iframe` → `build_lightweight_chart_html`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（隐式 None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown、get、chart_iframe_height、max、st.iframe、build_lightweight_chart_html |
| 复杂度 / 风险 | 分支 3；跨度 39 行；低 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-d4c3b6faa5"></a>

#### FUN-D4C3B6FAA5

| 设计项 | 说明 |
|---|---|
| 函数 | `_top_text_panel` |
| 源码位置 | [src/viz/report_views.py](../../../src/viz/report_views.py) · `L72` |
| 签名 | `_top_text_panel(title: str, body_html: str)` |
| 参数 | `title`（str）：由 `title` 表示的文本或标识<br>`body_html`（str）：由 `body_html` 表示的文本或标识 |
| 返回 | 无返回值（None） |
| 职责 | 执行`top_text_panel`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c6d32e207c"></a>

#### FUN-C6D32E207C

| 设计项 | 说明 |
|---|---|
| 函数 | `render_institutional_report` |
| 源码位置 | [src/viz/report_views.py](../../../src/viz/report_views.py) · `L79` |
| 签名 | `render_institutional_report(report, data, analyses, *, hide_title: bool=False)` |
| 参数 | `report`（实现约定类型）：分析报告<br>`data`（实现约定类型）：输入数据<br>`analyses`（实现约定类型）：各时间框架分析结果<br>`hide_title`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 无返回值（None） |
| 职责 | 渲染`institutional_report`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `format_utc8` → `pipeline_status_label` → `st.warning` → `st.info` → `format_archived_run_config` → `st.caption`；包含 12 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、format_utc8、bool、pipeline_status_label、st.warning、st.info、format_archived_run_config、st.caption、st.markdown、format_report_branding、render_final_decision_banner、render_decision_summary、st.columns、narratives.get、render_narrative_section、join、_top_text_panel、item.get、conclusion_display_lines |
| 复杂度 / 风险 | 分支 12；跨度 153 行；高 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-3c8ba1f22e"></a>

#### FUN-3C8BA1F22E

| 设计项 | 说明 |
|---|---|
| 函数 | `render_strategy_map` |
| 源码位置 | [src/viz/report_views.py](../../../src/viz/report_views.py) · `L234` |
| 签名 | `render_strategy_map(report, data, analyses)` |
| 参数 | `report`（实现约定类型）：分析报告<br>`data`（实现约定类型）：输入数据<br>`analyses`（实现约定类型）：各时间框架分析结果 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`strategy_map`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown` → `format_report_branding` → `render_final_decision_banner` → `render_decision_summary` → `st.columns` → `_embed_chart` → `render_key_levels` → `report.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown、format_report_branding、render_final_decision_banner、render_decision_summary、st.columns、_embed_chart、render_key_levels、report.get、render_strategy_sections、render_footer |
| 复杂度 / 风险 | 分支 1；跨度 21 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-ee18de86b2"></a>

### UNIT-EE18DE86B2

**模块**：`src/viz/run_config_panel.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EE18DE86B2 |
| 源码 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/run_config_panel.py` 的职责，通过 `mode_label_to_value`、`mode_value_to_label`、`selected_run_config`、`render_sidebar_replay`、`render_run_config_panel` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 20 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_render_archive_import_only](#fun-302db0d19b) | 渲染`archive_import_only`；无返回值（None）。 | 未检测到直接副作用 | — |
| [_render_archive_transfer_controls](#fun-c8de0e7538) | 渲染`archive_transfer_controls`；可能影响外部接口；无返回值（None）。 | 外部接口 I/O | — |

#### 函数导航

[mode_label_to_value](#fun-6478ef0ef9) · [mode_value_to_label](#fun-9df4825093) · [_apply_widget_state_from_run_config](#fun-a29290a4a9) · [_seed_run_config_widgets_if_needed](#fun-368d7e0325) · [_ensure_default_replay_run_id](#fun-dfbacecc76) · [_set_all_agent_llm_widgets](#fun-e60fed8b36) · [_analyst_checkbox_state](#fun-67955d3f49) · [_sync_stage_widgets_from_mode_preset](#fun-ac911b85c4) · [_on_advanced_toggle](#fun-fc0e4c8d13) · [_apply_mode_preset_to_widgets](#fun-4562c0a4e8) · [_advanced_core_stages_all_off](#fun-b8de98a787) · [selected_run_config](#fun-4712d21b11) · [_render_run_mode_guide](#fun-a56ca0818f) · [_on_open_replay_config](#fun-d6653fc459) · [render_sidebar_replay](#fun-8d7f136545) · [_render_replay_controls](#fun-fea885853a) · [_render_archive_import_only](#fun-302db0d19b) · [_render_archive_transfer_controls](#fun-c8de0e7538) · [_render_run_config_advanced_controls](#fun-5b83f91b90) · [render_run_config_panel](#fun-de6787dacc)

<a id="fun-6478ef0ef9"></a>

#### FUN-6478EF0EF9

| 设计项 | 说明 |
|---|---|
| 函数 | `mode_label_to_value` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L45` |
| 签名 | `mode_label_to_value(label: str)` |
| 参数 | `label`（str）：展示或分类标签 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`mode_label_to_value`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_MODE_LABEL_TO_VALUE.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _MODE_LABEL_TO_VALUE.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9df4825093"></a>

#### FUN-9DF4825093

| 设计项 | 说明 |
|---|---|
| 函数 | `mode_value_to_label` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L49` |
| 签名 | `mode_value_to_label(value: str)` |
| 参数 | `value`（str）：待处理值 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`mode_value_to_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_MODE_VALUE_TO_LABEL.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _MODE_VALUE_TO_LABEL.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a29290a4a9"></a>

#### FUN-A29290A4A9

| 设计项 | 说明 |
|---|---|
| 函数 | `_apply_widget_state_from_run_config` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L53` |
| 签名 | `_apply_widget_state_from_run_config(config: RunConfig)` |
| 参数 | `config`（RunConfig）：运行配置 |
| 返回 | 无返回值（None） |
| 职责 | 根据运行配置构建`apply_widget_state`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `items` → `run_config_widget_state`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | items、run_config_widget_state |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-368d7e0325"></a>

#### FUN-368D7E0325

| 设计项 | 说明 |
|---|---|
| 函数 | `_seed_run_config_widgets_if_needed` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L58` |
| 签名 | `_seed_run_config_widgets_if_needed(seed: RunConfig, *, force: bool=False)` |
| 参数 | `seed`（RunConfig）：由调用方提供的 `seed` 输入对象<br>`force`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 无返回值（None） |
| 职责 | 执行`seed_config_widgets_if_needed`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `run_config_widget_state` → `state.pop` → `state.items` → `_ensure_default_replay_run_id`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、bool、run_config_widget_state、state.pop、state.items、_ensure_default_replay_run_id |
| 复杂度 / 风险 | 分支 4；跨度 13 行；低 |
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py) · 直接动态测试 |

<a id="fun-dfbacecc76"></a>

#### FUN-DFBACECC76

| 设计项 | 说明 |
|---|---|
| 函数 | `_ensure_default_replay_run_id` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L73` |
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
| 复杂度 / 风险 | 分支 2；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e60fed8b36"></a>

#### FUN-E60FED8B36

| 设计项 | 说明 |
|---|---|
| 函数 | `_set_all_agent_llm_widgets` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L86` |
| 签名 | `_set_all_agent_llm_widgets(select: bool)` |
| 参数 | `select`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 无返回值（None） |
| 职责 | 执行`set_all_agent_llm_widgets`处理；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 2；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-67955d3f49"></a>

#### FUN-67955D3F49

| 设计项 | 说明 |
|---|---|
| 函数 | `_analyst_checkbox_state` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L94` |
| 签名 | `_analyst_checkbox_state()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[str, int]` 类型结果 |
| 职责 | 构建`analyst_checkbox_state`；可能影响共享状态；返回 `tuple[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, int]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、len |
| 复杂度 / 风险 | 分支 2；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ac911b85c4"></a>

#### FUN-AC911B85C4

| 设计项 | 说明 |
|---|---|
| 函数 | `_sync_stage_widgets_from_mode_preset` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L114` |
| 签名 | `_sync_stage_widgets_from_mode_preset()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 根据`mode_preset`构建`sync_stage_widgets`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `_MODE_LABEL_TO_VALUE.get` → `run_config_for_mode` → `items` → `run_config_widget_state` → `key.startswith`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、_MODE_LABEL_TO_VALUE.get、bool、run_config_for_mode、items、run_config_widget_state、key.startswith |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fc0e4c8d13"></a>

#### FUN-FC0E4C8D13

| 设计项 | 说明 |
|---|---|
| 函数 | `_on_advanced_toggle` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L127` |
| 签名 | `_on_advanced_toggle()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`on_advanced_toggle`处理；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `_sync_stage_widgets_from_mode_preset`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、_sync_stage_widgets_from_mode_preset |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4562c0a4e8"></a>

#### FUN-4562C0A4E8

| 设计项 | 说明 |
|---|---|
| 函数 | `_apply_mode_preset_to_widgets` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L132` |
| 签名 | `_apply_mode_preset_to_widgets(mode: str)` |
| 参数 | `mode`（str）：运行或分析模式 |
| 返回 | 无返回值（None） |
| 职责 | 应用`mode_preset_widgets`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `run_config_for_mode` → `items` → `run_config_widget_state`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、st.session_state.get、run_config_for_mode、items、run_config_widget_state |
| 复杂度 / 风险 | 分支 3；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b8de98a787"></a>

#### FUN-B8DE98A787

| 设计项 | 说明 |
|---|---|
| 函数 | `_advanced_core_stages_all_off` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L146` |
| 签名 | `_advanced_core_stages_all_off()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`advanced_core_stages_all_off`条件是否成立；可能影响共享状态；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `any` → `st.session_state.get`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | any、st.session_state.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4712d21b11"></a>

#### FUN-4712D21B11

| 设计项 | 说明 |
|---|---|
| 函数 | `selected_run_config` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L150` |
| 签名 | `selected_run_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `RunConfig` 类型结果 |
| 职责 | 执行`selected_config`；可能影响共享状态；返回 `RunConfig` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `st.session_state.get` → `normalized` → `RunConfig` → `_MODE_LABEL_TO_VALUE.get` → `run_config_for_mode` → `_advanced_core_stages_all_off` → `_analyst_checkbox_state` → `strip`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `RunConfig` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.session_state.get、normalized、RunConfig、str、_MODE_LABEL_TO_VALUE.get、run_config_for_mode、bool、_advanced_core_stages_all_off、_analyst_checkbox_state、strip |
| 复杂度 / 风险 | 分支 7；跨度 60 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config_panel.py](../../../tests/unit/test_run_config_panel.py) · 直接动态测试 |

<a id="fun-a56ca0818f"></a>

#### FUN-A56CA0818F

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_run_mode_guide` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L212` |
| 签名 | `_render_run_mode_guide()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`run_mode_guide`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.markdown`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.markdown |
| 复杂度 / 风险 | 分支 0；跨度 20 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d6653fc459"></a>

#### FUN-D6653FC459

| 设计项 | 说明 |
|---|---|
| 函数 | `_on_open_replay_config` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L234` |
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
| 复杂度 / 风险 | 分支 0；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8d7f136545"></a>

#### FUN-8D7F136545

| 设计项 | 说明 |
|---|---|
| 函数 | `render_sidebar_replay` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L244` |
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
| 复杂度 / 风险 | 分支 1；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fea885853a"></a>

#### FUN-FEA885853A

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_replay_controls` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L265` |
| 签名 | `_render_replay_controls()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`replay_controls`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `list_archives` → `st.markdown` → `st.info` → `st.session_state.get` → `_ensure_default_replay_run_id` → `st.checkbox` → `archive_label` → `options.keys`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list_archives、st.markdown、st.info、st.session_state.get、_ensure_default_replay_run_id、st.checkbox、archive_label、list、options.keys、st.selectbox、options.get、str、next、row.get、selected.get、st.warning、st.caption、len、_render_archive_transfer_controls、_render_archive_import_only |
| 复杂度 / 风险 | 分支 5；跨度 50 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-302db0d19b"></a>

#### FUN-302DB0D19B

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_archive_import_only` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L317` |
| 签名 | `_render_archive_import_only()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`archive_import_only`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.file_uploader` → `st.button` → `import_archive_zip` → `uploaded.getvalue` → `st.success` → `st.rerun` → `st.error`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.file_uploader、st.button、import_archive_zip、uploaded.getvalue、st.success、st.rerun、st.error、str |
| 复杂度 / 风险 | 分支 2；跨度 16 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c8de0e7538"></a>

#### FUN-C8DE0E7538

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_archive_transfer_controls` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L335` |
| 签名 | `_render_archive_transfer_controls(selected_id: str)` |
| 参数 | `selected_id`（str）：对象标识 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`archive_transfer_controls`；可能影响外部接口；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.columns` → `export_archive_zip` → `st.download_button` → `st.caption` → `st.file_uploader` → `st.button` → `import_archive_zip` → `uploaded.getvalue`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 无返回值（None）；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.columns、export_archive_zip、st.download_button、st.caption、st.file_uploader、st.button、import_archive_zip、uploaded.getvalue、st.success、st.rerun、st.error、str |
| 复杂度 / 风险 | 分支 4；跨度 34 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5b83f91b90"></a>

#### FUN-5B83F91B90

| 设计项 | 说明 |
|---|---|
| 函数 | `_render_run_config_advanced_controls` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L371` |
| 签名 | `_render_run_config_advanced_controls()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`run_config_advanced_controls`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `st.columns` → `st.button` → `st.markdown` → `st.checkbox` → `enumerate` → `_analyst_checkbox_state` → `st.warning`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.columns、st.button、st.markdown、st.checkbox、enumerate、_analyst_checkbox_state、st.warning |
| 复杂度 / 风险 | 分支 5；跨度 38 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-de6787dacc"></a>

#### FUN-DE6787DACC

| 设计项 | 说明 |
|---|---|
| 函数 | `render_run_config_panel` |
| 源码位置 | [src/viz/run_config_panel.py](../../../src/viz/run_config_panel.py) · `L411` |
| 签名 | `render_run_config_panel()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 渲染`run_config_panel`；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `default_panel_run_config` → `st.session_state.pop` → `_seed_run_config_widgets_if_needed` → `render_page_hero` → `_render_replay_controls` → `st.markdown` → `_render_run_mode_guide` → `st.session_state.get`；包含 14 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | default_panel_run_config、bool、st.session_state.pop、_seed_run_config_widgets_if_needed、render_page_hero、_render_replay_controls、st.markdown、_render_run_mode_guide、st.session_state.get、st.radio、list、_MODE_LABEL_TO_VALUE.get、_apply_mode_preset_to_widgets、llm_configured、st.info、st.warning、st.checkbox、st.expander、_render_run_config_advanced_controls、selected_run_config |
| 复杂度 / 风险 | 分支 14；跨度 104 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-6fa4e87f8a"></a>

### UNIT-6FA4E87F8A

**模块**：`src/viz/session_keys.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6FA4E87F8A |
| 源码 | [src/viz/session_keys.py](../../../src/viz/session_keys.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/session_keys.py` 的职责，通过 `session_id`、`generation_id`、`job_key`、`rotate_generation_id`、`invalidate_report_cache` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
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

<a id="unit-f568ea7ece"></a>

### UNIT-F568EA7ECE

**模块**：`src/viz/source_labels.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F568EA7ECE |
| 源码 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/source_labels.py` 的职责，通过 `is_llm_source`、`llm_was_invoked`、`stage_meta_label`、`source_label`、`stage_source`、`render_source_badge`、`render_stage_meta_badge`、`render_agent_source_banner` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 8 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_source_labels.py](../../../tests/unit/test_source_labels.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[is_llm_source](#fun-6c5c91dc85) · [llm_was_invoked](#fun-198b94558c) · [stage_meta_label](#fun-e190f43fff) · [source_label](#fun-7203478796) · [stage_source](#fun-154472495a) · [render_source_badge](#fun-757465430c) · [render_stage_meta_badge](#fun-405b8cf26d) · [render_agent_source_banner](#fun-0149440496)

<a id="fun-6c5c91dc85"></a>

#### FUN-6C5C91DC85

| 设计项 | 说明 |
|---|---|
| 函数 | `is_llm_source` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L35` |
| 签名 | `is_llm_source(source: str \| None)` |
| 参数 | `source`（str \| None）：数据或证据来源 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_source`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-198b94558c"></a>

#### FUN-198B94558C

| 设计项 | 说明 |
|---|---|
| 函数 | `llm_was_invoked` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L39` |
| 签名 | `llm_was_invoked(meta: dict)` |
| 参数 | `meta`（dict）：审计或处理元数据 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_was_invoked`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `llm.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | meta.get、bool、llm.get |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_source_labels.py](../../../tests/unit/test_source_labels.py) · 直接动态测试 |

<a id="fun-e190f43fff"></a>

#### FUN-E190F43FFF

| 设计项 | 说明 |
|---|---|
| 函数 | `stage_meta_label` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L48` |
| 签名 | `stage_meta_label(meta: dict)` |
| 参数 | `meta`（dict）：审计或处理元数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stage_meta_label`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `meta.get` → `strip` → `llm_was_invoked` → `llm.get`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | meta.get、strip、llm_was_invoked、llm.get |
| 复杂度 / 风险 | 分支 5；跨度 13 行；中 |
| 测试 / 验证 | [tests/unit/test_source_labels.py](../../../tests/unit/test_source_labels.py) · 直接动态测试 |

<a id="fun-7203478796"></a>

#### FUN-7203478796

| 设计项 | 说明 |
|---|---|
| 函数 | `source_label` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L63` |
| 签名 | `source_label(source: str \| None)` |
| 参数 | `source`（str \| None）：数据或证据来源 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成数据来源标签文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `SOURCE_LABELS.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | SOURCE_LABELS.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) · 直接动态测试 |

<a id="fun-154472495a"></a>

#### FUN-154472495A

| 设计项 | 说明 |
|---|---|
| 函数 | `stage_source` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L67` |
| 签名 | `stage_source(report: dict, stage: str)` |
| 参数 | `report`（dict）：分析报告<br>`stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stage_source`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `report.get` → `meta.get` → `entry.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、report.get、meta.get、entry.get |
| 复杂度 / 风险 | 分支 0；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-757465430c"></a>

#### FUN-757465430C

| 设计项 | 说明 |
|---|---|
| 函数 | `render_source_badge` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L73` |
| 签名 | `render_source_badge(source: str \| None, *, small: bool=False)` |
| 参数 | `source`（str \| None）：数据或证据来源<br>`small`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`source_badge`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `source_label` → `is_llm_source`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | source_label、is_llm_source |
| 复杂度 / 风险 | 分支 2；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-405b8cf26d"></a>

#### FUN-405B8CF26D

| 设计项 | 说明 |
|---|---|
| 函数 | `render_stage_meta_badge` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L81` |
| 签名 | `render_stage_meta_badge(meta: dict, *, small: bool=False)` |
| 参数 | `meta`（dict）：审计或处理元数据<br>`small`（bool）：控制对应行为是否启用的布尔值；默认值 `False` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`stage_meta_badge`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `stage_meta_label` → `llm_was_invoked`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | stage_meta_label、llm_was_invoked |
| 复杂度 / 风险 | 分支 2；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0149440496"></a>

#### FUN-0149440496

| 设计项 | 说明 |
|---|---|
| 函数 | `render_agent_source_banner` |
| 源码位置 | [src/viz/source_labels.py](../../../src/viz/source_labels.py) · `L89` |
| 签名 | `render_agent_source_banner(report: dict)` |
| 参数 | `report`（dict）：分析报告 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 渲染`agent_source_banner`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `report.get` → `meta.get` → `MODE_LABELS.get` → `STAGE_LABELS.get` → `entry.get` → `llm.get` → `llm_was_invoked` → `short_model_name`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | report.get、meta.get、MODE_LABELS.get、STAGE_LABELS.get、entry.get、llm.get、llm_was_invoked、short_model_name、chips.append、render_stage_meta_badge、render_source_badge、join |
| 复杂度 / 风险 | 分支 5；跨度 49 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-202db41fe0"></a>

### UNIT-202DB41FE0

**模块**：`src/viz/streamlit_common.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-202DB41FE0 |
| 源码 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 实现“Streamlit 展示”组件中 `src/viz/streamlit_common.py` 的职责，通过 `bootstrap_env`、`missing_runtime_dependencies`、`render_runtime_dependency_banner`、`page_setup`、`init_page`、`render_sidebar_refresh_button`、`render_sidebar_header`、`render_sidebar_footer` 提供该模块的公开能力。 |
| 关联需求 | [SWR-REP-004](../SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](../SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](../SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](../SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 20 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) |
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
| 处理逻辑 | 按源码执行顺序经过 `st.sidebar.markdown` → `st.sidebar.caption` → `short_model_name` → `render_sidebar_replay` → `render_sidebar_refresh_button`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | st.sidebar.markdown、st.sidebar.caption、short_model_name、render_sidebar_replay、render_sidebar_refresh_button |
| 复杂度 / 风险 | 分支 2；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-943d58e197"></a>

#### FUN-943D58E197

| 设计项 | 说明 |
|---|---|
| 函数 | `render_sidebar_footer` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L187` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L200` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L204` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L220` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L243` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L258` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L282` |
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
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L340` |
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
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |

<a id="fun-2268bf01ca"></a>

#### FUN-2268BF01CA

| 设计项 | 说明 |
|---|---|
| 函数 | `_store_report_bundle` |
| 源码位置 | [src/viz/streamlit_common.py](../../../src/viz/streamlit_common.py) · `L391` |
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
| 测试 / 验证 | [tests/regression/test_fixes.py](../../../tests/regression/test_fixes.py)、[tests/unit/test_streamlit_ensure_report.py](../../../tests/unit/test_streamlit_ensure_report.py) · 直接动态测试 |
