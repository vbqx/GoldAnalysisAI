# GoldAnalysisAI 文档中心

这里是全项目唯一的人工文档入口。正常阅读只需要进入下面四个区域；生成证据、历史记录和机器镜像不出现在主阅读路径中。

## 从这里开始

| 目标 | 入口 | 内容边界 |
|---|---|---|
| 理解并评审软件 | [ASPICE 软件域](./aspice/software-domain.md) | 需求、架构、详细设计、UT、IT、VT 与追溯 |
| 安装、运行和排障 | [运维与使用](./operations/operations-guide.md) | 环境、启动、数据源接入和操作流程 |
| 查看状态和后续计划 | [项目管理](./management/project-management.md) | 项目状态、路线图、审核计划和自动化工作方式 |
| 查阅已替代材料 | [历史归档](./archive/archive-policy.md) | 不再代表当前设计的历史资料 |

## 权威规则

1. 软件设计事实只维护在 `docs/aspice/`；不再建立平行的 `architecture/`、`reference/` 或 `testing/` 权威目录。
2. SWE.1、SWE.2、SWE.4、SWE.5、SWE.6 的 Markdown 是人工评审和修改入口。
3. SWE.3 使用一个过程入口和按组件拆分的函数设计文件，避免单文件膨胀。
4. `_machine/` 仅用于结构化追溯、生成和 CI，不属于正常阅读路径，也不得替代 Markdown 设计说明。
5. `records/` 保存历史审核和验证结果；历史结论不得覆盖当前主文档。
6. 所有本地 Markdown 文件和锚点链接必须通过全仓库自动校验。

## 维护命令

```bash
python scripts/check_aspice_assets.py --write
python scripts/generate_aspice_software_evidence.py --write
python scripts/generate_aspice_readable_docs.py --write

python scripts/check_aspice_assets.py --check
python scripts/generate_aspice_software_evidence.py --check
python scripts/generate_aspice_readable_docs.py --check
```

详细规则见 [文档治理策略](./aspice/governance/document-policy.md)。

## 免责声明

本项目仅供学习研究，不构成投资建议。
