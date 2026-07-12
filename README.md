# GoldAnalysisAI — XAUUSD PA+ICT 分析报告

基于 Price Action + ICT + SMC 方法论，自动生成 XAUUSD 机构级分析仪表盘。内部流水线参考 [TradingAgents](https://github.com/TauricResearch/TradingAgents)：**Analyst Team**（技术/基本面/新闻/情绪）→ 多空研究 → 辩论 → 交易 → 风控 → 经理；支持规则引擎与 LLM 双轨。

## 快速开始

```bash
git clone https://github.com/vbqx/GoldAnalysisAI.git
cd GoldAnalysisAI

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
copy .env.example .env          # Windows
# cp .env.example .env

# 启动（官方：跨平台 run_app.py；勿直接 streamlit run app.py）
python run_app.py
# Windows 快捷: .\run_app.bat
# Linux/macOS:   ./run_app.sh
```

浏览器打开 `http://localhost:8501`。启动后先在 **生成前配置** 面板选择规则 / LLM / 混合模式，点击「开始生成报告」后才拉取数据并生成报告。每次生成会自动归档；勾选 **历史回放** 可 **0 token** 即时查看已保存报告（不重跑 LLM）。

> **AI / 自动化**：见 [AGENTS.md](AGENTS.md)；统一用 `python run_app.py` 启动。

## 多页面导航

| 页面 | 文件 | 说明 |
|------|------|------|
| 机构级分析报告 | `views/1_机构级分析报告.py` | 机构完整报告，主图 5 分钟 |
| 外部数据 | `views/4_外部数据.py` | 新闻/日历/DXY/社媒，**fetch 完成后即可查看** |
| 短线策略 | `views/2_短线策略.py` | 短线策略图，**切换不重新生成** |
| LLM决策链 | `views/3_LLM决策链.py` | 智能体决策、LLM 文案、生成与智能体 I/O |

报告在 session 中缓存；后台线程生成，等待时可在 **「生成与 LLM I/O」** Tab 查看实时步骤与 **LLM 实时推理**（chunk 流式刷新）。仅点 **「重新配置 / 刷新报告」** 并再次确认配置后才重跑（规则模式约 30s；启用 LLM 全流程可能 5–6 分钟）。

**手动验证 Analyst 输入密度**：生成完成后在「LLM决策链」页查看 `context_stats`、`news_topics`、`spot_cross_check`；报告 `meta.context_stats` 与 `external` 块含结构化计数。

## 文档

完整索引见 **[docs/README.md](docs/README.md)**。

| 文档 | 说明 |
|------|------|
| **[docs/overview/project.md](docs/overview/project.md)** | **项目定位与 owner 读法** |
| [docs/overview/status.md](docs/overview/status.md) | 当前状态、剩余风险、建议顺序 |
| [docs/overview/codex-autonomy.md](docs/overview/codex-autonomy.md) | 给 Codex 持续自动优化的目标模板 |
| [docs/operations/setup.md](docs/operations/setup.md) | 本地 / VPS / MT5 / 环境变量运行手册 |
| [docs/architecture/architecture.md](docs/architecture/architecture.md) | 系统架构与 TradingAgents 对照 |
| [docs/architecture/review.md](docs/architecture/review.md) | 架构体检：保留、合并、延后边界 |
| [docs/testing/strategy.md](docs/testing/strategy.md) | fast / scenario / release 测试策略 |
| [docs/reference/handbook.md](docs/reference/handbook.md) | 开发参考手册（调用链速查） |

## 项目结构

根目录只保留 **入口、依赖、文档索引**；业务代码在 `src/`，页面在 `views/`。

```
GoldAnalysisAI/
├── app.py                 # Streamlit 导航（用 run_app.py 启动）
├── run_app.py             # 官方启动器
├── run_app.bat / run_app.sh
├── requirements*.txt
├── pytest.ini
├── AGENTS.md              # AI / 自动化说明
├── README.md
│
├── src/                   # 应用源码（pipeline / agents / analysis / viz …）
├── views/                 # Streamlit 四页
├── tests/                 # 测试（run.py 统一入口）
├── scripts/               # 开发脚本（非测试）
└── docs/                  # 文档
```

本地生成、勿提交：`.venv/` `.cache/` `.env` `.cursor/` `.pytest_cache/` 等（见 `.gitignore`）。

<details>
<summary>src/ 目录展开</summary>

```
src/
├── pipeline.py            # 对外 API：run_analysis()
├── config.py
├── core/                  # orchestrator, types, progress
├── run/                   # 运行配置 + 归档（from src.run import …）
├── data/                  # fetch, sources
├── agents/                # Analyst Team + LLM stages
├── analysis/              # ICT/PA, report_engine
├── indicators/
├── llm/
└── viz/                   # Streamlit 组件
```

</details>

## 能力一览

| 模块 | 状态 |
|------|------|
| Analyst Team 输入密度 | ✅ 结构化 Headline/Calendar/MacroQuote + derived/context_stats |
| 金十 quote/kline 交叉校验 | ✅ `derived.spot_cross_check` / `jin10_kline_summary` |
| 多页面 UI | ✅ 机构 / 短线 / LLM 决策 |
| Session 会话缓存 | ✅ 切换页面秒开 |
| 历史回放（0 token） | ✅ `.cache/run_archives/` + 配置页回放模式 |
| 外部数据（DXY/金十快讯·资讯·日历/TV 社媒） | ✅ 拉取 + UI 展示 |
| LLM 双轨 + 来源标识 | ✅ |
| 智能体 I/O（Analyst Team + LLM） | ✅ LLM决策链页 |
| LLM 传输重试 + 混合模式规则兜底 | ✅ |
| 主图 5 分钟 (5m) | ✅ |

## LLM 配置（硅基流动示例）

```env
LLM_BASE_URL=https://api.siliconflow.cn/v1
LLM_MODEL=deepseek-ai/DeepSeek-V4-Pro
LLM_MODEL_FAST=deepseek-ai/DeepSeek-V4-Pro
LLM_MODEL_STRONG=deepseek-ai/DeepSeek-V4-Pro
AGENT_MODE=hybrid
LLM_STAGE_RESEARCH=true
LLM_STAGE_DEBATE=true
LLM_STAGE_ANALYSTS=true
LLM_STAGE_LEVELS=true
LLM_STAGE_TRADER=true
LLM_STAGE_RISK=true
LLM_STAGE_MANAGER=true
# 调试单个分析师时可设：technical / fundamentals / news / sentiment
LLM_ANALYST_ONLY=
LLM_ENABLED=true
```

## MT5 execution bridge

`src/data/mt5.py` 提供可选 MetaTrader 5 账号/执行 provider。默认关闭，不安装 `MetaTrader5` 包也不会影响现有 TradingView 行情路径。MT5 只用于账号检查和后续模拟下单，不作为 K 线数据源：

```env
MT5_ENABLED=false
MT5_SYMBOL=XAUUSDm
MT5_ACCOUNT=
MT5_PASSWORD=
MT5_SERVER=
MT5_PATH=
```

密码只写入本机 `.env`，不要提交。首次连接前需要本机已安装 MetaTrader 5 终端，然后运行：

```bash
python scripts/check_mt5_connection.py
```

当前 MT5 接口只读取账号信息，不发送订单；模拟下单 / 实盘下单仍未接入。

## 测试

```bash
pip install -r requirements-dev.txt

# fast：单元 + 回归（无网络，日常门禁）
python tests/run.py --fast

# 外部 API 冒烟（DXY / 金十 MCP / TV 社媒，需网络）
python tests/run.py --external

# scenario：按功能域跑专项
python tests/run.py --financial
python tests/run.py --external

# release：完整集成（需 .env + TradingView；hybrid+LLM 可能 5–6 分钟）
python tests/run.py --full

# 规则模式一致性检查（输出 tests/reports/coherence_check.json）
$env:AGENT_MODE="rule"; $env:LLM_ENABLED="false"; python tests/tools/coherence_check.py

# 列出 / 校验历史归档（无需 Streamlit）
python scripts/inspect_archive.py list
```

测试分层、用例目录与维护说明见 [docs/testing/strategy.md](docs/testing/strategy.md)、[tests/README.md](tests/README.md)、[tests/cases/catalog.yaml](tests/cases/catalog.yaml)。

**主图说明**：机构报告主图为 **5 分钟 K 线**（K 线 + 成交量 + Lux SMC：近位 5 个 Internal OB + 可见范围 active FVG）。远位多周期结构（如 4H 需求区）进入决策参考（关键流动性、市场总览、`context_levels`），**不画在主图**。详见 [docs/architecture/chart-layers.md](docs/architecture/chart-layers.md)。

## 免责声明

本项目仅供学习研究，不构成投资建议。

---

## Windows 终端编码

如果在 PowerShell 中看到中文文档、日志或 pytest 输出乱码，先在项目根目录执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\scripts\dev-env.ps1
```

该脚本会设置 UTF-8 控制台和 Python UTF-8 输出。`Set-ExecutionPolicy -Scope Process` 只影响当前 PowerShell 窗口，不修改系统策略。后续所有本地命令建议在同一个 PowerShell 会话中运行。

读取含中文的源码或文档时，优先使用：

```powershell
python scripts/show_utf8.py docs/reviews/financial/static-code-review.md --start 520 --count 40
```

不要用未初始化编码环境下的 `Get-Content` 作为补丁上下文来源；它可能把 UTF-8 无 BOM 文件按系统 ANSI 解码，导致看到的文本与磁盘真实内容不一致。
