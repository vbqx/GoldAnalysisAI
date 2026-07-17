# GoldAnalysisAI 开发参考手册

本文件只保留代码级参考：调用链、模块职责、扩展点和调试入口。项目定位读 [project.md](../overview/project.md)，架构边界读 [architecture.md](../architecture/architecture.md)、[report-trust.md](../architecture/report-trust.md) 与 [review.md](../architecture/review.md)（评审索引见 [reviews/README.md](../reviews/README.md)），测试策略读 [strategy.md](../testing/strategy.md)。

## 入口

| 入口 | 文件 | 说明 |
|------|------|------|
| Streamlit 应用 | `app.py` | 注册四个页面；**用 `python run_app.py` 启动** |
| 报告流水线 | `src/pipeline.py` | 对外薄封装：`run_analysis()` |
| 编排器 | `src/core/orchestrator.py` | 端到端阶段调度、进度、审计字段注入 |
| 类型中心 | `src/core/types.py` | `MarketContext`、`AgentTrace`、智能体结果 dataclass |
| UI 会话 | `src/viz/streamlit_common.py` | 生成前配置、后台线程、session 缓存 |

对外稳定调用：

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
```

## 流水线速查

流水线步骤权威列表在 [pipeline-steps.yaml](./pipeline-steps.yaml)，并由 `tests/regression/test_doc_pipeline_sync.py` 与代码里的 `prog.start(...)` 同步校验。

| ID | 阶段 | 主文件 | 输出 |
|----|------|--------|------|
| `fetch` | 数据拉取 | `src/data/fetch_pipeline.py` | `DataFetchResult(raw, external, source_label)` |
| `indicators` | 技术指标 | `src/indicators/technical.py` | enriched OHLCV + EMA/VWAP |
| `ict` | ICT 结构 | `src/analysis/ict_pa.py` | `TimeframeAnalysis` |
| `analyst_team` | 分析师团队 | `src/agents/analysts/` | `AnalystTeam` |
| `bullish` | 看多研究 | `src/agents/bullish.py` + `factory.py` | `AgentEvidence` |
| `bearish` | 看空研究 | `src/agents/bearish.py` + `factory.py` | `AgentEvidence` |
| `debate` | 多空辩论 | `src/agents/debate.py` + `factory.py` | `ResearchDebate` |
| `trader` | 交易员 | `src/agents/trader.py` + `factory.py` | `TransactionProposal` |
| `risk` | 风控 | `src/agents/risk.py` + `factory.py` | `RiskReview[3]` |
| `manager` | 经理 | `src/agents/manager.py` + `factory.py` | `ManagerDecision` |
| `report` | 组装报告 | `src/analysis/report_engine.py` | report dict |
| `llm_narrative` | LLM 文案 | `src/llm/analyst.py` | `report["llm_analysis"]` |
| `archive` | 运行归档 | `src/run/archive/`（`from src.run import archive_run`） | `.cache/run_archives/<run_id>/` |

回放（0 token）：`src/viz/replay_loader.py` → `load_replay_bundle()` → `src.run.load_bundle`。

```text
TradingView OHLCV
  -> fetch_all_data()
  -> enrich()
  -> analyze_timeframe()
  -> assemble_market_context()
  -> finalize_market_context()
  -> analyst_team / bullish / bearish / debate
  -> compute_trading_signals()
  -> trader / risk / manager
  -> build_report()
  -> optional llm_narrative
  -> archive (manifest + report + enriched)
  -> Streamlit viz/*
```

MT5 不在这条行情/回测链路中。MT5 只作为账号检查和后续 `shadow` / `paper_mt5` / `live_mt5` 执行通道，边界见 [architecture/review.md](../architecture/review.md)。

## 模块地图

| 目录 | 职责 | 常看文件 |
|------|------|----------|
| `src/data/` | TradingView 行情、外部数据、MarketContext 组装 | `fetch_pipeline.py`, `tradingview.py`, `context_builder.py`, `sources/*` |
| `src/indicators/` | 技术指标列追加 | `technical.py` |
| `src/analysis/` | ICT/PA 结构、报告 schema、信号几何、LLM 点位 validator | `ict_pa.py`, `report_engine.py`, `level_validator.py` |
| `src/agents/` | 规则/LLM/hybrid 智能体调度 | `factory.py`, `analysts/*`, `llm/stages/*` |
| `src/llm/` | LLM 客户端、路由、文案层、I/O 格式化 | `client.py`, `router.py`, `analyst.py`, `format_io.py` |
| `src/backtest/` | 历史回放基础设施和规则 baseline | `engine.py`, `simulator.py` |
| `src/viz/` | Streamlit 页面组件、图表、审计面板 | `report_views.py`, `decision_page.py`, `pipeline_progress.py` |
| `tests/` | 自动化测试、测试 UI、用例 catalog | `run.py`, `dashboard.py`, `cases/catalog.yaml` |

## 配置速查

完整变量以 `.env.example` 为准。

| 变量 | 说明 |
|------|------|
| `TV_SYMBOL`, `TV_EXCHANGE`, `TV_USERNAME`, `TV_PASSWORD` | TradingView 行情配置 |
| `AGENT_MODE` | `rule` / `llm` / `hybrid` |
| `LLM_ENABLED` | 报告文案层开关 |
| `LLM_STAGE_ANALYSTS`, `LLM_STAGE_RESEARCH`, `LLM_STAGE_DEBATE` | 研究链 LLM 阶段 |
| `LLM_STAGE_LEVELS`, `LLM_STAGE_TRADER`, `LLM_STAGE_RISK`, `LLM_STAGE_MANAGER` | 点位、交易、风控、经理 LLM 阶段 |
| `LLM_ANALYST_ONLY` | 只调试单个 Analyst LLM |
| `LLM_TIMEOUT`, `LLM_CONNECT_TIMEOUT`, `LLM_READ_TIMEOUT` | 连接与流式空闲超时（秒）；见 [llm-agents.md §3.4](../architecture/llm-agents.md#34-传输重试与规则兜底) |
| `LLM_MAX_RETRIES`, `LLM_RETRY_BACKOFF_BASE_S` | 每阶段传输/JSON 重试与指数退避 |
| `JIN10_API_TOKEN` | 金十 MCP |
| `MT5_ENABLED`, `MT5_ACCOUNT`, `MT5_PASSWORD`, `MT5_SERVER`, `MT5_PATH` | MT5 执行通道配置 |
| `LOG_LEVEL`, `LOG_FILE` | 日志控制 |

## 常见改动入口

| 想改什么 | 优先读/改 | 最小验证 |
|----------|-----------|----------|
| K 线拉取和重试 | `src/data/tradingview.py` | `pytest tests/unit/test_tradingview_retry.py` |
| 外部数据源 | `src/data/sources/` + `fetch_pipeline.py` | `python tests/run.py --external` |
| EMA/VWAP | `src/indicators/technical.py` | `pytest tests/unit/test_indicators.py` |
| Swing/BOS/CHoCH/OB/FVG | `src/analysis/ict_pa.py` | `pytest tests/unit/test_ict_pa.py` |
| 信号几何和评分 | `src/analysis/report_engine.py` | `pytest tests/unit/test_financial_review.py` |
| LLM 点位校验 | `src/analysis/level_validator.py` | `pytest tests/unit/test_llm_level_validator.py` |
| Analyst Team | `src/agents/analysts/` | `pytest tests/unit/test_analyst_input_density.py` |
| LLM 阶段 | `src/agents/llm/stages/` + `factory.py` | `pytest tests/unit/test_llm_trade_stages.py` |
| Streamlit 布局 | `src/viz/` | `python tests/run.py --fast` + UI 冒烟 |
| 回测基础设施 | `src/backtest/` | `pytest tests/unit/test_backtest*.py` |
| MT5 账号检查 | `src/data/mt5.py` + `scripts/check_mt5_connection.py` | `pytest tests/unit/test_mt5_provider.py` |

## LLM 点位阶段

LLM 点位阶段只提出候选；任何候选都必须通过规则 validator 后才能进入 Trader/Risk。

| 顺序 | 函数 | 文件 | 输出 |
|------|------|------|------|
| 1 | `compute_trading_signals(ctx)` | `src/analysis/report_engine.py` | 规则候选 `list[TradingSignal]` |
| 2 | `agent_factory.run_level_proposer(...)` | `src/agents/factory.py` | LLM 原始 `list[LevelProposal]` |
| 3 | `validate_llm_levels(ctx, proposals)` | `src/analysis/level_validator.py` | 已校验 `TradingSignal` + 审计行 |
| 4 | `agent_factory.run_trader(..., signals)` | `src/agents/factory.py` | 基于规则 + 已校验 LLM 信号生成 `TransactionProposal` |

相关报告字段：

| 字段 | 说明 |
|------|------|
| `report["llm_levels"]` | LLM 原始点位输出 |
| `report["validated_plans"]` | validator 结果 |
| `report["agent_trace"]["llm_levels"]` | 点位阶段审计 |
| `report["agent_trace"]["validated_plans"]` | 校验审计 |

## UI 数据合同

| 数据 | 主要消费者 |
|------|------------|
| `report` | `src/viz/*` 中的指标卡、交易计划、决策链、LLM I/O |
| `data[tf]` | K 线图表 |
| `analyses[tf]` | OB/FVG/流动性 overlay |
| `report["agent_trace"]` | LLM 决策链页和审计侧栏 |
| `report["meta"]["generation_steps"]` | 生成进度与耗时 |
| `report["meta"]["llm_io"]` | 规则阶段 I/O 与 LLM 调用记录 |

Streamlit 页面切换复用同一份 session 报告，不重新跑流水线。只有用户确认“开始生成报告”或“重新配置 / 刷新报告”后才重新执行。

## 调试入口

```python
from src.pipeline import run_analysis

report, data, analyses = run_analysis()
print(report["meta"]["generation_steps"])
print(report["meta"]["stage_sources"])
print(report["agent_trace"]["decision"])
```

常用命令：

```bash
python tests/run.py --fast
python tests/run.py --external
python tests/run.py --financial
python tests/run.py --full
python tests/tools/coherence_check.py
python scripts/check_mt5_connection.py
```

调试日志：

```env
LOG_LEVEL=DEBUG
LOG_FILE=logs/goldanalysisai.log
```

## 维护约定

1. 改流水线阶段：同步 [pipeline-steps.yaml](./pipeline-steps.yaml)，跑 `pytest tests/regression/test_doc_pipeline_sync.py`。
2. 改 report 字段：同步 [report-schema.md](./examples/report-schema.md)，必要时更新 `sample-report.json`。
3. 改测试分层或输出边界：同步 [testing/strategy.md](../testing/strategy.md) 与 `tests/cases/catalog.yaml`。
4. 改架构边界：同步 [architecture/review.md](../architecture/review.md)，不要把当前事实只写在 roadmap。
5. 业务行为变更必须配最小专项测试；纯文档迁移至少跑 `python tests/run.py --fast` 和 `git diff --check`。

## 相关文档

| 文档 | 用途 |
|------|------|
| [docs/README.md](../README.md) | 文档中心 |
| [onboarding.md](../operations/onboarding.md) | 首次读项目 |
| [cheat-sheet.md](./cheat-sheet.md) | 改功能速查 |
| [glossary.md](./glossary.md) | 术语表 |
| [walkthrough.md](../operations/walkthrough.md) | UI 操作动线 |
| [llm-agents.md](../architecture/llm-agents.md) | LLM 智能体设计 |
| [report-trust.md](../architecture/report-trust.md) | 事实注册表、证据溯源、不变量、可靠度 |
| [backtesting.md](../architecture/backtesting.md) | 回测边界 |
| [strategy.md](../testing/strategy.md) | 测试策略 |

## 免责声明

本项目仅供学习研究，不构成投资建议。
