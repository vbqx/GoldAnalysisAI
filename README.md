# GoldAnalysisAI — XAUUSD PA+ICT 分析报告



基于 Price Action + ICT + SMC 方法论，自动生成 XAUUSD 机构级分析仪表盘。内部流水线参考 [TradingAgents](https://github.com/TauricResearch/TradingAgents)：**Analyst Team**（技术/基本面/新闻/情绪）→ 多空研究 → 辩论 → 交易 → 风控 → 经理；支持规则引擎与 LLM 双轨。



## 快速开始



```bash

git clone https://github.com/vbqx/GoldAnalysisAI.git

cd GoldAnalysisAI

python -m venv .venv

.venv\Scripts\activate          # Windows

pip install -r requirements.txt

copy .env.example .env

streamlit run app.py

```



浏览器打开 `http://localhost:8501`。



## 多页面导航



| 页面 | 文件 | 说明 |

|------|------|------|

| 机构级分析报告 | `views/1_机构级分析报告.py` | 机构完整报告，主图日线 |

| 短线策略 | `views/2_短线策略.py` | 短线策略图，**切换不重新生成** |

| LLM决策链 | `views/3_LLM决策链.py` | 智能体决策、LLM 文案、生成与智能体 I/O |



报告在 session 中缓存；后台线程生成，等待时可看实时步骤与 LLM I/O。仅点 **「刷新报告」** 才重跑（约 2–3 分钟）。



## 文档



| 文档 | 说明 |

|------|------|

| [docs/development.md](docs/development.md) | 开发文档 |

| [docs/architecture.md](docs/architecture.md) | 架构设计 |

| [docs/llm-agents.md](docs/llm-agents.md) | LLM 多智能体 |

| [docs/financial-review.md](docs/financial-review.md) | 金融逻辑评审 |

| [docs/reverse-engineering.md](docs/reverse-engineering.md) | 报告结构反推 |



## 项目结构



```

GoldAnalysisAI/

├── app.py                      # 导航入口（st.navigation）

├── views/                      # 三页视图（由 app.py 导航注册）

│   ├── 1_机构级分析报告.py

│   ├── 2_短线策略.py

│   └── 3_LLM决策链.py

├── tests/                      # 测试体系（用例 / 单元 / 集成 / 回归 / 工具）
│   ├── run.py                  # 统一入口
│   ├── cases/catalog.yaml      # 用例目录
│   ├── unit/
│   ├── integration/
│   └── regression/
└── src/
    ├── core/orchestrator.py
    ├── agents/
    │   ├── analysts/           # Analyst Team（TradingAgents 对齐）
    │   └── factory.py
    ├── llm/
    └── viz/
        ├── streamlit_common.py  # 共享 bootstrap + session 缓存
        ├── decision_page.py
        └── pipeline_progress.py
```



## 能力一览



| 模块 | 状态 |

|------|------|

| Analyst Team | ✅ 技术/基本面/新闻/情绪（规则版） |

| 多页面 UI | ✅ 机构 / 短线 / LLM 决策 |

| Session 缓存 | ✅ 切换页面秒开 |

| 外部数据（DXY/新闻/日历/TV 社媒） | ✅ 拉取 + UI 展示 |

| LLM 双轨 + 来源标识 | ✅ |

| 智能体 I/O（Analyst Team + LLM） | ✅ LLM决策链页 |

| LLM 传输重试 + hybrid 规则兜底 | ✅ |

| 主图日线 (1d) | ✅ |



## LLM 配置（硅基流动示例）



```env

LLM_BASE_URL=https://api.siliconflow.cn/v1

LLM_MODEL=deepseek-ai/DeepSeek-V4-Pro

LLM_MODEL_FAST=deepseek-ai/DeepSeek-V4-Pro

LLM_MODEL_STRONG=deepseek-ai/DeepSeek-V4-Pro

AGENT_MODE=hybrid

LLM_STAGE_RESEARCH=true

LLM_STAGE_DEBATE=true

LLM_STAGE_ANALYSTS=true

LLM_ENABLED=true

```



## 测试

```bash
pip install -r requirements-dev.txt

# 快速：单元 + 回归（无网络，推荐 CI / 日常）
python tests/run.py

# 外部 API 冒烟（DXY / 新闻 / TE 日历 / TV 社媒，需网络）
python tests/run.py --external

# 金融 Review：FIN-* 单测
python tests/run.py --financial

# 完整：含流水线集成（需 .env + TradingView，约 2–3 分钟）
python tests/run.py --full
```

用例目录与维护说明见 [tests/README.md](tests/README.md)、[tests/cases/catalog.yaml](tests/cases/catalog.yaml)。



## 免责声明



本项目仅供学习研究，不构成投资建议。

