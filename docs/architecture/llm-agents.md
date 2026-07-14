# LLM 多智能体架构

> **目标**：数据层保持确定性（TradingView + 指标 + 规则 ICT 事实），
> **Analyst Team**（技术/基本面/新闻/情绪）→ 多空研究 → 辩论 → 交易 → 风控 → 经理 各阶段可接入大模型。
> **约束**：`run_analysis()` 仍返回 `(report, data, analyses)`；报告 JSON schema 不变。

---

## 1. 设计原则

| 原则 | 说明 |
|------|------|
| **双轨实现** | 每阶段保留规则版 + LLM 版，经 `agents/factory.py` 统一调度 |
| **结构化输出** | LLM 返回 JSON（`response_format: json_object`），校验后进入流水线 |
| **规则兜底** | LLM 传输/解析失败自动重试（整次 SSE 重打 + 指数退避）；仍失败则 hybrid 回退规则版 |
| **流式可观测** | 机构页展示生成进度；LLM 完整 I/O 在「LLM决策链」页 |
| **可审计** | `stage_meta` 标 `rule/llm/hybrid`；`meta.llm_io` 存完整 I/O |
| **输入密度** | 结构化 `HeadlineItem` / `CalendarEvent` / `MacroQuote`；见 [analyst-context.md](./analyst-context.md) |
| **结论漏斗** | `LLM_PAYLOAD_FUNNEL=true`（默认）时，研究/辩论/交易员各阶段只读上游结论 + 最小校验上下文；见 §3.7 |

`src/agents/llm/payload.py` 负责 Analyst Team、研究与辩论阶段的结构化输入；`src/llm/context.py` 只服务最终报告文案层。技术字段由 `analysis/technical_context.py` 统一构造，再分别嵌入技术 Analyst payload 与 narrative-only payload，避免两层 JSON contract 互相污染。

---

## 2. 流水线总览

```
TradingView → enrich → ict_pa.analyze (规则事实)
                              │
                              ▼
              ┌───────────────────────────────────┐
              │  Analyst Team（rule / llm / hybrid，`LLM_STAGE_ANALYSTS`） │
              │  技术 · 基本面 · 新闻 · 情绪          │
              └───────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────────┐
              │  agents/factory.py                │
              │  AGENT_MODE: rule | llm | hybrid  │
              └───────────────────────────────────┘
                              │
     ┌────────────────────────┼────────────────────────┐
     ▼                        ▼                        ▼
 看多研究 (LLM)          看空研究 (LLM)           辩论 (LLM strong)
 research_payload        research_payload          debate_payload
 （analyst_team 为主）    （analyst_team 为主）      （research evidence）
     │                        │                        │
     └────────────────────────┴────────────────────────┘
                              ▼
              交易员 → 风控 → 经理  (trader 读 debate+signals；manager 仅 proposal+风控)
                              ▼
              report_engine.build_report（信号重排 + signal_role 在 orchestrator）
                              ▼
              llm/analyst.py 报告文案层 (LLM_ENABLED)
                              ▼
              views/3_LLM决策链.py — 来源标识 + 完整 LLM I/O 历史
```

---

## 3. 运行模式

### 3.1 `AGENT_MODE`

| 模式 | 行为 |
|------|------|
| `rule` | 全部规则（默认） |
| `llm` | 启用阶段走 LLM；失败回退规则 |
| `hybrid` | 规则先跑 baseline；LLM 置信度/强度 ≥ `LLM_OVERRIDE_THRESHOLD` 才覆盖 |

Streamlit 启动后会先显示 **生成前配置** 面板；用户选择规则 / LLM / 混合后，`RunConfig` 会在后台 worker 开始前同步到 `agents/factory.py`、`orchestrator.py` 与报告文案层。`.env` 仍作为默认值与 API key/model 来源。

### 3.2 模型路由

| 变量 | 用途 | 调用点 |
|------|------|--------|
| `LLM_MODEL_FAST` | Analyst Team + 研究阶段（四位分析师 / 看多/看空） | `llm/router.get_fast_client()` |
| `LLM_MODEL_STRONG` | 辩论 | `get_strong_client()` |
| `LLM_MODEL` | 报告文案层 | `llm/analyst.py` |

三者可设为同一模型（如 `deepseek-ai/DeepSeek-V4-Pro`）。

### 3.3 环境变量

```env
# 智能体模式
AGENT_MODE=hybrid

# 硅基流动（OpenAI 兼容）
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.siliconflow.cn/v1
LLM_MODEL=deepseek-ai/DeepSeek-V4-Pro
LLM_MODEL_FAST=deepseek-ai/DeepSeek-V4-Pro
LLM_MODEL_STRONG=deepseek-ai/DeepSeek-V4-Pro
LLM_TIMEOUT=120
LLM_CONNECT_TIMEOUT=30
LLM_READ_TIMEOUT=120
LLM_MAX_RETRIES=2
LLM_RETRY_BACKOFF_BASE_S=1.0
LLM_OVERRIDE_THRESHOLD=0.65

# 分阶段开关
LLM_STAGE_ANALYSTS=true
LLM_STAGE_RESEARCH=true
LLM_STAGE_DEBATE=true
LLM_STAGE_ICT=false
LLM_STAGE_LEVELS=true
LLM_STAGE_TRADER=true
LLM_STAGE_RISK=true
LLM_STAGE_MANAGER=true

# 可选：仅调试单个 Analyst LLM；留空或 all 表示四位都跑
LLM_ANALYST_ONLY=technical

# 报告结论文案层（独立于智能体链）
LLM_ENABLED=true
LLM_ENHANCE_CONCLUSION=true
```

`LLM_ANALYST_ONLY` 仅在 `LLM_STAGE_ANALYSTS=true` 且 `AGENT_MODE=llm|hybrid` 时生效；未选中的 Analyst 使用规则输出补齐，避免完整流水线等待四个 LLM 分析师全部完成。

### 3.4 传输重试与规则兜底

LLM 使用 OpenAI 兼容 **SSE 流式**；不支持流内续传，断流时**整次请求重打**。

| 环境变量 | 默认 | 含义 |
|----------|------|------|
| `LLM_TIMEOUT` | 60 | 遗留总超时；未单独设 connect/read 时 read 取此值 |
| `LLM_CONNECT_TIMEOUT` | `min(30, LLM_TIMEOUT)` | TCP/ TLS 建连超时（秒） |
| `LLM_READ_TIMEOUT` | `LLM_TIMEOUT` | 流式 **chunk 空闲**超时（秒）；长时间无 SSE 数据则失败 |
| `LLM_MAX_RETRIES` | 2 | 每阶段最多重试次数（实际尝试 = 1 + 此值，上限 5） |
| `LLM_RETRY_BACKOFF_BASE_S` | 1.0 | 指数退避基数（1s → 2s → 4s …） |

| 组件 | 行为 |
|------|------|
| `llm/client.py` | `requests.post(..., timeout=(connect, read))`；`ChunkedEncodingError`、连接/空闲超时 → `LLMClientError` |
| `agents/llm/base.py` `stream_llm_json()` | 传输失败最多 `LLM_MAX_RETRIES + 1` 次，指数退避 |
| `run_llm_stage()` | JSON 解析失败同样重试；传输与解析均失败 → 返回 `error` trace |
| `factory` hybrid | LLM 失败或置信度不足 → 采用规则版 `bullish`/`bearish`/`debate` |
| `llm/analyst.py` | 文案层经 `run_llm_stage()`（含传输 + JSON 重试）；失败写入 `llm_analysis.error`，不中断 pipeline |

单元测试：`tests/unit/test_llm_transport.py`、`tests/unit/test_llm_client_timeouts.py`。

### 3.5 规则智能体 — 金融 Review 三处改动（2026-06-20）

| 模块 | Finding | 行为摘要 | 单测 |
|------|---------|----------|------|
| `debate.py` | F-013 | `combined = 研究分 + sentiment_pct/50`；证据接近时以结构情绪 tiebreaker | `test_debate_coherence.py` |
| `trader.py` | F-014 | `sentiment_score` 门控主方向；偏空优先 short（强多共识 strength≥0.6 例外） | `test_trader_sentiment.py` |
| `factory.py` | — | `run_research_team` 并行 LLM 看多/看空；`run_parallel` 并行 Analyst Team | `test_research_parallel.py` |

编排层 `orchestrator.py`：研究阶段按 `research_uses_parallel_llm()` 分支；报告组装后按 sentiment 重排信号并写入 `signal_role`。门禁：`tests/tools/coherence_check.py`（rule 模式 `issues: []`）。

### 3.6 PA / SMC 提示词主次

字段释义与场景优先级集中在 `analysis/field_glossary.py`（`PA_SMC_PRIORITY`）。各 LLM 阶段注入对应 hint，**不得跨场景混用**：

| 场景 | 主 | 辅 | 注入位置 |
|------|----|----|----------|
| 报告五块叙事 | PA（POC/VAH/VAL、量价 S/R） | SMC 仅 `allowed_levels` 引用 | `llm/prompts.py`、`narrative_combine.py` |
| 交易计划 | PA 定区 | SMC 后台过滤 | `report_engine` → 文案 payload |
| 技术 Analyst / 多空研究 | SMC 定结构 | PA 确认共振 | `agents/llm/stages/analysts/technical.py`、`bullish.py`、`bearish.py` |

完整组合逻辑见 [smc-pa-narrative.md](./smc-pa-narrative.md)；检测与事实层见 [technical-analysis.md](./technical-analysis.md)。

### 3.7 结论漏斗（`LLM_PAYLOAD_FUNNEL`）

默认 `true`。各阶段 LLM 输入以**上游结论**为主，避免重复塞入 raw facts：

| 阶段 | Payload 函数 | 主要输入 | 排除 |
|------|-------------|---------|------|
| Analyst Team | 四位 specialist payload | 分域 raw/derived facts | 彼此结论 |
| 看多/看空研究 | `research_payload()` | `analyst_team` + structure_vote + event_risk | external、timeframes、metrics |
| 辩论 | `debate_payload()` | bull/bear evidence + analyst top items + event_risk | 原始快讯/社媒 |
| 交易员 | `trader_decision_payload()` | debate + analyst summaries + candidate_signals | 全量 market |
| 点位提议 | `level_proposer_payload()` | `technical_level_reactions`（技术分析产出）+ structure_context + debate；setup 绑定 `reaction_evidence_id`，短 deduction | external 新闻 |
| 风控 / 经理 | `risk_payload` / `manager_payload` | proposal + reviews | 市场与分析师 |

设 `LLM_PAYLOAD_FUNNEL=false` 可回退旧版（研究/交易员含 `market_payload`）。Analyst Team 的 `stage_io` 记录四位 specialist 实际输入（`analyst_team_input_payload`），而非泛化 `market_payload`。

### 3.8 报告可信度层（2026-07）

在叙事层与归档之间增加确定性门禁，详见 **[report-trust.md](./report-trust.md)**。与 LLM 链直接相关的变更：

| 主题 | 行为 |
|------|------|
| **observation_mode** | `data_as_of.executable=false` 时跳过 LLM Levels/Trader/Risk |
| **证据溯源** | Research parser 白名单校验 `evidence_id`；`AgentEvidence.provenance_meta` |
| **fact_registry** | 叙事前构建；`llm/context.py` 传 `price_fact_id` + 紧凑 fact 索引 |
| **叙事校验** | wait/观察模式下拒绝可执行措辞；失败字段在 `validate_llm_payload` 清空 |
| **可靠度 UI** | 展示 `overall_reliability`，LLM confidence 仅作审计 |

Research payload 额外包含 `allowed_evidence_ids`（Analyst 已有 ID 列表）。

---

## 4. 流式 I/O 与 UI

**多页面**（`ensure_report()` session 缓存，切换不重跑）：

| 页面 | 展示内容 |
|------|----------|
| `views/1_机构级分析报告.py` | 机构报告 + 生成时实时决策链 Tab |
| `views/2_短线策略.py` | 短线策略图 |
| `views/3_LLM决策链.py` | 三 Tab：智能体决策 / LLM 文案 / 生成与 LLM I/O |

**机构页 / 任意等待页生成时**：后台线程通过 `ModuleSyncProgressReporter` 同步步骤与 LLM 状态；等待页使用 **轻量进度面板**（`render_live_llm_status_lightweight`，约 **1s** 轮询，仅步骤 + 字符计数，避免流式 `text_area` 导致白屏）。完整 Prompt / JSON 在生成完成后的 **「LLM 决策链」→「生成与 I/O 审计」** 查看。

**生成完成后「LLM决策链」页**（`decision_page.render_live_generation_panel()` 可展示完整 Tab，含 **LLM 实时推理** 历史）：

- 顶栏 **来源条**（各阶段 规则/LLM）
- Tab **智能体决策** — `agent_trace` + 来源徽章
- Tab **生成与 LLM I/O** — 上方 `generation_steps`，下方 `meta.llm_io`（Analyst Team 规则 I/O + LLM Prompt/整理摘要）

实现路径：`core/progress.py`（`stage_io` / `llm_begin` / `run_llm_stream` / `llm_end`）→ `agents/llm/base.py`（`stream_llm_json`）→ `llm/client.chat_stream()`。

---

## 5. 各阶段状态

| 阶段 | 规则 | LLM | 当前行为 |
|------|------|-----|----------|
| ICT 结构事实 | `ict_pa.py` | 未接入 | 仅规则事实层 |
| **Analyst Team** | `analysts/*.py` | `llm/stages/analysts/` | `rule` / `llm` / `hybrid` 双轨 |
| 看多/看空研究 | `bullish.py` / `bearish.py` | `llm/stages/bullish.py` / `bearish.py` | 可由 `LLM_STAGE_RESEARCH` 或分方向开关启用 |
| 辩论 | `debate.py` | `llm/stages/debate.py` | 可由 `LLM_STAGE_DEBATE` 启用 |
| 点位提议 | `compute_trading_signals(ctx)` | `llm/stages/levels.py` | `LLM_STAGE_LEVELS` 启用后只提议点位，仍需 validator |
| 交易员 | `trader.py` | `llm/stages/trader.py` | `LLM_STAGE_TRADER` 启用后由 LLM 选择方向与候选信号索引，失败或置信不足回退规则 |
| 风控 | `risk.py` | `llm/stages/risk.py` | `LLM_STAGE_RISK` 启用后三档风险复核，索引与仓位由 schema 过滤 |
| 经理 | `manager.py` | `llm/stages/manager.py` | `LLM_STAGE_MANAGER` 启用后做最终执行/减仓/观望授权 |
| 报告文案 | 规则结论 | `llm/analyst.py` | `LLM_ENABLED` 控制最终叙事层 |

### 5.1 五块机构化文案双轨

`report.narrative_sections` 固定包含市场总览、流动性、4H、1H、15m。报告引擎先从确定性结构事实生成规则版；仅当 `AGENT_MODE=llm|hybrid` 且报告文案开关启用时，末端 LLM 才可逐块覆盖。

LLM 输入使用 `narrative_facts`：公共行情、质量警告、流动性、周期结构和带稳定 ID 的允许价位，不包含原始 OHLCV。输出按块执行 schema、6 行上限、价位白名单、禁用“胜率”措辞及方向一致性校验；Hybrid 还要求块级置信度达到 `LLM_OVERRIDE_THRESHOLD`。任一块失败只回退该块，结果与原因写入 `meta.stage_sources.narrative_sections`。

---

## 6. 审计字段

### `agent_trace.stage_meta`

```json
{
  "bullish": {
    "source": "rule",
    "fallback_reason": "confidence 0.50 < 0.65",
    "llm": {"stage": "bullish", "model": "deepseek-ai/DeepSeek-V4-Pro", "latency_ms": 2400}
  }
}
```

### `meta.llm_io`（智能体 I/O）

含 **规则阶段**（`kind: "rule"`，如 Analyst Team）与 **LLM 阶段**（`kind: "llm"`）：

```json
[
  {
    "stage": "analyst_team",
    "label": "Analyst Team",
    "model": "规则引擎",
    "kind": "rule",
    "messages": [{"role": "user", "content": "{...analyst_team_input_payload (per specialist)...}"}],
    "output": "{...technical/fundamentals/news/sentiment...}",
    "latency_ms": 12
  },
  {
    "stage": "bullish",
    "label": "看多研究",
    "model": "deepseek-ai/DeepSeek-V4-Pro",
    "kind": "llm",
    "messages": [{"role": "system", "content": "..."}],
    "output": "{...}",
    "latency_ms": 2400
  }
]
```

规则阶段由 `ProgressReporter.stage_io()` 写入；LLM 阶段由 `llm_begin` / `llm_end` 写入。

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [README.md](../README.md) | 文档中心索引 |
| [architecture.md](./architecture.md) | TradingAgents 对照与分层图 |
| [analyst-context.md](./analyst-context.md) | Analyst 输入密度与 payload |
| [roadmap.md](../planning/roadmap.md) | 后续执行接口、MT5 接入和 ICT 标准化计划 |
| [setup.md](../operations/setup.md) | 环境搭建与扩展指南 |

---

## 免责声明

LLM 输出仅供研究，不构成投资建议。规则硬约束层始终保留最终安全边界。

---

## LLM 点位提议

> UI 中文名：**LLM 点位提案**。英文实现名仍保留为 `LLM Level Proposer` / `llm_levels`，表示“由大模型提出候选交易点位”，不是最终交易员决策。

研究层仍是 Analyst Team -> Bullish/Bearish Research -> Debate。LLM 点位阶段插入 Debate 与 Trader 之间；完整架构说明见 [architecture.md §8.1](./architecture.md#81-llm-点位层)。

当前执行链：

```text
Analyst Team -> Bullish/Bearish Research -> Debate
  -> compute_trading_signals(ctx)
  -> LLM Level Proposer (LLM_STAGE_LEVELS)
  -> Level Validator
  -> Trader -> Risk -> Manager -> Report
```

**分工**：`level_reactions`（到价预期反应）由**技术分析师**产出；点位阶段只做**短绑定**并给出 A/B/C 入场几何。

| 阶段 | 字段 | 含义 |
|------|------|------|
| 技术分析 | `level_reactions[]` | 关键 POC/VA/S/R + `expected_reaction` + 短 rationale |
| 点位提案 | `reaction_evidence_id` | 引用技术分析 `level_reactions[].id` |
| 点位提案 | `anchor_level` / `expected_reaction` | 从被引用反应复制 |
| 点位提案 | `deduction` | **一句**绑定理由（禁止重写技术分析） |

确定性 validator 检查止损/目标几何，再转换为 `TradingSignal`。决策链页展开「点位绑定」。

审计字段：

- `report["llm_levels"]`: raw structured LLM proposals（含推演字段）。
- `report["validated_plans"]`: validator accept/reject audit.
- `report["agent_trace"]["llm_levels"]` and `report["agent_trace"]["validated_plans"]`.
- `report["meta"]["stage_sources"]["llm_levels"]`.

Trader / Risk / Manager 三段 LLM 已接入 `agents/factory.py` 双轨调度；后续实盘执行与 MT5 接入计划见 [roadmap.md](../planning/roadmap.md)。
