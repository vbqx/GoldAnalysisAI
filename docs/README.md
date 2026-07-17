# GoldAnalysisAI 文档中心

这套文档按“先理解项目，再查实现细节，再看历史记录”组织。每类信息只维护一个权威位置，避免计划、架构、测试、历史验收混在同一份文档里。

## Owner 阅读路径

| 你想知道 | 先读 |
|----------|------|
| 项目现在是什么状态 | [overview/project.md](./overview/project.md) -> [overview/status.md](./overview/status.md) |
| 怎么本机运行、配置、连接 MT5 | [operations/setup.md](./operations/setup.md) · 启动用 [AGENTS.md](../AGENTS.md) |
| 整体架构是否清楚 | [architecture/architecture.md](./architecture/architecture.md) -> [architecture/report-trust.md](./architecture/report-trust.md) · [architecture/technical-analysis.md](./architecture/technical-analysis.md) · [architecture/smc-pa-narrative.md](./architecture/smc-pa-narrative.md) · [architecture/review.md](./architecture/review.md) · [chart-layers.md](./architecture/chart-layers.md) |
| LLM 多智能体怎么工作 | [architecture/llm-agents.md](./architecture/llm-agents.md) |
| 回测和执行边界 | [architecture/backtesting.md](./architecture/backtesting.md) -> [architecture/review.md](./architecture/review.md) |
| 日常怎么测 | [testing/strategy.md](./testing/strategy.md) |
| 评审与验收（含完成状态） | [reviews/README.md](./reviews/README.md) -> [reviews/findings-status.md](./reviews/findings-status.md) |
| ASPICE 软件工程基线与全部文档归类 | [aspice/README.md](./aspice/README.md) -> [aspice/process-document-index.md](./aspice/process-document-index.md) |
| 让我持续自动优化该怎么下目标 | [overview/codex-autonomy.md](./overview/codex-autonomy.md) |

## 权威分工

| 目录 | 放什么 | 不放什么 |
|------|--------|----------|
| `overview/` | 项目定位、当前状态、 owner 决策入口、Codex 工作方式 | 代码级调用链 |
| `architecture/` | 稳定系统边界、数据流、Agent/LLM、回测、执行层、架构健康检查 | 历史验收流水账 |
| `reviews/` | 金融/GUI 评审、实跑结论、**F-* 完成状态** | 当前架构事实 |
| `operations/` | 本地/VPS/MT5/环境变量/运行手册/UI 操作 | 架构论证 |
| `testing/` | 测试分层、命令矩阵、用例维护、输出边界 | 单次测试结果 |
| `reference/` | 字段、术语、速查、样例 JSON、机器同步清单 | 计划和历史复盘 |
| `planning/` | 后续计划、优先级、验收标准 | 已完成 GUI 验收细节 |
| `archive/` | 算法反推、旧笔记；评审见 `reviews/` | 当前架构事实 |
| `aspice/` | 软件需求、架构、单元、验证、配置基线及全量文档注册 | 手工编辑生成型 CSV/索引 |

## 维护规则

1. 架构事实更新 `architecture/`，未来计划更新 `planning/roadmap.md`，评审结论更新 `reviews/` 并同步 [findings-status.md](./reviews/findings-status.md)。
2. 所有文档同时受 [ASPICE 文档控制规则](./aspice/document-control.md) 管理；新增或移动文档后运行 `python scripts/check_aspice_assets.py --write` 并提交生成的注册表与过程索引。
2. 报告字段变化更新 `reference/examples/report-schema.md`，必要时重生成 `reference/examples/sample-report.json`。
3. 流水线阶段变化同步 `reference/pipeline-steps.yaml`，并跑 `pytest tests/regression/test_doc_pipeline_sync.py`。
4. 测试策略变化更新 `testing/strategy.md` 和 `tests/cases/catalog.yaml`。
5. Codex 自动优化任务使用 [overview/codex-autonomy.md](./overview/codex-autonomy.md) 的目标模板。

## 免责声明

本项目仅供学习研究，不构成投资建议。
