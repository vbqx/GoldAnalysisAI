# Automotive SPICE 软件域

这里是 GoldAnalysisAI 软件域的人工阅读、评审和变更入口。主文档全部采用 Markdown，
并按 Automotive SPICE 软件工程过程排列；CSV、YAML、JSON 和依赖锁仅作为自动校验附录，
集中存放在 [`_machine/`](./_machine/) 中。

## 推荐阅读路径

```text
SWE.1 软件需求
   ↓ requirement ID
SWE.2 软件架构
   ↓ architecture / interface ID
SWE.3 函数与详细设计
   ↓ software unit / function ID
SWE.4 单元测试（UT）
   ↓ integration item / test reference
SWE.5 集成测试（IT）
   ↓ verification measure / accepted result
SWE.6 验证测试（VT）
```

每个 ID 都是稳定链接锚点，可以从需求一路跳转到架构、模块、函数、详细设计和测试证据，
也可以从 UT/IT/VT 反向返回需求与设计。

## 软件域主文档

| 顺序 | 过程域 | 文档 | 主要内容 |
|---|---|---|---|
| 1 | SWE.1 | [软件需求分析](./SWE.1-software-requirements.md) | 26 条需求、来源、优先级、接受准则、架构与验证链接 |
| 2 | SWE.2 | [软件架构设计](./SWE.2-software-architecture.md) | 组件、运行模式、静态接口、动态行为和组件接口 |
| 3 | SWE.3 | [软件详细设计](./SWE.3-software-detailed-design.md) | 按组件 → 模块 → 函数组织的完整详细设计 |
| 4 | SWE.4 | [单元测试（UT）](./SWE.4-unit-testing.md) | 每个软件单元的风险、测试选择、动态测试和结果 |
| 5 | SWE.5 | [集成测试（IT）](./SWE.5-integration-testing.md) | 集成顺序、接口、桩、资源、超时、用例和结果 |
| 6 | SWE.6 | [验证测试（VT）](./SWE.6-validation-testing.md) | 验证策略、需求覆盖、接受结果和发布结论 |

跨过程查看：[需求—架构—验证双向追溯](./traceability.md)。

## 支撑与发布

- [软件配置管理](./SUP.8-configuration-management.md)
- [软件域范围与关闭准则](./supporting/software-domain-scope-and-closure.md)
- [最新验证结果](./verification-results/latest.md)
- [文档控制规则](./supporting/document-control.md)
- [软件域关闭审核报告](../reviews/aspice/software-domain-closure-review-2026-07-18.md)

## 维护规则

- 人工评审以本目录的 Markdown 主文档为准。
- `_machine/` 是同一证据的结构化镜像，用于 CI 一致性、双向追溯和数量校验。
- 函数设计来自受控源码 AST；修改业务函数后必须重新生成 SWE.3 和相关 UT 选择证据。
- `--write` 只更新 ASPICE 文档和机器附录，不修改 `src/`、`views/`、`app.py` 或 `run_app.py`。

```bash
python scripts/check_aspice_assets.py --write
python scripts/generate_aspice_software_evidence.py --write
python scripts/generate_aspice_readable_docs.py --write

python scripts/check_aspice_assets.py --check
python scripts/generate_aspice_software_evidence.py --check
python scripts/generate_aspice_readable_docs.py --check
```

关联问题单：[#39](https://github.com/vbqx/GoldAnalysisAI/issues/39)、
[#40](https://github.com/vbqx/GoldAnalysisAI/issues/40)、
[#41](https://github.com/vbqx/GoldAnalysisAI/issues/41)、
[#42](https://github.com/vbqx/GoldAnalysisAI/issues/42)。
