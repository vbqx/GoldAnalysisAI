# GoldAnalysisAI 文档中心

本目录集中存放项目设计与开发文档。测试相关说明见 [`tests/README.md`](../tests/README.md)。

---

## 按角色阅读

| 角色 | 建议路径 |
|------|----------|
| **新用户** | [README.md](../README.md) → [development.md §2](./development.md#2-环境搭建) |
| **开发者（首次读代码）** | **[developer-onboarding.md](./developer-onboarding.md)** → `orchestrator.py` → [development.md](./development.md) |
| **开发者（查参考）** | [development.md](./development.md) → [architecture.md](./architecture.md) → [llm-agents.md](./llm-agents.md) |
| **数据 / 集成** | [jin10-mcp.md](./jin10-mcp.md) → [analyst-context.md](./analyst-context.md) |
| **测试 / QA** | [tests/README.md](../tests/README.md) → [financial-review.md](./financial-review.md) → [tests/cases/catalog.yaml](../tests/cases/catalog.yaml) |
| **产品 / 评审** | [reverse-engineering.md](./reverse-engineering.md) → [financial-review.md](./financial-review.md) |

---

## 文档索引

### 入门

| 文档 | 说明 |
|------|------|
| [README.md](../README.md) | 项目简介、快速开始、能力一览、LLM 配置示例 |
| **[developer-onboarding.md](./developer-onboarding.md)** | **开发者上手指南：心智模型、读码路线、改功能速查** |
| [development.md](./development.md) | 开发参考手册：环境、完整数据流、模块职责、扩展与调试 |

### 架构与设计

| 文档 | 说明 |
|------|------|
| [architecture.md](./architecture.md) | TradingAgents 对照、Analyst Team、分层数据流、目录结构 |
| [llm-agents.md](./llm-agents.md) | LLM 双轨调度、分阶段开关、传输重试、审计字段 |
| [analyst-context.md](./analyst-context.md) | Analyst Team 三层信息架构、配置上限、可观测性 |

### 数据源与集成

| 文档 | 说明 |
|------|------|
| [jin10-mcp.md](./jin10-mcp.md) | 金十 MCP 接入（快讯 / 资讯 / 日历 / quote / kline） |

### 领域参考

| 文档 | 说明 |
|------|------|
| [reverse-engineering.md](./reverse-engineering.md) | 报告各区块算法反推与 MVP 映射 |
| [financial-review.md](./financial-review.md) | 金融逻辑评审报告（Finding F-001～F-012） |

### 测试

| 文档 | 说明 |
|------|------|
| [tests/README.md](../tests/README.md) | 测试套件、CLI 命令、测试面板 |
| [tests/cases/README.md](../tests/cases/README.md) | 用例 ID 规则与维护流程 |
| [tests/cases/test-plan.md](../tests/cases/test-plan.md) | 分层测试设计 |
| [tests/cases/financial-review-cases.md](../tests/cases/financial-review-cases.md) | FIN-* 用例详设 |
| [tests/cases/catalog.yaml](../tests/cases/catalog.yaml) | 用例目录（ID、优先级、自动化状态） |

### 脚本

| 文档 | 说明 |
|------|------|
| [scripts/README.md](../scripts/README.md) | 旧脚本迁移对照（新测试一律放 `tests/`） |

---

## 文档关系

```
README.md（快速开始）
    │
    ├── developer-onboarding.md（开发者 15 分钟入门）
    │
    ├── development.md ──────► architecture.md
    │         │                      │
    │         │                      └── llm-agents.md
    │         │
    │         ├── analyst-context.md ◄── jin10-mcp.md
    │         │
    │         └── reverse-engineering.md
    │
    ├── financial-review.md ──► tests/cases/financial-review-cases.md
    │
    └── tests/README.md ──────► tests/cases/*
```

---

## 维护约定

1. **对外接口**（`run_analysis()` 返回值）变更时，同步更新 `development.md` 与 `architecture.md`。
2. **新增数据源**时，更新 `jin10-mcp.md` 或 `development.md` §5.2，并在 `analyst-context.md` 补充配置项。
3. **新增 LLM 阶段**时，更新 `llm-agents.md` 路线图与 `architecture.md` 对照表。
4. **金融逻辑变更**时，在 `financial-review.md` 追加 Finding 或在修订记录中标注已修复项。
5. **新增测试用例**时，在 `tests/cases/catalog.yaml` 登记，并在 `test-plan.md` 补充场景。

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
