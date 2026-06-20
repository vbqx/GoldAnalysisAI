# 金融评审 · 实跑结论（2026-06-20）

**评审类型**：基于真实流水线输出的运行时评审  
**行情快照**：OANDA:XAUUSD · 现价 **4155.40** · 日涨跌 **-1.27%**  
**运行模式**：规则引擎（`AGENT_MODE=rule`，`apply_run_config` 显式关闭 LLM）  
**数据来源**：`tests/tools/financial_review_run.py` → `tests/reports/financial_review_snapshot.json`  
**对照**：同日 hybrid+LLM 集成测试日志（`tests/integration/test_pipeline.py` 第 5 项）

---

## 1. 执行摘要

| 维度 | 评级 | 实跑结论 |
|------|------|----------|
| 数据与现价 | 🟢 | `metrics.current_price` 与 5m Close **完全一致**（4155.405） |
| 结构识别 | 🟢 | 多周期趋势与 ICT 输出自洽；1d/15m/5m 偏空，1h 偏多，4h 震荡 |
| 结论层（报告文案） | 🟢 | 「弱势偏空」与结构情绪 **45% bearish** 一致 |
| 辩论 / 交易链（规则） | 🔴 | 辩论 **bullish** → 交易员 **long** → 与结论 **反向** |
| 辩论 / 交易链（LLM） | 🟢 | 辩论 **bearish** → 交易员 **short** → 与结论 **同向** |
| 信号几何 | 🔴 | 「激进反抽做空」TP1 **高于** 入场，R:R 显示 **N/A** |
| 风控 / 经理 | 🟡 | 三档均 `approved=True`；经理 `reduce` 执行扫低做多，与主策略文案冲突 |
| 路径推演 | 🟢 | 主路径偏空（反弹 FVG → 新低），与结论一致；图表轴对齐已修复 |

**总体结论（规则模式）**：报告**读上去偏空、执行层偏多**，存在「文案与决策链脱节」的 P0 级金融风险。  
**总体结论（hybrid+LLM）**：同行情下决策链与结论**方向一致**，可作为规则模式的参照基线。

---

## 2. 市场上下文（实跑）

### 2.1 价格与结构

| 字段 | 值 |
|------|-----|
| 现价 / 5m Close | 4155.405 |
| 日高 / 日低 | 4210.69 / 4121.96 |
| Swing High / Low | 4595.33 / 4023.87 |
| 结构情绪 | 多 25% / **空 45%** / 震荡 30% |

| 周期 | 趋势 |
|------|------|
| 1d | bearish |
| 4h | ranging |
| 1h | bullish |
| 15m | bearish |
| 5m | bearish |

**解读**：大周期（1d）与执行周期（5m/15m）偏空，1h 逆势反弹——符合「大空小反弹」典型场景；结论层「主方向偏空，当前处于逆势反弹阶段」**金融语义正确**。

### 2.2 Analyst Team（规则）

| 分析师 | bias | 置信度 | 要点 |
|--------|------|--------|------|
| technical | **bearish** | 23% | 结构 bearish；RSI/MACD 多周期偏空；上方 1h OB 4155–4178 距现价 -0.28% |
| fundamentals | bullish | 53% | US10Y 下行支撑黄金；DXY 中性 |
| news | bullish | 57% | 地缘快讯 + 机构看多标题（新闻 bias 规则偏乐观） |
| sentiment | **bearish** | 55% | 结构投票 45% 空；社媒 delta 略偏多 |

技术与情绪分析师偏空，基本面/新闻偏多——**四分法本身合理**，不应单独作为缺陷。

---

## 3. 决策链追踪（规则模式 · 核心问题）

### 3.1 多空研究 → 辩论计分

| 项 | 看多 | 看空 |
|----|------|------|
| 证据条数 | 40 | 39 |
| 研究员置信度 | 26.1% | 22.5% |
| 加权分 `conf × items` | **10.44** | 8.78 |
| 结构情绪加成 `pct/100` | +0.25 | +0.45 |
| **合计** | **10.69** | 9.23 |

辩论公式（`src/agents/debate.py`）：

```
combined_bull = bull_score + bull_pct/100
combined_bear = bear_score + bear_pct/100
差值 10.69 - 9.23 = 1.46 > 0.15 → consensus_bias = bullish
```

**金融评判**：

- 结构情绪明确偏空（45% > 25%），但看多研究因 **条数多 1 条 × 略高置信** 压过看空。
- `bear_pct/100` 仅 +0.45 的加成，无法抵消 40 条证据的累积权重。
- 结果：辩论 **bullish (54%)**，与 sentiment 主导方向 **相反**。

### 3.2 各层输出对照

| 层级 | 输出 | 与「偏空主策略」一致？ |
|------|------|-------------------------|
| `build_conclusion` | 弱势偏空 ↓；等待 4150 阻力区做空 | ✅ |
| `sentiment_score` | 45% bearish | ✅ |
| `run_debate` | consensus **bullish** | ❌ |
| `run_trader_agent` | primary **long**，选中信号 index **2**（右侧扫低做多） | ❌ |
| `run_manager` | action **reduce**，confidence 0.55 | ⚠️ 缩减仓位但仍做多 |
| 交易计划首卡（经理重排后） | **右侧扫低做多** 置顶 | ❌ vs 结论「不追多」 |

**用户可见矛盾**：

1. 顶栏 / 结论：**偏空，等反弹做空**
2. 交易计划主信号：**扫低做多**（逆势轻仓）
3. 辩论面板：**共识看多**

从交易纪律角度，这属于 **主策略与执行建议冲突**——用户若只看交易计划，可能违背结论层的「不追多」。

### 3.3 hybrid+LLM 对照（同价 4155.40）

| 层级 | LLM 实跑 |
|------|----------|
| 研究 | 看多 20 条@18% vs 看空 9 条@**75%** |
| 辩论 | **bearish**，强度 0.70–0.82 |
| 交易员 | **short**，选中做空信号 [0,1,2] |
| 经理 | reduce · short |

LLM 辩论更重视**看空证据质量**而非条数，输出与结论同向。  
**金融含义**：当前规则辩论计分对「条数 × 低置信度」过敏感，在多空证据接近时易翻转方向。

---

## 4. 交易信号评审（实跑三条）

生成顺序（重排前 index）：`0=激进做空, 1=保守做空, 2=扫低做多`。

### 4.1 激进反抽做空 — 🔴 几何无效

| 字段 | 值 |
|------|-----|
| 入场 | 4149.76 – 4149.90（mid **4149.83**） |
| 止损 | 4149.96（仅高于入场 **0.13 点**） |
| TP1 / TP2 / TP3 | **4163.67** / 4063.33 / 4023.87 |
| R:R | **N/A** |

**问题**：

1. **TP1 4163.67 > 入场 mid** — 做空止盈在入场上方，不可执行。
2. 根因：`tp1 = price - (entry_high - price) * 1.5`；当 FVG 区在现价下方时 `(entry_high - price) < 0`，TP 被算到上方。
3. SL 几乎贴在入场区上沿，风险距离 ≈ 0.13 点，**不具备实际风控意义**。

**关联 Finding**：F-003（已登记）

### 4.2 保守反抽做空 — 🟢 几何有效

| 字段 | 值 |
|------|-----|
| 入场 | 4177.10 – 4183.76（mid 4180.43，**高于现价**） |
| 止损 | 4190.41 |
| TP1 | 4167.12（低于入场） |
| R:R | 1:1.3 |

符合「反弹至 1h OB 阻力做空」逻辑，与结论 action 一致。  
**未被交易员选为主信号**（规则模式下交易员因辩论 bullish 选了做多）。

### 4.3 右侧扫低做多 — 🟡 几何有效但战略位置矛盾

| 字段 | 值 |
|------|-----|
| 入场 | 4018.87 – 4023.87（mid 4021.37，**远低于现价 4155**） |
| 止损 | 4014.87 |
| TP1 | 4155.40（= 现价） |
| R:R | 1:20.6 |

几何上 BUY 方向正确，但：

- 入场区距现价 **~133 点**，属于远端限价，非当前可执行区。
- R:R 1:20.6 因 SL 距离极小而被放大，**误导性强**。
- 结论写「不追多」，经理却以 `reduce` 将其置顶 — **战略叙事冲突**。

**关联 Finding**：F-004（magic number：sweep_low = swing_low - 5，SL = swing_low - 9）

---

## 5. 路径推演与主图（实跑）

| 路径 | 概率 | 终点倾向 |
|------|------|----------|
| 主路径（反弹后回落） | 45% | 3966.72（新低） |
| 次路径（更深反弹） | 25% | 测试 OB 4377 → 回落 4023 |
| 极端路径（直接破位） | 30% | 4008.87 |

主路径与 **45% bearish** 情绪权重一致；5m 主图虚线已与 K 线同轴（`test_chart_projections.py` 通过）。  
**注意**：路径为 swing 级宏观示意，非 5m 逐 bar 预测——产品披露层面应维持「推演非预测」表述。

---

## 6. 风控与经理（实跑 · 规则）

| 档位 | approved | scale | 允许信号 |
|------|----------|-------|----------|
| aggressive | true | 1.0 | [2] 扫低做多 |
| neutral | true | 0.7 | [2] |
| conservative | true | 0.4 | [2] |

- `debate_bias=bullish`（非 neutral）→ 三档均通过（`risk.py` L40–46 逻辑**实跑符合代码**）。
- 经理取保守档 → `reduce`，仅保留 index 2（扫低做多）。

**F-001 状态更新**：原评审记录的 `approved` 布尔恒真 bug **已在当前代码修复**（`neutral` 共识时 `approved=False`）。本次偏空主导但辩论 bullish 的场景下，风控**未起到方向过滤作用**——问题已转移至 **F-013 辩论计分**。

---

## 7. 指标与数据（实跑）

| 检查项 | 结果 |
|--------|------|
| IND-01 现价 vs 5m | ✅ diff = 0 |
| 指标校验列 | ✅ 含 RSI14/MACD/ADX14/ATR14 |
| 外部源 | ✅ jin10 + DXY + US10Y live |
| EMA610（5m） | 数据充足（5000 bars） |

未发现新的数据层 P0 问题。

---

## 8. 发现项汇总与优先级

| ID | 级别 | 状态 | 修复 Phase |
|----|------|------|------------|
| **F-003** | **P0** | ✅ 已修复 | Phase 1-A |
| **F-013** | **P0** | ✅ 已修复 | Phase 1-B |
| **F-014** | **P1** | ✅ 已修复 | Phase 1-C + 2-C |
| F-004 | P1 | ✅ 已修复 | Phase 2-B |
| F-002 | P1 | ✅ 已修复 | Phase 2-A |
| F-005 | P1 | ✅ 已修复 | Phase 3-A |
| F-009 | P2 | ✅ 已修复 | Phase 3-B |
| F-010 | P2 | 🟡 部分 | Phase 3-C（UI 标签） |
| F-011 | P2 | ✅ 已修复 | Phase 3-D |
| F-001 | — | ✅ 已修复 | — |
| F-006 | — | ✅ 已修复 | — |

---

## 14. 修复后复测（2026-06-20 Post-fix）

**运行**：`AGENT_MODE=rule`，`LLM_ENABLED=false` · 工具：`coherence_check.py` + `financial_review_run.py`

| 检查项 | 修复前 | 修复后 |
|--------|--------|--------|
| `coherence_check` issues | 2（辩论反向 + 做空几何） | **0** |
| debate.consensus_bias | bullish | **bearish** (0.47) |
| trader.primary_direction | long | **short** |
| manager.action | reduce（首卡 long） | **reduce**（首卡 **激进反抽做空**） |
| 激进反抽做空 geom_ok | false（TP1 > entry） | **true** |
| 首卡信号 theme | long（逆势） | **short**（主策略） |
| 路径/结论 vs sentiment | ✅ 同向 | ✅ 同向 |

**新增 meta 字段（Phase 3）**：`price_drift_1d`、`indicator_notes`、`warnings`（含 VWAP/Volume 提示时）。

**门禁**：`python tests/run.py --financial` 10/10 · `coherence_check.py` exit 0。

---

## 9. 修复路径（Phase 1 摘要）

完整规划见 **[financial-review.md §7](./financial-review.md#7-修复路径规划2026-06-20)**。

| 步骤 | Finding | 文件 | 目标 |
|------|---------|------|------|
| 1-A | F-003 | `report_engine.py` | 做空 TP/SL 几何正确或跳过无效信号 |
| 1-B | F-013 | `debate.py` | 辩论与结构情绪（45% 空）同向 |
| 1-C | F-014 | `trader.py`, `orchestrator.py` | 偏空时主提案 short，首卡非扫低做多 |

**门禁**：`coherence_check.py` → `"issues": []`

---

## 10. 测试与复现

```bash
# 规则模式实跑快照
$env:AGENT_MODE="rule"; $env:LLM_ENABLED="false"
python tests/tools/financial_review_run.py

# 一致性检查
python tests/tools/coherence_check.py
```

输出：

- `tests/reports/financial_review_snapshot.json`
- `tests/reports/coherence_check.json`

---

## 11. 模式选择建议

- **研究 / 演示**：优先 **hybrid+LLM**
- **CI / 回归**：规则模式 + `coherence_check.py`（Phase 1 修复后须零 issue）

---

## 免责声明

本评审基于单次行情快照与规则/LLM 对比，不构成投资建议。金价与结构随时间变化，结论仅反映 2026-06-20 14:29 (UTC+8) 运行时刻的系统行为。
