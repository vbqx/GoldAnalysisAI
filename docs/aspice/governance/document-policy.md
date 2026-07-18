# 文档治理策略

## 1. 目标

文档必须首先服务阅读、评审和安全修改，其次才服务自动化。任何新增文档都必须有唯一职责、唯一入口和明确的生命周期状态。

## 2. 三层模型

| 层级 | 目录 | 权威性 | 是否人工编辑 |
|---|---|---|---|
| 当前设计 | `docs/aspice/` 的 SWE.1–SWE.6、SUP.8、治理文档 | 当前正式基线 | 是 |
| 结构化自动化 | `docs/aspice/_machine/` | Markdown 与源码的结构化镜像和生成证据 | 仅按生成/同步规则修改 |
| 历史记录 | `docs/aspice/records/`、`docs/archive/` | 历史证据，不代表当前设计 | 追加或归档，不回写当前事实 |

## 3. 单一入口

- 全项目入口：`docs/documentation-center.md`。
- 软件域入口：`docs/aspice/software-domain.md`。
- 仓库根目录 `README.md` 是唯一保留的 README；其他文档必须按实际职责使用语义化文件名。
- 每个 ASPICE 过程只有一个主入口；专题和组件文件必须从主入口可达。
- SWE.3 的“一个域一个文档”解释为一个过程入口，而不是把全部函数堆进一个超大文件。

## 4. 内容归属

| 内容 | 唯一位置 |
|---|---|
| 软件需求 | `SWE.1-software-requirements.md` |
| 当前软件架构 | `SWE.2-architecture/` |
| 组件、模块与函数设计 | `SWE.3-detailed-design/` |
| UT / IT / VT | SWE.4 / SWE.5 / SWE.6 主文档 |
| schema、术语和实现参考 | `SWE.3-detailed-design/reference/` |
| 验证策略和关闭准则 | `governance/` |
| 审核和验证历史 | `records/` |
| 安装、运行和排障 | `docs/operations/` |
| 状态、路线和管理计划 | `docs/management/` |

禁止重新创建顶层 `docs/architecture/`、`docs/reference/`、`docs/testing/`、`docs/reviews/`、`docs/overview/` 或 `docs/planning/`，避免恢复平行权威源。

## 5. 编辑规则

1. SWE.1、SWE.2、SWE.4、SWE.5、SWE.6 和治理 Markdown 是人工评审入口，不由可读文档生成器覆盖。
2. SWE.3 组件函数卡片由源码 AST 和验证映射生成；人工补充内容写入 `critical-units.md` 或 reference 文档。
3. `_machine/` 中的 CSV、JSON、锁文件和过程索引是自动生成产物；YAML 是结构化校验镜像，不作为普通评审入口。
4. 同一事实不得在两个当前设计文档中重复维护；专题文档只能补充主架构，不重新定义组件或接口。
5. 历史审核文件必须带日期，并放入 `records/`。

## 6. 变更检查

每次文档变更至少满足：

- 全仓库 Markdown 文件目标和锚点零断链；
- 文档注册表覆盖全部文档；
- SWE.1–SWE.6 的 ID 和追溯关系完整；
- 生成型 SWE.3 与源码、验证映射一致；
- 禁止目录没有重新出现；
- 业务代码路径无意外差异。

## 7. 规模约束

- 主入口只提供决策所需链接，不罗列全部文件。
- 单个生成型组件文档不得超过 500 KB；超过时按软件单元进一步拆分。
- 历史记录不进入 Owner 主阅读路径。
- `_machine/` 不出现在“推荐阅读”表格中。
