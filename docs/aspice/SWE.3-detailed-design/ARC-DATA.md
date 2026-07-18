# ARC-DATA — 行情与外部数据

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-data)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/data/__init__.py](#unit-5c9ecc73e4) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/aggregator.py](#unit-d3b9beaac0) | 4 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/calendar_utils.py](#unit-f5d8bd410b) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/context_builder.py](#unit-24843ac961) | 10 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/external_format.py](#unit-05079ecc27) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/fetch_pipeline.py](#unit-2b33a302fc) | 7 | 5 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/fetcher.py](#unit-5c3b60e30a) | 7 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/mt5.py](#unit-52888d723d) | 13 | 5 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/news_topics.py](#unit-c335b8f5cf) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/proxy_env.py](#unit-0f842b8ece) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive.py](#unit-ea7e4f88fe) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_compat.py](#unit-023a37a1e9) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_index.py](#unit-7bfc490988) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_prune.py](#unit-dad8bc5b0f) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_schema.py](#unit-767bf49f25) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/__init__.py](#unit-c3952c43cb) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/_http.py](#unit-c590fce576) | 3 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/base.py](#unit-0df4638d5e) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/dxy.py](#unit-1fa1bdf5ba) | 1 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/fundamentals.py](#unit-ec9b21793d) | 4 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/gold_relevance.py](#unit-4d4d8a02c7) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/jin10_feed.py](#unit-7020937074) | 23 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/jin10_mcp_client.py](#unit-927bb1749d) | 10 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/macro.py](#unit-fe5c27c113) | 5 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/market.py](#unit-603339624c) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/news.py](#unit-58d6f95301) | 4 | 2 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/social.py](#unit-ba8df8a829) | 3 | 3 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/social_feed.py](#unit-b05f7affa4) | 11 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/tradingview.py](#unit-c1711535ca) | 15 | 4 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/url_redact.py](#unit-62a1aff305) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) | selected |

<a id="unit-5c9ecc73e4"></a>

### UNIT-5C9ECC73E4

**模块**：`src/data/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5C9ECC73E4 |
| 源码 | [src/data/__init__.py](../../../src/data/__init__.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-d3b9beaac0"></a>

### UNIT-D3B9BEAAC0

**模块**：`src/data/aggregator.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D3B9BEAAC0 |
| 源码 | [src/data/aggregator.py](../../../src/data/aggregator.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/aggregator.py` 的职责，通过 `merge_external`、`collect_evidence`、`assemble_market_context`、`build_market_context` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 4 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [merge_external](#fun-4e87068569) | 合并外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py) |
| [collect_evidence](#fun-8b8349b09e) | 收集证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 | 外部接口 I/O | — |
| [build_market_context](#fun-e8cc53e6f4) | 构建`market_context`；可能影响外部接口；返回 `MarketContext` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[merge_external](#fun-4e87068569) · [collect_evidence](#fun-8b8349b09e) · [assemble_market_context](#fun-ddf5efe045) · [build_market_context](#fun-e8cc53e6f4)

<a id="fun-4e87068569"></a>

#### FUN-4E87068569

| 设计项 | 说明 |
|---|---|
| 函数 | `merge_external` |
| 源码位置 | [src/data/aggregator.py](../../../src/data/aggregator.py) · `L22` |
| 签名 | `merge_external(*parts: ExternalFactors)` |
| 参数 | `*parts`：附加位置参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 合并外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ExternalFactors` → `merged.news_headlines.extend` → `merged.headline_items.extend` → `merged.calendar_events.extend` → `merged.macro_quotes.extend` → `merged.social_posts.extend` → `merged.fetch_errors.extend` → `merged.sources.append`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ExternalFactors、merged.news_headlines.extend、merged.headline_items.extend、merged.calendar_events.extend、merged.macro_quotes.extend、merged.social_posts.extend、merged.fetch_errors.extend、merged.sources.append、sync_external_legacy_fields |
| 复杂度 / 风险 | 分支 6；跨度 22 行；高 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py) · 直接动态测试 |

<a id="fun-8b8349b09e"></a>

#### FUN-8B8349B09E

| 设计项 | 说明 |
|---|---|
| 函数 | `collect_evidence` |
| 源码位置 | [src/data/aggregator.py](../../../src/data/aggregator.py) · `L46` |
| 签名 | `collect_evidence(enriched: dict[str, pd.DataFrame])` |
| 参数 | `enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 收集证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `items.extend` → `fetch_evidence` → `MarketDataSource` → `NewsDataSource` → `SocialDataSource` → `FundamentalsDataSource`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | items.extend、fetch_evidence、MarketDataSource、NewsDataSource、SocialDataSource、FundamentalsDataSource |
| 复杂度 / 风险 | 分支 0；跨度 7 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ddf5efe045"></a>

#### FUN-DDF5EFE045

| 设计项 | 说明 |
|---|---|
| 函数 | `assemble_market_context` |
| 源码位置 | [src/data/aggregator.py](../../../src/data/aggregator.py) · `L55` |
| 签名 | `assemble_market_context(enriched: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], external: ExternalFactors, source_label: str)` |
| 参数 | `enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据<br>`analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果<br>`external`（ExternalFactors）：由调用方提供的 `external` 输入对象<br>`source_label`（str）：展示或分类标签 |
| 返回 | 返回 `MarketContext` 类型结果 |
| 职责 | 生成`assemble_market_context`结果；返回 `MarketContext` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `daily_metrics` → `MarketContext` → `finalize_market_context`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `MarketContext` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | daily_metrics、MarketContext、float、finalize_market_context |
| 复杂度 / 风险 | 分支 0；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e8cc53e6f4"></a>

#### FUN-E8CC53E6F4

| 设计项 | 说明 |
|---|---|
| 函数 | `build_market_context` |
| 源码位置 | [src/data/aggregator.py](../../../src/data/aggregator.py) · `L76` |
| 签名 | `build_market_context(enriched: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis])` |
| 参数 | `enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据<br>`analyses`（dict[str, TimeframeAnalysis]）：各时间框架分析结果 |
| 返回 | 返回 `MarketContext` 类型结果 |
| 职责 | 构建`market_context`；可能影响外部接口；返回 `MarketContext` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_external_bundle` → `assemble_market_context` → `get_active_source`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `MarketContext` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_external_bundle、assemble_market_context、get_active_source |
| 复杂度 / 风险 | 分支 0；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-f5d8bd410b"></a>

### UNIT-F5D8BD410B

**模块**：`src/data/calendar_utils.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F5D8BD410B |
| 源码 | [src/data/calendar_utils.py](../../../src/data/calendar_utils.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/calendar_utils.py` 的职责，通过 `parse_event_time`、`filter_upcoming_calendar_events`、`calendar_to_risk_text` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 函数导航

[parse_event_time](#fun-be22aae06a) · [filter_upcoming_calendar_events](#fun-07d2119d72) · [calendar_to_risk_text](#fun-d55bebcd6f)

<a id="fun-be22aae06a"></a>

#### FUN-BE22AAE06A

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_event_time` |
| 源码位置 | [src/data/calendar_utils.py](../../../src/data/calendar_utils.py) · `L11` |
| 签名 | `parse_event_time(raw: str)` |
| 参数 | `raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `datetime \| None` 类型结果 |
| 职责 | 解析`event_time`；返回 `datetime \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `datetime.strptime` → `re.search` → `match.group`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `datetime \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、datetime.strptime、re.search、match.group |
| 复杂度 / 风险 | 分支 5；跨度 22 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-07d2119d72"></a>

#### FUN-07D2119D72

| 设计项 | 说明 |
|---|---|
| 函数 | `filter_upcoming_calendar_events` |
| 源码位置 | [src/data/calendar_utils.py](../../../src/data/calendar_utils.py) · `L35` |
| 签名 | `filter_upcoming_calendar_events(events: list[CalendarEvent])` |
| 参数 | `events`（list[CalendarEvent]）：事件集合 |
| 返回 | 返回 `list[CalendarEvent]` 类型结果 |
| 职责 | 筛选`upcoming_calendar_events`；返回 `list[CalendarEvent]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `datetime.now` → `parse_event_time` → `total_seconds` → `kept.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[CalendarEvent]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | datetime.now、parse_event_time、total_seconds、kept.append |
| 复杂度 / 风险 | 分支 3；跨度 12 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) · 直接动态测试 |

<a id="fun-d55bebcd6f"></a>

#### FUN-D55BEBCD6F

| 设计项 | 说明 |
|---|---|
| 函数 | `calendar_to_risk_text` |
| 源码位置 | [src/data/calendar_utils.py](../../../src/data/calendar_utils.py) · `L49` |
| 签名 | `calendar_to_risk_text(events: list[CalendarEvent], *, limit: int=6)` |
| 参数 | `events`（list[CalendarEvent]）：事件集合<br>`limit`（int）：返回或处理数量上限；默认值 `6` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`calendar_to_risk_text`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `join` → `e.display`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | join、e.display |
| 复杂度 / 风险 | 分支 1；跨度 4 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-24843ac961"></a>

### UNIT-24843AC961

**模块**：`src/data/context_builder.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-24843AC961 |
| 源码 | [src/data/context_builder.py](../../../src/data/context_builder.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/context_builder.py` 的职责，通过 `build_market_position`、`build_spot_cross_check`、`build_event_countdown`、`build_jin10_kline_summary`、`build_derived_context`、`compute_context_stats`、`finalize_market_context` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 10 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [build_derived_context](#fun-21a4a84fe5) | 构建`derived_context`；可能影响外部接口；返回 `dict[str, Any]` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[build_market_position](#fun-750f9f2cf5) · [build_spot_cross_check](#fun-046ae84c1b) · [build_event_countdown](#fun-bc16d7a171) · [build_jin10_kline_summary](#fun-94a1869676) · [build_derived_context](#fun-21a4a84fe5) · [compute_context_stats](#fun-53864154eb) · [_technical_input_stats](#fun-309515b2c5) · [_volume_nonzero_ratio](#fun-12577f43a5) · [_analyst_input_stats](#fun-14f86ea322) · [finalize_market_context](#fun-260ff71074)

<a id="fun-750f9f2cf5"></a>

#### FUN-750F9F2CF5

| 设计项 | 说明 |
|---|---|
| 函数 | `build_market_position` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L44` |
| 签名 | `build_market_position(enriched: dict[str, pd.DataFrame], price: float)` |
| 参数 | `enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据<br>`price`（float）：当前或待评估价格 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`market_position`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ema_relation` → `round` → `relations.items` → `pd.notna` → `tail` → `max` → `min`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ema_relation、round、float、relations.items、pd.notna、len、tail、max、min |
| 复杂度 / 风险 | 分支 2；跨度 22 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-046ae84c1b"></a>

#### FUN-046AE84C1B

| 设计项 | 说明 |
|---|---|
| 函数 | `build_spot_cross_check` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L68` |
| 签名 | `build_spot_cross_check(tv_price: float, quote: dict[str, Any] \| None)` |
| 参数 | `tv_price`（float）：当前或待评估价格<br>`quote`（dict[str, Any] \| None）：由 `quote` 表示的键值映射 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`spot_cross_check`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `quote.get` → `abs` → `round`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、quote.get、abs、round |
| 复杂度 / 风险 | 分支 3；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-bc16d7a171"></a>

#### FUN-BC16D7A171

| 设计项 | 说明 |
|---|---|
| 函数 | `build_event_countdown` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L89` |
| 签名 | `build_event_countdown(events: list[CalendarEvent])` |
| 参数 | `events`（list[CalendarEvent]）：事件集合 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`event_countdown`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `datetime.now` → `filter_upcoming_calendar_events` → `parse_event_time` → `total_seconds` → `round`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | datetime.now、filter_upcoming_calendar_events、parse_event_time、total_seconds、round |
| 复杂度 / 风险 | 分支 6；跨度 26 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-94a1869676"></a>

#### FUN-94A1869676

| 设计项 | 说明 |
|---|---|
| 函数 | `build_jin10_kline_summary` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L117` |
| 签名 | `build_jin10_kline_summary(bars: list[dict[str, Any]], tv_price: float)` |
| 参数 | `bars`（list[dict[str, Any]]）：K 线记录集合<br>`tv_price`（float）：当前或待评估价格 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`jin10_kline_summary`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `last.get` → `first.get` → `abs` → `round`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、last.get、first.get、abs、len、round |
| 复杂度 / 风险 | 分支 6；跨度 26 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-21a4a84fe5"></a>

#### FUN-21A4A84FE5

| 设计项 | 说明 |
|---|---|
| 函数 | `build_derived_context` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L145` |
| 签名 | `build_derived_context(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`derived_context`；可能影响外部接口；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sentiment_score` → `filter_upcoming_calendar_events` → `sum` → `build_market_position` → `e.to_dict` → `cluster_headline_topics` → `build_event_countdown` → `fetch_jin10_quote`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sentiment_score、filter_upcoming_calendar_events、sum、build_market_position、e.to_dict、cluster_headline_topics、build_event_countdown、len、fetch_jin10_quote、build_spot_cross_check、fetch_jin10_kline、build_jin10_kline_summary |
| 复杂度 / 风险 | 分支 4；跨度 34 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-53864154eb"></a>

#### FUN-53864154EB

| 设计项 | 说明 |
|---|---|
| 函数 | `compute_context_stats` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L181` |
| 签名 | `compute_context_stats(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 计算`context_stats`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `ctx.analyses.values` → `_technical_input_stats` → `_analyst_input_stats` → `json.dumps` → `ctx.external.to_dict` → `payload_sample.encode`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、len、ctx.analyses.values、_technical_input_stats、_analyst_input_stats、list、json.dumps、ctx.external.to_dict、payload_sample.encode |
| 复杂度 / 风险 | 分支 1；跨度 19 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-309515b2c5"></a>

#### FUN-309515B2C5

| 设计项 | 说明 |
|---|---|
| 函数 | `_technical_input_stats` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L202` |
| 签名 | `_technical_input_stats(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`technical_input_stats`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ctx.enriched.items` → `support_resistance_context` → `pd.notna` → `ctx.analyses.items` → `bars.get` → `indicator_ready.get` → `_volume_nonzero_ratio` → `ctx.enriched.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、ctx.enriched.items、support_resistance_context、pd.notna、ctx.analyses.items、bars.get、indicator_ready.get、_volume_nonzero_ratio、ctx.enriched.get、sorted、set、sum、ctx.analyses.values、sr.get、technical_quality |
| 复杂度 / 风险 | 分支 3；跨度 52 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-12577f43a5"></a>

#### FUN-12577F43A5

| 设计项 | 说明 |
|---|---|
| 函数 | `_volume_nonzero_ratio` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L256` |
| 签名 | `_volume_nonzero_ratio(df: pd.DataFrame \| None)` |
| 参数 | `df`（pd.DataFrame \| None）：输入数据表 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`volume_nonzero_ratio`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `astype` → `round` → `sum`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | astype、round、float、sum、len |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-14f86ea322"></a>

#### FUN-14F86EA322

| 设计项 | 说明 |
|---|---|
| 函数 | `_analyst_input_stats` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L263` |
| 签名 | `_analyst_input_stats(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`analyst_input_stats`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `post.get` → `social_kind_counts.get` → `e.lower` → `ctx.derived.get` → `round`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、str、post.get、social_kind_counts.get、float、len、e.lower、ctx.derived.get、round、bool |
| 复杂度 / 风险 | 分支 2；跨度 52 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-260ff71074"></a>

#### FUN-260FF71074

| 设计项 | 说明 |
|---|---|
| 函数 | `finalize_market_context` |
| 源码位置 | [src/data/context_builder.py](../../../src/data/context_builder.py) · `L317` |
| 签名 | `finalize_market_context(ctx: MarketContext)` |
| 参数 | `ctx`（MarketContext）：运行上下文 |
| 返回 | 返回 `MarketContext` 类型结果 |
| 职责 | 生成`finalize_market_context`结果；返回 `MarketContext` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `filter_upcoming_calendar_events` → `sync_external_legacy_fields` → `build_derived_context` → `compute_context_stats`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `MarketContext` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | filter_upcoming_calendar_events、sync_external_legacy_fields、build_derived_context、compute_context_stats |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="unit-05079ecc27"></a>

### UNIT-05079ECC27

**模块**：`src/data/external_format.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-05079ECC27 |
| 源码 | [src/data/external_format.py](../../../src/data/external_format.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/external_format.py` 的职责，通过 `headlines_to_strings`、`sync_external_legacy_fields` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 函数导航

[headlines_to_strings](#fun-92f0ba6a2b) · [sync_external_legacy_fields](#fun-361441992e)

<a id="fun-92f0ba6a2b"></a>

#### FUN-92F0BA6A2B

| 设计项 | 说明 |
|---|---|
| 函数 | `headlines_to_strings` |
| 源码位置 | [src/data/external_format.py](../../../src/data/external_format.py) · `L13` |
| 签名 | `headlines_to_strings(items: list[HeadlineItem], *, limit: int \| None=None)` |
| 参数 | `items`（list[HeadlineItem]）：输入项集合<br>`limit`（int \| None）：返回或处理数量上限；默认值 `None` |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`headlines_to_strings`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.text.strip` → `seen.add` → `out.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、item.text.strip、seen.add、out.append、len |
| 复杂度 / 风险 | 分支 3；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-361441992e"></a>

#### FUN-361441992E

| 设计项 | 说明 |
|---|---|
| 函数 | `sync_external_legacy_fields` |
| 源码位置 | [src/data/external_format.py](../../../src/data/external_format.py) · `L28` |
| 签名 | `sync_external_legacy_fields(ext: ExternalFactors)` |
| 参数 | `ext`（ExternalFactors）：由调用方提供的 `ext` 输入对象 |
| 返回 | 无返回值（None） |
| 职责 | 执行`sync_external_legacy_fields`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `headlines_to_strings` → `filter_upcoming_calendar_events` → `log.info` → `calendar_to_risk_text`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | headlines_to_strings、filter_upcoming_calendar_events、len、log.info、calendar_to_risk_text |
| 复杂度 / 风险 | 分支 3；跨度 9 行；中 |
| 测试 / 验证 | [tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py) · 直接动态测试 |

<a id="unit-2b33a302fc"></a>

### UNIT-2B33A302FC

**模块**：`src/data/fetch_pipeline.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2B33A302FC |
| 源码 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/fetch_pipeline.py` 的职责，通过 `DataFetchResult`、`fetch_external_bundle`、`fetch_all_data` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 5 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_fetch_news_external](#fun-112152936c) | 获取`news_external`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| [_fetch_social_external](#fun-da07c46547) | 获取`social_external`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| [_fetch_fundamentals_external](#fun-984c9019fc) | 获取`fundamentals_external`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| [fetch_external_bundle](#fun-6df80aee05) | 获取`external_bundle`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| [fetch_all_data](#fun-d6c382b005) | 获取`all_data`；可能影响外部接口、共享状态；返回 `DataFetchResult` 类型结果。 | 外部接口 I/O；共享状态变更 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) |

#### 函数导航

[DataFetchResult.bars_summary](#fun-237e01db5b) · [DataFetchResult.external_preview](#fun-debf2265ca) · [_fetch_news_external](#fun-112152936c) · [_fetch_social_external](#fun-da07c46547) · [_fetch_fundamentals_external](#fun-984c9019fc) · [fetch_external_bundle](#fun-6df80aee05) · [fetch_all_data](#fun-d6c382b005)

<a id="fun-237e01db5b"></a>

#### FUN-237E01DB5B

| 设计项 | 说明 |
|---|---|
| 函数 | `DataFetchResult.bars_summary` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L34` |
| 签名 | `DataFetchResult.bars_summary(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, int]` 类型结果 |
| 职责 | 构建`bars_summary`；返回 `dict[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.raw.items`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、self.raw.items |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-debf2265ca"></a>

#### FUN-DEBF2265CA

| 设计项 | 说明 |
|---|---|
| 函数 | `DataFetchResult.external_preview` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L37` |
| 签名 | `DataFetchResult.external_preview(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 构建`external_preview`；返回 `dict` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len |
| 复杂度 / 风险 | 分支 0；跨度 15 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-112152936c"></a>

#### FUN-112152936C

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_news_external` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L54` |
| 签名 | `_fetch_news_external()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取`news_external`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_external` → `NewsDataSource`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_external、NewsDataSource |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-da07c46547"></a>

#### FUN-DA07C46547

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_social_external` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L58` |
| 签名 | `_fetch_social_external()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取`social_external`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_external` → `SocialDataSource`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_external、SocialDataSource |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-984c9019fc"></a>

#### FUN-984C9019FC

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_fundamentals_external` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L62` |
| 签名 | `_fetch_fundamentals_external()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取`fundamentals_external`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_external` → `FundamentalsDataSource`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_external、FundamentalsDataSource |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-6df80aee05"></a>

#### FUN-6DF80AEE05

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_external_bundle` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L66` |
| 签名 | `fetch_external_bundle(*, parallel_http: bool=True)` |
| 参数 | `parallel_http`（bool）：控制对应行为是否启用的布尔值；默认值 `True` |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取`external_bundle`；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ThreadPoolExecutor` → `pool.submit` → `fut_news.result` → `fut_social.result` → `fut_fund.result` → `_fetch_news_external` → `_fetch_fundamentals_external` → `_fetch_social_external`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ThreadPoolExecutor、pool.submit、fut_news.result、fut_social.result、fut_fund.result、_fetch_news_external、_fetch_fundamentals_external、_fetch_social_external、merge_external |
| 复杂度 / 风险 | 分支 1；跨度 15 行；高 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-d6c382b005"></a>

#### FUN-D6C382B005

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_all_data` |
| 源码位置 | [src/data/fetch_pipeline.py](../../../src/data/fetch_pipeline.py) · `L83` |
| 签名 | `fetch_all_data()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `DataFetchResult` 类型结果 |
| 职责 | 获取`all_data`；可能影响外部接口、共享状态；返回 `DataFetchResult` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_progress` → `time.perf_counter` → `prog.start` → `fetch_multi_timeframe` → `prog.fail` → `prog.update` → `fetch_external_bundle` → `get_active_source`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `DataFetchResult` 类型结果；可观察变化限于外部接口、共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O；共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_progress、time.perf_counter、prog.start、fetch_multi_timeframe、prog.fail、str、prog.update、fetch_external_bundle、get_active_source、int、len、raw.items、bars.get、ext_bits.append、DataFetchResult、prog.stage_io、json.dumps、result.external_preview、prog.done、join |
| 复杂度 / 风险 | 分支 5；跨度 62 行；高 |
| 测试 / 验证 | [tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py) · 直接动态测试 |

<a id="unit-5c3b60e30a"></a>

### UNIT-5C3B60E30A

**模块**：`src/data/fetcher.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5C3B60E30A |
| 源码 | [src/data/fetcher.py](../../../src/data/fetcher.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/fetcher.py` 的职责，通过 `clear_cache`、`get_active_source`、`fetch_multi_timeframe`、`fetch_all`、`daily_metrics`、`utc8_now`、`format_utc8` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [fetch_multi_timeframe](#fun-d6fbd9beaa) | 获取多时间框架分析；可能影响外部接口；返回 `dict[Timeframe, pd.DataFrame]` 类型结果。 | 外部接口 I/O | — |
| [fetch_all](#fun-1bb0e91f10) | 获取`all`；可能影响外部接口；返回 `'DataFetchResult'` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[clear_cache](#fun-f5cfdcfe8d) · [get_active_source](#fun-e9ad7716d7) · [fetch_multi_timeframe](#fun-d6fbd9beaa) · [fetch_all](#fun-1bb0e91f10) · [daily_metrics](#fun-5a69f43861) · [utc8_now](#fun-f3d127c2a7) · [format_utc8](#fun-782624f6ed)

<a id="fun-f5cfdcfe8d"></a>

#### FUN-F5CFDCFE8D

| 设计项 | 说明 |
|---|---|
| 函数 | `clear_cache` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L18` |
| 签名 | `clear_cache()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`clear_cache`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `log.debug` → `tradingview.reset_client`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.debug、tradingview.reset_client |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py) · 直接动态测试 |

<a id="fun-e9ad7716d7"></a>

#### FUN-E9AD7716D7

| 设计项 | 说明 |
|---|---|
| 函数 | `get_active_source` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L23` |
| 签名 | `get_active_source()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 获取`active_source`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `tradingview.source_label`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | tradingview.source_label |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d6fbd9beaa"></a>

#### FUN-D6FBD9BEAA

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_multi_timeframe` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L27` |
| 签名 | `fetch_multi_timeframe()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[Timeframe, pd.DataFrame]` 类型结果 |
| 职责 | 获取多时间框架分析；可能影响外部接口；返回 `dict[Timeframe, pd.DataFrame]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `tradingview.fetch_multi_timeframe`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `dict[Timeframe, pd.DataFrame]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | tradingview.fetch_multi_timeframe |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1bb0e91f10"></a>

#### FUN-1BB0E91F10

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_all` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L31` |
| 签名 | `fetch_all()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `'DataFetchResult'` 类型结果 |
| 职责 | 获取`all`；可能影响外部接口；返回 `'DataFetchResult'` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_all_data`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `'DataFetchResult'` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_all_data |
| 复杂度 / 风险 | 分支 0；跨度 5 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5a69f43861"></a>

#### FUN-5A69F43861

| 设计项 | 说明 |
|---|---|
| 函数 | `daily_metrics` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L38` |
| 签名 | `daily_metrics(df_1d: pd.DataFrame)` |
| 参数 | `df_1d`（pd.DataFrame）：由调用方提供的 `df_1d` 输入对象 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 构建`daily_metrics`；返回 `dict` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、float |
| 复杂度 / 风险 | 分支 2；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_indicators.py](../../../tests/unit/test_indicators.py) · 直接动态测试 |

<a id="fun-f3d127c2a7"></a>

#### FUN-F3D127C2A7

| 设计项 | 说明 |
|---|---|
| 函数 | `utc8_now` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L71` |
| 签名 | `utc8_now()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `datetime` 类型结果 |
| 职责 | 生成`utc8_now`结果；返回 `datetime` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `datetime.now`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `datetime` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | datetime.now |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-782624f6ed"></a>

#### FUN-782624F6ED

| 设计项 | 说明 |
|---|---|
| 函数 | `format_utc8` |
| 源码位置 | [src/data/fetcher.py](../../../src/data/fetcher.py) · `L75` |
| 签名 | `format_utc8(iso_value: object, *, fmt: str='%Y-%m-%d %H:%M')` |
| 参数 | `iso_value`（object）：待处理值<br>`fmt`（str）：由 `fmt` 表示的文本或标识；默认值 `'%Y-%m-%d %H:%M'` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`utc8`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `isdigit` → `raw.rstrip` → `replace` → `datetime.strptime` → `dt.astimezone` → `local.strftime` → `raw.replace`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、len、isdigit、raw.rstrip、replace、datetime.strptime、dt.astimezone、local.strftime、raw.replace、datetime.fromisoformat、dt.replace |
| 复杂度 / 风险 | 分支 5；跨度 22 行；中 |
| 测试 / 验证 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="unit-52888d723d"></a>

### UNIT-52888D723D

**模块**：`src/data/mt5.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-52888D723D |
| 源码 | [src/data/mt5.py](../../../src/data/mt5.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/mt5.py` 的职责，通过 `MT5Config`、`MT5Provider`、`MT5UnavailableError`、`DisabledMT5Provider`、`MetaTrader5Provider`、`get_mt5_provider` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 13 / 5 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [MetaTrader5Provider.__init__](#fun-efaf091f3b) | 初始化当前类实例并建立字段约束；无返回值（None）。 | 未检测到直接副作用 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) |
| [MetaTrader5Provider.is_available](#fun-d4e9736d8a) | 判断`available`；返回 `bool` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) |
| [MetaTrader5Provider.account_info](#fun-2c7542532d) | 构建交易账户信息；返回 `dict[str, object]` 类型结果。 | 未检测到直接副作用 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) |
| [MetaTrader5Provider.shutdown](#fun-573d1aeba3) | 执行`shutdown`处理；无返回值（None）。 | 未检测到直接副作用 | — |
| [MetaTrader5Provider._ensure_initialized](#fun-f8948e51cb) | 确保`initialized`；无返回值（None）。 | 未检测到直接副作用 | — |

#### 函数导航

[MT5Provider.is_available](#fun-a41f07faab) · [MT5Provider.account_info](#fun-a1dfe3ce6d) · [MT5Provider.shutdown](#fun-2ceb3ae7c8) · [DisabledMT5Provider.__init__](#fun-eba1ab6898) · [DisabledMT5Provider.is_available](#fun-142d9a85d4) · [DisabledMT5Provider.account_info](#fun-a96d8007a3) · [DisabledMT5Provider.shutdown](#fun-0f677dda5e) · [MetaTrader5Provider.__init__](#fun-efaf091f3b) · [MetaTrader5Provider.is_available](#fun-d4e9736d8a) · [MetaTrader5Provider.account_info](#fun-2c7542532d) · [MetaTrader5Provider.shutdown](#fun-573d1aeba3) · [MetaTrader5Provider._ensure_initialized](#fun-f8948e51cb) · [get_mt5_provider](#fun-28bba5cb4c)

<a id="fun-a41f07faab"></a>

#### FUN-A41F07FAAB

| 设计项 | 说明 |
|---|---|
| 函数 | `MT5Provider.is_available` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L40` |
| 签名 | `MT5Provider.is_available(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`available`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="fun-a1dfe3ce6d"></a>

#### FUN-A1DFE3CE6D

| 设计项 | 说明 |
|---|---|
| 函数 | `MT5Provider.account_info` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L43` |
| 签名 | `MT5Provider.account_info(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, object]` 类型结果 |
| 职责 | 构建交易账户信息；返回 `dict[str, object]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, object]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="fun-2ceb3ae7c8"></a>

#### FUN-2CEB3AE7C8

| 设计项 | 说明 |
|---|---|
| 函数 | `MT5Provider.shutdown` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L46` |
| 签名 | `MT5Provider.shutdown(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`shutdown`处理；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-eba1ab6898"></a>

#### FUN-EBA1AB6898

| 设计项 | 说明 |
|---|---|
| 函数 | `DisabledMT5Provider.__init__` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L57` |
| 签名 | `DisabledMT5Provider.__init__(self, reason: str='MT5_ENABLED=false')` |
| 参数 | `reason`（str）：判定或拒绝原因；默认值 `'MT5_ENABLED=false'` |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-142d9a85d4"></a>

#### FUN-142D9A85D4

| 设计项 | 说明 |
|---|---|
| 函数 | `DisabledMT5Provider.is_available` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L60` |
| 签名 | `DisabledMT5Provider.is_available(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`available`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="fun-a96d8007a3"></a>

#### FUN-A96D8007A3

| 设计项 | 说明 |
|---|---|
| 函数 | `DisabledMT5Provider.account_info` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L63` |
| 签名 | `DisabledMT5Provider.account_info(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, object]` 类型结果 |
| 职责 | 构建交易账户信息；返回 `dict[str, object]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `MT5UnavailableError`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, object]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | MT5UnavailableError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | MT5UnavailableError |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="fun-0f677dda5e"></a>

#### FUN-0F677DDA5E

| 设计项 | 说明 |
|---|---|
| 函数 | `DisabledMT5Provider.shutdown` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L66` |
| 签名 | `DisabledMT5Provider.shutdown(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`shutdown`处理；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-efaf091f3b"></a>

#### FUN-EFAF091F3B

| 设计项 | 说明 |
|---|---|
| 函数 | `MetaTrader5Provider.__init__` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L73` |
| 签名 | `MetaTrader5Provider.__init__(self, config: MT5Config \| None=None)` |
| 参数 | `config`（MT5Config \| None）：运行配置；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `MT5Config` → `MT5UnavailableError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | MT5UnavailableError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | MT5Config、MT5UnavailableError |
| 复杂度 / 风险 | 分支 1；跨度 8 行；高 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-d4e9736d8a"></a>

#### FUN-D4E9736D8A

| 设计项 | 说明 |
|---|---|
| 函数 | `MetaTrader5Provider.is_available` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L82` |
| 签名 | `MetaTrader5Provider.is_available(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`available`；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self._ensure_initialized`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._ensure_initialized |
| 复杂度 / 风险 | 分支 1；跨度 6 行；高 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="fun-2c7542532d"></a>

#### FUN-2C7542532D

| 设计项 | 说明 |
|---|---|
| 函数 | `MetaTrader5Provider.account_info` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L89` |
| 签名 | `MetaTrader5Provider.account_info(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, object]` 类型结果 |
| 职责 | 构建交易账户信息；返回 `dict[str, object]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self._ensure_initialized` → `self._mt5.account_info` → `self._mt5.last_error` → `MT5UnavailableError` → `info._asdict` → `data.get`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, object]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | MT5UnavailableError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._ensure_initialized、self._mt5.account_info、self._mt5.last_error、MT5UnavailableError、info._asdict、data.get |
| 复杂度 / 风险 | 分支 1；跨度 17 行；高 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="fun-573d1aeba3"></a>

#### FUN-573D1AEBA3

| 设计项 | 说明 |
|---|---|
| 函数 | `MetaTrader5Provider.shutdown` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L107` |
| 签名 | `MetaTrader5Provider.shutdown(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`shutdown`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._mt5.shutdown`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._mt5.shutdown |
| 复杂度 / 风险 | 分支 1；跨度 4 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f8948e51cb"></a>

#### FUN-F8948E51CB

| 设计项 | 说明 |
|---|---|
| 函数 | `MetaTrader5Provider._ensure_initialized` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L112` |
| 签名 | `MetaTrader5Provider._ensure_initialized(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 确保`initialized`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._mt5.initialize` → `self._mt5.last_error` → `MT5UnavailableError`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | MT5UnavailableError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、self._mt5.initialize、self._mt5.last_error、MT5UnavailableError |
| 复杂度 / 风险 | 分支 6；跨度 17 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-28bba5cb4c"></a>

#### FUN-28BBA5CB4C

| 设计项 | 说明 |
|---|---|
| 函数 | `get_mt5_provider` |
| 源码位置 | [src/data/mt5.py](../../../src/data/mt5.py) · `L131` |
| 签名 | `get_mt5_provider(config: MT5Config \| None=None)` |
| 参数 | `config`（MT5Config \| None）：运行配置；默认值 `None` |
| 返回 | 返回 `MT5Provider` 类型结果 |
| 职责 | 获取`mt5_provider`；返回 `MT5Provider` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `MT5Config` → `DisabledMT5Provider` → `MetaTrader5Provider`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `MT5Provider` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | MT5Config、DisabledMT5Provider、MetaTrader5Provider、str |
| 复杂度 / 风险 | 分支 2；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_mt5_provider.py](../../../tests/unit/test_mt5_provider.py) · 直接动态测试 |

<a id="unit-c335b8f5cf"></a>

### UNIT-C335B8F5CF

**模块**：`src/data/news_topics.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C335B8F5CF |
| 源码 | [src/data/news_topics.py](../../../src/data/news_topics.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/news_topics.py` 的职责，通过 `cluster_headline_topics` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[cluster_headline_topics](#fun-1ed76ebfc7)

<a id="fun-1ed76ebfc7"></a>

#### FUN-1ED76EBFC7

| 设计项 | 说明 |
|---|---|
| 函数 | `cluster_headline_topics` |
| 源码位置 | [src/data/news_topics.py](../../../src/data/news_topics.py) · `L17` |
| 签名 | `cluster_headline_topics(items: list[HeadlineItem], *, max_topics: int=3)` |
| 参数 | `items`（list[HeadlineItem]）：输入项集合<br>`max_topics`（int）：由 `max_topics` 表示的数值参数；默认值 `3` |
| 返回 | 返回 `list[dict[str, object]]` 类型结果 |
| 职责 | 构建`cluster_headline_topics`；返回 `list[dict[str, object]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.text.lower` → `any` → `k.lower` → `append` → `buckets.items` → `topics.append` → `topics.sort`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, object]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | item.text.lower、any、k.lower、append、buckets.items、topics.append、len、topics.sort、int |
| 复杂度 / 风险 | 分支 5；跨度 27 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="unit-0f842b8ece"></a>

### UNIT-0F842B8ECE

**模块**：`src/data/proxy_env.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0F842B8ECE |
| 源码 | [src/data/proxy_env.py](../../../src/data/proxy_env.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/proxy_env.py` 的职责，通过 `read_system_proxy`、`apply_system_proxy` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[read_system_proxy](#fun-ce8b65f86a) · [apply_system_proxy](#fun-2365b1ea92)

<a id="fun-ce8b65f86a"></a>

#### FUN-CE8B65F86A

| 设计项 | 说明 |
|---|---|
| 函数 | `read_system_proxy` |
| 源码位置 | [src/data/proxy_env.py](../../../src/data/proxy_env.py) · `L8` |
| 签名 | `read_system_proxy()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 读取系统代理配置；可能影响文件系统、共享状态；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `os.environ.get` → `winreg.OpenKey` → `winreg.QueryValueEx` → `strip` → `server.split` → `winreg.CloseKey`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `str \| None` 类型结果；可观察变化限于文件系统、共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写；共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | os.environ.get、winreg.OpenKey、winreg.QueryValueEx、strip、server.split、winreg.CloseKey |
| 复杂度 / 风险 | 分支 6；跨度 24 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2365b1ea92"></a>

#### FUN-2365B1EA92

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_system_proxy` |
| 源码位置 | [src/data/proxy_env.py](../../../src/data/proxy_env.py) · `L34` |
| 签名 | `apply_system_proxy()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 应用系统代理配置；可能影响共享状态；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `read_system_proxy` → `os.environ.setdefault`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | read_system_proxy、os.environ.setdefault |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-ea7e4f88fe"></a>

### UNIT-EA7E4F88FE

**模块**：`src/data/run_archive.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EA7E4F88FE |
| 源码 | [src/data/run_archive.py](../../../src/data/run_archive.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/run_archive.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-023a37a1e9"></a>

### UNIT-023A37A1E9

**模块**：`src/data/run_archive_compat.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-023A37A1E9 |
| 源码 | [src/data/run_archive_compat.py](../../../src/data/run_archive_compat.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/run_archive_compat.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-7bfc490988"></a>

### UNIT-7BFC490988

**模块**：`src/data/run_archive_index.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7BFC490988 |
| 源码 | [src/data/run_archive_index.py](../../../src/data/run_archive_index.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/run_archive_index.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-dad8bc5b0f"></a>

### UNIT-DAD8BC5B0F

**模块**：`src/data/run_archive_prune.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAD8BC5B0F |
| 源码 | [src/data/run_archive_prune.py](../../../src/data/run_archive_prune.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/run_archive_prune.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-767bf49f25"></a>

### UNIT-767BF49F25

**模块**：`src/data/run_archive_schema.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-767BF49F25 |
| 源码 | [src/data/run_archive_schema.py](../../../src/data/run_archive_schema.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/run_archive_schema.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-c3952c43cb"></a>

### UNIT-C3952C43CB

**模块**：`src/data/sources/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C3952C43CB |
| 源码 | [src/data/sources/__init__.py](../../../src/data/sources/__init__.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-c590fce576"></a>

### UNIT-C590FCE576

**模块**：`src/data/sources/_http.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C590FCE576 |
| 源码 | [src/data/sources/_http.py](../../../src/data/sources/_http.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/_http.py` 的职责，通过 `post_json`、`get_json`、`get_text` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [post_json](#fun-fc8cbed92a) | 生成`post_json`结果；可能影响外部接口；返回 `Any` 类型结果。 | 外部接口 I/O | [tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py) |
| [get_text](#fun-299c0d3a32) | 获取文本；可能影响外部接口；返回 `str` 类型结果。 | 外部接口 I/O | [tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py) |

#### 函数导航

[post_json](#fun-fc8cbed92a) · [get_json](#fun-6afe1ec0a4) · [get_text](#fun-299c0d3a32)

<a id="fun-fc8cbed92a"></a>

#### FUN-FC8CBED92A

| 设计项 | 说明 |
|---|---|
| 函数 | `post_json` |
| 源码位置 | [src/data/sources/_http.py](../../../src/data/sources/_http.py) · `L29` |
| 签名 | `post_json(url: str, *, body: dict[str, Any] \| list[Any], params: dict[str, Any] \| None=None, headers: dict[str, str] \| None=None, timeout: int \| None=None)` |
| 参数 | `url`（str）：外部资源地址<br>`body`（dict[str, Any] \| list[Any]）：由 `body` 表示的输入集合<br>`params`（dict[str, Any] \| None）：由 `params` 表示的键值映射；默认值 `None`<br>`headers`（dict[str, str] \| None）：表头或 HTTP 头字段；默认值 `None`<br>`timeout`（int \| None）：超时秒数；默认值 `None` |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`post_json`结果；可能影响外部接口；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `merged.setdefault` → `range` → `requests.post` → `resp.raise_for_status` → `resp.json` → `log.warning` → `time.sleep` → `RuntimeError`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `Any` 类型结果；可观察变化限于外部接口 |
| 显式异常 | RuntimeError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | merged.setdefault、range、requests.post、resp.raise_for_status、resp.json、log.warning、time.sleep、RuntimeError |
| 复杂度 / 风险 | 分支 4；跨度 32 行；高 |
| 测试 / 验证 | [tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py) · 直接动态测试 |

<a id="fun-6afe1ec0a4"></a>

#### FUN-6AFE1EC0A4

| 设计项 | 说明 |
|---|---|
| 函数 | `get_json` |
| 源码位置 | [src/data/sources/_http.py](../../../src/data/sources/_http.py) · `L63` |
| 签名 | `get_json(url: str, *, params: dict[str, Any] \| None=None, headers: dict[str, str] \| None=None, cookies: dict[str, str] \| None=None)` |
| 参数 | `url`（str）：外部资源地址<br>`params`（dict[str, Any] \| None）：由 `params` 表示的键值映射；默认值 `None`<br>`headers`（dict[str, str] \| None）：表头或 HTTP 头字段；默认值 `None`<br>`cookies`（dict[str, str] \| None）：由 `cookies` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 获取JSON 数据；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `json.loads` → `get_text`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | json.loads、get_text |
| 复杂度 / 风险 | 分支 0；跨度 8 行；中 |
| 测试 / 验证 | [tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py) · 直接动态测试 |

<a id="fun-299c0d3a32"></a>

#### FUN-299C0D3A32

| 设计项 | 说明 |
|---|---|
| 函数 | `get_text` |
| 源码位置 | [src/data/sources/_http.py](../../../src/data/sources/_http.py) · `L73` |
| 签名 | `get_text(url: str, *, params: dict[str, Any] \| None=None, headers: dict[str, str] \| None=None, cookies: dict[str, str] \| None=None)` |
| 参数 | `url`（str）：外部资源地址<br>`params`（dict[str, Any] \| None）：由 `params` 表示的键值映射；默认值 `None`<br>`headers`（dict[str, str] \| None）：表头或 HTTP 头字段；默认值 `None`<br>`cookies`（dict[str, str] \| None）：由 `cookies` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 获取文本；可能影响外部接口；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `range` → `requests.get` → `resp.raise_for_status` → `log.warning` → `time.sleep` → `RuntimeError`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `str` 类型结果；可观察变化限于外部接口 |
| 显式异常 | RuntimeError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | range、requests.get、resp.raise_for_status、log.warning、time.sleep、RuntimeError |
| 复杂度 / 风险 | 分支 3；跨度 29 行；高 |
| 测试 / 验证 | [tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py) · 直接动态测试 |

<a id="unit-0df4638d5e"></a>

### UNIT-0DF4638D5E

**模块**：`src/data/sources/base.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0DF4638D5E |
| 源码 | [src/data/sources/base.py](../../../src/data/sources/base.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/base.py` 的职责，通过 `DataSource` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) |
| 验证状态 | selected |

#### 函数导航

[DataSource.fetch](#fun-600c64bcb0)

<a id="fun-600c64bcb0"></a>

#### FUN-600C64BCB0

| 设计项 | 说明 |
|---|---|
| 函数 | `DataSource.fetch` |
| 源码位置 | [src/data/sources/base.py](../../../src/data/sources/base.py) · `L14` |
| 签名 | `DataSource.fetch(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[EvidenceItem] \| ExternalFactors` 类型结果 |
| 职责 | 获取外部或市场数据；返回 `list[EvidenceItem] \| ExternalFactors` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem] \| ExternalFactors` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_archive_compat.py](../../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_pipeline_progress_headline.py](../../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="unit-1fa1bdf5ba"></a>

### UNIT-1FA1BDF5BA

**模块**：`src/data/sources/dxy.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1FA1BDF5BA |
| 源码 | [src/data/sources/dxy.py](../../../src/data/sources/dxy.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/dxy.py` 的职责，通过 `fetch_dxy_impact` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [fetch_dxy_impact](#fun-85282ddc4d) | 获取`dxy_impact`；可能影响外部接口；返回 `tuple[str, dict]` 类型结果。 | 外部接口 I/O | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |

#### 函数导航

[fetch_dxy_impact](#fun-85282ddc4d)

<a id="fun-85282ddc4d"></a>

#### FUN-85282DDC4D

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_dxy_impact` |
| 源码位置 | [src/data/sources/dxy.py](../../../src/data/sources/dxy.py) · `L14` |
| 签名 | `fetch_dxy_impact()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[str, dict]` 类型结果 |
| 职责 | 获取`dxy_impact`；可能影响外部接口；返回 `tuple[str, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_symbol_daily` → `ValueError` → `round` → `log.info` → `log.warning` → `_PLACEHOLDER.replace`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[str, dict]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | ValueError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_symbol_daily、len、ValueError、float、round、log.info、log.warning、_PLACEHOLDER.replace、str |
| 复杂度 / 风险 | 分支 5；跨度 40 行；高 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-ec9b21793d"></a>

### UNIT-EC9B21793D

**模块**：`src/data/sources/fundamentals.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EC9B21793D |
| 源码 | [src/data/sources/fundamentals.py](../../../src/data/sources/fundamentals.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/fundamentals.py` 的职责，通过 `FundamentalsDataSource`、`macro_quotes_to_evidence`、`external_macro_evidence` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 4 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [FundamentalsDataSource.fetch_external](#fun-85ea252365) | 获取外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| [FundamentalsDataSource.fetch_evidence](#fun-6a23a66cff) | 获取证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 | 外部接口 I/O | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| [external_macro_evidence](#fun-683a4407dd) | 构建`external_macro_evidence`；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[FundamentalsDataSource.fetch_external](#fun-85ea252365) · [FundamentalsDataSource.fetch_evidence](#fun-6a23a66cff) · [macro_quotes_to_evidence](#fun-ad52255426) · [external_macro_evidence](#fun-683a4407dd)

<a id="fun-85ea252365"></a>

#### FUN-85EA252365

| 设计项 | 说明 |
|---|---|
| 函数 | `FundamentalsDataSource.fetch_external` |
| 源码位置 | [src/data/sources/fundamentals.py](../../../src/data/sources/fundamentals.py) · `L12` |
| 签名 | `FundamentalsDataSource.fetch_external(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_macro_quotes` → `next` → `any` → `sources.append` → `ExternalFactors`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_macro_quotes、next、any、sources.append、ExternalFactors |
| 复杂度 / 风险 | 分支 3；跨度 12 行；高 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-6a23a66cff"></a>

#### FUN-6A23A66CFF

| 设计项 | 说明 |
|---|---|
| 函数 | `FundamentalsDataSource.fetch_evidence` |
| 源码位置 | [src/data/sources/fundamentals.py](../../../src/data/sources/fundamentals.py) · `L25` |
| 签名 | `FundamentalsDataSource.fetch_evidence(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 获取证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `macro_quotes_to_evidence` → `fetch_macro_quotes`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | macro_quotes_to_evidence、fetch_macro_quotes |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-ad52255426"></a>

#### FUN-AD52255426

| 设计项 | 说明 |
|---|---|
| 函数 | `macro_quotes_to_evidence` |
| 源码位置 | [src/data/sources/fundamentals.py](../../../src/data/sources/fundamentals.py) · `L29` |
| 签名 | `macro_quotes_to_evidence(quotes: list[MacroQuote])` |
| 参数 | `quotes`（list[MacroQuote]）：由 `quotes` 表示的输入集合 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`macro_quotes_to_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `items.append` → `EvidenceItem` → `q.to_dict`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | items.append、EvidenceItem、q.to_dict |
| 复杂度 / 风险 | 分支 3；跨度 23 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-683a4407dd"></a>

#### FUN-683A4407DD

| 设计项 | 说明 |
|---|---|
| 函数 | `external_macro_evidence` |
| 源码位置 | [src/data/sources/fundamentals.py](../../../src/data/sources/fundamentals.py) · `L54` |
| 签名 | `external_macro_evidence(ext: ExternalFactors)` |
| 参数 | `ext`（ExternalFactors）：由调用方提供的 `ext` 输入对象 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`external_macro_evidence`；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `macro_quotes_to_evidence` → `EvidenceItem` → `fetch_evidence` → `FundamentalsDataSource`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | macro_quotes_to_evidence、EvidenceItem、fetch_evidence、FundamentalsDataSource |
| 复杂度 / 风险 | 分支 2；跨度 13 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-4d4d8a02c7"></a>

### UNIT-4D4D8A02C7

**模块**：`src/data/sources/gold_relevance.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4D4D8A02C7 |
| 源码 | [src/data/sources/gold_relevance.py](../../../src/data/sources/gold_relevance.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/gold_relevance.py` 的职责，通过 `matches_gold_headline`、`is_gold_macro_event` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[matches_gold_headline](#fun-64da59ba88) · [is_gold_macro_event](#fun-30d61ef6f5)

<a id="fun-64da59ba88"></a>

#### FUN-64DA59BA88

| 设计项 | 说明 |
|---|---|
| 函数 | `matches_gold_headline` |
| 源码位置 | [src/data/sources/gold_relevance.py](../../../src/data/sources/gold_relevance.py) · `L121` |
| 签名 | `matches_gold_headline(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`matches_gold_headline`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `text.lower` → `any`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | text.lower、any |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-30d61ef6f5"></a>

#### FUN-30D61EF6F5

| 设计项 | 说明 |
|---|---|
| 函数 | `is_gold_macro_event` |
| 源码位置 | [src/data/sources/gold_relevance.py](../../../src/data/sources/gold_relevance.py) · `L126` |
| 签名 | `is_gold_macro_event(event: str, region: str='', *, importance: float \| None=None)` |
| 参数 | `event`（str）：事件对象<br>`region`（str）：由 `region` 表示的文本或标识；默认值 `''`<br>`importance`（float \| None）：由调用方提供的 `importance` 输入对象；默认值 `None` |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`gold_macro_event`；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `text.lower` → `pat.search` → `any`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、text.lower、pat.search、any |
| 复杂度 / 风险 | 分支 4；跨度 12 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-7020937074"></a>

### UNIT-7020937074

**模块**：`src/data/sources/jin10_feed.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7020937074 |
| 源码 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/jin10_feed.py` 的职责，通过 `Jin10NewsBundle`、`fetch_jin10_flash`、`fetch_jin10_articles`、`fetch_jin10_calendar`、`fetch_jin10_risk_events`、`fetch_jin10_bundle`、`fetch_jin10_quote`、`fetch_jin10_kline` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 23 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py)、[tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [fetch_jin10_risk_events](#fun-051831ac48) | 获取`jin10_risk_events`；可能影响外部接口；返回 `tuple[str, str \| None]` 类型结果。 | 外部接口 I/O | — |
| [fetch_jin10_bundle](#fun-bb6ef855aa) | 获取`jin10_bundle`；可能影响外部接口；返回 `Jin10NewsBundle` 类型结果。 | 外部接口 I/O | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |

#### 函数导航

[Jin10NewsBundle.headline_items](#fun-ad84260cd0) · [Jin10NewsBundle.headlines](#fun-0424648ecf) · [Jin10NewsBundle.is_live](#fun-f87ac8a103) · [_cached](#fun-e4d9bf91ca) · [_iter_rows](#fun-54e278ddf4) · [_is_relevant](#fun-71917bcd45) · [_parse_flash_item](#fun-81d80410a1) · [_parse_article_item](#fun-99163599fb) · [_parse_calendar_row](#fun-6ac6fd360c) · [_collect_items](#fun-4ce9f1e780) · [fetch_jin10_flash](#fun-e38a05cb72) · [fetch_jin10_flash._pull](#fun-e26f91daa9) · [fetch_jin10_articles](#fun-fa951f8508) · [fetch_jin10_articles._pull](#fun-82911d6a6c) · [fetch_jin10_calendar](#fun-8780d21897) · [fetch_jin10_calendar._pull](#fun-bd5c7672d7) · [fetch_jin10_risk_events](#fun-051831ac48) · [fetch_jin10_bundle](#fun-bb6ef855aa) · [fetch_jin10_quote](#fun-b4ef16ee9f) · [fetch_jin10_quote._pull](#fun-67ef031b31) · [_normalize_kline_bars](#fun-fbced9bbe7) · [fetch_jin10_kline](#fun-759eaf2c78) · [fetch_jin10_kline._pull](#fun-c4acab9575)

<a id="fun-ad84260cd0"></a>

#### FUN-AD84260CD0

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10NewsBundle.headline_items` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L47` |
| 签名 | `Jin10NewsBundle.headline_items(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[HeadlineItem]` 类型结果 |
| 职责 | 构建`headline_items`；返回 `list[HeadlineItem]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[HeadlineItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_fact_registry.py](../../../tests/unit/test_fact_registry.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) · 直接动态测试 |

<a id="fun-0424648ecf"></a>

#### FUN-0424648ECF

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10NewsBundle.headlines` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L51` |
| 签名 | `Jin10NewsBundle.headlines(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[str]` 类型结果 |
| 职责 | 构建`headlines`；返回 `list[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.text.strip` → `seen.add` → `merged.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、item.text.strip、seen.add、merged.append、len |
| 复杂度 / 风险 | 分支 3；跨度 12 行；中 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-f87ac8a103"></a>

#### FUN-F87AC8A103

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10NewsBundle.is_live` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L65` |
| 签名 | `Jin10NewsBundle.is_live(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`live`；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e4d9bf91ca"></a>

#### FUN-E4D9BF91CA

| 设计项 | 说明 |
|---|---|
| 函数 | `_cached` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L69` |
| 签名 | `_cached(key: str, ttl: int, fn: Callable[[], Any])` |
| 参数 | `key`（str）：索引键<br>`ttl`（int）：由 `ttl` 表示的数值参数<br>`fn`（Callable[[], Any]）：调用方提供的回调函数 |
| 返回 | 返回 `tuple[Any, str \| None]` 类型结果 |
| 职责 | 构建`cached`；可能影响共享状态；返回 `tuple[Any, str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_CACHE.get` → `time.time` → `fn` → `log.warning`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[Any, str \| None]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _CACHE.get、time.time、fn、log.warning、str |
| 复杂度 / 风险 | 分支 4；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-54e278ddf4"></a>

#### FUN-54E278DDF4

| 设计项 | 说明 |
|---|---|
| 函数 | `_iter_rows` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L84` |
| 签名 | `_iter_rows(data: Any)` |
| 参数 | `data`（Any）：输入数据 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`iter_rows`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `data.get` → `_iter_rows`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、data.get、_iter_rows |
| 复杂度 / 风险 | 分支 6；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-71917bcd45"></a>

#### FUN-71917BCD45

| 设计项 | 说明 |
|---|---|
| 函数 | `_is_relevant` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L100` |
| 签名 | `_is_relevant(text: str, keyword: str)` |
| 参数 | `text`（str）：输入文本<br>`keyword`（str）：由 `keyword` 表示的文本或标识 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`relevant`；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `matches_gold_headline`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | matches_gold_headline、bool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-81d80410a1"></a>

#### FUN-81D80410A1

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_flash_item` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L104` |
| 签名 | `_parse_flash_item(row: dict[str, Any])` |
| 参数 | `row`（dict[str, Any]）：当前记录行 |
| 返回 | 返回 `HeadlineItem` 类型结果 |
| 职责 | 解析`flash_item`；返回 `HeadlineItem` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `row.get` → `HeadlineItem`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `HeadlineItem` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、row.get、HeadlineItem |
| 复杂度 / 风险 | 分支 1；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-99163599fb"></a>

#### FUN-99163599FB

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_article_item` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L118` |
| 签名 | `_parse_article_item(row: dict[str, Any])` |
| 参数 | `row`（dict[str, Any]）：当前记录行 |
| 返回 | 返回 `HeadlineItem` 类型结果 |
| 职责 | 解析`article_item`；返回 `HeadlineItem` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `row.get` → `HeadlineItem`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `HeadlineItem` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、row.get、HeadlineItem |
| 复杂度 / 风险 | 分支 2；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6ac6fd360c"></a>

#### FUN-6AC6FD360C

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_calendar_row` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L136` |
| 签名 | `_parse_calendar_row(row: dict[str, Any])` |
| 参数 | `row`（dict[str, Any]）：当前记录行 |
| 返回 | 返回 `CalendarEvent \| None` 类型结果 |
| 职责 | 解析`calendar_row`；返回 `CalendarEvent \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `row.get` → `is_gold_macro_event` → `CalendarEvent`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `CalendarEvent \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、str、row.get、is_gold_macro_event、CalendarEvent |
| 复杂度 / 风险 | 分支 4；跨度 24 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4ce9f1e780"></a>

#### FUN-4CE9F1E780

| 设计项 | 说明 |
|---|---|
| 函数 | `_collect_items` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L162` |
| 签名 | `_collect_items(rows: list[dict[str, Any]], *, parse_fn: Callable[[dict[str, Any]], HeadlineItem], keyword: str, limit: int, fallback: bool)` |
| 参数 | `rows`（list[dict[str, Any]]）：记录行集合<br>`parse_fn`（Callable[[dict[str, Any]], HeadlineItem]）：调用方提供的回调函数<br>`keyword`（str）：由 `keyword` 表示的文本或标识<br>`limit`（int）：返回或处理数量上限<br>`fallback`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `list[HeadlineItem]` 类型结果 |
| 职责 | 收集`items`；返回 `list[HeadlineItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `parse_fn` → `_is_relevant` → `seen.add` → `items.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[HeadlineItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | set、parse_fn、_is_relevant、seen.add、items.append、len |
| 复杂度 / 风险 | 分支 7；跨度 25 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e38a05cb72"></a>

#### FUN-E38A05CB72

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_flash` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L189` |
| 签名 | `fetch_jin10_flash()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[list[HeadlineItem], str \| None]` 类型结果 |
| 职责 | 获取`jin10_flash`；可能影响共享状态；返回 `tuple[list[HeadlineItem], str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `JIN10_KEYWORD.strip` → `jin10_call_tool` → `_cached` → `_collect_items` → `_iter_rows`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[HeadlineItem], str \| None]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | JIN10_KEYWORD.strip、jin10_call_tool、_cached、_collect_items、_iter_rows |
| 复杂度 / 风险 | 分支 3；跨度 22 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-e26f91daa9"></a>

#### FUN-E26F91DAA9

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_flash._pull` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L196` |
| 签名 | `fetch_jin10_flash._pull()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`pull`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `jin10_call_tool`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | jin10_call_tool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fa951f8508"></a>

#### FUN-FA951F8508

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_articles` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L213` |
| 签名 | `fetch_jin10_articles()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[list[HeadlineItem], str \| None]` 类型结果 |
| 职责 | 获取`jin10_articles`；可能影响共享状态；返回 `tuple[list[HeadlineItem], str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `JIN10_KEYWORD.strip` → `jin10_call_tool` → `_cached` → `_collect_items` → `_iter_rows`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[HeadlineItem], str \| None]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | JIN10_KEYWORD.strip、jin10_call_tool、_cached、_collect_items、_iter_rows |
| 复杂度 / 风险 | 分支 4；跨度 24 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-82911d6a6c"></a>

#### FUN-82911D6A6C

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_articles._pull` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L220` |
| 签名 | `fetch_jin10_articles._pull()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`pull`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `jin10_call_tool`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | jin10_call_tool |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8780d21897"></a>

#### FUN-8780D21897

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_calendar` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L239` |
| 签名 | `fetch_jin10_calendar()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[list[CalendarEvent], str \| None]` 类型结果 |
| 职责 | 获取`jin10_calendar`；可能影响共享状态；返回 `tuple[list[CalendarEvent], str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `jin10_call_tool` → `_cached` → `_iter_rows` → `_parse_calendar_row` → `ev.display` → `seen.add` → `events.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[CalendarEvent], str \| None]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | jin10_call_tool、_cached、set、_iter_rows、_parse_calendar_row、ev.display、seen.add、events.append、len |
| 复杂度 / 风险 | 分支 7；跨度 28 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-bd5c7672d7"></a>

#### FUN-BD5C7672D7

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_calendar._pull` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L243` |
| 签名 | `fetch_jin10_calendar._pull()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`pull`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `jin10_call_tool`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | jin10_call_tool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-051831ac48"></a>

#### FUN-051831AC48

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_risk_events` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L269` |
| 签名 | `fetch_jin10_risk_events()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[str, str \| None]` 类型结果 |
| 职责 | 获取`jin10_risk_events`；可能影响外部接口；返回 `tuple[str, str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_jin10_calendar` → `filter_upcoming_calendar_events` → `calendar_to_risk_text`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[str, str \| None]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_jin10_calendar、filter_upcoming_calendar_events、calendar_to_risk_text |
| 复杂度 / 风险 | 分支 2；跨度 9 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-bb6ef855aa"></a>

#### FUN-BB6EF855AA

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_bundle` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L280` |
| 签名 | `fetch_jin10_bundle()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Jin10NewsBundle` 类型结果 |
| 职责 | 获取`jin10_bundle`；可能影响外部接口；返回 `Jin10NewsBundle` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `Jin10NewsBundle` → `bundle.errors.append` → `fetch_jin10_flash` → `bundle.sources.append` → `fetch_jin10_articles` → `fetch_jin10_calendar` → `filter_upcoming_calendar_events` → `calendar_to_risk_text`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `Jin10NewsBundle` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | Jin10NewsBundle、bundle.errors.append、fetch_jin10_flash、bundle.sources.append、fetch_jin10_articles、fetch_jin10_calendar、filter_upcoming_calendar_events、calendar_to_risk_text |
| 复杂度 / 风险 | 分支 7；跨度 36 行；高 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-b4ef16ee9f"></a>

#### FUN-B4EF16EE9F

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_quote` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L321` |
| 签名 | `fetch_jin10_quote(code: str \| None=None)` |
| 参数 | `code`（str \| None）：由调用方提供的 `code` 输入对象；默认值 `None` |
| 返回 | 返回 `tuple[dict[str, Any] \| None, str \| None]` 类型结果 |
| 职责 | 获取`jin10_quote`；可能影响共享状态；返回 `tuple[dict[str, Any] \| None, str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `jin10_call_tool` → `_cached` → `isinstance` → `data.get`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[dict[str, Any] \| None, str \| None]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、jin10_call_tool、_cached、isinstance、data.get |
| 复杂度 / 风险 | 分支 4；跨度 20 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-67ef031b31"></a>

#### FUN-67EF031B31

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_quote._pull` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L329` |
| 签名 | `fetch_jin10_quote._pull()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`pull`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `jin10_call_tool`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | jin10_call_tool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fbced9bbe7"></a>

#### FUN-FBCED9BBE7

| 设计项 | 说明 |
|---|---|
| 函数 | `_normalize_kline_bars` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L343` |
| 签名 | `_normalize_kline_bars(data: Any)` |
| 参数 | `data`（Any）：输入数据 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 标准化`kline_bars`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_iter_rows` → `row.get` → `bars.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _iter_rows、row.get、float、bars.append |
| 复杂度 / 风险 | 分支 3；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-759eaf2c78"></a>

#### FUN-759EAF2C78

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_kline` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L367` |
| 签名 | `fetch_jin10_kline(code: str \| None=None, *, period: str \| None=None, count: int \| None=None)` |
| 参数 | `code`（str \| None）：由调用方提供的 `code` 输入对象；默认值 `None`<br>`period`（str \| None）：计算周期长度；默认值 `None`<br>`count`（int \| None）：由调用方提供的 `count` 输入对象；默认值 `None` |
| 返回 | 返回 `tuple[list[dict[str, Any]], str \| None]` 类型结果 |
| 职责 | 获取`jin10_kline`；可能影响共享状态；返回 `tuple[list[dict[str, Any]], str \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `jin10_call_tool` → `_cached` → `isinstance` → `data.get` → `_normalize_kline_bars`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict[str, Any]], str \| None]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、jin10_call_tool、_cached、isinstance、data.get、_normalize_kline_bars |
| 复杂度 / 风险 | 分支 6；跨度 34 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py) · 直接动态测试 |

<a id="fun-c4acab9575"></a>

#### FUN-C4ACAB9575

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_jin10_kline._pull` |
| 源码位置 | [src/data/sources/jin10_feed.py](../../../src/data/sources/jin10_feed.py) · `L386` |
| 签名 | `fetch_jin10_kline._pull()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`pull`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `jin10_call_tool`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | jin10_call_tool |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-927bb1749d"></a>

### UNIT-927BB1749D

**模块**：`src/data/sources/jin10_mcp_client.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-927BB1749D |
| 源码 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Jin10 (金十数据) official MCP client — JSON-RPC over SSE。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 10 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [Jin10McpClient._post](#fun-48e026a8bb) | 生成`post`结果；可能影响外部接口；返回 `Any` 类型结果。 | 外部接口 I/O | — |
| [get_jin10_client](#fun-6b5241464f) | 获取`jin10_client`；可能影响外部接口；返回 `Jin10McpClient` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[_parse_sse](#fun-a697c9be9d) · [_pick_data](#fun-78f0060e7a) · [Jin10McpClient.__init__](#fun-84897c5cce) · [Jin10McpClient._headers](#fun-45a198880a) · [Jin10McpClient._next_id](#fun-9cb066a5e9) · [Jin10McpClient._post](#fun-48e026a8bb) · [Jin10McpClient.connect](#fun-72bb9b66ce) · [Jin10McpClient.call_tool](#fun-f9d2c12d6e) · [get_jin10_client](#fun-6b5241464f) · [jin10_call_tool](#fun-57be12ae7a)

<a id="fun-a697c9be9d"></a>

#### FUN-A697C9BE9D

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_sse` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L25` |
| 签名 | `_parse_sse(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 解析`sse`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `text.find` → `RuntimeError` → `strip` → `json.loads` → `splitlines` → `line.startswith` → `buf.append` → `join`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | RuntimeError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | text.find、RuntimeError、strip、len、json.loads、splitlines、line.startswith、buf.append、join |
| 复杂度 / 风险 | 分支 5；跨度 26 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-78f0060e7a"></a>

#### FUN-78F0060E7A

| 设计项 | 说明 |
|---|---|
| 函数 | `_pick_data` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L53` |
| 签名 | `_pick_data(result: dict[str, Any] \| None)` |
| 参数 | `result`（dict[str, Any] \| None）：处理结果 |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`pick_data`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `result.get` → `isinstance` → `block.get` → `json.loads`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | result.get、isinstance、block.get、json.loads |
| 复杂度 / 风险 | 分支 7；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-84897c5cce"></a>

#### FUN-84897C5CCE

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10McpClient.__init__` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L72` |
| 签名 | `Jin10McpClient.__init__(self, *, token: str, url: str=JIN10_MCP_URL, protocol: str=JIN10_MCP_PROTOCOL)` |
| 参数 | `token`（str）：标记或认证令牌<br>`url`（str）：外部资源地址；默认值 `JIN10_MCP_URL`<br>`protocol`（str）：由 `protocol` 表示的文本或标识；默认值 `JIN10_MCP_PROTOCOL` |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 6 行；低 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-45a198880a"></a>

#### FUN-45A198880A

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10McpClient._headers` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L79` |
| 签名 | `Jin10McpClient._headers(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`headers`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 8 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-9cb066a5e9"></a>

#### FUN-9CB066A5E9

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10McpClient._next_id` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L88` |
| 签名 | `Jin10McpClient._next_id(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`next_id`；返回 `int` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-48e026a8bb"></a>

#### FUN-48E026A8BB

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10McpClient._post` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L92` |
| 签名 | `Jin10McpClient._post(self, body: dict[str, Any], *, expect_response: bool=True)` |
| 参数 | `body`（dict[str, Any]）：由 `body` 表示的键值映射<br>`expect_response`（bool）：控制对应行为是否启用的布尔值；默认值 `True` |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`post`结果；可能影响外部接口；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `range` → `requests.post` → `self._headers` → `time.sleep` → `RuntimeError` → `resp.headers.get` → `resp.content.decode` → `_parse_sse`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `Any` 类型结果；可观察变化限于外部接口 |
| 显式异常 | RuntimeError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | range、requests.post、self._headers、time.sleep、RuntimeError、resp.headers.get、resp.content.decode、_parse_sse、next、e.get、rpc.get、err.get |
| 复杂度 / 风险 | 分支 9；跨度 43 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-72bb9b66ce"></a>

#### FUN-72BB9B66CE

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10McpClient.connect` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L136` |
| 签名 | `Jin10McpClient.connect(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`connect`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `self._post` → `self._next_id`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._post、self._next_id |
| 复杂度 / 风险 | 分支 0；跨度 17 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py) · 直接动态测试 |

<a id="fun-f9d2c12d6e"></a>

#### FUN-F9D2C12D6E

| 设计项 | 说明 |
|---|---|
| 函数 | `Jin10McpClient.call_tool` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L154` |
| 签名 | `Jin10McpClient.call_tool(self, name: str, arguments: dict[str, Any] \| None=None)` |
| 参数 | `name`（str）：对象名称<br>`arguments`（dict[str, Any] \| None）：由 `arguments` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`call_tool`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self._post` → `self._next_id` → `isinstance` → `result.get` → `RuntimeError` → `_pick_data`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | RuntimeError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._post、self._next_id、isinstance、result.get、RuntimeError、_pick_data |
| 复杂度 / 风险 | 分支 1；跨度 12 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-6b5241464f"></a>

#### FUN-6B5241464F

| 设计项 | 说明 |
|---|---|
| 函数 | `get_jin10_client` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L168` |
| 签名 | `get_jin10_client()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Jin10McpClient` 类型结果 |
| 职责 | 获取`jin10_client`；可能影响外部接口；返回 `Jin10McpClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `RuntimeError` → `time.time` → `_SESSION.get` → `Jin10McpClient` → `client.connect`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `Jin10McpClient` 类型结果；可观察变化限于外部接口 |
| 显式异常 | RuntimeError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | RuntimeError、time.time、_SESSION.get、float、Jin10McpClient、client.connect |
| 复杂度 / 风险 | 分支 2；跨度 12 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-57be12ae7a"></a>

#### FUN-57BE12AE7A

| 设计项 | 说明 |
|---|---|
| 函数 | `jin10_call_tool` |
| 源码位置 | [src/data/sources/jin10_mcp_client.py](../../../src/data/sources/jin10_mcp_client.py) · `L182` |
| 签名 | `jin10_call_tool(name: str, arguments: dict[str, Any] \| None=None)` |
| 参数 | `name`（str）：对象名称<br>`arguments`（dict[str, Any] \| None）：由 `arguments` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `Any` 类型结果 |
| 职责 | 生成`jin10_call_tool`结果；返回 `Any` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `call_tool` → `get_jin10_client`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Any` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | call_tool、get_jin10_client |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-fe5c27c113"></a>

### UNIT-FE5C27C113

**模块**：`src/data/sources/macro.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FE5C27C113 |
| 源码 | [src/data/sources/macro.py](../../../src/data/sources/macro.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/macro.py` 的职责，通过 `fetch_dxy_quote`、`fetch_us10y_quote`、`fetch_macro_quotes` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 5 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [fetch_dxy_quote](#fun-708b026267) | 获取`dxy_quote`；可能影响外部接口；返回 `MacroQuote \| None` 类型结果。 | 外部接口 I/O | — |
| [fetch_us10y_quote](#fun-7bbbaadf8c) | 获取`us10y_quote`；可能影响外部接口；返回 `MacroQuote \| None` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[_daily_change](#fun-9a59422023) · [_gold_bias_from_change](#fun-e016877e87) · [fetch_dxy_quote](#fun-708b026267) · [fetch_us10y_quote](#fun-7bbbaadf8c) · [fetch_macro_quotes](#fun-777bc4df7e)

<a id="fun-9a59422023"></a>

#### FUN-9A59422023

| 设计项 | 说明 |
|---|---|
| 函数 | `_daily_change` |
| 源码位置 | [src/data/sources/macro.py](../../../src/data/sources/macro.py) · `L17` |
| 签名 | `_daily_change(df)` |
| 参数 | `df`（实现约定类型）：输入数据表 |
| 返回 | 返回 `tuple[float, float, float]` 类型结果 |
| 职责 | 构建`daily_change`；返回 `tuple[float, float, float]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e016877e87"></a>

#### FUN-E016877E87

| 设计项 | 说明 |
|---|---|
| 函数 | `_gold_bias_from_change` |
| 源码位置 | [src/data/sources/macro.py](../../../src/data/sources/macro.py) · `L24` |
| 签名 | `_gold_bias_from_change(change_pct: float, *, invert: bool)` |
| 参数 | `change_pct`（float）：百分比数值<br>`invert`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `tuple[str, str]` 类型结果 |
| 职责 | 根据`change`构建`gold_bias`；返回 `tuple[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 5；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-708b026267"></a>

#### FUN-708B026267

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_dxy_quote` |
| 源码位置 | [src/data/sources/macro.py](../../../src/data/sources/macro.py) · `L40` |
| 签名 | `fetch_dxy_quote()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `MacroQuote \| None` 类型结果 |
| 职责 | 获取`dxy_quote`；可能影响外部接口；返回 `MacroQuote \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_symbol_daily` → `_daily_change` → `_gold_bias_from_change` → `MacroQuote` → `round` → `log.warning`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `MacroQuote \| None` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_symbol_daily、len、_daily_change、_gold_bias_from_change、MacroQuote、round、log.warning |
| 复杂度 / 风险 | 分支 4；跨度 25 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-7bbbaadf8c"></a>

#### FUN-7BBBAADF8C

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_us10y_quote` |
| 源码位置 | [src/data/sources/macro.py](../../../src/data/sources/macro.py) · `L67` |
| 签名 | `fetch_us10y_quote()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `MacroQuote \| None` 类型结果 |
| 职责 | 获取`us10y_quote`；可能影响外部接口；返回 `MacroQuote \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_symbol_daily` → `_daily_change` → `_gold_bias_from_change` → `MacroQuote` → `round` → `log.warning`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `MacroQuote \| None` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_symbol_daily、len、_daily_change、_gold_bias_from_change、MacroQuote、round、log.warning |
| 复杂度 / 风险 | 分支 4；跨度 25 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-777bc4df7e"></a>

#### FUN-777BC4DF7E

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_macro_quotes` |
| 源码位置 | [src/data/sources/macro.py](../../../src/data/sources/macro.py) · `L94` |
| 签名 | `fetch_macro_quotes()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[MacroQuote]` 类型结果 |
| 职责 | 获取`macro_quotes`；返回 `list[MacroQuote]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fn` → `quotes.append`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[MacroQuote]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fn、quotes.append |
| 复杂度 / 风险 | 分支 2；跨度 7 行；中 |
| 测试 / 验证 | [tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-603339624c"></a>

### UNIT-603339624C

**模块**：`src/data/sources/market.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-603339624C |
| 源码 | [src/data/sources/market.py](../../../src/data/sources/market.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/market.py` 的职责，通过 `MarketDataSource` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[MarketDataSource.__init__](#fun-55497ef40f) · [MarketDataSource.fetch_evidence](#fun-eeff26c071)

<a id="fun-55497ef40f"></a>

#### FUN-55497EF40F

| 设计项 | 说明 |
|---|---|
| 函数 | `MarketDataSource.__init__` |
| 源码位置 | [src/data/sources/market.py](../../../src/data/sources/market.py) · `L16` |
| 签名 | `MarketDataSource.__init__(self, enriched: dict[str, pd.DataFrame])` |
| 参数 | `enriched`（dict[str, pd.DataFrame]）：已补充指标的行情数据 |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | [tests/unit/test_aspice_high_risk_contracts.py](../../../tests/unit/test_aspice_high_risk_contracts.py) · 直接动态测试 |

<a id="fun-eeff26c071"></a>

#### FUN-EEFF26C071

| 设计项 | 说明 |
|---|---|
| 函数 | `MarketDataSource.fetch_evidence` |
| 源码位置 | [src/data/sources/market.py](../../../src/data/sources/market.py) · `L19` |
| 签名 | `MarketDataSource.fetch_evidence(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 获取证据；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `daily_metrics` → `EvidenceItem` → `min` → `abs` → `pd.notna` → `items.append`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | daily_metrics、EvidenceItem、min、abs、pd.notna、float、items.append |
| 复杂度 / 风险 | 分支 3；跨度 37 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-58d6f95301"></a>

### UNIT-58D6F95301

**模块**：`src/data/sources/news.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-58D6F95301 |
| 源码 | [src/data/sources/news.py](../../../src/data/sources/news.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/news.py` 的职责，通过 `external_to_evidence`、`NewsDataSource` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 4 / 2 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [NewsDataSource.fetch_external](#fun-ad19eb744e) | 获取外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| [NewsDataSource.fetch_evidence](#fun-de57fb8e2a) | 获取证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 | 外部接口 I/O | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |

#### 函数导航

[_bundle_to_external](#fun-495f172db6) · [external_to_evidence](#fun-1e1d7d437a) · [NewsDataSource.fetch_external](#fun-ad19eb744e) · [NewsDataSource.fetch_evidence](#fun-de57fb8e2a)

<a id="fun-495f172db6"></a>

#### FUN-495F172DB6

| 设计项 | 说明 |
|---|---|
| 函数 | `_bundle_to_external` |
| 源码位置 | [src/data/sources/news.py](../../../src/data/sources/news.py) · `L12` |
| 签名 | `_bundle_to_external(bundle: Jin10NewsBundle)` |
| 参数 | `bundle`（Jin10NewsBundle）：由调用方提供的 `bundle` 输入对象 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 生成`bundle_to_external`结果；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ExternalFactors` → `headlines_to_strings` → `sync_external_legacy_fields`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ExternalFactors、headlines_to_strings、list、sync_external_legacy_fields |
| 复杂度 / 风险 | 分支 2；跨度 18 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1e1d7d437a"></a>

#### FUN-1E1D7D437A

| 设计项 | 说明 |
|---|---|
| 函数 | `external_to_evidence` |
| 源码位置 | [src/data/sources/news.py](../../../src/data/sources/news.py) · `L32` |
| 签名 | `external_to_evidence(ext: ExternalFactors, *, is_live: bool)` |
| 参数 | `ext`（ExternalFactors）：由调用方提供的 `ext` 输入对象<br>`is_live`（bool）：控制对应行为是否启用的布尔值 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 构建`external_to_evidence`；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `items.append` → `EvidenceItem` → `ev.display` → `min` → `any`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | items.append、EvidenceItem、ev.display、min、any |
| 复杂度 / 风险 | 分支 10；跨度 57 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ad19eb744e"></a>

#### FUN-AD19EB744E

| 设计项 | 说明 |
|---|---|
| 函数 | `NewsDataSource.fetch_external` |
| 源码位置 | [src/data/sources/news.py](../../../src/data/sources/news.py) · `L94` |
| 签名 | `NewsDataSource.fetch_external(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_bundle_to_external` → `fetch_jin10_bundle`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _bundle_to_external、fetch_jin10_bundle |
| 复杂度 / 风险 | 分支 0；跨度 2 行；高 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-de57fb8e2a"></a>

#### FUN-DE57FB8E2A

| 设计项 | 说明 |
|---|---|
| 函数 | `NewsDataSource.fetch_evidence` |
| 源码位置 | [src/data/sources/news.py](../../../src/data/sources/news.py) · `L97` |
| 签名 | `NewsDataSource.fetch_evidence(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 获取证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_jin10_bundle` → `_bundle_to_external` → `external_to_evidence`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_jin10_bundle、_bundle_to_external、external_to_evidence |
| 复杂度 / 风险 | 分支 0；跨度 4 行；高 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-ba8df8a829"></a>

### UNIT-BA8DF8A829

**模块**：`src/data/sources/social.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-BA8DF8A829 |
| 源码 | [src/data/sources/social.py](../../../src/data/sources/social.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/social.py` 的职责，通过 `SocialDataSource` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 3 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [SocialDataSource.fetch_external](#fun-95201e57fd) | 获取外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 | 外部接口 I/O | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| [SocialDataSource.fetch_external_summary](#fun-99eafc0124) | 获取`external_summary`；可能影响外部接口；返回 `tuple[str, dict]` 类型结果。 | 外部接口 I/O | — |
| [SocialDataSource.fetch_evidence](#fun-aad92ec141) | 获取证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 | 外部接口 I/O | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |

#### 函数导航

[SocialDataSource.fetch_external](#fun-95201e57fd) · [SocialDataSource.fetch_external_summary](#fun-99eafc0124) · [SocialDataSource.fetch_evidence](#fun-aad92ec141)

<a id="fun-95201e57fd"></a>

#### FUN-95201E57FD

| 设计项 | 说明 |
|---|---|
| 函数 | `SocialDataSource.fetch_external` |
| 源码位置 | [src/data/sources/social.py](../../../src/data/sources/social.py) · `L14` |
| 签名 | `SocialDataSource.fetch_external(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `ExternalFactors` 类型结果 |
| 职责 | 获取外部数据快照；可能影响外部接口；返回 `ExternalFactors` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_social_sentiment` → `refs.get` → `ExternalFactors`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `ExternalFactors` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_social_sentiment、refs.get、ExternalFactors |
| 复杂度 / 风险 | 分支 3；跨度 13 行；高 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-99eafc0124"></a>

#### FUN-99EAFC0124

| 设计项 | 说明 |
|---|---|
| 函数 | `SocialDataSource.fetch_external_summary` |
| 源码位置 | [src/data/sources/social.py](../../../src/data/sources/social.py) · `L28` |
| 签名 | `SocialDataSource.fetch_external_summary(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[str, dict]` 类型结果 |
| 职责 | 获取`external_summary`；可能影响外部接口；返回 `tuple[str, dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_social_sentiment`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `tuple[str, dict]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_social_sentiment |
| 复杂度 / 风险 | 分支 0；跨度 3 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-aad92ec141"></a>

#### FUN-AAD92EC141

| 设计项 | 说明 |
|---|---|
| 函数 | `SocialDataSource.fetch_evidence` |
| 源码位置 | [src/data/sources/social.py](../../../src/data/sources/social.py) · `L32` |
| 签名 | `SocialDataSource.fetch_evidence(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `list[EvidenceItem]` 类型结果 |
| 职责 | 获取证据；可能影响外部接口；返回 `list[EvidenceItem]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `fetch_social_sentiment` → `refs.get` → `EvidenceItem` → `post.get` → `items.append` → `min`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `list[EvidenceItem]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | fetch_social_sentiment、refs.get、EvidenceItem、post.get、str、int、items.append、min |
| 复杂度 / 风险 | 分支 2；跨度 32 行；高 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-b05f7affa4"></a>

### UNIT-B05F7AFFA4

**模块**：`src/data/sources/social_feed.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B05F7AFFA4 |
| 源码 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/sources/social_feed.py` 的职责，通过 `parse_tv_ideas`、`parse_tv_minds`、`fetch_social_sentiment` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 11 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [_collect_posts](#fun-b06d0a1526) | 收集`posts`；可能影响外部接口；返回 `list[dict]` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[_tv_headers](#fun-caabb05bc5) · [_score_text](#fun-a3dfefa187) · [_flatten_ast](#fun-90feed0db0) · [_idea_bias](#fun-73c783a893) · [_mind_bias](#fun-b89e173f01) · [parse_tv_ideas](#fun-f4bb9ead13) · [parse_tv_minds](#fun-b5dc3ce070) · [_fetch_tv_json](#fun-cf2373671f) · [_collect_posts](#fun-b06d0a1526) · [_summarize](#fun-c35dff8bfe) · [fetch_social_sentiment](#fun-e5da3d3910)

<a id="fun-caabb05bc5"></a>

#### FUN-CAABB05BC5

| 设计项 | 说明 |
|---|---|
| 函数 | `_tv_headers` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L29` |
| 签名 | `_tv_headers(symbol: str)` |
| 参数 | `symbol`（str）：交易品种代码 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`tv_headers`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 10 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-a3dfefa187"></a>

#### FUN-A3DFEFA187

| 设计项 | 说明 |
|---|---|
| 函数 | `_score_text` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L41` |
| 签名 | `_score_text(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 评分文本；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_BULL_WORDS.findall` → `_BEAR_WORDS.findall`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、_BULL_WORDS.findall、_BEAR_WORDS.findall |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-90feed0db0"></a>

#### FUN-90FEED0DB0

| 设计项 | 说明 |
|---|---|
| 函数 | `_flatten_ast` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L47` |
| 签名 | `_flatten_ast(node: Any)` |
| 参数 | `node`（Any）：AST 或结构节点 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`flatten_ast`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `strip` → `join` → `_flatten_ast` → `node.get` → `get` → `chunks.append`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、strip、join、_flatten_ast、node.get、str、get、chunks.append |
| 复杂度 / 风险 | 分支 6；跨度 15 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-73c783a893"></a>

#### FUN-73C783A893

| 设计项 | 说明 |
|---|---|
| 函数 | `_idea_bias` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L64` |
| 签名 | `_idea_bias(item: dict)` |
| 参数 | `item`（dict）：当前处理条目 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`idea_bias`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `item.get` → `isinstance` → `symbol.get` → `_DIRECTION_BIAS.get` → `_score_text`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | item.get、isinstance、symbol.get、_DIRECTION_BIAS.get、int、_score_text、str |
| 复杂度 / 风险 | 分支 3；跨度 11 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b89e173f01"></a>

#### FUN-B89E173F01

| 设计项 | 说明 |
|---|---|
| 函数 | `_mind_bias` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L77` |
| 签名 | `_mind_bias(item: dict)` |
| 参数 | `item`（dict）：当前处理条目 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`mind_bias`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_score_text` → `_flatten_ast` → `item.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _score_text、_flatten_ast、item.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-f4bb9ead13"></a>

#### FUN-F4BB9EAD13

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_tv_ideas` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L81` |
| 签名 | `parse_tv_ideas(payload: dict)` |
| 参数 | `payload`（dict）：结构化载荷 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 解析`tv_ideas`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `payload.get` → `ideas.get` → `isinstance` → `inner.get` → `strip` → `item.get` → `posts.append`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、payload.get、ideas.get、isinstance、inner.get、strip、str、item.get、posts.append、user.get、int、_idea_bias |
| 复杂度 / 风险 | 分支 7；跨度 26 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-b5dc3ce070"></a>

#### FUN-B5DC3CE070

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_tv_minds` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L109` |
| 签名 | `parse_tv_minds(payload: dict)` |
| 参数 | `payload`（dict）：结构化载荷 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 解析`tv_minds`；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get` → `payload.get` → `minds.get` → `isinstance` → `strip` → `_flatten_ast` → `item.get` → `posts.append`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get、payload.get、minds.get、isinstance、strip、_flatten_ast、item.get、posts.append、str、author.get、int、_mind_bias |
| 复杂度 / 风险 | 分支 6；跨度 25 行；中 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-cf2373671f"></a>

#### FUN-CF2373671F

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_tv_json` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L136` |
| 签名 | `_fetch_tv_json(path: str, symbol: str)` |
| 参数 | `path`（str）：文件或目录路径<br>`symbol`（str）：交易品种代码 |
| 返回 | 返回 `dict` 类型结果 |
| 职责 | 获取`tv_json`；返回 `dict` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_json` → `_tv_headers` → `isinstance`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_json、_tv_headers、isinstance |
| 复杂度 / 风险 | 分支 1；跨度 4 行；低 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-b06d0a1526"></a>

#### FUN-B06D0A1526

| 设计项 | 说明 |
|---|---|
| 函数 | `_collect_posts` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L142` |
| 签名 | `_collect_posts(symbol: str)` |
| 参数 | `symbol`（str）：交易品种代码 |
| 返回 | 返回 `list[dict]` 类型结果 |
| 职责 | 收集`posts`；可能影响外部接口；返回 `list[dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `posts.extend` → `parse_tv_ideas` → `_fetch_tv_json` → `parse_tv_minds`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `list[dict]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | posts.extend、parse_tv_ideas、_fetch_tv_json、parse_tv_minds |
| 复杂度 / 风险 | 分支 0；跨度 5 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c35dff8bfe"></a>

#### FUN-C35DFF8BFE

| 设计项 | 说明 |
|---|---|
| 函数 | `_summarize` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L149` |
| 签名 | `_summarize(posts: list[dict])` |
| 参数 | `posts`（list[dict]）：由 `posts` 表示的输入集合 |
| 返回 | 返回 `tuple[str, str, int, int]` 类型结果 |
| 职责 | 汇总当前对象；返回 `tuple[str, str, int, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `post.get` → `max`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, str, int, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | int、post.get、max、len |
| 复杂度 / 风险 | 分支 6；跨度 43 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e5da3d3910"></a>

#### FUN-E5DA3D3910

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_social_sentiment` |
| 源码位置 | [src/data/sources/social_feed.py](../../../src/data/sources/social_feed.py) · `L194` |
| 签名 | `fetch_social_sentiment()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[str, list[dict], dict]` 类型结果 |
| 职责 | 获取`social_sentiment`；返回 `tuple[str, list[dict], dict]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `upper` → `TV_SOCIAL_SYMBOL.strip` → `_collect_posts` → `_summarize` → `post.get` → `samples.append` → `sorted` → `p.get`；包含 10 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str, list[dict], dict]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | upper、TV_SOCIAL_SYMBOL.strip、_collect_posts、_summarize、post.get、len、samples.append、sorted、int、p.get、sum、log.warning、str |
| 复杂度 / 风险 | 分支 10；跨度 47 行；中 |
| 测试 / 验证 | [tests/integration/test_external_apis.py](../../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="unit-c1711535ca"></a>

### UNIT-C1711535CA

**模块**：`src/data/tradingview.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C1711535CA |
| 源码 | [src/data/tradingview.py](../../../src/data/tradingview.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/tradingview.py` 的职责，通过 `get_last_error`、`reset_client`、`compute_price_drift_1d`、`fetch_symbol_daily`、`fetch_multi_timeframe`、`source_label` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 15 / 4 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py)、[tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [fetch_symbol_daily](#fun-7ee0f590bb) | 获取`symbol_daily`；可能影响外部接口；返回 `pd.DataFrame` 类型结果。 | 外部接口 I/O | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) |
| [_fetch_htf_or_resample](#fun-c4f6abf085) | 获取`htf_or_resample`；可能影响外部接口；返回 `pd.DataFrame` 类型结果。 | 外部接口 I/O | — |
| [_fetch_multi_timeframe_once](#fun-d99b48f1eb) | 获取`multi_timeframe_once`；可能影响外部接口；返回 `dict[str, pd.DataFrame]` 类型结果。 | 外部接口 I/O | — |
| [fetch_multi_timeframe](#fun-440d380a28) | 获取多时间框架分析；可能影响外部接口；返回 `dict[str, pd.DataFrame]` 类型结果。 | 外部接口 I/O | — |

#### 函数导航

[_read_system_proxy](#fun-00fc6618ed) · [_setup_proxy](#fun-39e0f0e515) · [get_last_error](#fun-147aba77bf) · [reset_client](#fun-bb3555eebf) · [_report_fetch](#fun-cfbe891cfe) · [_get_client](#fun-71eb929876) · [_normalize](#fun-e022026116) · [_resample](#fun-e5a0c6906a) · [compute_price_drift_1d](#fun-ce47bd6ad9) · [_fetch_bars](#fun-fc45e4816c) · [fetch_symbol_daily](#fun-7ee0f590bb) · [_fetch_htf_or_resample](#fun-c4f6abf085) · [_fetch_multi_timeframe_once](#fun-d99b48f1eb) · [fetch_multi_timeframe](#fun-440d380a28) · [source_label](#fun-b1230c7d4a)

<a id="fun-00fc6618ed"></a>

#### FUN-00FC6618ED

| 设计项 | 说明 |
|---|---|
| 函数 | `_read_system_proxy` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L36` |
| 签名 | `_read_system_proxy()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 读取系统代理配置；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `read_system_proxy`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | read_system_proxy |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-39e0f0e515"></a>

#### FUN-39E0F0E515

| 设计项 | 说明 |
|---|---|
| 函数 | `_setup_proxy` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L40` |
| 签名 | `_setup_proxy()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 执行`setup_proxy`处理；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `apply_system_proxy` → `log.info` → `redact_url`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | apply_system_proxy、log.info、redact_url |
| 复杂度 / 风险 | 分支 1；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-147aba77bf"></a>

#### FUN-147ABA77BF

| 设计项 | 说明 |
|---|---|
| 函数 | `get_last_error` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L51` |
| 签名 | `get_last_error()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 获取`last_error`；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-bb3555eebf"></a>

#### FUN-BB3555EEBF

| 设计项 | 说明 |
|---|---|
| 函数 | `reset_client` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L55` |
| 签名 | `reset_client()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 重置`client`；可能影响全局状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `log.debug`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于全局状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 全局状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.debug |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | [tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="fun-cfbe891cfe"></a>

#### FUN-CFBE891CFE

| 设计项 | 说明 |
|---|---|
| 函数 | `_report_fetch` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L62` |
| 签名 | `_report_fetch(detail: str)` |
| 参数 | `detail`（str）：详细说明文本 |
| 返回 | 无返回值（None） |
| 职责 | 获取报告；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `update` → `get_progress`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | update、get_progress |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-71eb929876"></a>

#### FUN-71EB929876

| 设计项 | 说明 |
|---|---|
| 函数 | `_get_client` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L66` |
| 签名 | `_get_client()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回实现分支产生的结果（源码未标注类型） |
| 职责 | 获取`client`；可能影响全局状态；返回实现分支产生的结果（源码未标注类型）。 |
| 处理逻辑 | 按源码执行顺序经过 `log.info` → `TvDatafeed`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回实现分支产生的结果（源码未标注类型）；可观察变化限于全局状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 全局状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.info、TvDatafeed |
| 复杂度 / 风险 | 分支 2；跨度 12 行；低 |
| 测试 / 验证 | [tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="fun-e022026116"></a>

#### FUN-E022026116

| 设计项 | 说明 |
|---|---|
| 函数 | `_normalize` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L80` |
| 签名 | `_normalize(df: pd.DataFrame \| None)` |
| 参数 | `df`（pd.DataFrame \| None）：输入数据表 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 标准化当前对象；可能影响文件系统；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `ValueError` → `df.copy` → `pd.to_datetime` → `out.rename` → `rename.items` → `copy`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于文件系统 |
| 显式异常 | ValueError |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | ValueError、df.copy、pd.to_datetime、out.rename、rename.items、copy |
| 复杂度 / 风险 | 分支 4；跨度 22 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e5a0c6906a"></a>

#### FUN-E5A0C6906A

| 设计项 | 说明 |
|---|---|
| 函数 | `_resample` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L104` |
| 签名 | `_resample(df: pd.DataFrame, rule: str)` |
| 参数 | `df`（pd.DataFrame）：输入数据表<br>`rule`（str）：由 `rule` 表示的文本或标识 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 构建`resample`；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `agg` → `df.resample` → `ohlcv.dropna`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | agg、df.resample、ohlcv.dropna |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ce47bd6ad9"></a>

#### FUN-CE47BD6AD9

| 设计项 | 说明 |
|---|---|
| 函数 | `compute_price_drift_1d` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L111` |
| 签名 | `compute_price_drift_1d(df_5m: pd.DataFrame, df_1d: pd.DataFrame)` |
| 参数 | `df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`df_1d`（pd.DataFrame）：由调用方提供的 `df_1d` 输入对象 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`price_drift_1d`；返回 `float` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_resample` → `round`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | float、_resample、round |
| 复杂度 / 风险 | 分支 1；跨度 7 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-fc45e4816c"></a>

#### FUN-FC45E4816C

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_bars` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L120` |
| 签名 | `_fetch_bars(interval: 'Interval', n_bars: int, *, label: str, retries: int \| None=None, exchange: str \| None=None, symbol: str \| None=None, report_progress: bool=True)` |
| 参数 | `interval`（'Interval'）：由调用方提供的 `interval` 输入对象<br>`n_bars`（int）：K 线记录集合<br>`label`（str）：展示或分类标签<br>`retries`（int \| None）：由调用方提供的 `retries` 输入对象；默认值 `None`<br>`exchange`（str \| None）：由调用方提供的 `exchange` 输入对象；默认值 `None`<br>`symbol`（str \| None）：交易品种代码；默认值 `None`<br>`report_progress`（bool）：控制对应行为是否启用的布尔值；默认值 `True` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 获取`bars`；可能影响全局状态；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `range` → `_report_fetch` → `log.debug` → `get_hist` → `_get_client` → `_normalize` → `log.info` → `strftime`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于全局状态 |
| 显式异常 | RuntimeError |
| 副作用 | 全局状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | range、_report_fetch、log.debug、get_hist、_get_client、_normalize、log.info、len、strftime、str、log.warning、reset_client、time.sleep、RuntimeError |
| 复杂度 / 风险 | 分支 7；跨度 72 行；中 |
| 测试 / 验证 | [tests/unit/test_tradingview_retry.py](../../../tests/unit/test_tradingview_retry.py) · 直接动态测试 |

<a id="fun-7ee0f590bb"></a>

#### FUN-7EE0F590BB

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_symbol_daily` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L194` |
| 签名 | `fetch_symbol_daily(exchange: str, symbol: str, *, n_bars: int=5, label: str \| None=None)` |
| 参数 | `exchange`（str）：由 `exchange` 表示的文本或标识<br>`symbol`（str）：交易品种代码<br>`n_bars`（int）：K 线记录集合；默认值 `5`<br>`label`（str \| None）：展示或分类标签；默认值 `None` |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 获取`symbol_daily`；可能影响外部接口；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_fetch_bars`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _fetch_bars |
| 复杂度 / 风险 | 分支 0；跨度 19 行；高 |
| 测试 / 验证 | [tests/unit/test_external_sources.py](../../../tests/unit/test_external_sources.py) · 直接动态测试 |

<a id="fun-c4f6abf085"></a>

#### FUN-C4F6ABF085

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_htf_or_resample` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L219` |
| 签名 | `_fetch_htf_or_resample(interval: 'Interval', *, n_bars: int, label: str, df_5m: pd.DataFrame, resample_rule: str)` |
| 参数 | `interval`（'Interval'）：由调用方提供的 `interval` 输入对象<br>`n_bars`（int）：K 线记录集合<br>`label`（str）：展示或分类标签<br>`df_5m`（pd.DataFrame）：5 分钟 OHLCV 数据表<br>`resample_rule`（str）：由 `resample_rule` 表示的文本或标识 |
| 返回 | 返回 `pd.DataFrame` 类型结果 |
| 职责 | 获取`htf_or_resample`；可能影响外部接口；返回 `pd.DataFrame` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `time.sleep` → `_fetch_bars` → `log.warning` → `_report_fetch` → `_resample`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `pd.DataFrame` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | time.sleep、_fetch_bars、log.warning、_report_fetch、_resample |
| 复杂度 / 风险 | 分支 1；跨度 16 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-d99b48f1eb"></a>

#### FUN-D99B48F1EB

| 设计项 | 说明 |
|---|---|
| 函数 | `_fetch_multi_timeframe_once` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L237` |
| 签名 | `_fetch_multi_timeframe_once()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, pd.DataFrame]` 类型结果 |
| 职责 | 获取`multi_timeframe_once`；可能影响外部接口；返回 `dict[str, pd.DataFrame]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_report_fetch` → `_fetch_bars` → `_fetch_htf_or_resample` → `time.sleep` → `log.info` → `out.items`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `dict[str, pd.DataFrame]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _report_fetch、_fetch_bars、_fetch_htf_or_resample、time.sleep、log.info、float、len、out.items |
| 复杂度 / 风险 | 分支 0；跨度 46 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-440d380a28"></a>

#### FUN-440D380A28

| 设计项 | 说明 |
|---|---|
| 函数 | `fetch_multi_timeframe` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L285` |
| 签名 | `fetch_multi_timeframe()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, pd.DataFrame]` 类型结果 |
| 职责 | 获取多时间框架分析；可能影响外部接口；返回 `dict[str, pd.DataFrame]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `log.info` → `_report_fetch` → `range` → `reset_client` → `time.sleep` → `_fetch_multi_timeframe_once` → `log.warning` → `RuntimeError`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `dict[str, pd.DataFrame]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | RuntimeError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | log.info、_report_fetch、range、reset_client、time.sleep、_fetch_multi_timeframe_once、log.warning、RuntimeError |
| 复杂度 / 风险 | 分支 3；跨度 25 行；高 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b1230c7d4a"></a>

#### FUN-B1230C7D4A

| 设计项 | 说明 |
|---|---|
| 函数 | `source_label` |
| 源码位置 | [src/data/tradingview.py](../../../src/data/tradingview.py) · `L312` |
| 签名 | `source_label()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成数据来源标签文本；返回 `str` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 1；跨度 3 行；中 |
| 测试 / 验证 | [tests/unit/test_agent_chain.py](../../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_levels.py](../../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../../tests/unit/test_trader_sentiment.py) · 直接动态测试 |

<a id="unit-62a1aff305"></a>

### UNIT-62A1AFF305

**模块**：`src/data/url_redact.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-62A1AFF305 |
| 源码 | [src/data/url_redact.py](../../../src/data/url_redact.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 实现“行情与外部数据”组件中 `src/data/url_redact.py` 的职责，通过 `redact_url` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-001](../SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](../SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](../SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](../SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](../SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_url_redact.py](../../../tests/unit/test_url_redact.py) |
| 验证状态 | selected |

#### 函数导航

[redact_url](#fun-5d2f35cb3b)

<a id="fun-5d2f35cb3b"></a>

#### FUN-5D2F35CB3B

| 设计项 | 说明 |
|---|---|
| 函数 | `redact_url` |
| 源码位置 | [src/data/url_redact.py](../../../src/data/url_redact.py) · `L8` |
| 签名 | `redact_url(url: str)` |
| 参数 | `url`（str）：外部资源地址 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`redact_url`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `urlparse` → `url.strip` → `urlunparse`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | urlparse、url.strip、urlunparse |
| 复杂度 / 风险 | 分支 2；跨度 10 行；中 |
| 测试 / 验证 | [tests/unit/test_url_redact.py](../../../tests/unit/test_url_redact.py) · 直接动态测试 |
