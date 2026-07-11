# GoldAnalysisAI 测试用例设计

> 版本：v1.1 · 2026-06-20
> 范围：UI 布局 → 指标显示 → 整体功能 → 性能
> 用例明细见 [catalog.yaml](./catalog.yaml)

---

## 1. 测试分层

```
┌─────────────────────────────────────────────────────────┐
│  PERF  性能（耗时、缓存、并发）                           │
├─────────────────────────────────────────────────────────┤
│  FN    功能（流水线、导航、LLM、信号、刷新）                 │
├─────────────────────────────────────────────────────────┤
│  IND   指标（顶栏、侧边栏校验、图表、报告 JSON 一致性）       │
├─────────────────────────────────────────────────────────┤
│  UIL   UI 布局（导航、分区、Tab、响应式、样式）              │
└─────────────────────────────────────────────────────────┘
```

| 层级 | 前缀 | 自动化倾向 | 典型工具 |
|------|------|------------|----------|
| UI 布局 | `UIL-*` | 手工 + 未来 E2E | Browser / Playwright |
| 指标显示 | `IND-*` | 单元 + 集成 | pytest + report JSON |
| 整体功能 | `FN-*` | 集成 + 手工 | pytest + Streamlit |
| 性能 | `PERF-*` | 集成 + 计时脚本 | pytest marker `slow` |

---

## 2. UI 布局（UIL）

### 2.1 全局框架

| ID | 场景 | 验收要点 |
|----|------|----------|
| UIL-01 | 应用入口 `app.py` | `layout=wide`；三页导航可见；默认页为机构报告 |
| UIL-02 | 侧边栏 | GoldAnalysisAI 标题、数据源、LLM 模型、刷新按钮、指标校验 expander |
| UIL-03 | page-hero | 三页均有 hero 区；机构页含标题+时间+方法论 |
| UIL-04 | CSS 主题 | 卡片/网格/hbox 样式加载；无裸 HTML 错位 |

### 2.2 机构级分析报告页

| ID | 区域 | 验收要点 |
|----|------|----------|
| UIL-10 | 顶栏指标卡 | 6 格 header-grid：现价/日涨跌/日高低/情绪/美元/结论 |
| UIL-11 | 来源 Banner | agent-source-bar 各阶段 chip 可见 |
| UIL-12 | 总览四格 | 市场总览 / 路径 / 流动性 / 今日要点 |
| UIL-13 | 三列主区 | 左：4H/1H/15m 条带图+面板；中：**5 分钟主图**（K 线+量+SMC 结构区）；右：交易计划 |
| UIL-14 | 底部四列 | Fibonacci 表 / 投影图 / 风控失效 / 最终结论 |
| UIL-15 | 页脚 | footer-bar + 品牌行 |

### 2.3 短线策略页

| ID | 区域 | 验收要点 |
|----|------|----------|
| UIL-20 | 标题区 | 策略标题+副标题+生成时间（报告就绪后显示） |
| UIL-21 | 三列布局 | 左：15m+5m 图；中：关键价位 ladder；右：策略文字 |
| UIL-22 | 加载顺序 | 先 waiting hero，完成后才显示策略标题（无双标题） |

### 2.4 LLM 决策链页

| ID | 区域 | 验收要点 |
|----|------|----------|
| UIL-30 | Tab 四栏 | 智能体决策 / LLM 文案 / 生成步骤 / LLM 输入输出 |
| UIL-31 | 决策面板 | 经理/辩论/交易员三 metric + 风控表格 |
| UIL-32 | I/O 展开 | 每条 LLM 调用可展开 Prompt/Response |

### 2.5 生成等待 UI

| ID | 场景 | 验收要点 |
|----|------|----------|
| UIL-40 | 机构页 waiting | hero + live panel 四 Tab |
| UIL-41 | 子页 waiting | 同 UIL-40；无残留「报告尚未生成」info |
| UIL-42 | 进度刷新 | fragment 约 1s 刷新步骤与 LLM 流式输出 |

---

## 3. 指标显示（IND）

### 3.1 顶栏 metrics（report JSON）

| ID | 字段 | 验收要点 |
|----|------|----------|
| IND-01 | current_price | 与 5m 最新 Close 一致（±0.01） |
| IND-02 | daily_change / pct | 与 daily_high/low 逻辑自洽 |
| IND-03 | daily_high / daily_low | high ≥ price ≥ low（正常行情） |
| IND-04 | market_sentiment | 非空；与 sentiment 投票方向不矛盾 |
| IND-05 | 结论区 LLM badge | LLM 启用时显示 llm 来源标识 |

### 3.2 侧边栏「指标校验」

| ID | 场景 | 验收要点 |
|----|------|----------|
| IND-10 | 5m/15m 表格 | 列：周期/K线数/现价/EMA20/50/610/VWAP/**RSI14/MACD/MACD_SIG/ADX14/ATR14**/差值 |
| IND-11 | 现价一致 | 5m 与 15m 表格现价相同 |
| IND-12 | EMA610 说明 | bars<610 时 notes 含历史不足提示 |
| IND-13 | VWAP 偏差 | 偏离>5% 时有 notes 警告 |

### 3.3 多周期结构面板

| ID | 场景 | 验收要点 |
|----|------|----------|
| IND-20 | 4H/1H/15m tf-panel | 趋势中文、EMA 关系、OB/FVG 区间 |
| IND-21 | timeframes JSON | 与 analyses ICT 结果 trend 一致 |

### 3.4 图表与衍生指标

| ID | 场景 | 验收要点 |
|----|------|----------|
| IND-30 | 5m 主图 iframe | 高度约 420；含水印；含 OB/FVG/需求区/BOS/CHoCH overlay；**不**绘制 EMA/MACD/RSI 副图或路径虚线 |
| IND-34 | 路径预测对齐 | 显式 `show_projections=True` 时虚线与 K 线共用默认价格轴；方向与 `trend_projections()` 一致（`test_chart_projections.py`）；主图默认无虚线 |
| IND-35 | 一致性检查 | `coherence_check.py` 规则模式无 issue，或 issues 已登记为已知 Finding |
| IND-31 | 情绪甜甜圈 | Plotly 渲染；三分类占比合计 100% |
| IND-32 | Fibonacci 表 | 4 行比例/价位/含义 |
| IND-33 | 交易信号 | entry_low/high、stop_loss、take_profits 齐全 |

---

## 4. 整体功能（FN）

### 4.1 数据与流水线

| ID | 场景 | 验收要点 |
|----|------|----------|
| FN-01 | 多周期拉取 | 5m/15m/1h/4h/1d 均有数据 |
| FN-02 | ICT 分析 | 每周期 trend/BOS/OB/FVG |
| FN-03 | 智能体链 | 研究→辩论→交易→风控→经理 12 步 done |
| FN-04 | 报告 Schema | meta/metrics/signals/agent_trace 完整 |

### 4.2 导航与缓存

| ID | 场景 | 验收要点 |
|----|------|----------|
| FN-10 | Session 缓存 | 三页切换不重跑；updated_at 不变 |
| FN-11 | 刷新报告 | 点击后 counter+1；重新拉数据；时间戳更新 |
| FN-12 | 冷启动子页 | 直接开短线/LLM 页可触发 waiting UI |

### 4.3 LLM 双轨

| ID | 场景 | 验收要点 |
|----|------|----------|
| FN-20 | hybrid 回退 | LLM 失败时 stage_sources 标注 rule + fallback_reason |
| FN-21 | LLM I/O 记录 | meta.llm_io 与阶段调用数一致 |
| FN-22 | 报告文案层 | llm_analysis.enabled；无 error |

### 4.4 模式与配置

| ID | 场景 | 验收要点 |
|----|------|----------|
| FN-30 | AGENT_MODE=rule | 全部阶段 source=rule |
| FN-31 | LLM_ENABLED=false | 无 llm_io；规则结论仍生成 |
| FN-32 | 无 API Key | 流水线不崩溃；友好降级 |

---

## 5. 性能（PERF）

| ID | 场景 | 阈值（参考） | 测量方式 |
|----|------|--------------|----------|
| PERF-01 | 首次完整流水线 | rule ≤ 240s；hybrid+LLM ≤ 320s（并行后目标 180–220s） | integration test 分层计时 |
| PERF-02 | 纯规则流水线 | ≤ 30s（实测约 8–10s 含 TV 拉取） | `apply_run_config(rule)` 或 `coherence_check.py` |
| PERF-03 | 数据拉取阶段 | ≤ 20s | generation_steps 耗时 |
| PERF-04 | 页面切换（已缓存） | ≤ 3s 可交互 | 手工 / E2E |
| PERF-05 | 图表 HTML 生成 | ≤ 2s / 图 | unit 计时 |
| PERF-06 | 刷新期间点击控件 | 不重启流水线 | 手工：waiting 期间点 sidebar |

---

## 6. 自动化路线图

| 阶段 | 覆盖 | 动作 |
|------|------|------|
| **当前** | UT/RG/IT | `python tests/run.py` |
| **Phase 2** | IND-01~13 | `tests/unit/test_indicators.py` + report fixture |
| **Phase 3** | FN-01~04 | 扩展 `tests/integration/` |
| **Phase 4** | PERF-01~03 | `@pytest.mark.slow` + 阈值断言 |
| **Phase 5** | UIL / FN-10~12 | Streamlit AppTest 或 Playwright |

---

## 7. 执行命令

```bash
# 日常
python tests/run.py --fast

# 发版前
python tests/run.py --full

# 按层（未来）
pytest tests/unit/test_indicators.py -q          # IND
pytest tests/integration -m integration -q       # FN + PERF
```

---

## 8. 金融 Review 用例（FIN）

> 详设：[financial-review-cases.md](./financial-review-cases.md) · 来源 [financial-review.md](../../docs/archive/domain/financial-review.md)

| 前缀 | 范围 | 说明 |
|------|------|------|
| `FIN-*` | 信号/风控/数据语义 | F-001～F-011 单元与集成 |
| `FIN-UI-*` | 合规披露 | 胜率标注、占位数据、免责声明 |

**Sprint 1 优先（P0/P1）：** FIN-01 风控 approved · FIN-02 win_rate · FIN-06 结论硬编码 · FIN-03 R:R · FIN-UI-01/05

**已有覆盖：** F-005 现价一致 → `IND-01`；signals schema → `IT-03`；EMA610 notes → `IND-12`
