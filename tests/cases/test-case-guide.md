# 测试用例目录

本目录存放**用例定义与测试设计文档**，与 `tests/unit`、`tests/regression` 等实现代码分离。项目文档见 [`docs/documentation-center.md`](../../docs/documentation-center.md)。

| 文件 | 说明 |
|------|------|
| [test-plan.md](./test-plan.md) | 分层测试设计（UI → 指标 → 功能 → 性能 → 金融） |
| [financial-review-cases.md](./financial-review-cases.md) | **金融 Review** Finding→用例追溯（FIN-*）；状态见 [docs/aspice/records/reviews/findings-status.md](../../docs/aspice/records/reviews/findings-status.md) |
| [catalog.yaml](./catalog.yaml) | 用例 ID、优先级、套件、自动化状态、关联 Issue |

## 用例 ID 规则

| 前缀 | 层级 | 含义 |
|------|------|------|
| `UIL-*` | UI 布局 | 导航、分区、Tab、hero、CSS |
| `IND-*` | 指标显示 | 顶栏 metrics、侧边栏校验、图表、报告 JSON |
| `FN-*` | 整体功能 | 流水线、缓存、刷新、LLM、模式 |
| `PERF-*` | 性能 | 耗时阈值、缓存切换、并发 |
| `FIN-*` | 金融逻辑 | Review F-001～F-011（信号/风控/数据语义） |
| `FIN-UI-*` | 金融合规 UI | 胜率标注、占位数据、免责声明 |
| `UT-*` | — | 单元测试（快速、无网络） |
| `IT-*` | — | 集成测试（流水线、外部服务） |
| `RG-*` | — | 回归测试（Issue 修复、约定检查） |
| `UI-*` | — | **已废弃**，请用 `FN-*` / `UIL-*`；catalog 中保留映射 |

## 优先级

| 级别 | 说明 |
|------|------|
| P0 | 阻塞发布（流水线、缓存、waiting UI） |
| P1 | 核心体验（布局主区、指标、导航） |
| P2 | 重要但可延后（样式细节、LLM I/O） |
| P3 | 低优先级（页脚、单图性能） |

## 维护流程

1. 在 [test-plan.md](./test-plan.md) 补充场景与验收要点
2. 在 [catalog.yaml](./catalog.yaml) 新增条目（含 `layer`、`automated`、`maps_to`）
3. 在 `tests/<suite>/` 实现可自动化用例
4. 本地执行 `python tests/run.py` 验证
5. 关单时在 GitHub Issue 引用用例 ID（如 `UIL-41` / `IND-01`）

## 手工测试清单（发版前）

按顺序执行 catalog 中 `suite: manual` 且 `priority: P0|P1` 的 UIL / IND / FN / PERF 条目，记录于 `tests/reports/manual-YYYY-MM-DD.md`。
