# GoldAnalysisAI 文档中心

这套文档按“先理解项目，再查实现细节，再看历史记录”组织。每类信息只维护一个权威位置，避免计划、架构、测试、历史验收混在同一份文档里。

## Owner 阅读路径

| 你想知道 | 先读 |
|----------|------|
| 项目现在是什么状态 | [overview/project.md](./overview/project.md) -> [overview/status.md](./overview/status.md) |
| 怎么本机运行、配置、连接 MT5 | [operations/setup.md](./operations/setup.md) · 启动用 [AGENTS.md](../AGENTS.md) |
| 整体架构是否清楚 | [architecture/architecture.md](./architecture/architecture.md) -> [architecture/review.md](./architecture/review.md) |
| LLM 多智能体怎么工作 | [architecture/llm-agents.md](./architecture/llm-agents.md) |
| 回测和执行边界 | [architecture/backtesting.md](./architecture/backtesting.md) -> [architecture/review.md](./architecture/review.md) |
| 日常怎么测 | [testing/strategy.md](./testing/strategy.md) |
| 让我持续自动优化该怎么下目标 | [overview/codex-autonomy.md](./overview/codex-autonomy.md) |

## 权威分工

| 目录 | 放什么 | 不放什么 |
|------|--------|----------|
| `overview/` | 项目定位、当前状态、 owner 决策入口、Codex 工作方式 | 代码级调用链 |
| `architecture/` | 稳定系统边界、数据流、Agent/LLM、回测、执行层、架构评审 | 历史验收流水账 |
| `operations/` | 本地/VPS/MT5/环境变量/运行手册/UI 操作 | 架构论证 |
| `testing/` | 测试分层、命令矩阵、用例维护、输出边界 | 单次测试结果 |
| `reference/` | 字段、术语、速查、样例 JSON、机器同步清单 | 计划和历史复盘 |
| `planning/` | 后续计划、优先级、验收标准 | 已完成 GUI 验收细节 |
| `archive/` | 历史金融评审、实跑快照、旧审计资料 | 当前架构事实 |

## 维护规则

1. 架构事实更新 `architecture/`，未来计划更新 `planning/roadmap.md`，历史记录进入 `archive/`。
2. 报告字段变化更新 `reference/examples/report-schema.md`，必要时重生成 `reference/examples/sample-report.json`。
3. 流水线阶段变化同步 `reference/pipeline-steps.yaml`，并跑 `pytest tests/regression/test_doc_pipeline_sync.py`。
4. 测试策略变化更新 `testing/strategy.md` 和 `tests/cases/catalog.yaml`。
5. Codex 自动优化任务使用 [overview/codex-autonomy.md](./overview/codex-autonomy.md) 的目标模板。

## 免责声明

本项目仅供学习研究，不构成投资建议。
