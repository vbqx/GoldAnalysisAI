# ASPICE 软件域范围与关闭准则

## 1. 适用范围

本基线只对 Automotive SPICE 软件工程过程组作出完成性结论：SWE.1、SWE.2、SWE.3、
SWE.4、SWE.5 和 SWE.6。SUP、MAN、ACQ、SPL、SYS、HWE、MLE、PIM 与 REU 不在本轮
完成性声明中；其中配置、问题和变更记录仅作为软件工程证据的支撑信息。

软件发布范围包括 `app.py`、`run_app.py`、`views/`、`src/` 和随产品维护的 `scripts/`。
一个 Python 模块定义为一个 software unit；模块内每个函数/方法都必须映射到该 unit，并在
逐函数 as-built 设计表中记录静态接口、行为、异常、外部影响、并发、风险和验证处置。

## 2. 不修改功能代码的整改边界

本轮只允许修改 `docs/`、`tests/`、`scripts/` 中的治理工具和 `.github/workflows/`。
禁止修改 `src/`、`views/`、`app.py` 与 `run_app.py`。发布前必须用 Git 路径差异再次证明该
边界；若业务代码出现差异，软件域关闭审核自动失败。

## 3. SWE.1–SWE.6 关闭条件

| 过程 | 关闭条件 | 主要证据 |
|---|---|---|
| SWE.1 | 发布需求属性完整，均有架构和验证正向链接，反向无孤儿 | [软件需求](../SWE.1-software-requirements.md)、[双向追溯](../traceability.md) |
| SWE.2 | 组件、接口、模式和动态行为受控，并与需求双向一致 | [软件架构](../SWE.2-architecture/software-architecture.md)、[IT](../SWE.5-integration-testing.md) |
| SWE.3 | 所有 unit/function 有稳定 ID；全部函数有 as-built 设计字段；公开/高风险设计可审查 | [软件详细设计](../SWE.3-detailed-design/software-detailed-design.md) |
| SWE.4 | 每个 unit 有选定验证措施；高风险 unit 有直接或受控组件级动态证据；无未处置阻断项 | [UT](../SWE.4-unit-testing.md)、JUnit 结果 |
| SWE.5 | 集成顺序、接口、前置条件、桩、超时、资源、用例和结果均受控 | [IT](../SWE.5-integration-testing.md)、离线 integration JUnit |
| SWE.6 | 每条软件需求均有验证措施和结果；发布验证绑定 Git、配置、环境和用例版本 | [VT](../SWE.6-validation-testing.md)、[最新结果](../records/verification/latest.md) |

## 4. 关闭规则

只有以下检查全部通过才能关闭软件域问题单：

1. 两个 ASPICE 生成器以 `--check` 返回 0，且无 orphan、dangling 或 blocking-gap。
2. 完整 unit、regression 和确定性 integration 通过，并由 CI 保存 JUnit。
3. 发布需求覆盖率、unit 验证选择率、函数设计记录率均为 100%。
4. `git diff` 证明业务代码零修改。
5. 基线提交和 tag 已发布，远端 CI 通过，Issue 留有提交、tag、测试和偏差证据。

该关闭审核是项目的软件工程证据审查，不冒充由认可评估师实施的正式能力等级评估。
