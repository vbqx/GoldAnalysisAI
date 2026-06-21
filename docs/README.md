# GoldAnalysisAI 文档中心

文档按“先读核心，再查细节”的方式维护。新内容优先合并到现有核心文档，避免为每次迭代新增一份说明。

---

## 核心阅读路径

| 目标 | 阅读顺序 |
|------|----------|
| 快速跑起来 | [../README.md](../README.md) -> [getting-started/setup.md](./getting-started/setup.md) |
| 第一次读代码 | [getting-started/onboarding.md](./getting-started/onboarding.md) -> [reference/cheat-sheet.md](./reference/cheat-sheet.md) |
| 理解架构 | [design/architecture.md](./design/architecture.md) -> [design/llm-agents.md](./design/llm-agents.md) |
| 查看后续计划 | [planning/roadmap.md](./planning/roadmap.md) |
| 理解金融可信度 | [domain/financial-review.md](./domain/financial-review.md) |
| 查接口和字段 | [reference/handbook.md](./reference/handbook.md) -> [examples/report-schema.md](./examples/report-schema.md) |
| 查测试策略 | [../tests/README.md](../tests/README.md) -> [../tests/cases/README.md](../tests/cases/README.md) |

---

## 权威文档分工

| 文档 | 维护边界 |
|------|----------|
| [design/architecture.md](./design/architecture.md) | 稳定架构事实：系统分层、agent 链路、执行层和代码边界 |
| [design/llm-agents.md](./design/llm-agents.md) | LLM 双轨、prompt/payload、阶段开关和审计字段 |
| [design/analyst-context.md](./design/analyst-context.md) | 分析师输入密度、technical context、上下文字段来源 |
| [domain/financial-review.md](./domain/financial-review.md) | 金融风险发现、修复路径和验收记录 |
| [planning/roadmap.md](./planning/roadmap.md) | 后续迭代、优先级、专项计划和完成定义 |
| [reference/handbook.md](./reference/handbook.md) | 详细开发手册：调用链、模块说明、调试和扩展方法 |
| [reference/pipeline-steps.yaml](./reference/pipeline-steps.yaml) | 流水线步骤的机器可校验清单 |

同一主题只维护一个权威位置：

- 架构事实放 `design/architecture.md`。
- LLM 行为放 `design/llm-agents.md`。
- 金融可信度和验收放 `domain/financial-review.md`。
- 后续计划放 `planning/roadmap.md`。
- 代码调用细节放 `reference/handbook.md`。

---

## 参考与归档

| 目录 | 内容 |
|------|------|
| `getting-started/` | 入门、环境搭建、界面动线 |
| `reference/` | 手册、术语、速查、流水线 YAML |
| `domain/` | 金融评审、实跑快照、报告算法反推 |
| `planning/` | 路线图、优先级、专项任务 |
| `integrations/` | 外部数据源接入说明 |
| `examples/` | 报告 schema 和样例 JSON |

`domain/financial-review-run-2026-06-20.md` 是一次实跑快照，作为审计记录保留，不作为当前架构事实源。

---

## 维护约定

1. 新增流水线步骤：同步 `orchestrator.py` / `fetch_pipeline.py`、`reference/pipeline-steps.yaml`，并运行 `pytest tests/regression/test_doc_pipeline_sync.py`。
2. 修改报告字段：更新 `examples/report-schema.md`，必要时重新生成 `examples/sample-report.json`。
3. 修改 agent 或 LLM 阶段：已实现的稳定链路更新 `design/architecture.md` 或 `design/llm-agents.md`；未实现计划更新 `planning/roadmap.md`。
4. 修改金融交易逻辑：更新 `domain/financial-review.md` 的发现项或验收记录；后续批次更新 `planning/roadmap.md`，并跑 `tests/unit` 与 coherence 检查。
5. 读取中文文档作为补丁上下文时，使用 `python scripts/show_utf8.py <path> --start N --count M`，避免未初始化 PowerShell 编码导致上下文乱码。

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
