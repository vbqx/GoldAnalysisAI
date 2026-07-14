# 开发者速查表

一页纸回答：**我想改 X，该动哪个文件、跑什么测试**。
流水线步骤权威列表见 [pipeline-steps.yaml](./pipeline-steps.yaml)（与代码在 CI 中同步校验）。

持续审核的模块范围、证据门槛、每日归档审核与每周/发布前流程门槛，见[交易分析系统持续审核蓝图](../planning/audit-plan.md)。

---

## 流水线步骤与代码对照

| 步骤 ID | 中文名 | 主文件 | 大模型 |
|---------|--------|--------|--------|
| `fetch` | 数据拉取 | `data/fetch_pipeline.py` | 否 |
| `indicators` | 技术指标 | `indicators/technical.py` | 否 |
| `ict` | ICT 结构 (LuxAlgo SMC) | `analysis/ict_pa.py`, `analysis/luxalgo_smc.py` | 否 |
| `analyst_team` | 分析师团队 | `agents/analysts/*` + `factory.py` | 可选 |
| `bullish` | 看多研究 | `agents/bullish.py` + `factory.py` | 可选 |
| `bearish` | 看空研究 | `agents/bearish.py` + `factory.py` | 可选 |
| `debate` | 多空辩论 | `agents/debate.py` + `factory.py` | 可选 |
| `trader` | 交易员 | `agents/factory.py` + `agents/trader.py` | 可选 |
| `risk` | 风控 | `agents/factory.py` + `agents/risk.py` | 可选 |
| `manager` | 经理 | `agents/factory.py` + `agents/manager.py` | 可选 |
| `report` | 组装报告 | `analysis/report_engine.py` | 否 |
| `llm_narrative` | LLM 文案 | `llm/analyst.py` | 可选 |
| `archive` | 运行归档 | `data/run_archive.py` | 否 |

**回放**（不进上表进度条）：`viz/replay_loader.py` → `load_replay_bundle()`，读 `.cache/run_archives/`。

---

## 改功能 → 文件 → 测试

| 我想… | 改这里 | 验证 |
|-------|--------|------|
| **启动 Streamlit 应用** | `python run_app.py` | 勿直接 `streamlit run app.py`；见 [AGENTS.md](../../AGENTS.md) |
| 调整 EMA/VWAP/Fib | `indicators/technical.py` | `pytest tests/unit/test_indicators.py` |
| 调整 Lux 检测 (BOS/OB/FVG) | `analysis/luxalgo_smc.py` | `pytest tests/unit/test_luxalgo_smc.py` |
| 调整 DGT 量价 (POC/VA/S/R) | `analysis/dgt_price_action.py` | `pytest tests/unit/test_dgt_price_action.py` |
| 调整 PA/SMC 提示词主次 | `analysis/field_glossary.py` | 对照 [smc-pa-narrative.md](../architecture/smc-pa-narrative.md) |
| 调整周期事实快照 / LLM 结构字段 | `analysis/tf_snapshot.py`, `analysis/technical_context.py` | `pytest tests/unit/test_tf_snapshot.py tests/unit/test_technical_context_lux.py` |
| 调整五块叙事合并逻辑 | `analysis/narrative_combine.py` | `pytest tests/unit/test_narrative_combine.py` |
| 调整交易计划信号几何 | `analysis/plan_signals.py` | `pytest tests/unit/test_plan_signals.py` |
| 调整报告五块文案 (总览/流动性/结构) | `analysis/narrative_sections.py` | `pytest tests/unit/test_narrative_sections.py` |
| 调整报告流动性/周期汇总事实 | `analysis/report_facts.py` | `pytest tests/unit/test_report_facts.py` |
| 改交易信号几何 | `analysis/report_engine.py` | `pytest tests/unit/test_financial_review.py` |
| **Manager 授权 / 仓位映射** | `analysis/report_engine.py` (`apply_manager_authorization`) | `pytest tests/unit/test_manager_authorization.py` |
| **确定性风控门控** | `analysis/risk_gates.py`, `agents/risk.py`, `agents/factory.py` | `pytest tests/unit/test_risk_gates.py tests/unit/test_rule_chain_stability.py` |
| **信号几何 / 稳定 signal_id** | `analysis/signal_geometry.py`, `analysis/signal_identity.py` | `pytest tests/unit/test_signal_geometry.py tests/unit/test_signal_identity.py` |
| **数据时效 / 观察模式** | `analysis/data_freshness.py`, `core/orchestrator.py` | `pytest tests/unit/test_data_freshness.py` |
| **LLM 叙事授权边界** | `analysis/narrative_sections.py`, `llm/analyst.py` | `pytest tests/unit/test_narrative_authorization.py tests/unit/test_narrative_top_level.py` |
| **事实注册表 / 不变量 / 质量分** | `analysis/fact_registry.py`, `report_invariants.py`, `report_invariant_gate.py`, `report_reliability.py` | `pytest tests/unit/test_fact_registry.py tests/unit/test_report_invariants.py tests/unit/test_report_invariant_gate.py tests/unit/test_report_reliability.py tests/unit/test_golden_report_benchmark.py`；见 [report-trust.md](../architecture/report-trust.md) |
| **证据溯源（Research/Debate）** | `agents/analysts/evidence_provenance.py`, `agents/llm/schemas.py` | `pytest tests/unit/test_evidence_provenance.py` |
| **Session PA / 1d 交易时段** | `analysis/price_action_facts.py` | `pytest tests/unit/test_dgt_price_action.py` |
| **LLM 叙事 context 压缩** | `llm/context.py`, `analysis/narrative_facts.py` | `pytest tests/unit/test_llm_context_compact.py` |
| **Levels A/B/C 硬契约** | `agents/llm/schemas.py`, `analysis/level_validator.py` | `pytest tests/unit/test_llm_levels.py` |
| **日历过滤 / 外部文本** | `data/calendar_utils.py`, `data/external_format.py` | `pytest tests/unit/test_external_sources.py tests/unit/test_analyst_input_density.py` |
| **运行审计摘要** | `analysis/audit_summary.py` | `pytest tests/unit/test_audit_summary.py` |
| **历史回放归档 / 兼容** | `run/archive/`（入口 `src/run`） | `pytest tests/unit/test_run_archive.py tests/unit/test_archive_optimizations.py` |
| **主图 OB/FVG 可见范围** | `analysis/chart_zone_filters.py`, `viz/lightweight_chart.py` | `pytest tests/unit/test_chart_projections.py`；见 [chart-layers.md](../architecture/chart-layers.md) |
| 规则模式一致性门禁 | `tests/tools/coherence_check.py` | `$env:AGENT_MODE="rule"; python tests/tools/coherence_check.py` |
| 金融实跑快照 | `tests/tools/financial_review_run.py` | 输出 `tests/reports/financial_review_snapshot.json` |
| 改新闻分析师逻辑 | `agents/analysts/news.py` | `pytest tests/unit/test_analyst_input_density.py` |
| 接入新外部数据源 | `data/sources/` + `fetch_pipeline.py` | `pytest tests/unit/test_external_sources.py` |
| 金十 MCP 参数 | `config.py` + `jin10_feed.py` | `python tests/run.py --external` |
| 新增 LLM 阶段 | `agents/llm/stages/` + `factory.py` | `pytest tests/unit/test_analyst_team_llm.py tests/unit/test_llm_trade_stages.py` |
| LLM 传输/重试/超时 | `llm/client.py`, `agents/llm/base.py` | `pytest tests/unit/test_llm_transport.py tests/unit/test_llm_client_timeouts.py` |
| 改 Streamlit 布局 | `viz/report_views.py` + `viz/dashboard_components.py` | 手工界面 / 用例 catalog `UIL-*` |
| 改外部数据页 | `viz/external_data_view.py` + `views/4_外部数据.py` | `pytest tests/unit/test_external_data_view.py` |
| 改运行前配置/回放 UI | `viz/run_config_panel.py` + `core/run_config.py` | `pytest tests/unit/test_run_config.py tests/unit/test_streamlit_ensure_report.py` |
| **评审发现项 / FIN-* 状态** | [reviews/findings-status.md](../reviews/findings-status.md) | 改信号/风控前必读 |
| 改后台生成/回放加载 | `viz/generation_worker.py`, `viz/replay_loader.py` | 同上 + `pytest tests/unit/test_archive_optimizations.py` |
| **等待页轻量进度（防白屏）** | `viz/streamlit_common.py`, `viz/generation_worker.py` (`compact_llm_io_for_live`) | `pytest tests/unit/test_live_progress_ui.py` |
| **观察模式仍跑 LLM（点位/交易/风控）** | `core/orchestrator.py`, `agents/factory.py` | `pytest tests/unit/test_llm_trade_stages.py` |
| 改 session 缓存/ensure_report | `viz/streamlit_common.py`, `viz/session_keys.py` | 同上 |
| 改进度条/I/O 展示 | `viz/pipeline_progress.py` | 手工生成报告 |
| 改流水线顺序 | `core/orchestrator.py` + **`docs/reference/pipeline-steps.yaml`** | `pytest tests/regression/test_doc_pipeline_sync.py` |

---

## 配置速查

| 变量 | 典型值 | 作用 |
|------|--------|------|
| `AGENT_MODE` | `rule` / `llm` / `hybrid` | 智能体调度：规则 / 纯 LLM / 混合 |
| `LLM_ENABLED` | `true` / `false` | 报告文案层开关 |
| `LLM_STAGE_ANALYSTS` | `true` | 分析师团队 LLM |
| `LLM_ANALYST_ONLY` | `technical` / `fundamentals` / `news` / `sentiment` | 仅调试单个 Analyst LLM |
| `LLM_STAGE_RESEARCH` | `true` | 看多/看空 LLM |
| `LLM_STAGE_DEBATE` | `true` | 辩论 LLM |
| `LLM_STAGE_TRADER` | `true` | 交易员 LLM |
| `LLM_STAGE_RISK` | `true` | 风控 LLM |
| `LLM_STAGE_MANAGER` | `true` | 经理 LLM |
| `LLM_PAYLOAD_FUNNEL` | `true` | 研究/辩论/交易员只读上游结论（非全量 market） |
| `LLM_TIMEOUT` | `120` | 遗留总超时；未单独设 read 时作为流式 chunk 空闲上限 |
| `LLM_CONNECT_TIMEOUT` | `min(30, LLM_TIMEOUT)` | TCP/TLS 建连超时（秒） |
| `LLM_READ_TIMEOUT` | `LLM_TIMEOUT` | SSE chunk 空闲超时（秒） |
| `LLM_MAX_RETRIES` | `2` | 每阶段重试次数（实际尝试 = 1 + 此值） |
| `LLM_RETRY_BACKOFF_BASE_S` | `1.0` | 重试指数退避基数（秒） |
| `LLM_STAGE_WARN_MS` | `120000` | 单阶段 LLM 耗时超过此值写 warning 日志 |
| `MT5_ENABLED` | `false` | 可选 MT5 provider，默认不影响 TradingView |
| `JIN10_API_TOKEN` | — | 金十 MCP |
| `LOG_LEVEL` | `DEBUG` | 跟踪流水线 |

完整列表见 `.env.example` 与 [handbook.md §2.3](./handbook.md#23-配置env)。

---

## 调试三件套

```python
from src.pipeline import run_analysis
report, data, analyses = run_analysis()

# 1. 步骤与耗时
print(report["meta"]["generation_steps"])

# 2. 决策链
print(report["agent_trace"]["debate"]["consensus_bias"])
print(report["agent_trace"]["decision"]["action"])

# 3. 每阶段用规则还是 LLM
print(report["meta"]["stage_sources"])
```

---

## 对外接口（勿轻易改签名）

```python
from src.pipeline import run_analysis
report, data, analyses = run_analysis()
```

| 返回值 | 消费者 |
|--------|--------|
| `report` | `viz/*` 全部界面 |
| `data` | K 线图表 |
| `analyses` | 结构区图表叠加 |

---

## 相关文档

| 文档 | 何时用 |
|------|--------|
| [onboarding.md](../operations/onboarding.md) | 首次读项目 |
| [glossary.md](./glossary.md) | 不懂术语 |
| [examples/report-schema.md](./examples/report-schema.md) | 不懂 report JSON |
| [walkthrough.md](../operations/walkthrough.md) | 界面操作动线 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
