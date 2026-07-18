# ASPICE 软件域当前验证基线

- **执行日期**：2026-07-18
- **当前状态**：`verified-local`；本文件所在文档一致性修订提交已完成本地确定性门禁，远端门禁将在推送后重新执行
- **业务代码基准**：`ac0a7a6e7c302f4d466c47c14df344deccdf71f9`
- **业务代码变更**：无；本候选只修改文档、测试设计资产和生成型文档索引
- **上一发布快照**：[software-domain-2026-07-18.yaml](./software-domain-2026-07-18.yaml)；该文件是旧发布的不可变历史证据，不代表当前候选统计
- **验证环境**：Windows、CPython 3.12.13；确定性门禁不调用付费 LLM、MT5 或 live supplier API

## 当前候选本地结果

| 措施 | 结果 | 证据或命令 |
|---|---|---|
| VM-UNIT | 通过：417 项；88 条非阻断依赖弃用警告 | `python tests/run.py` 的 unit 阶段 |
| VM-REGRESSION | 通过：31 项 | `python tests/run.py` 的 regression 阶段 |
| VM-DOCS | 通过 | 31 项 regression 包含文档结构、链接、锚点、流水线同步和 ASPICE 工作产品检查 |
| VM-TRACE | 通过 | 26 条需求、182 个软件单元、1082 个函数；157 个高风险函数；需求和单元阻断项均为 0 |
| VM-STATIC | 通过 | `git diff --check`；业务代码路径差异为空 |
| VM-CONFIG | 通过 | 配置项、依赖锁、SBOM、文档注册表和生成索引一致 |
| VM-INTEGRATION-PIPELINE | 本次未选择 | 仅修改文档和测试说明；接口与业务实现未变 |
| VM-INTEGRATION-EXTERNAL | 本次未选择 | 本候选不修改供应商适配器；实时可用性不属于确定性文档门禁 |
| VM-MANUAL-UI | 影响分析后未选择 | UI 代码未变；测试资产仅把现有四页实现同步到验收文字 |

执行的 ASPICE 一致性命令：

```bash
python scripts/check_aspice_assets.py --check
python scripts/generate_aspice_software_evidence.py --check
python scripts/generate_aspice_readable_docs.py --check
```

## 最近一次远端源代码基线

业务代码基准 `ac0a7a6` 的远端门禁已经通过：

- [Docs 29639972034](https://github.com/vbqx/GoldAnalysisAI/actions/runs/29639972034)：成功。
- [Offline quality gate 29639972058](https://github.com/vbqx/GoldAnalysisAI/actions/runs/29639972058)：成功，450 项通过；26 条需求、182 个单元、1082 个函数、90 份文档，阻断项为 0。

上述远端结果证明本轮业务代码基准可用，但不冒充当前尚未推送的文档候选验证。当前候选提交推送后，必须以该提交的新 Docs 和 Offline quality gate 结果更新本节，才可把状态提升为 `released`。

## 偏差与处置

- `DEV-NUMPY-PANDAS-DEPRECATION`：本地 unit 阶段出现 88 条第三方库/时间单位弃用警告；当前均为非阻断，且本候选不修改业务代码。
- 首次本地运行使用了不可写的系统 pytest 临时目录，导致 23 项 fixture setup 权限错误；改用受控 `--basetemp` 后相关测试全部通过，判定为环境边界而非产品缺陷。
