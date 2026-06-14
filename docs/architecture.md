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
| **Bullish Researcher** | `agents/factory.py` → rule / `llm/stages/bullish` | ✅ 双轨（P0） |
| **Bearish Researcher** | `agents/factory.py` → rule / `llm/stages/bearish` | ✅ 双轨（P0） |
| **Discussion** | `agents/factory.py` → rule / `llm/stages/debate` | ✅ 双轨（P0） |
| **Trader Agent** | `agents/trader.py` | ✅ 生成交易提案（复用 signal 引擎） |
| **Risk Team** (激进/中性/保守) | `agents/risk.py` | ✅ 三档风控过滤 |
| **Manager** | `agents/manager.py` | ✅ 最终执行/观望决策 |
| **LLM 报告文案** | `llm/analyst.py` | ✅ 流水线末尾（`LLM_ENABLED`） |
| **流式 LLM I/O** | `viz/pipeline_progress.py` | ✅ 生成时实时展示 |
| **Execution** | （未来）券商/MT5 API | 🔲 未实现 |
| **Streamlit UI** | `app.py` + `views/*` + `viz/*` | ✅ 三页：机构 / 短线 / LLM 决策 |

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
│   + report["agent_trace"] + meta.stage_sources + meta.llm_io
│   + 可选 llm/analyst 文案层
└────────────────────────────┬────────────────────────────────────┘
                             ▼
                      app.py + views/* + viz/*
                      ensure_report() 线程生成 + session 缓存
```

\* 占位模块，后续接真实 API 时不改 UI。

---

## 3. 目录结构

```
src/
├── core/
│   ├── types.py          # Evidence, Debate, Proposal, Decision…
│   ├── progress.py       # 生成进度 + LLM I/O 记录（contextvar）
│   └── orchestrator.py   # run_trade_agent_pipeline()
├── agents/
│   ├── factory.py          # 统一调度 rule / llm / hybrid
│   ├── bullish.py          # 规则：看多研究员
│   ├── bearish.py          # 规则：看空研究员
│   ├── debate.py           # 规则：辩论
│   ├── trader.py / risk.py / manager.py
│   └── llm/
│       ├── base.py
│       ├── payload.py
│       └── stages/         # LLM 各阶段实现
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

## 5. 后续迭代

| 优先级 | 任务 | 负责层 |
|--------|------|--------|
| **P0** | LLM 研究 + 辩论 + 流式 I/O | ✅ 见 [llm-agents.md](./llm-agents.md) |
| P1 | LLM 交易员（hybrid 信号选择） | `agents/llm/stages/trader.py` |
| P2 | LLM 风控 + 经理 | `agents/llm/stages/risk.py`, `manager.py` |
| P3 | ICT Interpreter + DXY/日历 API | `ict_pa.py`, `data/sources/` |
| **P4** | 报告文案层 | ✅ `llm/analyst.py` |

完整 LLM 设计见 **[docs/llm-agents.md](./llm-agents.md)**。

---

## 6. 调试 agent_trace

```python
report, _, _ = run_analysis()
print(report["agent_trace"]["debate"]["discussion_notes"])
print(report["agent_trace"]["decision"]["summary"])
```

可在 Streamlit 侧边栏「智能体决策链」「LLM 输入/输出」查看 trace 与完整 Prompt/响应。
