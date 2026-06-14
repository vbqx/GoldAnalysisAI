# 金融 Review 测试用例设计

> 来源：[docs/financial-review.md](../../docs/financial-review.md) §6  
> 登记：[catalog.yaml](./catalog.yaml)（`FIN-*` / `FIN-UI-*`）  
> 版本：v1.0 · 2026-06-14

---

## 1. 说明

| 项 | 约定 |
|----|------|
| **用例前缀** | `FIN-*` 金融逻辑（单元/集成）；`FIN-UI-*` 合规与展示（手工） |
| **Finding 映射** | `finding: F-00N` 对应 Review 发现项编号 |
| **与 FN-* 区别** | 现有 `FN-10+` 为 Streamlit 导航/LLM 功能；本文件覆盖 **信号/风控/数据语义** |
| **MVP 边界** | Sharpe/VaR/回测/Execution **不设计用例**（Review §2 已排除） |

---

## 2. Finding → 用例追溯矩阵

| Finding | 级别 | 用例 ID | 自动化 | Sprint 建议 |
|---------|------|---------|--------|-------------|
| F-001 风控 approved 逻辑 | P0 | FIN-01 | 单元 | Sprint 1 |
| F-002 win_rate 命名误导 | P0 | FIN-02, FIN-UI-01 | 单元 + 手工 | Sprint 1 |
| F-003 risk_reward 硬编码 | P1 | FIN-03 | 单元 | Sprint 1 |
| F-004 止损 magic number | P1 | FIN-04 | 单元 | Sprint 2 |
| F-005 双源价格不一致 | P1 | FIN-05, FIN-INT-01 | 集成 | Sprint 2 |
| F-006 结论硬编码价位 | P1 | FIN-06 | 单元 | Sprint 1 |
| F-007 Fib probability 伪精度 | P2 | FIN-07, FIN-UI-01 | 单元 + 手工 | Sprint 2 |
| F-008 EMA610 不足仍展示 | P2 | FIN-08, FIN-UI-04 | 单元 + 手工 | Sprint 2 |
| F-009 VWAP/Volume | P2 | FIN-09 | 单元 | Sprint 2 |
| F-010 占位外部因子 | P2 | FIN-10, FIN-UI-02 | 单元 + 手工 | Sprint 3 |
| F-011 Agent 链边界 | P2 | FIN-11 | 单元 | Sprint 3 |
| F-012 文档列名 | P3 | — | 文档 | Backlog |
| §8 合规披露 | — | FIN-UI-05 | 手工 | Sprint 1 |

**已有覆盖（不必重复实现）：**

| Review 建议 | 已有用例 |
|-------------|----------|
| INT-01 现价 vs 5m | `IND-01` / `IT-01`（已实现） |
| INT-02 signals schema | `IT-03` / `IND-33`（已实现） |
| IND-12 EMA610 notes | `IND-12`（已实现） |

---

## 3. 单元测试用例（无网络）

### FIN-01 · 风控 approved（F-001）

**模块：** `src/agents/risk.py`  
**优先级：** P0  
**前置：** 构造 `TransactionProposal`（有 signal_indices，`debate_bias` 可变）

| 步骤 | 输入 | 期望 |
|------|------|------|
| 1 | `debate_bias=neutral`，三档各有 allowed 信号 | **修复 F-001 前**：aggressive/neutral 可能错误 `approved=True`；**修复后**：按产品定义断言（建议 conservative=False，aggressive/neutral 仅降仓或拒绝） |
| 2 | `debate_bias=bearish`，有 short 信号 | aggressive/neutral/conservative 按 profile 规则通过或缩仓 |
| 3 | `primary_direction=wait` | 三档均 `approved=False` |

```python
# 计划路径：tests/unit/test_risk.py
```

---

### FIN-02 · win_rate 语义（F-002）

**模块：** `src/analysis/report_engine.py`  
**优先级：** P0

| 验收 |
|------|
| `signals[*].win_rate` 数值等于对应 `sentiment` 分量（bearish/bullish %），**非**历史回测胜率 |
| 字段重命名后：断言新字段名存在、旧 `win_rate` 可选 deprecated |

---

### FIN-03 · risk_reward 计算（F-003）

**模块：** `report_engine.generate_trading_signals`  
**优先级：** P1

对每个 signal：

- SELL：`stop_loss > entry_mid > take_profits[0]`
- BUY：`stop_loss < entry_mid < take_profits[0]`
- 展示 `risk_reward` 与 `(TP1-entry)/(entry-SL)` 一致（容差 ±0.1）；无法计算时为 `N/A`

---

### FIN-04 · 入场/止损几何（F-004）

**模块：** `report_engine` 扫低做多模板  
**优先级：** P1

| 给定 | 期望 |
|------|------|
| `swing_low=4200` | `entry_low=4195`, `entry_high=4200`, `stop_loss=4191`（当前 magic 5/9，修复后改读配置常量） |

---

### FIN-05 · 现价与 5m 一致（F-005）

**已覆盖：** `IND-01`（集成）  
**补充：** 在 report `meta` 记录 `price_drift_1d`（独立 1d vs resample）— 见 FIN-INT-01

---

### FIN-06 · 结论无硬编码价位（F-006）

**模块：** `build_conclusion`  
**优先级：** P1

| 验收 |
|------|
| `conclusion.action` 不包含固定四位数常量（如 `4389`） |
| 无 signals 时不引用具体 entry 区间 |

---

### FIN-07 · Fibonacci probability 静态（F-007）

**模块：** `src/indicators/technical.py`  
**优先级：** P2

| 验收 |
|------|
| `0.382→0.65`, `0.618→0.70` 等为固定映射，非动态统计 |
| 重命名后 UI 不展示为「概率 XX%」（见 FIN-UI-01） |

---

### FIN-08 · EMA610 高周期警告（F-008）

**模块：** `indicator_snapshot` / 报告 JSON  
**优先级：** P2  
**关联：** `IND-12`

| 验收 |
|------|
| 4h/1d bars < 610 时 notes 或 report 字段含「EMA610 仅供参考」 |

---

### FIN-09 · VWAP Volume 缺失（F-009）

**模块：** `technical.add_vwap`, `verify.indicator_snapshot`  
**优先级：** P2

| 场景 | 期望 |
|------|------|
| Volume 全 0 | VWAP notes 含不可用/警告 |
| 跨 UTC 0 点 | VWAP 日切重置（单测固定 index） |

---

### FIN-10 · 占位外部因子（F-010）

**模块：** `data/sources/news.py`, `report.external`  
**优先级：** P2

| 验收 |
|------|
| `external.source` 或等价字段为 `placeholder` |
| LLM prompt 快照含「占位数据不可采信」（可选 snapshot test） |

---

### FIN-11 · Agent 决策链边界（F-011）

**模块：** `trader`, `debate`, `manager`  
**优先级：** P2

| 场景 | 期望 |
|------|------|
| debate=bearish，有 short 信号 | `trader.primary_direction=short` |
| debate=neutral，有信号 | 与 FIN-01 修复后风控/经理行为一致 |
| conservative approved | `decision.action=reduce`, `position_scale=0.4` |
| 三档均否决 | `decision.action=wait` |

```python
# 计划路径：tests/unit/test_agent_chain.py
```

---

## 4. 集成测试（需 TradingView）

### FIN-INT-01 · 1d 双源价差（F-005）

| 验收 |
|------|
| 记录 `fetch 1d 独立` 与 `5m resample→1d` 末 close 差值 |
| 价差 > 阈值时 `meta.warnings` 含提示 |

### FIN-INT-02 · K 线时间戳新鲜度

| 验收 |
|------|
| 5m 末 bar 时间与当前 UTC 差 < 可配置阈值（如 24h，周末除外） |

---

## 5. 手工 / 合规 UI（FIN-UI-*）

| ID | 页面 | 验收（Review §6.3 / §8） |
|----|------|--------------------------|
| FIN-UI-01 | 机构报告 | 「胜率」「概率」须标注 **结构权重，非回测**；不出现未标注的「胜率 XX%」 |
| FIN-UI-02 | 机构报告 | DXY / 日历 / 新闻显示 **占位/模拟** 视觉区分 |
| FIN-UI-03 | LLM 决策链 | manager `reduce` 时展示 `position_scale`（如 40%） |
| FIN-UI-04 | 机构报告 + 侧边栏 | EMA610 历史不足时有可见警告 |
| FIN-UI-05 | 全页 footer | 固定免责声明：「胜率非历史回测，不构成投资建议」 |

---

## 6. 实施路线图

| 阶段 | 用例 | 动作 |
|------|------|------|
| **Sprint 1** | FIN-01, FIN-02, FIN-06, FIN-03, FIN-UI-01/05 | 修 P0/P1 逻辑 + 合规文案 |
| **Sprint 2** | FIN-04, FIN-05, FIN-07~09, FIN-INT-01, FIN-UI-04 | 数据与指标标注 |
| **Sprint 3** | FIN-10, FIN-11, FIN-UI-02/03 | 占位标注 + Agent 单测 |
| **已Done** | IND-01, IT-03, IND-12 | 维持回归 |

---

## 7. 执行

```bash
python tests/run.py --financial   # FIN-*（4 项预期失败，见 GitHub #9-#13）
```

发版前手工：执行 **FIN-UI-01 ~ FIN-UI-05**（P0/P1）。
