# ASPICE 软件域当前验证基线

- **执行日期**：2026-08-12
- **状态**：`verified-local`
- **范围**：Advice V2、LLM 思考过程页、硅基流动默认模型、离线报告契约集成测试
- **网络**：确定性门禁未调用实时供应商或付费 LLM
- **详细结果**：[software-domain-2026-08-12.yaml](./software-domain-2026-08-12.yaml)

## 验证结果

| 措施 | 结果 | 证据 |
|---|---|---|
| VM-UNIT | 通过，167 项 | `python tests/run.py --unit` |
| VM-REGRESSION | 通过，20 项 | `python tests/run.py --regression` |
| VM-INTEGRATION-PIPELINE | 通过，3 项 | `python -m pytest tests/integration/test_offline_report_contract.py -m integration` |
| VM-DOCS / VM-TRACE | 通过 | 22 条需求、114 个单元、618 个函数；阻断缺口为 0 |
| VM-STATIC | 通过 | `compileall` 与 `git diff --check` |
| VM-CONFIG | 通过 | ASPICE 资产、登记表、SBOM 与 schema 一致 |
| VM-INTEGRATION-EXTERNAL | 未选择 | 实时供应商不属于离线重构门禁 |
| VM-MANUAL-UI | 未选择 | 自动化 UI 契约已覆盖；视觉冒烟留作发布活动 |

## 关键接受结论

- 当前输出是 `human_review_advice` / `artifact_version: 2`。
- 一次最多一个主建议，决策仅允许 `WAIT`、`WATCH_LONG`、`WATCH_SHORT`、`AVOID`。
- 方向、关注区、失效价、目标和证据由确定性引擎拥有；LLM 只能润色文字。
- **LLM 思考过程** 页展示生成步骤与 I/O 审计，不恢复 V1 决策链。
- 默认可选文案模型为硅基流动 `deepseek-ai/DeepSeek-V4-Flash`。
- 数据过期、高周期冲突、证据不足和非法几何均会降级，不生成伪精确建议。
- V1 Agent/辩论/风险经理/回测主链已从当前代码删除；旧配置字段仅在读取旧归档时兼容。

## 已接受偏差

- pytest 无法写入工作区 `.pytest_cache`，产生非阻断权限警告；测试执行和产品文件不受影响。
- 当前结果是本地工作区候选，远端 CI 离线门禁需与 PR 分支同步后复验。
