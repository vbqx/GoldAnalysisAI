# 环境搭建与运行

安装、配置与测试命令速查。心智模型与读码路线见 **[onboarding.md](./onboarding.md)**。

---

## 1. 依赖

- Python 3.10+
- Git
- 可访问 TradingView WebSocket（国内常需代理）

---

## 2. 安装

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

---

## 3. 配置（`.env`）

| 变量 | 默认 | 说明 |
|------|------|------|
| `TV_SYMBOL` | `XAUUSD` | TradingView 品种 |
| `TV_EXCHANGE` | `OANDA` | 交易所 |
| `TV_USERNAME` / `TV_PASSWORD` | 空 | 可选；登录后历史 bar 更多 |
| `JIN10_API_TOKEN` | 空 | 金十 MCP（[申请](https://mcp.jin10.com/app)） |
| `AGENT_MODE` | `rule` | `rule` / `llm` / `hybrid`，见 [llm-agents.md](../design/llm-agents.md) |
| `LLM_*` | 见 `.env.example` | 硅基流动 / OpenAI 兼容 API |

完整变量表见 [handbook.md §2.3](../reference/handbook.md#23-配置env)。

---

## 4. 运行

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

界面操作动线见 [walkthrough.md](./walkthrough.md)。

---

## 5. 测试

```bash
pip install -r requirements-dev.txt
python tests/run.py              # 快速：单元 + 回归（约 88 项，无网络）
python tests/run.py --external     # 外部 API 冒烟
python tests/run.py --financial    # 金融 Review FIN-*
python tests/run.py --full         # 含完整流水线
```

详见 [tests/README.md](../../tests/README.md)。

---

## 6. 对外 API

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
```

| 返回值 | 类型 | 含义 |
|--------|------|------|
| `report` | `dict` | UI 消费的报告 JSON |
| `data` | `dict[str, DataFrame]` | 各周期 K 线 + 指标列 |
| `analyses` | `dict[str, TimeframeAnalysis]` | 各周期结构分析结果 |

流水线步骤权威列表：[pipeline-steps.yaml](../reference/pipeline-steps.yaml)（与 `orchestrator.py` 在 CI 中同步）

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [onboarding.md](./onboarding.md) | 15 分钟开发者入门 |
| [handbook.md](../reference/handbook.md) | 完整数据流与模块参考 |
| [cheat-sheet.md](../reference/cheat-sheet.md) | 改功能速查 |
| [../README.md](../README.md) | 文档中心索引 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
