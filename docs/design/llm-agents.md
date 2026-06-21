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
 （含 analyst_team）      （含 analyst_team）        │
     │                        │                        │
     └────────────────────────┴────────────────────────┘
                              ▼
              交易员 → 风控 → 经理  (规则；trader 含 F-014 结构门控)
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
LLM_OVERRIDE_THRESHOLD=0.65

# 分阶段开关
LLM_STAGE_ANALYSTS=true
LLM_STAGE_RESEARCH=true
LLM_STAGE_DEBATE=true
LLM_STAGE_ICT=false
LLM_STAGE_LEVELS=true
LLM_STAGE_TRADER=false
LLM_STAGE_RISK=false
LLM_STAGE_MANAGER=false

# 可选：仅调试单个 Analyst LLM；留空或 all 表示四位都跑
LLM_ANALYST_ONLY=technical

# 报告结论文案层（独立于智能体链）
LLM_ENABLED=true
LLM_ENHANCE_CONCLUSION=true
```

`LLM_ANALYST_ONLY` 仅在 `LLM_STAGE_ANALYSTS=true` 且 `AGENT_MODE=llm|hybrid` 时生效；未选中的 Analyst 使用规则输出补齐，避免完整流水线等待四个 LLM 分析师全部完成。

### 3.4 传输重试与规则兜底

LLM 使用 OpenAI 兼容 **SSE 流式**；不支持流内续传，断流时**整次请求重打**。

| 组件 | 行为 |
|------|------|
| `llm/client.py` | `ChunkedEncodingError`、连接超时等 → `LLMClientError` |
| `agents/llm/base.py` `stream_llm_json()` | 最多 `_MAX_STAGE_RETRIES + 1`（3 次）尝试，退避 1s → 2s |
| `run_llm_stage()` | JSON 解析失败同样重试；传输与解析均失败 → 返回 `error` trace |
| `factory` hybrid | LLM 失败或置信度不足 → 采用规则版 `bullish`/`bearish`/`debate` |
| `llm/analyst.py` | 文案层经 `stream_llm_json()`；失败写入 `llm_analysis.error`，不中断 pipeline |

单元测试：`tests/unit/test_llm_transport.py`。

### 3.5 规则智能体 — 金融 Review 三处改动（2026-06-20）

| 模块 | Finding | 行为摘要 | 单测 |
|------|---------|----------|------|
| `debate.py` | F-013 | `combined = 研究分 + sentiment_pct/50`；证据接近时以结构情绪 tiebreaker | `test_debate_coherence.py` |
| `trader.py` | F-014 | `sentiment_score` 门控主方向；偏空优先 short（强多共识 strength≥0.6 例外） | `test_trader_sentiment.py` |
| `factory.py` | — | `run_research_team` 并行 LLM 看多/看空；`run_parallel` 并行 Analyst Team | `test_research_parallel.py` |

编排层 `orchestrator.py`：研究阶段按 `research_uses_parallel_llm()` 分支；报告组装后按 sentiment 重排信号并写入 `signal_role`。门禁：`tests/tools/coherence_check.py`（rule 模式 `issues: []`）。

---

## 4. 流式 I/O 与 UI

**多页面**（`ensure_report()` session 缓存，切换不重跑）：

| 页面 | 展示内容 |
|------|----------|
| `views/1_机构级分析报告.py` | 机构报告 + 生成时实时决策链 Tab |
| `views/2_短线策略.py` | 短线策略图 |
| `views/3_LLM决策链.py` | 三 Tab：智能体决策 / LLM 文案 / 生成与 LLM I/O |

**机构页 / 任意等待页生成时**：后台线程通过 `_ModuleSyncProgressReporter` 同步步骤与 LLM chunk；`decision_page.render_live_generation_panel()` 每 **400ms** 轮询刷新。

**生成中「生成与 LLM I/O」Tab**（实时）：

- 上方：**生成步骤**（`generation_steps` 快照）
- **LLM 实时推理** — 进行中的阶段（`latency_ms` 为空）展示 Prompt + 逐字增长的 JSON 输出
- 下方：**已完成 I/O** — 已结束阶段的完整记录

**生成完成后「LLM决策链」页**：

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
| 交易员 | `trader.py` | 未接入 | `LLM_STAGE_TRADER` 为预留开关，当前回退规则 |
| 风控 | `risk.py` | 未接入 | `LLM_STAGE_RISK` 为预留开关，当前回退规则 |
| 经理 | `manager.py` | 未接入 | `LLM_STAGE_MANAGER` 为预留开关，当前回退规则 |
| 报告文案 | 规则结论 | `llm/analyst.py` | `LLM_ENABLED` 控制最终叙事层 |

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
    "messages": [{"role": "user", "content": "{...market_payload...}"}],
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
| [roadmap.md](../planning/roadmap.md) | 后续 LLM 风控、经理和 ICT 标准化计划 |
| [setup.md](../getting-started/setup.md) | 环境搭建与扩展指南 |

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

LLM 点位阶段只提出候选 BUY/SELL 区。确定性 validator 检查止损/目标几何关系、风险收益方向和现有 setup 评分规则，再把通过建议转换为 `TradingSignal`，因此 Trader、Risk 和 UI 仍使用原有合同。

审计字段：

- `report["llm_levels"]`: raw structured LLM proposals.
- `report["validated_plans"]`: validator accept/reject audit.
- `report["agent_trace"]["llm_levels"]` and `report["agent_trace"]["validated_plans"]`.
- `report["meta"]["stage_sources"]["llm_levels"]`.

`LLM_STAGE_RISK` 的后续实现计划不在本文维护，见 [roadmap.md §LLM 风控阶段](../planning/roadmap.md#llm-风控阶段)。
