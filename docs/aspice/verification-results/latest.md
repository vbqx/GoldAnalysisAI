# ASPICE 软件域验证结果

**执行日期**：2026-07-18
**状态**：本地验证通过，等待发布提交及远端 CI
**发布基线**：`refs/tags/aspice-software-domain-baseline-2026-07-18`
**源代码基准**：`c9660f1`；本轮业务代码零修改
**结构化记录**：[software-domain-2026-07-18.yaml](./software-domain-2026-07-18.yaml)
**环境**：Windows、CPython 3.12；确定性离线门禁不调用付费 LLM、MT5 或 live supplier API。

| 措施 | 结果 | 证据 |
|---|---|---|
| VM-UNIT | 通过：417 | `python tests/run.py`，OpenBLAS/OMP 单线程 |
| VM-REGRESSION | 通过：25 | `python tests/run.py`，含软件域关闭门禁 |
| VM-INTEGRATION-PIPELINE | 通过：2 | 冻结报告夹具、零网络 |
| VM-BACKTEST | 通过：9 | point-in-time 回测测试；3 条非阻断弃用警告 |
| VM-DOCS | 通过：14 | 文档、追溯、示例和 ASPICE 工作产品回归 |
| VM-TRACE | 通过 | 26 条需求、181 个单元、1046 个函数、71 份文档；需求和单元阻断项均为 0 |
| VM-STATIC | 通过 | `compileall` 与 `git diff --check` |
| VM-CONFIG | 通过 | 配置项、依赖锁、SBOM 和解析结果一致 |
| VM-INTEGRATION-EXTERNAL | 本次未选择 | 供应商接口业务代码未变；HTTP 边界由确定性 mock 单元测试验证 |
| VM-MANUAL-UI | 继承通过 | UI/业务代码未变；沿用受控 UI 验收证据并记录影响分析 |

发布前必须再次执行两个 ASPICE `--check`、完整离线套件和业务代码路径差异检查。远端 CI
未通过前，不得把本记录状态改为 `released`，也不得关闭软件域问题单。
