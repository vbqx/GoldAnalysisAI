# Advice V2 关键软件单元详细设计

完整函数级设计由 [SWE.3 组件导航](./software-detailed-design.md)生成。本文件补充人工复核建议链中风险最高的单元边界。

## `src/core/orchestrator.py`

- 职责：按数据、指标、结构、建议、报告、归档顺序编排一次运行。
- 输入：规范化 `RunConfig` 和已配置数据源。
- 输出：`(report, enriched_data, analyses)`；报告固定为 Advice V2。
- 约束：建议完成确定性审计后才能归档；失败必须结束进度状态并保留诊断。
- 追溯：SWR-CORE-001、SWR-CORE-002、SWR-ARC-001；ARC-CORE；VM-INTEGRATION-PIPELINE。

## `src/advice/engine.py`

- 职责：把高周期方向、15m 上下文、结构事实和数据质量压缩为一个建议。
- 输出：`WAIT`、`WATCH_LONG`、`WATCH_SHORT` 或 `AVOID`；最多一个关注区和两个目标。
- 不变量：做多失效价低于关注区、目标高于关注区；做空反向；证据 ID 必须来自输入事实。
- 降级：数据过期直接规避，高周期冲突等待，证据或几何不足不生成观察方向。
- 追溯：SWR-ADV-001～SWR-ADV-004；ARC-ADVICE；VM-UNIT。

## `src/advice/audit.py`

- 职责：独立复核建议 schema、方向几何、证据引用、目标数量与风险收益。
- 输出：可审计问题列表和通过状态；不得静默修正不合法价格。
- 追溯：SWR-ADV-002、SWR-ADV-003、SWR-NFR-002；ARC-ADVICE；VM-UNIT。

## `src/advice/llm.py` 与 `src/llm/stage.py`

- 职责：对确定性建议执行可选的文字润色，并记录模型、重试、预算和错误。
- 安全边界：只接受允许的文字字段；方向、关注区、失效价、目标、证据和审计结果不可修改。
- 回退：输出含未授权价格、schema 越界、传输失败或 JSON 失败时，保留原规则文字。
- 追溯：SWR-LLM-001、SWR-LLM-002；ARC-ADVICE、ARC-LLM；VM-UNIT。

## `src/viz/replay_loader.py`

- 职责：展示 Advice V2 归档；旧归档忽略旧报告内容并从保存的行情和结构事实重建 V2。
- 隔离：回放不得重新请求行情、外部数据或 LLM；缺失外部快照时使用明确的空背景并显示警告。
- 追溯：SWR-ARC-002、SWR-UI-002、SWR-NFR-004；ARC-VIZ、ARC-RUN；VM-REGRESSION。

## 继承规则

其余模块继承所属 SWE.2 组件职责和自动生成的函数级设计。涉及外部副作用、并发、归档写入、建议数值或人工确认边界的变更，必须在本文件补充专项设计并新增动态验证。
