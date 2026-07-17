# Automotive SPICE 软件工程工作产品

本目录是 GoldAnalysisAI 的 ASPICE 软件域控制入口。现有文档不批量移动；全部文档通过注册表按过程、信息项、状态和权威性重新归纳。

## 受控基线

| 过程 | 工作产品 |
|---|---|
| SWE.1 | [软件需求基线](./software-requirements.yaml) |
| SWE.2 | [软件架构基线](./software-architecture.yaml) |
| SWE.3 | [软件单元目录](./software-unit-catalog.csv) · [函数映射](./software-function-map.csv) · [关键单元详细设计](./key-unit-detailed-designs.md) |
| SWE.4–SWE.6 | [验证措施](./verification-measures.yaml) · [最新验证结果](./verification-results/latest.md) |
| SWE.1–SWE.6 | [双向追溯矩阵](./traceability-matrix.csv) |
| SWE.1–SWE.6 范围 | [软件域范围与关闭准则](./software-domain-scope-and-closure.md) |
| SWE.3 | [逐函数 as-built 详细设计](./software-function-detailed-design.csv) |
| SWE.4 | [软件单元验证选择矩阵](./software-unit-verification-matrix.csv) |
| SWE.5 | [软件集成计划与结果矩阵](./software-integration-plan.yaml) |
| SWE.6 | [软件需求验证覆盖矩阵](./software-requirement-verification-coverage.csv) |
| SUP.8 | [配置管理基线](./configuration-management.yaml) · [依赖锁](./dependency-lock.txt) · [SBOM](./sbom.json) |
| SUP.8 文档控制 | [控制规则](./document-control.md) · [全部文档注册表](./document-register.csv) · [过程文档索引](./process-document-index.md) |

## 生成与校验

```bash
python scripts/check_aspice_assets.py --write
python scripts/check_aspice_assets.py --check
python scripts/generate_aspice_software_evidence.py --write
python scripts/generate_aspice_software_evidence.py --check
```

`--write` 只更新生成型治理资产，不修改功能代码。`--check` 验证：

- 每份现有文档均已注册并分类；
- requirement、architecture、verification 双向链接无孤儿或悬挂；
- 每个非测试 Python 模块和函数映射到稳定 software unit；
- 配置项路径存在；dependency lock 与 SBOM 一致；
- 生成文件与受控源同步。

## 评估与改进记录

- [2026-07-17 软件域文档审核报告](../reviews/aspice/software-domain-document-audit-2026-07-17.md)
- GitHub Issues：[#39](https://github.com/vbqx/GoldAnalysisAI/issues/39)、[#40](https://github.com/vbqx/GoldAnalysisAI/issues/40)、[#41](https://github.com/vbqx/GoldAnalysisAI/issues/41)、[#42](https://github.com/vbqx/GoldAnalysisAI/issues/42)
