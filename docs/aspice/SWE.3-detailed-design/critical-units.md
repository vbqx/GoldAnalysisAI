# 关键软件单元详细设计

软件单元边界以模块语义为主，不等同于每个 Python 函数。全部模块与函数设计从 [SWE.3 组件导航](./software-detailed-design.md)进入；低风险 helper 继承所属组件设计，以下保留高风险单元的人工专项说明。

## UNIT `src/core/orchestrator.py`

- 职责：实现主流水线状态机并协调 fetch、analysis、agents、report gate 和 archive。
- 输入：冻结 `RunConfig`、环境配置、外部 provider；不得接收未声明的可变全局业务状态。
- 输出：`(report, enriched_data, analyses)`；失败也应通过归档/进度记录明确状态。
- 顺序：begin run → fetch → enrich/analyze → analyst/research/debate → levels/trader/risk/manager → report → invariant gate → archive。
- 前置：运行配置合法；输出目录可写；付费/实盘能力默认禁用。
- 后置：成功/失败状态完成；运行 ID、阶段来源和 audit summary 可追溯。
- 异常：外部源、LLM 或 archive 失败按模块契约降级或失败，不得伪造成 verified 数据。
- 并发：独立研究/外部源可并行；共享进度和 LLM I/O 必须线程安全。
- 追溯：SWR-CORE-001、SWR-CORE-002、SWR-NFR-001、SWR-NFR-002；ARC-CORE；VM-INTEGRATION-PIPELINE。

## UNIT `src/analysis/claim_eligibility.py`

- 职责：对 LLM 技术主张及其事实关系执行确定性资格裁决。
- 输入：结构化 claim、fact registry、entry zone；价格为 XAUUSD 报价单位，区间必须 low≤high。
- 输出：资格、关系审计、反证和理由；未知/部分引用不得成为 `core_execution`。
- 动态行为：解析 fact IDs → 校验允许类型 → 复算 overlap/near/contradiction → 检查与入场区连通性 → 汇总 eligibility。
- 异常：缺字段、未知关系、非数值和断开事实均返回拒绝/降级，不抛出可绕过门禁的异常。
- 追溯：SWR-LLM-003、SWR-ANA-003；ARC-ANALYSIS；VM-UNIT、VM-REGRESSION。

## UNIT `src/backtest/simulator.py`

- 职责：按时间顺序模拟信号入场、止损、目标、到期和平仓。
- 输入：已验证信号和未来窗口 OHLCV；价格单位为 XAUUSD 报价点，费用/滑点使用相同单位。
- 输出：`TradeResult`，包含入场/退出、原因、PnL 和元数据。
- 顺序：检查可成交 → 记录入场 → 每根已收盘 K 线检查 stop/TP → 到期按规则退出。
- 约束：同一根 K 线同时触及止损/目标时使用文档化的保守顺序；不得访问信号时点之后尚未到达的数据生成信号。
- 异常：零/负风险、错误方向或非法目标由上游验证拒绝；模拟器返回可审计失败而非静默修正。
- 追溯：SWR-BT-001、SWR-ANA-002；ARC-BACKTEST；VM-BACKTEST。

## UNIT `src/viz/lightweight_chart.py`

- 职责：把冻结 OHLCV、结构区、投影和信号序列化为 Lightweight Charts HTML。
- 输入：带时间索引的 DataFrame 和已筛选 overlay；显示价格使用 XAUUSD 报价单位。
- 输出：自包含 HTML 字符串；不得修改报告或分析状态。
- 动态行为：裁剪数据 → 序列化 bars/overlays → 构建 projection → 注入只读 HTML/JS 模板。
- 约束：所有时间对齐到图表索引；可见性裁剪不改变决策事实；HTML 转义用户/外部文本。
- 异常：空/不足数据返回可显示降级状态，不制造 K 线或结构。
- 追溯：SWR-UI-001、SWR-UI-002；ARC-VIZ；VM-UNIT、VM-MANUAL-UI。

## 继承式详细设计规则

未在本文件单列的模块，其静态接口由 [SWE.3 软件详细设计](./software-detailed-design.md) 的函数/类清单和类型注解定义，动态职责由 [SWE.2 软件架构](../SWE.2-architecture/software-architecture.md) 定义。若模块包含以下任一特征，必须新增专门章节：执行授权、外部副作用、归档写入、并发、超过 200 行的公开函数、关键算法或安全边界。
