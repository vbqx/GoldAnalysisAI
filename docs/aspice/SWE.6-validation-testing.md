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
| release_scope | Advice V2 source, tests, configuration and controlled documentation. |
| regression_rule | Unit, regression, documentation, trace and static measures block release; live supplier health is classified separately. |
| entry_criteria | Requirements, architecture and interfaces are agreed and deterministic fixtures are available. |
| exit_criteria | Every requirement has an accepted verification disposition and no blocking failure remains. |

## 验证措施目录

| ID | 级别 | 技术 |
|---|---|---|
| [VM-UNIT](#vm-unit) | SWE.4 | automated unit testing |
| [VM-REGRESSION](#vm-regression) | SWE.6 | automated regression testing |
| [VM-INTEGRATION-PIPELINE](#vm-integration-pipeline) | SWE.5 | deterministic Advice V2 cross-component contract integration |
| [VM-INTEGRATION-EXTERNAL](#vm-integration-external) | SWE.5 | live supplier health smoke |
| [VM-DOCS](#vm-docs) | SWE.6 | documentation structure, links, pipeline and sample synchronization |
| [VM-TRACE](#vm-trace) | SWE.1-SWE.6 | bidirectional traceability and document-register validation |
| [VM-STATIC](#vm-static) | SWE.4 | compile and patch hygiene |
| [VM-MANUAL-UI](#vm-manual-ui) | SWE.6 | Streamlit visual and interaction acceptance |
| [VM-CONFIG](#vm-config) | SUP.8 | configuration item, dependency lock and SBOM consistency |

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
| 技术 | deterministic Advice V2 cross-component contract integration |
| 命令 | python -m pytest tests/unit/test_advice_v2.py tests/unit/test_orchestrator_hooks.py |
| 通过准则 | pytest exit code 0 within declared timeout |
| 环境 | frozen fixtures; no network or paid LLM |

<a id="vm-integration-external"></a>

## VM-INTEGRATION-EXTERNAL

| 属性 | 内容 |
|---|---|
| 级别 | SWE.5 |
| 技术 | live supplier health smoke |
| 命令 | python tests/run.py --external |
| 通过准则 | result classified as pass, supplier unavailable, or software failure; only software failure blocks release |
| 环境 | network required; separate from deterministic offline gate |

<a id="vm-docs"></a>

## VM-DOCS

| 属性 | 内容 |
|---|---|
| 级别 | SWE.6 |
| 技术 | documentation structure, links, pipeline and sample synchronization |
| 命令 | python tests/run.py --regression |
| 通过准则 | documentation regression tests exit 0 |
| 环境 | no network |

<a id="vm-trace"></a>

## VM-TRACE

| 属性 | 内容 |
|---|---|
| 级别 | SWE.1-SWE.6 |
| 技术 | bidirectional traceability and document-register validation |
| 命令 | python scripts/check_aspice_assets.py --check and python scripts/generate_aspice_software_evidence.py --check |
| 通过准则 | exit code 0 with no orphan or dangling identifier |
| 环境 | no network; PyYAML available |

<a id="vm-static"></a>

## VM-STATIC

| 属性 | 内容 |
|---|---|
| 级别 | SWE.4 |
| 技术 | compile and patch hygiene |
| 命令 | python -m compileall -q src app.py run_app.py scripts and git diff --check |
| 通过准则 | both commands exit code 0 |
| 环境 | no network |

<a id="vm-manual-ui"></a>

## VM-MANUAL-UI

| 属性 | 内容 |
|---|---|
| 级别 | SWE.6 |
| 技术 | Streamlit visual and interaction acceptance |
| 命令 | python run_app.py |
| 通过准则 | Advice V2 UI catalog cases pass with screenshots or review notes |
| 环境 | supported browser at desktop and mobile widths |

<a id="vm-config"></a>

## VM-CONFIG

| 属性 | 内容 |
|---|---|
| 级别 | SUP.8 |
| 技术 | configuration item, dependency lock and SBOM consistency |
| 命令 | python scripts/check_aspice_assets.py --check |
| 通过准则 | controlled paths exist and dependency lock equals SBOM versions |
| 环境 | no network |

## 需求覆盖结论

共 **22 条需求**；阻断覆盖缺口 **0** 条。

| 需求 | 架构 | 验证措施 | 接受结果 | 状态 |
|---|---|---|---|---|
| [SWR-CORE-001](SWE.1-software-requirements.md#swr-core-001) | [ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-CORE-002](SWE.1-software-requirements.md#swr-core-002) | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-DATA-001](SWE.1-software-requirements.md#swr-data-001) | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-DATA-002](SWE.1-software-requirements.md#swr-data-002) | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-DATA-003](SWE.1-software-requirements.md#swr-data-003) | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ANA-001](SWE.1-software-requirements.md#swr-ana-001) | [ARC-INDICATORS](SWE.2-architecture/software-architecture.md#arc-indicators)、[ARC-ANALYSIS](SWE.2-architecture/software-architecture.md#arc-analysis) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ADV-001](SWE.1-software-requirements.md#swr-adv-001) | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-ADV-002](SWE.1-software-requirements.md#swr-adv-002) | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-ADV-003](SWE.1-software-requirements.md#swr-adv-003) | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-ADV-004](SWE.1-software-requirements.md#swr-adv-004) | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-LLM-001](SWE.1-software-requirements.md#swr-llm-001) | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-PIPELINE](SWE.5-integration-testing.md#vm-integration-pipeline) | closed |
| [SWR-LLM-002](SWE.1-software-requirements.md#swr-llm-002) | [ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-REP-001](SWE.1-software-requirements.md#swr-rep-001) | [ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ARC-001](SWE.1-software-requirements.md#swr-arc-001) | [ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run)、[ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-ARC-002](SWE.1-software-requirements.md#swr-arc-002) | [ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-UI-001](SWE.1-software-requirements.md#swr-ui-001) | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-UI-002](SWE.1-software-requirements.md#swr-ui-002) | [ARC-VIZ](SWE.2-architecture/software-architecture.md#arc-viz)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](SWE.6-validation-testing.md#vm-manual-ui) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-CFG-001](SWE.1-software-requirements.md#swr-cfg-001) | [ARC-APP](SWE.2-architecture/software-architecture.md#arc-app)、[ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-CONFIG](SWE.6-validation-testing.md#vm-config) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-CONFIG](SWE.6-validation-testing.md#vm-config) | closed |
| [SWR-NFR-001](SWE.1-software-requirements.md#swr-nfr-001) | [ARC-DATA](SWE.2-architecture/software-architecture.md#arc-data)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-LLM](SWE.2-architecture/software-architecture.md#arc-llm) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](SWE.5-integration-testing.md#vm-integration-external) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit) | closed |
| [SWR-NFR-002](SWE.1-software-requirements.md#swr-nfr-002) | [ARC-CORE](SWE.2-architecture/software-architecture.md#arc-core)、[ARC-ADVICE](SWE.2-architecture/software-architecture.md#arc-advice)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression) | closed |
| [SWR-NFR-003](SWE.1-software-requirements.md#swr-nfr-003) | [ARC-TOOLS](SWE.2-architecture/software-architecture.md#arc-tools) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace)、[VM-STATIC](SWE.6-validation-testing.md#vm-static) | [VM-UNIT](SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](SWE.6-validation-testing.md#vm-regression)、[VM-DOCS](SWE.6-validation-testing.md#vm-docs)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace)、[VM-STATIC](SWE.6-validation-testing.md#vm-static) | closed |
| [SWR-NFR-004](SWE.1-software-requirements.md#swr-nfr-004) | [ARC-TOOLS](SWE.2-architecture/software-architecture.md#arc-tools)、[ARC-RUN](SWE.2-architecture/software-architecture.md#arc-run) | [VM-CONFIG](SWE.6-validation-testing.md#vm-config)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace) | [VM-CONFIG](SWE.6-validation-testing.md#vm-config)、[VM-TRACE](SWE.6-validation-testing.md#vm-trace) | closed |

## 最新结果

详见 [软件域验证结果](./records/verification/latest.md)。
