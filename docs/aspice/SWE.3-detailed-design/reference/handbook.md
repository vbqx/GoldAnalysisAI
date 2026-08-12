# Advice V2 工程手册

## 端到端调用

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
```

流水线固定为：`fetch` → `indicators` → `structure` → `advice` → `report` → `archive`。

| 关注点 | 修改位置 | 主要测试 |
|---|---|---|
| 数据源与降级 | `src/data/` | `test_external_sources.py`、`test_http_helpers.py` |
| 指标与结构 | `src/indicators/`、`src/analysis/` | `test_indicators.py`、`test_ict_pa.py` |
| 建议选择 | `src/advice/engine.py` | `test_advice_v2.py` |
| 几何和证据审计 | `src/advice/audit.py` | `test_advice_v2.py` |
| LLM 文案边界 | `src/advice/llm.py` | `test_advice_v2.py`、`test_llm_stage_policy.py` |
| LLM 思考过程与流式面板 | `src/viz/llm_process_view.py`、`src/viz/pipeline_progress.py` | `test_llm_process_view.py`、`test_live_llm_process_panel.py` |
| 默认 LLM 提供商配置 | `src/config.py`、`.env.example` | `test_llm_config.py` |
| V2 报告 | `src/advice/report.py` | `test_export_sample_report.py`、`test_offline_report_contract.py` |
| 归档和回放 | `src/run/archive/`、`src/viz/replay_loader.py` | `test_archive_*.py` |
| 界面 | `src/viz/advice_view.py`、`views/3_LLM思考过程.py` | UI helper tests + manual review |

决策只能是 `WAIT`、`WATCH_LONG`、`WATCH_SHORT`、`AVOID`。任何自动执行、仓位授权、多方案竞选或 Agent 辩论都不属于 Advice V2。

## 可选 LLM 与审计页

- 默认文案模型：`deepseek-ai/DeepSeek-V4-Flash`（硅基流动 `https://api.siliconflow.cn/v1`），见 `.env.example`。
- `views/3_LLM思考过程.py` 展示 `meta.generation_steps`、`meta.llm_io` 与 `advisor_trace`；不是 V1 决策链。
- 离线契约：`tests/integration/test_offline_report_contract.py` 校验样例报告与 `build_advice_report()` 输出符合 Advice V2 契约。
