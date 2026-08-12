# Advice V2 修改速查

主流程：`fetch` → `indicators` → `structure` → `advice` → `report` → `archive`。

| 想改什么 | 文件 |
|---|---|
| 方向一致性规则 | `src/advice/engine.py::_bias` |
| 关注区共振 | `src/advice/engine.py::_pick_cluster` |
| 目标和失效位 | `src/advice/engine.py::_target_prices`、`build_advice_packet` |
| 人工确认清单 | `src/advice/engine.py::_human_checklist` |
| 硬性审计 | `src/advice/audit.py` |
| 报告字段 | `src/advice/report.py`、`src/advice/types.py` |
| LLM 允许编辑的字段 | `src/advice/llm.py` |
| 默认 LLM 提供商与模型 | `src/config.py`、`.env.example` |
| LLM 思考过程页 | `src/viz/llm_process_view.py`、`views/3_LLM思考过程.py` |
| 生成中 LLM 流式面板 | `src/viz/pipeline_progress.py`、`src/viz/streamlit_common.py` |
| 主卡片展示 | `src/viz/advice_view.py` |
| 旧归档重建 | `src/viz/replay_loader.py` |

每次修改建议逻辑至少运行：

```powershell
python -m pytest tests/unit/test_advice_v2.py -q
python -m pytest tests/integration/test_offline_report_contract.py -m integration -q
python tests/run.py
```

新增流水线阶段时同步本目录的 `pipeline-steps.yaml` 及四份流程文档。
