# SWE.1 软件需求分析

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.1 |
| 状态 | 受控基线 |
| 用途 | 理解、评审并追踪软件需求 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 基线概览

本基线包含 **22 条软件需求**。需求按唯一 ID 管理，并链接到架构组件、验证措施和接受准则。

| 优先级 | 数量 |
|---|---|
| P0 | 14 |
| P1 | 8 |

## 需求目录

| ID | 标题 | 类型 | 优先级 | 状态 |
|---|---|---|---|---|
| [SWR-CORE-001](#swr-core-001) | Advice V2 analysis pipeline | functional | P0 | agreed |
| [SWR-CORE-002](#swr-core-002) | Controlled run modes | functional | P1 | agreed |
| [SWR-DATA-001](#swr-data-001) | Multi-timeframe XAUUSD market data | functional | P0 | agreed |
| [SWR-DATA-002](#swr-data-002) | External data as background context | reliability | P1 | agreed |
| [SWR-DATA-003](#swr-data-003) | Data freshness and as-of control | reliability | P0 | agreed |
| [SWR-ANA-001](#swr-ana-001) | Reproducible market-structure facts | functional | P0 | agreed |
| [SWR-ADV-001](#swr-adv-001) | Exactly one primary suggestion or no setup | functional | P0 | agreed |
| [SWR-ADV-002](#swr-adv-002) | Human-confirmable setup | functional | P0 | agreed |
| [SWR-ADV-003](#swr-adv-003) | Deterministic advice audit | reliability | P0 | agreed |
| [SWR-ADV-004](#swr-adv-004) | Evidence and uncertainty disclosure | reliability | P1 | agreed |
| [SWR-LLM-001](#swr-llm-001) | Single constrained wording pass | functional | P1 | agreed |
| [SWR-LLM-002](#swr-llm-002) | LLM immutability and fallback | reliability | P0 | agreed |
| [SWR-REP-001](#swr-rep-001) | Versioned human-review report | functional | P0 | agreed |
| [SWR-ARC-001](#swr-arc-001) | Run archive persistence | functional | P1 | agreed |
| [SWR-ARC-002](#swr-arc-002) | Legacy archive reconstruction | compatibility | P1 | agreed |
| [SWR-UI-001](#swr-ui-001) | Human-review advice interface | functional | P1 | agreed |
| [SWR-UI-002](#swr-ui-002) | Manual-confirmation disclosure | reliability | P0 | agreed |
| [SWR-CFG-001](#swr-cfg-001) | Configuration and secret handling | security | P0 | agreed |
| [SWR-NFR-001](#swr-nfr-001) | Fault isolation and graceful degradation | reliability | P0 | agreed |
| [SWR-NFR-002](#swr-nfr-002) | Auditability and reproducibility | maintainability | P0 | agreed |
| [SWR-NFR-003](#swr-nfr-003) | Automated quality gate | maintainability | P0 | agreed |
| [SWR-NFR-004](#swr-nfr-004) | Configuration-management evidence | maintainability | P1 | agreed |

<a id="swr-core-001"></a>

## SWR-CORE-001

**标题**：Advice V2 analysis pipeline

The system shall execute data acquisition, indicator enrichment, market-structure extraction, advice generation, report composition and archive persistence in a controlled order, returning the report, enriched frames and timeframe analyses.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/records/reviews/financial/advice-v2-rearchitecture-2026-08-12.md |
| 验证准则 | Deterministic integration tests demonstrate the ordered pipeline and an Advice V2 artifact result. |
| 运行环境影响 | CPython 3.12; Windows primary development environment and Linux CI. |
| 架构组件 | [ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-core-002"></a>

## SWR-CORE-002

**标题**：Controlled run modes

The system shall support deterministic advice, optional LLM wording enhancement and archive replay using an immutable per-run configuration; replay shall not fetch new data or invoke an LLM.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/system-overview.md |
| 验证准则 | Configuration tests cover defaults, normalization, legacy hybrid mapping, replay isolation and fingerprints. |
| 运行环境影响 | Environment variables come from .env or the host and secrets shall not be written into reports. |
| 架构组件 | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-data-001"></a>

## SWR-DATA-001

**标题**：Multi-timeframe XAUUSD market data

The system shall acquire and normalize 5m, 15m, 1h, 4h and 1d OHLCV data with source and timestamp semantics; current price shall be anchored to the latest 5m close in the same batch.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/technical-analysis.md |
| 验证准则 | Data tests verify columns, ordering, timeframe coverage, degradation and current-price alignment. |
| 运行环境影响 | Live acquisition depends on configured market-data suppliers and UTC timestamp semantics. |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |

<a id="swr-data-002"></a>

## SWR-DATA-002

**标题**：External data as background context

The system shall acquire or explicitly degrade DXY, yield, news, calendar and social sources, retain source and error metadata, and prevent external narrative data from directly creating entry prices.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P1 / agreed |
| 来源 | docs/aspice/records/reviews/financial/advice-v2-rearchitecture-2026-08-12.md |
| 验证准则 | Tests cover success, confirmed-empty, timeout, unavailable and source-policy behavior. |
| 运行环境影响 | Supplier availability is external; live smoke results are separated from deterministic release gates. |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |

<a id="swr-data-003"></a>

## SWR-DATA-003

**标题**：Data freshness and as-of control

The system shall calculate data-as-of and freshness state and shall produce AVOID rather than a watch setup when the market snapshot does not satisfy freshness requirements.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Fixed-clock tests cover fresh, stale, closed-market, future-data and timezone boundaries. |
| 运行环境影响 | Internal comparisons use timezone-aware UTC values. |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-ana-001"></a>

## SWR-ANA-001

**标题**：Reproducible market-structure facts

The system shall calculate indicators, PA/ICT structure, liquidity, support and resistance from point-in-time data and retain timeframe and source semantics for facts used by advice.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/technical-analysis.md |
| 验证准则 | Deterministic fixtures cover normal, inverse, boundary, insufficient-history and no-future-data cases. |
| 运行环境影响 | pandas and numpy versions and resampling semantics are configuration-baseline items. |
| 架构组件 | [ARC-INDICATORS](SWE.2-architecture/software-architecture.md#arc-indicators)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-adv-001"></a>

## SWR-ADV-001

**标题**：Exactly one primary suggestion or no setup

The system shall emit exactly one decision from WAIT, WATCH_LONG, WATCH_SHORT or AVOID and shall include at most one primary setup; it shall never authorize or execute a trade.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/records/reviews/financial/advice-v2-rearchitecture-2026-08-12.md |
| 验证准则 | Advice tests cover aligned bullish, aligned bearish, conflicting and unavailable scenarios and reject V1 execution semantics. |
| 运行环境影响 | Output is for manual review only. |
| 架构组件 | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-adv-002"></a>

## SWR-ADV-002

**标题**：Human-confirmable setup

A watch setup shall include an attention zone, current state, rationale, an observable confirmation checklist, invalidation condition and level, no more than two targets, evidence identifiers and reward-risk values.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Contract tests assert every required field, cardinality and evidence reference. |
| 运行环境影响 | All prices use XAUUSD quote units; display rounding shall not change validation geometry. |
| 架构组件 | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-adv-003"></a>

## SWR-ADV-003

**标题**：Deterministic advice audit

Before publication the system shall validate decision-direction alignment, attention-zone geometry, invalidation placement, target ordering, evidence references and checklist presence; failed audits shall degrade to AVOID.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Boundary tests cover BUY and SELL geometry, missing evidence, missing checklist and audit degradation. |
| 运行环境影响 | The audit is offline deterministic code and does not depend on LLM availability. |
| 架构组件 | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-adv-004"></a>

## SWR-ADV-004

**标题**：Evidence and uncertainty disclosure

Advice shall distinguish source-backed evidence, risks and uncertainties and shall use WAIT or AVOID when directional agreement, confluence or target space is insufficient.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Tests cover higher-timeframe conflict, isolated levels, absent targets and stale data. |
| 运行环境影响 | Confidence is a qualitative evidence grade, not a historical win probability. |
| 架构组件 | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-llm-001"></a>

## SWR-LLM-001

**标题**：Single constrained wording pass

When enabled, the system shall perform one optional LLM pass limited to editing explanatory text and shall record model, latency, retry, budget and usage telemetry.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Mock-client tests cover success, transport failure, invalid JSON, retry exhaustion and telemetry. |
| 运行环境影响 | The pass uses an OpenAI-compatible external API; paid calls are excluded from deterministic gates. |
| 架构组件 | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |

<a id="swr-llm-002"></a>

## SWR-LLM-002

**标题**：LLM immutability and fallback

LLM output shall not change decision, bias, confidence, direction or any numeric value and shall not invent a setup or price; rejected or failed output shall preserve deterministic advice.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Tests inject changed numbers, invented setup fields and malformed output and verify deterministic fallback. |
| 运行环境影响 | LLM availability cannot prevent deterministic Advice V2 generation. |
| 架构组件 | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-rep-001"></a>

## SWR-REP-001

**标题**：Versioned human-review report

The system shall publish artifact_kind human_review_advice with artifact_version 2 and the meta, metrics, advice, timeframes, levels and external sections; V1 agent_trace, signals, projections and validated_plans shall be absent.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P0 / agreed |
| 来源 | docs/aspice/SWE.3-detailed-design/reference/examples/report-schema.md |
| 验证准则 | Unit and sample-export regression tests verify required and prohibited fields. |
| 运行环境影响 | Contract-breaking changes require an artifact-version increment. |
| 架构组件 | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-arc-001"></a>

## SWR-ARC-001

**标题**：Run archive persistence

The system shall archive run configuration, manifest, Advice V2 report, analyses, data summary and status with atomic local-file behavior and support listing, loading, transfer and retention.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/SWE.3-detailed-design/reference/run-archive-schema.md |
| 验证准则 | Archive tests cover success, failure, atomic write, index, transfer and pruning. |
| 运行环境影响 | The configured data directory must be writable. |
| 架构组件 | [ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-arc-002"></a>

## SWR-ARC-002

**标题**：Legacy archive reconstruction

Replay shall load an Advice V2 report directly or reconstruct Advice V2 from stored market data and analyses in a legacy archive; legacy V1 report recommendations shall not be displayed as active advice.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | compatibility / P1 / agreed |
| 来源 | docs/aspice/SWE.3-detailed-design/reference/run-archive-schema.md |
| 验证准则 | Compatibility fixtures cover V2, legacy reconstruction, missing payloads and incompatible archives without new fetch or LLM calls. |
| 运行环境影响 | Historical archives may originate from different Git revisions and schema versions. |
| 架构组件 | [ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-ui-001"></a>

## SWR-UI-001

**标题**：Human-review advice interface

The Streamlit application shall make the compact advice card the primary view and provide external-data, optional LLM thinking-process audit and replay access without V1 strategy, debate or decision-chain pages.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | functional / P1 / agreed |
| 来源 | docs/aspice/records/reviews/financial/advice-v2-rearchitecture-2026-08-12.md |
| 验证准则 | UI helper tests and manual acceptance cover navigation, generation, replay, advice presentation and LLM telemetry audit. |
| 运行环境影响 | The application is launched through run_app.py. |
| 架构组件 | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) |

<a id="swr-ui-002"></a>

## SWR-UI-002

**标题**：Manual-confirmation disclosure

The interface shall clearly state that suggestions require human confirmation and are not automatically executed, and shall expose evidence, uncertainty, audit state, invalidation and alternative scenario where applicable.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/aspice/SWE.2-architecture/human-review-advice.md |
| 验证准则 | Component tests and manual review verify disclosure and audit-detail accessibility. |
| 运行环境影响 | Text must remain readable at supported desktop and mobile widths. |
| 架构组件 | [ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) |

<a id="swr-cfg-001"></a>

## SWR-CFG-001

**标题**：Configuration and secret handling

Runtime supplier, LLM, timeout and archive settings shall come from controlled environment configuration, with secrets disabled by default in examples and excluded from reports and logs; the controlled template documents SiliconFlow DeepSeek-V4-Flash as the default optional wording provider.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | security / P0 / agreed |
| 来源 | docs/operations/setup.md |
| 验证准则 | Configuration tests and secret scans verify defaults, URL sanitization and controlled examples. |
| 运行环境影响 | Production credentials are supplied outside version control. |
| 架构组件 | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-CONFIG](SWE.6-validation-testing.md#vm-config) |

<a id="swr-nfr-001"></a>

## SWR-NFR-001

**标题**：Fault isolation and graceful degradation

Supplier and optional LLM failures shall be bounded by timeout, recorded explicitly and degraded without fabricating facts or losing deterministic advice when sufficient market data remains.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | reliability / P0 / agreed |
| 来源 | docs/management/audit-plan.md |
| 验证准则 | Fault-injection tests cover timeout, empty result, invalid JSON, HTTP errors and partial external data. |
| 运行环境影响 | Network supplier availability is not controlled by the software. |
| 架构组件 | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |

<a id="swr-nfr-002"></a>

## SWR-NFR-002

**标题**：Auditability and reproducibility

Each run shall retain data source, data-as-of, run configuration fingerprint, generation steps, advice source, deterministic audit and optional LLM telemetry sufficient to explain the result.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | maintainability / P0 / agreed |
| 来源 | docs/management/audit-plan.md |
| 验证准则 | Report, progress and archive tests verify stable and complete metadata. |
| 运行环境影响 | Archive retention is bounded by configured count and size limits. |
| 架构组件 | [ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |

<a id="swr-nfr-003"></a>

## SWR-NFR-003

**标题**：Automated quality gate

Source, tests, documentation and configuration changes shall pass unit, regression, documentation, traceability and static-hygiene checks before release.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | maintainability / P0 / agreed |
| 来源 | .github/workflows/quality.yml |
| 验证准则 | The declared commands complete with zero blocking failure. |
| 运行环境影响 | CI runs on a supported CPython environment with deterministic tests offline. |
| 架构组件 | [ARC-TOOLS](SWE.2-architecture/software-architecture.md#arc-tools) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace)、[VM-STATIC](SWE.6-validation-testing.md#vm-static) |

<a id="swr-nfr-004"></a>

## SWR-NFR-004

**标题**：Configuration-management evidence

The project shall maintain controlled configuration items, exact dependency resolution, SBOM, document register and bidirectional requirement-to-architecture-to-verification traceability.

| 属性 | 内容 |
|---|---|
| 类型 / 优先级 / 状态 | maintainability / P1 / agreed |
| 来源 | docs/aspice/_machine/configuration-management.yaml |
| 验证准则 | Configuration and trace checks report no missing path, orphan identifier or dependency mismatch. |
| 运行环境影响 | Generated evidence is deterministic for the same repository baseline. |
| 架构组件 | [ARC-TOOLS](SWE.2-architecture/software-architecture.md#arc-tools)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) |
| 验证措施 | [VM-CONFIG](SWE.6-validation-testing.md#vm-config)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace) |
