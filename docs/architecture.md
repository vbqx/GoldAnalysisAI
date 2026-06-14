# GoldAnalysisAI 架构设计（TradingAgents 参考）

> **原则**：前端 Streamlit 不变；`run_analysis()` 仍返回 `(report, data, analyses)`。  
> 内部分层按 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 多智能体流水线重构。

---

## 1. 与 TradingAgents 对照

| TradingAgents 模块 | GoldAnalysisAI 对应 | 当前状态 |
|-----------------|---------------------|----------|
| **Market** (Yahoo 等) | `data/sources/market.py` → TradingView OANDA:XAUUSD | ✅ 已接入 |
| **Technical Analyst** | `agents/analysts/technical.py` | ✅ 规则版（EMA + ICT 结构） |
| **Fundamentals Analyst** | `agents/analysts/fundamentals.py` | ✅ 规则版（DXY 占位） |
| **News Analyst** | `agents/analysts/news.py` | ✅ 规则版（事件风险占位） |
| **Sentiment Analyst** | `agents/analysts/sentiment.py` | ✅ 规则版（结构投票 + 社媒占位） |
| **Bullish Researcher** | `agents/factory.py` → rule / `llm/stages/bullish` | ✅ 整合 Analyst Team 输出 |
| **Bearish Researcher** | `agents/factory.py` → rule / `llm/stages/bearish` | ✅ 整合 Analyst Team 输出 |
| **Discussion** | `agents/factory.py` → rule / `llm/stages/debate` | ✅ 双轨（P0） |
| **Trader Agent** | `agents/trader.py` | ✅ 生成交易提案 |
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
│                     ANALYST TEAM  ← TradingAgents 对齐           │
│   Technical │ Fundamentals │ News │ Sentiment → AnalystReport[]  │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RESEARCHER TEAM                              │
│   Bullish Agent ──┐   （引用 Analyst Team 同向证据 + ICT 结构）    │
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
│   + report["agent_trace"]["analyst_team"] + stage_sources      │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
                      app.py + views/* + viz/*
```

\* News / Social / Fundamentals 数据源仍为占位，Analyst 层已接入并在 `agent_trace` 中可审计；接真实 API 时不改 UI schema。

---

## 3. Analyst Team 设计

| 分析师 | 文件 | 输入 | 输出 |
|--------|------|------|------|
| Technical | `analysts/technical.py` | EMA/VWAP、ICT 多周期结构 | `AnalystReport(bias, items, summary)` |
| Fundamentals | `analysts/fundamentals.py` | DXY / 宏观占位 | 黄金多空宏观偏向 |
| News | `analysts/news.py` | 头条 + 事件日历占位 | 波动/事件风险（通常 neutral） |
| Sentiment | `analysts/sentiment.py` | 结构情绪投票 + 社媒占位 | 短期情绪偏向 |

**类型**（`core/types.py`）：

- `AnalystReport` — 单个分析师报告（含 `bias: bullish|bearish|neutral`）
- `AnalystTeam` — 四个报告容器，`to_dict()` 写入 `agent_trace.analyst_team`

**研究员整合**（`bullish.py` / `bearish.py`）：

- 保留原有 ICT 结构证据提取
- 通过 `items_for_direction()` 并入 Analyst Team 中**同向**证据
- 辩论阶段在 `discussion_notes` 开头输出四位分析师摘要

---

## 4. 目录结构

```
src/
├── core/
│   ├── types.py          # AnalystReport, AnalystTeam, AgentTrace…
│   ├── progress.py       # 生成进度 + LLM I/O 记录
│   └── orchestrator.py   # run_trade_agent_pipeline()
├── agents/
│   ├── factory.py          # 统一调度 rule / llm / hybrid
│   ├── analysts/           # ← Analyst Team（新增）
│   │   ├── technical.py
│   │   ├── fundamentals.py
│   │   ├── news.py
│   │   ├── sentiment.py
│   │   └── base.py
│   ├── bullish.py / bearish.py / debate.py
│   ├── trader.py / risk.py / manager.py
│   └── llm/stages/         # LLM 各阶段（payload 含 analyst_team）
├── data/
│   ├── aggregator.py
│   └── sources/            # market / news / social / fundamentals
├── analysis/
├── indicators/
├── viz/
└── pipeline.py
```

---

## 5. 对外接口（不变）

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
# 新增可选字段：
# report["agent_trace"]["analyst_team"]  # 四位分析师报告
# report["agent_trace"]["stage_meta"]    # 各阶段 rule/llm 来源
```

---

## 6. 后续迭代

| 优先级 | 任务 | 负责层 |
|--------|------|--------|
| **P0** | Analyst Team 规则版 + 接入流水线 | ✅ `agents/analysts/` |
| **P0** | LLM 研究 + 辩论 + 流式 I/O | ✅ 见 [llm-agents.md](./llm-agents.md) |
| **P1** | Analyst Team LLM 双轨（每分析师独立 Prompt） | `agents/llm/stages/analysts/` |
| **P1** | 真实 News / DXY / 社媒 API | `data/sources/` |
| **P2** | LLM 交易员 / 风控 / 经理 | `agents/llm/stages/` |
| **P3** | ICT Interpreter | `ict_pa.py` |

完整 LLM 设计见 **[docs/llm-agents.md](./llm-agents.md)**。

---

## 7. 调试 agent_trace

```python
report, _, _ = run_analysis()
team = report["agent_trace"]["analyst_team"]
print(team["technical"]["summary"])
print(team["fundamentals"]["bias"])
print(report["agent_trace"]["debate"]["discussion_notes"])
```

可在 Streamlit「LLM决策链」页「智能体决策」Tab 查看 Analyst Team 四列摘要与完整 JSON。
