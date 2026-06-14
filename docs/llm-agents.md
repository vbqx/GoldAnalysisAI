# LLM 多智能体架构



> **目标**：数据层保持确定性（TradingView + 指标 + 规则 ICT 事实），  

> 多空研究 → 辩论 → 交易 → 风控 → 经理 各阶段可接入大模型。  

> **约束**：`run_analysis()` 仍返回 `(report, data, analyses)`；报告 JSON schema 不变。



---



## 1. 设计原则



| 原则 | 说明 |

|------|------|

| **双轨实现** | 每阶段保留规则版 + LLM 版，经 `agents/factory.py` 统一调度 |

| **结构化输出** | LLM 返回 JSON（`response_format: json_object`），校验后进入流水线 |

| **规则兜底** | LLM 失败或 hybrid 置信度不足 → 自动回退规则版 |

| **流式可观测** | 机构页展示生成进度；LLM 完整 I/O 在「LLM决策链」页 |

| **可审计** | `stage_meta` 标 `rule/llm/hybrid`；`meta.llm_io` 存完整 I/O |



---



## 2. 流水线总览



```

TradingView → enrich → ict_pa.analyze (规则事实)

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



### 3.2 模型路由



| 变量 | 用途 | 调用点 |

|------|------|--------|

| `LLM_MODEL_FAST` | 研究阶段（看多/看空） | `llm/router.get_fast_client()` |

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

LLM_STAGE_RESEARCH=true

LLM_STAGE_DEBATE=true

LLM_STAGE_ICT=false

LLM_STAGE_TRADER=false

LLM_STAGE_RISK=false

LLM_STAGE_MANAGER=false



# 报告结论文案层（独立于智能体链）

LLM_ENABLED=true

LLM_ENHANCE_CONCLUSION=true

```



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

- Tab **生成与 LLM I/O** — 上方 `generation_steps`，下方 `meta.llm_io`（Prompt + 整理摘要）



实现路径：`core/progress.py`（`llm_begin` / `run_llm_stream` / `llm_end`）→ `agents/llm/base.py` → `llm/client.chat_stream()`。



---



## 5. 各阶段状态



| 阶段 | 规则 | LLM | 状态 |

|------|------|-----|------|

| ICT 结构事实 | `ict_pa.py` | P3 解读 | 事实 ✅ / LLM 🔲 |

| 看多/看空研究 | `bullish.py` / `bearish.py` | `llm/stages/*` | ✅ P0 |

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



### `meta.llm_io`



```json

[

  {

    "stage": "bullish",

    "label": "看多研究",

    "model": "deepseek-ai/DeepSeek-V4-Pro",

    "messages": [{"role": "system", "content": "..."}],

    "output": "{...}",

    "latency_ms": 2400

  }

]

```



---



## 7. 路线图



| 阶段 | 内容 | 状态 |

|------|------|------|

| **P0** | factory + LLM 研究 + 辩论 + 流式 I/O | ✅ |

| **P4** | 报告文案层 | ✅ |

| **P1** | LLM 交易员 | 🔲 |

| **P2** | LLM 风控 + 经理 | 🔲 |

| **P3** | ICT Interpreter | 🔲 |



---



## 免责声明



LLM 输出仅供研究，不构成投资建议。规则硬约束层始终保留最终安全边界。

