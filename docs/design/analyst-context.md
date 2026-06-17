# Analyst Team 输入密度

Analyst Team（技术 / 基本面 / 新闻 / 情绪）共享三层信息架构。文档索引见 [README.md](../README.md)。

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
- `MarketContext.context_stats["technical_inputs"]` — 技术侧 K 线、OB/FVG、liquidity、premium/discount、volume 与指标可用性
- `MarketContext.context_stats["analyst_inputs"]` — 基本面 / 新闻 / 情绪分角色输入数量、来源覆盖与样本质量
- `report["meta"]["context_stats"]` — 写入报告 meta，便于对比生成批次
- `derived.event_countdown` — 距下一高影响日历事件的小时数
- `derived.jin10_kline_summary` — 金十 K 线与 TV 价格偏差摘要
- Analyst Team `stage_io` input 含 `context_stats`（规则/LLM 双轨）
- 单元测试：`tests/unit/test_analyst_input_density.py`

## 技术分析输入优化方案

问题：K 线与 ICT 引擎已经产出多周期结构，但规则版技术分析师只稳定消费部分输入，导致后续研究/辩论/报告可能基于过窄 evidence 做判断。

| 阶段 | 目标 | 落地内容 |
|------|------|----------|
| P0 | 技术输入可观测 | 在 `context_stats.technical_inputs` 记录每周期 K 线数量、结构事件、OB/FVG/liquidity、premium/discount、volume signal、volume 有效性与指标 readiness |
| P1 | 技术 evidence 补齐 | 将 `1d` 趋势、premium/discount、equilibrium、volume signal、liquidity 与 Fibonacci 价位转成 `technical_analyst.items` |
| P2 | 上下文统一 | `analysis/technical_context.py` 统一规则技术分析师、LLM 技术分析师、最终叙事层的技术上下文字段 |
| P3 | 指标扩展 | 基于 OHLCV 增加 ATR14、RSI14、MACD、ADX14，并将动能/波动率/趋势强度转成 evidence |
| P4 | 质量降级 | 技术质量评分检查 K 线数量、indicator warm-up、volume 有效性与 ICT 输入；输入不足时降低 confidence 并在 summary 标注原因 |
| P5 | 支撑阻力上下文 | 从日高/日低、swing、equilibrium、Fib、liquidity、OB/FVG 聚合 support/resistance/neutral levels，并输出最近支撑/压力 evidence |

当前实施范围：P0-P5 已在规则技术分析师、LLM 技术 payload 与最终 narrative payload 中落地；后续可继续细化指标权重与历史回测校准。

## ICT / PA / SMC 输入审计

| 输入 | 状态 | 说明 |
|------|------|------|
| Swing structure | ✅ 简化实现 | 3-left/3-right 局部高低点 + 多周期 trend |
| BOS / CHoCH | ✅ 简化实现 | 最新 close 相对近期 swing high/low 判定 |
| FVG | ✅ 基础实现 | 三 K 缺口 + active FVG 过滤 |
| Order Block | ⚠️ 启发式 | 三 K 推动前反向 K，未包含 mitigation/breaker 生命周期 |
| Liquidity | ⚠️ 部分实现 | Equal highs/lows、stop hunt offset；尚未检测 sweep event |
| Premium / Discount | ✅ 简化实现 | swing range 中点 equilibrium + premium/discount |
| Volume / Displacement | ⚠️ 部分实现 | volume ratio + OB 内隐 displacement；尚未有 ATR 标准化 displacement |
| Support / Resistance | ✅ 已实现 | P5 聚合日高/日低、swing、Fib、liquidity、OB/FVG，并进入 technical evidence |
| Multi-TF confluence | ⚠️ 部分实现 | 趋势投票 + 最近 S/R；尚未有跨周期 zone overlap score |
| Kill zones / Sessions | ❌ 未实现 | 未按 London/NY/Asia 时段标注结构事件 |
| Breaker / Mitigation blocks | ❌ 未实现 | 仍需 OB/FVG lifecycle 状态 |
| Liquidity sweep detection | ❌ 未实现 | 交易模板有“扫低”，但没有 wick sweep + reclaim 检测 |
| PDH/PDL / prior sessions | ❌ 未实现 | 当前只有日高/日低/前收，缺前日/前周/Session 高低点记忆 |

## 其他分析师输入优化方案

目标：让 fundamentals / news / sentiment 三位分析师像技术分析师一样，把已经抓取或派生出的输入转成可审计 evidence，并把输入质量写入 `context_stats`。

| 分析师 | 当前缺口 | P0/P1 落地 |
|--------|----------|------------|
| fundamentals | 主要消费 DXY/US10Y quote；日历高影响事件、事件倒计时、宏观来源覆盖没有稳定变成 evidence | 增加高影响日历、下一事件倒计时、DXY/US10Y 覆盖与 fetch error 质量 evidence |
| news | 已有 headline/calendar evidence；但 topic 聚类、flash/article/calendar 渠道密度、来源质量没有进入规则输出 | 增加新闻主题、渠道密度、Jin10 live/fallback 状态 evidence |
| sentiment | 已有结构投票和社媒帖子；但社媒样本数量、kind 分布、bias_delta 汇总、长短周期结构分歧没有进入 summary/evidence | 增加社媒样本质量、社媒 bias_delta、结构趋势分歧 evidence，并只在结构投票接近时用社媒作轻量 tie-break |

后续迭代：基本面可加入实际利率/美元篮子，新闻可加入去重与事件影响窗口，情绪可加入社媒质量权重和异常样本过滤。

## 架构边界与 Review 结论

- `context_builder.finalize_market_context()` 是唯一写入 `derived` 与 `context_stats` 的入口；规则分析师只消费 `MarketContext`，不重新 fetch 外部源。
- `context_stats.technical_inputs` / `context_stats.analyst_inputs` 是可观测性与质量审计字段，不直接等同于交易信号。
- 规则分析师负责把可用输入转成 `EvidenceItem`；技术上下文由 `analysis/technical_context.py` 共享给规则技术分析师、LLM Analyst payload 与最终 narrative payload。
- 当前已完成 P0-P5：输入密度可观测、规则 evidence 补齐、共享 technical context、OHLCV 指标扩展、输入不足质量降级、支撑阻力上下文。

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
- [x] 技术分析师补齐 `1d`、premium/discount、volume、liquidity 与 Fibonacci evidence
- [x] 技术输入密度写入 `context_stats.technical_inputs`
- [x] 技术上下文共享给 rule technical、LLM technical 与 narrative payload
- [x] ATR14 / RSI14 / MACD / ADX14 指标扩展与质量降级
- [x] Support / resistance context 与最近支撑/压力 evidence
- [x] fundamentals/news/sentiment 补齐输入密度、来源质量与主题/样本 evidence
- [x] 分角色输入密度写入 `context_stats.analyst_inputs`
- [x] 并行拉取 macro + news + social（`fetch_external_bundle` 三线程）
- [x] LLM prompt 分 channel 细化（快讯 vs 资讯 vs 日历）
