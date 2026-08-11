# 运行时质量评审（2026-08-11）

| 属性 | 内容 |
|---|---|
| 评审对象 | 归档 `20260811T143236Z`，生产提交 `49c7038` |
| 运行模式 | `agent_mode=llm`，Analyst / Research / Debate / Levels / Trader / Risk / Manager 全开 |
| 数据状态 | OANDA XAUUSD，行情年龄约 0.2 h，五周期齐全，无 fetch error |
| 归档状态 | schema v2，compatible，pipeline complete |
| 评审状态 | 已关闭；本地确定性门禁与实时集成回归通过 |

## 1. 结论

归档、数据时效与最终执行门禁正常：不变量通过，最终 `wait`，六个未触发候选均未授权执行。主要缺陷位于报告后置计算顺序、PA 支撑阻力语义、Research 证据契约、LLM 重试计量、payload 预算、长周期指标就绪条件和审计展示降噪。

本评审不把供应商延迟或市场无可执行信号本身判为软件缺陷；只登记可由冻结归档和源码复现的产品问题。

## 2. 运行证据

| 指标 | 实跑值 | 判定 |
|---|---:|---|
| 总耗时 | 970.504 s | 性能退化，主要由 Research 重试与大 payload 导致 |
| 供应商汇总 token | 183,564 | 当前只计每阶段最后一次 usage，失败重试实际消耗被低估 |
| Bearish Research | 378.7 s / 3 次 schema 失败 | 最终回退规则 |
| Technical 输入 | 82,399 chars | 超硬预算，触发 hard degrade |
| Levels 输入 | 102,128 chars | 超硬预算，触发 hard degrade |
| Narrative 输入 | 113,202 chars | 超硬预算，触发 hard degrade |
| 报告文件 | 约 1.3 MB | `meta.llm_io` 约 660 KB，审计与用户摘要未分层 |
| 运行时可靠度 | 0.650 | 计算时 `agent_trace` 尚未写入，证据覆盖与来源多样性错误为 0 |
| 归档后重算可靠度 | 0.945 | 同一算法读取完整 trace 后的对照值；仍为启发式、非胜率 |

## 3. Findings

### F-015 · P0 · 报告可靠度在证据链落盘前计算

- 证据：`orchestrator` 先调用 `compute_report_reliability(report)`，后写入 `report["agent_trace"]`。
- 影响：`evidence_coverage`、`source_diversity`、`bull_bear_separation` 使用空 trace，UI 与归档质量分失真。
- 要求：事实注册、不变量、完整 `agent_trace` 写入后才可计算可靠度与 audit summary。
- 追溯：SWR-REP-004、SWR-NFR-002；ARC-CORE、ARC-ANALYSIS；VM-UNIT、VM-INTEGRATION-PIPELINE。

### F-016 · P0 · PA 最近支撑/阻力允许跨越现价

- 证据：现价 4386.59 时，`nearest_support` 含 4393.78、4392.19；实现允许支撑最高到 `price*1.002`、阻力最低到 `price*0.998`。
- 影响：上方价位被称为支撑、下方价位被称为阻力，污染 Technical、Levels 与 Narrative 的金融语义。
- 要求：支撑必须严格不高于现价，阻力必须严格不低于现价；共振容差只用于匹配，不得改变方向标签。
- 追溯：SWR-ANA-001；ARC-ANALYSIS；VM-UNIT、VM-REGRESSION。

### F-017 · P0 · Research evidence ID 契约冲突与规则回退失控

- 证据：Research prompt 允许新增 structure ID，parser 却只接受 Analyst 白名单；Bearish 连续生成三个未知 ID 后失败。规则回退产生 163 条无 `evidence_id` 证据，且 Bull/Bear 流动性追加位于不可达 `continue` 之后。
- 影响：付费重试、来源断链、上下文膨胀、Bull/Bear 证据不对称。
- 要求：Research 只允许引用上游白名单 ID；规则证据必须分配稳定 ID、按强度/时效限额并保留来源；流动性分支必须可达。
- 追溯：SWR-AGT-001、SWR-LLM-002、SWR-REP-002；ARC-AGENTS、ARC-LLM；VM-UNIT、VM-REGRESSION。

### F-018 · P1 · LLM 预算与 usage 审计不闭合

- 证据：stage trace 只保存 `last_usage`；重试前两次 usage 被覆盖。三个阶段以字符串硬截断进入 `hard_degrade`，黄金日内 mandate 在 system/user 中重复。
- 影响：token 低估、成本不可审计、截断可能切断结构化 JSON、延迟与报告体积异常。
- 要求：逐 attempt 记录并累计供应商 usage；在序列化前按业务优先级压缩结构化 payload；硬截断仅作最后防线且必须可见。
- 追溯：SWR-LLM-001、SWR-NFR-002；ARC-LLM、ARC-CORE；VM-UNIT、VM-REGRESSION。

### F-019 · P1 · EMA610 数据不足仍被声明 ready

- 证据：1d/4h/1h/15m 仅 360–365 根仍计算并上报 `EMA610` ready，仅以 warning 披露。
- 影响：未充分预热的长周期指标进入分析和 LLM 上下文。
- 要求：bars < 610 时 EMA610 必须为不可用，或先拉足预热窗口；不得同时显示 warning 与 ready。
- 追溯：SWR-ANA-001；ARC-INDICATORS、ARC-DATA；VM-UNIT、VM-REGRESSION。

### F-020 · P2 · 未授权候选审计文案重复

- 证据：六个信号各重复 1,400–1,600 字全局 Manager/Risk/Trader 说明，结论出现重复标点。
- 影响：用户难以区分最终决定、候选条件和详细审计。
- 要求：信号卡只保留本信号直接原因与短摘要；全局完整轨迹只在折叠审计区展示；标点规范化。
- 追溯：SWR-UI-002；ARC-VIZ、ARC-ANALYSIS；VM-UNIT、VM-MANUAL-UI。

## 4. 关闭准则

1. 对每项 Finding 增加冻结夹具或假客户端单测，并将用例登记到 `tests/cases/catalog.yaml`。
2. `python tests/run.py`、ASPICE docs/trace/static 门禁通过。
3. 完整报告契约测试证明可靠度在 trace 后计算、Research 回退有界、usage 跨重试累计。
4. 手工或 helper 验证未授权候选只显示短原因，完整审计仍可访问。
5. `findings-status.md` 回写关闭状态与测试证据；`records/verification/latest.md` 记录本候选验证结果。

## 5. 关闭证据（2026-08-11）

| Finding | 实现与验证 |
|---|---|
| F-015 | `orchestrator` 在写入完整 `agent_trace`/LLM telemetry 后计算可靠度；实时 rule pipeline 通过 coherence 与报告契约检查。 |
| F-016 | `nearest_pa_sr` 严格按现价分侧；`test_nearest_pa_sr_never_crosses_current_price_side` 通过。 |
| F-017 | LLM Research 仅复制白名单 ID；规则回退分配稳定 ID/来源并受 `PAYLOAD_EVIDENCE_MAX` 限制；Bull/Bear 回归通过。 |
| F-018 | 每次 attempt 记录 usage，阶段值累计；Technical/Levels facts 先按引用、周期、距离语义压缩；mandate 每消息单次出现。 |
| F-019 | EMA610 使用 `min_periods=610`，context stats 与 snapshot 在不足 610 根时统一为不可用；609/610 边界测试通过。 |
| F-020 | 拒绝卡摘要合并风控档位、去重、限 6 条并规范标点；完整 Manager/Risk/Trader 数据仍保留在 `agent_trace`。 |

附带修复：实时完整集成发现 `build_report` 使用 1d 收盘而非同批 5m 快照作为 `current_price`，现统一由 `market_metrics` 锚定 5m 最新收盘；报告 swing 区间包含当前价。相关集成用例通过。

历史尾项一并闭环：Fibonacci 静态值从 `probability` 改名为 `display_weight`（F-007）；所有外部 LLM payload 加入“占位数据不可采信”的结构化策略（F-010）；文档字段扫描确认统一使用 `EMA20` / `EMA50` / `EMA610`（F-012）。至此登记的 F-001～F-020 全部关闭。
