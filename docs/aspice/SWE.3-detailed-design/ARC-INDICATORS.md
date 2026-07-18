# ARC-INDICATORS — 指标计算

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./README.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/README.md#arc-indicators)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/indicators/__init__.py](#unit-7d2cf26834) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) | selected |
| [src/indicators/technical.py](#unit-2f8c299c5b) | 10 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |
| [src/indicators/verify.py](#unit-d35a8017fe) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) | selected |

<a id="unit-7d2cf26834"></a>

### UNIT-7D2CF26834

**模块**：`src/indicators/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7D2CF26834 |
| 源码 | [src/indicators/__init__.py](../../../src/indicators/__init__.py) |
| 架构组件 | ARC-INDICATORS — 指标计算 |
| 职责 | 实现“指标计算”组件中 `src/indicators/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-2f8c299c5b"></a>

### UNIT-2F8C299C5B

**模块**：`src/indicators/technical.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F8C299C5B |
| 源码 | [src/indicators/technical.py](../../../src/indicators/technical.py) |
| 架构组件 | ARC-INDICATORS — 指标计算 |
| 职责 | 实现“指标计算”组件中 `src/indicators/technical.py` 的职责，通过 `add_emas`、`add_vwap`、`add_atr`、`add_rsi`、`add_macd`、`add_adx`、`enrich`、`indicator_values` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 10 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) |
| 验证状态 | selected |

#### 函数导航

[add_emas](#fun-8f7e8730d6) · [add_vwap](#fun-c3db0f8450) · [add_atr](#fun-4d1a54987d) · [add_rsi](#fun-3901170d43) · [add_macd](#fun-5299aa4622) · [add_adx](#fun-a8f0fc0306) · [enrich](#fun-3f2d66c862) · [indicator_values](#fun-d44171a8a2) · [ema_relation](#fun-1fcd39f6e9) · [fibonacci_levels](#fun-6537a68fb4)

<a id="fun-8f7e8730d6"></a>

#### FUN-8F7E8730D6

| 设计项 | 说明 |
|---|---|
| 函数 | `add_emas` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L10` |
| 签名 | `add_emas(df: pd.DataFrame, periods: tuple[int, ...]=(20, 50, 610))` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`periods`（tuple[int, ...]）：由调用方提供的 `periods` 输入对象；默认值 `(20, 50, 610)` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 添加`emas`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `mean` → `ewm`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、mean、ewm |
| 复杂度 / 风险 | 分支 1；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c3db0f8450"></a>

#### FUN-C3DB0F8450

| 设计项 | 说明 |
|---|---|
| 函数 | `add_vwap` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L17` |
| 签名 | `add_vwap(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 添加`vwap`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `fillna` → `replace` → `cumsum` → `tp_vol.groupby` → `vol.groupby`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、fillna、replace、cumsum、tp_vol.groupby、vol.groupby |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4d1a54987d"></a>

#### FUN-4D1A54987D

| 设计项 | 说明 |
|---|---|
| 函数 | `add_atr` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L27` |
| 签名 | `add_atr(df: pd.DataFrame, period: int=14)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`period`（int）：计算周期长度；默认值 `14` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 添加`atr`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `shift` → `max` → `pd.concat` → `abs` → `mean` → `tr.rolling`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、shift、max、pd.concat、abs、mean、tr.rolling |
| 复杂度 / 风险 | 分支 0；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3901170d43"></a>

#### FUN-3901170D43

| 设计项 | 说明 |
|---|---|
| 函数 | `add_rsi` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L42` |
| 签名 | `add_rsi(df: pd.DataFrame, period: int=14)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`period`（int）：计算周期长度；默认值 `14` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 添加`rsi`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `diff` → `mean` → `rolling` → `delta.clip` → `loss.replace` → `rsi.mask`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、diff、mean、rolling、delta.clip、loss.replace、rsi.mask |
| 复杂度 / 风险 | 分支 0；跨度 11 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5299aa4622"></a>

#### FUN-5299AA4622

| 设计项 | 说明 |
|---|---|
| 函数 | `add_macd` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L55` |
| 签名 | `add_macd(df: pd.DataFrame, *, fast: int=12, slow: int=26, signal: int=9)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`fast`（int）：由 `fast` 表示的数值参数；默认值 `12`<br>`slow`（int）：由 `slow` 表示的数值参数；默认值 `26`<br>`signal`（int）：当前交易信号；默认值 `9` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 添加`macd`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `mean` → `ewm`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、mean、ewm |
| 复杂度 / 风险 | 分支 0；跨度 14 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a8f0fc0306"></a>

#### FUN-A8F0FC0306

| 设计项 | 说明 |
|---|---|
| 函数 | `add_adx` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L71` |
| 签名 | `add_adx(df: pd.DataFrame, period: int=14)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`period`（int）：计算周期长度；默认值 `14` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 添加`adx`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `diff` → `up_move.where` → `down_move.where` → `shift` → `max` → `pd.concat` → `abs`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、diff、up_move.where、down_move.where、shift、max、pd.concat、abs、sum、tr.rolling、plus_dm.rolling、tr_sum.replace、minus_dm.rolling、replace、mean、dx.rolling |
| 复杂度 / 风险 | 分支 0；跨度 22 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3f2d66c862"></a>

#### FUN-3F2D66C862

| 设计项 | 说明 |
|---|---|
| 函数 | `enrich` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L95` |
| 签名 | `enrich(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 构建`enrich`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `add_adx` → `add_macd` → `add_rsi` → `add_atr` → `add_vwap` → `add_emas`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | add_adx、add_macd、add_rsi、add_atr、add_vwap、add_emas |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py) · 直接动态测试 |

<a id="fun-d44171a8a2"></a>

#### FUN-D44171A8A2

| 设计项 | 说明 |
|---|---|
| 函数 | `indicator_values` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L99` |
| 签名 | `indicator_values(row: pd.Series)` |
| 参数 | `row`（pd.Series）：当前记录行 |
| 返回 | 返回 `dict[str, float \| None]` 类型结果 |
| 职责 | 构建`indicator_values`；返回 `dict[str, float \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.isna` → `round`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, float \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.isna、round、float |
| 复杂度 / 风险 | 分支 2；跨度 8 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1fcd39f6e9"></a>

#### FUN-1FCD39F6E9

| 设计项 | 说明 |
|---|---|
| 函数 | `ema_relation` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L109` |
| 签名 | `ema_relation(price: float, row: pd.Series)` |
| 参数 | `price`（float）：当前或待评估价格<br>`row`（pd.Series）：当前记录行 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`ema_relation`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.isna`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.isna、float |
| 复杂度 / 风险 | 分支 4；跨度 14 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_report_facts.py](../../../tests/unit/test_report_facts.py) · 直接动态测试 |

<a id="fun-6537a68fb4"></a>

#### FUN-6537A68FB4

| 设计项 | 说明 |
|---|---|
| 函数 | `fibonacci_levels` |
| 源码位置 | [src/indicators/technical.py](../../../src/indicators/technical.py) · `L125` |
| 签名 | `fibonacci_levels(swing_high: float, swing_low: float)` |
| 参数 | `swing_high`（float）：摆动高点价格<br>`swing_low`（float）：摆动低点价格 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 构建`fibonacci_levels`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `levels.append` → `round`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | levels.append、round |
| 复杂度 / 风险 | 分支 1；跨度 21 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py) · 直接动态测试 |

<a id="unit-d35a8017fe"></a>

### UNIT-D35A8017FE

**模块**：`src/indicators/verify.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D35A8017FE |
| 源码 | [src/indicators/verify.py](../../../src/indicators/verify.py) |
| 架构组件 | ARC-INDICATORS — 指标计算 |
| 职责 | 实现“指标计算”组件中 `src/indicators/verify.py` 的职责，通过 `indicator_snapshot`、`indicator_table_rows` 提供该模块的公开能力。 |
| 关联需求 | [SWR-ANA-001](../SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py) |
| 验证状态 | selected |

#### 函数导航

[indicator_snapshot](#fun-c3ec67606c) · [indicator_table_rows](#fun-44ba63c6e8)

<a id="fun-c3ec67606c"></a>

#### FUN-C3EC67606C

| 设计项 | 说明 |
|---|---|
| 函数 | `indicator_snapshot` |
| 源码位置 | [src/indicators/verify.py](../../../src/indicators/verify.py) · `L10` |
| 签名 | `indicator_snapshot(df: pd.DataFrame, timeframe: str)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`timeframe`（str）：行情时间框架 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 构建指标快照；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round` → `pd.notna` → `ema_relation` → `row.update` → `indicator_values` → `sum` → `fillna` → `notes.append`；包含 13 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、len、str、round、pd.notna、ema_relation、row.update、indicator_values、int、sum、fillna、notes.append、abs、row.get |
| 复杂度 / 风险 | 分支 13；跨度 58 行；中 |
| 测试 / 验证 | [tests/unit/test_financial_review.py](../../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py) · 直接动态测试 |

<a id="fun-44ba63c6e8"></a>

#### FUN-44BA63C6E8

| 设计项 | 说明 |
|---|---|
| 函数 | `indicator_table_rows` |
| 源码位置 | [src/indicators/verify.py](../../../src/indicators/verify.py) · `L70` |
| 签名 | `indicator_table_rows(snapshots: list[dict])` |
| 参数 | `snapshots`（list[dict]）：由 `snapshots` 表示的输入集合 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 构建`indicator_table_rows`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `rows.append` → `s.get`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | rows.append、s.get |
| 复杂度 / 风险 | 分支 2；跨度 26 行；中 |
| 测试 / 验证 | [tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py) · 直接动态测试 |
