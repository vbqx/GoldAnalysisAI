# 评审文档索引

本目录集中存放**有审计价值的评审、验收与实跑结论**。与「当前系统事实」分离：

| 类型 | 权威位置 |
|------|----------|
| 架构边界（持续维护） | [architecture/review.md](../architecture/review.md) |
| 当前实现与字段 | [architecture/](../architecture/) · [reference/](../reference/) |
| 后续计划 | [planning/roadmap.md](../planning/roadmap.md) |
| 算法反推笔记（非评审） | [archive/domain/reverse-engineering.md](../archive/domain/reverse-engineering.md) |

**发现项完成状态一览** → [findings-status.md](./findings-status.md)

---

## 评审清单

| 状态 | 类型 | 文档 | 日期 | 范围 | 说明 |
|------|------|------|------|------|------|
| ✅ 已完成 | 金融 · 静态代码 | [financial/static-code-review.md](./financial/static-code-review.md) | 2026-06-14 | Phase 1 MVP 全模块 | F-001～F-014 发现与修复路径；FIN-* 用例追溯 |
| ✅ 已完成 | 金融 · 实跑 | [financial/runtime-review-2026-06-20.md](./financial/runtime-review-2026-06-20.md) | 2026-06-20 | 规则模式实跑 | 基于 `financial_review_run.py` 快照；P0/P1 修复验收 |
| ✅ 已完成 | GUI · 验收 | [gui/streamlit-acceptance-2026-07-08.md](./gui/streamlit-acceptance-2026-07-08.md) | 2026-07-08 | Streamlit 四页 | 桌面/移动宽度布局与组件审计 |
| ✅ 已完成 | ASPICE · 软件域文档审核 | [aspice/software-domain-document-audit-2026-07-17.md](./aspice/software-domain-document-audit-2026-07-17.md) | 2026-07-17 | SWE.1–SWE.6 + 支持过程 | 1,013 个函数逐项证据附录；过程差距与整改提单 |
| 🔄 持续维护 | 架构 · 健康检查 | [architecture/review.md](../architecture/review.md) | — | 全栈边界 | 非历史流水账；评估模块是否臃肿、边界是否清晰 |

### 状态图例

| 标记 | 含义 |
|------|------|
| ✅ 已完成 | 评审结论已落地或验收通过；仅作历史追溯 |
| 🟡 部分完成 | 核心已修复，残余项在 roadmap 或待复核 |
| ⏳ 待复核 | 已登记发现项，尚未关闭或优先级 P3 |
| 🔄 持续维护 |  living document，随架构演进更新 |

---

## 相关测试与工具

| 资源 | 路径 |
|------|------|
| FIN-* 用例详设 | [tests/cases/financial-review-cases.md](../../tests/cases/financial-review-cases.md) |
| 用例目录 | [tests/cases/catalog.yaml](../../tests/cases/catalog.yaml) |
| 规则模式一致性 | `python tests/tools/coherence_check.py` |
| 金融实跑快照 | `python tests/tools/financial_review_run.py` → `tests/reports/financial_review_snapshot.json` |
| 金融单测 | `pytest tests/unit/test_financial_review.py -m financial` |
| ASPICE 函数级附录 | [aspice/software-function-audit-2026-07-17.csv](./aspice/software-function-audit-2026-07-17.csv) |

---

## 维护规则

1. **新评审**放入 `reviews/<类型>/`，文件名建议 `YYYY-MM-DD-<主题>.md`。
2. 在本表与 [findings-status.md](./findings-status.md) 登记**完成状态**；勿把发现项只写在 roadmap 或 architecture 正文里。
3. 修复关闭后更新发现项状态，并在对应评审文档 § 修复批次中打勾。
4. `docs/archive/` 仅保留非评审历史（如 reverse-engineering）；评审材料不再放入 archive。
