# 报告可信度层（Report Trust）

> **目标**：在 LLM 多智能体链与 Streamlit 展示之间，增加**确定性**的事实注册、证据溯源、一致性与可靠度门禁，避免「模型自说自话」与跨板块矛盾悄悄进入归档。
>
> 关联 GitHub daily-audit：**#21–#32**（Session PA、授权边界、时效门禁、证据链、事实注册表、不变量、可靠度、golden 基准）。

文档索引：[architecture.md](./architecture.md) · [llm-agents.md](./llm-agents.md) · [analyst-context.md](./analyst-context.md) · [report-schema.md](../reference/examples/report-schema.md)

---

## 1. 在流水线中的位置

```
… → Manager → build_report → apply_manager_authorization
         │
         ├─ build_data_as_of → observation_mode（不可执行快照）
         ├─ 跳过 LLM Levels / Trader / Risk（observation_mode 时）
         │
         ├─ build_fact_registry（叙事前，供 LLM context 引用）
         ├─ llm/analyst.py（叙事层，消费 fact_registry + narrative_facts）
         │
         └─ validate_report_invariants → apply_report_invariant_gate（#30）
              → build_fact_registry（二次）→ compute_report_reliability
              → agent_trace 快照（与交付 report 一致）
              → build_audit_summary → archive_run → return report（Streamlit UI）
```

**交付路径**：gate 改写的 `report` dict **同时**进入归档与 UI（`generation_worker` 使用 `run_analysis()` 返回值），不是「只写磁盘」。gate 不拦截已完成的 Agent/LLM 调用，只修正**最终交付物**（授权、结论、叙事字段、`pipeline_status`）。

**原则**：

| 层级 | 职责 | 模块 |
|------|------|------|
| 事实注册 | 所有进入报告/叙事的数字与关键文本带 `fact_id`、`as_of`、`source`、`quality` | `analysis/fact_registry.py` |
| 证据溯源 | Analyst → Research → Debate 保留 `evidence_id` + `refs` | `agents/analysts/evidence_*.py` |
| 不变量门禁 | 授权/几何/时效/经理对齐等确定性校验 + 失败降级 | `report_invariants.py` + `report_invariant_gate.py` |
| 可靠度 | 可解释、代码计算的报告质量分（非 LLM 自报胜率） | `analysis/report_reliability.py` |
| Golden 基准 | 零 token 确定性回归（starter 3 例，目标扩至 30–50） | `tests/fixtures/golden_reports/` |

---

## 2. 事实注册表（Fact Registry）

**版本**：`fr-v2`（`FACT_REGISTRY_VERSION`）  
**计算版本**：`pa-v3`（Session PA 锚定最新 1d K 线 open，见 #21）

### 2.1 单条事实契约

```json
{
  "fact_id": "pa.session.poc",
  "value": 4102.31,
  "value_type": "numeric",
  "as_of": "2026-07-10T20:55:00Z",
  "source": "OANDA:XAUUSD",
  "timeframe": "session",
  "calculation_version": "pa-v3",
  "quality": "verified"
}
```

文本类事实（日历状态、新闻时间、market_status）使用 `value_type: text`。

### 2.2 注册范围

| 前缀 | 示例 | 来源 |
|------|------|------|
| `metrics.*` | `metrics.current_price` | OANDA 现价 / 日 OHLC |
| `pa.session.*` / `pa.{tf}.*` | `pa.session.poc`, `pa.5m.sr.0` | DGT 量价（session 用 canonical id） |
| `{tf}.*` | `4h.swing_high`, `4h.ob.0.low` | Lux SMC |
| `liquidity.*` | 流动性池价位 | 报告 liquidity 表 |
| `signal.{id}.*` | entry/SL/TP | 交易计划（primary/alternate = verified） |
| `freshness.*` | `freshness.executable`, `bar.5m.count` | `data_as_of` + `context_stats` |
| `calendar.*` | `calendar.state`, `calendar.event.0.time` | 金十 / risk_events |
| `news.*` | `news.0.published_at` | `external.headline_items` |
| `macro.*` | `macro.DXY.close` | TradingView 宏观报价（PIT 对齐标记） |
| `sentiment.*` | 结构情绪百分比 | `ict_pa.sentiment_score` |

**冲突**：同一 `fact_id` 二次注册不同数值 → `quality=conflict`，写入 `conflict_fact_ids`，不变量 `INV-FACT-001` 可拦截。

### 2.3 LLM 消费方式

- **叙事层**（`llm/context.py`）：payload 含 `price_fact_id`、`fact_registry.facts`（`compact_fact_index`）、信号几何的 `*_fact_id` 映射。
- **Research 层**：`allowed_evidence_ids` 白名单；**禁止** LLM 自造 `*:structure:*` ID
- 叙事层（`llm/context.py`）：**不发送**裸 `price`/`metrics`/信号几何数字，仅 `fact_id` 索引 + `fact_registry`

写入位置：`report.meta.fact_registry`（叙事前构建一次，LLM 与归档后再构建一次）。

---

## 3. 证据溯源（Evidence Provenance）

**问题**（#27）：Research 阶段 LLM 重写 evidence 时丢弃 `refs`，Debate 无法追溯至 jin10 / TV 等原始来源。

### 3.1 稳定 ID

| 阶段 | ID 规则 |
|------|---------|
| Analyst Team | `{agent}:{index}`，如 `technical_analyst:0`（`evidence_ids.assign_evidence_ids`） |
| Research 引用 | 必须携带 Analyst 已有 `evidence_id`；或 `{agent}:structure:{n}` 表示新增结构证据 |
| 合并进 Research 输入 | `items_for_direction()` 保留 `upstream_id` |

### 3.2 Parser 硬约束（LLM Research）

`parse_agent_evidence(..., allowed_evidence_ids=...)`：

- **缺 ID** → `ValueError`
- **未知 ID**（不在白名单且非合法 structure id）→ `ValueError`
- **LLM 丢弃 refs** → 从 `evidence_registry` 恢复 upstream `source`
- **重复 ID** → 按 `evidence_id` 去重，保留最高 `strength`

### 3.3 置信度元数据

| 对象 | 字段 | 含义 |
|------|------|------|
| `AgentEvidence` | `provenance_meta` | `upstream_coverage`, `source_diversity`, `computed_confidence`, `model_confidence`, `dedupe_dropped` |
| `AgentEvidence.confidence` | 混合值 | 45% 模型自报 + 55% 确定性计算 |
| `ResearchDebate` | `debate_meta` | `evidence_balance`, `shared_evidence_ids`, `computed_consensus_strength` |
| `ResearchDebate.consensus_strength` | 混合值 | 40% 模型 + 60% 确定性 |

---

## 4. 数据时效与观察模式（#26）

**时机**：Debate 完成后、`run_trader` 之前调用 `build_data_as_of(raw)`。

| 条件 | 行为 |
|------|------|
| `executable=false`（周末 / 滞后 >4h 等） | `observation_mode=true` |
| observation_mode | **跳过** LLM Levels、LLM Trader、LLM Risk；规则 Trader + 确定性 Risk |
| observation_mode | Manager 倾向 wait；叙事 prompt 要求 observation_only |
| 结论前缀 | `【快照观察，非实时执行】` |

Risk payload（`risk_payload`）在 LLM 路径传入完整几何 + `data_as_of`；观察模式下不调用付费 Risk LLM。

---

## 5. 报告不变量门禁（#30）

**模块**：`analysis/report_invariants.py` → `report.meta.report_invariants`

| 代码 | 检查项 |
|------|--------|
| `INV-GEO-*` | 信号 entry/SL/TP 几何、SELL/BUY 相对现价位置、TP 阶梯 |
| `INV-AUTH-*` | wait/observation 下叙事含可执行措辞（扩展中英文黑名单+正则） |
| `INV-MGR-*` | 经理 wait vs 结论标题矛盾 |
| `INV-PRICE-*` | LLM 叙事中未注册价位 |
| `INV-FRESH-*` | 陈旧快照 + 急迫执行措辞 |
| `INV-META-*` | 缺 narrative 审计元数据 |
| `INV-FACT-*` | fact_registry 冲突 |

未通过时执行 **`apply_report_invariant_gate`**：撤销执行授权、清空违规 LLM 字段、重写结论、`pipeline_status=degraded`（不可 replay）；`meta.warnings` 仍追加摘要供 UI 展示。

---

## 6. 报告质量分（#31，启发式）

**模块**：`analysis/report_reliability.py` → `report.meta.report_reliability`

| 分量 | 权重 | 说明 |
|------|------|------|
| `data_quality` | 0.20 | 来自 `data_as_of.executable` / 数据年龄 |
| `freshness_quality` | 0.15 | 观察模式降权 |
| `evidence_coverage` | 0.15 | Analyst + Debate 填 evidence 比例 |
| `source_diversity` | 0.10 | **仅** `refs.source/provider`（不含 agent 前缀） |
| `cross_timeframe_agreement` | 0.15 | 多周期 trend 一致性 |
| `bull_bear_separation` | 0.10 | 多空 research 置信差 |
| `schema_quality` | 0.15 | 不变量是否通过 / 是否已降级 |

主字段 **`report_quality_score`**（`overall_reliability` 为兼容别名）；`calibration_status=heuristic`。

**UI**：展示「报告质量分（启发式，非胜率）」。

---

## 7. Session PA 边界（#21 / #28）

**模块**：`analysis/price_action_facts.py`

- Session 切片锚定 **最新 1d K 线 open**（OANDA 21:00/22:00 UTC），**非** UTC 自然日零点。
- 聚合 5m H/L/C 须与最新 1d 线在容差内一致，否则跳过 session block。
- 非 `DatetimeIndex` 输入 → 安全返回空（不 crash 技术链）。

注册表对应 ID：`pa.session.poc` / `vah` / `val`。

---

## 8. Levels 硬契约（#25）

- LLM Levels 必须返回 **恰好 3** 条 setup，`path_id` 为 **A/B/C** 各一（禁止静默补 id）。
- `level_validator` 校验完整 TP 阶梯（非仅 TP1）。
- 激进 SELL 入场区须在现价上方（`plan_signals` + `INV-GEO-003`）。

---

## 9. Golden 基准（#32，进行中）

| 路径 | 用途 |
|------|------|
| `tests/fixtures/golden_reports/*.json` | 冻结 point-in-time 报告片段 |
| `tests/unit/test_golden_report_benchmark.py` | 零 token：fact_registry + invariants + reliability 快照 |

当前 **3** 个 starter 样本（观望 / 几何错误 / 陈旧急迫措辞）；路线图目标 30–50 个标注场景。

---

## 10. 相关测试

```bash
pytest tests/unit/test_fact_registry.py
pytest tests/unit/test_report_invariants.py
pytest tests/unit/test_report_reliability.py
pytest tests/unit/test_evidence_provenance.py
pytest tests/unit/test_report_invariant_gate.py
pytest tests/unit/test_evidence_provenance.py
pytest tests/unit/test_llm_context_fact_refs.py
pytest tests/unit/test_dgt_price_action.py      # session PA
pytest tests/unit/test_narrative_top_level.py # 授权措辞
pytest tests/unit/test_risk_gates.py
pytest tests/unit/test_llm_context_compact.py
```

---

## 11. 改功能速查

| 我想… | 改这里 |
|-------|--------|
| 扩展注册事实类型 | `analysis/fact_registry.py` |
| 调整不变量规则 | `analysis/report_invariants.py` |
| 调整可靠度公式 | `analysis/report_reliability.py` |
| 证据 ID / 去重 / 校准置信 | `agents/analysts/evidence_provenance.py` + `agents/llm/schemas.py` |
| 叙事 fact_id 引用 | `llm/context.py` |
| 编排注入顺序 | `core/orchestrator.py` |
| UI 可靠度/不变量展示 | `viz/llm_view.py`, `viz/agent_trace_view.py` |

更完整的文件→测试对照见 [cheat-sheet.md](../reference/cheat-sheet.md)。
