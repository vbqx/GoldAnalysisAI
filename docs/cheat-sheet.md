# 开发者速查表（Cheat Sheet）

一页纸回答：**我想改 X，该动哪个文件、跑什么测试**。  
流水线步骤权威列表见 [pipeline-steps.yaml](./pipeline-steps.yaml)（CI 与代码同步校验）。

---

## 流水线步骤 → 代码

| 步骤 ID | 中文 | 主文件 | LLM |
|---------|------|--------|-----|
| `fetch` | 数据拉取 | `data/fetch_pipeline.py` | 否 |
| `indicators` | 技术指标 | `indicators/technical.py` | 否 |
| `ict` | ICT 结构 | `analysis/ict_pa.py` | 否 |
| `analyst_team` | Analyst Team | `agents/analysts/*` + `factory.py` | 可选 |
| `bullish` | 看多研究 | `agents/bullish.py` + `factory.py` | 可选 |
| `bearish` | 看空研究 | `agents/bearish.py` + `factory.py` | 可选 |
| `debate` | 多空辩论 | `agents/debate.py` + `factory.py` | 可选 |
| `trader` | 交易员 | `agents/trader.py` | 否 |
| `risk` | 风控 | `agents/risk.py` | 否 |
| `manager` | 经理 | `agents/manager.py` | 否 |
| `report` | 组装报告 | `analysis/report_engine.py` | 否 |
| `llm_narrative` | LLM 文案 | `llm/analyst.py` | 可选 |

---

## 改功能 → 文件 → 测试

| 我想… | 改这里 | 验证 |
|-------|--------|------|
| 调整 EMA/VWAP/Fib | `indicators/technical.py` | `pytest tests/unit/test_indicators.py` |
| 调整 Swing/BOS/OB/FVG | `analysis/ict_pa.py` | 手工看 `analyses["5m"]` 或 DEBUG 日志 |
| 改交易信号几何 | `analysis/report_engine.py` | `pytest tests/unit/test_financial_review.py` |
| 改辩论/共识逻辑 | `agents/debate.py` | 单元测试 + 看 `agent_trace.debate` |
| 改 Analyst 新闻逻辑 | `agents/analysts/news.py` | `pytest tests/unit/test_analyst_input_density.py` |
| 接入新外部数据源 | `data/sources/` + `fetch_pipeline.py` | `pytest tests/unit/test_external_sources.py` |
| 金十 MCP 参数 | `config.py` + `jin10_feed.py` | `python tests/run.py --external` |
| 新增 LLM 阶段 | `agents/llm/stages/` + `factory.py` | `pytest tests/unit/test_analyst_team_llm.py` |
| LLM 传输/重试 | `agents/llm/base.py` | `pytest tests/unit/test_llm_transport.py` |
| 改 Streamlit 布局 | `viz/report_views.py` | 手工 UI / catalog `UIL-*` |
| 改缓存/刷新行为 | `viz/streamlit_common.py` | catalog `FN-*` |
| 改进度条/I/O 展示 | `viz/pipeline_progress.py` | 手工生成报告 |
| 改流水线顺序 | `core/orchestrator.py` + **`docs/pipeline-steps.yaml`** | `pytest tests/regression/test_doc_pipeline_sync.py` |

---

## 配置速查

| 变量 | 典型值 | 作用 |
|------|--------|------|
| `AGENT_MODE` | `rule` / `llm` / `hybrid` | 智能体调度模式 |
| `LLM_ENABLED` | `true` / `false` | 报告文案层开关 |
| `LLM_STAGE_ANALYSTS` | `true` | Analyst Team LLM |
| `LLM_STAGE_RESEARCH` | `true` | 看多/看空 LLM |
| `LLM_STAGE_DEBATE` | `true` | 辩论 LLM |
| `JIN10_API_TOKEN` | — | 金十 MCP |
| `LOG_LEVEL` | `DEBUG` | 跟踪流水线 |

完整列表见 `.env.example` 与 [development-reference.md §2.3](./development-reference.md#23-配置env)。

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

# 3. 每阶段 rule 还是 llm
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
| `report` | `viz/*` 全部 UI |
| `data` | K 线图表 |
| `analyses` | 结构 overlay |

---

## 相关文档

| 文档 | 何时用 |
|------|--------|
| [developer-onboarding.md](./developer-onboarding.md) | 首次读项目 |
| [glossary.md](./glossary.md) | 不懂术语 |
| [examples/report-schema.md](./examples/report-schema.md) | 不懂 report JSON |
| [walkthrough.md](./walkthrough.md) | UI 操作动线 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
