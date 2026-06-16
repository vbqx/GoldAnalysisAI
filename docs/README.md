# GoldAnalysisAI 文档中心

本目录集中存放项目设计与开发文档。测试说明见 [`tests/README.md`](../tests/README.md)。

---

## 按角色阅读

| 角色 | 建议路径 |
|------|----------|
| **新用户** | [README.md](../README.md) → [development.md §2](./development.md#2-环境搭建) |
| **开发者（首次读代码）** | **[developer-onboarding.md](./developer-onboarding.md)** → `orchestrator.py` → [cheat-sheet.md](./cheat-sheet.md) |
| **开发者（查参考）** | [development-reference.md](./development-reference.md) · [glossary.md](./glossary.md) · [examples/report-schema.md](./examples/report-schema.md) |
| **数据 / 集成** | [jin10-mcp.md](./jin10-mcp.md) → [analyst-context.md](./analyst-context.md) |
| **测试 / 质量** | [tests/README.md](../tests/README.md) → [financial-review.md](./financial-review.md) |
| **产品 / 界面** | [walkthrough.md](./walkthrough.md) → [reverse-engineering.md](./reverse-engineering.md) |

---

## 文档索引

### 教程层（优先阅读）

| 文档 | 说明 |
|------|------|
| [README.md](../README.md) | 项目简介、快速开始 |
| **[developer-onboarding.md](./developer-onboarding.md)** | 15 分钟心智模型、读码路线、刷新报告步骤表 |
| **[walkthrough.md](./walkthrough.md)** | 界面三页操作动线、流程图、验证清单 |

### 参考层

| 文档 | 说明 |
|------|------|
| [development.md](./development.md) | 开发入口：环境搭建 + 分册导航 |
| [development-reference.md](./development-reference.md) | 完整数据流、模块说明、调试与常见问题（600+ 行） |
| **[glossary.md](./glossary.md)** | 术语表：ICT、分析师团队、混合模式、胜率字段等 |
| **[examples/report-schema.md](./examples/report-schema.md)** | 报告 JSON 字段说明 |
| **[examples/sample-report.json](./examples/sample-report.json)** | 脱敏样例（`scripts/export_sample_report.py` 生成） |

### 架构与设计

| 文档 | 说明 |
|------|------|
| [architecture.md](./architecture.md) | 与 TradingAgents 对照、分层数据流 |
| [llm-agents.md](./llm-agents.md) | 大模型双轨调度、审计字段 |
| [analyst-context.md](./analyst-context.md) | 分析师团队输入密度 |
| [jin10-mcp.md](./jin10-mcp.md) | 金十 MCP 接入 |

### 速查与同步

| 文档 | 说明 |
|------|------|
| **[cheat-sheet.md](./cheat-sheet.md)** | 改功能 → 文件 → 测试，一页速查 |
| **[pipeline-steps.yaml](./pipeline-steps.yaml)** | 流水线步骤权威列表（与代码 CI 同步） |

### 领域参考

| 文档 | 说明 |
|------|------|
| [reverse-engineering.md](./reverse-engineering.md) | 报告各区块算法反推 |
| [financial-review.md](./financial-review.md) | 金融逻辑评审 F-001～F-012 |

### 测试

| 文档 | 说明 |
|------|------|
| [tests/README.md](../tests/README.md) | 测试套件与命令行 |
| [tests/cases/catalog.yaml](../tests/cases/catalog.yaml) | 用例目录 |

---

## 文档关系

```
README.md（快速开始）
    │
    ├── developer-onboarding.md ──► walkthrough.md（界面动线）
    │         │
    │         ├── cheat-sheet.md ◄── pipeline-steps.yaml（CI 同步）
    │         ├── glossary.md（术语）
    │         └── examples/（报告 JSON 样例）
    │
    ├── development.md（开发入口）
    │         └── development-reference.md（详细参考）
    │
    ├── architecture.md ──► llm-agents.md
    └── financial-review.md
```

---

## 维护约定

1. **新增流水线步骤**：同时修改 `orchestrator.py` / `fetch_pipeline.py`、`pipeline-steps.yaml`、上手指南中的步骤表；运行 `pytest tests/regression/test_doc_pipeline_sync.py`。
2. **修改报告字段**：更新 `examples/report-schema.md`，并运行 `python scripts/export_sample_report.py`。
3. **新增术语**：写入 `glossary.md`。
4. **修改界面动线**：同步 `walkthrough.md`。
5. **持续集成**：`.github/workflows/docs.yml` 自动校验文档与代码一致。

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
