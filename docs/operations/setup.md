# 环境搭建与运行

安装、配置与测试命令速查。心智模型与读码路线见 **[onboarding.md](./onboarding.md)**。

---

## 1. 依赖

- CPython 3.12（当前受控与 CI 验证基线；其他版本未纳入本基线）
- Git
- 可访问 TradingView WebSocket（国内常需代理）
- 可选：MetaTrader 5 Windows 终端 + `MetaTrader5` Python 包（仅账号检查/下单执行接口需要）

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
| `MT5_ENABLED` | `false` | 可选；启用 MT5 账号/执行接口，不改变 K 线数据源 |
| `MT5_ACCOUNT` / `MT5_PASSWORD` / `MT5_SERVER` | 空 | MT5 模拟/实盘账户；只写入本机 `.env` |
| `MT5_PATH` / `MT5_TIMEOUT_MS` | 空 / `10000` | 可选；指定 `terminal64.exe` 路径与 IPC 初始化超时 |
| `JIN10_API_TOKEN` | 空 | 金十 MCP（[申请](https://mcp.jin10.com/app)） |
| `AGENT_MODE` | `rule` | `rule` / `llm` / `hybrid`，见 [llm-agents.md](../aspice/SWE.2-architecture/llm-agents.md) |
| `LLM_*` | 见 `.env.example` | 硅基流动 / OpenAI 兼容 API |

完整变量表见 [handbook.md §2.3](../aspice/SWE.3-detailed-design/reference/handbook.md#配置速查)。

### MT5 账号连接自检

1. 在 Windows 上安装并打开 MetaTrader 5 终端。
2. 将模拟账户写入 `.env`：`MT5_ENABLED=true`、`MT5_ACCOUNT`、`MT5_PASSWORD`、`MT5_SERVER`、`MT5_SYMBOL`。
3. 安装可选依赖：`pip install MetaTrader5`。
4. 运行：

```bash
python scripts/check_mt5_connection.py
```

自检脚本只打印非敏感账号摘要，不读取 K 线，不打印密码，不发送订单。

---

## 4. 运行

**请用官方启动脚本**，不要直接 `streamlit run app.py`。脚本会：

1. 加载项目根目录 `.env` 到进程环境变量
2. 设置 UTF-8 开发终端变量
3. 终止本仓库残留的 Streamlit / `app.py` 进程
4. 启动 Streamlit（默认 `http://localhost:8501`）

```bash
# 跨平台（推荐）
python run_app.py

# 快捷方式
.\run_app.bat          # Windows
./run_app.sh           # Linux / macOS

# 自定义端口
python run_app.py --port 8503
```

AI 代理与自动化工具见根目录 **[AGENTS.md](../../AGENTS.md)**。

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

流水线步骤权威列表：[pipeline-steps.yaml](../aspice/SWE.3-detailed-design/reference/pipeline-steps.yaml)（与 `orchestrator.py` 在 CI 中同步）

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [onboarding.md](./onboarding.md) | 15 分钟开发者入门 |
| [handbook.md](../aspice/SWE.3-detailed-design/reference/handbook.md) | 完整数据流与模块参考 |
| [cheat-sheet.md](../aspice/SWE.3-detailed-design/reference/cheat-sheet.md) | 改功能速查 |
| [../README.md](../README.md) | 文档中心索引 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
