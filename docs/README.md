# GoldAnalysisAI 文档中心

项目文档按用途分目录存放。测试说明见 [`tests/README.md`](../tests/README.md)。

---

## 目录结构

```
docs/
├── getting-started/     # 入门：心智模型、环境、界面动线
├── reference/           # 参考：手册、术语、速查、流水线步骤
├── design/              # 设计：架构、LLM、分析师输入
├── domain/              # 领域：算法反推、金融评审
├── integrations/        # 集成：外部数据源
└── examples/            # 报告 JSON 样例与字段说明
```

---

## 按角色阅读

| 角色 | 建议路径 |
|------|----------|
| **新用户** | [README.md](../README.md) → [getting-started/setup.md](./getting-started/setup.md) |
| **开发者（首次读代码）** | **[getting-started/onboarding.md](./getting-started/onboarding.md)** → `orchestrator.py` → [reference/cheat-sheet.md](./reference/cheat-sheet.md) |
| **开发者（查参考）** | [reference/handbook.md](./reference/handbook.md) · [reference/glossary.md](./reference/glossary.md) · [examples/report-schema.md](./examples/report-schema.md) |
| **数据 / 集成** | [integrations/jin10-mcp.md](./integrations/jin10-mcp.md) → [design/analyst-context.md](./design/analyst-context.md) |
| **测试 / 质量** | [tests/README.md](../tests/README.md) → [domain/financial-review.md](./domain/financial-review.md) |
| **产品 / 界面** | [getting-started/walkthrough.md](./getting-started/walkthrough.md) → [domain/reverse-engineering.md](./domain/reverse-engineering.md) |

---

## 文档索引

### getting-started — 入门

| 文档 | 说明 |
|------|------|
| **[onboarding.md](./getting-started/onboarding.md)** | 15 分钟心智模型、读码路线、刷新报告步骤表 |
| [setup.md](./getting-started/setup.md) | 环境搭建、配置、运行与测试 |
| [walkthrough.md](./getting-started/walkthrough.md) | 界面三页操作动线、流程图、验证清单 |

### reference — 参考

| 文档 | 说明 |
|------|------|
| [handbook.md](./reference/handbook.md) | 完整数据流、模块说明、调试与常见问题 |
| [glossary.md](./reference/glossary.md) | 术语表：ICT、分析师团队、混合模式、胜率字段等 |
| [cheat-sheet.md](./reference/cheat-sheet.md) | 改功能 → 文件 → 测试，一页速查 |
| [pipeline-steps.yaml](./reference/pipeline-steps.yaml) | 流水线步骤权威列表（与代码 CI 同步） |

### design — 架构与设计

| 文档 | 说明 |
|------|------|
| [architecture.md](./design/architecture.md) | 与 TradingAgents 对照、分层数据流 |
| [llm-agents.md](./design/llm-agents.md) | 大模型双轨调度、审计字段 |
| [analyst-context.md](./design/analyst-context.md) | 分析师团队输入密度 |

### domain — 领域参考

| 文档 | 说明 |
|------|------|
| [reverse-engineering.md](./domain/reverse-engineering.md) | 报告各区块算法反推 |
| [financial-review.md](./domain/financial-review.md) | 金融逻辑评审 F-001～F-014、**§7 修复路径** |
| [financial-review-run-2026-06-20.md](./domain/financial-review-run-2026-06-20.md) | 实跑评审快照 |

### integrations — 外部集成

| 文档 | 说明 |
|------|------|
| [jin10-mcp.md](./integrations/jin10-mcp.md) | 金十 MCP 接入 |

### examples — 样例

| 文档 | 说明 |
|------|------|
| [report-schema.md](./examples/report-schema.md) | 报告 JSON 字段说明 |
| [sample-report.json](./examples/sample-report.json) | 脱敏样例（`scripts/export_sample_report.py` 生成） |

---

## 文档关系

```
README.md（快速开始）
    │
    ├── getting-started/onboarding.md ──► walkthrough.md（界面动线）
    │         │
    │         ├── reference/cheat-sheet.md ◄── pipeline-steps.yaml（CI 同步）
    │         ├── reference/glossary.md（术语）
    │         └── examples/（报告 JSON 样例）
    │
    ├── getting-started/setup.md（环境搭建）
    │         └── reference/handbook.md（详细参考）
    │
    ├── design/architecture.md ──► llm-agents.md
    └── domain/financial-review.md
```

---

## 维护约定

1. **新增流水线步骤**：同时修改 `orchestrator.py` / `fetch_pipeline.py`、`reference/pipeline-steps.yaml`、上手指南中的步骤表；运行 `pytest tests/regression/test_doc_pipeline_sync.py`。
2. **修改报告字段**：更新 `examples/report-schema.md`，并运行 `python scripts/export_sample_report.py`。
3. **新增术语**：写入 `reference/glossary.md`。
4. **修改界面动线**：同步 `getting-started/walkthrough.md`。
5. **金融修复**：合并 Phase 1–3 相关改动后须跑 `coherence_check.py`（零 issue）与 `python tests/run.py --financial`；修复路径见 [domain/financial-review.md §7](./domain/financial-review.md#7-修复路径规划2026-06-20)。
6. **持续集成**：`.github/workflows/docs.yml` 自动校验文档与代码一致。

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
