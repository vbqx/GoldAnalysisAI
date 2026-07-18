# ASPICE 过程文档索引

本文件由 `python scripts/check_aspice_assets.py --write` 生成。人工评审以 `../README.md` 导航的 Markdown 主文档为准；完整机器注册表位于 `../_machine/document-register.csv`。

## MAN.3/MAN.5

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [交易分析系统持续审核蓝图](../../planning/audit-plan.md) | Project/Risk Plan | reviewed | supporting |
| [GoldAnalysisAI 路线图](../../planning/roadmap.md) | Project/Risk Plan | reviewed | supporting |

## SUP.1/SUP.9

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [Automotive SPICE 软件域关闭审核报告](./reviews/software-domain-closure-review-2026-07-18.md) | Review/Problem Analysis Evidence | reviewed | supporting |
| [Automotive SPICE 4.0 软件域文档审核报告](./reviews/software-domain-document-audit-2026-07-17.md) | Review/Problem Analysis Evidence | reviewed | supporting |
| [software function audit 2026 07 17](./reviews/software-function-audit-2026-07-17.csv) | Review/Problem Analysis Evidence | reviewed | supporting |
| [software function audit summary 2026 07 17](./reviews/software-function-audit-summary-2026-07-17.json) | Review/Problem Analysis Evidence | reviewed | supporting |
| [金融评审 · 实跑结论（2026-06-20）](../../reviews/financial/runtime-review-2026-06-20.md) | Review/Problem Analysis Evidence | reviewed | supporting |
| [GoldAnalysisAI 金融实现 Review 报告](../../reviews/financial/static-code-review.md) | Review/Problem Analysis Evidence | reviewed | supporting |
| [评审发现项 · 完成状态登记](../../reviews/findings-status.md) | Review/Problem Analysis Evidence | reviewed | supporting |
| [GUI 验收快照：2026-07-08](../../reviews/gui/streamlit-acceptance-2026-07-08.md) | Review/Problem Analysis Evidence | reviewed | supporting |
| [评审文档索引](../../reviews/README.md) | Review/Problem Analysis Evidence | reviewed | supporting |

## SUP.8

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [Instructions for AI Agents & Automation](../../../AGENTS.md) | Document/Automation Guidance | reviewed | supporting |
| [已迁移](../../archive/domain/financial-review-run-2026-06-20.md) | Historical Record | historical | historical |
| [已迁移](../../archive/domain/financial-review.md) | Historical Record | historical | historical |
| [群友黄金分析报告 — 实现反推](../../archive/domain/reverse-engineering.md) | Historical Record | historical | historical |
| [已迁移](../../archive/gui-acceptance-2026-07-08.md) | Historical Record | historical | historical |
| [Archive](../../archive/README.md) | Historical Record | historical | historical |
| [configuration management](../_machine/configuration-management.yaml) | Configuration Item/Baseline | agreed | normative |
| [dependency lock](../_machine/dependency-lock.txt) | Configuration Item/Baseline | agreed | normative |
| [document register](../_machine/document-register.csv) | Configuration Status Record | generated | generated |
| [pip resolution](../_machine/pip-resolution.json) | Configuration Item/Baseline | agreed | normative |
| [sbom](../_machine/sbom.json) | Configuration Item/Baseline | agreed | normative |
| [SUP.8 软件配置管理](../SUP.8-configuration-management.md) | Configuration Status/Baseline | agreed | normative |
| [文档体系与 ASPICE 过程归属](./document-architecture.md) | Document Control | agreed | normative |
| [ASPICE 文档控制与归类规则](./document-control.md) | Document Control | agreed | normative |
| [ASPICE 过程文档索引](./process-document-index.md) | Configuration Status Record | generated | generated |
| [GoldAnalysisAI 文档中心](../../README.md) | Document/Automation Guidance | reviewed | supporting |

## SUP.8/MAN.3

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [cursor mcp.json](../../operations/integrations/cursor-mcp.json.example) | Operation/Configuration Guidance | reviewed | supporting |
| [金十数据 MCP 接入](../../operations/integrations/jin10-mcp.md) | Operation/Configuration Guidance | reviewed | supporting |
| [开发者上手指南](../../operations/onboarding.md) | Operation/Configuration Guidance | reviewed | supporting |
| [环境搭建与运行](../../operations/setup.md) | Operation/Configuration Guidance | reviewed | supporting |
| [界面操作动线](../../operations/walkthrough.md) | Operation/Configuration Guidance | reviewed | supporting |

## SWE.1

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [software requirements](../_machine/software-requirements.yaml) | Machine-readable Requirement Mirror | generated | generated |
| [SWE.1 软件需求分析](../SWE.1-software-requirements.md) | 17-00 Software Requirements | agreed | normative |
| [Codex 自动优化目标模板](../../overview/codex-autonomy.md) | Stakeholder/Software Context | reviewed | supporting |
| [Project Overview](../../overview/project.md) | Stakeholder/Software Context | reviewed | supporting |
| [Current Status](../../overview/status.md) | Stakeholder/Software Context | reviewed | supporting |
| [GoldAnalysisAI — XAUUSD PA+ICT 分析报告](../../../README.md) | Stakeholder/Software Context | reviewed | supporting |

## SWE.1-SWE.6

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [traceability matrix](../_machine/traceability-matrix.csv) | 13-51 Consistency Evidence | generated | generated |
| [Automotive SPICE 软件域](../README.md) | Software Domain Navigation | agreed | normative |
| [ASPICE 软件域范围与关闭准则](./software-domain-scope-and-closure.md) | 15-52 Evaluation Results | agreed | normative |
| [软件双向追溯](../traceability.md) | 13-51 Consistency Evidence | agreed | normative |

## SWE.2

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [Analyst Team 输入密度](../../architecture/analyst-context.md) | 04-04 Software Architecture | reviewed | supporting |
| [GoldAnalysisAI 架构设计（TradingAgents 参考）](../../architecture/architecture.md) | 04-04 Software Architecture | reviewed | supporting |
| [Backtesting Design](../../architecture/backtesting.md) | 04-04 Software Architecture | reviewed | supporting |
| [主图与多周期决策分层](../../architecture/chart-layers.md) | 04-04 Software Architecture | reviewed | supporting |
| [LLM 多智能体架构](../../architecture/llm-agents.md) | 04-04 Software Architecture | reviewed | supporting |
| [报告可信度层（Report Trust）](../../architecture/report-trust.md) | 04-04 Software Architecture | reviewed | supporting |
| [Architecture Review](../../architecture/review.md) | 04-04 Software Architecture | reviewed | supporting |
| [SMC + PA 叙事组合](../../architecture/smc-pa-narrative.md) | 04-04 Software Architecture | reviewed | supporting |
| [技术分析模块架构](../../architecture/technical-analysis.md) | 04-04 Software Architecture | reviewed | supporting |
| [software architecture](../_machine/software-architecture.yaml) | Machine-readable Architecture Mirror | generated | generated |
| [SWE.2 软件架构设计](../SWE.2-software-architecture.md) | 04-04 Software Architecture | agreed | normative |

## SWE.3

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [software function detailed design](../_machine/software-function-detailed-design.csv) | 04-05 Software Detailed Design | agreed | normative |
| [software function map](../_machine/software-function-map.csv) | 04-05 Software Detailed Design | agreed | normative |
| [software unit catalog](../_machine/software-unit-catalog.csv) | 04-05 Software Detailed Design | agreed | normative |
| [关键软件单元详细设计](./key-unit-detailed-designs.md) | 04-05 Software Detailed Design | agreed | normative |
| [SWE.3 软件详细设计](../SWE.3-software-detailed-design.md) | 04-05 Software Detailed Design | agreed | normative |
| [开发者速查表](../../reference/cheat-sheet.md) | Detailed Design/Interface Reference | reviewed | supporting |
| [报告 JSON 结构说明](../../reference/examples/report-schema.md) | Detailed Design/Interface Reference | reviewed | supporting |
| [sample report](../../reference/examples/sample-report.json) | Detailed Design/Interface Reference | reviewed | supporting |
| [术语表](../../reference/glossary.md) | Detailed Design/Interface Reference | reviewed | supporting |
| [GoldAnalysisAI 开发参考手册](../../reference/handbook.md) | Detailed Design/Interface Reference | reviewed | supporting |
| [pipeline steps](../../reference/pipeline-steps.yaml) | Detailed Design/Interface Reference | reviewed | supporting |
| [Run archive replay contract](../../reference/run-archive-schema.md) | Detailed Design/Interface Reference | reviewed | supporting |

## SWE.4

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [software unit verification matrix](../_machine/software-unit-verification-matrix.csv) | 08-50 Verification Measure/Result | agreed | normative |
| [SWE.4 单元测试（UT）](../SWE.4-unit-testing.md) | 08-50 Unit Verification | agreed | normative |

## SWE.4-SWE.6

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [verification measures](../_machine/verification-measures.yaml) | 08-60/15-52 Verification | agreed | normative |
| [ASPICE 软件域验证结果](../verification-results/latest.md) | 08-60/15-52 Verification | agreed | normative |
| [software domain 2026 07 18](../verification-results/software-domain-2026-07-18.yaml) | 08-60/15-52 Verification | agreed | normative |
| [Testing Strategy](../../testing/strategy.md) | Verification Strategy/Measure | reviewed | supporting |
| [catalog](../../../tests/cases/catalog.yaml) | Verification Strategy/Measure | reviewed | supporting |
| [金融 Review 测试用例设计](../../../tests/cases/financial-review-cases.md) | Verification Strategy/Measure | reviewed | supporting |
| [测试用例目录](../../../tests/cases/README.md) | Verification Strategy/Measure | reviewed | supporting |
| [GoldAnalysisAI 测试用例设计](../../../tests/cases/test-plan.md) | Verification Strategy/Measure | reviewed | supporting |
| [GoldAnalysisAI 测试体系](../../../tests/README.md) | Verification Strategy/Measure | reviewed | supporting |

## SWE.5

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [software integration plan](../_machine/software-integration-plan.yaml) | 08-52 Integration Verification Measure | agreed | normative |
| [SWE.5 集成测试（IT）](../SWE.5-integration-testing.md) | 08-52 Integration Verification | agreed | normative |

## SWE.6

| 文档 | 信息项 | 状态 | 权威性 |
|---|---|---|---|
| [software requirement verification coverage](../_machine/software-requirement-verification-coverage.csv) | 13-51 Consistency Evidence | generated | generated |
| [SWE.6 验证测试（VT）](../SWE.6-validation-testing.md) | 08-54 Software Qualification Test | agreed | normative |
