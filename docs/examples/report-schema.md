# 报告 JSON 结构说明

`run_analysis()` 返回的 `report` 字典是 Streamlit 界面的**唯一数据契约**。  
脱敏样例：[sample-report.json](./sample-report.json)（由 `scripts/export_sample_report.py` 生成，可重复导出）。

```bash
python scripts/export_sample_report.py
```

---

## 顶层字段一览

| 字段 | 类型 | 界面用途 | 产出阶段 |
|------|------|----------|----------|
| `meta` | 对象 | 标题、数据源、模式、步骤、输入输出 | 编排器收尾 |
| `metrics` | 对象 | 顶栏现价、日涨跌 | 报告引擎 |
| `sentiment` | 对象 | 饼图（结构权重，**非回测胜率**） | 报告引擎 |
| `conclusion` | 对象 | 结论文案、必做事项 | 报告引擎 + 可选 LLM |
| `timeframes` | 对象 | 各周期结构摘要 | 报告引擎 |
| `signals` | 数组 | 交易计划卡片 | 报告引擎 |
| `projections` | 数组 | 路径投影图 | 报告引擎 |
| `fibonacci` | 数组 | 斐波那契回撤位 | 报告引擎 |
| `external` | 对象 | DXY/新闻/社媒面板 | 编排器注入 |
| `agent_trace` | 对象 | LLM决策链页决策审计 | 编排器注入 |
| `llm_analysis` | 对象 | LLM 深度文案（可选） | `llm/analyst.py` |
| `calendar_events` | 数组 | 财经日历 | 金十实时或占位 |
| `llm_levels` | 数组 | LLM 原始点位建议审计 | `LLM_STAGE_LEVELS` 开启时 |
| `validated_plans` | 数组 | LLM 点位 validator 接受/拒绝记录 | `level_validator.py` |

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
| `agent_mode` | 当前模式：`rule` / `llm` / `hybrid` |
| `stage_sources` | 每阶段实际用规则还是 LLM，及回退原因 |
| `generation_steps` | 与 [pipeline-steps.yaml](../reference/pipeline-steps.yaml) 步骤 ID 对应 |
| `llm_io` | 规则阶段输入输出 + LLM 消息与响应 |
| `context_stats` | 分析师输入密度，见 [analyst-context.md](../design/analyst-context.md) |

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

来源：`fetcher.daily_metrics()`，基于 1 日 K 线。

---

## `sentiment` — 结构情绪（⚠️ 非回测胜率）

```json
{ "bullish": 25.0, "bearish": 62.0, "ranging": 13.0 }
```

来自 `ict_pa.sentiment_score()` 多周期趋势加权。界面若展示为「胜率」，须标注为**结构权重**。见 [financial-review.md](../domain/financial-review.md) F-002。

---

## `signals[]` — 交易计划

每条信号常见字段：

| 字段 | 说明 |
|------|------|
| `name` | 策略名称（如「激进做空」） |
| `theme` | `"short"` 空 / `"long"` 多 |
| `entry_low` / `entry_high` | 入场区间 |
| `stop_loss` | 止损价 |
| `take_profits` | 止盈价列表 |
| `win_rate` | ⚠️ 结构偏多权重字符串，**非历史胜率** |
| `risk_reward` | 展示用风险收益比（部分为固定模板） |
| `position_size` | 描述性仓位档位 |
| `signal_role` | `primary` / `alternate`，表示是否与结构主导方向一致 |
| `setup_type` | setup 类型，如 `fvg_retest_short`、`liquidity_sweep_long`、`llm_fvg` |
| `status` | `candidate` / `watch` / `active` / `invalid` |
| `trigger_confirmed` | 触发条件是否满足 |
| `trigger_note` | 触发或降级说明 |
| `score_total` / `score_grade` | 信号质量评分与等级 |
| `score_reasons` | 评分依据、触发缺口或降级原因 |

经理可能按 `decision.selected_signal_indices` 重排顺序；orchestrator 会按结构主导方向写入 `signal_role`。`setup_type` 以 `llm_` 开头时表示来源为已通过 validator 的 LLM 点位建议。

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
  "decision": { "action": "execute", "summary": "..." },
  "llm_levels": [],
  "validated_plans": []
}
```

在「LLM决策链」页 **智能体决策** 标签页中可视化。  
`decision.action` 常见值：`execute`（执行）、`reduce`（减仓）、`wait`（观望）。

`agent_trace.llm_levels` 与 `agent_trace.validated_plans` 是决策链页展示 LLM 点位建议和确定性校验结果的审计字段；顶层 `llm_levels` / `validated_plans` 保留同一批数据，便于导出和回放。

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

| `sources` 取值 | 含义 |
|----------------|------|
| `tradingview` / `jin10_mcp` | 实时拉取成功 |
| `placeholder` | 拉取失败，使用占位文案 |
| `disabled` | 功能已关闭 |

---

## 在代码中探索

```python
import json
from pathlib import Path

sample = json.loads(Path("docs/examples/sample-report.json").read_text(encoding="utf-8"))
print(sample.keys())
print(sample["agent_trace"]["analyst_team"].keys())
```

实时报告：

```python
from src.pipeline import run_analysis
report, _, _ = run_analysis()
print(json.dumps(report["meta"]["generation_steps"], ensure_ascii=False, indent=2))
```

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [onboarding.md](../getting-started/onboarding.md) | 三种返回值说明 |
| [glossary.md](../reference/glossary.md) | win_rate、AgentTrace 等术语 |
| [reverse-engineering.md](../domain/reverse-engineering.md) | 各界面区块的算法来源 |

---

## 免责声明

样例 JSON 仅供学习研究；实时报告不构成投资建议。
