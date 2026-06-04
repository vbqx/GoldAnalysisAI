# GoldAnalysisAI 架构设计（TradeAgent 参考）

> **原则**：前端 Streamlit 不变；`run_analysis()` 仍返回 `(report, data, analyses)`。  
> 内部分层按 [TradeAgent](https://github.com/TauricResearch/TradingAgents) 多智能体流水线重构。

---

## 1. 与 TradeAgent 对照

| TradeAgent 模块 | GoldAnalysisAI 对应 | 当前状态 |
|-----------------|---------------------|----------|
| **Market** (Yahoo 等) | `data/sources/market.py` → TradingView OANDA:XAUUSD | ✅ 已接入 |
| **News** (Bloomberg/Reuters) | `data/sources/news.py` | 🔲 占位，规则文案 |
| **Social** (X/Reddit) | `data/sources/social.py` | 🔲 占位 |
| **Fundamentals** (DXY/宏观) | `data/sources/fundamentals.py` | 🔲 占位 |
| **Bullish Researcher** | `agents/bullish.py` | ✅ 从 ICT 结构提取看多证据 |
| **Bearish Researcher** | `agents/bearish.py` | ✅ 从 ICT 结构提取看空证据 |
| **Discussion** | `agents/debate.py` | ✅ 多空辩论 → 共识 bias |
| **Trader Agent** | `agents/trader.py` | ✅ 生成交易提案（复用 signal 引擎） |
| **Risk Team** (激进/中性/保守) | `agents/risk.py` | ✅ 三档风控过滤 |
| **Manager** | `agents/manager.py` | ✅ 最终执行/观望决策 |
| **Execution** | （未来）券商/MT5 API | 🔲 未实现 |
| **Streamlit UI** | `app.py` + `viz/*` | ✅ 不变 |

---

## 2. 数据流

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
│  Market(TV) │ News* │ Social* │ Fundamentals(DXY)*              │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
                    data/aggregator.py
                    → MarketContext
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   indicators/          analysis/          (external evidence)
   technical.enrich      ict_pa.analyze
         │                   │
         └─────────┬─────────┘
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RESEARCHER TEAM                              │
│   Bullish Agent ──┐                                              │
│                   ├──► Debate ──► consensus_bias                 │
│   Bearish Agent ──┘                                              │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TRADER AGENT                                 │
│   generate_trading_signals + debate → TransactionProposal        │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RISK MANAGEMENT TEAM                           │
│   Aggressive │ Neutral │ Conservative → RiskReview[]             │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MANAGER                                    │
│   ManagerDecision → 排序 signals / 观望                          │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   REPORT BUILDER                                 │
│   analysis/report_engine.build_report (JSON schema 不变)         │
│   + report["agent_trace"] 审计链（UI 暂未展示）                   │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
                      app.py / viz/*
```

\* 占位模块，后续接真实 API 时不改 UI。

---

## 3. 目录结构

```
src/
├── core/
│   ├── types.py          # Evidence, Debate, Proposal, Decision…
│   └── orchestrator.py   # run_trade_agent_pipeline()
├── agents/
│   ├── bullish.py        # 看多研究员
│   ├── bearish.py        # 看空研究员
│   ├── debate.py         # 辩论
│   ├── trader.py         # 交易员
│   ├── risk.py           # 风控三档
│   └── manager.py        # 经理决策
├── data/
│   ├── aggregator.py     # 汇总数据源 → MarketContext
│   ├── fetcher.py        # (legacy facade)
│   ├── tradingview.py
│   └── sources/
│       ├── market.py
│       ├── news.py
│       ├── social.py
│       └── fundamentals.py
├── analysis/             # 结构引擎 + 报告组装（逐步拆进 agents）
├── indicators/
├── viz/                  # 前端 — 不改动
└── pipeline.py           # → orchestrator 薄封装
```

---

## 4. 对外接口（不变）

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
# report 结构与原 MVP 相同，新增可选字段：
# report["agent_trace"]  # 智能体决策链，便于调试与后续 UI
```

---

## 5. 后续迭代（分析质量）

当前已知问题：**部分结论仍依赖规则模板，外部数据为占位**。建议按层修复：

| 优先级 | 任务 | 负责层 |
|--------|------|--------|
| P0 | ICT 检测逻辑校准（BOS/OB/FVG 与实盘对齐） | `analysis/ict_pa.py` |
| P1 | DXY / 经济日历真实 API | `data/sources/fundamentals.py`, `news.py` |
| P2 | 结论文案由 `ManagerDecision` + 证据链生成，去掉硬编码 | `agents/manager.py`, `report_engine.py` |
| P3 | LLM 深度思考层（Trader Agent o1 类） | `agents/trader.py` + 可选 OpenAI |
| P4 | 执行层对接模拟/实盘 | 新 `execution/` 模块 |

---

## 6. 调试 agent_trace

```python
report, _, _ = run_analysis()
print(report["agent_trace"]["debate"]["discussion_notes"])
print(report["agent_trace"]["decision"]["summary"])
```

可在 Streamlit 侧边栏增加「智能体 trace」折叠面板（可选，不影响现有布局）。
