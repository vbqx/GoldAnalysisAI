# 技术分析模块架构

> LuxAlgo SMC 检测、报告事实、LLM 上下文、机构文案的分层说明。  
> 原则：**检测一次、事实一处、文案一层、图表单独过滤**。

---

## 1. 分层总览

```
┌─────────────────────────────────────────────────────────────┐
│  DETECTION  检测层（全量 K 线）                               │
│  luxalgo_smc.py → ict_pa.py  |  dgt_price_action.py        │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  FACTS  事实层（无文案、无图表裁剪）                           │
│  tf_snapshot.py · report_facts.py · display_labels.py       │
└────────────────────────────┬────────────────────────────────┘
                             ▼
          ┌──────────────────┴──────────────────┐
          ▼                                         ▼
┌──────────────────────┐              ┌──────────────────────────┐
│  MACHINE CONTEXT      │              │  HUMAN COPY               │
│  technical_context.py │              │  narrative_sections.py    │
│  → LLM / 规则分析师    │              │  → 报告五块 UI + LLM 覆盖   │
└──────────────────────┘              └──────────────────────────┘
          │                                         │
          └──────────────────┬──────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  ASSEMBLY  报告组装                                          │
│  report_engine.py — 信号、结论、路径、schema 壳               │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  CHART  主图可视层（仅 5m 主图 / 策略图）                      │
│  chart_zone_filters.py → lightweight_chart.py               │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 模块职责

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| `luxalgo_smc.py` | Lux Pine 规则移植：结构、OB、FVG、摆动点 | OHLCV DataFrame | `LuxAlgoResult` |
| `ict_pa.py` | 公共类型 + `analyze_timeframe()` 适配 + `sentiment_score()` | OHLCV | `TimeframeAnalysis` |
| `tf_snapshot.py` | **单周期事实快照**（最近 5 条 BOS/CHoCH/OB/FVG、Swing/Strong·Weak H/L） | `TimeframeAnalysis` | `dict` |
| `report_facts.py` | 报告级事实：`timeframes` 汇总、流动性列表 | `data` + `analyses` | `dict` / `list` |
| `display_labels.py` | 趋势/区位/流动性中文标签 | — | 常量与 `liquidity_label()` |
| `technical_context.py` | **LLM/分析师 JSON**：指标、S/R、质量、`timeframe_context()` | `MarketContext` | `dict` |
| `narrative_sections.py` | **机构文案五块** + LLM 校验合并 + `narrative_facts` | `report` | `narrative_sections` |
| `report_engine.py` | 交易信号、结论、关键位、Fib、组装 `report` schema | `data` + `analyses` | `report` |
| `dgt_price_action.py` | DGT 量价：S&R、放量、高波动、Volume Profile（POC/VAH/VAL） | OHLCV | `DgtPriceActionResult` |
| `price_action_facts.py` | 报告级 `price_action` 汇总（5m Profile 用 5m 细拆；**session 锚定最新 1d open**） | `data` | `dict` |
| `chart_zone_filters.py` | **主图**可见 K 线范围内的 Lux OB/FVG 裁剪 | `TimeframeAnalysis` + `plot_df` | 可见 zone 列表 |
| `chart_sr_filters.py` | **主图**可见范围内的 DGT S/R 水平线 | `sr_levels` + `plot_df` | `priceLines` |
| `proximity.py` | ATR/距离阈值（远位结构、流动性 context） | 价格 + ATR | `bool` |
| `level_validator.py` | LLM 价位提案几何校验 | 提案 + ctx | `TradingSignal` |

---

## 3. 数据边界（易混点）

### 全量检测 vs 主图裁剪

| 场景 | 用全量 K 线？ | 可见价格范围过滤？ |
|------|--------------|-------------------|
| Lux 检测 `analyze_timeframe()` | ✅ 是 | ❌ 否 |
| `build_tf_snapshot()` / LLM / 叙事五块 | ✅ 是（用检测结果） | ❌ 否 |
| 5m 主图 OB/FVG 色块 | 检测用全量；**绘制**时再裁 | ✅ 是（最近 360 根 5m 高低价） |
| 5m 主图 DGT S/R 线 | 检测用全量；**绘制**时裁到可见价区 | ✅ 是 |
| 4H/1H/15M 条带图 | 仅 K 线 | 不画 OB/FVG / S/R |

### 唯一事实源

- 每周期结构列表：**只**通过 `build_tf_snapshot()` 生成。
- `report["timeframes"]` = `build_tf_summaries()` → 内部调用 `build_tf_snapshot()`。
- `technical_context.timeframes[]` = `timeframe_context()` → 同样基于 `build_tf_snapshot()`。
- **禁止**在 UI/报告里再写一套平行的 BOS/OB 格式化逻辑；文案走 `narrative_sections.py`。

### DGT Volume Profile 窗口（Fixed 360，非 Visible）

与 dgtrd Pine「Volume Profile → Profile Lookback Range = **Fixed Range**，Length = **360**」对齐：

| 项 | 取值 |
|----|------|
| 模式 | **Fixed Range**（禁止跟图表缩放/Visible Range） |
| 根数 | 各周期各自最近 **360** 根该周期 K（数据不足则用全部，`lookback_bars` / `lookback_requested` 记录） |
| 行数 / VA | 100 rows · 68% value area |
| HTF 成交细分 | 同一时钟窗内的 **5m**（`profile_source=ltf_5m`）；若 5m 覆盖不足窗长 85%，回退该周期原生 K（`native_tf`） |
| 拉取 | `tradingview.fetch_multi_timeframe` 对 15m/1h/4h **各自拉 ≥360 根**；失败才 5m 聚合 |
| LLM | `price_action_summary` 每周期带 `lookback_*` / `profile_source` / 独立 POC；提示禁止混周期 |

`session` 除外：仍按最新 1d open 锚定交易日（见下）。

FVG 进入 fact registry 时附带 `width` / `width_atr_ratio` / `atr`，并与 OB、PA S/R、VA/POC 一起生成稳定 `technical_claim_facts`，供 `claim_eligibility`（`claim-v2`）复算引用关系与核心执行资格；见 [report-trust.md](./report-trust.md) §5.2。

### Session 量价（OANDA 交易时段）

`price_action_facts.build_session_price_action_block()`：

- 以 **最新 1d K 线 open** 为 session 起点（OANDA 约 21:00/22:00 UTC），**不得**用 UTC 自然日 00:00。
- 取该 open 至当前末根 5m 的 bars 做 Volume Profile；聚合 H/L/C 须与最新 1d 线一致（容差内），否则丢弃 session block。
- 非 `DatetimeIndex` 输入安全返回空（降级，不终止 Technical 链）。
- 事实注册表 canonical id：`pa.session.poc` / `vah` / `val`（见 [report-trust.md](./report-trust.md)）。

### 文案单一路径（SMC + PA 组合）

| 字段 | 来源 |
|------|------|
| `report["narrative_sections"]` | **主路径**：`build_rule_narrative_sections()`（SMC 主干 + PA 确认），可选 LLM 逐块覆盖 |
| `report["price_action"]` | DGT 全量计算；文案/LLM 消费，主图仅 S/R 线 |
| 组合规则文档 | [smc-pa-narrative.md](./smc-pa-narrative.md) |
| `report["market_overview"]` | **兼容字段**：由 `overview_bullets_from_sections()` 从 `narrative_sections.market_overview` 派生 |
| `report["conclusion"]` | `report_engine.build_conclusion()` — 交易方向与计划，非结构文案 |

---

## 4. 报告 UI 消费关系

`src/viz/report_views.py`：

| 面板 | 读取字段 |
|------|----------|
| 市场总览 | `narrative_sections["market_overview"]`（回退 `market_overview`） |
| 关键流动性 | `narrative_sections["liquidity"]`（回退 `liquidity`） |
| 4H / 1H / 15M 结构 | `narrative_sections["4h"|"1h"|"15m"]`（回退 `timeframes` + `render_tf_panel`） |
| 结论要点 | `conclusion`（非 narrative_sections） |
| 5m 主图色块 | `analyses["5m"]` + `chart_zone_filters`（Lux OB/FVG） |
| 5m 主图 S/R 线 | `report.price_action.5m` + `chart_sr_filters`（DGT 支撑阻力） |

---

## 5. 扩展指南

| 要改什么 | 改哪个文件 |
|----------|------------|
| Lux 检测规则（OB/FVG/BOS 算法） | `luxalgo_smc.py` |
| 新增结构字段进 LLM | `tf_snapshot.py` + `technical_context.timeframe_context()` |
| 调整机构报告五块文案 | `narrative_sections.py` |
| 主图多画/少画 OB | `chart_zone_filters.py`（不要改 `tf_snapshot`） |
| 交易信号与止损逻辑 | `report_engine.py` |

---

## 6. 已废弃（勿再使用）

| 旧模块 | 替代 |
|--------|------|
| `lux_tf_display.py` | `tf_snapshot.py` |
| `lux_report.py` | `report_facts.py` + `narrative_sections.py` |
| `build_lux_market_overview()` | `narrative_sections` + `overview_bullets_from_sections()` |
| 多套 `_TREND_CN` 常量 | `display_labels.py` |

---

## 7. 相关文档

- [architecture.md](./architecture.md) — 全流水线
- [chart-layers.md](./chart-layers.md) — 主图叠加层
- [analyst-context.md](./analyst-context.md) — LLM 技术上下文
- [llm-agents.md](./llm-agents.md) — `narrative_sections` 双轨
- [report-schema.md](../reference/examples/report-schema.md) — JSON 字段
