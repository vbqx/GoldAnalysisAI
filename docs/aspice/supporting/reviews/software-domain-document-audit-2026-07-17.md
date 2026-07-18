# Automotive SPICE 4.0 软件域文档审核报告

**项目**：GoldAnalysisAI
**审核日期**：2026-07-17
**审核快照**：`main@6da1e0c2e1ea0f4b43bba85a19db0576a88a37fa`，与 `origin/main` 一致，审核开始时工作区干净
**审核范围**：软件工程过程组 SWE.1–SWE.6；为判断软件域过程可管理性，补充检查 SUP.1、SUP.8、SUP.9、SUP.10 和 MAN.3 的仓库证据
**详细程度**：正文覆盖过程、信息项和根因；函数级附录覆盖 179 个非测试 Python 文件中的 1,013 个函数
**报告性质**：基于仓库静态证据和测试执行的差距审核，不是经认可评估师实施的正式 Automotive SPICE 能力等级评估

## 1. 结论

项目已经形成较强的“实现可读性”和“回归保护”基础：架构、报告可信度、回测、运行归档、测试策略等主题有专门文档；本次离线执行的 412 项单元测试和 21 项回归测试全部通过。现有代码中 860/1,013 个函数具备完整参数/返回注解。

但当前文档体系尚不能提供 Automotive SPICE 4.0 所要求的软件生命周期双向证据链。主要断点不是代码是否可运行，而是没有受控的软件需求基线，也没有将需求、软件架构、软件详细设计/软件单元、验证措施和验证结果连接起来。因此，当前仓库证据不足以证明任何 SWE 过程完整达到 Capability Level 1；更不能证明 Level 2 的计划、监控、职责、工作产品管理和质量保证。

本次结论按“审核前已有证据”判定。本文和函数附录本身是审核产物，不能反向视为审核前已满足 SWE.3 或 SWE.4。

### 1.1 过程结论

| 过程 | 结论 | 已有证据 | 主要断点 |
|---|---|---|---|
| SWE.1 软件需求分析 | N 未满足 | 项目定位、roadmap、测试用例目录包含分散需求意图 | 无受控 SRS、需求属性、优先级、可验证准则、运行环境影响分析和双向追溯 |
| SWE.2 软件架构设计 | P 部分满足 | `docs/architecture/` 有静态分层、数据流、模式和接口说明 | 无架构元素 ID、接口全集、架构分析准则/结果、需求↔架构双向追溯 |
| SWE.3 软件详细设计与单元构建 | P 部分满足 | 源码、类型注解、部分 docstring 和代码级 handbook | 766/1,013 个函数无函数说明；无软件单元详细设计基线；缺值域、物理单位、异常、状态和并发契约 |
| SWE.4 软件单元验证 | P 部分满足 | 单元测试 412 项通过；大量局部测试 | 无逐软件单元验证措施、选取准则、入口/出口、完整追溯和持久化结果；646 个函数无同名测试引用证据 |
| SWE.5 软件组件与集成验证 | P 部分满足 | `tests/integration/`、流水线/外部源集成用例 | 无集成顺序、前置条件、组件接口/交互验证矩阵和结果基线；本次套件在 6 项通过后长时间无新增结果，未形成完整结果 |
| SWE.6 软件验证 | P 部分满足 | 116 条测试目录项、手工/集成/回归场景 | 用例未从软件需求基线派生；无需求覆盖、版本化验证结果和发布范围选择证据 |

`N/P` 是本文的文档证据判定，不等同于正式 assessment 的 N/P/L/F rating。

### 1.2 函数级总览

| 指标 | 数量 | 比例 |
|---|---:|---:|
| 纳入审核的函数 | 1,013 | 100% |
| 有 docstring/函数说明 | 247 | 24.4% |
| 参数与返回完整注解 | 860 | 84.9% |
| 在 Markdown 文档中有同名符号引用 | 171 | 16.9% |
| 在测试中有同名符号引用 | 367 | 36.2% |
| 函数级判定“部分满足” | 40 | 3.9% |
| 函数级判定“证据不足” | 454 | 44.8% |
| 函数级判定“未满足” | 519 | 51.2% |

完整逐函数记录见 [software-function-audit-2026-07-17.csv](./software-function-audit-2026-07-17.csv)。每一行都包含稳定软件单元 ID、文件/行号、函数名、可见性、函数说明、接口证据、需求/架构追溯、测试引用、ASPICE 文档判定和关联发现。

## 2. 准则与方法

### 2.1 规范基线

审核使用 VDA QMC 发布的 **Automotive SPICE 4.0 PRM/PAM（2023-12）**：

- 发布页：<https://vda-qmc.de/en/automotive-spice/automotive-spice-veroeffentlichungen/>
- 英文 PAM：<https://vda-qmc.de/wp-content/uploads/2023/12/Automotive-SPICE-PAM-v40.pdf>
- 中文 PAM：<https://vda-qmc.de/wp-content/uploads/2024/08/AutomotiveSPICE_PAM_40_Chinese.pdf>

SWE.1–SWE.6 是 Automotive SPICE 4.0 软件工程插件的 V 模型过程。PAM 要求以基本实践和信息项判断过程成果；仅有源代码、链接或测试数量不等于信息一致。

本项目调用第三方大模型，但仓库内未训练或交付自有 ML 模型，因此本次不对 MLE.1–MLE.4 作过程判定。LLM 输入输出契约、供应商模型配置和降级行为仍作为软件组件接口纳入 SWE.1–SWE.6。

### 2.2 证据源

- 当前文档：`README.md`、`docs/overview/`、`docs/architecture/`、`docs/reference/`、`docs/testing/`、`docs/planning/`、`docs/reviews/`
- 软件实现：`app.py`、`run_app.py`、`src/`、`views/`、`scripts/`
- 验证资产：`tests/unit/`、`tests/regression/`、`tests/integration/`、`tests/cases/catalog.yaml`、`.github/workflows/docs.yml`
- 配置资产：`requirements*.txt`、`.env.example`、`pytest.ini`、Git 历史和 GitHub Issues
- 函数清单：Python AST；排除 `tests/`、虚拟环境、缓存和审核工具本身

### 2.3 函数级判定规则

函数级附录采用保守的可复核规则：

1. `有函数说明` 仅表示存在 docstring，不代表已形成经评审的软件详细设计。
2. `完整注解` 检查参数和返回注解，不检查业务值域、量纲和运行时契约。
3. 文档/测试引用使用精确符号名匹配；它能证明存在引用，不能证明语义覆盖。
4. 无同名测试引用不等于函数一定未被间接测试，因此判为“缺追溯证据”，不直接判为代码未测试。
5. 每个函数都关联到共性根因，整改应建立可生成的追溯矩阵，不应机械创建 1,013 个独立 Issue。

## 3. SWE.1 软件需求分析

### 3.1 已有证据

- `docs/overview/project.md` 说明产品定位和能力边界。
- `docs/planning/roadmap.md` 包含目标、阶段任务和部分验收条件。
- `tests/cases/catalog.yaml` 有 116 条目录项，其中 42 条 unit、12 条 integration、8 条 regression、49 条 manual；58 条标为自动、53 条标为手工，5 条未填写。
- `docs/planning/audit-plan.md` 对报告可信度和运行审核给出较强的不变量要求。

### 3.2 不符合/缺口

- 没有唯一的软件需求工作产品；roadmap、架构说明、测试目录和历史 review 混合了承诺、设计、计划与缺陷。
- 没有稳定软件需求 ID、版本、状态、来源、优先级、责任人、发布范围和变更历史。
- 大部分描述不是“单一、无歧义、可验证、无实现约束”的需求语句。
- 功能需求、性能、可靠性、安全、数据时效、可观测性、降级、隐私/凭据、可维护性等非功能需求没有统一结构。
- 未形成软件需求对运行环境的系统化影响分析，例如 Windows/Streamlit、TradingView/Jin10、第三方 LLM、MT5、网络/代理、时区和市场 session。
- 没有系统/利益相关方需求↔软件需求↔软件架构的双向追溯。

### 3.3 判定

SWE.1 的核心输出 `17-00 Requirement`、`17-54 Requirement Attribute`、`15-51 Analysis Results`、`13-51 Consistency Evidence`、`13-52 Communication Evidence` 均不完整。分散文档可作为需求挖掘输入，但不能作为已约定的软件需求基线。

## 4. SWE.2 软件架构设计

### 4.1 已有证据

- `docs/architecture/architecture.md` 给出数据流、分层、主组件和关键对外接口。
- `llm-agents.md`、`report-trust.md`、`backtesting.md`、`technical-analysis.md` 等文档补充分支模式和领域架构。
- `docs/reference/handbook.md` 提供模块职责、调用入口和最小测试建议。

### 4.2 不符合/缺口

- 架构元素和接口没有稳定 ID，无法作为追溯端点。
- 外部接口、组件接口、数据结构、异常、超时、重试、并发、资源/性能和各运行模式未形成完整统一清单。
- 没有基于明确准则的架构分析记录，例如可测试性、时延预算、资源、可修改性、故障隔离和第三方失效。
- 无软件需求↔架构元素双向矩阵；现有链接主要是导航链接。
- 发现实际文档漂移：`docs/reference/handbook.md` 仍称 `src/backtest/` 包含 `replay.py`，当前实现不存在该文件。

### 4.3 判定

静态和动态架构已有良好骨架，但 SWE.2.BP3/BP4 的分析与一致性/双向追溯证据不足。文档可作为建立正式架构工作产品的基础。

## 5. SWE.3 软件详细设计与单元构建

### 5.1 已有证据

- 1,013 个函数均可定位到源文件和行号。
- 860 个函数具备完整参数/返回注解。
- 247 个函数有 docstring；部分复杂模块拥有专题架构说明和测试。
- 源码与 Git 提供软件单元构建和版本历史。

### 5.2 不符合/缺口

- 766 个函数没有函数级说明；842 个函数没有任何同名文档引用。
- 未定义软件组件与软件单元的正式拆分原则。文件、类、函数和 ASPICE software unit 之间没有受控映射。
- 缺少每个软件单元的静态结构、动态行为、调用关系、状态转换、异常和降级路径。
- 接口注解普遍不能表达应用域约束；153 个函数连完整类型注解也没有。
- 交易价格、时间、周期、百分比、置信度、token、毫秒等输入输出缺少统一值域和物理/测量单位契约。
- 源代码↔详细设计↔架构↔软件需求没有双向追溯。

### 5.3 高风险示例

| 软件单元 | 规模 | 文档/验证风险 |
|---|---:|---|
| `src/viz/lightweight_chart.py::build_lightweight_chart_html` | 478 行 | 无同名架构引用；长函数承载序列化、图层和 HTML 生成 |
| `src/core/orchestrator.py::run_trade_agent_pipeline` | 371 行 | 有架构引用，但没有同名测试追溯；主状态机缺函数级详细设计 |
| `src/analysis/claim_eligibility.py::adjudicate_level_proposal_claim` | 274 行 | 有测试引用但无同名设计引用；属于执行资格关键单元 |
| `src/viz/agent_trace_view.py::render_agent_trace_panel` | 266 行 | 无同名文档与测试引用 |
| `src/backtest/simulator.py::simulate_signal` | 156 行 | 有测试引用但无同名设计引用；交易仿真假设需明确值域/顺序 |

这些是风险排序示例，所有函数的结论均在 CSV 附录中。

## 6. SWE.4 软件单元验证

### 6.1 已有证据

- 本次运行：`tests/unit` 为 **412 passed，3 warnings，14.36s**。
- 测试覆盖主要算法、数据时效、报告事实/不变量、LLM schema、回测、归档和 UI helper。
- 代码和测试命名较清晰，便于后续建立追溯。

### 6.2 不符合/缺口

- 没有针对每个 software unit 的验证措施定义；缺 pass/fail、入口/出口、基础设施和环境要求。
- 没有记录静态分析、代码评审、边界值、等价类、故障注入等措施的选择准则。
- 无 release scope 到回归选择的证据。
- 646 个函数没有同名测试引用；其中可能存在间接覆盖，但仓库没有可证明的追溯关系。
- 没有覆盖率/分支覆盖证据，也没有说明为何当前覆盖对发布范围充分。
- `tests/run.py` 只输出终端结果，未生成持久化、可关联 HEAD/环境/用例版本的验证结果信息项。

### 6.3 判定

“测试通过”证明大量软件单元已被验证，不证明 SWE.4 的选择、充分性、双向追溯和结果管理已完成。

## 7. SWE.5 软件组件验证与集成验证

### 7.1 已有证据

- 存在 `tests/integration/test_coherence.py`、`test_pipeline.py`、`test_external_apis.py`。
- `tests/cases/catalog.yaml` 登记 12 条 integration 项。
- 架构文档描述了 Fetch→Analysis→Agents→Report→Archive 的主链路。

### 7.2 不符合/缺口

- 未定义软件元素集成顺序、前置条件、桩/模拟、接口兼容、数据流、时序/并发和资源目标。
- 集成验证措施没有与软件架构、详细设计接口双向追溯。
- 缺组件级验证和集成级验证的清晰分层。
- 外部 API 冒烟与确定性集成验证混在同一过程入口，发布门禁可能受网络和供应商时延影响。
- 本次 `--integration` 在 6 项通过后长时间未产生完整结果；因无法安全确认宿主 Python 进程归属，未强制终止。该现象作为未完成验证边界，不据此认定代码缺陷。

### 7.3 判定

存在实际集成验证活动，但 SWE.5 要求的计划化验证措施、架构/详细设计追溯和完整结果证据不足。

## 8. SWE.6 软件验证

### 8.1 已有证据

- 本次运行：`tests/regression` 为 **21 passed，4.44s**。
- 测试目录包含功能、金融、UI、性能、集成和回归场景。
- `docs/testing/strategy.md` 区分 fast/full/release 层级。

### 8.2 不符合/缺口

- 没有软件需求基线，因此测试不能证明从需求派生，也无法给出需求覆盖率。
- 116 条目录项中有 5 条缺 suite/automation 等关键属性；手工项未形成一致的执行结果记录。
- 测试用例常映射 FIN finding、旧 issue 或 UI ID，不是完整软件需求 ID。
- 无验证措施选择集、发布范围、回归准则、入口/出口和汇总沟通记录。
- GitHub Actions 只有 `docs.yml`，且仅对特定文档/少量源码路径运行 3 个文档回归测试；没有覆盖所有变更的 unit/regression 软件验证门禁。

### 8.3 判定

已有测试资产可复用，但当前无法从测试结果反向证明软件需求满足。

## 9. 支持与管理过程证据

| 过程 | 结论 | 证据与缺口 |
|---|---|---|
| SUP.1 质量保证 | P | 有 review、测试和 CI；但无独立 QA 计划、符合性检查、偏差处置和关闭证据 |
| SUP.8 配置管理 | P | Git 管理源码/文档；但无配置项清单、发布基线、状态记录；`requirements.txt` 使用版本范围而非可复现锁文件 |
| SUP.9 问题解决管理 | P/L | GitHub Issues 有严重度、证据、复现和验收，基础较好；仍缺统一 ASPICE 分类、状态/关闭准则和过程指标 |
| SUP.10 变更请求管理 | P | Git/Issue 能承载变更；缺需求影响分析、受影响追溯闭包、变更批准和发布范围证据 |
| MAN.3 项目管理 | P | roadmap 和 audit plan 有计划；缺以软件过程工作产品为对象的职责、里程碑、资源、监控和偏差管理 |

## 10. 审核发现与整改优先级

### ASPICE-01（P1）：缺软件需求基线及需求↔架构双向追溯

**影响过程**：SWE.1、SWE.2、SWE.6、SUP.10。
**根因**：项目以 roadmap、架构文档、测试目录和 Issue 代替需求工作产品。
**整改**：建立 `software-requirements.yaml/md`，为每条需求记录 ID、版本、来源、类型、优先级、状态、验证准则、运行环境影响、架构元素和验证措施；生成双向矩阵并在 CI 校验孤儿/悬挂链接。
**验收**：全部发布范围需求可追溯到至少一个架构元素和验证措施；反向不存在无依据实现/测试；变更能输出受影响闭包。

### ASPICE-02（P1）：缺软件单元/函数详细设计与代码一致性证据

**影响过程**：SWE.3、SWE.4。
**根因**：详细设计主要隐含在实现中，software unit 未定义。
**整改**：定义组件/单元分解和稳定 ID；优先为关键链路补充职责、输入输出、值域/量纲、前置/后置、异常、状态/并发、调用关系、需求/架构链接；由 AST 生成函数清单并校验设计漂移。
**验收**：1,013 个函数全部映射到软件单元；公开/关键内部单元拥有经评审详细设计；源代码与详细设计双向一致；高风险长函数完成拆分判定或保留理由。

### ASPICE-03（P1）：验证措施、需求/单元追溯和结果基线不完整

**影响过程**：SWE.4、SWE.5、SWE.6、SUP.1。
**根因**：测试以开发回归为中心，未建成基于 release scope 的验证工作产品。
**整改**：建立 verification measure/selection/result 模型；将 unit、component、integration、software verification 分层；每项记录 pass/fail、入口/出口、环境、版本、结果和缺陷；生成 `requirement↔test` 与 `unit↔test` 矩阵；全变更 CI 执行离线门禁并保存 JUnit/覆盖率。
**验收**：发布范围需求和软件单元有覆盖/豁免；结果绑定 HEAD、环境和用例版本；失败自动关联问题单；回归选择理由可复核。

### ASPICE-04（P2）：软件配置与文档基线不可完全复现

**影响过程**：SUP.8、SWE.2、SWE.5、SWE.6。
**根因**：依赖使用宽版本范围；架构导航有漂移；CI 只覆盖文档子集。
**整改**：定义配置项和发布基线，生成锁文件/SBOM，修复 `replay.py` 漂移引用，增加链接/符号/配置一致性检查，保存 release verification summary。
**验收**：从基线可复现安装和离线测试；不存在指向缺失文件/符号的权威文档；每次发布能列出配置项、版本和验证结果。

## 11. 建议实施顺序

1. 先建立需求 ID、架构元素 ID 和验证措施 ID 的最小信息模型；不要先批量补 docstring。
2. 对执行授权、数据时效、报告可信度、回测/仿真和外部数据边界建立首批端到端追溯链。
3. 用函数 CSV 生成 software unit 清单，按风险补详细设计；低风险 getter/format helper 可用模板和组件级设计覆盖，但必须保留明确映射。
4. 将现有 433 项通过的离线测试挂接到需求/单元，并补缺口；避免重复重写已有测试。
5. 拆分确定性 integration 与 live external smoke，建立可重复发布门禁和独立供应商健康检查。
6. 完成 SUP.8/SUP.10 后再申请正式预评估；否则文档会随代码继续漂移。

## 12. 验证记录与限制

### 12.1 本次执行

| 检查 | 结果 |
|---|---|
| `git fetch origin --prune` + 本地/远端比较 | `HEAD == origin/main == 6da1e0c` |
| 函数 AST 清单 | 179 文件，1,013 函数，生成 CSV/JSON 成功 |
| unit | 412 passed，3 Pandas 弃用 warnings |
| regression | 21 passed |
| integration | 6 项通过后未取得完整终态；不计为通过或失败 |
| 现有 GitHub Issue 去重 | 未发现覆盖 ASPICE 软件过程文档根因的现有 Issue；业务/报告可信度 Issue 不重复创建 |

### 12.2 限制

- 未访谈项目经理、开发、测试、QA 或利益相关方，无法验证文档是否在仓库外存在或是否被实际执行。
- 未检查组织级标准过程、培训、资源计划、供应商合同、评审会议纪要和发布审批。
- 未执行付费 LLM、MT5 下单或生产部署。
- 逐函数测试关联是保守的符号级静态证据；间接覆盖需在整改后的追溯矩阵中确认。
- 正式 Automotive SPICE 评估应由合格评估团队按约定 scope、sampling 和访谈证据实施。

## 13. 交付物

- 本报告：`docs/aspice/supporting/reviews/software-domain-document-audit-2026-07-17.md`
- 逐函数附录：`docs/aspice/supporting/reviews/software-function-audit-2026-07-17.csv`
- 机器摘要：`docs/aspice/supporting/reviews/software-function-audit-summary-2026-07-17.json`
- 可重复生成工具：`tests/tools/generate_aspice_function_audit.py`
