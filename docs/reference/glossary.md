# 术语表

GoldAnalysisAI 文档与代码中的常见术语。算法细节见 [reverse-engineering.md](../archive/domain/reverse-engineering.md)。

---

## 项目与架构

| 术语 | 含义 |
|------|------|
| **GoldAnalysisAI** | 本仓库：XAUUSD 分析报告生成器 + Streamlit 网页仪表盘 |
| **TradingAgents** | 开源多智能体交易研究框架；本项目**参考其分层设计**，非直接依赖 |
| **分析师团队（Analyst Team）** | 四位按信息类型分工：技术 / 基本面 / 新闻 / 情绪 |
| **研究员** | 看多（Bullish）、看空（Bearish）智能体，按**交易方向**整合 ICT 与分析师同向证据 |
| **智能体（Agent）** | 流水线中的一个决策阶段（规则函数或大模型包装）；不等于「全程都是 LLM」 |
| **factory（工厂）** | `src/agents/factory.py`，统一调度规则 / 纯 LLM / 混合 三种模式 |
| **orchestrator（编排器）** | `src/core/orchestrator.py`，端到端流水线编排 |
| **MarketContext** | 流水线共享的只读上下文：K 线、结构分析、外部因子、二次加工摘要（derived） |
| **AgentTrace** | 写入 `report["agent_trace"]` 的完整决策审计链 |

---

## 运行模式

| 术语 | 含义 |
|------|------|
| **rule（规则模式）** | `AGENT_MODE=rule`，全部走 Python 规则，最快最稳定 |
| **llm（纯大模型）** | 启用阶段优先调用 LLM；失败则回退规则 |
| **hybrid（混合模式）** | 规则先出结果；仅当 LLM 置信度超过阈值才覆盖 |
| **stage_sources** | `report["meta"]["stage_sources"]`，记录每阶段实际用规则还是 LLM |
| **llm_io** | `report["meta"]["llm_io"]`，规则阶段与 LLM 阶段的输入输出审计 |
| **LLM 报告文案** | 流水线**末尾** `llm/analyst.py` 润色结论，独立于分析师团队 |

---

## 金融与 ICT/PA

| 术语 | 含义 |
|------|------|
| **XAUUSD** | 黄金/美元 spot，默认分析品种 |
| **PA（Price Action，价格行为）** | 基于 K 线结构与关键位的分析 |
| **ICT** | Inner Circle Trader 方法论；本项目为**启发式简化版** |
| **SMC（Smart Money Concepts）** | 与 ICT 类似的机构资金流叙事 |
| **摆动高/低点（Swing）** | 局部极值，结构检测的基础 |
| **BOS（Break of Structure）** | 结构突破，顺势延续信号 |
| **CHoCH（Change of Character）** | 性质转变，原趋势可能反转 |
| **OB（Order Block，订单块）** | 推动 K 线前最后一根反向 K 线所在区域 |
| **FVG（Fair Value Gap，公平价值缺口）** | 三根 K 线形成的价格缺口 |
| **流动性区（Liquidity）** | 等高/等低、扫止损等价位聚集区 |
| **溢价/折价区** | 相对最近 swing 区间的上方/下方 |
| **win_rate（报告字段名）** | ⚠️ **不是历史胜率**；已逐步替换为 `sentiment_bias_pct`（结构偏多/偏空权重 %） |
| **sentiment_bias_pct** | 信号卡片展示的「结构权重」，数值来自 `sentiment_score` 对应分量（如 bearish 45%） |
| **sentiment_score** | 多周期趋势加权 → 饼图多/空/震荡比例 |
| **coherence_check** | `tests/tools/coherence_check.py` — 规则模式跑完整流水线，校验结论/辩论/信号几何一致性；P0 门禁 |
| **主策略 / 逆势备选** | `signal_role`：`primary` 与结构主导方向一致；`alternate` 为逆势方案，UI 徽章区分 |
| **risk_reward** | 风险收益比展示；> 1:8 时标注「远端限价」 |

---

## 数据与外部源

| 术语 | 含义 |
|------|------|
| **TradingView / tvdatafeed** | 非官方接口拉 OHLCV；2 次请求 + 本地聚合多周期 |
| **金十 MCP** | 官方接口：快讯、资讯、日历、报价、K 线 |
| **DXY** | 美元指数；偏强通常利空黄金 |
| **US10Y** | 美国 10 年期国债收益率，宏观参考 |
| **实时 / 占位 / 回退** | 外部数据：拉取成功 / 失败占位文案 / 界面应区分展示 |
| **context_stats** | 分析师输入密度计数，在 `report["meta"]["context_stats"]` |
| **derived / 二次加工摘要** | 由 `context_builder` 在 fetch 阶段生成的基础字段；完整报告后含新闻主题、spot 交叉校验等。界面标签为「二次加工摘要」，见 **外部数据** 页 |

---

## 界面与 Streamlit

| 术语 | 含义 |
|------|------|
| **ensure_report()** | 界面入口：会话缓存 + 后台线程跑完整流水线 |
| **ensure_external_data()** | 外部数据页入口：fetch 完成后即可展示 `report.external`，不等待 LLM |
| **重新配置 / 刷新报告** | 侧边栏操作：清空缓存并回到生成前配置面板（预填上次 RunConfig），确认后重跑流水线 |
| **generation_steps** | 生成进度与耗时，对应 `docs/reference/pipeline-steps.yaml` |
| **LLM决策链页** | 第三个导航页：决策链 + LLM 输入输出 |

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [onboarding.md](../operations/onboarding.md) | 15 分钟开发者入门 |
| [cheat-sheet.md](./cheat-sheet.md) | 改功能速查 |
| [examples/report-schema.md](./examples/report-schema.md) | 报告 JSON 字段说明 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
