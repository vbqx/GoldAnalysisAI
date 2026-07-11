# 开发者上手指南

> 目标：在 **15 分钟内** 建立心智模型，弄清「点刷新后发生了什么」「该读哪些文件」「改功能该改哪里」。
> 项目能跑但难懂，通常是因为三层概念叠在一起：**金融方法论（ICT/PA）**、**多智能体流水线（TradingAgents）**、**大模型双轨调度（规则 / 纯 LLM / 混合）**。

---

## 1. 一句话理解项目

**GoldAnalysisAI = 用规则引擎和/或大语言模型，把 XAUUSD 行情与外部新闻、宏观数据，加工成一份 JSON 报告，再用 Streamlit 渲染成网页仪表盘。**

它**不是**：
- 实盘下单系统（没有券商 Execution 层）
- 严格意义上的回测平台（报告里的「胜率」是多周期趋势投票，不是历史统计）
- 单纯的聊天式 LLM 应用（大模型只是流水线若干阶段的可选增强）

它**是**：
- **确定性计算**（K 线、指标、ICT 结构、交易信号几何）+ **可选大模型解读**（分析师 / 研究 / 辩论 / 报告文案）
- 对外只有一个稳定入口：`run_analysis()` → 返回 `(report, data, analyses)`

---

## 2. 五层心智模型（由外到内）

```
┌─────────────────────────────────────────────────────────┐
│  第 0 层 — 界面（Streamlit）                              │
│  app.py 导航 → views/* 三页 → viz/* 只读 report 渲染       │
└───────────────────────────┬─────────────────────────────┘
                            │ ensure_report() 触发
┌───────────────────────────▼─────────────────────────────┐
│  第 1 层 — 流水线入口                                     │
│  pipeline.run_analysis() → orchestrator 编排全流程       │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
┌───────────────────┐                 ┌───────────────────┐
│ 第 2 层 — 确定性   │                 │ 第 3 层 — 智能体   │
│ 拉数→指标→ICT结构  │ ──MarketContext─▶│ 分析师→研究→辩论   │
│ → 交易信号几何     │                 │ → 交易→风控→经理   │
└───────────────────┘                 └─────────┬─────────┘
                                              │
┌─────────────────────────────────────────────▼─────────────┐
│  第 4 层 — 报告 JSON + 可选 LLM 文案（llm/analyst.py）    │
└───────────────────────────────────────────────────────────┘
```

**关键分界**：
- **第 2 层始终执行**：不依赖 API Key，产出可复现的结构化事实
- **第 3 层默认走规则**：`AGENT_MODE=rule` 时全部是 Python 规则函数
- **第 3、4 层的大模型**：须配置 `LLM_API_KEY` 且打开对应开关；失败时在混合模式下回退到规则结果

---

## 3. 一次「生成 / 刷新报告」发生了什么

首次进入页面时，`src/viz/streamlit_common.py` 中的 `ensure_report()` 会先显示 **生成前配置** 面板；用户选择规则 / LLM / 混合模式并点击 **「开始生成报告」** 后，后台线程才会调用 `run_analysis()`。已有报告后点击 **「重新配置 / 刷新报告」** 会清空缓存并回到配置面板。

> 步骤 ID 权威列表见 [pipeline-steps.yaml](../reference/pipeline-steps.yaml)（与 `orchestrator.py`、`fetch_pipeline.py` 在 CI 中同步校验）

| 步骤 ID | 代码位置 | 产出 | 是否用大模型 |
|---------|----------|------|--------------|
| `fetch` | `data/fetch_pipeline.py` | K 线、新闻、DXY、社媒 | 否 |
| `indicators` | `indicators/technical.py` | EMA/VWAP 列 | 否 |
| `ict` | `analysis/ict_pa.py` | 五周期 trend/BOS/OB/FVG | 否 |
| `analyst_team` | `agents/analysts/*` + `factory.py` | 四位分析师倾向与证据 | 可选 |
| `bullish` | `agents/bullish.py` / `factory.py` | 看多证据与置信度 | 可选 |
| `bearish` | `agents/bearish.py` / `factory.py` | 看空证据与置信度 | 可选 |
| `debate` | `agents/debate.py` / `factory.py` | 多空共识 `consensus_bias` | 可选 |
| `trader` | `factory.py` + `agents/trader.py` | 交易信号与提案 | 可选 |
| `risk` | `factory.py` + `agents/risk.py` | 三档风控通过/降仓 | 可选 |
| `manager` | `factory.py` + `agents/manager.py` | 执行 / 减仓 / 观望 | 可选 |
| `report` | `analysis/report_engine.py` | 界面消费的 JSON | 否 |
| `llm_narrative` | `llm/analyst.py` | `report["llm_analysis"]` | 可选 |

**切换页面不会重跑流水线** — 三页共享 `st.session_state` 中缓存的同一份 `(report, data, analyses)`。

---

## 4. 15 分钟读码路线

按顺序打开，每个文件只关注「入口函数 + 返回值」：

| 顺序 | 文件 | 关注点 |
|------|------|--------|
| 1 | `app.py` | 纯导航，不跑流水线 |
| 2 | `src/viz/streamlit_common.py` | `ensure_report()` — 生成前配置、缓存、后台线程 |
| 3 | `src/core/run_config.py` | UI 运行配置与 import-bound 模块同步 |
| 4 | `src/pipeline.py` | 对外 API，一行委托 |
| 5 | `src/core/orchestrator.py` | **主调用图**，建议通读 |
| 6 | `src/core/types.py` | 全部数据结构：`MarketContext`、`AnalystReport`、`AgentTrace` 等 |
| 7 | `src/agents/factory.py` | 规则 / 大模型 / 混合模式如何调度 |
| 8 | `src/analysis/report_engine.py` | 报告 JSON 结构与信号如何生成 |

读完后应能回答：
- 改信号逻辑 → `report_engine.py`
- 改辩论规则 → `debate.py` 或 `factory.py` 中的 LLM 阶段
- 改界面布局 → `viz/report_views.py`（**不要** import agents）
- 加外部数据源 → `data/sources/` + `fetch_pipeline.py`

---

## 5. 三个最容易混淆的概念

### 5.1 分析师团队 vs 研究员 vs LLM 报告文案

| 名称 | 职责 | 输出字段 |
|------|------|----------|
| **分析师团队（Analyst Team）** | 按信息类型分工：技术 / 宏观 / 新闻 / 情绪 | `agent_trace.analyst_team` |
| **看多 / 看空研究员** | 按交易方向整合证据 | 辩论前的 evidence |
| **LLM 报告文案** | 流水线**末尾**润色结论文本 | `report["llm_analysis"]` |

分析师提供「原材料」，研究员形成「多空立场」，经理决定「是否执行」——这是 TradingAgents 的两阶段研究设计。

### 5.2 规则 / 纯 LLM / 混合 三种模式

| 模式 | 行为 |
|------|------|
| `rule`（规则） | 全部走 Python 规则，最快、最稳定 |
| `llm`（纯大模型） | 启用阶段优先 LLM；失败回退规则 |
| `hybrid`（混合） | 规则先跑；仅当 LLM 置信度 ≥ 阈值才覆盖规则结果 |

调度中心：`src/agents/factory.py` 中的 `_pick_evidence()` 与各 `run_*` 函数。

### 5.3 report / data / analyses 三种返回值

```python
report, data, analyses = run_analysis()
```

| 返回值 | 类型 | 谁在用 | 内容 |
|--------|------|--------|------|
| `report` | `dict` | 界面主消费 | 价格、结论、信号、外部数据、决策链 |
| `data` | `dict[str, DataFrame]` | 图表 | 各周期 OHLCV + EMA/VWAP |
| `analyses` | `dict[str, TimeframeAnalysis]` | 图表叠加 | OB/FVG/结构事件 |

**界面原则**：`viz/*` 只读上述三个对象，不直接 import `agents/*`。

---

## 6. 报告 JSON 核心字段速查

生成报告后，可在 Python 或「LLM决策链」页查看：

```python
report, data, analyses = run_analysis()

report["metrics"]                 # 现价、日涨跌
report["conclusion"]              # 顶栏结论文案
report["signals"]                 # 交易计划卡片
report["sentiment"]               # 饼图（结构权重，非回测胜率）
report["external"]                # DXY、新闻、社媒及来源标签
report["agent_trace"]             # 完整决策链
report["meta"]["agent_mode"]      # rule / llm / hybrid
report["meta"]["run_config"]      # UI 本次选择的运行配置
report["meta"]["stage_sources"]   # 每阶段实际用规则还是 LLM
report["meta"]["generation_steps"]# 各步耗时
report["meta"]["llm_io"]          # 智能体输入输出审计
report["meta"]["context_stats"]   # 分析师输入密度计数
```

**调试决策链**：优先看 `report["agent_trace"]` 和 `report["meta"]["stage_sources"]`。

---

## 7. 配置：从能跑到完整体验

### 最小可跑（纯规则，无外部 Key）

```env
AGENT_MODE=rule
LLM_ENABLED=false
```

TradingView 匿名也可拉数（历史 K 线较少）。新闻/日历可能为占位文案。

### 推荐开发配置

```env
JIN10_API_TOKEN=...     # 金十快讯、资讯、日历
AGENT_MODE=rule         # 先搞懂规则链，再开大模型
LLM_ENABLED=false
LOG_LEVEL=DEBUG
```

### 完整大模型体验

见根目录 [README.md](../../README.md) 或 [llm-agents.md](../architecture/llm-agents.md) 中的环境变量说明。

### 启动 Streamlit（官方方式）

```bash
python run_app.py
```

**不要**直接 `streamlit run app.py`。详见 [AGENTS.md](../../AGENTS.md)。

---

## 8. 常见问题（开发者版）

| 困惑 | 解释 |
|------|------|
| 为什么叫 Agent 但大部分是规则？ | 命名对齐 TradingAgents 分层；LLM 是渐进接入的，交易/风控/经理仍是规则 |
| 改了代码界面不变 | Streamlit 缓存了 report；需重启并点「重新配置 / 刷新报告」 |
| 开了 LLM 但没效果 | 检查 `LLM_API_KEY`、`AGENT_MODE`、`LLM_STAGE_*`；看 `stage_sources` |
| 生成要 5 分钟 | 全流程多次 API 调用属正常；`AGENT_MODE=rule` 可降到约 30 秒 |
| 文档与代码不一致 | 以 `orchestrator.py` 调用顺序为准 |
| 胜率 62% 是回测吗？ | **不是**；见 [financial-review.md](../archive/domain/financial-review.md) F-002 |

---

## 9. 改功能该动哪里

完整速查见 **[cheat-sheet.md](../reference/cheat-sheet.md)**。

| 我想… | 改这里 |
|-------|--------|
| 调整 EMA/OB/FVG | `analysis/ict_pa.py` |
| 改入场/止损/止盈 | `analysis/report_engine.py` |
| 改新闻分析师逻辑 | `agents/analysts/news.py` + `data/sources/news.py` |
| 接入新 LLM 阶段 | `agents/llm/stages/` + `factory.py` |
| 改 Streamlit 布局 | `viz/report_views.py` |
| 改缓存/刷新 | `viz/streamlit_common.py` |
| 改流水线步骤 | `orchestrator.py` + **`../reference/pipeline-steps.yaml`** |

---

## 10. 建议阅读顺序

```
本文（约 15 分钟）
    ↓
orchestrator.py + types.py（约 30 分钟）
    ↓
handbook.md §3（查函数链时）
    ↓
examples/report-schema.md + sample-report.json（理解输出）
    ↓
llm-agents.md（启用大模型时）
    ↓
financial-review.md（改信号/风控前必读）
```

**不要**一开始通读 [handbook.md](../reference/handbook.md)（600+ 行）——那是**参考手册**，不是**入门教程**。

---

## 11. 文档分层说明

| 层级 | 文档 | 用途 |
|------|------|------|
| 教程层 | 本文 + [walkthrough.md](./walkthrough.md) | 心智模型 + 界面动线 |
| 参考层 | [handbook.md](../reference/handbook.md) · [glossary.md](../reference/glossary.md) · [examples/report-schema.md](../reference/examples/report-schema.md) | 函数链 · 术语 · JSON |
| 速查层 | [cheat-sheet.md](../reference/cheat-sheet.md) · [pipeline-steps.yaml](../reference/pipeline-steps.yaml) | 改功能 · CI 步骤校验 |
| 演示层 | [walkthrough.md](./walkthrough.md) 流程图 | 可另录演示视频 |

---

## 相关文档

| 文档 | 何时读 |
|------|--------|
| [README.md](../README.md) | 文档索引 |
| [cheat-sheet.md](../reference/cheat-sheet.md) | 改功能速查 |
| [glossary.md](../reference/glossary.md) | 不懂术语 |
| [setup.md](./setup.md) | 环境搭建入口 |
| [walkthrough.md](./walkthrough.md) | 界面操作动线 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
