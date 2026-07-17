# Automotive SPICE 软件域关闭审核报告

**项目**：GoldAnalysisAI
**审核日期**：2026-07-18
**范围**：SWE.1–SWE.6
**候选基线**：`refs/tags/aspice-software-domain-baseline-2026-07-18-v3`
**变更边界**：文档、治理工具、测试与 CI；业务代码零修改
**报告性质**：项目级软件工程证据关闭审核，不是正式 Automotive SPICE 能力等级评估

## 发布门禁偏差处置

- 首次远端门禁暴露两项非业务代码偏差：文档工作流使用 Python 3.11，无法解析现有
  Python 3.12 语法；证据文件路径排序依赖宿主操作系统大小写规则。
- 处置限定在 CI、治理生成器和受控环境文档：工作流与软件环境基线统一为 CPython
  3.12，所有生成输入按 POSIX 相对路径的 `casefold()` 结果确定性排序。
- 发布标签触发被排除，避免同一提交因主分支与注释标签产生重复验证记录；拉取请求和
  `main` 推送门禁保持不变。
- v2 的 Linux 离线门禁进一步发现 3 个 Jin10 mock 用例隐式依赖开发者 `.env`；用例已
  显式注入假令牌，并在清空 Jin10 凭据的环境下完成全套离线验证。

## 1. 关闭结论

按 `docs/aspice/software-domain-scope-and-closure.md` 的项目关闭准则，SWE.1–SWE.6 本地
候选基线判定为 **PASS**。该结论只有在候选基线提交发布、远端 CI 通过且业务代码路径差异
仍为空后才转为 released；在此之前问题单不得关闭。

| 过程 | 结论 | 量化证据 | 关键工作产品 |
|---|---|---|---|
| SWE.1 | PASS | 26/26 发布软件需求属性完整；均有架构和验证链接 | `software-requirements.yaml`、`traceability-matrix.csv` |
| SWE.2 | PASS | 11 个组件、4 个受控架构接口、6 个集成步骤；双向链接无悬挂 | `software-architecture.yaml`、`software-integration-plan.yaml` |
| SWE.3 | PASS | 181/181 unit 和 1046/1046 function 有稳定 ID；逐函数设计字段 100% | `software-unit-catalog.csv`、`software-function-detailed-design.csv` |
| SWE.4 | PASS | 181/181 unit 有选定措施；157 个高风险函数进入风险处置；阻断 unit 为 0 | `software-unit-verification-matrix.csv`、417 项 unit 结果 |
| SWE.5 | PASS | 6/6 集成项含顺序、接口、前置、桩、超时、资源、用例和结果；离线 integration 2 项、回测 9 项通过 | `software-integration-plan.yaml`、结构化结果 |
| SWE.6 | PASS | 26/26 软件需求至少有一个接受结果；阻断需求为 0；25 项 regression 通过 | `software-requirement-verification-coverage.csv`、`verification-results/` |

## 2. 逐函数设计与验证处置

每个函数记录 signature、return contract、职责、前置/后置、显式异常、检测到的副作用、并发
模型、调用依赖、分支数、长度、风险、需求/架构链接、测试引用和验证处置。该表是从受控源码
生成的 as-built 详细设计；高风险关键模块另有人工专项设计。

392 个函数存在直接符号测试引用；其余函数依据风险选择静态验证和所属组件/集成验证。直接
符号引用只作为追溯证据，不被夸大为语义覆盖率。选择矩阵自动阻断“高风险、无动态组件证据、
无已记录处置”的软件单元；候选基线阻断项为 0。

## 3. 验证结果与选择说明

- unit：417 passed；3 条 Pandas 未来弃用警告，已记录为非阻断偏差。
- regression：25 passed。
- deterministic integration：2 passed，冻结夹具、零网络、零付费 token。
- point-in-time backtest：9 passed。
- docs/trace/ASPICE：14 项定向回归通过；两个生成器 `--check` 通过。
- live supplier smoke：本次未选择，因为供应商接口业务代码未变；HTTP 边界使用 mock 完成确定性验证。
- manual UI：本次未修改 UI/业务代码，按影响分析继承既有受控 UI 验收证据。

结构化选择、环境、命令、结果和偏差见
`docs/aspice/verification-results/software-domain-2026-07-18.yaml`。

## 4. 业务代码零修改证明

发布前使用以下路径集合执行 staged 和 baseline 差异检查：

```text
src/
views/
app.py
run_app.py
```

任一集合出现差异均推翻本报告 PASS 结论。本轮新增的 HTTP 测试只在 `tests/` 中使用 mock
验证既有边界，不修改 HTTP 适配器实现。

## 5. 问题单关闭判定

本地验收已满足 #39、#40、#41 的验收标准。#42 属于 SUP.8，不计入软件域完成性声明；其
配置清单、解析结果、依赖锁、SBOM、基线标签和验证汇总已作为软件验证可复现性的支撑证据
完成，可独立按自身验收标准关闭。

只有远端 CI 对发布提交给出成功终态后，才可向每个 Issue 回填提交、tag、测试计数、追溯
计数、偏差和业务代码零修改证据，然后执行关闭。

## 6. 限制

- 本报告不声明 Automotive SPICE CL1/CL2，也不替代合格评估师的访谈、抽样与组织证据评估。
- 外部供应商实时可用性不是软件可控属性；其 smoke 结果必须与确定性软件回归分开解释。
- 后续任何业务代码、需求或架构变更都会使影响闭包内的设计和验证证据重新进入待评审状态。
