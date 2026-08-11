# ASPICE 软件域范围与关闭准则

## 1. 适用范围

本基线覆盖 Automotive SPICE 软件工程过程 SWE.1～SWE.6，并以 SUP.8 配置管理证据支撑变更追溯。它是项目内部的软件工程符合性基线，不冒充认可评估师实施的正式能力等级评估。

本次受控变更是 Advice V2 重构：产品从 V1 多阶段决策报告调整为“生成一条可供人工确认的交易建议”。变更范围包括 `app.py`、`views/`、`src/`、`tests/`、`scripts/`、`.env.example` 和相关文档。V1 删除属于已批准范围，不适用“业务代码零差异”的文档整改规则。

软件单元以 Python 模块为边界；每个函数或方法必须归属一个单元，并记录设计、风险和验证处置。历史评审记录保留原时点事实，但不得定义当前架构。

## 2. Advice V2 产品边界

- 输出供人工审核，不自动下单，不授权仓位。
- 一次最多一个主建议；无合格机会时输出 `WAIT` 或 `AVOID`。
- 方向、关注区、失效价、目标和证据由确定性逻辑拥有。
- LLM 只能润色允许的文字字段，失败或越界时回退确定性结果。
- 旧归档只用保存的数据重建 Advice V2，不重新获取外部数据或调用 LLM。

## 3. SWE.1～SWE.6 关闭条件

| 过程 | 关闭条件 | 主要证据 |
|---|---|---|
| SWE.1 | 每条需求具有来源、优先级、接受准则、架构分配和验证措施 | [软件需求](../SWE.1-software-requirements.md)、[追溯](../traceability.md) |
| SWE.2 | Advice V2 组件、接口、运行模式和故障降级与需求一致 | [软件架构](../SWE.2-architecture/software-architecture.md)、[建议专题](../SWE.2-architecture/human-review-advice.md) |
| SWE.3 | 所有当前源码单元和函数具有稳定 ID、设计字段与验证处置 | [软件详细设计](../SWE.3-detailed-design/software-detailed-design.md) |
| SWE.4 | 每个软件单元选择验证措施，高风险逻辑具有直接或组件级动态证据 | [单元测试](../SWE.4-unit-testing.md) |
| SWE.5 | 数据、分析、建议、LLM、报告和归档接口具有顺序、桩、超时和结果 | [集成测试](../SWE.5-integration-testing.md) |
| SWE.6 | 每条需求均有接受结果；未选择的实时或人工活动具有明确偏差处置 | [验证测试](../SWE.6-validation-testing.md)、[最新结果](../records/verification/latest.md) |

## 4. 本地候选关闭规则

满足以下条件可标记为 `verified-local`：

1. ASPICE 资产、软件证据和可读文档三项 `--check` 均返回 0。
2. 离线 unit 与 regression 全部通过，Advice V2 关键集成契约有自动化证据。
3. 需求覆盖、软件单元验证选择和函数设计记录无 `blocking-gap`。
4. `git diff --check` 与 Python 编译通过。
5. 业务代码差异与 Advice V2 变更范围一致；删除项和兼容边界有评审记录。
6. 未执行的实时供应商或人工视觉活动在验证结果中标记为 `not-selected`，不得表述为通过。

## 5. 发布关闭规则

`verified-local` 不等于已发布。发布关闭还要求：

1. 变更提交到可追溯 commit，并完成评审批准。
2. 远端 CI 通过并保存测试证据。
3. 需要发布视觉验收时执行 `python run_app.py` 完成人工冒烟。
4. 建立发布 tag 或等价不可变引用，并将 SUP.8 的候选基线更新为正式基线。

当前候选状态见 [验证基线](../records/verification/latest.md)。
