# SWE.6 验证测试（VT）

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.6 |
| 状态 | 受控基线 |
| 用途 | 评审验证措施、需求覆盖和发布接受结果 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 选择策略

| 规则 | 内容 |
|---|---|
| release_scope | 所有修改过的源码、文档、配置和测试，以及其追溯闭包。 |
| regression_rule | unit、regression、docs、trace 和 static 为离线必选；integration 按受影响接口选择；live external 独立运行。 |
| entry_criteria | 依赖可用、工作区范围明确、追溯数据通过 schema 校验。 |
| exit_criteria | 必选措施通过；失败已有 SUP.9 Issue；结果绑定 Git SHA、环境和用例版本。 |

## 验证措施目录

| ID | 级别 | 技术 |
|---|---|---|
| [VM-UNIT](#vm-unit) | SWE.4 | automated unit testing |
| [VM-REGRESSION](#vm-regression) | SWE.6 | automated regression testing |
| [VM-INTEGRATION-PIPELINE](#vm-integration-pipeline) | SWE.5 | deterministic cross-component report trust-chain integration |
| [VM-INTEGRATION-EXTERNAL](#vm-integration-external) | SWE.5 | live supplier health smoke |
| [VM-BACKTEST](#vm-backtest) | SWE.5 | point-in-time simulation with frozen fixtures |
| [VM-DOCS](#vm-docs) | SWE.6 | document structure, link and sample synchronization tests |
| [VM-TRACE](#vm-trace) | SWE.1-SWE.6 | bidirectional traceability and document register validation |
| [VM-STATIC](#vm-static) | SWE.4 | compile and patch hygiene |
| [VM-MANUAL-UI](#vm-manual-ui) | SWE.6 | Streamlit visual and interaction acceptance |
| [VM-CONFIG](#vm-config) | SUP.8 | configuration item, lock and SBOM consistency |

<a id="vm-unit"></a>

## VM-UNIT

| 属性 | 内容 |
|---|---|
| 级别 | SWE.4 |
| 技术 | automated unit testing |
| 命令 | python tests/run.py --unit |
| 通过准则 | pytest exit code 0 |
| 环境 | CPython 3.12, no network |

<a id="vm-regression"></a>

## VM-REGRESSION

| 属性 | 内容 |
|---|---|
| 级别 | SWE.6 |
| 技术 | automated regression testing |
| 命令 | python tests/run.py --regression |
| 通过准则 | pytest exit code 0 |
| 环境 | CPython 3.12, no network |

<a id="vm-integration-pipeline"></a>

## VM-INTEGRATION-PIPELINE

| 属性 | 内容 |
|---|---|
| 级别 | SWE.5 |
| 技术 | deterministic cross-component report trust-chain integration |
| 命令 | python -m pytest tests/integration/test_offline_report_contract.py -m integration |
| 通过准则 | pytest exit code 0 within declared timeout |
| 环境 | frozen fixtures; no network, paid LLM, or MT5 |

<a id="vm-integration-external"></a>

## VM-INTEGRATION-EXTERNAL

| 属性 | 内容 |
|---|---|
| 级别 | SWE.5 |
| 技术 | live supplier health smoke |
| 命令 | python tests/run.py --external |
| 通过准则 | result classified as pass, supplier unavailable, or software failure; only software failure blocks release |
| 环境 | network required; not part of deterministic offline gate |

<a id="vm-backtest"></a>

## VM-BACKTEST

| 属性 | 内容 |
|---|---|
| 级别 | SWE.5 |
| 技术 | point-in-time simulation with frozen fixtures |
| 命令 | python -m pytest tests/unit/test_backtest_*.py |
| 通过准则 | pytest exit code 0 and no future-data assertion violation |
| 环境 | no network |

<a id="vm-docs"></a>

## VM-DOCS

| 属性 | 内容 |
|---|---|
| 级别 | SWE.6 |
| 技术 | document structure, link and sample synchronization tests |
| 命令 | python -m pytest tests/regression/test_doc_pipeline_sync.py tests/regression/test_docs_structure.py tests/regression/test_export_sample_report.py |
| 通过准则 | pytest exit code 0 |
| 环境 | no network |

<a id="vm-trace"></a>

## VM-TRACE

| 属性 | 内容 |
|---|---|
| 级别 | SWE.1-SWE.6 |
| 技术 | bidirectional traceability and document register validation |
| 命令 | python scripts/check_aspice_assets.py --check and python scripts/generate_aspice_software_evidence.py --check |
| 通过准则 | exit code 0, no orphan or dangling identifier |
| 环境 | no network; PyYAML available |

<a id="vm-static"></a>

## VM-STATIC

| 属性 | 内容 |
|---|---|
| 级别 | SWE.4 |
| 技术 | compile and patch hygiene |
| 命令 | python -m compileall -q src app.py run_app.py scripts && git diff --check |
| 通过准则 | both commands exit code 0 |
| 环境 | no network |

<a id="vm-manual-ui"></a>

## VM-MANUAL-UI

| 属性 | 内容 |
|---|---|
| 级别 | SWE.6 |
| 技术 | Streamlit visual and interaction acceptance |
| 命令 | python run_app.py |
| 通过准则 | applicable UI catalog cases pass with screenshots/notes |
| 环境 | supported browser at desktop and mobile widths |

<a id="vm-config"></a>

## VM-CONFIG

| 属性 | 内容 |
|---|---|
| 级别 | SUP.8 |
| 技术 | configuration item, lock and SBOM consistency |
| 命令 | python scripts/check_aspice_assets.py --check |
| 通过准则 | all controlled paths exist and dependency lock equals SBOM component versions |
| 环境 | no network |

## 需求覆盖结论

共 **26 条需求**；阻断覆盖缺口 **0** 条。

| 需求 | 架构 | 验证措施 | 接受结果 | 状态 |
|---|---|---|---|---|
| [SWR-CORE-001](SWE.1-software-requirements.md#swr-core-001) | [ARC-CORE](SWE.2-software-architecture.md#arc-core)、[ARC-DATA](SWE.2-software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-software-architecture.md#arc-agents)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-CORE-002](SWE.1-software-requirements.md#swr-core-002) | [ARC-APP](SWE.2-software-architecture.md#arc-app)、[ARC-CORE](SWE.2-software-architecture.md#arc-core)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-DATA-001](SWE.1-software-requirements.md#swr-data-001) | [ARC-DATA](SWE.2-software-architecture.md#arc-data) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-DATA-002](SWE.1-software-requirements.md#swr-data-002) | [ARC-DATA](SWE.2-software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-DATA-003](SWE.1-software-requirements.md#swr-data-003) | [ARC-DATA](SWE.2-software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ANA-001](SWE.1-software-requirements.md#swr-ana-001) | [ARC-INDICATORS](SWE.2-software-architecture.md#arc-indicators)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ANA-002](SWE.1-software-requirements.md#swr-ana-002) | [ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-software-architecture.md#arc-agents) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ANA-003](SWE.1-software-requirements.md#swr-ana-003) | [ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-software-architecture.md#arc-agents) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-AGT-001](SWE.1-software-requirements.md#swr-agt-001) | [ARC-AGENTS](SWE.2-software-architecture.md#arc-agents)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-LLM-001](SWE.1-software-requirements.md#swr-llm-001) | [ARC-LLM](SWE.2-software-architecture.md#arc-llm)、[ARC-AGENTS](SWE.2-software-architecture.md#arc-agents)、[ARC-CORE](SWE.2-software-architecture.md#arc-core) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-LLM-002](SWE.1-software-requirements.md#swr-llm-002) | [ARC-LLM](SWE.2-software-architecture.md#arc-llm)、[ARC-AGENTS](SWE.2-software-architecture.md#arc-agents) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-LLM-003](SWE.1-software-requirements.md#swr-llm-003) | [ARC-LLM](SWE.2-software-architecture.md#arc-llm)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-AGENTS](SWE.2-software-architecture.md#arc-agents) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-REP-001](SWE.1-software-requirements.md#swr-rep-001) | [ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-CORE](SWE.2-software-architecture.md#arc-core)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-REP-002](SWE.1-software-requirements.md#swr-rep-002) | [ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-REP-003](SWE.1-software-requirements.md#swr-rep-003) | [ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-CORE](SWE.2-software-architecture.md#arc-core)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-REP-004](SWE.1-software-requirements.md#swr-rep-004) | [ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis)、[ARC-VIZ](SWE.2-software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ARC-001](SWE.1-software-requirements.md#swr-arc-001) | [ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ARC-002](SWE.1-software-requirements.md#swr-arc-002) | [ARC-RUN](SWE.2-software-architecture.md#arc-run)、[ARC-VIZ](SWE.2-software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-BT-001](SWE.1-software-requirements.md#swr-bt-001) | [ARC-BACKTEST](SWE.2-software-architecture.md#arc-backtest)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](SWE.5-integration-testing.md#vm-backtest) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](SWE.5-integration-testing.md#vm-backtest) | closed |
| [SWR-UI-001](SWE.1-software-requirements.md#swr-ui-001) | [ARC-APP](SWE.2-software-architecture.md#arc-app)、[ARC-VIZ](SWE.2-software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) | closed |
| [SWR-UI-002](SWE.1-software-requirements.md#swr-ui-002) | [ARC-VIZ](SWE.2-software-architecture.md#arc-viz)、[ARC-ANALYSIS](SWE.2-software-architecture.md#arc-analysis) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) | closed |
| [SWR-CFG-001](SWE.1-software-requirements.md#swr-cfg-001) | [ARC-APP](SWE.2-software-architecture.md#arc-app)、[ARC-CORE](SWE.2-software-architecture.md#arc-core)、[ARC-DATA](SWE.2-software-architecture.md#arc-data)、[ARC-LLM](SWE.2-software-architecture.md#arc-llm) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-CONFIG](SWE.6-validation-testing.md#vm-config) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-CONFIG](SWE.6-validation-testing.md#vm-config) | closed |
| [SWR-NFR-001](SWE.1-software-requirements.md#swr-nfr-001) | [ARC-DATA](SWE.2-software-architecture.md#arc-data)、[ARC-LLM](SWE.2-software-architecture.md#arc-llm)、[ARC-CORE](SWE.2-software-architecture.md#arc-core) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-NFR-002](SWE.1-software-requirements.md#swr-nfr-002) | [ARC-CORE](SWE.2-software-architecture.md#arc-core)、[ARC-RUN](SWE.2-software-architecture.md#arc-run)、[ARC-VIZ](SWE.2-software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-NFR-003](SWE.1-software-requirements.md#swr-nfr-003) | [ARC-TOOLS](SWE.2-software-architecture.md#arc-tools) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace)、[VM-STATIC](SWE.6-validation-testing.md#vm-static) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace)、[VM-STATIC](SWE.6-validation-testing.md#vm-static) | closed |
| [SWR-NFR-004](SWE.1-software-requirements.md#swr-nfr-004) | [ARC-TOOLS](SWE.2-software-architecture.md#arc-tools)、[ARC-RUN](SWE.2-software-architecture.md#arc-run) | [VM-CONFIG](SWE.6-validation-testing.md#vm-config)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace) | [VM-CONFIG](SWE.6-validation-testing.md#vm-config)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace) | closed |

## 最新结果

详见 [软件域验证结果](./verification-results/latest.md)。
