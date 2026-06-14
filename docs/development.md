# GoldAnalysisAI 开发文档

说明本仓库的架构、执行路径、模块职责与扩展方式。

---

## 1. 项目是什么

GoldAnalysisAI 是一个 **XAUUSD 分析报告生成器**：

1. 从 TradingView 拉多周期 OHLCV；
2. 计算 EMA/VWAP/Fib，做 ICT/PA 结构检测（BOS、CHoCH、OB、FVG）；
3. 经多阶段「智能体」流水线（研究 → 辩论 → 交易 → 风控 → 经理）产出交易提案；
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
- 内部流水线参考 [TradeAgent](https://github.com/TauricResearch/TradingAgents)；
- 数据源通过 Protocol 解耦，便于替换实现。

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
| `LOG_LEVEL` | `INFO` | `DEBUG` 可跟踪流水线 |
| `LOG_FILE` | 空 | 如 `logs/goldanalysisai.log` |
| `AGENT_MODE` | `rule` | `rule` / `llm` / `hybrid`，见 [llm-agents.md](./llm-agents.md) |
| `LLM_*` | 见 `.env.example` | 硅基流动 / OpenAI 兼容 API |

配置在 **`src/config.py`** 读取环境变量（模块 import 时自动加载 `.env`）；`app.py` 在 import 前也会预加载 `.env`。

### 2.4 运行

```bash
streamlit run app.py    # http://localhost:8501
```

**多页面**（`st.navigation` 左侧导航，`app.py` 仅作路由入口，不显示为「app」页）：

| 页面 | 文件 |
|------|------|
| 机构级分析报告 | `views/1_机构级分析报告.py` |
| 短线策略 | `views/2_短线策略.py` |
| LLM决策链 | `views/3_LLM决策链.py` |

**缓存策略**：`ensure_report()`（`src/viz/streamlit_common.py`）后台线程跑流水线 + `session_state` 缓存。切换页面或点击控件**不**重跑；仅首次进入、浏览器刷新或点 **「刷新报告」** 才重新生成。生成等待期间机构页展示与 LLM 决策链相同的步骤 / I/O Tab（每秒刷新）。

首次进入或刷新后约需 2–3 分钟。无 UI 测试：

```bash
python scripts/run_pipeline_test.py
```

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
analyze_timeframe() × 4  →  dict[str, TimeframeAnalysis]  analyses
        │
        ▼  [data/aggregator.py]
build_market_context()  →  MarketContext  ctx
        │
        ▼  [agents/factory.py]
bullish / bearish → debate → trader → risk → manager
  (rule / llm / hybrid，经 factory 调度)
        │
        ▼  [llm/analyst.py]  （可选，LLM_ENABLED）
报告文案层
        │
        ▼  [analysis/report_engine.py]
build_report()  →  dict  report
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

### 3.3 阶段二：TradingView 拉数

| 顺序 | 函数 | 文件 | 说明 |
|------|------|------|------|
| 1 | `fetch_multi_timeframe()` | `src/data/fetcher.py` | facade，转调 tradingview |
| 2 | `fetch_multi_timeframe()` | `src/data/tradingview.py` | 组装 5m/15m/1h/4h/1d |
| 3 | `_get_client()` | `src/data/tradingview.py` | 单例 `TvDatafeed()` |
| 4 | `_fetch_bars()` | `src/data/tradingview.py` | 调用 `tv.get_hist()`，重试 2 次 |
| 5 | `_normalize()` | `src/data/tradingview.py` | 列名 → Open/High/Low/Close/Volume |
| 6 | `_resample()` | `src/data/tradingview.py` | 5m 聚合为 15m / 1h / 4h |
| 7 | `source_label()` | `src/data/tradingview.py` | 数据源标签字符串 |

**请求次数**：2 次（5000×5m + 365×1d）；15m/1h/4h 本地 resample，不再请求。

**输出变量**（orchestrator 内）：`raw: dict[str, DataFrame]`，键为 `"5m" | "15m" | "1h" | "4h" | "1d"`。

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
| 1 | `build_market_context(enriched, analyses)` | `src/data/aggregator.py` | 组装 `MarketContext` |
| 2 | `daily_metrics(enriched["1d"])` | `src/data/fetcher.py` | 现价、日涨跌、日高日低 |
| 3 | `get_active_source()` | `src/data/fetcher.py` | → `tradingview.source_label()` |
| 4 | `merge_external()` | `src/data/aggregator.py` | 合并外部因子 |
| 5 | `NewsDataSource().fetch_external()` | `src/data/sources/news.py` | 新闻 / 风险事件（占位） |
| 6 | `FundamentalsDataSource().fetch_external()` | `src/data/sources/fundamentals.py` | DXY 等（占位） |
| 7 | `collect_evidence()` | `src/data/aggregator.py` | 调各 DataSource（日志用） |

**输出变量**：`ctx: MarketContext`（含 `enriched`、`analyses`、`metrics`、`price`、`external`）。

---

### 3.7 阶段六：智能体流水线

| 顺序 | 函数 | 文件 | 输入 → 输出 |
|------|------|------|-------------|
| 1 | `agent_factory.run_bullish(ctx, pipeline_meta)` | `src/agents/factory.py` | → `AgentEvidence`（rule/llm/hybrid） |
| 2 | `agent_factory.run_bearish(...)` | 同上 | → `AgentEvidence` |
| 3 | `agent_factory.run_debate(...)` | 同上 | → `ResearchDebate` |
| 4 | `agent_factory.run_trader(...)` | 同上 | → `(TransactionProposal, signals[])` |
| 5 | `generate_trading_signals(...)` | `src/analysis/report_engine.py` | trader 内部调用 |
| 6 | `agent_factory.run_risk(...)` | `src/agents/factory.py` | → `RiskReview[3]` |
| 7 | `agent_factory.run_manager(...)` | 同上 | → `ManagerDecision` |

研究员内部均调用 `_structure_items(analyses)` 从结构中提取证据。

---

### 3.8 阶段七：报告组装与 orchestrator 收尾

**`build_report(enriched, analyses)`**（`src/analysis/report_engine.py`）内部调用：

| 函数 | 产出字段 |
|------|----------|
| `daily_metrics(data["1d"])` | `metrics` |
| `sentiment_score(analyses)` | `sentiment` |
| `fibonacci_levels(...)` | `fibonacci` |
| `generate_trading_signals(...)` | `signals` |
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
| `report["meta"]["generation_steps"]` | 生成步骤与耗时 |
| `report["meta"]["llm_io"]` | 全部 LLM 调用的输入/输出 |
| `AgentTrace(...).to_dict()` → `report["agent_trace"]` | 决策审计链 |
| `run_llm_analysis` + `apply_llm_to_report` | `report["llm_analysis"]`、增强 `conclusion` |
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
| `build_sentiment_donut()` | `src/viz/charts.py` | `report["sentiment"]` |
| `build_projection_chart()` | `src/viz/charts.py` | `report["projections"]` |
| `render_agent_source_banner()` | `src/viz/source_labels.py` | 顶栏 规则/LLM 来源 |
| `StreamlitProgressReporter` | `src/viz/pipeline_progress.py` | 进度 + LLM 流式 I/O |
| `render_llm_io_history()` | 同上 | 侧边栏 LLM 历史 |
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
├── docs/
├── scripts/chart_compare_test.py
└── src/
    ├── pipeline.py             # 对外 API 薄封装
    ├── config.py               # 环境变量 → 模块级常量
    ├── log.py                  # logging 初始化
    ├── core/
    │   ├── types.py            # dataclass 定义
    │   ├── progress.py         # 进度 + LLM I/O（contextvar）
    │   └── orchestrator.py     # 流水线编排
    ├── data/
    │   ├── tradingview.py      # 网络 I/O + resample
    │   ├── fetcher.py          # facade
    │   ├── aggregator.py       # MarketContext 组装
    │   └── sources/            # 可插拔 DataSource
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

经 **`factory.py`** 调度，支持 `AGENT_MODE=rule|llm|hybrid`。规则实现仍在 `bullish.py` 等；LLM 实现在 `agents/llm/stages/`。

| 阶段 | factory 入口 | 规则实现 | LLM 实现 |
|------|-------------|----------|----------|
| Research | `run_bullish` / `run_bearish` | `bullish.py` / `bearish.py` | `llm/stages/bullish.py` 等 |
| Debate | `run_debate` | `debate.py` | `llm/stages/debate.py` |
| Trade | `run_trader` | `trader.py` | P1 规划中 |
| Risk | `run_risk` | `risk.py` | P2 规划中 |
| Manager | `run_manager` | `manager.py` | P2 规划中 |

`run_manager` 优先级：**conservative** → **neutral** → **aggressive**；全否决则 `action="wait"`。

### 5.6 报告引擎 `analysis/report_engine.py`

`build_report(data, analyses) -> dict` 生成 UI schema。Orchestrator 随后注入：

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
| `pipeline_progress.py` | 生成进度 + LLM 流式面板 |
| `source_labels.py` | 规则/LLM 来源条 |
| `llm_view.py` | LLM 文案侧边栏 |

**分层原则**：viz 只读 `report`/`data`/`analyses`，不 import agents。

---

## 6. 领域类型（`core/types.py`）

读 agents 前先扫一遍此文件，这是项目的类型定义中心：

```
EvidenceItem          # 单条证据
AgentEvidence         # 某研究员输出
ResearchDebate        # 辩论结果 + consensus_bias
TransactionProposal   # 方向 + signal 索引列表
RiskReview            # 某档风控结果
ManagerDecision       # execute | reduce | wait
MarketContext         # 流水线共享上下文（只读输入）
ExternalFactors       # DXY、新闻等
AgentTrace            # 全链路审计（序列化进 report）
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

文件：`src/analysis/report_engine.py` → `generate_trading_signals()`

Trader agent 自动消费；Manager 按 index 重排。

### 7.3 新增 pipeline 阶段

1. 在 `src/agents/` 或新包实现 `run_xxx(ctx) -> XxxResult`；
2. 在 `orchestrator.py` 插入调用；
3. 扩展 `AgentTrace` 或 `report` 字段；
4. 可选：更新 `viz/agent_trace_view.py`。

### 7.4 接入 LLM 多智能体

完整设计见 **[llm-agents.md](./llm-agents.md)**。

- **调度**：`agents/factory.py`，`AGENT_MODE=rule|llm|hybrid`
- **分阶段开关**：`LLM_STAGE_RESEARCH`、`LLM_STAGE_DEBATE` 等
- **规则兜底**：LLM 失败自动回退 `agents/bullish.py` 等规则实现
- **报告文案层**（流水线末尾）：`llm/analyst.py`，`LLM_ENABLED` 独立开关
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
trace["debate"]["discussion_notes"]
trace["decision"]   # action, selected_signal_indices, summary
```

### 8.3 其他

```bash
python scripts/chart_compare_test.py
```

---

## 9. 性能说明

| 项目 | 行为 |
|------|------|
| 报告生成 | 首次进入或「刷新报告」时全量执行，约 2–3 分钟 |
| 切换页面 | 复用 `session_state` 缓存，秒开 |
| LLM 耗时 | 研究阶段 30–90s/次属正常（V4-Pro）；UI 统一显示秒，并去重 JSON 重试记录 |
| 数据拉取 | 2 次 TV 请求 + resample，典型 3–15s |

---

## 10. 常见问题

| 现象 | 原因 / 处理 |
|------|-------------|
| 「数据获取失败」 | TradingView WebSocket 不可达；检查代理、`TV_USERNAME/PASSWORD` |
| EMA610 异常 | 历史 bar 不足；增大 `n_bars` 或登录 TV |
| 改了代码 UI 不变 | 重启 Streamlit；已缓存报告需点「刷新报告」 |
| LLM 模型名不对 | `config.py` import 时读 `.env`；各阶段见 `stage_sources.llm.model` |
| 看多/看空耗时差大 | 同模型下 Prompt 体量不同，30–90s/次属正常 |
| 胜率 % | **非回测**；`sentiment_score()` 多周期趋势加权 |
| DXY/新闻占位 | `sources/news.py` 等待接 API；orchestrator 写入 `report["external"]` |

---

## 11. 测试与路线图

**当前无自动化测试。** 手动检查：

- [ ] 生成进度与 LLM 流式 I/O 正常显示
- [ ] 侧边栏「LLM 输入/输出」有完整记录
- [ ] 顶栏来源条与决策链徽章正确
- [ ] 两种报告模式渲染正常
- [ ] `python scripts/run_pipeline_test.py` 输出 `OK price=...`

| 优先级 | 任务 | 状态 |
|--------|------|------|
| P0 | factory + LLM 研究 + 辩论 + 流式 I/O | ✅ |
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
| [architecture.md](./architecture.md) | TradeAgent 对照、分层图 |
| [llm-agents.md](./llm-agents.md) | LLM 双轨、流式 I/O、硅基流动配置 |
| [reverse-engineering.md](./reverse-engineering.md) | 报告各区块算法反推 |
| [README.md](../README.md) | 快速开始 |

---

## 免责声明

本项目仅供学习研究，不构成投资建议。
