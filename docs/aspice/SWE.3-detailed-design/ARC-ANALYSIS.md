# ARC-ANALYSIS — Point-in-time market structure

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
| [src/analysis/chart_sr_filters.py](#unit-271badecbe) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/chart_zone_filters.py](#unit-070aa8511c) | 8 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/data_freshness.py](#unit-3549e9d9b7) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/dgt_price_action.py](#unit-7dfc57faf9) | 10 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/display_labels.py](#unit-3b1598dc1b) | 2 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/ict_pa.py](#unit-3962aaac44) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/luxalgo_smc.py](#unit-2f7fedba6f) | 15 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/price_action_facts.py](#unit-daf97d09e5) | 7 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/proximity.py](#unit-ce01c0290c) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/technical_context.py](#unit-7faaa8edca) | 17 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/tf_snapshot.py](#unit-ebf42549f9) | 4 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-cf43fe46e5"></a>

### UNIT-CF43FE46E5

**模块**：`src/analysis/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CF43FE46E5 |
| 源码 | [src/analysis/__init__.py](../../../src/analysis/__init__.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-271badecbe"></a>

### UNIT-271BADECBE

**模块**：`src/analysis/chart_sr_filters.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-271BADECBE |
| 源码 | [src/analysis/chart_sr_filters.py](../../../src/analysis/chart_sr_filters.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/chart_sr_filters.py` 的职责，通过 `visible_sr_price_lines` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/chart_zone_filters.py` 的职责，通过 `chart_plot_df`、`chart_price_bounds`、`zone_overlaps_chart_range`、`visible_order_blocks`、`visible_active_fvgs`、`visible_zone_snapshots`、`visible_zones_for_chart` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [visible_order_blocks](#fun-f8e5f51975) | 构建`visible_order_blocks`；返回 `list[OrderBlock]` 类型结果。 | 未检测到直接副作用 | — |

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
| 测试 / 验证 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) · 直接动态测试 |

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
| 测试 / 验证 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) · 直接动态测试 |

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
| 测试 / 验证 | — · 静态分析与组件级验证 |

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
| 测试 / 验证 | — · 静态分析与组件级验证 |

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
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-3549e9d9b7"></a>

### UNIT-3549E9D9B7

**模块**：`src/analysis/data_freshness.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3549E9D9B7 |
| 源码 | [src/analysis/data_freshness.py](../../../src/analysis/data_freshness.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/data_freshness.py` 的职责，通过 `build_data_as_of` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/dgt_price_action.py` 的职责，通过 `SrLevel`、`VolumeProfileResult`、`DgtPriceActionResult`、`build_volume_profile`、`analyze_dgt_price_action`、`dgt_result_to_dict` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/display_labels.py` 的职责，通过 `infer_trade_theme`、`liquidity_label` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [infer_trade_theme](#fun-f014f8a0dd) | 生成`infer_trade_theme`文本；返回 `str` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) |

#### 函数导航

[infer_trade_theme](#fun-f014f8a0dd) · [liquidity_label](#fun-f519f9a949)

<a id="fun-f014f8a0dd"></a>

#### FUN-F014F8A0DD

| 设计项 | 说明 |
|---|---|
| 函数 | `infer_trade_theme` |
| 源码位置 | [src/analysis/display_labels.py](../../../src/analysis/display_labels.py) · `L11` |
| 签名 | `infer_trade_theme(*, theme: str='', direction: str='', direction_cn: str='')` |
| 参数 | `theme`（str）：由 `theme` 表示的文本或标识；默认值 `''`<br>`direction`（str）：交易方向；默认值 `''`<br>`direction_cn`（str）：由 `direction_cn` 表示的文本或标识；默认值 `''` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`infer_trade_theme`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `any`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、any |
| 复杂度 / 风险 | 分支 1；跨度 3 行；高 |
| 测试 / 验证 | [tests/unit/test_advice_architecture_smoke.py](../../../tests/unit/test_advice_architecture_smoke.py) · 直接动态测试 |

<a id="fun-f519f9a949"></a>

#### FUN-F519F9A949

| 设计项 | 说明 |
|---|---|
| 函数 | `liquidity_label` |
| 源码位置 | [src/analysis/display_labels.py](../../../src/analysis/display_labels.py) · `L24` |
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

<a id="unit-3962aaac44"></a>

### UNIT-3962AAAC44

**模块**：`src/analysis/ict_pa.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3962AAAC44 |
| 源码 | [src/analysis/ict_pa.py](../../../src/analysis/ict_pa.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/ict_pa.py` 的职责，通过 `SwingPoint`、`OrderBlock`、`FairValueGap`、`LiquidityZone`、`StructureEvent`、`TimeframeAnalysis`、`analyze_timeframe`、`sentiment_score` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_advice_v2.py](../../../tests/unit/test_advice_v2.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_tf_snapshot.py](../../../tests/unit/test_tf_snapshot.py) |
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
| 测试 / 验证 | — · 静态分析与组件级验证 |

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
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_luxalgo_smc.py](../../../tests/unit/test_luxalgo_smc.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

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

<a id="unit-2f7fedba6f"></a>

### UNIT-2F7FEDBA6F

**模块**：`src/analysis/luxalgo_smc.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F7FEDBA6F |
| 源码 | [src/analysis/luxalgo_smc.py](../../../src/analysis/luxalgo_smc.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/luxalgo_smc.py` 的职责，通过 `LuxAlgoResult`、`analyze_luxalgo` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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

<a id="unit-daf97d09e5"></a>

### UNIT-DAF97D09E5

**模块**：`src/analysis/price_action_facts.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAF97D09E5 |
| 源码 | [src/analysis/price_action_facts.py](../../../src/analysis/price_action_facts.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/price_action_facts.py` 的职责，通过 `build_session_price_action_block`、`build_price_action_summaries`、`chart_sr_levels` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/proximity.py` 的职责，通过 `proximity_threshold`、`zone_near_price`、`level_near_price` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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

<a id="unit-7faaa8edca"></a>

### UNIT-7FAAA8EDCA

**模块**：`src/analysis/technical_context.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7FAAA8EDCA |
| 源码 | [src/analysis/technical_context.py](../../../src/analysis/technical_context.py) |
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/technical_context.py` 的职责，通过 `distance_pct`、`primary_analysis`、`fibonacci_context`、`support_resistance_context`、`indicator_snapshot`、`structure_narrative`、`timeframe_context`、`technical_quality` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 17 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py) |
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
| 测试 / 验证 | [tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py) · 直接动态测试 |

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
| 测试 / 验证 | — · 静态分析与组件级验证 |

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
| 测试 / 验证 | [tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py) · 直接动态测试 |

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
| 架构组件 | ARC-ANALYSIS — Point-in-time market structure |
| 职责 | 实现“Point-in-time market structure”组件中 `src/analysis/tf_snapshot.py` 的职责，通过 `build_tf_snapshot` 提供该模块的公开能力。 |
| 关联需求 | [SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
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
