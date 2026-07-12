# 评审发现项 · 完成状态登记

> 权威详述见 [financial/static-code-review.md](./financial/static-code-review.md) §4。  
> 实跑验收见 [financial/runtime-review-2026-06-20.md](./financial/runtime-review-2026-06-20.md)。

最后同步：**2026-07-12**

---

## 金融 Review（F-*）

| ID | 优先级 | 状态 | 修复批次 | 摘要 | 验收 |
|----|--------|------|----------|------|------|
| F-001 | P0 | ✅ 已完成 | — | 风控 `approved` 逻辑 | FIN-01 |
| F-002 | P1 | ✅ 已完成 | Phase 2-A | `win_rate` 误导 → 结构权重 UI | FIN-02 · FIN-UI-01 |
| F-003 | P0 | ✅ 已完成 | Phase 1-A | 激进做空 TP/SL 几何错误 | FIN-03 |
| F-004 | P1 | ✅ 已完成 | Phase 2-B | SL/TP magic number → 配置化 + R:R 封顶 | FIN-04 |
| F-005 | P1 | ✅ 已完成 | Phase 3-A | 双数据源 1d 不一致 | FIN-05 · FIN-INT-01 |
| F-006 | — | ✅ 已完成 | — | `build_conclusion` 硬编码价格/情绪错配 | FIN-06 |
| F-007 | P2 | ⏳ 待复核 | — | Fib `probability` 静态常量（伪精度） | FIN-07 |
| F-008 | P2 | ⏳ 待复核 | — | EMA610 历史不足仍展示 | IND-12 部分 |
| F-009 | P2 | ✅ 已完成 | Phase 3-B | VWAP 日切 / Volume 缺失 | FIN-09 |
| F-010 | P2 | 🟡 部分完成 | Phase 3-C | 外部 fallback UI 标签 ✅；LLM prompt 警告待后续 | FIN-10 · FIN-UI-02 |
| F-011 | P2 | ✅ 已完成 | Phase 3-D | Agent 规则链边界测试不足 | FIN-11 |
| F-012 | P3 | ⏳ 待复核 | — | 文档列名 `EMA_20` vs 代码 `EMA20` | — |
| F-013 | P0 | ✅ 已完成 | Phase 1-B | 辩论共识与结构情绪背离 | FIN-13 · coherence_check |
| F-014 | P1 | ✅ 已完成 | Phase 1-C + 2-C | 偏空时主提案仍 long / 置顶逆势 | FIN-14 · coherence_check |

**汇总**：14 项中 **10 已完成** · **1 部分完成** · **3 待复核**

---

## 修复批次（Phase 1～3）

| 批次 | 状态 | Findings | Definition of Done |
|------|------|----------|-------------------|
| Phase 1 | ✅ 已完成 | F-003, F-013, F-014 | `coherence_check` → `issues: []`；debate/trader/首卡同向 |
| Phase 2 | ✅ 已完成 | F-002, F-004, UI 披露 | 结构权重标签；R:R 免责声明 |
| Phase 3 | ✅ 已完成 | F-005, F-009, F-010, F-011 | 数据质量 + Agent 边界 + 占位标签 |
| 待复核 | ⏳ 进行中 | F-007, F-008, F-012 | 见 [roadmap.md](../planning/roadmap.md) |

---

## GUI 验收

| ID | 日期 | 状态 | 文档 |
|----|------|------|------|
| GUI-ACC-2026-07-08 | 2026-07-08 | ✅ 已完成 | [gui/streamlit-acceptance-2026-07-08.md](./gui/streamlit-acceptance-2026-07-08.md) |

检查项：四页非空白、无 Streamlit 异常、主计划不重复、外部数据审计区、决策链阶段摘要优先。

---

## 架构健康检查（非 Finding 编号）

| 文档 | 状态 | 说明 |
|------|------|------|
| [architecture/review.md](../architecture/review.md) | 🔄 持续维护 | 分层是否清晰、MT5/回测边界；非一次性验收 |

---

## 更新流程

1. 新 Finding → 写入对应评审正文 + 本表一行（状态 ⏳ 待复核）。
2. 合并修复 → 改状态为 ✅，填修复批次与 FIN-* / 单测。
3. 部分落地 → 🟡，在 roadmap 挂残余任务。
4. 同步 [tests/cases/catalog.yaml](../../tests/cases/catalog.yaml) 中 FIN-* 条目。
