# ASPICE 文档控制与归类规则

本项目保留现有文档路径，以避免批量移动导致历史链接、测试和外部引用失效。ASPICE 归纳通过受控注册表和过程索引完成，而不是通过目录名猜测过程。

## 文档生命周期

| 状态 | 含义 |
|---|---|
| `agreed` | 当前权威工作产品，变更需评审并更新受影响追溯 |
| `reviewed` | 已评审的支持证据，但不是唯一权威事实 |
| `informative` | 指南、示例或上手材料，不作为符合性唯一证据 |
| `historical` | 历史记录，仅用于追溯，不参与当前设计判断 |
| `generated` | 从受控源生成，禁止手工编辑 |

## 权威性

- `normative`：定义当前需求、架构、设计、验证或配置基线。
- `supporting`：提供操作、解释、评审或验证证据。
- `historical`：保留旧判断或运行快照。
- `generated`：由 `scripts/check_aspice_assets.py --write` 生成。

## 变更规则

1. 新增文档必须出现在 `_machine/document-register.csv`，并声明 primary process、information item、状态和权威性。
2. 修改 normative 文档时必须更新受影响需求、架构、单元或验证追溯。
3. 被替代文档不删除，转为 historical 并记录 `superseded_by`。
4. 评审记录和验证结果绑定 Git SHA、环境和日期。
5. `scripts/check_aspice_assets.py --check` 在 CI 中阻断未登记文档、悬挂链接和生成物漂移。

## 过程归类

| 过程 | 主要文档类型 |
|---|---|
| SWE.1 | 软件需求、需求属性、运行环境影响和约定证据 |
| SWE.2 | 软件架构、接口、模式、架构分析和一致性证据 |
| SWE.3 | 软件单元目录、函数映射、关键单元详细设计 |
| SWE.4 | 单元验证措施、选择和结果 |
| SWE.5 | 组件/集成顺序、接口验证和结果 |
| SWE.6 | 软件需求验证、回归选择和汇总结果 |
| SUP.1 | 质量保证、评审和符合性记录 |
| SUP.8 | 文档注册表、配置项、基线、锁和 SBOM |
| SUP.9 | 问题单、复现、原因和关闭证据 |
| SUP.10 | 变更请求、影响分析和批准 |
| MAN.3/MAN.5 | 计划、状态、风险和里程碑 |

完整逐文档归类见 [_machine/document-register.csv](../_machine/document-register.csv)，按过程导航见 [process-document-index.md](./process-document-index.md)。人工评审请从 [软件域入口](../README.md) 开始。
