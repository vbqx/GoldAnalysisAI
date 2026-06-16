# GoldAnalysisAI 开发参考手册

> 函数调用链、模块职责、调试与常见问题的**详细参考**。入门请先读 [developer-onboarding.md](./developer-onboarding.md)。

---

## 2. 环境配置参考

### 2.3 配置（`.env`）

| 变量 | 默认 | 说明 |
|------|------|------|
| `TV_SYMBOL` | `XAUUSD` | TradingView 品种 |
| `TV_EXCHANGE` | `OANDA` | 交易所 |
| `TV_USERNAME` / `TV_PASSWORD` | 空 | 可选；登录后历史 bar 更多 |
| `TV_FETCH_RETRIES` / `TV_FETCH_ROUND_RETRIES` | `3` / `1` | TradingView 拉数重试 |
| `JIN10_API_TOKEN` | 空 | 金十官方 MCP 快讯 + 资讯 + 财经日历（[申请](https://mcp.jin10.com/app)） |
| `JIN10_KEYWORD` | `黄金` | 快讯/资讯筛选关键词 |
| `ANALYST_*` / `TV_US10Y_*` | 见 [analyst-context.md](./analyst-context.md) | Analyst Team 输入密度上限 |
| `LOG_LEVEL` | `INFO` | `DEBUG` 可跟踪流水线 |
| `LOG_FILE` | 空 | 如 `logs/goldanalysisai.log` |
| `AGENT_MODE` | `rule` | `rule` / `llm` / `hybrid`，见 [llm-agents.md](./llm-agents.md) |
| `LLM_*` | 见 `.env.example` | 硅基流动 / OpenAI 兼容 API |

配置在 **`src/config.py`** 读取环境变量（模块 import 时自动加载 `.env`）；`app.py` 在 import 前也会预加载 `.env`。

---

## 3. 整体数据流与函数调用链

数据**全程在内存**，不落盘。一次完整请求从 TradingView 到 UI 经过以下阶段。

### 3.1 总览

```
TradingView WebSocket
        │
        ▼  [data/tradingview.py]
fetch_multi_timeframe()  →  dict[str, DataFrame]  raw
        │
        ▼  [indicators/technical.py]
enrich() × 各周期  →  dict[str, DataFrame]  enriched（+EMA/VWAP）
        │
        ▼  [analysis/ict_pa.py]
analyze_timeframe() × 5  →  dict[str, TimeframeAnalysis]  analyses
        │
        ▼  [data/aggregator.py]
assemble_market_context()  →  MarketContext  ctx
        │
        ▼  [data/context_builder.py]
finalize_market_context()  →  ctx.derived + ctx.context_stats
        │
        ▼  [agents/analysts/ + agents/factory.py]
analyst_team → bullish / bearish → debate
        │
        ▼  [report_engine.compute_trading_signals(ctx)]  ← 信号唯一生成点
        │
        ▼  [agents/factory.py]
trader(signals) → risk → manager
  (Analyst Team 规则；研究/辩论 rule / llm / hybrid)
        │
        ▼  [llm/analyst.py]  （可选，LLM_ENABLED）
报告文案层
        │
        ▼  [analysis/report_engine.py]
build_report(signals=…)  →  dict  report
        │
        ▼  [core/orchestrator.py]
注入 external、agent_trace、stage_sources、generation_steps、llm_io
        │
        ▼  [app.py + viz/*]
进度条 + LLM 流式 I/O + render_*  →  浏览器 UI
```

**Streamlit 入口**：各页面调用 `ensure_report()`（`src/viz/streamlit_common.py`），共享 session 缓存。仅 `app.py` 首次加载或「刷新报告」时跑完整流水线并显示进度条。

---

### 3.2 阶段一：UI 启动与流水线入口

| 顺序 | 函数 | 文件 | 输入 | 输出 |
|------|------|------|------|------|
| 1 | `_load_dotenv()` | `config.py` / `app.py` | 从 `.env` 加载配置（import 前） |
| 2 | `_inject_proxy()` | `streamlit_common.py` | 环境变量 / Windows 注册表代理 |
| 3 | `setup_logging()` | `src/log.py` | 配置 root logger（UTF-8 stderr） |
| 4 | `ensure_report()` | `streamlit_common.py` | session 缓存 / 首次或刷新时 `run_analysis()` |
| 5 | `run_analysis()` | `src/pipeline.py` | 委托 orchestrator |
| 6 | `run_trade_agent_pipeline()` | `src/core/orchestrator.py` | `(report, enriched, analyses)` |

---

### 3.3 阶段二：数据拉取（`fetch_pipeline.py`）

| 顺序 | 函数 | 文件 | 说明 |
|------|------|------|------|
| 1 | `fetch_all_data()` | `src/data/fetch_pipeline.py` | orchestrator 入口：K 线 + 外部源 |
| 2 | `fetch_multi_timeframe()` | `src/data/fetcher.py` → `tradingview.py` | 组装 5m/15m/1h/4h/1d |
| 3 | `fetch_external_bundle()` | `src/data/fetch_pipeline.py` | 新闻 / DXY+US10Y / 社媒（三源并行） |
| 4 | `fetch_jin10_bundle()` | `src/data/sources/jin10_feed.py` | 金十 MCP：快讯 + 资讯 + 日历 |
| 5 | `fetch_jin10_quote()` / `fetch_jin10_kline()` | `jin10_feed.py` | 可选：spot/K 线与 TV 交叉校验（在 `finalize_market_context` 内） |
| 6 | `merge_external()` | `src/data/aggregator.py` | → `ExternalFactors` |
| 7 | `finalize_market_context()` | `src/data/context_builder.py` | derived 信号 + context_stats |

详见 [analyst-context.md](./analyst-context.md)（三层架构、配置项、Phase 0–6 状态）。

**TradingView 细节**（步骤 2 内部）：

| 顺序 | 函数 | 文件 | 说明 |
|------|------|------|------|
| 1 | `_get_client()` | `src/data/tradingview.py` | 单例 `TvDatafeed()` |
| 2 | `_fetch_bars()` | `src/data/tradingview.py` | 调用 `tv.get_hist()`，可配置重试 |
| 3 | `_normalize()` | `src/data/tradingview.py` | 列名 → Open/High/Low/Close/Volume |
| 4 | `_resample()` | `src/data/tradingview.py` | 5m 聚合为 15m / 1h / 4h |
| 5 | `source_label()` | `src/data/tradingview.py` | 数据源标签字符串 |

**请求次数**：2 次 TV（5000×5m + 365×1d）；15m/1h/4h 本地 resample。外部 HTTP 见 [jin10-mcp.md](./jin10-mcp.md)。

**输出变量**：`DataFetchResult(raw, external, source_label)`。

---

### 3.4 阶段三：指标 enrich

| 顺序 | 函数 | 文件 | 说明 |
|------|------|------|------|
| 1 | `enrich(df)` | `src/indicators/technical.py` | 入口 |
| 2 | `add_emas(df)` | 同上 | 追加 EMA20 / EMA50 / EMA610 |
| 3 | `add_vwap(df)` | 同上 | 按日锚定 VWAP |

**输出变量**：`enriched: dict[str, DataFrame]`（即最终返回给 UI 的 `data`）。

---

### 3.5 阶段四：ICT / PA 结构分析

| 顺序 | 函数 | 文件 | 说明 |
|------|------|------|------|
| 1 | `analyze_timeframe(df, tf)` | `src/analysis/ict_pa.py` | 每周期入口，×5（5m/15m/1h/4h/1d） |
| 2 | `_find_swings()` | 同上 | 摆动高低点 |
| 3 | `_infer_trend()` | 同上 | bullish / bearish / ranging |
| 4 | `_detect_structure_events()` | 同上 | BOS / CHoCH |
| 5 | `_detect_fvgs()` | 同上 | Fair Value Gap |
| 6 | `_detect_order_blocks()` | 同上 | Order Block |
| 7 | `_liquidity_from_swings()` | 同上 | 流动性区 |
| 8 | `_active_fvgs()` | 同上 | 未填补 FVG |
| 9 | `_premium_discount()` | 同上 | 溢价 / 折价区 |
| 10 | `_volume_signal()` | 同上 | 成交量描述 |

**输出变量**：`analyses: dict[str, TimeframeAnalysis]`。

后续还会调用 `sentiment_score(analyses)`（同文件），在 report 与 trader 阶段使用。

---

### 3.6 阶段五：市场上下文

| 顺序 | 函数 | 文件 | 说明 |
|------|------|------|------|
| 1 | `assemble_market_context(...)` | `src/data/aggregator.py` | 组装 `MarketContext`（external 已由 fetch_pipeline 拉取） |
| 2 | `daily_metrics(enriched["1d"])` | `src/data/fetcher.py` | 现价、日涨跌、日高日低 |
| 3 | `get_active_source()` | `src/data/fetcher.py` | → `tradingview.source_label()` |
| 4 | `collect_evidence()` | `src/data/aggregator.py` | 调各 DataSource（日志用） |

**输出变量**：`ctx: MarketContext`（含 `enriched`、`analyses`、`metrics`、`price`、`external`）。

---

### 3.7 阶段六：智能体流水线

| 顺序 | 函数 | 文件 | 输入 → 输出 |
|------|------|------|-------------|
| 0 | `agent_factory.run_analyst_team(ctx, pipeline_meta)` | `src/agents/analysts/` | → `AnalystTeam`（四位分析师，规则；`stage_io` 记入 `meta.llm_io`） |
| 1 | `agent_factory.run_bullish(ctx, pipeline_meta, team)` | `src/agents/factory.py` | → `AgentEvidence`（整合 Analyst 同向证据 + ICT） |
| 2 | `agent_factory.run_bearish(...)` | 同上 | → `AgentEvidence` |
| 3 | `agent_factory.run_debate(..., team)` | 同上 | → `ResearchDebate`（含 Analyst 摘要） |
| 4 | `compute_trading_signals(ctx)` | `src/analysis/report_engine.py` | → `list[TradingSignal]`（pipeline 唯一生成点） |
| 5 | `agent_factory.run_trader(..., signals)` | 同上 | → `(TransactionProposal, signals[])` |
| 6 | `agent_factory.run_risk(...)` | `src/agents/factory.py` | → `RiskReview[3]` |
| 7 | `agent_factory.run_manager(...)` | 同上 | → `ManagerDecision` |

研究员从 ICT 结构提取证据，并通过 `items_for_direction()` 并入 Analyst Team 同向条目。

---

### 3.8 阶段七：报告组装与 orchestrator 收尾

**`build_report(enriched, analyses, signals=...)`**（`src/analysis/report_engine.py`）内部调用：

| 函数 | 产出字段 |
|------|----------|
| `daily_metrics(data["1d"])` | `metrics` |
| `sentiment_score(analyses)` | `sentiment` |
| `fibonacci_levels(...)` | `fibonacci` |
| （传入 `signals` 或内部 `generate_trading_signals`） | `signals` |
| `build_conclusion(...)` | `conclusion` |
| `ema_relation(...)` | `timeframes[*].ema_relation` |
| `trend_projections(...)` | `projections` |
| `build_path_summary(...)` | `path_summary` |
| `build_key_levels(...)` | `key_levels` |
| `build_resistance_support(...)` | `resistance_levels`, `support_levels` |
| `build_strategy_plans(...)` | `strategy_plans` |
| `build_market_overview(...)` | `market_overview` |
| `build_calendar_events()` | `calendar_events` |
| `invalidation_rules(...)` | `invalidation` |
| `utc8_now()` | `meta.updated_at` |

**orchestrator 追加**（`run_trade_agent_pipeline` 末尾）：

| 操作 | 说明 |
|------|------|
| `report["meta"]["agent_mode"]` | 当前 `AGENT_MODE` |
| `report["meta"]["stage_sources"]` | 各阶段 rule/llm/hybrid |
| `report["meta"]["generation_steps"]` | 生成步骤与耗时（含 `analyst_team`） |
| `report["meta"]["llm_io"]` | 智能体 I/O：规则阶段（`stage_io`，如 Analyst Team）+ LLM 调用 |
| `AgentTrace(...).to_dict()` → `report["agent_trace"]` | 决策审计链（含 `analyst_team` 四位分析师） |
| `report["external"]` | DXY、新闻、日历、TV 社媒 + `sources` 标签 |
| `parse_risk_events_calendar()` → `report["calendar_events"]` | 有金十财经日历时覆盖占位日历 |
| `run_llm_analysis` + `apply_llm_to_report` | `report["llm_analysis"]`、增强 `conclusion`（进度步骤 `llm_narrative` / LLM 报告文案） |
| 按 `decision.selected_signal_indices` 重排 | `report["signals"]` |

**返回值**：`(report, enriched, analyses)` → 存入 session 后由各页 `render_*` 展示。

---

### 3.9 阶段八：UI 渲染

| 函数 | 文件 | 主要数据来源 |
|------|------|--------------|
| `render_institutional_report()` | `src/viz/report_views.py` | 机构报告布局 |
| `render_strategy_map()` | `src/viz/report_views.py` | 短线策略（独立页） |
| `render_llm_decision_page()` | `src/viz/decision_page.py` | LLM 决策链（独立页） |
| `ensure_report()` | `src/viz/streamlit_common.py` | session 缓存 + 生成进度 |
| `_embed_chart()` | `src/viz/report_views.py` | 图表 iframe 封装 |
| `build_lightweight_chart_html()` | `src/viz/lightweight_chart.py` | K 线、EMA/VWAP、OB/FVG  overlay |
| `_serialize_overlays()` | `src/viz/lightweight_chart.py` | 结构区、投影线 |
| `render_header()` 等 | `src/viz/dashboard_components.py` | `report` 各字段 → HTML |
| `render_external_data_panel()` | `src/viz/dashboard_components.py` | 外部拉取数据面板（DXY/新闻/日历/社媒） |
| `build_sentiment_donut()` | `src/viz/charts.py` | `report["sentiment"]` |
| `build_projection_chart()` | `src/viz/charts.py` | `report["projections"]` |
| `render_agent_source_banner()` | `src/viz/source_labels.py` | 顶栏 规则/LLM 来源 |
| `StreamlitProgressReporter` | `src/viz/pipeline_progress.py` | 进度 + LLM 流式 I/O |
| `render_llm_io_history()` | 同上 | 智能体 I/O（Analyst Team 规则输出 + LLM） |
| `render_agent_trace_sidebar()` | `src/viz/agent_trace_view.py` | 决策链 + 来源徽章 |
| `render_llm_sidebar()` | `src/viz/llm_view.py` | LLM 深度分析文案 |
| `indicator_snapshot()` | `src/indicators/verify.py` | 指标校验表 |

机构报告**主图**使用 **1d 日线**（`report_views.py` + `lightweight_chart.py`）。

**UI 数据分工**：

| 数据 | UI 用途 |
|------|---------|
| `data[tf]` | K 线 OHLCV、EMA/VWAP 曲线（来自 TV + enrich） |
| `analyses[tf]` | 图表上 OB/FVG/流动性 overlay |
| `report` | 价格摘要、结论、周期文字、信号卡片、饼图、路径、Fib 等 |

侧边栏切换 **机构报告 / 短线策略 / LLM决策链** 时复用同一份 session 报告，**不重新跑流水线**。

---

## 4. 目录结构与读码顺序

### 4.1 目录地图

```
GoldAnalysisAI/
├── app.py                      # st.navigation 入口（纯路由）
├── views/                      # 三页视图脚本
│   ├── 1_机构级分析报告.py
│   ├── 2_短线策略.py
│   └── 3_LLM决策链.py
├── requirements.txt
├── .env.example
├── requirements-dev.txt        # pytest 等开发依赖
├── tests/                      # 测试体系，见 tests/README.md
├── docs/
└── src/
    ├── pipeline.py             # 对外 API 薄封装
    ├── config.py               # 环境变量 → 模块级常量
    ├── log.py                  # logging 初始化
    ├── core/
    │   ├── types.py            # dataclass 定义
    │   ├── progress.py         # 进度 + LLM I/O（contextvar）
    │   └── orchestrator.py     # 流水线编排
    ├── data/
    │   ├── fetch_pipeline.py   # K 线 + 外部源统一拉取
    │   ├── tradingview.py      # 网络 I/O + resample
    │   ├── fetcher.py          # facade
    │   ├── aggregator.py       # MarketContext 组装
    │   └── sources/            # DataSource（jin10 / dxy / social / market）
    ├── indicators/technical.py
    ├── analysis/
    │   ├── ict_pa.py           # 结构检测（计算密集）
    │   └── report_engine.py    # 报告 JSON + 信号生成
    ├── agents/
    │   ├── factory.py          # rule/llm/hybrid 调度
    │   ├── llm/                # LLM 阶段实现
    │   └── *.py                # 规则智能体
    ├── llm/                    # client、router、analyst、format_io
    └── viz/
        ├── pipeline_progress.py  # 进度 + 流式 LLM 面板
        ├── source_labels.py      # 规则/LLM 来源标识
        └── ...
```

### 4.2 建议读码顺序

| 顺序 | 文件 | 关注点 |
|------|------|--------|
| 1 | `app.py` | UI 生命周期、缓存边界 |
| 2 | `pipeline.py` → `orchestrator.py` | 调用图、阶段顺序 |
| 3 | `core/types.py` | 领域类型（先读此文件再读 agents） |
| 4 | `data/tradingview.py` | I/O、重试、resample |
| 5 | `analysis/ict_pa.py` | 核心算法 |
| 6 | `analysis/report_engine.py` | 输出 schema |
| 7 | `agents/debate.py` → `trader.py` → `manager.py` | 决策逻辑 |
| 8 | `viz/report_views.py` | report 字段如何映射到 UI |

---

## 5. 核心模块说明

### 5.1 `app.py` 与多页面

- **`app.py`**：`st.navigation` 注册三页；预加载 `.env`；不显示为侧边栏「app」
- **`views/1_机构级分析报告.py`**：`ensure_report()` 触发首次生成 + 实时决策链 Tab
- **`views/2_短线策略.py`**：`ensure_report(show_generation_ui=False)`，秒开
- **`views/3_LLM决策链.py`**：决策链、LLM 文案、`meta.llm_io` 完整记录
- **共享**：`src/viz/streamlit_common.py`（bootstrap、sidebar、线程生成、session 缓存）

### 5.2 数据层 `src/data/`

**`tradingview.py`**

- 2 次 HTTP/WebSocket 请求：5000×5m + 365×1d；
- 15m/1h/4h 由 5m **resample** 聚合（OHLCV 规则：`Open=first, High=max, Low=min, Close=last, Volume=sum`）；
- 模块级单例 `_tv_client`；`reset_client()` 置空；
- 失败重试 2 次，指数退避 `sleep(1.5 * attempt)`。

**`aggregator.py`**

- 输出 `MarketContext`：enriched bars + analyses + metrics + external factors；
- `collect_evidence()` 聚合各 `DataSource` 的 `EvidenceItem`。

**扩展数据源**：在 `sources/` 实现 `fetch_external()` / `fetch_evidence()`，注册到 `aggregator.py`；不必改 `run_analysis()` 签名。

**外部数据源**（`src/data/sources/`）：

| 模块 | 数据源 | 说明 |
|------|--------|------|
| `dxy.py` | TradingView `TVC:DXY` | 日涨跌 → 黄金影响文案 |
| `jin10_feed.py` / `jin10_mcp_client.py` | 金十官方 MCP | `list_flash` / `search_news` / `list_calendar` |
| `news.py` | NewsDataSource | 合并快讯 + 资讯 + 日历 → ExternalFactors |
| `social_feed.py` | TradingView Ideas/Minds | XAUUSD 社区多空加权情绪 |

合并后写入 `ExternalFactors`（`social_posts`、`sources`），UI 经 `report["external"]` 展示；失败时回退占位文案，不中断流水线。

### 5.3 指标层 `indicators/technical.py`

对 DataFrame **原地追加列**：`EMA_20`, `EMA_50`, `EMA_610`, `VWAP`。

注意：5m 上 EMA610 需要足够 bar 数；匿名 TradingView 可能不足。

### 5.4 结构分析 `analysis/ict_pa.py`

每周期返回 `TimeframeAnalysis` dataclass：

| 字段 | 说明 |
|------|------|
| `trend` | `bullish` / `bearish` / `ranging` |
| `bos`, `choch` | 结构突破描述字符串 |
| `order_blocks`, `fvgs`, `active_fvgs` | 区域列表 |
| `liquidity` | 流动性价位 |
| `swing_high`, `swing_low` | 最近摆动极值 |
| `events` | `StructureEvent` 列表（BOS/CHoCH） |

算法为 **启发式 MVP**，详见 [reverse-engineering.md](./reverse-engineering.md)。

### 5.5 智能体层 `src/agents/`

经 **`factory.py`** 调度，支持 `AGENT_MODE=rule|llm|hybrid`。流水线分两阶段研究，对齐 TradingAgents：

**阶段 A — Analyst Team**（`agents/analysts/`，按信息类型分工）

| 分析师 | 规则实现 | 数据源 | LLM |
|--------|----------|--------|-----|
| Technical | `analysts/technical.py` | EMA/VWAP + ICT 结构 | ✅ `llm/stages/analysts/technical.py` |
| Fundamentals | `analysts/fundamentals.py` | `sources/dxy.py` + TradingView | ✅ `llm/stages/analysts/fundamentals.py` |
| News | `analysts/news.py` | `sources/news.py` + `jin10_feed.py` | ✅ `llm/stages/analysts/news.py` |
| Sentiment | `analysts/sentiment.py` | 结构投票 + `sources/social_feed.py`（TV Ideas/Minds） | ✅ `llm/stages/analysts/sentiment.py` |

输出 `AnalystTeam` → 写入 `agent_trace.analyst_team`。

**阶段 B — Researcher / Trade / Risk**（按交易方向与执行）

| 阶段 | factory 入口 | 规则实现 | LLM 实现 |
|------|-------------|----------|----------|
| Research | `run_bullish` / `run_bearish` | `bullish.py` / `bearish.py`（整合 Analyst 同向证据） | `llm/stages/bullish.py` 等 |
| Debate | `run_debate` | `debate.py`（含 Analyst 摘要） | `llm/stages/debate.py` |
| Trade | `run_trader` | `trader.py` | P1 规划中 |
| Risk | `run_risk` | `risk.py` | P2 规划中 |
| Manager | `run_manager` | `manager.py` | P2 规划中 |

`run_manager` 优先级：**conservative** → **neutral** → **aggressive**；全否决则 `action="wait"`。

### 5.6 报告引擎 `analysis/report_engine.py`

`build_report(data, analyses, *, signals=None) -> dict` 生成 UI schema。Orchestrator 传入已生成的 `signals`，避免与 trader 重复计算。

Orchestrator 随后注入：

- `report["meta"]["data_source"]`
- `report["external"]`（来自 aggregator）
- `report["agent_trace"]`（审计链 + `stage_meta`）
- `report["meta"]["llm_io"]`（LLM 完整 I/O）
- `report["llm_analysis"]`（文案层，若 `LLM_ENABLED`）

**主要字段**：

```python
{
    "meta": {...},
    "metrics": {          # current_price, daily_change, daily_high, ...
    "sentiment": {        # bullish / bearish / ranging 百分比
    "conclusion": {...},
    "timeframes": {...},  # 各 TF 结构摘要
    "signals": [...],     # TradingSignal → dict
    "projections": [...],
    "fibonacci": [...],
    "invalidation": [...],
    "chart": {...},
    "agent_trace": {...}, # orchestrator 追加
}
```

`TradingSignal` dataclass 字段：`entry_low/high`, `stop_loss`, `take_profits[]`, `theme`（`"short"|"long"`）等。

### 5.7 可视化层 `src/viz/`

| 模块 | 职责 |
|------|------|
| `report_views.py` | 两种布局入口 |
| `charts.py` | Plotly 图 |
| `lightweight_chart.py` | TradingView Lightweight Charts iframe |
| `dashboard_components.py` | HTML/CSS 组件 |
| `agent_trace_view.py` | 决策链 + 来源徽章 |
| `pipeline_progress.py` | 生成进度 + 智能体 I/O（规则 `stage_io` + LLM 流式） |
| `source_labels.py` | 规则/LLM 来源条 |
| `llm_view.py` | LLM 文案侧边栏 |

**分层原则**：viz 只读 `report`/`data`/`analyses`，不 import agents。

---

## 6. 领域类型（`core/types.py`）

读 agents 前先扫一遍此文件，这是项目的类型定义中心：

```
EvidenceItem          # 单条证据
AnalystReport         # 单个分析师报告（Technical / News 等）
AnalystTeam           # 四位分析师容器
AgentEvidence         # 某研究员输出
ResearchDebate        # 辩论结果 + consensus_bias
TransactionProposal   # 方向 + signal 索引列表
RiskReview            # 某档风控结果
ManagerDecision       # execute | reduce | wait
MarketContext         # 流水线共享上下文（只读输入）
ExternalFactors       # DXY、新闻等
AgentTrace            # 全链路审计（含 analyst_team）
```

均提供 `to_dict()` 用于 JSON 序列化。

---

## 7. 开发与扩展

### 7.1 修改结构检测

文件：`src/analysis/ict_pa.py`

- `_find_swings(df, left=3, right=3)` — 局部极值窗口
- BOS/CHoCH 判定
- OB/FVG 检测

验证：`run_analysis()` 后检查 `analyses["5m"].events` 等，或 `LOG_LEVEL=DEBUG`。

### 7.2 修改交易信号

文件：`src/analysis/report_engine.py`

- `generate_trading_signals()` — 信号几何与模板逻辑
- `compute_trading_signals(ctx)` — 从 `MarketContext` 组装参数（orchestrator 入口）
- `build_report(..., signals=...)` — 传入则跳过内部生成

Trader 只消费 orchestrator 传入的 `signals`；Manager 按 index 重排 `report["signals"]`。

### 7.3 新增 pipeline 阶段

1. 在 `src/agents/` 或新包实现 `run_xxx(ctx) -> XxxResult`；
2. 在 `orchestrator.py` 插入调用；
3. 扩展 `AgentTrace` 或 `report` 字段；
4. 可选：更新 `viz/agent_trace_view.py`。

### 7.4 接入 LLM 多智能体

完整设计见 **[llm-agents.md](./llm-agents.md)**。

- **调度**：`agents/factory.py`，`AGENT_MODE=rule|llm|hybrid`
- **分阶段开关**：`LLM_STAGE_ANALYSTS`、`LLM_STAGE_RESEARCH`、`LLM_STAGE_DEBATE`（`LLM_STAGE_ICT/TRADER/RISK/MANAGER` 已在 config 定义，factory 尚未接入）
- **单 Analyst 调试**：`LLM_ANALYST_ONLY=technical|fundamentals|news|sentiment` 时，仅该 Analyst 走 LLM，其余使用规则输出补齐
- **传输重试**：`agents/llm/base.py` 的 `stream_llm_json()` — SSE 断流时整次重打，最多 3 次、退避 1s/2s；`llm/client.py` 将 `ChunkedEncodingError` 等包装为 `LLMClientError`
- **规则兜底**：重试耗尽或 JSON 解析失败 → hybrid 回退 `agents/bullish.py` 等规则实现；流水线不崩溃
- **报告文案层**（流水线末尾）：`llm/analyst.py`，同样经 `stream_llm_json()`，`LLM_ENABLED` 独立开关
- 配置统一在 `config.py` + `.env.example`

### 7.5 代码约定

- 文件头 `from __future__ import annotations`；
- 日志：`log = get_logger(__name__)`；
- **勿改** `run_analysis()` 返回类型签名，除非同步改 `app.py` 与 viz。

---

## 8. 调试

### 8.1 日志

```env
LOG_LEVEL=DEBUG
LOG_FILE=logs/goldanalysisai.log
```

| 模块 | 内容 |
|------|------|
| `src.data.tradingview` | 请求、重试、bar 数量 |
| `src.core.orchestrator` | 每阶段 trend/bos/choch、耗时 |
| `src.analysis.report_engine` | signals 数量、sentiment |

### 8.2 Agent trace

```python
trace = report["agent_trace"]
trace["analyst_team"]["technical"]["summary"]   # Analyst Team
trace["debate"]["discussion_notes"]
trace["decision"]   # action, selected_signal_indices, summary
report["meta"]["llm_io"]   # Analyst Team 规则 I/O + LLM 阶段
```

### 8.3 其他

```bash
python tests/tools/chart_compare.py
```

---

## 9. 性能说明

| 项目 | 行为 |
|------|------|
| 报告生成 | 首次进入或「刷新报告」时全量执行，约 2–3 分钟 |
| 切换页面 | 复用 `session_state` 缓存，秒开 |
| LLM 耗时 | 研究阶段 30–90s/次属正常（V4-Pro）；传输断流自动重试，不拖垮整条 pipeline |
| 数据拉取 | 2 次 TV 请求 + resample，典型 3–15s |

---

## 10. 常见问题

| 现象 | 原因 / 处理 |
|------|-------------|
| 「数据获取失败」 | TradingView WebSocket 不可达；检查代理、`TV_USERNAME/PASSWORD` |
| EMA610 异常 | 历史 bar 不足；增大 `n_bars` 或登录 TV |
| 改了代码 UI 不变 | 重启 Streamlit；已缓存报告需点「刷新报告」 |
| LLM 模型名不对 | `config.py` import 时读 `.env`；各阶段见 `stage_sources.llm.model` |
| LLM 阶段报错但报告仍有内容 | hybrid 已回退规则；查看 `stage_sources` 与 `llm_io` 中 `error` 字段 |
| SSE 断流 / ChunkedEncoding | `stream_llm_json` 自动整次重打（最多 3 次）；仍失败则 hybrid 用规则 |
| 看多/看空耗时差大 | 同模型下 Prompt 体量不同，30–90s/次属正常 |
| 胜率 % | **非回测**；`sentiment_score()` 多周期趋势加权 |
| DXY/新闻/社媒 | `dxy.py`、`jin10_feed.py`、`news.py`、`social_feed.py` |

---

## 11. 测试与路线图

自动化测试见 [`tests/`](../tests/README.md) 与 [`tests/cases/catalog.yaml`](../tests/cases/catalog.yaml)。

```bash
python tests/run.py --fast       # 日常 / CI（约 77 项）
python tests/run.py --external   # 外部 API 冒烟（需网络）
python tests/run.py --financial  # FIN-* 金融 Review
python tests/run.py --full       # 发版前（含流水线）
```

手工检查（尚未自动化，见 catalog `UI-*` / `FIN-UI-*`）：

- [ ] 生成步骤含「构建市场上下文」与 external 子步骤；I/O 含 context 规则记录
- [ ] 生成步骤含 `Analyst Team`；I/O 含四位分析师 LLM 或规则输出
- [ ] 「LLM决策链」三 Tab：智能体决策 / LLM 文案 / 生成与 LLM I/O
- [ ] 顶栏与「外部数据 · 实时拉取」面板展示 DXY/新闻/日历/TV 社媒（实时数据或明确占位/回退说明）
- [ ] Analyst Team 四列 badge 与 stage_sources 一致
- [ ] 两种报告模式渲染正常；结构权重标注「非回测胜率」

| 优先级 | 任务 | 状态 |
|--------|------|------|
| P0 | Analyst Team 规则版 + 智能体 I/O | ✅ |
| P0 | factory + LLM 研究 + 辩论 + 流式 I/O + 传输重试 | ✅ |
| P1 | Analyst Team LLM 双轨（`LLM_STAGE_ANALYSTS`） | ✅ |
| P1 | 信号生成去重（trader / report 共用） | ✅ |
| P1 | 真实 News / DXY / 社媒 API | ✅ |
| P1 | 流水线并行（bull/bear、Analyst×4、risk×3） | 🔲 |
| P4 | 报告文案层 | ✅ |
| P1 | LLM 交易员 | 🔲 |
| P2 | LLM 风控 + 经理 | 🔲 |
| P3 | ICT Interpreter + DXY | 🔲 |
| P5 | HTML/PDF 导出 | 🔲 |
| P6 | 回测 | 🔲 |

---

## 12. 相关文档

| 文档 | 内容 |
|------|------|
| [README.md](./README.md) | 文档中心索引 |
| [developer-onboarding.md](./developer-onboarding.md) | 开发者入门 |
| [cheat-sheet.md](./cheat-sheet.md) | 改功能速查 |
| [glossary.md](./glossary.md) | 术语表 |
| [walkthrough.md](./walkthrough.md) | UI 动线 |
| [examples/report-schema.md](./examples/report-schema.md) | 报告 JSON |
| [architecture.md](./architecture.md) | TradingAgents 对照 |
| [llm-agents.md](./llm-agents.md) | LLM 双轨、传输重试、智能体 I/O、硅基流动配置 |
| [analyst-context.md](./analyst-context.md) | Analyst Team 输入密度与配置 |
| [jin10-mcp.md](./jin10-mcp.md) | 金十 MCP 接入 |
| [financial-review.md](./financial-review.md) | 金融逻辑评审与 FIN-* 用例追溯 |
| [reverse-engineering.md](./reverse-engineering.md) | 报告各区块算法反推 |
| [tests/README.md](../tests/README.md) | 测试套件与面板 |
| [README.md](../README.md) | 项目快速开始 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
