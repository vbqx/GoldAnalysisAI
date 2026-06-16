# 开发者上手指南

> 目标：让你在 **15 分钟内** 建立心智模型，知道「点刷新后发生了什么」「该读哪些文件」「改功能该动哪里」。  
> 本项目能跑但难懂，通常不是因为代码乱，而是 **三层概念叠在一起**：金融方法论（ICT/PA）、多智能体流水线（TradingAgents）、LLM 双轨调度。

---

## 1. 先用一句话理解项目

**GoldAnalysisAI = 用规则和/或大模型，把 XAUUSD 行情 + 外部新闻宏观，加工成一份 JSON 报告，再用 Streamlit 画成网页。**

它不是：
- 实盘交易系统（没有下单 Execution）
- 严格意义的回测平台（「胜率」是多周期趋势投票，不是历史统计）
- 单一 LLM Chat 应用（LLM 只是流水线若干阶段的可选增强）

它是：
- **确定性计算**（K 线、指标、ICT 结构、交易信号几何）+ **可选 LLM 解读**（Analyst / 研究 / 辩论 / 报告文案）
- 对外只有一个稳定入口：`run_analysis() → (report, data, analyses)`

---

## 2. 五层心智模型（由外到内）

```
┌─────────────────────────────────────────────────────────┐
│  Layer 0 — UI（Streamlit）                               │
│  app.py 导航 → views/* 三页 → viz/* 只读 report 渲染      │
└───────────────────────────┬─────────────────────────────┘
                            │ ensure_report() 触发
┌───────────────────────────▼─────────────────────────────┐
│  Layer 1 — 流水线入口                                     │
│  pipeline.run_analysis() → orchestrator.run_trade_agent…  │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
┌───────────────────┐                 ┌───────────────────┐
│ Layer 2 — 确定性   │                 │ Layer 3 — 智能体   │
│ 拉数 → 指标 → ICT  │ ──MarketContext─▶│ Analyst→研究→辩论  │
│ → 信号几何         │                 │ → 交易→风控→经理    │
└───────────────────┘                 └─────────┬─────────┘
                                              │
┌─────────────────────────────────────────────▼─────────────┐
│  Layer 4 — 报告 JSON + 可选 LLM 文案（llm/analyst.py）     │
└───────────────────────────────────────────────────────────┘
```

**关键分界**：
- **Layer 2 永远跑**：不依赖 API Key，产出可复现的结构化事实
- **Layer 3 默认规则**：`AGENT_MODE=rule` 时全是 Python 规则函数
- **Layer 3/4 的 LLM**：只有配置了 `LLM_API_KEY` 且开关打开才参与；失败会 hybrid 回退规则

---

## 3. 一次「刷新报告」发生了什么

用户点 **「刷新报告」** 或首次进入页面时，`src/viz/streamlit_common.py` 的 `ensure_report()` 在后台线程调用 `run_analysis()`。

> 步骤 ID 权威列表：[pipeline-steps.yaml](./pipeline-steps.yaml)（CI 与 `orchestrator.py` / `fetch_pipeline.py` 同步校验）

| 步骤 ID | 代码位置 | 产出 | 是否用 LLM |
|---------|----------|------|------------|
| `fetch` | `data/fetch_pipeline.py` | OHLCV、新闻、DXY、社媒 | 否 |
| `indicators` | `indicators/technical.py` | EMA/VWAP 列 | 否 |
| `ict` | `analysis/ict_pa.py` | 5 个周期的 trend/BOS/OB/FVG | 否 |
| `analyst_team` | `agents/analysts/*` + `factory.py` | 四位分析师 bias + items | 可选 |
| `bullish` | `agents/bullish.py` / `factory.py` | 证据列表 + 置信度 | 可选 |
| `bearish` | `agents/bearish.py` / `factory.py` | 证据列表 + 置信度 | 可选 |
| `debate` | `agents/debate.py` / `factory.py` | `consensus_bias` | 可选 |
| `trader` | `analysis/report_engine.py` + `agents/trader.py` | `TradingSignal[]` + 提案 | 否 |
| `risk` | `agents/risk.py` | 通过/降仓 | 否 |
| `manager` | `agents/manager.py` | execute / reduce / wait | 否 |
| `report` | `analysis/report_engine.py` | UI 消费的 JSON | 否 |
| `llm_narrative` | `llm/analyst.py` | `report["llm_analysis"]` | 可选 |

**切换页面不会重跑**——三页共享 `st.session_state` 里缓存的同一份 `(report, data, analyses)`。

---

## 4. 15 分钟读码路线

按顺序打开，每文件只抓「入口函数 + 返回值」：

| 顺序 | 文件 | 看什么 |
|------|------|--------|
| 1 | `app.py` | 纯导航，不跑流水线 |
| 2 | `src/viz/streamlit_common.py` | `ensure_report()` — UI 与流水线的唯一连接点 |
| 3 | `src/pipeline.py` | 对外 API，一行委托 |
| 4 | `src/core/orchestrator.py` | **主调用图**，建议通读 |
| 5 | `src/core/types.py` | 所有 dataclass：`MarketContext`、`AnalystReport`、`AgentTrace`… |
| 6 | `src/agents/factory.py` | rule / llm / hybrid 怎么选 |
| 7 | `src/analysis/report_engine.py` | 报告 JSON 长什么样、信号怎么生成 |

读完后你应该能回答：
- 「改信号逻辑」→ `report_engine.py`
- 「改辩论规则」→ `debate.py` 或 `factory.py` 的 LLM stage
- 「改 UI 布局」→ `viz/report_views.py`（**不要** import agents）
- 「加外部数据源」→ `data/sources/` + `fetch_pipeline.py`

---

## 5. 三个最容易混淆的概念

### 5.1 Analyst Team vs 研究员 vs LLM 文案

| 名称 | 职责 | 输出字段 |
|------|------|----------|
| **Analyst Team** | 按信息类型分工（技术/宏观/新闻/情绪） | `agent_trace.analyst_team` |
| **Bull/Bear 研究员** | 按交易方向整合证据 | `agent_trace` 中 debate 之前的 evidence |
| **LLM 报告文案** | 流水线**末尾**润色结论文字 | `report["llm_analysis"]` |

Analyst 提供「原材料」，研究员做「多空立场」，经理做「执行与否」——这是 TradingAgents 的两阶段研究设计。

### 5.2 rule / llm / hybrid

| 模式 | 行为 |
|------|------|
| `rule` | 全部走 Python 规则函数，最快、最稳定 |
| `llm` | 启用阶段优先 LLM；失败回退规则 |
| `hybrid` | 规则先跑；LLM 置信度 ≥ 阈值才覆盖规则结果 |

调度中心：`src/agents/factory.py` 的 `_pick_evidence()` 和各 `run_*` 函数。

### 5.3 report vs data vs analyses

```python
report, data, analyses = run_analysis()
```

| 返回值 | 类型 | 谁消费 | 内容 |
|--------|------|--------|------|
| `report` | `dict` | UI 主消费 | 价格、结论、信号、外部数据、agent_trace |
| `data` | `dict[str, DataFrame]` | 图表 | 各周期 OHLCV + EMA/VWAP |
| `analyses` | `dict[str, TimeframeAnalysis]` | 图表 overlay | OB/FVG/结构事件 |

**UI 原则**：`viz/*` 只读这三个对象，不直接 import `agents/*`。

---

## 6. 报告 JSON 核心字段速查

生成一次报告后，在 Python 或「LLM决策链」页查看：

```python
report, data, analyses = run_analysis()

report["metrics"]          # 现价、日涨跌
report["conclusion"]       # 顶栏结论文案
report["signals"]          # 交易计划卡片
report["sentiment"]        # 饼图（结构偏多权重，非回测胜率）
report["external"]         # DXY、新闻、社媒、sources 标签
report["agent_trace"]        # 完整决策链（含 analyst_team）
report["meta"]["agent_mode"]       # rule / llm / hybrid
report["meta"]["stage_sources"]    # 每阶段实际用的 rule 还是 llm
report["meta"]["generation_steps"] # 耗时步骤
report["meta"]["llm_io"]           # 智能体 I/O 审计
report["meta"]["context_stats"]    # Analyst 输入密度计数
```

**调试决策链**：优先看 `report["agent_trace"]` 和 `report["meta"]["stage_sources"]`。

---

## 7. 配置：最小可跑 vs 完整体验

### 最小可跑（纯规则，无外部 Key）

```env
# .env 留空或只配 TV；TradingView 匿名也可拉数（历史 bar 较少）
AGENT_MODE=rule
LLM_ENABLED=false
```

能出报告，但新闻/日历可能是 fallback 占位文案。

### 推荐开发配置

```env
JIN10_API_TOKEN=...        # 金十快讯/资讯/日历
AGENT_MODE=rule            # 先搞懂规则链，再开 LLM
LLM_ENABLED=false
LOG_LEVEL=DEBUG
```

### 完整 LLM 体验

见 [README.md](../README.md) LLM 配置块或 [llm-agents.md](./llm-agents.md) §3.3。

---

## 8. 常见问题（开发者版）

| 困惑 | 解释 |
|------|------|
| 为什么叫 Agent 但大部分是规则？ | 架构按 TradingAgents **分层命名**；LLM 阶段是渐进接入的，trader/risk/manager 仍是规则 |
| 改了代码 UI 不变 | Streamlit 缓存了 report；需重启 + 点「刷新报告」 |
| LLM 开了但没效果 | 检查 `LLM_API_KEY`、`AGENT_MODE`、`LLM_STAGE_*` 开关；看 `stage_sources` |
| 生成要 5 分钟 | LLM 全流程多次 API 调用正常；用 `AGENT_MODE=rule` 可降到 ~30s |
| 文档和代码对不上 | 以 `orchestrator.py` 调用顺序为准；架构 doc 可能滞后 |
| 胜率 62% 是回测吗？ | **不是**；是 `sentiment_score()` 多周期趋势加权，见 [financial-review.md](./financial-review.md) F-002 |

---

## 9. 改功能该动哪里

完整速查表见 **[cheat-sheet.md](./cheat-sheet.md)**（含测试命令与配置项）。

| 我想… | 改这里 |
|-------|--------|
| 调整 EMA/OB/FVG 检测 | `analysis/ict_pa.py` |
| 改入场/止损/止盈规则 | `analysis/report_engine.py` |
| 改 Analyst 新闻筛选 | `agents/analysts/news.py` + `data/sources/news.py` |
| 接入新 LLM 阶段 | `agents/llm/stages/` + `factory.py` |
| 改 Streamlit 布局 | `viz/report_views.py` |
| 改刷新/缓存行为 | `viz/streamlit_common.py` |
| 改流水线步骤 | `orchestrator.py` + **`pipeline-steps.yaml`** |

---

## 10. 建议的深入学习顺序

```
本文（15 min）
    ↓
orchestrator.py + types.py（30 min）
    ↓
development.md §3 数据流（需要查函数链时）
    ↓
examples/report-schema.md + sample-report.json（理解输出）
    ↓
llm-agents.md（开 LLM 时）
    ↓
financial-review.md（改信号/风控时必读边界）
```

**不要**一开始通读 [development-reference.md](./development-reference.md)（600+ 行）——它是 **参考手册**，不是 **教程**。

---

## 11. 文档体系（P0–P3）

| 层级 | 文档 | 用途 |
|------|------|------|
| P0 教程 | 本文 + [walkthrough.md](./walkthrough.md) | 心智模型 + UI 动线 |
| P1 参考 | [development-reference.md](./development-reference.md) · [glossary.md](./glossary.md) · [examples/report-schema.md](./examples/report-schema.md) | 函数链 · 术语 · JSON |
| P2 速查/同步 | [cheat-sheet.md](./cheat-sheet.md) · [pipeline-steps.yaml](./pipeline-steps.yaml) | 改功能 · CI 步骤校验 |
| P3 演示 | [walkthrough.md](./walkthrough.md) mermaid 序列图 | 可扩展录屏至 `docs/assets/` |

---

## 相关文档

| 文档 | 何时读 |
|------|--------|
| [README.md](./README.md) | 文档索引 |
| [cheat-sheet.md](./cheat-sheet.md) | 改功能速查 |
| [glossary.md](./glossary.md) | 不懂术语 |
| [development.md](./development.md) | 环境搭建 hub |
| [development-reference.md](./development-reference.md) | 查具体函数、模块、FAQ |
| [examples/report-schema.md](./examples/report-schema.md) | 理解 report JSON |
| [walkthrough.md](./walkthrough.md) | UI 操作动线 |
| [architecture.md](./architecture.md) | 理解 TradingAgents 对照 |
| [llm-agents.md](./llm-agents.md) | 开 LLM / 调试 hybrid |
| [financial-review.md](./financial-review.md) | 理解字段语义与已知缺陷 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
