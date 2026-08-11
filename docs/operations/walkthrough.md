# Advice V2 代码导览

`src.pipeline.run_analysis()` 调用 `run_advice_pipeline()`，并保持 `(report, data, analyses)` 返回形状。

```text
fetch -> indicators -> structure -> advice -> report -> archive
```

- `fetch`: `src/data/fetch_pipeline.py` 聚合行情与外部背景。
- `indicators`: `src/indicators/technical.py` 补全技术指标。
- `structure`: `src/analysis/ict_pa.py` 生成各周期结构事实。
- `advice`: `src/advice/engine.py` 只形成一个首选方案或无方案，`src/advice/audit.py` 检查几何与证据。
- `report`: `src/advice/report.py` 组装 `human_review_advice` v2。
- `archive`: `src/run/archive/` 保存运行，`src/viz/replay_loader.py` 负责回放与旧归档重建。

可选 LLM 路径在 `src/advice/llm.py`：模型只能编辑文字，不能改方向和数值。

调试生成内容时按顺序看：`report.advice.decision`、`primary_setup`、`evidence`、`audit`、`meta.data_as_of`。不要再查找 V1 的 `signals` 或 `agent_trace`；它们已退出当前契约。
