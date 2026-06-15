# Analyst Team 输入密度

Analyst Team（技术 / 基本面 / 新闻 / 情绪）共享三层信息架构：

| 层级 | 模块 | 内容 |
|------|------|------|
| **Layer 1 — RawFacts** | `fetch_pipeline` + `sources/*` | K 线、金十快讯/资讯/日历、DXY/US10Y、TV 社媒 |
| **Layer 2 — Derived** | `data/context_builder.py` | EMA/VWAP 位置、结构情绪、日历高影响计数 |
| **Layer 3 — Evidence** | `agents/analysts/*` | `AnalystReport.items`（规则 + LLM 共用） |

## 结构化类型（`core/types.py`）

- `HeadlineItem` — 金十快讯 / 资讯（source, time, title, text, url）
- `CalendarEvent` — 财经日历（time, region, event, importance）
- `MacroQuote` — DXY / US10Y 快照（close, change_pct, impact, bias）

`ExternalFactors` 同时保留 legacy 字段 `news_headlines` / `risk_events`（供 UI 与旧逻辑），并由 `sync_external_legacy_fields()` 自动同步。

## 配置（`.env`）

```env
# 金十拉取（fetch 层）
JIN10_FLASH_LIMIT=8
JIN10_ARTICLE_LIMIT=6
JIN10_NEWS_LIMIT=12

# Analyst / LLM payload 上限
ANALYST_NEWS_MAX=20
ANALYST_CALENDAR_MAX=12
ANALYST_SOCIAL_MAX=15
ANALYST_ICT_EVENTS_MAX=8
ANALYST_TEAM_ITEMS_MAX=16
PAYLOAD_EVIDENCE_MAX=20

# 宏观
TV_US10Y_EXCHANGE=TVC
TV_US10Y_SYMBOL=US10Y

# 金十 spot / K 线交叉校验
JIN10_QUOTE_ENABLED=true
JIN10_KLINE_ENABLED=true
JIN10_KLINE_COUNT=20
LLM_MIN_ANALYST_ITEMS=4
```

## 数据流

```
fetch_all_data()
  → merge_external(news, fundamentals, social)
  → assemble_market_context()
  → finalize_market_context()   # derived + context_stats
  → agent_factory.run_analyst_team(ctx)
```

## LLM Payload（`agents/llm/payload.py`）

| 分析师 | 专用 payload 增强 |
|--------|-------------------|
| technical | `market_position`, EMA/VWAP 关系, ICT events 按优先级排序 |
| fundamentals | `macro_quotes[]`, 高影响日历计数 |
| news | 分 channel 的 flash / article / calendar + `news_topics` |
| sentiment | 完整 `social_posts`（上限 `ANALYST_SOCIAL_MAX`） |

## 可观测性

- `MarketContext.context_stats` — headline/calendar/macro/ICT 计数 + external payload 字节数
- `report["meta"]["context_stats"]` — 写入报告 meta，便于对比生成批次
- `derived.event_countdown` — 距下一高影响日历事件的小时数
- `derived.jin10_kline_summary` — 金十 K 线与 TV 价格偏差摘要
- Analyst Team `stage_io` input 含 `context_stats`（规则/LLM 双轨）
- 单元测试：`tests/unit/test_analyst_input_density.py`

## 路线图状态（Phase 0–6）

| Phase | 内容 | 状态 |
|-------|------|------|
| 0 | context_stats 基线 + 密度测试 | ✅ |
| 1 | HeadlineItem/CalendarEvent/MacroQuote + US10Y + get_quote/kline | ✅ |
| 2 | 按角色 payload 选编 + 配置上限 | ✅ |
| 3 | 规则分析师加深 + 去重 fetch | ✅ |
| 4 | LLM prompt 分 channel + min items + source | ✅ |
| 5 | 辩论层 topics/calendar/countdown | ✅ |
| 6 | 可观测性 + 并行 fetch + 全量测试 | ✅ |

## 后续迭代（Phase 3+）

- [x] 金十 MCP `get_quote` spot 与 TV 价格交叉校验（`derived.spot_cross_check`）
- [x] 金十 MCP `get_kline` 摘要（`derived.jin10_kline_summary`）
- [x] 新闻主题聚类（`derived.news_topics` → 辩论层）
- [x] 日历事件倒计时（`derived.event_countdown`）
- [x] LLM 最小 evidence 条数校验（`LLM_MIN_ANALYST_ITEMS`）
- [x] LLM items 自动补全 `refs.source`
- [x] 技术分析师 FVG/OB 距离现价 evidence
- [x] 并行拉取 macro + news + social（`fetch_external_bundle` 三线程）
- [x] LLM prompt 分 channel 细化（快讯 vs 资讯 vs 日历）
