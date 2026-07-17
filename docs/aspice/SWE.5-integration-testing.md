# SWE.5 集成测试（IT）

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.5 |
| 状态 | 受控基线 |
| 用途 | 评审集成顺序、接口、桩、资源和 IT 结果 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

<a id="vm-integration-pipeline"></a>
<a id="vm-integration-external"></a>
<a id="vm-backtest"></a>

## 准入与退出

### 准入条件

- linked software requirements and architecture interfaces are agreed
- unit verification selection has no blocking gap
- frozen fixtures are available and paid LLM, MT5, and live suppliers are disabled

### 退出条件

- every planned integration item has a verification measure and result disposition
- deterministic integration tests pass within the declared timeout
- supplier-unavailable results are recorded separately from software failures

## 集成顺序

1. `INT-01-CONFIG-RUN`
2. `INT-02-DATA-INDICATORS`
3. `INT-03-ANALYSIS-AGENTS`
4. `INT-04-AGENTS-REPORT-GATE`
5. `INT-05-REPORT-ARCHIVE`
6. `INT-06-REPORT-VIZ`

<a id="int-01-config-run"></a>

## INT-01-CONFIG-RUN

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-APP、ARC-RUN → ARC-CORE |
| 接口 | RunConfig、RunContext、run manifest |
| 需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 前置条件 | frozen environment and temporary archive root |
| 桩 / 隔离 | environment and archive filesystem are isolated by pytest fixtures |
| 超时 / 资源 | 30 秒；no network and no background service |
| 测试 | [tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证措施 | [VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression) |
| 结果 | pass-in-latest-baseline |

<a id="int-02-data-indicators"></a>

## INT-02-DATA-INDICATORS

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-DATA、ARC-INDICATORS → ARC-ANALYSIS |
| 接口 | IF-DATA-CONTEXT |
| 需求 | [SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001) |
| 前置条件 | frozen OHLCV and mocked HTTP responses |
| 桩 / 隔离 | external HTTP is monkeypatched; live supplier health is a separate measure |
| 超时 / 资源 | 30 秒；no network; bounded fixture frames |
| 测试 | [tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_data_freshness.py](../../tests/unit/test_data_freshness.py) |
| 验证措施 | [VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 结果 | pass-deterministic;live-smoke-separate |

<a id="int-03-analysis-agents"></a>

## INT-03-ANALYSIS-AGENTS

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-ANALYSIS → ARC-AGENTS、ARC-LLM |
| 接口 | IF-ANALYSIS-AGENTS |
| 需求 | [SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 前置条件 | fact registry and candidate plans use frozen fixtures |
| 桩 / 隔离 | LLM transport is mocked or disabled |
| 超时 / 资源 | 30 秒；zero paid tokens and no network |
| 测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_llm_context_fact_refs.py](../../tests/unit/test_llm_context_fact_refs.py) |
| 验证措施 | [VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression) |
| 结果 | pass-in-latest-baseline |

<a id="int-04-agents-report-gate"></a>

## INT-04-AGENTS-REPORT-GATE

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-AGENTS、ARC-ANALYSIS → ARC-CORE |
| 接口 | IF-AGENTS-REPORT、FactRegistry、invariant result |
| 需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003) |
| 前置条件 | golden report fixtures include passing and failing invariants |
| 桩 / 隔离 | no external dependency |
| 超时 / 资源 | 30 秒；deterministic and zero network |
| 测试 | [tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py) |
| 验证措施 | [VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 结果 | pass-in-latest-baseline |

<a id="int-05-report-archive"></a>

## INT-05-REPORT-ARCHIVE

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-ANALYSIS、ARC-CORE → ARC-RUN |
| 接口 | IF-REPORT-ARCHIVE、archive schema、compatibility loader |
| 需求 | [SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 前置条件 | temporary archive root and frozen report payload |
| 桩 / 隔离 | filesystem redirected to pytest temporary directory |
| 超时 / 资源 | 30 秒；atomic local writes; no network |
| 测试 | [tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) |
| 验证措施 | [VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression) |
| 结果 | pass-in-latest-baseline |

<a id="int-06-report-viz"></a>

## INT-06-REPORT-VIZ

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-ANALYSIS、ARC-RUN → ARC-VIZ、ARC-APP |
| 接口 | IF-REPORT-ARCHIVE、report dict、chart HTML |
| 需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 前置条件 | frozen report and chart fixtures |
| 桩 / 隔离 | Streamlit rendering uses test doubles where automated; visual acceptance remains controlled manual evidence |
| 超时 / 资源 | 60 秒；no supplier network |
| 测试 | [tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py)、[tests/regression/test_export_sample_report.py](../../tests/regression/test_export_sample_report.py) |
| 验证措施 | [VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 结果 | pass-automated;manual-evidence-referenced |
