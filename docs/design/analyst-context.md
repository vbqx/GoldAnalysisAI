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

| 能力 | 当前落地内容 |
|------|--------------|
| 技术输入可观测 | 在 `context_stats.technical_inputs` 记录每周期 K 线数量、结构事件、OB/FVG/liquidity、premium/discount、volume signal、volume 有效性与指标 readiness |
| 技术 evidence 补齐 | 将 `1d` 趋势、premium/discount、equilibrium、volume signal、liquidity 与 Fibonacci 价位转成 `technical_analyst.items` |
| 上下文统一 | `analysis/technical_context.py` 统一规则技术分析师、LLM 技术分析师、最终叙事层的技术上下文字段 |
| 指标扩展 | 基于 OHLCV 增加 ATR14、RSI14、MACD、ADX14，并将动能/波动率/趋势强度转成 evidence |
| 质量降级 | 技术质量评分检查 K 线数量、indicator warm-up、volume 有效性与 ICT 输入；输入不足时降低 confidence 并在 summary 标注原因 |
| 支撑阻力上下文 | 从日高/日低、swing、equilibrium、Fib、liquidity、OB/FVG 聚合 support/resistance/neutral levels，并输出最近支撑/压力 evidence |

以上能力已在规则技术分析师、LLM 技术 payload 与最终 narrative payload 中落地；指标权重和历史校准计划见 [roadmap.md](../planning/roadmap.md)。

## ICT / PA / SMC 输入审计

| 输入 | 状态 | 说明 |
|------|------|------|
| Swing structure | ✅ 简化实现 | 3-left/3-right 局部高低点 + 多周期 trend |
| BOS / CHoCH | ✅ 简化实现 | 最新 close 相对近期 swing high/low 判定 |
| FVG | ✅ 基础实现 | 三 K 缺口 + active FVG 过滤 |
| Order Block | ⚠️ 启发式 | 三 K 推动前反向 K，未包含 mitigation/breaker 生命周期 |
| Liquidity | ⚠️ 部分实现 | Equal highs/lows、stop hunt offset 已随 ATR/价格缩放，并记录 `swept` 标记 |
| Premium / Discount | ✅ 简化实现 | swing range 中点 equilibrium + premium/discount |
| Volume / Displacement | ⚠️ 部分实现 | volume ratio + OB 内隐 displacement；尚未有 ATR 标准化 displacement |
| Support / Resistance | ✅ 已实现 | P5 聚合日高/日低、swing、Fib、liquidity、OB/FVG，并进入 technical evidence |
| Multi-TF confluence | ⚠️ 部分实现 | 趋势投票 + 最近 S/R；尚未有跨周期 zone overlap score |
| Kill zones / Sessions | ❌ 未实现 | 未按 London/NY/Asia 时段标注结构事件 |
| Breaker / Mitigation blocks | ❌ 未实现 | 仍需 OB/FVG lifecycle 状态 |
| Liquidity sweep detection | ⚠️ 部分实现 | `report_engine` 已对 sweep long 检查扫穿深度、收回和 bullish BOS/CHoCH；尚未形成完整 session/kill zone 级 ICT 事件模型 |
| PDH/PDL / prior sessions | ❌ 未实现 | 当前只有日高/日低/前收，缺前日/前周/Session 高低点记忆 |

## 其他分析师输入优化方案

目标：让 fundamentals / news / sentiment 三位分析师像技术分析师一样，把已经抓取或派生出的输入转成可审计 evidence，并把输入质量写入 `context_stats`。

| 分析师 | 当前输入覆盖 | 输出约束 |
|--------|--------------|----------|
| fundamentals | DXY/US10Y quote、高影响日历、下一事件倒计时、来源覆盖与 fetch error | 只把已抓取或明确 fallback 的宏观输入转成 evidence |
| news | headline/calendar evidence、新闻主题、渠道密度、Jin10 live/fallback 状态 | 区分快讯、资讯和日历，不把 fallback 当实时事实 |
| sentiment | 结构投票、社媒帖子、样本质量、bias_delta、长短周期结构分歧 | 社媒仅作轻量辅助，不能覆盖结构主导方向 |

## 架构边界与 Review 结论

- `context_builder.finalize_market_context()` 是唯一写入 `derived` 与 `context_stats` 的入口；规则分析师只消费 `MarketContext`，不重新 fetch 外部源。
- `context_stats.technical_inputs` / `context_stats.analyst_inputs` 是可观测性与质量审计字段，不直接等同于交易信号。
- 规则分析师负责把可用输入转成 `EvidenceItem`；技术上下文由 `analysis/technical_context.py` 共享给规则技术分析师、LLM Analyst payload 与最终 narrative payload。
- 当前已完成：输入密度可观测、规则 evidence 补齐、共享 technical context、OHLCV 指标扩展、输入不足质量降级、支撑阻力上下文。

## 专项边界

流动性质量专项不在本文重复维护。实现边界见 [architecture.md §8.2](./architecture.md#82-流动性质量层)，后续计划见 [roadmap.md](../planning/roadmap.md#流动性质量专项)，金融验收见 [financial-review.md](../domain/financial-review.md#2026-06-21-流动性可靠性验收口径)。
