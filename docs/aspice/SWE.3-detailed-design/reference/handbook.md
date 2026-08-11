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
| V2 报告 | `src/advice/report.py` | `test_export_sample_report.py` |
| 归档和回放 | `src/run/archive/`、`src/viz/replay_loader.py` | `test_archive_*.py` |
| 界面 | `src/viz/advice_view.py` | UI helper tests + manual review |

决策只能是 `WAIT`、`WATCH_LONG`、`WATCH_SHORT`、`AVOID`。任何自动执行、仓位授权、多方案竞选或 Agent 辩论都不属于 Advice V2。
