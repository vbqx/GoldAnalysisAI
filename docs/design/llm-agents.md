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
              交易员 → 风控 → 经理  (当前规则)
                              ▼
              report_engine.build_report
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

---

## 4. 流式 I/O 与 UI

**多页面**（`ensure_report()` session 缓存，切换不重跑）：

| 页面 | 展示内容 |
|------|----------|
| `views/1_机构级分析报告.py` | 机构报告 + 生成时实时决策链 Tab |
| `views/2_短线策略.py` | 短线策略图 |
| `views/3_LLM决策链.py` | 三 Tab：智能体决策 / LLM 文案 / 生成与 LLM I/O |

**机构页生成时**：进度条（`viz/pipeline_progress.py`）；LLM 流式详情在「LLM决策链」页查看。

**LLM决策链页**：

- 顶栏 **来源条**（各阶段 规则/LLM）
- Tab **智能体决策** — `agent_trace` + 来源徽章
- Tab **生成与 LLM I/O** — 上方 `generation_steps`，下方 `meta.llm_io`（Analyst Team 规则 I/O + LLM Prompt/整理摘要）

实现路径：`core/progress.py`（`stage_io` / `llm_begin` / `run_llm_stream` / `llm_end`）→ `agents/llm/base.py`（`stream_llm_json`）→ `llm/client.chat_stream()`。

---

## 5. 各阶段状态

| 阶段 | 规则 | LLM | 状态 |
|------|------|-----|------|
| ICT 结构事实 | `ict_pa.py` | P3 解读 | 事实 ✅ / LLM 🔲 |
| **Analyst Team** | `analysts/*.py` + `llm/stages/analysts/` | 每分析师独立 Prompt | ✅ rule / llm / hybrid |
| 看多/看空研究 | `bullish.py` / `bearish.py` | `llm/stages/*` | ✅ P0（含 analyst_team payload） |
| 辩论 | `debate.py` | `llm/stages/debate.py` | ✅ P0 |
| 交易员 | `trader.py` | P1 | 🔲 |
| 风控 | `risk.py` | P2 | 🔲 |
| 经理 | `manager.py` | P2 | 🔲 |
| 报告文案 | — | `llm/analyst.py` | ✅ |

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

## 7. 路线图

| 阶段 | 内容 | 状态 |
|------|------|------|
| **P0** | Analyst Team 规则版 + 流水线接入 | ✅ |
| **P0** | LLM 传输重试 + hybrid 规则兜底 | ✅ |
| **P4** | 报告文案层 | ✅ |
| **P1** | Analyst Team LLM 双轨（`LLM_STAGE_ANALYSTS`） | ✅ |
| **P1** | 真实 News/DXY/社媒 API | ✅ |
| **P1** | 流水线并行（bull/bear、Analyst×4） | 🔲 |
| **P1** | LLM 交易员 | 🔲 |
| **P2** | LLM 风控 + 经理 | 🔲 |
| **P3** | ICT Interpreter | 🔲 |

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [README.md](../README.md) | 文档中心索引 |
| [architecture.md](./architecture.md) | TradingAgents 对照与分层图 |
| [analyst-context.md](./analyst-context.md) | Analyst 输入密度与 payload |
| [setup.md](../getting-started/setup.md) | 环境搭建与扩展指南 |

---

## 免责声明

LLM 输出仅供研究，不构成投资建议。规则硬约束层始终保留最终安全边界。
