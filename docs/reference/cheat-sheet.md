# 开发者速查表

一页纸回答：**我想改 X，该动哪个文件、跑什么测试**。  
流水线步骤权威列表见 [pipeline-steps.yaml](./pipeline-steps.yaml)（与代码在 CI 中同步校验）。

---

## 流水线步骤与代码对照

| 步骤 ID | 中文名 | 主文件 | 大模型 |
|---------|--------|--------|--------|
| `fetch` | 数据拉取 | `data/fetch_pipeline.py` | 否 |
| `indicators` | 技术指标 | `indicators/technical.py` | 否 |
| `ict` | ICT 结构 | `analysis/ict_pa.py` | 否 |
| `analyst_team` | 分析师团队 | `agents/analysts/*` + `factory.py` | 可选 |
| `bullish` | 看多研究 | `agents/bullish.py` + `factory.py` | 可选 |
| `bearish` | 看空研究 | `agents/bearish.py` + `factory.py` | 可选 |
| `debate` | 多空辩论 | `agents/debate.py` + `factory.py` | 可选 |
| `trader` | 交易员 | `agents/factory.py` + `agents/trader.py` | 可选 |
| `risk` | 风控 | `agents/factory.py` + `agents/risk.py` | 可选 |
| `manager` | 经理 | `agents/factory.py` + `agents/manager.py` | 可选 |
| `report` | 组装报告 | `analysis/report_engine.py` | 否 |
| `llm_narrative` | LLM 文案 | `llm/analyst.py` | 可选 |

---

## 改功能 → 文件 → 测试

| 我想… | 改这里 | 验证 |
|-------|--------|------|
| 调整 EMA/VWAP/Fib | `indicators/technical.py` | `pytest tests/unit/test_indicators.py` |
| 调整 Swing/BOS/OB/FVG | `analysis/ict_pa.py` | 查看 `analyses["5m"]` 或 DEBUG 日志 |
| 改辩论/共识逻辑 | `agents/debate.py` | `pytest tests/unit/test_debate_coherence.py` |
| 改交易信号几何 | `analysis/report_engine.py` | `pytest tests/unit/test_financial_review.py` |
| 规则模式一致性门禁 | `tests/tools/coherence_check.py` | `$env:AGENT_MODE="rule"; python tests/tools/coherence_check.py` |
| 金融实跑快照 | `tests/tools/financial_review_run.py` | 输出 `tests/reports/financial_review_snapshot.json` |
| 改新闻分析师逻辑 | `agents/analysts/news.py` | `pytest tests/unit/test_analyst_input_density.py` |
| 接入新外部数据源 | `data/sources/` + `fetch_pipeline.py` | `pytest tests/unit/test_external_sources.py` |
| 金十 MCP 参数 | `config.py` + `jin10_feed.py` | `python tests/run.py --external` |
| 新增 LLM 阶段 | `agents/llm/stages/` + `factory.py` | `pytest tests/unit/test_analyst_team_llm.py tests/unit/test_llm_trade_stages.py` |
| LLM 传输/重试 | `agents/llm/base.py` | `pytest tests/unit/test_llm_transport.py` |
| 改 Streamlit 布局 | `viz/report_views.py` + `viz/dashboard_components.py` | 手工界面 / 用例 catalog `UIL-*` |
| 改外部数据页 | `viz/external_data_view.py` + `views/4_外部数据.py` | `pytest tests/unit/test_external_data_view.py` |
| 改运行前配置/缓存/刷新行为 | `viz/streamlit_common.py` + `core/run_config.py` | 用例 catalog `FN-*` / `pytest tests/unit/test_run_config.py` |
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
| [onboarding.md](../getting-started/onboarding.md) | 首次读项目 |
| [glossary.md](./glossary.md) | 不懂术语 |
| [examples/report-schema.md](../examples/report-schema.md) | 不懂 report JSON |
| [walkthrough.md](../getting-started/walkthrough.md) | 界面操作动线 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
