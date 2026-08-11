# GoldAnalysisAI / TradingAgentCN

面向 XAUUSD 的人工审核交易建议系统。它读取多周期行情和外部背景，生成一份可证伪、可追溯的 Advice V2 建议；系统本身不执行交易。

## 输出

每次运行只返回以下之一：

- `WATCH_LONG`：等待人工确认做多条件；
- `WATCH_SHORT`：等待人工确认做空条件；
- `WAIT`：证据不足或高周期冲突；
- `AVOID`：数据时效或审计不合格。

Watch 方案最多一个，包含关注区、确认清单、失效位、1–2 个目标、证据和风险收益比。可选 LLM 只润色文字，不能修改方向或数字。

## 启动

```powershell
Copy-Item .env.example .env
python run_app.py
```

默认地址：`http://localhost:8501`。不要直接运行 `streamlit run app.py`。

## 验证

```powershell
python tests/run.py
python tests/run.py --full
python scripts/inspect_archive.py list
```

## 文档

- [开发者上手](docs/operations/onboarding.md)
- [系统概览](docs/aspice/SWE.2-architecture/system-overview.md)
- [人工审核建议架构](docs/aspice/SWE.2-architecture/human-review-advice.md)
- [修改速查](docs/aspice/SWE.3-detailed-design/reference/cheat-sheet.md)
- [ASPICE 软件域入口](docs/aspice/software-domain.md)
