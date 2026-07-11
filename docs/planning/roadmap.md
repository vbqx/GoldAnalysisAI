# GoldAnalysisAI 路线图

本文只维护“计划、优先级、验收标准”。稳定架构事实放在 [architecture.md](../architecture/architecture.md)，LLM 阶段细节放在 [llm-agents.md](../architecture/llm-agents.md)，金融风险发现与验收记录放在 [financial-review.md](../archive/domain/financial-review.md)。

---

## 优先级规则

`P0/P1/P2/P3` 是全局优先级：

| 优先级 | 含义 |
|--------|------|
| P0 | 会导致结论方向、几何关系或风控明显错误的阻断项 |
| P1 | 影响可信度、透明度或用户误读风险的高优先级项 |
| P2 | 数据质量、边界行为、统计口径或工程体验优化 |
| P3 | 长周期增强、研究型能力或非阻断体验优化 |

专项编号使用 `P*-主题-*`。例如 `P1-LQ-*` 表示 P1 可信度优先级下的 Liquidity Quality 专项，不代表新增一套与 P0/P1/P2/P3 并列的阶段体系。

---

## 当前状态

| 优先级 | 任务 | 状态 | 参考 |
|--------|------|------|------|
| P0 | Analyst Team 规则版 + 接入流水线 | 已完成 | `src/agents/analysts/` |
| P0 | LLM 研究 + 辩论 + 流式 I/O | 已完成 | [llm-agents.md](../architecture/llm-agents.md) |
| P1 | 信号生成去重，Trader 与 report 共用候选信号 | 已完成 | `src/analysis/report_engine.py` |
| P1 | Analyst Team LLM 双轨，每个分析师独立 prompt | 已完成 | `src/agents/llm/stages/analysts/` |
| P1 | 真实 News / DXY / 社媒 API | 已完成 | `src/data/sources/` |
| P1 | Bull/Bear 与 Analyst Team 并行 | 已完成 | `src/agents/` |
| P1 | LLM 点位提议 + 规则 validator | 已完成 | [architecture.md §8.1](../architecture/architecture.md#81-llm-点位层) |
| P2 | LLM 交易员 / 风控 / 经理 | 已完成基础接入 | `src/agents/llm/stages/` |
| P3 | ICT Interpreter 完整标准化 | 计划中 | `src/analysis/ict_pa.py` |

---

## 交易假设系统

目标：把报告从“直接给交易计划”升级为“候选区 -> 触发条件 -> 执行计划 -> 失效”的交易假设系统，降低规则模板造成的误导。

### Phase A：交易计划去误导化

状态：已落地基础合同。

| 任务 | 说明 | 验收 |
|------|------|------|
| A-1 信号状态 | `TradingSignal.status`: `candidate` / `watch` / `active` / `invalid` | UI 不再把所有候选区显示成可执行计划 |
| A-2 触发确认 | `trigger_confirmed` 与 `trigger_note` | 未扫低收回、未反抽失败的信号必须显示等待触发 |
| A-3 质量评分 | `score_total` / `score_grade` / `score_reasons` | 每条计划展示结构、位置、R:R、触发缺口 |
| A-4 几何过滤 | SELL 区低于现价、BUY 未触发 sweep 时降级 | 主交易计划不把无触发区间当作 active |

### Phase B：多周期职责重构

| 周期 | 职责 |
|------|------|
| 4H / 1H | 市场背景：趋势、震荡、过热 |
| 15M | 交易区：FVG / OB / liquidity zone |
| 5M | 触发：反抽失败、扫流动性收回、低级别 CHoCH |

目标输出应表达为：`背景方向 + 候选区 + 等待触发条件`，而不是单一买卖建议。

### Phase C：宏观与事件门控

- 高影响数据发布前后：禁止 `active` 信号，最多保留 `candidate`。
- DXY / US10Y 与方向冲突时：降低 `score_total`。
- 外部数据缺失或 fallback：降低 `data_quality`，并在报告中降级置信。

### Phase D：回测闭环

实现轻量回放：

1. 历史 K 线生成 setup。
2. 判断是否触发。
3. 统计 TP1 / SL 谁先到。
4. 输出样本数、TP1 命中率、平均 R、最大不利波动。

没有样本前，UI 不展示“胜率”或暗示统计概率。

---

## 流动性质量专项

目标：把“流动性”从静态价位提示升级为可解释、可降级、可回放验证的交易假设输入。LLM 可以使用这些输入给点位，但系统必须说明点位依据和确认条件。

| 阶段 | 内容 | 验收标准 |
|------|------|----------|
| P1-LQ-1 | 记录最近收盘、最近高低点，并要求 sweep long 同时满足扫穿、收回、低级别 bullish BOS/CHoCH | 未收回或无结构转强时只能是 `candidate` |
| P1-LQ-2 | 用 ATR 标准化 equal highs/lows 容差、stop-hunt 偏移和 sweep buffer | 报告中的流动性区不再依赖固定 2/5 点偏移 |
| P1-LQ-3 | 输出 Liquidity Quality Score：扫穿深度、收回幅度、结构确认、与候选区距离 | 每条 sweep 信号在 `score_reasons` 中显示可审计原因 |
| P1-LQ-4 | 区分 breakout continuation 与 failed sweep/reclaim | 跌破后未收回时不允许表达为“扫流动性做多” |
| P2-LQ-5 | 历史回放统计 TP1/SL 先触发、样本数和平均 R | 没有样本前 UI 不展示“胜率”类措辞 |

当前实施批次覆盖 P1-LQ-1 至 P1-LQ-3；P1-LQ-4 与 P2-LQ-5 放入后续批次。

---

## 运行配置与 UI

| 阶段 | 内容 | 状态 |
|------|------|------|
| RC-1 | Streamlit 会话层门禁：首屏显示配置面板，点击后才后台生成 | 已完成 |
| RC-2 | 将 `RunConfig` 显式传入 `run_analysis()` / `run_trade_agent_pipeline()` / factory，移除模块全局同步 | 计划中 |
| RC-3 | UI 支持完整 stage matrix，并支持多用户隔离 | 计划中 |

---

## GUI 信息架构优化

目标：继续把界面维持在“先给交易判断，再给证据链审计”的结构。GUI-1 至 GUI-5 已完成首轮落地；历史验收快照已归档到 [gui-acceptance-2026-07-08.md](../archive/gui-acceptance-2026-07-08.md)。

后续只保留增量优化：

| 阶段 | 内容 | 状态 |
|------|------|------|
| GUI-6 | 将关键视觉验收沉淀为更稳定的截图/DOM 冒烟流程 | 计划中 |
| GUI-7 | 补齐移动端核心路径的自动化检查 | 计划中 |
| GUI-8 | 将手动验收项同步到 `tests/cases/catalog.yaml` | 计划中 |
| GUI-9 | 市场总览、流动性、4H、1H、15m 使用同契约机构化短文案；LLM 按块校验回退 | 已完成 |

验收标准保持不变：首屏能判断方向、计划状态和主失效条件；异常状态有清晰视觉层级；高级 LLM 调试不干扰默认生成路径。

---

## LLM 交易执行链

`LLM_STAGE_TRADER`、`LLM_STAGE_RISK`、`LLM_STAGE_MANAGER` 已完成基础接入。三段均通过 `agents/factory.py` 保留规则 baseline；`hybrid` 模式下只有 LLM 输出通过结构化 schema 且置信度达到 `LLM_OVERRIDE_THRESHOLD` 才覆盖规则结果，否则回退规则层。

后续增强要求：

1. LLM 只能复核风险，不直接绕过 `level_validator.py` 与信号几何约束。
2. 风控输出必须保持三档 profile：`aggressive` / `neutral` / `conservative`。
3. 交易员、风控、经理结论必须写入 `agent_trace.stage_meta` 和 `meta.llm_io`，供 UI 决策链审计。
4. 与规则风控冲突时，默认采用更保守结论；后续可加入显式 conflict resolver。
5. 实盘执行仍未启用；MT5 账号连接接口已接入，下一步是模拟下单、订单回执审计和风控熔断。
