# GoldAnalysisAI — XAUUSD PA+ICT 分析报告

基于 Price Action + ICT + SMC 方法论，自动生成 XAUUSD 机构级分析仪表盘。内部流水线参考 [TradeAgent](https://github.com/TauricResearch/TradingAgents) 多智能体架构。

## 快速开始

```bash
git clone https://github.com/vbqx/GoldAnalysisAI.git
cd GoldAnalysisAI
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
copy .env.example .env          # 按需配置 TradingView
streamlit run app.py
```

浏览器打开 `http://localhost:8501` 即可查看报告。

## 文档

| 文档 | 说明 |
|------|------|
| [docs/development.md](docs/development.md) | 开发文档 — 环境、架构、读码顺序、扩展 |
| [docs/architecture.md](docs/architecture.md) | 架构设计与 TradeAgent 对照 |
| [docs/reverse-engineering.md](docs/reverse-engineering.md) | 原报告结构反推 |

## 项目结构

```
GoldAnalysisAI/
├── app.py                      # Streamlit 仪表盘入口
├── requirements.txt
├── docs/
│   ├── development.md          # 开发文档
│   ├── architecture.md         # 架构设计
│   └── reverse-engineering.md  # 原报告实现反推
└── src/
    ├── pipeline.py             # 分析主流程（→ orchestrator）
    ├── core/                   # 类型定义 + 流水线编排
    ├── agents/                 # 多空研究 / 辩论 / 交易 / 风控 / 经理
    ├── data/                   # TradingView 数据 + 可插拔数据源
    ├── indicators/technical.py # EMA / VWAP / Fibonacci
    ├── analysis/
    │   ├── ict_pa.py           # BOS / CHoCH / OB / FVG
    │   └── report_engine.py    # 报告组装 + 交易计划
    └── viz/                    # Streamlit 渲染组件
```

## MVP 能力

| 模块 | 状态 |
|------|------|
| 实时价格 / 日涨跌 | ✅ TradingView |
| 多周期结构 (5m/15m/1h/4h) | ✅ 简化 swing 算法 |
| BOS / CHoCH | ✅ 突破前高/前低 |
| Order Block / FVG | ✅ 启发式检测 |
| EMA20/50/610 + VWAP | ✅ |
| Fibonacci 回调 | ✅ |
| 多空胜率饼图 | ✅ 多周期加权 |
| 交易计划卡片 | ✅ 自动生成 |
| 趋势路径投影 | ✅ 三路径概率 |
| 多智能体流水线 | ✅ 研究 / 辩论 / 风控 / 经理 |

## 数据源

**默认：TradingView**（`OANDA:XAUUSD`，通过 [tvdatafeed](https://github.com/rongardF/tvdatafeed) 非官方 WebSocket 接口）

复制 `.env.example` 为 `.env` 并按需配置：

```env
TV_SYMBOL=XAUUSD
TV_EXCHANGE=OANDA
TV_USERNAME=          # 可选，登录后可获取更多历史数据
TV_PASSWORD=
```

常见黄金 symbol（在 TradingView 搜索后填入）：

| 交易所 | Symbol | 说明 |
|--------|--------|------|
| OANDA | XAUUSD | 默认，外汇黄金 |
| TVC | GOLD | TradingView 综合 |
| CAPITALCOM | GOLD | CFD |

**注意：** TradingView 无官方免费 API；`tvdatafeed` 为第三方库。国内网络连接 TradingView WebSocket 可能需要代理/VPN。

## 下一步扩展

1. **LLM 文案层** — 用 GPT/Claude 将结构化 JSON 转为自然语言结论
2. **DXY 联动** — 拉取美元指数并量化对黄金的影响
3. **HTML/PDF 导出** — 生成与群友报告一致的静态图片
4. **回测** — 验证 OB/FVG 信号历史胜率

## 免责声明

本项目仅供学习研究，不构成投资建议。
