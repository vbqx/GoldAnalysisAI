# ARC-BACKTEST — Point-in-time 回测

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-backtest)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/backtest/__init__.py](#unit-d4fb321d1e) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/engine.py](#unit-b336aa1943) | 10 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/macro.py](#unit-d40a0640bf) | 6 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/metrics.py](#unit-a92846cf7a) | 3 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/simulator.py](#unit-d6d81aa6c4) | 10 | 10 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/types.py](#unit-a71e1f8ce9) | 5 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) | selected |

<a id="unit-d4fb321d1e"></a>

### UNIT-D4FB321D1E

**模块**：`src/backtest/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D4FB321D1E |
| 源码 | [src/backtest/__init__.py](../../../src/backtest/__init__.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | 实现“Point-in-time 回测”组件中 `src/backtest/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[__getattr__](#fun-3eb645c6d9)

<a id="fun-3eb645c6d9"></a>

#### FUN-3EB645C6D9

| 设计项 | 说明 |
|---|---|
| 函数 | `__getattr__` |
| 源码位置 | [src/backtest/__init__.py](../../../src/backtest/__init__.py) · `L17` |
| 签名 | `__getattr__(name: str)` |
| 参数 | `name`（str）：对象名称 |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 生成`getattr`结果；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `AttributeError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；静态扫描未发现直接外部副作用 |
| 显式异常 | AttributeError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | AttributeError |
| 复杂度 / 风险 | 分支 1；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-b336aa1943"></a>

### UNIT-B336AA1943

**模块**：`src/backtest/engine.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B336AA1943 |
| 源码 | [src/backtest/engine.py](../../../src/backtest/engine.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | 实现“Point-in-time 回测”组件中 `src/backtest/engine.py` 的职责，通过 `normalize_ohlcv`、`resample_ohlcv`、`make_multitimeframe`、`run_backtest`、`run_random_window_backtest`、`run_backtest_from_archive` 提供该模块的公开能力。 |
| 关联需求 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 10 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_backtest_engine.py](../../../tests/unit/test_backtest_engine.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_macro_data_for_run](#fun-f28876ab16) | 执行`macro_data`；可能影响外部接口；返回 `tuple[pd.DataFrame \| None, str \| None]` 类型结果。 | 外部接口 I/O | — |
| [run_backtest_from_archive](#fun-ee64e9ff2e) | 根据`archive`构建`run_backtest`；返回 `BacktestResult` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) |

#### 函数导航

[normalize_ohlcv](#fun-9b29434b63) · [resample_ohlcv](#fun-7de676802f) · [make_multitimeframe](#fun-a04b254b5f) · [_enough_data](#fun-18097428b1) · [_selected_signals](#fun-e547fb0bfe) · [_iter_signal_points](#fun-0ed117c7ab) · [_macro_data_for_run](#fun-f28876ab16) · [run_backtest](#fun-96250d4b68) · [run_random_window_backtest](#fun-2ce7bcc851) · [run_backtest_from_archive](#fun-ee64e9ff2e)

<a id="fun-9b29434b63"></a>

#### FUN-9B29434B63

| 设计项 | 说明 |
|---|---|
| 函数 | `normalize_ohlcv` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L17` |
| 签名 | `normalize_ohlcv(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 标准化`ohlcv`；可能影响文件系统；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `out.rename` → `rename.items` → `pd.to_datetime` → `out.pop` → `ValueError` → `astype` → `dropna`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于文件系统 |
| 显式异常 | ValueError |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、out.rename、rename.items、pd.to_datetime、out.pop、ValueError、astype、dropna、out.sort_index |
| 复杂度 / 风险 | 分支 4；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_backtest_engine.py](../../../tests/unit/test_backtest_engine.py) · 直接动态测试 |

<a id="fun-7de676802f"></a>

#### FUN-7DE676802F

| 设计项 | 说明 |
|---|---|
| 函数 | `resample_ohlcv` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L43` |
| 签名 | `resample_ohlcv(df_5m: pd.DataFrame, rule: str)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`rule`（str）：由 `rule` 表示的文本或标识 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 构建`resample_ohlcv`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `agg` → `df_5m.resample` → `out.dropna`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | agg、df_5m.resample、out.dropna |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a04b254b5f"></a>

#### FUN-A04B254B5F

| 设计项 | 说明 |
|---|---|
| 函数 | `make_multitimeframe` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L50` |
| 签名 | `make_multitimeframe(df_5m: pd.DataFrame)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表 |
| 返回 | 返回 `dict[str, pd.DataFrame]` 类型结果 |
| 职责 | 构造`multitimeframe`；返回 `dict[str, pd.DataFrame]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `resample_ohlcv`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, pd.DataFrame]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | resample_ohlcv |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_backtest_engine.py](../../../tests/unit/test_backtest_engine.py) · 直接动态测试 |

<a id="fun-18097428b1"></a>

#### FUN-18097428B1

| 设计项 | 说明 |
|---|---|
| 函数 | `_enough_data` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L60` |
| 签名 | `_enough_data(data: dict[str, pd.DataFrame])` |
| 参数 | `data`（dict[str, pd.DataFrame]）：输入数据 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`enough_data`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `all` → `data.get` → `required.items`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | all、len、data.get、required.items |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e547fb0bfe"></a>

#### FUN-E547FB0BFE

| 设计项 | 说明 |
|---|---|
| 函数 | `_selected_signals` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L65` |
| 签名 | `_selected_signals(data_5m: pd.DataFrame, *, config: BacktestConfig, dxy_daily: pd.DataFrame \| None=None)` |
| 参数 | `data_5m`（pd.DataFrame）：由调用方提供的 `data_5m` 输入对象<br>`config`（BacktestConfig）：运行配置<br>`dxy_daily`（pd.DataFrame \| None）：美元指数日线数据；默认值 `None` |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 生成`selected_signals`结果；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `make_multitimeframe` → `_enough_data` → `enrich` → `data.items` → `analyze_timeframe` → `daily_metrics` → `MarketContext` → `ExternalFactors`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | make_multitimeframe、_enough_data、enrich、data.items、analyze_timeframe、daily_metrics、MarketContext、float、ExternalFactors、compute_trading_signals、sentiment_score、macro_state_at、apply_macro_to_signals、sentiment.get、min、max、macro_notes.append、EvidenceItem、AgentEvidence、ResearchDebate |
| 复杂度 / 风险 | 分支 11；跨度 102 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0ed117c7ab"></a>

#### FUN-0ED117C7AB

| 设计项 | 说明 |
|---|---|
| 函数 | `_iter_signal_points` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L169` |
| 签名 | `_iter_signal_points(df_5m: pd.DataFrame, config: BacktestConfig)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`config`（BacktestConfig）：运行配置 |
| 返回 | 返回 `Iterable[int]` 类型结果 |
| 职责 | 计算`iter_signal_points`；返回 `Iterable[int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `range`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Iterable[int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、max、range |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f28876ab16"></a>

#### FUN-F28876AB16

| 设计项 | 说明 |
|---|---|
| 函数 | `_macro_data_for_run` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L174` |
| 签名 | `_macro_data_for_run(config: BacktestConfig, dxy_daily: pd.DataFrame \| None)` |
| 参数 | `config`（BacktestConfig）：运行配置<br>`dxy_daily`（pd.DataFrame \| None）：美元指数日线数据 |
| 返回 | 返回 `tuple[pd.DataFrame \| None, str \| None]` 类型结果 |
| 职责 | 执行`macro_data`；可能影响外部接口；返回 `tuple[pd.DataFrame \| None, str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `normalize_macro_ohlcv` → `fetch_historical_dxy`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[pd.DataFrame \| None, str \| None]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | normalize_macro_ohlcv、fetch_historical_dxy、str |
| 复杂度 / 风险 | 分支 3；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-96250d4b68"></a>

#### FUN-96250D4B68

| 设计项 | 说明 |
|---|---|
| 函数 | `run_backtest` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L185` |
| 签名 | `run_backtest(df_5m: pd.DataFrame, config: BacktestConfig \| None=None, *, dxy_daily: pd.DataFrame \| None=None)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`config`（BacktestConfig \| None）：运行配置；默认值 `None`<br>`dxy_daily`（pd.DataFrame \| None）：美元指数日线数据；默认值 `None` |
| 返回 | 返回 `BacktestResult` 类型结果 |
| 职责 | 执行`backtest`；返回 `BacktestResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `BacktestConfig` → `normalize_ohlcv` → `_macro_data_for_run` → `_iter_signal_points` → `_selected_signals` → `metadata.get` → `getattr` → `trades.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `BacktestResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | BacktestConfig、normalize_ohlcv、_macro_data_for_run、_iter_signal_points、_selected_signals、metadata.get、float、getattr、trades.append、simulate_signal、summarize_trades、len、str、BacktestResult、group_trades |
| 复杂度 / 风险 | 分支 7；跨度 54 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2ce7bcc851"></a>

#### FUN-2CE7BCC851

| 设计项 | 说明 |
|---|---|
| 函数 | `run_random_window_backtest` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L241` |
| 签名 | `run_random_window_backtest(df_5m: pd.DataFrame, config: BacktestConfig \| None=None, *, dxy_daily: pd.DataFrame \| None=None)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`config`（BacktestConfig \| None）：运行配置；默认值 `None`<br>`dxy_daily`（pd.DataFrame \| None）：美元指数日线数据；默认值 `None` |
| 返回 | 返回 `BacktestResult` 类型结果 |
| 职责 | 执行`random_window_backtest`；返回 `BacktestResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `BacktestConfig` → `replace` → `normalize_ohlcv` → `_macro_data_for_run` → `random.Random` → `max` → `run_backtest` → `range`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `BacktestResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | BacktestConfig、replace、normalize_ohlcv、_macro_data_for_run、random.Random、max、len、run_backtest、set、range、rng.randint、seen.add、all_trades.append、window_stats.append、str、all_trades.sort、summarize_trades、sum、sorted、int |
| 复杂度 / 风险 | 分支 6；跨度 60 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ee64e9ff2e"></a>

#### FUN-EE64E9FF2E

| 设计项 | 说明 |
|---|---|
| 函数 | `run_backtest_from_archive` |
| 源码位置 | [src/backtest/engine.py](../../../src/backtest/engine.py) · `L303` |
| 签名 | `run_backtest_from_archive(run_id: str, config: BacktestConfig \| None=None, *, dxy_daily: pd.DataFrame \| None=None)` |
| 参数 | `run_id`（str）：对象标识<br>`config`（BacktestConfig \| None）：运行配置；默认值 `None`<br>`dxy_daily`（pd.DataFrame \| None）：美元指数日线数据；默认值 `None` |
| 返回 | 返回 `BacktestResult` 类型结果 |
| 职责 | 根据`archive`构建`run_backtest`；返回 `BacktestResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `load_archive_5m_bars` → `BacktestConfig` → `run_backtest` → `replace`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `BacktestResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | load_archive_5m_bars、BacktestConfig、run_backtest、dict、replace |
| 复杂度 / 风险 | 分支 0；跨度 16 行；高 |
| 测试 / 验证 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) · 直接动态测试 |

<a id="unit-d40a0640bf"></a>

### UNIT-D40A0640BF

**模块**：`src/backtest/macro.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D40A0640BF |
| 源码 | [src/backtest/macro.py](../../../src/backtest/macro.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | 实现“Point-in-time 回测”组件中 `src/backtest/macro.py` 的职责，通过 `fetch_historical_dxy`、`normalize_macro_ohlcv`、`macro_state_at`、`apply_macro_to_signals` 提供该模块的公开能力。 |
| 关联需求 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 6 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_macro.py](../../../tests/unit/test_backtest_macro.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [fetch_historical_dxy](#fun-ba325106f2) | 获取`historical_dxy`；可能影响外部接口；返回 `pd.DataFrame` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[fetch_historical_dxy](#fun-ba325106f2) · [normalize_macro_ohlcv](#fun-0012d514e3) · [macro_state_at](#fun-3652f686d6) · [macro_state_at.pct_change](#fun-9797b95972) · [apply_macro_to_signals](#fun-d64ad4df14) · [_grade](#fun-81f066d179)

<a id="fun-ba325106f2"></a>

#### FUN-BA325106F2

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_historical_dxy` |
| 源码位置 | [src/backtest/macro.py](../../../src/backtest/macro.py) · `L10` |
| 签名 | `fetch_historical_dxy(n_bars: int=1500)` |
| 参数 | `n_bars`（int）：K 线记录集合；默认值 `1500` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 获取`historical_dxy`；可能影响外部接口；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_fetch_bars`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _fetch_bars |
| 复杂度 / 风险 | 分支 0；跨度 15 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0012d514e3"></a>

#### FUN-0012D514E3

| 设计项 | 说明 |
|---|---|
| 函数 | `normalize_macro_ohlcv` |
| 源码位置 | [src/backtest/macro.py](../../../src/backtest/macro.py) · `L27` |
| 签名 | `normalize_macro_ohlcv(df: pd.DataFrame)` |
| 参数 | `df`（pd.DataFrame）：输入数据表 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 标准化`macro_ohlcv`；可能影响文件系统；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `df.copy` → `out.rename` → `rename.items` → `pd.to_datetime` → `out.pop` → `ValueError` → `out.sort_index`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于文件系统 |
| 显式异常 | ValueError |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | df.copy、out.rename、rename.items、pd.to_datetime、out.pop、ValueError、out.sort_index |
| 复杂度 / 风险 | 分支 2；跨度 20 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3652f686d6"></a>

#### FUN-3652F686D6

| 设计项 | 说明 |
|---|---|
| 函数 | `macro_state_at` |
| 源码位置 | [src/backtest/macro.py](../../../src/backtest/macro.py) · `L49` |
| 签名 | `macro_state_at(dxy_daily: pd.DataFrame \| None, timestamp: pd.Timestamp)` |
| 参数 | `dxy_daily`（pd.DataFrame \| None）：美元指数日线数据<br>`timestamp`（pd.Timestamp）：时间戳 |
| 返回 | 返回 `MacroReplayState` 类型结果 |
| 职责 | 生成`macro_state_at`结果；返回 `MacroReplayState` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `pd.Timestamp` → `ts.tz_localize` → `ts.tz_convert` → `MacroReplayState` → `normalize_macro_ohlcv` → `ts.floor` → `pct_change` → `round`；包含 22 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `MacroReplayState` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | pd.Timestamp、ts.tz_localize、ts.tz_convert、MacroReplayState、normalize_macro_ohlcv、ts.floor、len、float、pct_change、round、min、abs |
| 复杂度 / 风险 | 分支 22；跨度 84 行；中 |
| 测试 / 验证 | [tests/unit/test_backtest_macro.py](../../../tests/unit/test_backtest_macro.py) · 直接动态测试 |

<a id="fun-9797b95972"></a>

#### FUN-9797B95972

| 设计项 | 说明 |
|---|---|
| 函数 | `macro_state_at.pct_change` |
| 源码位置 | [src/backtest/macro.py](../../../src/backtest/macro.py) · `L90` |
| 签名 | `macro_state_at.pct_change(periods: int)` |
| 参数 | `periods`（int）：由 `periods` 表示的数值参数 |
| 返回 | 返回 `float \| None` 类型结果 |
| 职责 | 计算`pct_change`；返回 `float \| None` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、float |
| 复杂度 / 风险 | 分支 2；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d64ad4df14"></a>

#### FUN-D64AD4DF14

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_macro_to_signals` |
| 源码位置 | [src/backtest/macro.py](../../../src/backtest/macro.py) · `L135` |
| 签名 | `apply_macro_to_signals(signals: list, state: MacroReplayState, weight: float)` |
| 参数 | `signals`（list）：交易信号集合<br>`state`（MacroReplayState）：状态对象<br>`weight`（float）：由 `weight` 表示的数值参数 |
| 返回 | 返回 `list` 类型结果 |
| 职责 | 应用`macro_signals`；返回 `list` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `getattr` → `round` → `max` → `min` → `_grade` → `signal.score_reasons.append` → `setattr` → `sorted`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | getattr、float、round、max、min、_grade、signal.score_reasons.append、setattr、str、sorted |
| 复杂度 / 风险 | 分支 5；跨度 22 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-81f066d179"></a>

#### FUN-81F066D179

| 设计项 | 说明 |
|---|---|
| 函数 | `_grade` |
| 源码位置 | [src/backtest/macro.py](../../../src/backtest/macro.py) · `L159` |
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

<a id="unit-a92846cf7a"></a>

### UNIT-A92846CF7A

**模块**：`src/backtest/metrics.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A92846CF7A |
| 源码 | [src/backtest/metrics.py](../../../src/backtest/metrics.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | 实现“Point-in-time 回测”组件中 `src/backtest/metrics.py` 的职责，通过 `summarize_trades`、`group_trades` 提供该模块的公开能力。 |
| 关联需求 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 3 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_metrics.py](../../../tests/unit/test_backtest_metrics.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [summarize_trades](#fun-b1a235a7d0) | 汇总`trades`；返回 `dict` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_backtest_metrics.py](../../../tests/unit/test_backtest_metrics.py) |
| [group_trades](#fun-da4189939e) | 分组`trades`；返回 `list[dict]` 类型结果。 | 未检测到直接副作用 | — |

#### 函数导航

[_max_drawdown](#fun-b0fc151afd) · [summarize_trades](#fun-b1a235a7d0) · [group_trades](#fun-da4189939e)

<a id="fun-b0fc151afd"></a>

#### FUN-B0FC151AFD

| 设计项 | 说明 |
|---|---|
| 函数 | `_max_drawdown` |
| 源码位置 | [src/backtest/metrics.py](../../../src/backtest/metrics.py) · `L11` |
| 签名 | `_max_drawdown(values: list[float])` |
| 参数 | `values`（list[float]）：待处理值集合 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`max_drawdown`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min` → `round`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、round |
| 复杂度 / 风险 | 分支 1；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b1a235a7d0"></a>

#### FUN-B1A235A7D0

| 设计项 | 说明 |
|---|---|
| 函数 | `summarize_trades` |
| 源码位置 | [src/backtest/metrics.py](../../../src/backtest/metrics.py) · `L22` |
| 签名 | `summarize_trades(trades: list[TradeResult])` |
| 参数 | `trades`（list[TradeResult]）：由 `trades` 表示的输入集合 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 汇总`trades`；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `t.exit_reason.startswith` → `sum` → `abs` → `round` → `_max_drawdown`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | t.exit_reason.startswith、sum、abs、len、round、_max_drawdown |
| 复杂度 / 风险 | 分支 11；跨度 27 行；高 |
| 测试 / 验证 | [tests/unit/test_backtest_metrics.py](../../../tests/unit/test_backtest_metrics.py) · 直接动态测试 |

<a id="fun-da4189939e"></a>

#### FUN-DA4189939E

| 设计项 | 说明 |
|---|---|
| 函数 | `group_trades` |
| 源码位置 | [src/backtest/metrics.py](../../../src/backtest/metrics.py) · `L51` |
| 签名 | `group_trades(trades: Iterable[TradeResult], key: str)` |
| 参数 | `trades`（Iterable[TradeResult]）：由 `trades` 表示的输入集合<br>`key`（str）：索引键 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 分组`trades`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `defaultdict` → `append` → `getattr` → `sorted` → `buckets.items` → `summarize_trades` → `rows.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | defaultdict、append、str、getattr、sorted、buckets.items、summarize_trades、rows.append |
| 复杂度 / 风险 | 分支 2；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-d6d81aa6c4"></a>

### UNIT-D6D81AA6C4

**模块**：`src/backtest/simulator.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D6D81AA6C4 |
| 源码 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | 实现“Point-in-time 回测”组件中 `src/backtest/simulator.py` 的职责，通过 `simulate_signal` 提供该模块的公开能力。 |
| 关联需求 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 10 / 10 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_simulator.py](../../../tests/unit/test_backtest_simulator.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_signal_value](#fun-45cf111f4c) | 生成信号数值结果；返回实现分支产生的结果（源码未标注类型）。 | 未检测到直接副作用 | — |
| [_entry_price](#fun-c8726a960a) | 计算`entry_price`；返回 `float` 类型结果。 | 未检测到直接副作用 | — |
| [_fillable](#fun-45fe26e9d1) | 判断`fillable`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_risk_points](#fun-49b51b8f5c) | 计算`risk_points`；返回 `float` 类型结果。 | 未检测到直接副作用 | — |
| [_entered](#fun-fbd39fd99d) | 判断`entered`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_hit_stop](#fun-c957603ed9) | 停止`hit`；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_hit_tp](#fun-082bf9ce12) | 判断`hit_tp`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [_pnl_points](#fun-23462233b9) | 计算`pnl_points`；返回 `float` 类型结果。 | 未检测到直接副作用 | — |
| [_signal_metadata](#fun-58d5ab9bc5) | 构建`signal_metadata`；返回 `dict` 类型结果。 | 未检测到直接副作用 | — |
| [simulate_signal](#fun-203e3a1ea2) | 模拟交易信号；返回 `TradeResult` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_backtest_simulator.py](../../../tests/unit/test_backtest_simulator.py) |

#### 函数导航

[_signal_value](#fun-45cf111f4c) · [_entry_price](#fun-c8726a960a) · [_fillable](#fun-45fe26e9d1) · [_risk_points](#fun-49b51b8f5c) · [_entered](#fun-fbd39fd99d) · [_hit_stop](#fun-c957603ed9) · [_hit_tp](#fun-082bf9ce12) · [_pnl_points](#fun-23462233b9) · [_signal_metadata](#fun-58d5ab9bc5) · [simulate_signal](#fun-203e3a1ea2)

<a id="fun-45cf111f4c"></a>

#### FUN-45CF111F4C

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_value` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L11` |
| 签名 | `_signal_value(signal: TradingSignal \| dict, key: str, default=None)` |
| 参数 | `signal`（TradingSignal \| dict）：当前交易信号<br>`key`（str）：索引键<br>`default`（实现约定类型）：由调用方提供的 `default` 输入对象；默认值 `None` |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 生成信号数值结果；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `signal.get` → `getattr`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、signal.get、getattr |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c8726a960a"></a>

#### FUN-C8726A960A

| 设计项 | 说明 |
|---|---|
| 函数 | `_entry_price` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L17` |
| 签名 | `_entry_price(signal: TradingSignal \| dict, direction: str, slippage: float)` |
| 参数 | `signal`（TradingSignal \| dict）：当前交易信号<br>`direction`（str）：交易方向<br>`slippage`（float）：由 `slippage` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`entry_price`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_signal_value`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_signal_value |
| 复杂度 / 风险 | 分支 1；跨度 6 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-45fe26e9d1"></a>

#### FUN-45FE26E9D1

| 设计项 | 说明 |
|---|---|
| 函数 | `_fillable` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L25` |
| 签名 | `_fillable(row: pd.Series, entry: float)` |
| 参数 | `row`（pd.Series）：当前记录行<br>`entry`（float）：入场价格或入场记录 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`fillable`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-49b51b8f5c"></a>

#### FUN-49B51B8F5C

| 设计项 | 说明 |
|---|---|
| 函数 | `_risk_points` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L29` |
| 签名 | `_risk_points(entry: float, stop: float, direction: str)` |
| 参数 | `entry`（float）：入场价格或入场记录<br>`stop`（float）：由 `stop` 表示的数值参数<br>`direction`（str）：交易方向 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`risk_points`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fbd39fd99d"></a>

#### FUN-FBD39FD99D

| 设计项 | 说明 |
|---|---|
| 函数 | `_entered` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L35` |
| 签名 | `_entered(row: pd.Series, entry: float)` |
| 参数 | `row`（pd.Series）：当前记录行<br>`entry`（float）：入场价格或入场记录 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`entered`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_fillable`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _fillable |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c957603ed9"></a>

#### FUN-C957603ED9

| 设计项 | 说明 |
|---|---|
| 函数 | `_hit_stop` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L39` |
| 签名 | `_hit_stop(row: pd.Series, stop: float, direction: str)` |
| 参数 | `row`（pd.Series）：当前记录行<br>`stop`（float）：由 `stop` 表示的数值参数<br>`direction`（str）：交易方向 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 停止`hit`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-082bf9ce12"></a>

#### FUN-082BF9CE12

| 设计项 | 说明 |
|---|---|
| 函数 | `_hit_tp` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L45` |
| 签名 | `_hit_tp(row: pd.Series, tp: float, direction: str)` |
| 参数 | `row`（pd.Series）：当前记录行<br>`tp`（float）：由 `tp` 表示的数值参数<br>`direction`（str）：交易方向 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`hit_tp`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-23462233b9"></a>

#### FUN-23462233B9

| 设计项 | 说明 |
|---|---|
| 函数 | `_pnl_points` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L51` |
| 签名 | `_pnl_points(entry: float, exit_price: float, direction: str, fee_points: float)` |
| 参数 | `entry`（float）：入场价格或入场记录<br>`exit_price`（float）：当前或待评估价格<br>`direction`（str）：交易方向<br>`fee_points`（float）：由 `fee_points` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`pnl_points`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 3 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-58d5ab9bc5"></a>

#### FUN-58D5AB9BC5

| 设计项 | 说明 |
|---|---|
| 函数 | `_signal_metadata` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L56` |
| 签名 | `_signal_metadata(signal: TradingSignal \| dict)` |
| 参数 | `signal`（TradingSignal \| dict）：当前交易信号 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 构建`signal_metadata`；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_signal_value`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _signal_value |
| 复杂度 / 风险 | 分支 0；跨度 7 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-203e3a1ea2"></a>

#### FUN-203E3A1EA2

| 设计项 | 说明 |
|---|---|
| 函数 | `simulate_signal` |
| 源码位置 | [src/backtest/simulator.py](../../../src/backtest/simulator.py) · `L65` |
| 签名 | `simulate_signal(signal: TradingSignal \| dict, future_5m: pd.DataFrame, signal_time: pd.Timestamp, config: BacktestConfig)` |
| 参数 | `signal`（TradingSignal \| dict）：当前交易信号<br>`future_5m`（pd.DataFrame）：由调用方提供的 `future_5m` 输入对象<br>`signal_time`（pd.Timestamp）：事件或数据时间<br>`config`（BacktestConfig）：运行配置 |
| 返回 | 返回 `TradeResult` 类型结果 |
| 职责 | 模拟交易信号；返回 `TradeResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `_signal_value` → `_entry_price` → `TradeResult` → `_signal_metadata` → `_risk_points` → `enumerate` → `bars.iterrows`；包含 8 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `TradeResult` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、str、_signal_value、float、_entry_price、TradeResult、_signal_metadata、_risk_points、enumerate、bars.iterrows、_entered、len、active.iterrows、_hit_stop、next、_hit_tp、_pnl_points、round |
| 复杂度 / 风险 | 分支 8；跨度 156 行；高 |
| 测试 / 验证 | [tests/unit/test_backtest_simulator.py](../../../tests/unit/test_backtest_simulator.py) · 直接动态测试 |

<a id="unit-a71e1f8ce9"></a>

### UNIT-A71E1F8CE9

**模块**：`src/backtest/types.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A71E1F8CE9 |
| 源码 | [src/backtest/types.py](../../../src/backtest/types.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | 实现“Point-in-time 回测”组件中 `src/backtest/types.py` 的职责，通过 `BacktestMode`、`BacktestConfig`、`MacroReplayState`、`TradeResult`、`BacktestResult` 提供该模块的公开能力。 |
| 关联需求 | [SWR-BT-001](../SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 5 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](../SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_metrics.py](../../../tests/unit/test_backtest_metrics.py)、[tests/unit/test_backtest_simulator.py](../../../tests/unit/test_backtest_simulator.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [TradeResult.triggered](#fun-56d05c06ee) | 判断`triggered`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [TradeResult.won](#fun-e8ac0554d3) | 判断`won`条件是否成立；返回 `bool` 类型结果。 | 未检测到直接副作用 | — |
| [TradeResult.to_dict](#fun-f9db9c8f7c) | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |

#### 函数导航

[MacroReplayState.to_dict](#fun-e85e437686) · [TradeResult.triggered](#fun-56d05c06ee) · [TradeResult.won](#fun-e8ac0554d3) · [TradeResult.to_dict](#fun-f9db9c8f7c) · [BacktestResult.to_dict](#fun-8075ec23fd)

<a id="fun-e85e437686"></a>

#### FUN-E85E437686

| 设计项 | 说明 |
|---|---|
| 函数 | `MacroReplayState.to_dict` |
| 源码位置 | [src/backtest/types.py](../../../src/backtest/types.py) · `L53` |
| 签名 | `MacroReplayState.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict、str |
| 复杂度 / 风险 | 分支 1；跨度 6 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-56d05c06ee"></a>

#### FUN-56D05C06EE

| 设计项 | 说明 |
|---|---|
| 函数 | `TradeResult.triggered` |
| 源码位置 | [src/backtest/types.py](../../../src/backtest/types.py) · `L81` |
| 签名 | `TradeResult.triggered(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`triggered`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e8ac0554d3"></a>

#### FUN-E8AC0554D3

| 设计项 | 说明 |
|---|---|
| 函数 | `TradeResult.won` |
| 源码位置 | [src/backtest/types.py](../../../src/backtest/types.py) · `L85` |
| 签名 | `TradeResult.won(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`won`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f9db9c8f7c"></a>

#### FUN-F9DB9C8F7C

| 设计项 | 说明 |
|---|---|
| 函数 | `TradeResult.to_dict` |
| 源码位置 | [src/backtest/types.py](../../../src/backtest/types.py) · `L88` |
| 签名 | `TradeResult.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict、str |
| 复杂度 / 风险 | 分支 2；跨度 6 行；高 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-8075ec23fd"></a>

#### FUN-8075EC23FD

| 设计项 | 说明 |
|---|---|
| 函数 | `BacktestResult.to_dict` |
| 源码位置 | [src/backtest/types.py](../../../src/backtest/types.py) · `L105` |
| 签名 | `BacktestResult.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict` → `t.to_dict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict、t.to_dict |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |
