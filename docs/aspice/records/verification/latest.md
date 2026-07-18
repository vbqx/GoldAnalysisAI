# ASPICE 软件域验证结果

**执行日期**：2026-07-18
**状态**：`released`；可读文档候选的远端 Docs 与 Offline quality gate 均通过
**发布基线**：`refs/tags/aspice-software-domain-release-2026-07-18`
**已验证候选**：`08ddc89e9652f38fd4d27bd007cbf48f410fc240`（`refs/tags/aspice-software-domain-readable-baseline-2026-07-18`）
**源代码基准**：`c9660f1`；本轮业务代码零修改
**结构化记录**：[software-domain-2026-07-18.yaml](./software-domain-2026-07-18.yaml)
**环境**：Windows 本地与 Ubuntu GitHub Actions、CPython 3.12；确定性离线门禁不调用付费 LLM、MT5 或 live supplier API。
**远端证据**：Docs [29608653351](https://github.com/vbqx/GoldAnalysisAI/actions/runs/29608653351)；Offline quality gate [29608653375](https://github.com/vbqx/GoldAnalysisAI/actions/runs/29608653375)，Linux 环境 445 项通过。

| 措施 | 结果 | 证据 |
|---|---|---|
| VM-UNIT | 通过：417 | `python tests/run.py`，OpenBLAS/OMP 单线程 |
| VM-REGRESSION | 通过：26 | `python tests/run.py`，含软件域关闭门禁与跨文档锚点检查 |
| VM-INTEGRATION-PIPELINE | 通过：2 | 冻结报告夹具、零网络 |
| VM-BACKTEST | 通过：9 | point-in-time 回测测试；3 条非阻断弃用警告 |
| VM-DOCS | 通过：15 | 文档、追溯、示例、跨域导航和 ASPICE 工作产品回归 |
| VM-TRACE | 通过 | 26 条需求、182 个单元、1068 个函数、79 份文档；需求和单元阻断项均为 0 |
| VM-STATIC | 通过 | `compileall` 与 `git diff --check` |
| VM-CONFIG | 通过 | 配置项、依赖锁、SBOM 和解析结果一致 |
| VM-INTEGRATION-EXTERNAL | 本次未选择 | 供应商接口业务代码未变；HTTP 边界由确定性 mock 单元测试验证 |
| VM-MANUAL-UI | 继承通过 | UI/业务代码未变；沿用受控 UI 验收证据并记录影响分析 |

发布准入已经完成：三个 ASPICE `--check`、445 项完整离线套件、业务代码路径差异检查和
当前可读文档候选的远端双门禁均通过。最终发布记录提交通过同一双门禁后关闭软件域问题单。
