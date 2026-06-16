# 术语表（Glossary）

GoldAnalysisAI 文档与代码中常见术语速查。算法细节见 [reverse-engineering.md](./reverse-engineering.md)。

---

## 项目与架构

| 术语 | 含义 |
|------|------|
| **GoldAnalysisAI** | 本仓库：XAUUSD 分析报告生成器 + Streamlit 仪表盘 |
| **TradingAgents** | 开源多智能体交易研究框架；本项目流水线**参考其分层**，非直接依赖 |
| **Analyst Team** | 四位按信息类型分工的分析师：Technical / Fundamentals / News / Sentiment |
| **研究员（Researcher）** | Bullish / Bearish 智能体，按**交易方向**整合 ICT + Analyst 同向证据 |
| **Agent / 智能体** | 流水线中一个决策阶段（含规则函数或 LLM 包装）；不等于「全是 LLM」 |
| **factory** | `src/agents/factory.py`，统一调度 rule / llm / hybrid |
| **orchestrator** | `src/core/orchestrator.py`，端到端流水线编排 |
| **MarketContext** | 流水线共享只读上下文：K 线、结构分析、外部因子、derived 信号 |
| **AgentTrace** | 写入 `report["agent_trace"]` 的完整决策审计链 |

---

## 运行模式

| 术语 | 含义 |
|------|------|
| **rule** | `AGENT_MODE=rule`，全部走 Python 规则，最快最稳定 |
| **llm** | 启用阶段优先大模型；失败回退规则 |
| **hybrid** | 规则 baseline + LLM 置信度超阈值才覆盖 |
| **stage_sources** | `report["meta"]["stage_sources"]`，记录每阶段实际 rule/llm |
| **llm_io** | `report["meta"]["llm_io"]`，规则阶段 I/O + LLM Prompt/响应审计 |
| **LLM 报告文案** | 流水线**末尾** `llm/analyst.py` 润色，独立于 Analyst Team |

---

## 金融与 ICT/PA

| 术语 | 含义 |
|------|------|
| **XAUUSD** | 黄金/美元 spot 品种，默认分析对象 |
| **PA（Price Action）** | 价格行为分析，关注 K 线结构与关键位 |
| **ICT** | Inner Circle Trader 方法论；本项目为**启发式 MVP**，非完整 ICT |
| **SMC** | Smart Money Concepts，与 ICT 类似的机构流叙事 |
| **Swing High/Low** | 局部摆动高低点，结构检测基础 |
| **BOS** | Break of Structure，顺势结构突破 |
| **CHoCH** | Change of Character，逆原趋势的结构转变 |
| **OB（Order Block）** | 订单块：推动 K 线前最后一根反向 K 线区域 |
| **FVG（Fair Value Gap）** | 公平价值缺口：三根 K 线价格缺口 |
| **Liquidity** | 流动性区：equal highs/lows、扫流动性等 |
| **Premium / Discount** | 相对最近 swing 区间的溢价/折价区 |
| **win_rate（报告字段）** | ⚠️ **非历史胜率**；实为 `sentiment_score` 结构偏多权重 |
| **sentiment_score** | 多周期趋势加权投票 → 饼图 bullish/bearish/ranging |
| **risk_reward** | 报告展示的风险收益比；部分模板仍为固定字符串（见 F-003） |

---

## 数据与外部源

| 术语 | 含义 |
|------|------|
| **TradingView / tvdatafeed** | 非官方 WebSocket 拉 OHLCV；2 次请求 + 本地 resample |
| **金十 MCP** | 官方 MCP 接口：快讯、资讯、日历、quote、kline |
| **DXY** | 美元指数，TradingView `TVC:DXY`；偏强通常利空黄金 |
| **US10Y** | 10 年期美债收益率宏观参考 |
| **live / placeholder / fallback** | 外部数据状态：实时拉取成功 / 拉取失败占位 / UI 应区分展示 |
| **context_stats** | Analyst 输入密度计数，写入 `report["meta"]["context_stats"]` |
| **derived** | `context_builder` 产出：news_topics、spot_cross_check、event_countdown 等 |

---

## UI 与 Streamlit

| 术语 | 含义 |
|------|------|
| **ensure_report()** | `streamlit_common.py` 入口：session 缓存 + 后台线程跑流水线 |
| **刷新报告** | 唯一强制重跑流水线的用户操作（另：浏览器刷新） |
| **generation_steps** | 生成进度步骤与耗时，对应 `docs/pipeline-steps.yaml` |
| **LLM决策链页** | `views/3_LLM决策链.py`：决策链 + LLM I/O 三 Tab |

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [developer-onboarding.md](./developer-onboarding.md) | 15 分钟开发者入门 |
| [cheat-sheet.md](./cheat-sheet.md) | 改功能速查 |
| [examples/report-schema.md](./examples/report-schema.md) | 报告 JSON 字段说明 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
