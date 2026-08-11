# ASPICE 软件域当前验证基线

- **执行日期**：2026-08-12
- **状态**：`verified-local`
- **范围**：Advice V2 重构、V1 删除、旧归档兼容重建
- **网络**：确定性门禁未调用实时供应商或付费 LLM
- **详细结果**：[software-domain-2026-08-12.yaml](./software-domain-2026-08-12.yaml)

## 验证结果

| 措施 | 结果 | 证据 |
|---|---|---|
| VM-UNIT | 通过，159 项 | `python tests/run.py` unit 阶段 |
| VM-REGRESSION | 通过，20 项 | `python tests/run.py` regression 阶段 |
| VM-INTEGRATION-PIPELINE | 通过 | Advice 引擎、编排、报告与旧归档重建测试 |
| VM-DOCS / VM-TRACE | 通过 | 22 条需求、111 个单元、604 个函数；阻断缺口为 0 |
| VM-STATIC | 通过 | `compileall` 与 `git diff --check` |
| VM-CONFIG | 通过 | ASPICE 资产、登记表、SBOM 与 schema 一致 |
| VM-INTEGRATION-EXTERNAL | 未选择 | 实时供应商不属于离线重构门禁 |
| VM-MANUAL-UI | 未选择 | 自动化 UI 契约已覆盖；视觉冒烟留作发布活动 |

## 关键接受结论

- 当前输出是 `human_review_advice` / `artifact_version: 2`。
- 一次最多一个主建议，决策仅允许 `WAIT`、`WATCH_LONG`、`WATCH_SHORT`、`AVOID`。
- 方向、关注区、失效价、目标和证据由确定性引擎拥有；LLM 只能润色文字。
- 数据过期、高周期冲突、证据不足和非法几何均会降级，不生成伪精确建议。
- V1 Agent/辩论/风险经理/回测主链已从当前代码删除；旧配置字段仅在读取旧归档时兼容。

## 已接受偏差

- pytest 无法写入工作区 `.pytest_cache`，产生非阻断权限警告；测试执行和产品文件不受影响。
- 当前结果是本地工作区候选，不代表远端 CI 或已发布提交。
