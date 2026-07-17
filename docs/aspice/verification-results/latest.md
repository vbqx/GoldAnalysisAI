# ASPICE 软件域验证结果

**执行日期**：2026-07-17
**发布基线**：`refs/tags/aspice-doc-baseline-2026-07-17`（发布时指向承载本记录的提交）
**源代码基准 SHA**：`6da1e0c2e1ea0f4b43bba85a19db0576a88a37fa`
**需求基线 SHA-256**：`CA08FD103533FC09AC1FECE8CCCFCBD75C48874F9ACC94BC56C00D3681A7BD22`
**依赖锁定 SHA-256**：`1F2DE921FA648F2791ACD6DCB8B59B8407F6B27FA1257B6C896371F33D176C8F`
**环境**：Windows、CPython 3.12；离线门禁不调用付费 LLM、MT5 或 live external API。
**变更边界**：仅文档、治理脚本、测试与 CI；`src/`、`views/`、`app.py`、`run_app.py` 零修改。

| 措施 | 结果 | 证据 |
|---|---|---|
| VM-UNIT | 通过：412 | `python tests/run.py`，OpenBLAS/OMP 单线程 |
| VM-REGRESSION | 通过：23 | `python tests/run.py`，含 ASPICE 资产检查 |
| VM-INTEGRATION-PIPELINE | 通过：2 | `test_offline_report_contract.py`，冻结夹具、零网络 |
| VM-DOCS | 通过：12 | ASPICE、文档结构、流水线同步、示例报告定向回归 |
| VM-TRACE | 通过 | 26 条需求、180 个软件单元、1033 个函数、64 份文档 |
| VM-STATIC | 通过 | `compileall` 与 `git diff --check` |
| VM-CONFIG | 通过 | 配置项、依赖锁定、SBOM、解析结果一致性 |
| VM-INTEGRATION-EXTERNAL | 未执行、不阻断 | 属于受控 live supplier smoke，不纳入确定性离线门禁 |
| VM-MANUAL-UI | 不适用 | 本次未修改功能代码或 UI 行为 |

首次完整单元测试因主机 OpenBLAS 线程内存分配失败而中断（411 通过、1 环境失败）；限制
`OPENBLAS_NUM_THREADS=1` 与 `OMP_NUM_THREADS=1` 后完整重跑通过。该现象归类为执行环境噪声，
没有据此修改功能实现。

本结果由 `.github/workflows/quality.yml` 在发布提交上再次生成 JUnit 证据；若门禁失败，发布和
Issue 关闭必须停止，按 SUP.9 重新进入问题解决流程。
