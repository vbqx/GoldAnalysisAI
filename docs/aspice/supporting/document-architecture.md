# 文档体系与 ASPICE 过程归属

## 1. 目的

本文件定义 GoldAnalysisAI 文档的受控入口、物理目录、ASPICE 过程归属和变更规则。目标是让评审人员从 `docs/aspice/README.md` 出发理解软件需求、架构、详细设计、UT、IT、VT 及其支撑证据，同时避免为追求单一物理目录而破坏既有引用。

## 2. 组织原则

| 原则 | 约束 |
|---|---|
| 单一评审入口 | `docs/aspice/README.md` 是 ASPICE 软件域及支撑证据的正式入口。 |
| 一个过程一个主文档 | SWE.1–SWE.6、SUP.8 各有一份面向人工评审的 Markdown 主文档。 |
| 物理位置与过程归属分离 | 专题文档可以保留在最适合维护的位置，但必须登记 ASPICE 过程、信息项、状态和权威性。 |
| 机器数据不替代设计 | `_machine/` 只服务于生成、一致性、追溯、配置锁和 CI；设计评审以 Markdown 主文档为准。 |
| 全量登记 | 仓库内文档必须进入 `_machine/document-register.csv`，并出现在 `process-document-index.md`。 |
| 防止漂移 | 新增、删除或移动文档后，生成资产必须同步；CI 对遗漏登记或陈旧产物失败。 |

## 3. 物理目录与过程映射

| 目录 | 内容职责 | 主要 ASPICE 归属 | 在评审中的角色 |
|---|---|---|---|
| `docs/aspice/` | SWE.1–SWE.6、SUP.8 主文档和双向追溯 | SWE.1–SWE.6、SUP.8 | 规范性评审入口 |
| `docs/aspice/supporting/` | 文档控制、范围、关键设计、审核与过程索引 | SUP.1、SUP.8、SUP.9、SWE.3 | 支撑证据 |
| `docs/architecture/` | 专题架构背景、数据流和技术决策 | SWE.2、SWE.3 | 主架构文档的深入参考 |
| `docs/reference/` | schema、配置、接口和示例参考 | SWE.1、SWE.2、SWE.3、SUP.8 | 接口与配置参考 |
| `docs/testing/` | 测试策略、手工步骤、覆盖与度量 | SWE.4、SWE.5、SWE.6 | 验证方法支撑 |
| `docs/operations/` | 安装、运行、故障处理和开发者入门 | SUP.8、MAN.3 | 环境与配置使用说明 |
| `docs/planning/` | 路线、审核计划和风险安排 | MAN.3、MAN.5 | 管理过程证据 |
| `docs/reviews/` | 非 ASPICE 专题评审和历史验收记录 | SUP.1、SUP.9 | 质量与问题分析证据 |
| `docs/archive/` | 已被替代但需保留的历史记录 | SUP.8 | 历史配置状态记录 |

ASPICE 专属审核记录统一放在 `docs/aspice/supporting/reviews/`；其他领域评审继续保留在 `docs/reviews/`，但必须通过过程索引纳入 ASPICE 支撑过程追踪。

## 4. 人工评审路径

1. 从 [ASPICE 文档入口](../README.md)确认评审范围和基线。
2. 按 SWE.1 → SWE.2 → SWE.3 阅读需求、架构、软件单元和逐函数设计。
3. 通过文档内稳定 ID 跳转到 SWE.4、SWE.5、SWE.6 的 UT、IT、VT 证据。
4. 通过 [双向追溯](../traceability.md)检查需求覆盖闭环。
5. 通过 [过程文档索引](./process-document-index.md)检查全部专题和支撑文档的 ASPICE 归属。

## 5. 重构判定

当前不实施“把全部文档物理搬入 `docs/aspice/`”的目录重构。原因是专题文档的维护边界清晰，且仓库内已有大量稳定链接；整体搬迁会产生高变更噪声，却不会提高过程符合性。

只有出现以下情况之一时，才启动物理目录重构：

- 同一信息项存在两个以上相互冲突的权威文档；
- 文档无法唯一映射到过程和所有者；
- 现有目录导致评审人员无法从主文档导航到必要证据；
- 自动链接和登记校验无法在保留路径的前提下消除漂移。

在上述条件出现前，采用“ASPICE 单一入口 + 全量过程登记 + 原专题目录维护”作为受控文档架构。
