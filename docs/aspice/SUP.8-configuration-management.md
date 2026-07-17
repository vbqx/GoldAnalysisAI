# SUP.8 软件配置管理

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SUP.8 |
| 状态 | 受控基线 |
| 用途 | 评审配置项、变更控制、依赖和基线 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 基线

| 属性 | 内容 |
|---|---|
| 基线 ID | ASPICE-CM-2026-07-17 |
| 状态 | agreed |
| 发布引用 | refs/tags/aspice-software-domain-readable-baseline-2026-07-18 |
| 负责人角色 | configuration-manager |

## 变更控制

| 控制项 | 规则 |
|---|---|
| request_system | GitHub Issues and pull requests or reviewed direct commits |
| impact_analysis | requirement, architecture, unit, verification and document register trace closure |
| approval | project owner or delegated reviewer |
| status_accounting | Git history, GitHub Issue state, verification result record |

## 配置项

| ID | 路径 | 过程 |
|---|---|---|
| CI-SWR | docs/aspice/SWE.1-software-requirements.md | SWE.1 |
| CI-SAD | docs/aspice/SWE.2-software-architecture.md | SWE.2 |
| CI-SDD | docs/aspice/SWE.3-software-detailed-design.md | SWE.3 |
| CI-FUNCTION-MAP | docs/aspice/_machine/software-function-map.csv | SWE.3 |
| CI-FUNCTION-DESIGN | docs/aspice/_machine/software-function-detailed-design.csv | SWE.3 |
| CI-UNIT-VERIFICATION | docs/aspice/SWE.4-unit-testing.md | SWE.4 |
| CI-REQUIREMENT-VERIFICATION | docs/aspice/SWE.6-validation-testing.md | SWE.6 |
| CI-INTEGRATION-PLAN | docs/aspice/SWE.5-integration-testing.md | SWE.5 |
| CI-VERIFICATION | docs/aspice/SWE.6-validation-testing.md | SWE.4-SWE.6 |
| CI-TRACE | docs/aspice/traceability.md | SWE.1-SWE.6 |
| CI-DOC-REGISTER | docs/aspice/_machine/document-register.csv | SUP.8 |
| CI-SOURCE | src | SWE.3 |
| CI-TESTS | tests | SWE.4-SWE.6 |
| CI-RUNTIME-DEPS | docs/aspice/_machine/dependency-lock.txt | SUP.8 |
| CI-SBOM | docs/aspice/_machine/sbom.json | SUP.8 |
| CI-CONFIG-TEMPLATE | .env.example | SUP.8 |
| CI-ARCHIVE-SCHEMA | docs/reference/run-archive-schema.md | SWE.2 |
| CI-REPORT-SCHEMA | docs/reference/examples/report-schema.md | SWE.2 |
| CI-VERIFICATION-RESULT | docs/aspice/verification-results/latest.md | SWE.4-SWE.6 |
| CI-SOFTWARE-CLOSURE | docs/aspice/supporting/software-domain-scope-and-closure.md | SWE.1-SWE.6 |

## 依赖基线

锁定 **53 个依赖组件**。机器可校验的哈希、SBOM 和 pip 解析结果保存在 `_machine/`。

| 包 | 版本 |
|---|---|
| altair | 6.2.2 |
| anyio | 4.14.2 |
| attrs | 26.1.0 |
| blinker | 1.9.0 |
| cachetools | 7.1.4 |
| certifi | 2026.6.17 |
| charset-normalizer | 3.4.9 |
| click | 8.4.2 |
| colorama | 0.4.6 |
| gitdb | 4.0.12 |
| GitPython | 3.1.52 |
| h11 | 0.16.0 |
| httptools | 0.8.0 |
| idna | 3.18 |
| iniconfig | 2.3.0 |
| itsdangerous | 2.2.0 |
| Jinja2 | 3.1.6 |
| jsonschema | 4.26.0 |
| jsonschema-specifications | 2025.9.1 |
| MarkupSafe | 3.0.3 |
| narwhals | 2.24.0 |
| numpy | 2.5.1 |
| packaging | 26.2 |
| pandas | 2.3.3 |
| pillow | 12.3.0 |
| plotly | 6.9.0 |
| pluggy | 1.6.0 |
| protobuf | 7.35.1 |
| pyarrow | 24.0.0 |
| pydeck | 0.9.3 |
| Pygments | 2.20.0 |
| pytest | 9.1.1 |
| python-dateutil | 2.9.0.post0 |
| python-multipart | 0.0.32 |
| pytz | 2026.2 |
| PyYAML | 6.0.3 |
| referencing | 0.37.0 |
| requests | 2.34.2 |
| rpds-py | 2026.6.3 |
| six | 1.17.0 |
| smmap | 5.0.3 |
| starlette | 1.3.1 |
| streamlit | 1.59.2 |
| tenacity | 9.1.4 |
| toml | 0.10.2 |
| tvdatafeed-enhanced | 2.2.1 |
| typing_extensions | 4.16.0 |
| tzdata | 2026.3 |
| urllib3 | 2.7.0 |
| uvicorn | 0.51.0 |
| watchdog | 6.0.0 |
| websocket-client | 1.9.0 |
| websockets | 16.1 |
