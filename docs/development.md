# GoldAnalysisAI 开发文档

说明本仓库的架构、执行路径、模块职责与扩展方式。  
**文档索引**：[docs/README.md](./README.md)

---

## 读哪份文档？

| 你的目标 | 读这个 |
|----------|--------|
| 15 分钟搞懂项目、知道从哪读代码 | **[developer-onboarding.md](./developer-onboarding.md)** |
| 查函数链、模块细节、调试 FAQ | **[development-reference.md](./development-reference.md)** |
| 不懂术语（BOS、混合模式、分析师团队） | **[glossary.md](./glossary.md)** |
| 改功能不知道动哪个文件 | **[cheat-sheet.md](./cheat-sheet.md)** |
| 看报告 JSON 长什么样 | **[examples/report-schema.md](./examples/report-schema.md)** |
| 界面操作与页面动线 | **[walkthrough.md](./walkthrough.md)** |

---

## 1. 项目是什么

GoldAnalysisAI 是一个 **XAUUSD 分析报告生成器**：

1. 从 TradingView 拉多周期 OHLCV；
2. 计算 EMA/VWAP/Fib，做 ICT/PA 结构检测（BOS、CHoCH、OB、FVG）；
3. 经 **Analyst Team**（技术/基本面/新闻/情绪）与多空研究 → 辩论 → 交易 → 风控 → 经理 流水线产出交易提案；
4. 组装为 JSON 报告，由 Streamlit 渲染为网页仪表盘。

**对外稳定接口**（重构内部时尽量保持不变）：

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
```

| 返回值 | 类型 | 含义 |
|--------|------|------|
| `report` | `dict` | UI 消费的报告 JSON |
| `data` | `dict[str, DataFrame]` | 各周期 K 线 + 指标列 |
| `analyses` | `dict[str, TimeframeAnalysis]` | 各周期结构分析结果 |

**技术栈**：Python 3.10+ · Streamlit · pandas/numpy · Plotly · tvdatafeed（TradingView 非官方 WebSocket）

**设计约束**：

- UI 只依赖 `report` dict，不直接依赖 agents 层；
- 内部流水线参考 [TradingAgents](https://github.com/TauricResearch/TradingAgents)（两阶段研究：Analyst Team → Bull/Bear）；
- 数据源通过 Protocol 解耦，便于替换实现。

**流水线步骤权威列表**：[pipeline-steps.yaml](./pipeline-steps.yaml)（与 `orchestrator.py` 在 CI 中同步）

---

## 2. 环境搭建

### 2.1 依赖

- Python 3.10+
- Git
- 可访问 TradingView WebSocket（国内常需代理）

### 2.2 安装

```bash
git clone https://github.com/vbqx/GoldAnalysisAI.git
cd GoldAnalysisAI

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
copy .env.example .env          # Windows
# cp .env.example .env
```

### 2.3 配置（`.env`）

| 变量 | 默认 | 说明 |
|------|------|------|
| `TV_SYMBOL` | `XAUUSD` | TradingView 品种 |
| `TV_EXCHANGE` | `OANDA` | 交易所 |
| `TV_USERNAME` / `TV_PASSWORD` | 空 | 可选；登录后历史 bar 更多 |
| `JIN10_API_TOKEN` | 空 | 金十 MCP（[申请](https://mcp.jin10.com/app)） |
| `AGENT_MODE` | `rule` | `rule` / `llm` / `hybrid`，见 [llm-agents.md](./llm-agents.md) |
| `LLM_*` | 见 `.env.example` | 硅基流动 / OpenAI 兼容 API |

完整变量表见 [development-reference.md §2.3](./development-reference.md#23-配置env)。

### 2.4 运行

```bash
streamlit run app.py    # http://localhost:8501
```

**多页面**（`st.navigation` 左侧导航）：

| 页面 | 文件 |
|------|------|
| 机构级分析报告 | `views/1_机构级分析报告.py` |
| 短线策略 | `views/2_短线策略.py` |
| LLM决策链 | `views/3_LLM决策链.py` |

**缓存策略**：`ensure_report()` 先显示生成前配置面板；用户点击 **「开始生成报告」** 后，后台线程跑流水线并写入 session 缓存。切换页面**不**重跑；点 **「重新配置 / 刷新报告」** 会清空缓存并回到配置面板。

### 2.5 测试

```bash
pip install -r requirements-dev.txt
python tests/run.py              # 快速：单元 + 回归（约 77 项，无网络）
python tests/run.py --external     # 外部 API 冒烟
python tests/run.py --financial    # 金融 Review FIN-*
python tests/run.py --full         # 含完整流水线
```

详见 [tests/README.md](../tests/README.md)。

---

## 3. 详细参考（分册）

以下内容已拆分至专门文档，避免单文件过长：

| 主题 | 文档 |
|------|------|
| 完整数据流与函数调用链（§3.1–3.9） | [development-reference.md §3](./development-reference.md#3-整体数据流与函数调用链) |
| 目录结构与读码顺序 | [development-reference.md §4](./development-reference.md#4-目录结构与读码顺序) |
| 核心模块说明 | [development-reference.md §5](./development-reference.md#5-核心模块说明) |
| 领域类型 | [development-reference.md §6](./development-reference.md#6-领域类型coretypespy) |
| 开发与扩展 | [development-reference.md §7](./development-reference.md#7-开发与扩展) |
| 调试 / 性能 / FAQ / 路线图 | [development-reference.md §8–11](./development-reference.md#8-调试) |

---

## 4. 相关文档

| 文档 | 内容 |
|------|------|
| [README.md](./README.md) | 文档中心索引 |
| [developer-onboarding.md](./developer-onboarding.md) | 开发者 15 分钟入门 |
| [cheat-sheet.md](./cheat-sheet.md) | 改功能速查 |
| [glossary.md](./glossary.md) | 术语表 |
| [architecture.md](./architecture.md) | TradingAgents 对照 |
| [llm-agents.md](./llm-agents.md) | LLM 双轨调度 |
| [walkthrough.md](./walkthrough.md) | UI 操作动线 |
| [examples/report-schema.md](./examples/report-schema.md) | 报告 JSON 说明 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
