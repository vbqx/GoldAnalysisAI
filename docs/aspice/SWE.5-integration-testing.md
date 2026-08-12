# SWE.5 集成测试（IT）

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.5 |
| 状态 | 受控基线 |
| 用途 | 评审集成顺序、接口、桩、资源和 IT 结果 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

<a id="vm-unit"></a>

## VM-UNIT

关联集成项：[INT-01-CONFIG-CORE](#int-01-config-core)、[INT-02-DATA-STRUCTURE](#int-02-data-structure)、[INT-03-CONTEXT-ADVICE](#int-03-context-advice)、[INT-04-ADVICE-LLM](#int-04-advice-llm)、[INT-05-REPORT-ARCHIVE](#int-05-report-archive)、[INT-06-REPORT-VIZ](#int-06-report-viz)

<a id="vm-regression"></a>

## VM-REGRESSION

关联集成项：[INT-01-CONFIG-CORE](#int-01-config-core)、[INT-04-ADVICE-LLM](#int-04-advice-llm)、[INT-05-REPORT-ARCHIVE](#int-05-report-archive)、[INT-06-REPORT-VIZ](#int-06-report-viz)

<a id="vm-integration-external"></a>

## VM-INTEGRATION-EXTERNAL

关联集成项：[INT-02-DATA-STRUCTURE](#int-02-data-structure)

<a id="vm-integration-pipeline"></a>

## VM-INTEGRATION-PIPELINE

关联集成项：[INT-03-CONTEXT-ADVICE](#int-03-context-advice)

<a id="vm-manual-ui"></a>

## VM-MANUAL-UI

关联集成项：[INT-06-REPORT-VIZ](#int-06-report-viz)

## 准入与退出

### 准入条件

- linked software requirements and architecture interfaces are agreed
- unit verification selection has no blocking gap
- frozen fixtures are available and external suppliers and paid LLM calls are disabled

### 退出条件

- every planned integration item has a verification measure and disposition
- deterministic integration tests pass within the declared timeout
- supplier-unavailable results remain separate from software failures

## 集成顺序

1. `INT-01-CONFIG-CORE`
2. `INT-02-DATA-STRUCTURE`
3. `INT-03-CONTEXT-ADVICE`
4. `INT-04-ADVICE-LLM`
5. `INT-05-REPORT-ARCHIVE`
6. `INT-06-REPORT-VIZ`

<a id="int-01-config-core"></a>

## INT-01-CONFIG-CORE

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-APP、ARC-RUN → ARC-CORE |
| 接口 | application entry、run_advice_pipeline |
| 需求 | [SWR-CORE-001](SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](SWE.1-software-requirements.md#swr-core-002)、[SWR-CFG-001](SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-002](SWE.1-software-requirements.md#swr-nfr-002) |
| 前置条件 | frozen environment and temporary archive root |
| 桩 / 隔离 | environment and filesystem are isolated by pytest fixtures |
| 超时 / 资源 | 30 秒；no network and no background service |
| 测试 | [tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |
| 结果 | pass-in-current-baseline |

<a id="int-02-data-structure"></a>

## INT-02-DATA-STRUCTURE

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-DATA、ARC-INDICATORS → ARC-ANALYSIS、ARC-ADVICE |
| 接口 | IF-DATA-CONTEXT |
| 需求 | [SWR-DATA-001](SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](SWE.1-software-requirements.md#swr-ana-001) |
| 前置条件 | frozen OHLCV and mocked external responses |
| 桩 / 隔离 | external HTTP is monkeypatched; live health is a separate measure |
| 超时 / 资源 | 30 秒；no network and bounded fixture frames |
| 测试 | [tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_data_freshness.py](../../tests/unit/test_data_freshness.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) |
| 结果 | pass-deterministic;live-smoke-separate |

<a id="int-03-context-advice"></a>

## INT-03-CONTEXT-ADVICE

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-DATA、ARC-ANALYSIS → ARC-ADVICE |
| 接口 | IF-CONTEXT-ADVICE、AdvicePacket |
| 需求 | [SWR-ADV-001](SWE.1-software-requirements.md#swr-adv-001)、[SWR-ADV-002](SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-003](SWE.1-software-requirements.md#swr-adv-003)、[SWR-ADV-004](SWE.1-software-requirements.md#swr-adv-004) |
| 前置条件 | frozen aligned bullish, bearish, conflicting and stale contexts |
| 桩 / 隔离 | no external dependency |
| 超时 / 资源 | 30 秒；deterministic and zero network |
| 测试 | [tests/unit/test_advice_v2.py](../../tests/unit/test_advice_v2.py)、[tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) |
| 结果 | pass-in-current-baseline |

<a id="int-04-advice-llm"></a>

## INT-04-ADVICE-LLM

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-ADVICE → ARC-LLM |
| 接口 | IF-ADVICE-LLM、advisor wording pass |
| 需求 | [SWR-LLM-001](SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](SWE.1-software-requirements.md#swr-llm-002)、[SWR-NFR-001](SWE.1-software-requirements.md#swr-nfr-001) |
| 前置条件 | deterministic AdvicePacket and mocked LLM transport |
| 桩 / 隔离 | model responses and transport errors are fully controlled |
| 超时 / 资源 | 30 秒；zero paid tokens and no network |
| 测试 | [tests/unit/test_advice_v2.py](../../tests/unit/test_advice_v2.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |
| 结果 | pass-in-current-baseline |

<a id="int-05-report-archive"></a>

## INT-05-REPORT-ARCHIVE

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-ADVICE、ARC-CORE → ARC-RUN |
| 接口 | IF-ADVICE-REPORT、IF-REPORT-ARCHIVE、archive bundle |
| 需求 | [SWR-REP-001](SWE.1-software-requirements.md#swr-rep-001)、[SWR-ARC-001](SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](SWE.1-software-requirements.md#swr-nfr-002) |
| 前置条件 | temporary archive root and deterministic V2 and legacy fixtures |
| 桩 / 隔离 | filesystem redirected to pytest temporary directory |
| 超时 / 资源 | 30 秒；atomic local writes and no network |
| 测试 | [tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) |
| 结果 | pass-in-current-baseline |

<a id="int-06-report-viz"></a>

## INT-06-REPORT-VIZ

| 属性 | 内容 |
|---|---|
| 提供者 → 消费者 | ARC-ADVICE、ARC-RUN → ARC-VIZ、ARC-APP |
| 接口 | IF-ADVICE-REPORT、IF-REPORT-ARCHIVE、render_advice |
| 需求 | [SWR-ADV-002](SWE.1-software-requirements.md#swr-adv-002)、[SWR-ADV-004](SWE.1-software-requirements.md#swr-adv-004)、[SWR-UI-001](SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](SWE.1-software-requirements.md#swr-ui-002) |
| 前置条件 | frozen Advice V2 report and replay fixtures |
| 桩 / 隔离 | Streamlit rendering uses test doubles where automated |
| 超时 / 资源 | 60 秒；no supplier network |
| 测试 | [tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_process_view.py](../../tests/unit/test_llm_process_view.py)、[tests/unit/test_live_llm_process_panel.py](../../tests/unit/test_live_llm_process_panel.py)、[tests/regression/test_export_sample_report.py](../../tests/regression/test_export_sample_report.py) |
| 验证措施 | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) |
| 结果 | pass-automated;manual-review-required-for-new-baseline |
