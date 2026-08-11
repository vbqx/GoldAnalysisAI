# Advice V2 报告 JSON 契约

`run_analysis()` 返回的 `report` 是界面和归档共同消费的人工审核建议。

```json
{
  "artifact_kind": "human_review_advice",
  "artifact_version": 2,
  "meta": {},
  "metrics": {},
  "advice": {},
  "timeframes": {},
  "levels": {},
  "external": {}
}
```

## 顶层字段

| 字段 | 说明 |
|---|---|
| `meta` | 数据源、更新时间、data-as-of、观察模式、运行配置、步骤和可选 LLM 遥测。 |
| `metrics` | 当前价、日内高低和涨跌等市场摘要。 |
| `advice` | 唯一有效的人工审核建议契约。 |
| `timeframes` | 4h、1h、15m、5m 结构上下文。 |
| `levels` | 来源和周期可追溯的支撑、阻力结构。 |
| `external` | 新闻、日历、宏观报价和抓取状态；只作背景风险。 |

V1 字段 `signals`、`agent_trace`、`projections`、`validated_plans` 不属于本契约。

## `advice`

固定字段为：

- `decision`: `WAIT | WATCH_LONG | WATCH_SHORT | AVOID`
- `bias`: `bullish | bearish | mixed | neutral`
- `confidence`: `low | medium | high`，表示证据等级，不是历史胜率
- `summary`、`horizon`、`current_price`
- `primary_setup`: 最多一个；`WAIT`/`AVOID` 时为 `null`
- `alternative_scenario`
- `market_context`、`risks`、`uncertainties`、`evidence`
- `audit`: `passed`、`violations`、`warnings`、`policy_version`

`primary_setup` 包含 `direction`、`attention_zone`、`current_state`、`rationale`、`confirmation_checklist`、`invalidation`、`invalidation_level`、`targets`、`evidence_ids` 和 `reward_risk_to_targets`。

可重复生成脱敏样例：

```bash
python scripts/export_sample_report.py
```

样例见 [sample-report.json](./sample-report.json)。
