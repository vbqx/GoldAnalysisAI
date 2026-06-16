# 报告 JSON 结构说明

`run_analysis()` 返回的 `report` dict 是 UI 的**唯一数据契约**。  
脱敏样例文件：[sample-report.json](./sample-report.json)（由 `scripts/export_sample_report.py` 生成，可重复导出）。

```bash
python scripts/export_sample_report.py
```

---

## 顶层字段一览

| 字段 | 类型 | UI 用途 | 产出阶段 |
|------|------|---------|----------|
| `meta` | object | 标题、数据源、agent_mode、步骤、I/O | orchestrator 收尾 |
| `metrics` | object | 顶栏现价、日涨跌 | report_engine |
| `sentiment` | object | 饼图（结构权重，非回测胜率） | report_engine |
| `conclusion` | object | 结论文案、must_do | report_engine + 可选 LLM |
| `timeframes` | object | 各周期结构摘要 | report_engine |
| `signals` | array | 交易计划卡片 | report_engine |
| `projections` | array | 路径投影图 | report_engine |
| `fibonacci` | array | Fib 回撤位 | report_engine |
| `external` | object | DXY/新闻/社媒面板 | orchestrator 注入 |
| `agent_trace` | object | LLM决策链页决策审计 | orchestrator 注入 |
| `llm_analysis` | object | LLM 深度文案（可选） | llm/analyst.py |
| `calendar_events` | array | 财经日历 | 金十 live 或占位 |

---

## `meta` — 元信息与审计

```json
{
  "symbol": "XAUUSD",
  "updated_at": "2026-06-16 08:39 (UTC+8)",
  "data_source": "OANDA:XAUUSD",
  "agent_mode": "rule",
  "stage_sources": { "bullish": { "source": "rule" } },
  "generation_steps": [ { "id": "fetch", "label": "数据拉取", "status": "done" } ],
  "llm_io": [ { "stage": "analyst_team", "kind": "rule" } ],
  "context_stats": { "headline_count": 12, "calendar_count": 5 }
}
```

| 子字段 | 说明 |
|--------|------|
| `agent_mode` | 当前 `AGENT_MODE`：rule / llm / hybrid |
| `stage_sources` | 每阶段实际 rule/llm 及 fallback 原因 |
| `generation_steps` | 与 [pipeline-steps.yaml](../pipeline-steps.yaml) 步骤 ID 对应 |
| `llm_io` | 规则 stage_io + LLM messages/output |
| `context_stats` | Analyst 输入密度，见 [analyst-context.md](../analyst-context.md) |

---

## `metrics` — 价格摘要

```json
{
  "current_price": 2659.6,
  "daily_change": -8.5,
  "daily_change_pct": -0.32,
  "daily_high": 2671.6,
  "daily_low": 2644.6
}
```

来源：`fetcher.daily_metrics()`，基于 1d K 线。

---

## `sentiment` — 结构情绪（⚠️ 非回测胜率）

```json
{ "bullish": 25.0, "bearish": 62.0, "ranging": 13.0 }
```

来自 `ict_pa.sentiment_score()` 多周期趋势加权。UI 若展示为「胜率」须标注 **结构权重**。见 [financial-review.md](../financial-review.md) F-002。

---

## `signals[]` — 交易计划

每条 signal 典型字段：

| 字段 | 说明 |
|------|------|
| `name` | 策略名称（如「激进做空」） |
| `theme` | `"short"` / `"long"` |
| `entry_low` / `entry_high` | 入场区间 |
| `stop_loss` | 止损价 |
| `take_profits` | 止盈价列表 |
| `win_rate` | ⚠️ 结构偏多权重字符串，非历史胜率 |
| `risk_reward` | 展示用 R:R（部分为固定模板） |
| `position_size` | 描述性仓位档位 |

Manager 可能按 `decision.selected_signal_indices` 重排顺序。

---

## `agent_trace` — 决策审计链

```json
{
  "analyst_team": {
    "technical": { "bias": "bearish", "summary": "...", "items": [] },
    "fundamentals": { "bias": "bearish", "summary": "..." },
    "news": { "bias": "neutral", "summary": "..." },
    "sentiment": { "bias": "bullish", "summary": "..." }
  },
  "debate": {
    "consensus_bias": "bearish",
    "consensus_strength": 0.65,
    "discussion_notes": ["..."]
  },
  "proposal": { "primary_direction": "short", "signal_indices": [0] },
  "risk_reviews": [ { "profile": "conservative", "approved": true } ],
  "decision": { "action": "execute", "summary": "..." }
}
```

在「LLM决策链」页 **智能体决策** Tab 可视化。

---

## `external` — 外部数据

```json
{
  "dxy_impact": "偏强 → 利空黄金",
  "news_headlines": ["..."],
  "macro_quotes": [ { "name": "DXY", "close": 104.2, "bias": "bearish" } ],
  "sources": { "dxy": "tradingview", "news": "jin10_mcp" },
  "fetch_errors": []
}
```

| `sources` 值 | 含义 |
|--------------|------|
| `tradingview` / `jin10_mcp` | live 拉取成功 |
| `placeholder` | 拉取失败回退文案 |
| `disabled` | 功能关闭 |

---

## 如何在代码中探索

```python
import json
from pathlib import Path

sample = json.loads(Path("docs/examples/sample-report.json").read_text())
print(sample.keys())
print(sample["agent_trace"]["analyst_team"].keys())
```

Live 报告：

```python
from src.pipeline import run_analysis
report, _, _ = run_analysis()
print(json.dumps(report["meta"]["generation_steps"], ensure_ascii=False, indent=2))
```

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [developer-onboarding.md](../developer-onboarding.md) | 三种返回值说明 |
| [glossary.md](../glossary.md) | win_rate、AgentTrace 等术语 |
| [reverse-engineering.md](../reverse-engineering.md) | 各 UI 区块算法来源 |

---

## 免责声明

样例 JSON 仅供学习研究；live 报告不构成投资建议。
