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

streamlit run app.py
```

浏览器打开 `http://localhost:8501`。启动后先在 **生成前配置** 面板选择规则 / LLM / 混合模式，点击「开始生成报告」后才拉取数据并生成报告。

## 多页面导航

| 页面 | 文件 | 说明 |
|------|------|------|
| 机构级分析报告 | `views/1_机构级分析报告.py` | 机构完整报告，主图 5 分钟 |
| 外部数据 | `views/4_外部数据.py` | 新闻/日历/DXY/社媒，**fetch 完成后即可查看** |
| 短线策略 | `views/2_短线策略.py` | 短线策略图，**切换不重新生成** |
| LLM决策链 | `views/3_LLM决策链.py` | 智能体决策、LLM 文案、生成与智能体 I/O |

报告在 session 中缓存；后台线程生成，等待时可看实时步骤与 LLM I/O。仅点 **「重新配置 / 刷新报告」** 并再次确认配置后才重跑（规则模式约 30s；启用 LLM 全流程可能 5–6 分钟）。

**手动验证 Analyst 输入密度**：生成完成后在「LLM决策链」页查看 `context_stats`、`news_topics`、`spot_cross_check`；报告 `meta.context_stats` 与 `external` 块含结构化计数。

## 文档

完整索引见 **[docs/README.md](docs/README.md)**。

| 文档 | 说明 |
|------|------|
| **[docs/getting-started/onboarding.md](docs/getting-started/onboarding.md)** | **开发者上手指南（建议先读）** |
| [docs/getting-started/setup.md](docs/getting-started/setup.md) | 环境搭建与运行 |
| [docs/getting-started/walkthrough.md](docs/getting-started/walkthrough.md) | UI 操作动线与序列图 |
| [docs/reference/cheat-sheet.md](docs/reference/cheat-sheet.md) | 改功能速查表 |
| [docs/reference/handbook.md](docs/reference/handbook.md) | 开发参考手册（完整数据流） |
| [docs/design/architecture.md](docs/design/architecture.md) | 架构设计（TradingAgents 对照） |
| [docs/domain/financial-review.md](docs/domain/financial-review.md) | 金融逻辑评审 |
| [tests/README.md](tests/README.md) | 测试体系与 CLI 命令 |

## 项目结构

```
GoldAnalysisAI/
├── app.py                      # 导航入口（st.navigation）
├── views/                      # 四页视图（由 app.py 导航注册）
│   ├── 1_机构级分析报告.py
│   ├── 4_外部数据.py
│   ├── 2_短线策略.py
│   └── 3_LLM决策链.py
├── tests/                      # 测试体系（用例 / 单元 / 集成 / 回归 / 工具）
│   ├── run.py                  # 统一入口
│   ├── cases/catalog.yaml      # 用例目录
│   ├── unit/
│   ├── integration/
│   └── regression/
└── src/
    ├── pipeline.py             # 对外 API 薄封装
    ├── config.py
    ├── core/                   # types, orchestrator, progress
    ├── data/
    │   ├── fetch_pipeline.py
    │   ├── context_builder.py
    │   └── sources/            # jin10_mcp, macro (DXY/US10Y), news, social
    ├── agents/
    │   ├── factory.py
    │   ├── analysts/           # Analyst Team（TradingAgents 对齐）
    │   └── llm/stages/         # LLM 各阶段
    ├── analysis/               # ict_pa, report_engine
    ├── indicators/
    ├── llm/
    └── viz/
        ├── streamlit_common.py # 共享 bootstrap + session 缓存
        ├── decision_page.py
        └── pipeline_progress.py
```

## 能力一览

| 模块 | 状态 |
|------|------|
| Analyst Team 输入密度 | ✅ 结构化 Headline/Calendar/MacroQuote + derived/context_stats |
| 金十 quote/kline 交叉校验 | ✅ `derived.spot_cross_check` / `jin10_kline_summary` |
| 多页面 UI | ✅ 机构 / 短线 / LLM 决策 |
| Session 会话缓存 | ✅ 切换页面秒开 |
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
# 调试单个分析师时可设：technical / fundamentals / news / sentiment
LLM_ANALYST_ONLY=
LLM_ENABLED=true
```

## 测试

```bash
pip install -r requirements-dev.txt

# 快速：单元 + 回归（无网络，约 88 项，推荐 CI / 日常）
python tests/run.py

# 外部 API 冒烟（DXY / 金十 MCP / TV 社媒，需网络）
python tests/run.py --external

# 金融 Review：FIN-* 单测（发版前建议配合 coherence_check）
python tests/run.py --financial

# 完整：含流水线集成（需 .env + TradingView；规则模式约 1 分钟，hybrid+LLM 约 5–6 分钟）
python tests/run.py --full

# 规则模式一致性检查（P0 门禁；输出 tests/reports/coherence_check.json）
$env:AGENT_MODE="rule"; $env:LLM_ENABLED="false"; python tests/tools/coherence_check.py
```

**金融三阶段修复**（2026-06-20）：F-003/F-013/F-014（P0）+ UI/配置（P1）+ 数据质量/Agent 边界（P2）已落地；详见 [docs/domain/financial-review.md §7](docs/domain/financial-review.md#7-修复路径规划2026-06-20)。

用例目录与维护说明见 [tests/README.md](tests/README.md)、[tests/cases/catalog.yaml](tests/cases/catalog.yaml)。

**主图说明**：机构报告主图为 **5 分钟 K 线**（K 线 + 成交量 + SMC 结构/支撑阻力叠加）；路径推演在底栏卡片展示。EMA/MACD/RSI 等在流水线中计算并供 agent 使用，在侧边栏 **「指标校验」** 展示，不绘制在主图上。

## 免责声明

本项目仅供学习研究，不构成投资建议。
