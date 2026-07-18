# 群友黄金分析报告 — 实现反推

> 基于截图结构的逆向分析，对应本仓库 MVP 的实现映射。

## 1. 报告整体架构

原报告是一个 **单页分析仪表盘**，数据流大致如下：

```
行情 API (OHLCV)
    ↓
指标层 (EMA / VWAP / Fib)
    ↓
结构层 (Swing → BOS/CHoCH → OB/FVG → Liquidity)
    ↓
策略层 (多空胜率 / 交易计划 / 路径概率)
    ↓
渲染层 (HTML 模板 + 图表库 + 可选 LLM 文案)
```

群友版本大概率是：**Python 计算 + Plotly/ECharts 图表 + 模板渲染**，结论文字可能来自规则引擎或 LLM 二次生成。

---

## 2. 各模块反推

### 2.1 Header 区（价格 + 结论）

| 字段 | 来源 | MVP 实现 |
|------|------|----------|
| Current Price | 最新 tick/close | `fetcher.daily_metrics()` |
| Daily Change | close - prev_close | 同上 |
| Daily High/Low | 当日 K 线 | 同上 |
| Market Sentiment | 多周期趋势加权 | `ict_pa.sentiment_score()` |
| 结论文字 | 规则 / LLM | `report_engine.build_conclusion()` |

Sentiment 规则：4H 权重最高，1H 次之，15m/5m 辅助。原报告 62% Bearish 符合「大周期空 + 小周期反弹」场景。

### 2.2 多周期分析（左侧）

每个周期块包含：

- **Trend** — 比较最近 swing high/low 是否 HH/HL（多）或 LH/LL（空）
- **BOS** — 顺势突破前结构点
- **CHoCH** — 逆原趋势突破（如空头中的向上突破前高）
- **EMA 关系** — 价格与各 EMA/VWAP 的上下方
- **OB / FVG / Liquidity** — 见 2.4

MVP: `ict_pa.analyze_timeframe()` → `luxalgo_smc.analyze_luxalgo()`

### 2.3 主图（5min 执行结构）

机构报告主图使用 **5 分钟** Lightweight Charts（`report_views.py` + `lightweight_chart.py`）：

- K 线 + 成交量
- 5m 主图绘制近位 5 个 Internal OB；active FVG 仍按可见价格范围过滤；远位多周期结构见 `context_levels`
- BOS/CHoCH 标记（5m + 15m 事件）
- **不绘制** EMA/VWAP 曲线、MACD/RSI/ADX 副图、路径预测虚线

分层说明见 `docs/aspice/SWE.2-architecture/chart-layers.md`
- 路径推演见底栏 **未来走势推演**（`report["path_summary"]`，源自 `trend_projections()`）

技术指标仍在 `enrich()` 管道计算，供 agent/LLM 使用，并在侧边栏 **指标校验** 表展示（含 RSI14、MACD、ADX14、ATR14 等）。

短线策略页（`views/2_短线策略.py`）仍展示 15m + 5m 执行级图表。

### 2.4 ICT/PA 核心算法（LuxAlgo SMC）

实现：`src/analysis/luxalgo_smc.py`（移植 LuxAlgo Smart Money Concepts Pine，默认参数）。

| 模块 | 规则摘要 |
|------|----------|
| Swing structure | leg size=50，pivot 在 leg 翻转时记录 |
| Internal structure | leg size=5，用于 internal OB |
| BOS/CHoCH | close crossover/crossunder swing pivot |
| FVG | `low>high[2]` + `close[1]>high[2]` + auto threshold；作废：bull `low<bottom` |
| OB | 突破时 parsedHigh/Low 极值柱；ATR(200) 高波动过滤；High/Low 作废 |
| EQH/EQL | size=3，阈值 0.1×ATR(200) |
| swing_high/low | 最近 swing pivot（非 min/max 全历史） |

`ict_pa.analyze_timeframe()` 为对外入口，内部调用 `analyze_luxalgo()`。

#### Premium / Discount
- 使用主 swing range 中点作为 equilibrium
- 价格高于 / 低于 equilibrium 约 0.1% 判定为 premium / discount

#### 技术输入密度
- `analysis/technical_context.py` 统一 rule technical、LLM technical、最终 narrative 的技术上下文
- 支撑/阻力从日高/日低、前收、swing、equilibrium、Fib、liquidity、OB/FVG 聚合
- ATR14 / RSI14 / MACD / ADX14 由 OHLCV 计算，并参与技术 evidence
- 技术质量评分检查 K 线数量、指标 warm-up、volume 有效性与 ICT 输入密度

> 完整 ICT 体系还包含 Kill Zone、Breaker / Mitigation Block、PDH/PDL 与 session 高低点等；当前 liquidity sweep 只实现了规则确认的一部分，不等同于完整 ICT 事件模型。

### 2.5 右侧统计 & 交易计划

**胜率饼图** — 非真实回测胜率，而是多周期趋势投票：
```
score_bear = 0.35×4H_bear + 0.30×1H_bear + ...
```

**交易计划卡片** — 规则生成：
| 类型 | 逻辑 |
|------|------|
| 激进做空 | 最近 bearish FVG 下沿~上沿 |
| 保守做空 | 更高 TF 的 bearish OB |
| 扫低做多 | swing low 下方 ATR/配置偏移，且需要 sweep + reclaim 质量确认 |

SL/TP 按 zone 宽度或 swing 极值推算，RR 1:2~1:4。

MVP: `report_engine.compute_trading_signals(ctx)`（orchestrator 唯一入口；`build_report` 与 trader 共用）

### 2.6 底部区域

- **Fibonacci** — 最近 swing high→low 的 0.382/0.5/0.618（swing 来自近期结构边界）
- **路径投影** — 三路径 + 概率（`trend_projections` 主路径随 bullish / bearish / ranging 主导情绪切换；底栏卡片展示，非主图虚线）
- **失效条件** — 15min 站稳某价位、出现 bullish CHoCH 等

---

## 3. 原报告可能的完整技术栈

| 层级 | 可能选型 |
|------|----------|
| 数据 | TradingView webhook / OANDA / MT5 / 券商 API |
| 计算 | Python (pandas + ta-lib) |
| 图表 | Plotly / Lightweight Charts / ECharts |
| 前端 | 静态 HTML / Streamlit / Next.js |
| 文案 | GPT-4 + 结构化 prompt |
| 输出 | html2image / Puppeteer 截图发群 |

---

## 4. 与原报告的差距（MVP 已知限制）

1. EMA610 在 5min 上需要足够历史数据，匿名 TradingView 可能不足
2. OB/FVG 检测为启发式，非 ICT 标准定义
3. 胜率是趋势投票，非历史回测统计
4. DXY / 金十 / 社媒已接入实时 API，拉取失败时回退占位文案（UI 应区分 live / fallback）
5. LLM 结论润色可选（`LLM_ENABLED`）；默认规则引擎生成结论文案
6. Kill Zone、Breaker/Mitigation、PDH/PDL、session 高低点与跨周期 zone overlap 仍是后续输入缺口；liquidity sweep 目前为规则确认的部分实现

---

## 5. 文档边界

本文只做报告结构与算法反推，不维护后续迭代。当前路线图见 [roadmap.md](../../management/roadmap.md)。

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [documentation-center.md](../../documentation-center.md) | 文档中心索引 |
| [handbook.md](../../aspice/SWE.3-detailed-design/reference/handbook.md) | 模块实现与数据流 |
| [static-code-review.md](../../aspice/records/reviews/financial/static-code-review.md) | 金融逻辑评审 |
