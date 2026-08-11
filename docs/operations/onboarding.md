# 15 分钟开发者上手

## 启动

```powershell
Copy-Item .env.example .env
python run_app.py
```

不要直接运行 `streamlit run app.py`；项目启动器负责加载 `.env`、清理遗留进程并设置 UTF-8。默认地址是 `http://localhost:8501`。

## 当前产品边界

系统生成一份供人工审核的 XAUUSD 建议，不自动下单。报告契约是 Advice V2：最多一个首选方案，或明确返回 `WAIT` / `AVOID`。

## 流水线

权威清单是 [pipeline-steps.yaml](../aspice/SWE.3-detailed-design/reference/pipeline-steps.yaml)：

1. `fetch` — 数据拉取
2. `indicators` — 计算技术指标
3. `structure` — 提取市场结构
4. `advice` — 生成人工审核建议
5. `report` — 组装人工审核卡
6. `archive` — 运行归档

主要入口：`src/core/orchestrator.py`。建议策略：`src/advice/engine.py`。确定性审计：`src/advice/audit.py`。界面：`src/viz/advice_view.py`。

## 验证

```powershell
python tests/run.py
python tests/run.py --full
python scripts/check_aspice_assets.py --check
```

历史运行可用 `python scripts/inspect_archive.py list` 查看。回放不抓取新数据、不调用 LLM；旧 V1 归档会从保存的数据重建 Advice V2。
