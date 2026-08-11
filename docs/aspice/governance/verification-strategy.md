# Advice V2 验证策略

当前验证对象是供人工确认的交易建议，不包含自动下单。验证优先保证建议可解释、价格几何正确、证据可追溯，并确保 LLM 不能改变方向或数值。

## 分层门禁

| 层级 | 命令 | 目的 |
|---|---|---|
| 日常回归 | `python tests/run.py` | 无网络单元测试与文档回归 |
| Advice 专项 | `pytest tests/unit/test_advice_v2.py tests/unit/test_advice_architecture_smoke.py -q` | 决策、几何、证据、时效和输出契约 |
| 软件证据 | `python scripts/generate_aspice_software_evidence.py --check` | SWE.1–SWE.6 机器证据一致性 |
| 可读文档 | `python scripts/generate_aspice_readable_docs.py --check` | 机器证据与评审文档同步 |
| 资产与链接 | `python scripts/check_aspice_assets.py --check` | 文档登记、链接与追溯有效 |
| 静态校验 | `python -m compileall -q src app.py run_app.py scripts` | Python 模块可编译 |
| GUI 验收 | `python run_app.py` | 建议页、外部数据页和历史回放人工冒烟 |

## Advice V2 接受准则

- 决策只能是 `WAIT`、`WATCH_LONG`、`WATCH_SHORT`、`AVOID`。
- 每次最多一个主建议；无合格机会时明确等待或规避。
- 关注区、失效价和目标价满足方向几何，目标不超过两个。
- 建议引用实际结构证据；高周期冲突、数据过期和低质量输入会降级。
- LLM 仅润色解释文字，任何新增价格、方向变更或 schema 越界均回退规则结果。
- 归档报告标识为 `human_review_advice` / `artifact_version: 2`，旧归档仅作为输入重建 V2。

## 维护规则

- 改建议字段时同步 [报告 schema](../SWE.3-detailed-design/reference/examples/report-schema.md)。
- 改流水线阶段时同步 [流水线步骤](../SWE.3-detailed-design/reference/pipeline-steps.yaml)。
- 新增验证用例时同步 [测试目录](../../../tests/cases/catalog.yaml)。
- 发版前保存验证结果到 [records/verification](../records/verification/)。
