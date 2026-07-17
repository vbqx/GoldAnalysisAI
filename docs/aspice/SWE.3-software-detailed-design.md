# SWE.3 软件详细设计

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 在一个文档内按组件、模块和函数阅读完整详细设计 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

## 阅读方式

一个 Python 模块对应一个 software unit。本文件按组件、模块、函数三级组织；目录链接使用稳定 ID。

当前覆盖 **182 个软件单元**。全部函数详细设计均在本文件内，SWE.4 汇总 UT 选择与结果。

### 全部函数的共同契约

- 前置条件：调用方满足函数签名、所属单元状态和关联需求约束。
- 后置条件：正常返回满足返回契约；副作用不得超出函数卡片记录的类别。
- 未单列运行约束时，默认值为：显式异常 `none-explicit`、副作用 `none-detected`、并发 `caller-thread`；这不代表底层依赖绝不会抛出异常。


<a id="arc-app"></a>

## ARC-APP — 应用入口与运行配置

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [app.py](#unit-13cce7fd07) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [run_app.py](#unit-b2a1584dad) | 13 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/1_机构级分析报告.py](#unit-02d5d8e12e) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/2_短线策略.py](#unit-0e03ccecca) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/3_LLM决策链.py](#unit-74cd83898f) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/4_外部数据.py](#unit-1fe6319d7a) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |

<a id="unit-13cce7fd07"></a>

### app.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-13CCE7FD07 |
| 源码 | [app.py](../../app.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | GoldAnalysisAI — Streamlit 入口（纯导航，不显示为侧边栏页面）。 |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[_ensure_streamlit_runtime](#fun-188c32a8d7)

<a id="fun-188c32a8d7"></a>

#### `_ensure_streamlit_runtime`

- **ID / 行**：`FUN-188C32A8D7` / `L29`（源码见本单元概览）
- **签名 / 返回**：`_ensure_streamlit_runtime()` → `None`
- **职责**：Block `python app.py` — Streamlit must host this file.
- **异常 / 副作用 / 并发**：SystemExit / none-detected / caller-thread
- **依赖**：SystemExit、get_script_run_ctx、print
- **复杂度 / 风险**：分支 2；跨度 17 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-b2a1584dad"></a>

### run_app.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B2A1584DAD |
| 源码 | [run_app.py](../../run_app.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | GoldAnalysisAI cross-platform launcher (Windows + Linux + macOS). |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 13 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[load_dotenv](#fun-dccdace066) · [init_dev_env](#fun-79cfc89b7c) · [ensure_streamlit_config](#fun-acd09c876b) · [_python_is_usable](#fun-8991377fd4) · [resolve_python](#fun-50c4f81dd9) · [_pids_listening_on_port](#fun-40c14bb01b) · [_command_line_for_pid](#fun-efea1102a6) · [_is_project_streamlit_pid](#fun-5f95c44360) · [_streamlit_pids](#fun-e5e889737f) · [_terminate_pid](#fun-2f41b39115) · [stop_stale_streamlit](#fun-93afb64487) · [parse_args](#fun-5749848613) · [main](#fun-8c169563e6)

<a id="fun-dccdace066"></a>

#### `load_dotenv`

- **ID / 行**：`FUN-DCCDACE066` / `L27`（源码见本单元概览）
- **签名 / 返回**：`load_dotenv(path: Path)` → `None`
- **职责**：As-built responsibility derived from `load_dotenv` and its owning unit.
- **依赖**：key.strip、len、line.split、line.startswith、path.is_file、path.read_text、print、raw.strip、splitlines、val.strip
- **复杂度 / 风险**：分支 4；跨度 15 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-79cfc89b7c"></a>

#### `init_dev_env`

- **ID / 行**：`FUN-79CFC89B7C` / `L44`（源码见本单元概览）
- **签名 / 返回**：`init_dev_env()` → `None`
- **职责**：As-built responsibility derived from `init_dev_env` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：os.environ.setdefault
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-acd09c876b"></a>

#### `ensure_streamlit_config`

- **ID / 行**：`FUN-ACD09C876B` / `L51`（源码见本单元概览）
- **签名 / 返回**：`ensure_streamlit_config()` → `None`
- **职责**：As-built responsibility derived from `ensure_streamlit_config` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：cfg_dir.mkdir、config_path.is_file、config_path.write_text、cred_path.is_file、cred_path.write_text
- **复杂度 / 风险**：分支 2；跨度 15 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8991377fd4"></a>

#### `_python_is_usable`

- **ID / 行**：`FUN-8991377FD4` / `L68`（源码见本单元概览）
- **签名 / 返回**：`_python_is_usable(candidate: Path)` → `bool`
- **职责**：As-built responsibility derived from `_python_is_usable` and its owning unit.
- **依赖**：str、subprocess.run
- **复杂度 / 风险**：分支 1；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-50c4f81dd9"></a>

#### `resolve_python`

- **ID / 行**：`FUN-50C4F81DD9` / `L82`（源码见本单元概览）
- **签名 / 返回**：`resolve_python()` → `Path | str`
- **职责**：As-built responsibility derived from `resolve_python` and its owning unit.
- **依赖**：_python_is_usable、candidate.is_file
- **复杂度 / 风险**：分支 3；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-40c14bb01b"></a>

#### `_pids_listening_on_port`

- **ID / 行**：`FUN-40C14BB01B` / `L90`（源码见本单元概览）
- **签名 / 返回**：`_pids_listening_on_port(port: int)` → `list[int]`
- **职责**：As-built responsibility derived from `_pids_listening_on_port` and its owning unit.
- **依赖**：int、line.split、line.upper、os.getpid、out.split、out.splitlines、pids.append、subprocess.check_output、token.isdigit
- **复杂度 / 风险**：分支 13；跨度 42 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-efea1102a6"></a>

#### `_command_line_for_pid`

- **ID / 行**：`FUN-EFEA1102A6` / `L134`（源码见本单元概览）
- **签名 / 返回**：`_command_line_for_pid(pid: int)` → `str`
- **职责**：As-built responsibility derived from `_command_line_for_pid` and its owning unit.
- **依赖**：str、strip、subprocess.check_output
- **复杂度 / 风险**：分支 3；跨度 25 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5f95c44360"></a>

#### `_is_project_streamlit_pid`

- **ID / 行**：`FUN-5F95C44360` / `L161`（源码见本单元概览）
- **签名 / 返回**：`_is_project_streamlit_pid(pid: int, root: Path)` → `bool`
- **职责**：As-built responsibility derived from `_is_project_streamlit_pid` and its owning unit.
- **依赖**：_command_line_for_pid、lower、str
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e5e889737f"></a>

#### `_streamlit_pids`

- **ID / 行**：`FUN-E5E889737F` / `L169`（源码见本单元概览）
- **签名 / 返回**：`_streamlit_pids(root: Path)` → `list[int]`
- **职责**：As-built responsibility derived from `_streamlit_pids` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：chr、int、line.isdigit、line.strip、lower、os.getpid、out.splitlines、pids.append、root_marker.replace、str、subprocess.check_output
- **复杂度 / 风险**：分支 9；跨度 46 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2f41b39115"></a>

#### `_terminate_pid`

- **ID / 行**：`FUN-2F41B39115` / `L217`（源码见本单元概览）
- **签名 / 返回**：`_terminate_pid(pid: int)` → `None`
- **职责**：As-built responsibility derived from `_terminate_pid` and its owning unit.
- **依赖**：os.kill、str、subprocess.run
- **复杂度 / 风险**：分支 3；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-93afb64487"></a>

#### `stop_stale_streamlit`

- **ID / 行**：`FUN-93AFB64487` / `L235`（源码见本单元概览）
- **签名 / 返回**：`stop_stale_streamlit(port: int)` → `None`
- **职责**：As-built responsibility derived from `stop_stale_streamlit` and its owning unit.
- **依赖**：_is_project_streamlit_pid、_pids_listening_on_port、_terminate_pid、print、targets.append
- **复杂度 / 风险**：分支 4；跨度 16 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5749848613"></a>

#### `parse_args`

- **ID / 行**：`FUN-5749848613` / `L253`（源码见本单元概览）
- **签名 / 返回**：`parse_args()` → `argparse.Namespace`
- **职责**：As-built responsibility derived from `parse_args` and its owning unit.
- **依赖**：argparse.ArgumentParser、parser.add_argument、parser.parse_args
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8c169563e6"></a>

#### `main`

- **ID / 行**：`FUN-8C169563E6` / `L264`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：ensure_streamlit_config、init_dev_env、int、load_dotenv、os.chdir、os.environ.get、parse_args、print、resolve_python、stop_stale_streamlit、str、subprocess.call、subprocess.run
- **复杂度 / 风险**：分支 4；跨度 49 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-02d5d8e12e"></a>

### views/1_机构级分析报告.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-02D5D8E12E |
| 源码 | [views/1_机构级分析报告.py](../../views/1_机构级分析报告.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 机构级分析报告 — 主页面。 |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-0e03ccecca"></a>

### views/2_短线策略.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0E03CCECCA |
| 源码 | [views/2_短线策略.py](../../views/2_短线策略.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 短线策略图 — 独立页面。 |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-74cd83898f"></a>

### views/3_LLM决策链.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-74CD83898F |
| 源码 | [views/3_LLM决策链.py](../../views/3_LLM决策链.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | LLM 决策链 — 独立页面。 |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-1fe6319d7a"></a>

### views/4_外部数据.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1FE6319D7A |
| 源码 | [views/4_外部数据.py](../../views/4_外部数据.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 外部数据 — 新闻、日历、DXY、社媒；fetch 完成后即可查看。 |
| 关联需求 | [SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="arc-core"></a>

## ARC-CORE — 主编排与进度

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/__init__.py](#unit-b141e8a708) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/config.py](#unit-f43788fe2b) | 5 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/__init__.py](#unit-21570b9deb) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/orchestrator.py](#unit-aa59bf5421) | 1 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/orchestrator_hooks.py](#unit-d0bec20560) | 4 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/parallel.py](#unit-d85010dca2) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/progress.py](#unit-0dc607ab64) | 31 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/run_config.py](#unit-4bd152d87b) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/run_context.py](#unit-338f795d63) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/core/types.py](#unit-d5eb6e2a98) | 21 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/log.py](#unit-a91501b8ca) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/pipeline.py](#unit-ba3f06e87a) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-b141e8a708"></a>

### src/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B141E8A708 |
| 源码 | [src/__init__.py](../../src/__init__.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | TradingAgentCN - XAUUSD PA+ICT Analysis MVP. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-f43788fe2b"></a>

### src/config.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F43788FE2B |
| 源码 | [src/config.py](../../src/config.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Application configuration from environment variables. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 5 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) |
| 验证状态 | selected |

#### 函数导航

[_load_dotenv](#fun-f4d8ffcbf2) · [short_model_name](#fun-9eb4bec26a) · [llm_sidebar_models](#fun-9f79e7b13e) · [_stage_flag](#fun-d31153bd15) · [_stage_flag_or](#fun-09dea713ba)

<a id="fun-f4d8ffcbf2"></a>

#### `_load_dotenv`

- **ID / 行**：`FUN-F4D8FFCBF2` / `L9`（源码见本单元概览）
- **签名 / 返回**：`_load_dotenv()` → `None`
- **职责**：As-built responsibility derived from `_load_dotenv` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：Path、env_path.exists、env_path.read_text、key.strip、line.split、line.startswith、line.strip、os.environ.setdefault、resolve、splitlines、val.strip
- **复杂度 / 风险**：分支 3；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9eb4bec26a"></a>

#### `short_model_name`

- **ID / 行**：`FUN-9EB4BEC26A` / `L138`（源码见本单元概览）
- **签名 / 返回**：`short_model_name(model: str)` → `str`
- **职责**：As-built responsibility derived from `short_model_name` and its owning unit.
- **依赖**：model.split
- **复杂度 / 风险**：分支 1；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9f79e7b13e"></a>

#### `llm_sidebar_models`

- **ID / 行**：`FUN-9F79E7B13E` / `L142`（源码见本单元概览）
- **签名 / 返回**：`llm_sidebar_models()` → `str`
- **职责**：Sidebar caption: show actual fast/strong models from .env.
- **依赖**：join、parts.append、short_model_name
- **复杂度 / 风险**：分支 2；跨度 15 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) · direct-dynamic

<a id="fun-d31153bd15"></a>

#### `_stage_flag`

- **ID / 行**：`FUN-D31153BD15` / `L159`（源码见本单元概览）
- **签名 / 返回**：`_stage_flag(name: str)` → `bool`
- **职责**：As-built responsibility derived from `_stage_flag` and its owning unit.
- **依赖**：lower、os.getenv
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-09dea713ba"></a>

#### `_stage_flag_or`

- **ID / 行**：`FUN-09DEA713BA` / `L174`（源码见本单元概览）
- **签名 / 返回**：`_stage_flag_or(name: str, default: bool)` → `bool`
- **职责**：As-built responsibility derived from `_stage_flag_or` and its owning unit.
- **依赖**：_stage_flag
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-21570b9deb"></a>

### src/core/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-21570B9DEB |
| 源码 | [src/core/__init__.py](../../src/core/__init__.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | 继承 主编排与进度 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-aa59bf5421"></a>

### src/core/orchestrator.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-AA59BF5421 |
| 源码 | [src/core/orchestrator.py](../../src/core/orchestrator.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | TradeAgent-style orchestrator — data → research → trade → risk → manager → report. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) |
| 验证状态 | selected |

#### 函数导航

[run_trade_agent_pipeline](#fun-67d665990e)

<a id="fun-67d665990e"></a>

#### `run_trade_agent_pipeline`

- **ID / 行**：`FUN-67D665990E` / `L46`（源码见本单元概览）
- **签名 / 返回**：`run_trade_agent_pipeline()` → `tuple[dict, dict, dict]`
- **职责**：End-to-end pipeline mirroring TradeAgent flow:
- **异常 / 副作用 / 并发**：none-explicit / external-io;shared-state / caller-thread
- **依赖**：AgentPipelineMeta、AgentTrace、LLMAnalysis、StageMeta、abs、agent_factory.research_uses_parallel_llm、agent_factory.run_analyst_team、agent_factory.run_bearish、agent_factory.run_bullish、agent_factory.run_debate、agent_factory.run_level_proposer、agent_factory.run_manager、agent_factory.run_research_team、agent_factory.run_risk、agent_factory.run_trader、agent_mode、align_conclusion_with_manager_decision、analyses.items、analyst_team.to_dict、analyze_timeframe
- **复杂度 / 风险**：分支 20；跨度 371 行；high
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="unit-d0bec20560"></a>

### src/core/orchestrator_hooks.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D0BEC20560 |
| 源码 | [src/core/orchestrator_hooks.py](../../src/core/orchestrator_hooks.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Small hooks extracted from orchestrator for readability and testing. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 4 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) |
| 验证状态 | selected |

#### 函数导航

[begin_pipeline_run](#fun-dd1340f890) · [fetch_market_data](#fun-06f77b71cb) · [publish_external_snapshot](#fun-d2656c49ea) · [finalize_pipeline_archive](#fun-e9ab4f388f)

<a id="fun-dd1340f890"></a>

#### `begin_pipeline_run`

- **ID / 行**：`FUN-DD1340F890` / `L15`（源码见本单元概览）
- **签名 / 返回**：`begin_pipeline_run()` → `tuple[str, float]`
- **职责**：As-built responsibility derived from `begin_pipeline_run` and its owning unit.
- **依赖**：allocate_run_id、log.info、set_current_run_id、time.perf_counter
- **复杂度 / 风险**：分支 0；跨度 7 行；high
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="fun-06f77b71cb"></a>

#### `fetch_market_data`

- **ID / 行**：`FUN-06F77B71CB` / `L24`（源码见本单元概览）
- **签名 / 返回**：`fetch_market_data()` → `DataFetchResult`
- **职责**：As-built responsibility derived from `fetch_market_data` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：fetch_all_data
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="fun-d2656c49ea"></a>

#### `publish_external_snapshot`

- **ID / 行**：`FUN-D2656C49EA` / `L28`（源码见本单元概览）
- **签名 / 返回**：`publish_external_snapshot(fetched: DataFetchResult, prog: Any)` → `None`
- **职责**：As-built responsibility derived from `publish_external_snapshot` and its owning unit.
- **依赖**：external_snapshot_from_fetch、prog.set_external_snapshot
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="fun-e9ab4f388f"></a>

#### `finalize_pipeline_archive`

- **ID / 行**：`FUN-E9AB4F388F` / `L34`（源码见本单元概览）
- **签名 / 返回**：`finalize_pipeline_archive(run_id: str, *, fetched: DataFetchResult, report: dict[str, Any], enriched: dict, analyses: dict, elapsed_s: float, run_config: RunConfig | None=None)` → `None`
- **职责**：As-built responsibility derived from `finalize_pipeline_archive` and its owning unit.
- **依赖**：archive_run、get_run_config、normalized
- **复杂度 / 风险**：分支 0；跨度 20 行；high
- **测试 / 验证**：[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="unit-d85010dca2"></a>

### src/core/parallel.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D85010DCA2 |
| 源码 | [src/core/parallel.py](../../src/core/parallel.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Thread-pool helpers with ContextVar propagation for pipeline parallelism. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_parallel.py](../../tests/unit/test_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[ParallelTaskError.__init__](#fun-121ea3a282) · [run_parallel](#fun-f68413bb73) · [run_parallel._run](#fun-554230efc2)

<a id="fun-121ea3a282"></a>

#### `ParallelTaskError.__init__`

- **ID / 行**：`FUN-121EA3A282` / `L20`（源码见本单元概览）
- **签名 / 返回**：`ParallelTaskError.__init__(self, errors: dict[str, BaseException])` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **依赖**：__init__、join、sorted、super
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-f68413bb73"></a>

#### `run_parallel`

- **ID / 行**：`FUN-F68413BB73` / `L26`（源码见本单元概览）
- **签名 / 返回**：`run_parallel(tasks: list[tuple[str, Callable[[], T]]], *, max_workers: int, label: str='', raise_on_error: bool=False)` → `dict[str, T]`
- **职责**：Run independent callables in a thread pool.
- **异常 / 副作用 / 并发**：ParallelTaskError / none-detected / caller-thread
- **依赖**：ParallelTaskError、ThreadPoolExecutor、as_completed、contextvars.copy_context、fn、future.result、len、log.warning、max、min、pool.submit、worker_ctx.run
- **复杂度 / 风险**：分支 7；跨度 49 行；medium
- **测试 / 验证**：[tests/unit/test_parallel.py](../../tests/unit/test_parallel.py) · direct-dynamic

<a id="fun-554230efc2"></a>

#### `run_parallel._run`

- **ID / 行**：`FUN-554230EFC2` / `L46`（源码见本单元概览）
- **签名 / 返回**：`run_parallel._run(name: str, fn: Callable[[], T], worker_ctx: contextvars.Context)` → `tuple[str, T | None, BaseException | None]`
- **职责**：As-built responsibility derived from `_run` and its owning unit.
- **依赖**：worker_ctx.run
- **复杂度 / 风险**：分支 1；跨度 9 行；low
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="unit-0dc607ab64"></a>

### src/core/progress.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0DC607AB64 |
| 源码 | [src/core/progress.py](../../src/core/progress.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Pipeline progress reporting — contextvar + noop for non-UI callers. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 31 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_coherence.py](../../tests/integration/test_coherence.py)、[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/regression/test_doc_pipeline_sync.py](../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_live_progress_ui.py](../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) |
| 验证状态 | selected |

#### 函数导航

[PipelineProgressState.to_dict](#fun-e6e1bb921a) · [LLMIORecord.to_dict](#fun-15a8181c39) · [ProgressReporter.__init__](#fun-cb609da8dc) · [ProgressReporter.set_external_snapshot](#fun-71a259922f) · [ProgressReporter.start](#fun-ef0ac17bf3) · [ProgressReporter.start_sibling](#fun-a57d337b7d) · [ProgressReporter.update](#fun-f4408a209b) · [ProgressReporter.done](#fun-5e62a87f3a) · [ProgressReporter.fail](#fun-59b596d460) · [ProgressReporter.skip](#fun-1f365c723b) · [ProgressReporter.snapshot](#fun-40fa2599e6) · [ProgressReporter.llm_io_snapshot](#fun-0cb129ff59) · [ProgressReporter.stage_io](#fun-2b8326fbcd) · [ProgressReporter.llm_begin](#fun-776ea31038) · [ProgressReporter.llm_note_attempt](#fun-326c939089) · [ProgressReporter.run_llm_stream](#fun-5665b88765) · [ProgressReporter.llm_end](#fun-7ac82003df) · [ProgressReporter._new_llm_record](#fun-c39210a2c9) · [ProgressReporter._apply_telemetry](#fun-b1d16223b8) · [ProgressReporter._find_llm](#fun-46d50ce2f3) · [ProgressReporter._on_llm_begin](#fun-e72e9180d4) · [ProgressReporter._on_llm_chunk](#fun-f3e1b56237) · [ProgressReporter._on_llm_end](#fun-2246070cd9) · [ProgressReporter._find](#fun-56d0f4ca20) · [ProgressReporter._finish_all_running](#fun-473e5d3fd6) · [ProgressReporter._finish_running](#fun-d1368ea00b) · [ProgressReporter._elapsed_since_step_start](#fun-592ed31999) · [ProgressReporter._on_change](#fun-5a6a8e27cf) · [get_progress](#fun-ec9d010cf8) · [set_progress](#fun-6b37902476) · [reset_progress](#fun-f2934a14dd)

<a id="fun-e6e1bb921a"></a>

#### `PipelineProgressState.to_dict`

- **ID / 行**：`FUN-E6E1BB921A` / `L29`（源码见本单元概览）
- **签名 / 返回**：`PipelineProgressState.to_dict(self)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 11 行；high
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-15a8181c39"></a>

#### `LLMIORecord.to_dict`

- **ID / 行**：`FUN-15A8181C39` / `L66`（源码见本单元概览）
- **签名 / 返回**：`LLMIORecord.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：list
- **复杂度 / 风险**：分支 0；跨度 23 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-cb609da8dc"></a>

#### `ProgressReporter.__init__`

- **ID / 行**：`FUN-CB609DA8DC` / `L109`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.__init__(self)` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：PipelineProgressState、threading.RLock
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-71a259922f"></a>

#### `ProgressReporter.set_external_snapshot`

- **ID / 行**：`FUN-71A259922F` / `L115`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.set_external_snapshot(self, data: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `set_external_snapshot` and its owning unit.
- **依赖**：self._on_change
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="fun-ef0ac17bf3"></a>

#### `ProgressReporter.start`

- **ID / 行**：`FUN-EF0AC17BF3` / `L119`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.start(self, step_id: str, label: str, detail: str='')` → `None`
- **职责**：As-built responsibility derived from `start` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：PipelineProgressStep、self._finish_all_running、self._on_change、self.state.steps.append、time.perf_counter
- **复杂度 / 风险**：分支 0；跨度 7 行；medium
- **测试 / 验证**：[tests/regression/test_doc_pipeline_sync.py](../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="fun-a57d337b7d"></a>

#### `ProgressReporter.start_sibling`

- **ID / 行**：`FUN-A57D337B7D` / `L127`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.start_sibling(self, step_id: str, label: str, detail: str='')` → `None`
- **职责**：Mark an additional step running without finishing other running steps.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：PipelineProgressStep、self._on_change、self.state.steps.append、time.perf_counter
- **复杂度 / 风险**：分支 0；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py) · direct-dynamic

<a id="fun-f4408a209b"></a>

#### `ProgressReporter.update`

- **ID / 行**：`FUN-F4408A209B` / `L135`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.update(self, step_id: str, *, detail: str | None=None, label: str | None=None)` → `None`
- **职责**：As-built responsibility derived from `update` and its owning unit.
- **依赖**：self._find、self._on_change
- **复杂度 / 风险**：分支 3；跨度 9 行；medium
- **测试 / 验证**：[tests/regression/test_doc_pipeline_sync.py](../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py) · direct-dynamic

<a id="fun-5e62a87f3a"></a>

#### `ProgressReporter.done`

- **ID / 行**：`FUN-5E62A87F3A` / `L145`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.done(self, step_id: str, detail: str='')` → `None`
- **职责**：As-built responsibility derived from `done` and its owning unit.
- **依赖**：self._elapsed_since_step_start、self._find、self._on_change
- **复杂度 / 风险**：分支 2；跨度 9 行；medium
- **测试 / 验证**：[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_live_progress_ui.py](../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-59b596d460"></a>

#### `ProgressReporter.fail`

- **ID / 行**：`FUN-59B596D460` / `L155`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.fail(self, step_id: str, detail: str='')` → `None`
- **职责**：As-built responsibility derived from `fail` and its owning unit.
- **依赖**：self._elapsed_since_step_start、self._find、self._on_change
- **复杂度 / 风险**：分支 1；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py) · direct-dynamic

<a id="fun-1f365c723b"></a>

#### `ProgressReporter.skip`

- **ID / 行**：`FUN-1F365C723B` / `L164`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.skip(self, step_id: str, label: str, detail: str='')` → `None`
- **职责**：As-built responsibility derived from `skip` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：PipelineProgressStep、self._on_change、self.state.steps.append
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：[tests/integration/test_coherence.py](../../tests/integration/test_coherence.py)、[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="fun-40fa2599e6"></a>

#### `ProgressReporter.snapshot`

- **ID / 行**：`FUN-40FA2599E6` / `L170`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.snapshot(self)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `snapshot` and its owning unit.
- **依赖**：self.state.to_dict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/integration/test_coherence.py](../../tests/integration/test_coherence.py)、[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="fun-0cb129ff59"></a>

#### `ProgressReporter.llm_io_snapshot`

- **ID / 行**：`FUN-0CB129FF59` / `L173`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.llm_io_snapshot(self)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `llm_io_snapshot` and its owning unit.
- **依赖**：r.to_dict
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-2b8326fbcd"></a>

#### `ProgressReporter.stage_io`

- **ID / 行**：`FUN-2B8326FBCD` / `L177`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.stage_io(self, stage: str, *, input_text: str, output_text: str, latency_ms: int | None=None, label: str | None=None)` → `None`
- **职责**：Record rule-based stage input/output for the generation I/O panel.
- **依赖**：LLMIORecord、STAGE_LABELS.get、self.llm_io.append
- **复杂度 / 风险**：分支 0；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-776ea31038"></a>

#### `ProgressReporter.llm_begin`

- **ID / 行**：`FUN-776EA31038` / `L201`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], *, telemetry: dict[str, Any] | None=None)` → `None`
- **职责**：As-built responsibility derived from `llm_begin` and its owning unit.
- **依赖**：STAGE_LABELS.get、bool、list、self._apply_telemetry、self._find_llm、self._new_llm_record、self._on_llm_begin、self.llm_io.append、tel.get
- **复杂度 / 风险**：分支 2；跨度 29 行；medium
- **测试 / 验证**：[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-326c939089"></a>

#### `ProgressReporter.llm_note_attempt`

- **ID / 行**：`FUN-326C939089` / `L231`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.llm_note_attempt(self, stage: str, *, attempt: int, reason: str, error: str | None=None, latency_ms: int | None=None)` → `None`
- **职责**：As-built responsibility derived from `llm_note_attempt` and its owning unit.
- **依赖**：rec.attempts.append、self._find_llm
- **复杂度 / 风险**：分支 1；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5665b88765"></a>

#### `ProgressReporter.run_llm_stream`

- **ID / 行**：`FUN-5665B88765` / `L254`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.run_llm_stream(self, stage: str, chunk_iter)` → `str`
- **职责**：Consume streamed chunks; Streamlit subclass uses st.write_stream.
- **依赖**：join、parts.append、self._on_llm_chunk
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-7ac82003df"></a>

#### `ProgressReporter.llm_end`

- **ID / 行**：`FUN-7AC82003DF` / `L262`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter.llm_end(self, stage: str, output: str, *, error: str | None=None, latency_ms: int | None=None, telemetry: dict[str, Any] | None=None)` → `None`
- **职责**：As-built responsibility derived from `llm_end` and its owning unit.
- **依赖**：estimate_text_size、self._apply_telemetry、self._find_llm、self._on_llm_end、telemetry.get
- **复杂度 / 风险**：分支 3；跨度 25 行；medium
- **测试 / 验证**：[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-c39210a2c9"></a>

#### `ProgressReporter._new_llm_record`

- **ID / 行**：`FUN-C39210A2C9` / `L288`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._new_llm_record(self, stage: str, label: str, model: str, messages: list[dict[str, str]], tel: dict[str, Any])` → `LLMIORecord`
- **职责**：As-built responsibility derived from `_new_llm_record` and its owning unit.
- **依赖**：LLMIORecord、list、self._apply_telemetry
- **复杂度 / 风险**：分支 0；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b1d16223b8"></a>

#### `ProgressReporter._apply_telemetry`

- **ID / 行**：`FUN-B1D16223B8` / `L301`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._apply_telemetry(rec: LLMIORecord, tel: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `_apply_telemetry` and its owning unit.
- **依赖**：int、str
- **复杂度 / 风险**：分支 11；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-46d50ce2f3"></a>

#### `ProgressReporter._find_llm`

- **ID / 行**：`FUN-46D50CE2F3` / `L325`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._find_llm(self, stage: str)` → `LLMIORecord | None`
- **职责**：As-built responsibility derived from `_find_llm` and its owning unit.
- **依赖**：reversed
- **复杂度 / 风险**：分支 2；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e72e9180d4"></a>

#### `ProgressReporter._on_llm_begin`

- **ID / 行**：`FUN-E72E9180D4` / `L331`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str)` → `None`
- **职责**：As-built responsibility derived from `_on_llm_begin` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f3e1b56237"></a>

#### `ProgressReporter._on_llm_chunk`

- **ID / 行**：`FUN-F3E1B56237` / `L334`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._on_llm_chunk(self, stage: str, chunk: str)` → `None`
- **职责**：As-built responsibility derived from `_on_llm_chunk` and its owning unit.
- **依赖**：self._find_llm
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-2246070cd9"></a>

#### `ProgressReporter._on_llm_end`

- **ID / 行**：`FUN-2246070CD9` / `L340`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._on_llm_end(self, stage: str, output: str, *, error: str | None=None)` → `None`
- **职责**：As-built responsibility derived from `_on_llm_end` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-56d0f4ca20"></a>

#### `ProgressReporter._find`

- **ID / 行**：`FUN-56D0F4CA20` / `L343`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._find(self, step_id: str)` → `PipelineProgressStep | None`
- **职责**：As-built responsibility derived from `_find` and its owning unit.
- **依赖**：reversed
- **复杂度 / 风险**：分支 2；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-473e5d3fd6"></a>

#### `ProgressReporter._finish_all_running`

- **ID / 行**：`FUN-473E5D3FD6` / `L349`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._finish_all_running(self)` → `None`
- **职责**：As-built responsibility derived from `_finish_all_running` and its owning unit.
- **依赖**：self._elapsed_since_step_start
- **复杂度 / 风险**：分支 2；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d1368ea00b"></a>

#### `ProgressReporter._finish_running`

- **ID / 行**：`FUN-D1368EA00B` / `L355`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._finish_running(self)` → `None`
- **职责**：As-built responsibility derived from `_finish_running` and its owning unit.
- **依赖**：reversed、self._elapsed_since_step_start
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-592ed31999"></a>

#### `ProgressReporter._elapsed_since_step_start`

- **ID / 行**：`FUN-592ED31999` / `L362`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._elapsed_since_step_start(self, step: PipelineProgressStep)` → `int | None`
- **职责**：As-built responsibility derived from `_elapsed_since_step_start` and its owning unit.
- **依赖**：int、time.perf_counter
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5a6a8e27cf"></a>

#### `ProgressReporter._on_change`

- **ID / 行**：`FUN-5A6A8E27CF` / `L367`（源码见本单元概览）
- **签名 / 返回**：`ProgressReporter._on_change(self)` → `None`
- **职责**：As-built responsibility derived from `_on_change` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ec9d010cf8"></a>

#### `get_progress`

- **ID / 行**：`FUN-EC9D010CF8` / `L378`（源码见本单元概览）
- **签名 / 返回**：`get_progress()` → `ProgressReporter`
- **职责**：As-built responsibility derived from `get_progress` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_progress_ctx.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-6b37902476"></a>

#### `set_progress`

- **ID / 行**：`FUN-6B37902476` / `L382`（源码见本单元概览）
- **签名 / 返回**：`set_progress(reporter: ProgressReporter | None)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `set_progress` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_progress_ctx.set
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="fun-f2934a14dd"></a>

#### `reset_progress`

- **ID / 行**：`FUN-F2934A14DD` / `L386`（源码见本单元概览）
- **签名 / 返回**：`reset_progress(token)` → `None`
- **职责**：As-built responsibility derived from `reset_progress` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_progress_ctx.reset
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="unit-4bd152d87b"></a>

### src/core/run_config.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4BD152D87B |
| 源码 | [src/core/run_config.py](../../src/core/run_config.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Backward-compatible re-export — prefer ``src.run.config`` or ``src.run``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-338f795d63"></a>

### src/core/run_context.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-338F795D63 |
| 源码 | [src/core/run_context.py](../../src/core/run_context.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Backward-compatible re-export — prefer ``src.run.context`` or ``src.run``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-d5eb6e2a98"></a>

### src/core/types.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D5EB6E2A98 |
| 源码 | [src/core/types.py](../../src/core/types.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Shared types for the TradeAgent-style pipeline. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 21 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_coherence.py](../../tests/integration/test_coherence.py)、[tests/regression/test_docs_structure.py](../../tests/regression/test_docs_structure.py)、[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_coherence.py](../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_context_compact.py](../../tests/unit/test_llm_context_compact.py)、[tests/unit/test_llm_context_fact_refs.py](../../tests/unit/test_llm_context_fact_refs.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py)、[tests/unit/test_risk_gates_trigger.py](../../tests/unit/test_risk_gates_trigger.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[AnalystReport.to_dict](#fun-1a5c4973e8) · [AnalystTeam.reports](#fun-11d5edef39) · [AnalystTeam.to_dict](#fun-d1937786ae) · [AgentEvidence.to_dict](#fun-3104427770) · [ResearchDebate.to_dict](#fun-378c040696) · [LevelProposal.to_dict](#fun-78898fe309) · [TransactionProposal.to_dict](#fun-cbd371affe) · [RiskReview.to_dict](#fun-1d042f655d) · [ManagerDecision.to_dict](#fun-f763a5c226) · [HeadlineItem.to_dict](#fun-1f2e0f588a) · [CalendarEvent.to_dict](#fun-5a0e6a3977) · [CalendarEvent.display](#fun-4654e9b6a5) · [MacroQuote.to_dict](#fun-0b81375e45) · [ExternalFactors.to_dict](#fun-b52c340615) · [MarketContext.to_dict](#fun-6449e7e08e) · [LLMStageTrace.to_dict](#fun-a2365082b2) · [StageMeta.to_dict](#fun-870ca31bac) · [AgentPipelineMeta.record](#fun-9f425d9994) · [AgentPipelineMeta.to_dict](#fun-fc7d17553e) · [AgentTrace.to_dict](#fun-e1230024c0) · [LLMAnalysis.to_dict](#fun-0ed4ada825)

<a id="fun-1a5c4973e8"></a>

#### `AnalystReport.to_dict`

- **ID / 行**：`FUN-1A5C4973E8` / `L41`（源码见本单元概览）
- **签名 / 返回**：`AnalystReport.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-11d5edef39"></a>

#### `AnalystTeam.reports`

- **ID / 行**：`FUN-11D5EDEF39` / `L57`（源码见本单元概览）
- **签名 / 返回**：`AnalystTeam.reports(self)` → `list[AnalystReport]`
- **职责**：As-built responsibility derived from `reports` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/integration/test_coherence.py](../../tests/integration/test_coherence.py)、[tests/regression/test_docs_structure.py](../../tests/regression/test_docs_structure.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) · direct-dynamic

<a id="fun-d1937786ae"></a>

#### `AnalystTeam.to_dict`

- **ID / 行**：`FUN-D1937786AE` / `L60`（源码见本单元概览）
- **签名 / 返回**：`AnalystTeam.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：self.fundamentals.to_dict、self.news.to_dict、self.sentiment.to_dict、self.technical.to_dict
- **复杂度 / 风险**：分支 0；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-3104427770"></a>

#### `AgentEvidence.to_dict`

- **ID / 行**：`FUN-3104427770` / `L78`（源码见本单元概览）
- **签名 / 返回**：`AgentEvidence.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-378c040696"></a>

#### `ResearchDebate.to_dict`

- **ID / 行**：`FUN-378C040696` / `L93`（源码见本单元概览）
- **签名 / 返回**：`ResearchDebate.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：self.bearish.to_dict、self.bullish.to_dict
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-78898fe309"></a>

#### `LevelProposal.to_dict`

- **ID / 行**：`FUN-78898FE309` / `L132`（源码见本单元概览）
- **签名 / 返回**：`LevelProposal.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-cbd371affe"></a>

#### `TransactionProposal.to_dict`

- **ID / 行**：`FUN-CBD371AFFE` / `L143`（源码见本单元概览）
- **签名 / 返回**：`TransactionProposal.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-1d042f655d"></a>

#### `RiskReview.to_dict`

- **ID / 行**：`FUN-1D042F655D` / `L155`（源码见本单元概览）
- **签名 / 返回**：`RiskReview.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-f763a5c226"></a>

#### `ManagerDecision.to_dict`

- **ID / 行**：`FUN-F763A5C226` / `L168`（源码见本单元概览）
- **签名 / 返回**：`ManagerDecision.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-1f2e0f588a"></a>

#### `HeadlineItem.to_dict`

- **ID / 行**：`FUN-1F2E0F588A` / `L182`（源码见本单元概览）
- **签名 / 返回**：`HeadlineItem.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-5a0e6a3977"></a>

#### `CalendarEvent.to_dict`

- **ID / 行**：`FUN-5A0E6A3977` / `L195`（源码见本单元概览）
- **签名 / 返回**：`CalendarEvent.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-4654e9b6a5"></a>

#### `CalendarEvent.display`

- **ID / 行**：`FUN-4654E9B6A5` / `L198`（源码见本单元概览）
- **签名 / 返回**：`CalendarEvent.display(self)` → `str`
- **职责**：As-built responsibility derived from `display` and its owning unit.
- **依赖**：strip
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py) · direct-dynamic

<a id="fun-0b81375e45"></a>

#### `MacroQuote.to_dict`

- **ID / 行**：`FUN-0B81375E45` / `L214`（源码见本单元概览）
- **签名 / 返回**：`MacroQuote.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-b52c340615"></a>

#### `ExternalFactors.to_dict`

- **ID / 行**：`FUN-B52C340615` / `L231`（源码见本单元概览）
- **签名 / 返回**：`ExternalFactors.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：c.to_dict、h.to_dict、m.to_dict
- **复杂度 / 风险**：分支 0；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-6449e7e08e"></a>

#### `MarketContext.to_dict`

- **ID / 行**：`FUN-6449E7E08E` / `L267`（源码见本单元概览）
- **签名 / 返回**：`MarketContext.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：list、self.analyses.keys、self.external.to_dict
- **复杂度 / 风险**：分支 0；跨度 10 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-a2365082b2"></a>

#### `LLMStageTrace.to_dict`

- **ID / 行**：`FUN-A2365082B2` / `L299`（源码见本单元概览）
- **签名 / 返回**：`LLMStageTrace.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-870ca31bac"></a>

#### `StageMeta.to_dict`

- **ID / 行**：`FUN-870CA31BAC` / `L311`（源码见本单元概览）
- **签名 / 返回**：`StageMeta.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：self.llm.to_dict
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-9f425d9994"></a>

#### `AgentPipelineMeta.record`

- **ID / 行**：`FUN-9F425D9994` / `L326`（源码见本单元概览）
- **签名 / 返回**：`AgentPipelineMeta.record(self, name: str, meta: StageMeta)` → `None`
- **职责**：As-built responsibility derived from `record` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-fc7d17553e"></a>

#### `AgentPipelineMeta.to_dict`

- **ID / 行**：`FUN-FC7D17553E` / `L329`（源码见本单元概览）
- **签名 / 返回**：`AgentPipelineMeta.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：self.stages.items、v.to_dict
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-e1230024c0"></a>

#### `AgentTrace.to_dict`

- **ID / 行**：`FUN-E1230024C0` / `L348`（源码见本单元概览）
- **签名 / 返回**：`AgentTrace.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-0ed4ada825"></a>

#### `LLMAnalysis.to_dict`

- **ID / 行**：`FUN-0ED4ADA825` / `L371`（源码见本单元概览）
- **签名 / 返回**：`LLMAnalysis.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="unit-a91501b8ca"></a>

### src/log.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A91501B8CA |
| 源码 | [src/log.py](../../src/log.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Central logging setup for GoldAnalysisAI. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[setup_logging](#fun-286f9adbe7) · [get_logger](#fun-02cd3d28ec)

<a id="fun-286f9adbe7"></a>

#### `setup_logging`

- **ID / 行**：`FUN-286F9ADBE7` / `L17`（源码见本单元概览）
- **签名 / 返回**：`setup_logging(*, level: str | None=None, log_file: str | None=None)` → `None`
- **职责**：Configure root logger once (console + optional rotating file).
- **异常 / 副作用 / 并发**：none-explicit / filesystem;global-state / caller-thread
- **依赖**：Path、RotatingFileHandler、console.setFormatter、debug、file_handler.setFormatter、getattr、hasattr、logging.Formatter、logging.StreamHandler、logging.getLogger、path.parent.mkdir、root.addHandler、root.setLevel、setLevel、sys.stderr.reconfigure、upper
- **复杂度 / 风险**：分支 5；跨度 43 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-02cd3d28ec"></a>

#### `get_logger`

- **ID / 行**：`FUN-02CD3D28EC` / `L62`（源码见本单元概览）
- **签名 / 返回**：`get_logger(name: str)` → `logging.Logger`
- **职责**：Return a module logger; ensures logging is configured.
- **依赖**：logging.getLogger、setup_logging
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-ba3f06e87a"></a>

### src/pipeline.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-BA3F06E87A |
| 源码 | [src/pipeline.py](../../src/pipeline.py) |
| 架构组件 | ARC-CORE — 主编排与进度 |
| 职责 | Main analysis pipeline — delegates to TradeAgent-style orchestrator. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) |
| 验证状态 | selected |

#### 函数导航

[run_analysis](#fun-33aef245ba)

<a id="fun-33aef245ba"></a>

#### `run_analysis`

- **ID / 行**：`FUN-33AEF245BA` / `L11`（源码见本单元概览）
- **签名 / 返回**：`run_analysis()` → `tuple[dict, dict, dict]`
- **职责**：As-built responsibility derived from `run_analysis` and its owning unit.
- **依赖**：log.debug、run_trade_agent_pipeline
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) · direct-dynamic

<a id="arc-data"></a>

## ARC-DATA — 行情与外部数据

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/data/__init__.py](#unit-5c9ecc73e4) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/aggregator.py](#unit-d3b9beaac0) | 4 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/calendar_utils.py](#unit-f5d8bd410b) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/context_builder.py](#unit-24843ac961) | 10 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/external_format.py](#unit-05079ecc27) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/fetch_pipeline.py](#unit-2b33a302fc) | 7 | 5 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/fetcher.py](#unit-5c3b60e30a) | 7 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/mt5.py](#unit-52888d723d) | 13 | 5 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/news_topics.py](#unit-c335b8f5cf) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/proxy_env.py](#unit-0f842b8ece) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive.py](#unit-ea7e4f88fe) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_compat.py](#unit-023a37a1e9) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_index.py](#unit-7bfc490988) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_prune.py](#unit-dad8bc5b0f) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/run_archive_schema.py](#unit-767bf49f25) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/__init__.py](#unit-c3952c43cb) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/_http.py](#unit-c590fce576) | 3 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/base.py](#unit-0df4638d5e) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/dxy.py](#unit-1fa1bdf5ba) | 1 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/fundamentals.py](#unit-ec9b21793d) | 4 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/gold_relevance.py](#unit-4d4d8a02c7) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/jin10_feed.py](#unit-7020937074) | 23 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/jin10_mcp_client.py](#unit-927bb1749d) | 10 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/macro.py](#unit-fe5c27c113) | 5 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/market.py](#unit-603339624c) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/news.py](#unit-58d6f95301) | 4 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/social.py](#unit-ba8df8a829) | 3 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/sources/social_feed.py](#unit-b05f7affa4) | 11 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/tradingview.py](#unit-c1711535ca) | 15 | 4 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |
| [src/data/url_redact.py](#unit-62a1aff305) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) | selected |

<a id="unit-5c9ecc73e4"></a>

### src/data/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5C9ECC73E4 |
| 源码 | [src/data/__init__.py](../../src/data/__init__.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | 继承 行情与外部数据 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-d3b9beaac0"></a>

### src/data/aggregator.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D3B9BEAAC0 |
| 源码 | [src/data/aggregator.py](../../src/data/aggregator.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Aggregate all data sources into a unified context slice. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 4 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py) |
| 验证状态 | selected |

#### 函数导航

[merge_external](#fun-4e87068569) · [collect_evidence](#fun-8b8349b09e) · [assemble_market_context](#fun-ddf5efe045) · [build_market_context](#fun-e8cc53e6f4)

<a id="fun-4e87068569"></a>

#### `merge_external`

- **ID / 行**：`FUN-4E87068569` / `L22`（源码见本单元概览）
- **签名 / 返回**：`merge_external(*parts: ExternalFactors)` → `ExternalFactors`
- **职责**：As-built responsibility derived from `merge_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：ExternalFactors、merged.calendar_events.extend、merged.fetch_errors.extend、merged.headline_items.extend、merged.macro_quotes.extend、merged.news_headlines.extend、merged.social_posts.extend、merged.sources.append、sync_external_legacy_fields
- **复杂度 / 风险**：分支 6；跨度 22 行；high
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py) · direct-dynamic

<a id="fun-8b8349b09e"></a>

#### `collect_evidence`

- **ID / 行**：`FUN-8B8349B09E` / `L46`（源码见本单元概览）
- **签名 / 返回**：`collect_evidence(enriched: dict[str, pd.DataFrame])` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `collect_evidence` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：FundamentalsDataSource、MarketDataSource、NewsDataSource、SocialDataSource、fetch_evidence、items.extend
- **复杂度 / 风险**：分支 0；跨度 7 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-ddf5efe045"></a>

#### `assemble_market_context`

- **ID / 行**：`FUN-DDF5EFE045` / `L55`（源码见本单元概览）
- **签名 / 返回**：`assemble_market_context(enriched: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], external: ExternalFactors, source_label: str)` → `MarketContext`
- **职责**：Bind pre-fetched external data with enriched bars and ICT analyses.
- **依赖**：MarketContext、daily_metrics、finalize_market_context、float
- **复杂度 / 风险**：分支 0；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e8cc53e6f4"></a>

#### `build_market_context`

- **ID / 行**：`FUN-E8CC53E6F4` / `L76`（源码见本单元概览）
- **签名 / 返回**：`build_market_context(enriched: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis])` → `MarketContext`
- **职责**：Legacy entry — fetches external again. Prefer fetch_all_data + assemble_market_context.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：assemble_market_context、fetch_external_bundle、get_active_source
- **复杂度 / 风险**：分支 0；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="unit-f5d8bd410b"></a>

### src/data/calendar_utils.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F5D8BD410B |
| 源码 | [src/data/calendar_utils.py](../../src/data/calendar_utils.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Calendar parsing and filtering — no data-source imports. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 函数导航

[parse_event_time](#fun-be22aae06a) · [filter_upcoming_calendar_events](#fun-07d2119d72) · [calendar_to_risk_text](#fun-d55bebcd6f)

<a id="fun-be22aae06a"></a>

#### `parse_event_time`

- **ID / 行**：`FUN-BE22AAE06A` / `L11`（源码见本单元概览）
- **签名 / 返回**：`parse_event_time(raw: str)` → `datetime | None`
- **职责**：As-built responsibility derived from `parse_event_time` and its owning unit.
- **依赖**：datetime.strptime、match.group、re.search、strip
- **复杂度 / 风险**：分支 5；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-07d2119d72"></a>

#### `filter_upcoming_calendar_events`

- **ID / 行**：`FUN-07D2119D72` / `L35`（源码见本单元概览）
- **签名 / 返回**：`filter_upcoming_calendar_events(events: list[CalendarEvent])` → `list[CalendarEvent]`
- **职责**：Keep only future (or very recent) events with parseable times.
- **依赖**：datetime.now、kept.append、parse_event_time、total_seconds
- **复杂度 / 风险**：分支 3；跨度 12 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) · direct-dynamic

<a id="fun-d55bebcd6f"></a>

#### `calendar_to_risk_text`

- **ID / 行**：`FUN-D55BEBCD6F` / `L49`（源码见本单元概览）
- **签名 / 返回**：`calendar_to_risk_text(events: list[CalendarEvent], *, limit: int=6)` → `str`
- **职责**：As-built responsibility derived from `calendar_to_risk_text` and its owning unit.
- **依赖**：e.display、join
- **复杂度 / 风险**：分支 1；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-24843ac961"></a>

### src/data/context_builder.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-24843AC961 |
| 源码 | [src/data/context_builder.py](../../src/data/context_builder.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Build derived analyst context and density metrics. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 10 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 函数导航

[build_market_position](#fun-750f9f2cf5) · [build_spot_cross_check](#fun-046ae84c1b) · [build_event_countdown](#fun-bc16d7a171) · [build_jin10_kline_summary](#fun-94a1869676) · [build_derived_context](#fun-21a4a84fe5) · [compute_context_stats](#fun-53864154eb) · [_technical_input_stats](#fun-309515b2c5) · [_volume_nonzero_ratio](#fun-12577f43a5) · [_analyst_input_stats](#fun-14f86ea322) · [finalize_market_context](#fun-260ff71074)

<a id="fun-750f9f2cf5"></a>

#### `build_market_position`

- **ID / 行**：`FUN-750F9F2CF5` / `L44`（源码见本单元概览）
- **签名 / 返回**：`build_market_position(enriched: dict[str, pd.DataFrame], price: float)` → `dict[str, Any]`
- **职责**：EMA / VWAP distances and recent range for technical analyst.
- **依赖**：ema_relation、float、len、max、min、pd.notna、relations.items、round、tail
- **复杂度 / 风险**：分支 2；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-046ae84c1b"></a>

#### `build_spot_cross_check`

- **ID / 行**：`FUN-046AE84C1B` / `L68`（源码见本单元概览）
- **签名 / 返回**：`build_spot_cross_check(tv_price: float, quote: dict[str, Any] | None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_spot_cross_check` and its owning unit.
- **依赖**：abs、float、quote.get、round
- **复杂度 / 风险**：分支 3；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-bc16d7a171"></a>

#### `build_event_countdown`

- **ID / 行**：`FUN-BC16D7A171` / `L89`（源码见本单元概览）
- **签名 / 返回**：`build_event_countdown(events: list[CalendarEvent])` → `dict[str, Any]`
- **职责**：Hours until the next high-impact calendar event.
- **依赖**：datetime.now、filter_upcoming_calendar_events、parse_event_time、round、total_seconds
- **复杂度 / 风险**：分支 6；跨度 26 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-94a1869676"></a>

#### `build_jin10_kline_summary`

- **ID / 行**：`FUN-94A1869676` / `L117`（源码见本单元概览）
- **签名 / 返回**：`build_jin10_kline_summary(bars: list[dict[str, Any]], tv_price: float)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_jin10_kline_summary` and its owning unit.
- **依赖**：abs、first.get、float、last.get、len、round
- **复杂度 / 风险**：分支 6；跨度 26 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-21a4a84fe5"></a>

#### `build_derived_context`

- **ID / 行**：`FUN-21A4A84FE5` / `L145`（源码见本单元概览）
- **签名 / 返回**：`build_derived_context(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_derived_context` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：build_event_countdown、build_jin10_kline_summary、build_market_position、build_spot_cross_check、cluster_headline_topics、e.to_dict、fetch_jin10_kline、fetch_jin10_quote、filter_upcoming_calendar_events、len、sentiment_score、sum
- **复杂度 / 风险**：分支 4；跨度 34 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-53864154eb"></a>

#### `compute_context_stats`

- **ID / 行**：`FUN-53864154EB` / `L181`（源码见本单元概览）
- **签名 / 返回**：`compute_context_stats(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `compute_context_stats` and its owning unit.
- **依赖**：_analyst_input_stats、_technical_input_stats、ctx.analyses.values、ctx.external.to_dict、json.dumps、len、list、payload_sample.encode、sum
- **复杂度 / 风险**：分支 1；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-309515b2c5"></a>

#### `_technical_input_stats`

- **ID / 行**：`FUN-309515B2C5` / `L202`（源码见本单元概览）
- **签名 / 返回**：`_technical_input_stats(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：Observability snapshot for K-line-derived technical inputs.
- **依赖**：_volume_nonzero_ratio、bars.get、ctx.analyses.items、ctx.analyses.values、ctx.enriched.get、ctx.enriched.items、indicator_ready.get、len、pd.notna、set、sorted、sr.get、sum、support_resistance_context、technical_quality
- **复杂度 / 风险**：分支 3；跨度 52 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-12577f43a5"></a>

#### `_volume_nonzero_ratio`

- **ID / 行**：`FUN-12577F43A5` / `L256`（源码见本单元概览）
- **签名 / 返回**：`_volume_nonzero_ratio(df: pd.DataFrame | None)` → `float`
- **职责**：As-built responsibility derived from `_volume_nonzero_ratio` and its owning unit.
- **依赖**：astype、float、len、round、sum
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-14f86ea322"></a>

#### `_analyst_input_stats`

- **ID / 行**：`FUN-14F86EA322` / `L263`（源码见本单元概览）
- **签名 / 返回**：`_analyst_input_stats(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：Role-level input density for the non-technical analysts.
- **依赖**：bool、ctx.derived.get、e.lower、float、len、post.get、round、social_kind_counts.get、str、sum
- **复杂度 / 风险**：分支 2；跨度 52 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-260ff71074"></a>

#### `finalize_market_context`

- **ID / 行**：`FUN-260FF71074` / `L317`（源码见本单元概览）
- **签名 / 返回**：`finalize_market_context(ctx: MarketContext)` → `MarketContext`
- **职责**：Attach derived signals and density stats after assembly.
- **依赖**：build_derived_context、compute_context_stats、filter_upcoming_calendar_events、sync_external_legacy_fields
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="unit-05079ecc27"></a>

### src/data/external_format.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-05079ECC27 |
| 源码 | [src/data/external_format.py](../../src/data/external_format.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | ExternalFactors legacy string fields — no data-source imports. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 函数导航

[headlines_to_strings](#fun-92f0ba6a2b) · [sync_external_legacy_fields](#fun-361441992e)

<a id="fun-92f0ba6a2b"></a>

#### `headlines_to_strings`

- **ID / 行**：`FUN-92F0BA6A2B` / `L13`（源码见本单元概览）
- **签名 / 返回**：`headlines_to_strings(items: list[HeadlineItem], *, limit: int | None=None)` → `list[str]`
- **职责**：As-built responsibility derived from `headlines_to_strings` and its owning unit.
- **依赖**：item.text.strip、len、out.append、seen.add、set
- **复杂度 / 风险**：分支 3；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-361441992e"></a>

#### `sync_external_legacy_fields`

- **ID / 行**：`FUN-361441992E` / `L28`（源码见本单元概览）
- **签名 / 返回**：`sync_external_legacy_fields(ext: ExternalFactors)` → `None`
- **职责**：Keep news_headlines / risk_events in sync with structured fields.
- **依赖**：calendar_to_risk_text、filter_upcoming_calendar_events、headlines_to_strings、len、log.info
- **复杂度 / 风险**：分支 3；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) · direct-dynamic

<a id="unit-2b33a302fc"></a>

### src/data/fetch_pipeline.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2B33A302FC |
| 源码 | [src/data/fetch_pipeline.py](../../src/data/fetch_pipeline.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Unified data fetch — TradingView bars + external feeds at pipeline start. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 5 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[DataFetchResult.bars_summary](#fun-237e01db5b) · [DataFetchResult.external_preview](#fun-debf2265ca) · [_fetch_news_external](#fun-112152936c) · [_fetch_social_external](#fun-da07c46547) · [_fetch_fundamentals_external](#fun-984c9019fc) · [fetch_external_bundle](#fun-6df80aee05) · [fetch_all_data](#fun-d6c382b005)

<a id="fun-237e01db5b"></a>

#### `DataFetchResult.bars_summary`

- **ID / 行**：`FUN-237E01DB5B` / `L34`（源码见本单元概览）
- **签名 / 返回**：`DataFetchResult.bars_summary(self)` → `dict[str, int]`
- **职责**：As-built responsibility derived from `bars_summary` and its owning unit.
- **依赖**：len、self.raw.items
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-debf2265ca"></a>

#### `DataFetchResult.external_preview`

- **ID / 行**：`FUN-DEBF2265CA` / `L37`（源码见本单元概览）
- **签名 / 返回**：`DataFetchResult.external_preview(self)` → `dict`
- **职责**：As-built responsibility derived from `external_preview` and its owning unit.
- **依赖**：len
- **复杂度 / 风险**：分支 0；跨度 15 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-112152936c"></a>

#### `_fetch_news_external`

- **ID / 行**：`FUN-112152936C` / `L54`（源码见本单元概览）
- **签名 / 返回**：`_fetch_news_external()` → `ExternalFactors`
- **职责**：As-built responsibility derived from `_fetch_news_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：NewsDataSource、fetch_external
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-da07c46547"></a>

#### `_fetch_social_external`

- **ID / 行**：`FUN-DA07C46547` / `L58`（源码见本单元概览）
- **签名 / 返回**：`_fetch_social_external()` → `ExternalFactors`
- **职责**：As-built responsibility derived from `_fetch_social_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：SocialDataSource、fetch_external
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-984c9019fc"></a>

#### `_fetch_fundamentals_external`

- **ID / 行**：`FUN-984C9019FC` / `L62`（源码见本单元概览）
- **签名 / 返回**：`_fetch_fundamentals_external()` → `ExternalFactors`
- **职责**：As-built responsibility derived from `_fetch_fundamentals_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：FundamentalsDataSource、fetch_external
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-6df80aee05"></a>

#### `fetch_external_bundle`

- **ID / 行**：`FUN-6DF80AEE05` / `L66`（源码见本单元概览）
- **签名 / 返回**：`fetch_external_bundle(*, parallel_http: bool=True)` → `ExternalFactors`
- **职责**：News + social + fundamentals (DXY/US10Y). All three HTTP sources run in parallel when enabled.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：ThreadPoolExecutor、_fetch_fundamentals_external、_fetch_news_external、_fetch_social_external、fut_fund.result、fut_news.result、fut_social.result、merge_external、pool.submit
- **复杂度 / 风险**：分支 1；跨度 15 行；high
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-d6c382b005"></a>

#### `fetch_all_data`

- **ID / 行**：`FUN-D6C382B005` / `L83`（源码见本单元概览）
- **签名 / 返回**：`fetch_all_data()` → `DataFetchResult`
- **职责**：Pull everything up front:
- **异常 / 副作用 / 并发**：none-explicit / external-io;shared-state / caller-thread
- **依赖**：DataFetchResult、bars.get、ext_bits.append、fetch_external_bundle、fetch_multi_timeframe、get_active_source、get_progress、int、join、json.dumps、len、log.info、prog.done、prog.fail、prog.stage_io、prog.start、prog.update、raw.items、result.external_preview、str
- **复杂度 / 风险**：分支 5；跨度 62 行；high
- **测试 / 验证**：[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="unit-5c3b60e30a"></a>

### src/data/fetcher.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5C3B60E30A |
| 源码 | [src/data/fetcher.py](../../src/data/fetcher.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Market data fetcher — TradingView (via tvDatafeed). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[clear_cache](#fun-f5cfdcfe8d) · [get_active_source](#fun-e9ad7716d7) · [fetch_multi_timeframe](#fun-d6fbd9beaa) · [fetch_all](#fun-1bb0e91f10) · [daily_metrics](#fun-5a69f43861) · [utc8_now](#fun-f3d127c2a7) · [format_utc8](#fun-782624f6ed)

<a id="fun-f5cfdcfe8d"></a>

#### `clear_cache`

- **ID / 行**：`FUN-F5CFDCFE8D` / `L18`（源码见本单元概览）
- **签名 / 返回**：`clear_cache()` → `None`
- **职责**：As-built responsibility derived from `clear_cache` and its owning unit.
- **依赖**：log.debug、tradingview.reset_client
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) · direct-dynamic

<a id="fun-e9ad7716d7"></a>

#### `get_active_source`

- **ID / 行**：`FUN-E9AD7716D7` / `L23`（源码见本单元概览）
- **签名 / 返回**：`get_active_source()` → `str`
- **职责**：As-built responsibility derived from `get_active_source` and its owning unit.
- **依赖**：tradingview.source_label
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d6fbd9beaa"></a>

#### `fetch_multi_timeframe`

- **ID / 行**：`FUN-D6FBD9BEAA` / `L27`（源码见本单元概览）
- **签名 / 返回**：`fetch_multi_timeframe()` → `dict[Timeframe, pd.DataFrame]`
- **职责**：As-built responsibility derived from `fetch_multi_timeframe` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：tradingview.fetch_multi_timeframe
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-1bb0e91f10"></a>

#### `fetch_all`

- **ID / 行**：`FUN-1BB0E91F10` / `L31`（源码见本单元概览）
- **签名 / 返回**：`fetch_all()` → `'DataFetchResult'`
- **职责**：Unified fetch: bars + external. See ``src.data.fetch_pipeline``.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：fetch_all_data
- **复杂度 / 风险**：分支 0；跨度 5 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-5a69f43861"></a>

#### `daily_metrics`

- **ID / 行**：`FUN-5A69F43861` / `L38`（源码见本单元概览）
- **签名 / 返回**：`daily_metrics(df_1d: pd.DataFrame)` → `dict`
- **职责**：As-built responsibility derived from `daily_metrics` and its owning unit.
- **依赖**：float、len
- **复杂度 / 风险**：分支 2；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py) · direct-dynamic

<a id="fun-f3d127c2a7"></a>

#### `utc8_now`

- **ID / 行**：`FUN-F3D127C2A7` / `L71`（源码见本单元概览）
- **签名 / 返回**：`utc8_now()` → `datetime`
- **职责**：As-built responsibility derived from `utc8_now` and its owning unit.
- **依赖**：datetime.now
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-782624f6ed"></a>

#### `format_utc8`

- **ID / 行**：`FUN-782624F6ED` / `L75`（源码见本单元概览）
- **签名 / 返回**：`format_utc8(iso_value: object, *, fmt: str='%Y-%m-%d %H:%M')` → `str`
- **职责**：Format an ISO UTC timestamp for UI display in Beijing time (UTC+8).
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：datetime.fromisoformat、datetime.strptime、dt.astimezone、dt.replace、isdigit、len、local.strftime、raw.replace、raw.rstrip、replace、str、strip
- **复杂度 / 风险**：分支 5；跨度 22 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="unit-52888d723d"></a>

### src/data/mt5.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-52888D723D |
| 源码 | [src/data/mt5.py](../../src/data/mt5.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Optional MetaTrader 5 execution bridge. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 13 / 5 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) |
| 验证状态 | selected |

#### 函数导航

[MT5Provider.is_available](#fun-a41f07faab) · [MT5Provider.account_info](#fun-a1dfe3ce6d) · [MT5Provider.shutdown](#fun-2ceb3ae7c8) · [DisabledMT5Provider.__init__](#fun-eba1ab6898) · [DisabledMT5Provider.is_available](#fun-142d9a85d4) · [DisabledMT5Provider.account_info](#fun-a96d8007a3) · [DisabledMT5Provider.shutdown](#fun-0f677dda5e) · [MetaTrader5Provider.__init__](#fun-efaf091f3b) · [MetaTrader5Provider.is_available](#fun-d4e9736d8a) · [MetaTrader5Provider.account_info](#fun-2c7542532d) · [MetaTrader5Provider.shutdown](#fun-573d1aeba3) · [MetaTrader5Provider._ensure_initialized](#fun-f8948e51cb) · [get_mt5_provider](#fun-28bba5cb4c)

<a id="fun-a41f07faab"></a>

#### `MT5Provider.is_available`

- **ID / 行**：`FUN-A41F07FAAB` / `L40`（源码见本单元概览）
- **签名 / 返回**：`MT5Provider.is_available(self)` → `bool`
- **职责**：As-built responsibility derived from `is_available` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="fun-a1dfe3ce6d"></a>

#### `MT5Provider.account_info`

- **ID / 行**：`FUN-A1DFE3CE6D` / `L43`（源码见本单元概览）
- **签名 / 返回**：`MT5Provider.account_info(self)` → `dict[str, object]`
- **职责**：As-built responsibility derived from `account_info` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="fun-2ceb3ae7c8"></a>

#### `MT5Provider.shutdown`

- **ID / 行**：`FUN-2CEB3AE7C8` / `L46`（源码见本单元概览）
- **签名 / 返回**：`MT5Provider.shutdown(self)` → `None`
- **职责**：As-built responsibility derived from `shutdown` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-eba1ab6898"></a>

#### `DisabledMT5Provider.__init__`

- **ID / 行**：`FUN-EBA1AB6898` / `L57`（源码见本单元概览）
- **签名 / 返回**：`DisabledMT5Provider.__init__(self, reason: str='MT5_ENABLED=false')` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-142d9a85d4"></a>

#### `DisabledMT5Provider.is_available`

- **ID / 行**：`FUN-142D9A85D4` / `L60`（源码见本单元概览）
- **签名 / 返回**：`DisabledMT5Provider.is_available(self)` → `bool`
- **职责**：As-built responsibility derived from `is_available` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="fun-a96d8007a3"></a>

#### `DisabledMT5Provider.account_info`

- **ID / 行**：`FUN-A96D8007A3` / `L63`（源码见本单元概览）
- **签名 / 返回**：`DisabledMT5Provider.account_info(self)` → `dict[str, object]`
- **职责**：As-built responsibility derived from `account_info` and its owning unit.
- **异常 / 副作用 / 并发**：MT5UnavailableError / none-detected / caller-thread
- **依赖**：MT5UnavailableError
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="fun-0f677dda5e"></a>

#### `DisabledMT5Provider.shutdown`

- **ID / 行**：`FUN-0F677DDA5E` / `L66`（源码见本单元概览）
- **签名 / 返回**：`DisabledMT5Provider.shutdown(self)` → `None`
- **职责**：As-built responsibility derived from `shutdown` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-efaf091f3b"></a>

#### `MetaTrader5Provider.__init__`

- **ID / 行**：`FUN-EFAF091F3B` / `L73`（源码见本单元概览）
- **签名 / 返回**：`MetaTrader5Provider.__init__(self, config: MT5Config | None=None)` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **异常 / 副作用 / 并发**：MT5UnavailableError / none-detected / caller-thread
- **依赖**：MT5Config、MT5UnavailableError
- **复杂度 / 风险**：分支 1；跨度 8 行；high
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-d4e9736d8a"></a>

#### `MetaTrader5Provider.is_available`

- **ID / 行**：`FUN-D4E9736D8A` / `L82`（源码见本单元概览）
- **签名 / 返回**：`MetaTrader5Provider.is_available(self)` → `bool`
- **职责**：As-built responsibility derived from `is_available` and its owning unit.
- **依赖**：self._ensure_initialized
- **复杂度 / 风险**：分支 1；跨度 6 行；high
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="fun-2c7542532d"></a>

#### `MetaTrader5Provider.account_info`

- **ID / 行**：`FUN-2C7542532D` / `L89`（源码见本单元概览）
- **签名 / 返回**：`MetaTrader5Provider.account_info(self)` → `dict[str, object]`
- **职责**：As-built responsibility derived from `account_info` and its owning unit.
- **异常 / 副作用 / 并发**：MT5UnavailableError / none-detected / caller-thread
- **依赖**：MT5UnavailableError、data.get、info._asdict、self._ensure_initialized、self._mt5.account_info、self._mt5.last_error
- **复杂度 / 风险**：分支 1；跨度 17 行；high
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="fun-573d1aeba3"></a>

#### `MetaTrader5Provider.shutdown`

- **ID / 行**：`FUN-573D1AEBA3` / `L107`（源码见本单元概览）
- **签名 / 返回**：`MetaTrader5Provider.shutdown(self)` → `None`
- **职责**：As-built responsibility derived from `shutdown` and its owning unit.
- **依赖**：self._mt5.shutdown
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-f8948e51cb"></a>

#### `MetaTrader5Provider._ensure_initialized`

- **ID / 行**：`FUN-F8948E51CB` / `L112`（源码见本单元概览）
- **签名 / 返回**：`MetaTrader5Provider._ensure_initialized(self)` → `None`
- **职责**：As-built responsibility derived from `_ensure_initialized` and its owning unit.
- **异常 / 副作用 / 并发**：MT5UnavailableError / none-detected / caller-thread
- **依赖**：MT5UnavailableError、int、self._mt5.initialize、self._mt5.last_error
- **复杂度 / 风险**：分支 6；跨度 17 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-28bba5cb4c"></a>

#### `get_mt5_provider`

- **ID / 行**：`FUN-28BBA5CB4C` / `L131`（源码见本单元概览）
- **签名 / 返回**：`get_mt5_provider(config: MT5Config | None=None)` → `MT5Provider`
- **职责**：As-built responsibility derived from `get_mt5_provider` and its owning unit.
- **依赖**：DisabledMT5Provider、MT5Config、MetaTrader5Provider、str
- **复杂度 / 风险**：分支 2；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_mt5_provider.py](../../tests/unit/test_mt5_provider.py) · direct-dynamic

<a id="unit-c335b8f5cf"></a>

### src/data/news_topics.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C335B8F5CF |
| 源码 | [src/data/news_topics.py](../../src/data/news_topics.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Cluster Jin10 headlines into macro themes for debate / derived context. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[cluster_headline_topics](#fun-1ed76ebfc7)

<a id="fun-1ed76ebfc7"></a>

#### `cluster_headline_topics`

- **ID / 行**：`FUN-1ED76EBFC7` / `L17`（源码见本单元概览）
- **签名 / 返回**：`cluster_headline_topics(items: list[HeadlineItem], *, max_topics: int=3)` → `list[dict[str, object]]`
- **职责**：Rule-based topic buckets from headline text.
- **依赖**：any、append、buckets.items、int、item.text.lower、k.lower、len、topics.append、topics.sort
- **复杂度 / 风险**：分支 5；跨度 27 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="unit-0f842b8ece"></a>

### src/data/proxy_env.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0F842B8ECE |
| 源码 | [src/data/proxy_env.py](../../src/data/proxy_env.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Apply system / env HTTP proxy for requests and WebSocket clients. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[read_system_proxy](#fun-ce8b65f86a) · [apply_system_proxy](#fun-2365b1ea92)

<a id="fun-ce8b65f86a"></a>

#### `read_system_proxy`

- **ID / 行**：`FUN-CE8B65F86A` / `L8`（源码见本单元概览）
- **签名 / 返回**：`read_system_proxy()` → `str | None`
- **职责**：As-built responsibility derived from `read_system_proxy` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem;shared-state / caller-thread
- **依赖**：os.environ.get、server.split、strip、winreg.CloseKey、winreg.OpenKey、winreg.QueryValueEx
- **复杂度 / 风险**：分支 6；跨度 24 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2365b1ea92"></a>

#### `apply_system_proxy`

- **ID / 行**：`FUN-2365B1EA92` / `L34`（源码见本单元概览）
- **签名 / 返回**：`apply_system_proxy()` → `str | None`
- **职责**：Set http_proxy/https_proxy from env or Windows registry (idempotent).
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：os.environ.setdefault、read_system_proxy
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-ea7e4f88fe"></a>

### src/data/run_archive.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EA7E4F88FE |
| 源码 | [src/data/run_archive.py](../../src/data/run_archive.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Backward-compatible re-export — prefer ``src.run.archive`` or ``src.run``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-023a37a1e9"></a>

### src/data/run_archive_compat.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-023A37A1E9 |
| 源码 | [src/data/run_archive_compat.py](../../src/data/run_archive_compat.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Backward-compatible re-export — prefer ``src.run.archive.compat``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-7bfc490988"></a>

### src/data/run_archive_index.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7BFC490988 |
| 源码 | [src/data/run_archive_index.py](../../src/data/run_archive_index.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Backward-compatible re-export — prefer ``src.run.archive.index``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-dad8bc5b0f"></a>

### src/data/run_archive_prune.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAD8BC5B0F |
| 源码 | [src/data/run_archive_prune.py](../../src/data/run_archive_prune.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Backward-compatible re-export — prefer ``src.run.archive.prune``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-767bf49f25"></a>

### src/data/run_archive_schema.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-767BF49F25 |
| 源码 | [src/data/run_archive_schema.py](../../src/data/run_archive_schema.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Backward-compatible re-export — prefer ``src.run.archive.schema``. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-c3952c43cb"></a>

### src/data/sources/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C3952C43CB |
| 源码 | [src/data/sources/__init__.py](../../src/data/sources/__init__.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | External data sources — Jin10 MCP, DXY, TV social, market bars. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-c590fce576"></a>

### src/data/sources/_http.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C590FCE576 |
| 源码 | [src/data/sources/_http.py](../../src/data/sources/_http.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Shared HTTP helpers for external data sources. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py) |
| 验证状态 | selected |

#### 函数导航

[post_json](#fun-fc8cbed92a) · [get_json](#fun-6afe1ec0a4) · [get_text](#fun-299c0d3a32)

<a id="fun-fc8cbed92a"></a>

#### `post_json`

- **ID / 行**：`FUN-FC8CBED92A` / `L29`（源码见本单元概览）
- **签名 / 返回**：`post_json(url: str, *, body: dict[str, Any] | list[Any], params: dict[str, Any] | None=None, headers: dict[str, str] | None=None, timeout: int | None=None)` → `Any`
- **职责**：As-built responsibility derived from `post_json` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / external-io / caller-thread
- **依赖**：RuntimeError、log.warning、merged.setdefault、range、requests.post、resp.json、resp.raise_for_status、time.sleep
- **复杂度 / 风险**：分支 4；跨度 32 行；high
- **测试 / 验证**：[tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py) · direct-dynamic

<a id="fun-6afe1ec0a4"></a>

#### `get_json`

- **ID / 行**：`FUN-6AFE1EC0A4` / `L63`（源码见本单元概览）
- **签名 / 返回**：`get_json(url: str, *, params: dict[str, Any] | None=None, headers: dict[str, str] | None=None, cookies: dict[str, str] | None=None)` → `Any`
- **职责**：As-built responsibility derived from `get_json` and its owning unit.
- **依赖**：get_text、json.loads
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py) · direct-dynamic

<a id="fun-299c0d3a32"></a>

#### `get_text`

- **ID / 行**：`FUN-299C0D3A32` / `L73`（源码见本单元概览）
- **签名 / 返回**：`get_text(url: str, *, params: dict[str, Any] | None=None, headers: dict[str, str] | None=None, cookies: dict[str, str] | None=None)` → `str`
- **职责**：As-built responsibility derived from `get_text` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / external-io / caller-thread
- **依赖**：RuntimeError、log.warning、range、requests.get、resp.raise_for_status、time.sleep
- **复杂度 / 风险**：分支 3；跨度 29 行；high
- **测试 / 验证**：[tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py) · direct-dynamic

<a id="unit-0df4638d5e"></a>

### src/data/sources/base.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0DF4638D5E |
| 源码 | [src/data/sources/base.py](../../src/data/sources/base.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Data source protocols (TradeAgent data layer). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) |
| 验证状态 | selected |

#### 函数导航

[DataSource.fetch](#fun-600c64bcb0)

<a id="fun-600c64bcb0"></a>

#### `DataSource.fetch`

- **ID / 行**：`FUN-600C64BCB0` / `L14`（源码见本单元概览）
- **签名 / 返回**：`DataSource.fetch(self)` → `list[EvidenceItem] | ExternalFactors`
- **职责**：As-built responsibility derived from `fetch` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="unit-1fa1bdf5ba"></a>

### src/data/sources/dxy.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1FA1BDF5BA |
| 源码 | [src/data/sources/dxy.py](../../src/data/sources/dxy.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | DXY (US Dollar Index) snapshot via TradingView. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[fetch_dxy_impact](#fun-85282ddc4d)

<a id="fun-85282ddc4d"></a>

#### `fetch_dxy_impact`

- **ID / 行**：`FUN-85282DDC4D` / `L14`（源码见本单元概览）
- **签名 / 返回**：`fetch_dxy_impact()` → `tuple[str, dict]`
- **职责**：Return (human impact text, refs dict).
- **异常 / 副作用 / 并发**：ValueError / external-io;filesystem / caller-thread
- **依赖**：ValueError、_PLACEHOLDER.replace、fetch_symbol_daily、float、len、log.info、log.warning、round、str
- **复杂度 / 风险**：分支 5；跨度 40 行；high
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-ec9b21793d"></a>

### src/data/sources/fundamentals.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EC9B21793D |
| 源码 | [src/data/sources/fundamentals.py](../../src/data/sources/fundamentals.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Macro / fundamentals for gold — DXY + US10Y via TradingView. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 4 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[FundamentalsDataSource.fetch_external](#fun-85ea252365) · [FundamentalsDataSource.fetch_evidence](#fun-6a23a66cff) · [macro_quotes_to_evidence](#fun-ad52255426) · [external_macro_evidence](#fun-683a4407dd)

<a id="fun-85ea252365"></a>

#### `FundamentalsDataSource.fetch_external`

- **ID / 行**：`FUN-85EA252365` / `L12`（源码见本单元概览）
- **签名 / 返回**：`FundamentalsDataSource.fetch_external(self)` → `ExternalFactors`
- **职责**：As-built responsibility derived from `fetch_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：ExternalFactors、any、fetch_macro_quotes、next、sources.append
- **复杂度 / 风险**：分支 3；跨度 12 行；high
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-6a23a66cff"></a>

#### `FundamentalsDataSource.fetch_evidence`

- **ID / 行**：`FUN-6A23A66CFF` / `L25`（源码见本单元概览）
- **签名 / 返回**：`FundamentalsDataSource.fetch_evidence(self)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `fetch_evidence` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：fetch_macro_quotes、macro_quotes_to_evidence
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-ad52255426"></a>

#### `macro_quotes_to_evidence`

- **ID / 行**：`FUN-AD52255426` / `L29`（源码见本单元概览）
- **签名 / 返回**：`macro_quotes_to_evidence(quotes: list[MacroQuote])` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `macro_quotes_to_evidence` and its owning unit.
- **依赖**：EvidenceItem、items.append、q.to_dict
- **复杂度 / 风险**：分支 3；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-683a4407dd"></a>

#### `external_macro_evidence`

- **ID / 行**：`FUN-683A4407DD` / `L54`（源码见本单元概览）
- **签名 / 返回**：`external_macro_evidence(ext: ExternalFactors)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `external_macro_evidence` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：EvidenceItem、FundamentalsDataSource、fetch_evidence、macro_quotes_to_evidence
- **复杂度 / 风险**：分支 2；跨度 13 行；high
- **测试 / 验证**：— · static-and-component

<a id="unit-4d4d8a02c7"></a>

### src/data/sources/gold_relevance.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4D4D8A02C7 |
| 源码 | [src/data/sources/gold_relevance.py](../../src/data/sources/gold_relevance.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Gold / XAUUSD relevance filters for headlines and macro events. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[matches_gold_headline](#fun-64da59ba88) · [is_gold_macro_event](#fun-30d61ef6f5)

<a id="fun-64da59ba88"></a>

#### `matches_gold_headline`

- **ID / 行**：`FUN-64DA59BA88` / `L121`（源码见本单元概览）
- **签名 / 返回**：`matches_gold_headline(text: str)` → `bool`
- **职责**：As-built responsibility derived from `matches_gold_headline` and its owning unit.
- **依赖**：any、text.lower
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-30d61ef6f5"></a>

#### `is_gold_macro_event`

- **ID / 行**：`FUN-30D61EF6F5` / `L126`（源码见本单元概览）
- **签名 / 返回**：`is_gold_macro_event(event: str, region: str='', *, importance: float | None=None)` → `bool`
- **职责**：True if macro calendar row is likely to move XAUUSD.
- **依赖**：any、pat.search、strip、text.lower
- **复杂度 / 风险**：分支 4；跨度 12 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-7020937074"></a>

### src/data/sources/jin10_feed.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7020937074 |
| 源码 | [src/data/sources/jin10_feed.py](../../src/data/sources/jin10_feed.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Jin10 MCP — flash, articles, macro calendar (structured + legacy strings). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 23 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py)、[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[Jin10NewsBundle.headline_items](#fun-ad84260cd0) · [Jin10NewsBundle.headlines](#fun-0424648ecf) · [Jin10NewsBundle.is_live](#fun-f87ac8a103) · [_cached](#fun-e4d9bf91ca) · [_iter_rows](#fun-54e278ddf4) · [_is_relevant](#fun-71917bcd45) · [_parse_flash_item](#fun-81d80410a1) · [_parse_article_item](#fun-99163599fb) · [_parse_calendar_row](#fun-6ac6fd360c) · [_collect_items](#fun-4ce9f1e780) · [fetch_jin10_flash](#fun-e38a05cb72) · [fetch_jin10_flash._pull](#fun-e26f91daa9) · [fetch_jin10_articles](#fun-fa951f8508) · [fetch_jin10_articles._pull](#fun-82911d6a6c) · [fetch_jin10_calendar](#fun-8780d21897) · [fetch_jin10_calendar._pull](#fun-bd5c7672d7) · [fetch_jin10_risk_events](#fun-051831ac48) · [fetch_jin10_bundle](#fun-bb6ef855aa) · [fetch_jin10_quote](#fun-b4ef16ee9f) · [fetch_jin10_quote._pull](#fun-67ef031b31) · [_normalize_kline_bars](#fun-fbced9bbe7) · [fetch_jin10_kline](#fun-759eaf2c78) · [fetch_jin10_kline._pull](#fun-c4acab9575)

<a id="fun-ad84260cd0"></a>

#### `Jin10NewsBundle.headline_items`

- **ID / 行**：`FUN-AD84260CD0` / `L47`（源码见本单元概览）
- **签名 / 返回**：`Jin10NewsBundle.headline_items(self)` → `list[HeadlineItem]`
- **职责**：As-built responsibility derived from `headline_items` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-0424648ecf"></a>

#### `Jin10NewsBundle.headlines`

- **ID / 行**：`FUN-0424648ECF` / `L51`（源码见本单元概览）
- **签名 / 返回**：`Jin10NewsBundle.headlines(self)` → `list[str]`
- **职责**：As-built responsibility derived from `headlines` and its owning unit.
- **依赖**：item.text.strip、len、merged.append、seen.add、set
- **复杂度 / 风险**：分支 3；跨度 12 行；medium
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-f87ac8a103"></a>

#### `Jin10NewsBundle.is_live`

- **ID / 行**：`FUN-F87AC8A103` / `L65`（源码见本单元概览）
- **签名 / 返回**：`Jin10NewsBundle.is_live(self)` → `bool`
- **职责**：As-built responsibility derived from `is_live` and its owning unit.
- **依赖**：bool
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e4d9bf91ca"></a>

#### `_cached`

- **ID / 行**：`FUN-E4D9BF91CA` / `L69`（源码见本单元概览）
- **签名 / 返回**：`_cached(key: str, ttl: int, fn: Callable[[], Any])` → `tuple[Any, str | None]`
- **职责**：As-built responsibility derived from `_cached` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_CACHE.get、fn、log.warning、str、time.time
- **复杂度 / 风险**：分支 4；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-54e278ddf4"></a>

#### `_iter_rows`

- **ID / 行**：`FUN-54E278DDF4` / `L84`（源码见本单元概览）
- **签名 / 返回**：`_iter_rows(data: Any)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_iter_rows` and its owning unit.
- **依赖**：_iter_rows、data.get、isinstance
- **复杂度 / 风险**：分支 6；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-71917bcd45"></a>

#### `_is_relevant`

- **ID / 行**：`FUN-71917BCD45` / `L100`（源码见本单元概览）
- **签名 / 返回**：`_is_relevant(text: str, keyword: str)` → `bool`
- **职责**：As-built responsibility derived from `_is_relevant` and its owning unit.
- **依赖**：bool、matches_gold_headline
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-81d80410a1"></a>

#### `_parse_flash_item`

- **ID / 行**：`FUN-81D80410A1` / `L104`（源码见本单元概览）
- **签名 / 返回**：`_parse_flash_item(row: dict[str, Any])` → `HeadlineItem`
- **职责**：As-built responsibility derived from `_parse_flash_item` and its owning unit.
- **依赖**：HeadlineItem、row.get、str、strip
- **复杂度 / 风险**：分支 1；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-99163599fb"></a>

#### `_parse_article_item`

- **ID / 行**：`FUN-99163599FB` / `L118`（源码见本单元概览）
- **签名 / 返回**：`_parse_article_item(row: dict[str, Any])` → `HeadlineItem`
- **职责**：As-built responsibility derived from `_parse_article_item` and its owning unit.
- **依赖**：HeadlineItem、row.get、str、strip
- **复杂度 / 风险**：分支 2；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6ac6fd360c"></a>

#### `_parse_calendar_row`

- **ID / 行**：`FUN-6AC6FD360C` / `L136`（源码见本单元概览）
- **签名 / 返回**：`_parse_calendar_row(row: dict[str, Any])` → `CalendarEvent | None`
- **职责**：As-built responsibility derived from `_parse_calendar_row` and its owning unit.
- **依赖**：CalendarEvent、is_gold_macro_event、row.get、str、strip
- **复杂度 / 风险**：分支 4；跨度 24 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4ce9f1e780"></a>

#### `_collect_items`

- **ID / 行**：`FUN-4CE9F1E780` / `L162`（源码见本单元概览）
- **签名 / 返回**：`_collect_items(rows: list[dict[str, Any]], *, parse_fn: Callable[[dict[str, Any]], HeadlineItem], keyword: str, limit: int, fallback: bool)` → `list[HeadlineItem]`
- **职责**：As-built responsibility derived from `_collect_items` and its owning unit.
- **依赖**：_is_relevant、items.append、len、parse_fn、seen.add、set
- **复杂度 / 风险**：分支 7；跨度 25 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e38a05cb72"></a>

#### `fetch_jin10_flash`

- **ID / 行**：`FUN-E38A05CB72` / `L189`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_flash()` → `tuple[list[HeadlineItem], str | None]`
- **职责**：As-built responsibility derived from `fetch_jin10_flash` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：JIN10_KEYWORD.strip、_cached、_collect_items、_iter_rows、jin10_call_tool
- **复杂度 / 风险**：分支 3；跨度 22 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-e26f91daa9"></a>

#### `fetch_jin10_flash._pull`

- **ID / 行**：`FUN-E26F91DAA9` / `L196`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_flash._pull()` → `Any`
- **职责**：As-built responsibility derived from `_pull` and its owning unit.
- **依赖**：jin10_call_tool
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fa951f8508"></a>

#### `fetch_jin10_articles`

- **ID / 行**：`FUN-FA951F8508` / `L213`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_articles()` → `tuple[list[HeadlineItem], str | None]`
- **职责**：As-built responsibility derived from `fetch_jin10_articles` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：JIN10_KEYWORD.strip、_cached、_collect_items、_iter_rows、jin10_call_tool
- **复杂度 / 风险**：分支 4；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-82911d6a6c"></a>

#### `fetch_jin10_articles._pull`

- **ID / 行**：`FUN-82911D6A6C` / `L220`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_articles._pull()` → `Any`
- **职责**：As-built responsibility derived from `_pull` and its owning unit.
- **依赖**：jin10_call_tool
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8780d21897"></a>

#### `fetch_jin10_calendar`

- **ID / 行**：`FUN-8780D21897` / `L239`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_calendar()` → `tuple[list[CalendarEvent], str | None]`
- **职责**：As-built responsibility derived from `fetch_jin10_calendar` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_cached、_iter_rows、_parse_calendar_row、ev.display、events.append、jin10_call_tool、len、seen.add、set
- **复杂度 / 风险**：分支 7；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-bd5c7672d7"></a>

#### `fetch_jin10_calendar._pull`

- **ID / 行**：`FUN-BD5C7672D7` / `L243`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_calendar._pull()` → `Any`
- **职责**：As-built responsibility derived from `_pull` and its owning unit.
- **依赖**：jin10_call_tool
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-051831ac48"></a>

#### `fetch_jin10_risk_events`

- **ID / 行**：`FUN-051831AC48` / `L269`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_risk_events()` → `tuple[str, str | None]`
- **职责**：As-built responsibility derived from `fetch_jin10_risk_events` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：calendar_to_risk_text、fetch_jin10_calendar、filter_upcoming_calendar_events
- **复杂度 / 风险**：分支 2；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-bb6ef855aa"></a>

#### `fetch_jin10_bundle`

- **ID / 行**：`FUN-BB6EF855AA` / `L280`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_bundle()` → `Jin10NewsBundle`
- **职责**：Pull flash + articles + calendar in one call.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：Jin10NewsBundle、bundle.errors.append、bundle.sources.append、calendar_to_risk_text、fetch_jin10_articles、fetch_jin10_calendar、fetch_jin10_flash、filter_upcoming_calendar_events
- **复杂度 / 风险**：分支 7；跨度 36 行；high
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-b4ef16ee9f"></a>

#### `fetch_jin10_quote`

- **ID / 行**：`FUN-B4EF16EE9F` / `L321`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_quote(code: str | None=None)` → `tuple[dict[str, Any] | None, str | None]`
- **职责**：XAUUSD spot quote via Jin10 MCP get_quote (cached).
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_cached、data.get、isinstance、jin10_call_tool、strip
- **复杂度 / 风险**：分支 4；跨度 20 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-67ef031b31"></a>

#### `fetch_jin10_quote._pull`

- **ID / 行**：`FUN-67EF031B31` / `L329`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_quote._pull()` → `Any`
- **职责**：As-built responsibility derived from `_pull` and its owning unit.
- **依赖**：jin10_call_tool
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fbced9bbe7"></a>

#### `_normalize_kline_bars`

- **ID / 行**：`FUN-FBCED9BBE7` / `L343`（源码见本单元概览）
- **签名 / 返回**：`_normalize_kline_bars(data: Any)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_normalize_kline_bars` and its owning unit.
- **依赖**：_iter_rows、bars.append、float、row.get
- **复杂度 / 风险**：分支 3；跨度 22 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-759eaf2c78"></a>

#### `fetch_jin10_kline`

- **ID / 行**：`FUN-759EAF2C78` / `L367`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_kline(code: str | None=None, *, period: str | None=None, count: int | None=None)` → `tuple[list[dict[str, Any]], str | None]`
- **职责**：XAUUSD K-line via Jin10 MCP get_kline (cached).
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_cached、_normalize_kline_bars、data.get、isinstance、jin10_call_tool、strip
- **复杂度 / 风险**：分支 6；跨度 34 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-c4acab9575"></a>

#### `fetch_jin10_kline._pull`

- **ID / 行**：`FUN-C4ACAB9575` / `L386`（源码见本单元概览）
- **签名 / 返回**：`fetch_jin10_kline._pull()` → `Any`
- **职责**：As-built responsibility derived from `_pull` and its owning unit.
- **依赖**：jin10_call_tool
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-927bb1749d"></a>

### src/data/sources/jin10_mcp_client.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-927BB1749D |
| 源码 | [src/data/sources/jin10_mcp_client.py](../../src/data/sources/jin10_mcp_client.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Jin10 (金十数据) official MCP client — JSON-RPC over SSE. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 10 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py)、[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py) |
| 验证状态 | selected |

#### 函数导航

[_parse_sse](#fun-a697c9be9d) · [_pick_data](#fun-78f0060e7a) · [Jin10McpClient.__init__](#fun-84897c5cce) · [Jin10McpClient._headers](#fun-45a198880a) · [Jin10McpClient._next_id](#fun-9cb066a5e9) · [Jin10McpClient._post](#fun-48e026a8bb) · [Jin10McpClient.connect](#fun-72bb9b66ce) · [Jin10McpClient.call_tool](#fun-f9d2c12d6e) · [get_jin10_client](#fun-6b5241464f) · [jin10_call_tool](#fun-57be12ae7a)

<a id="fun-a697c9be9d"></a>

#### `_parse_sse`

- **ID / 行**：`FUN-A697C9BE9D` / `L25`（源码见本单元概览）
- **签名 / 返回**：`_parse_sse(text: str)` → `list[dict[str, Any]]`
- **职责**：Parse Jin10 MCP SSE — payload may span multiple physical lines.
- **异常 / 副作用 / 并发**：RuntimeError / none-detected / caller-thread
- **依赖**：RuntimeError、buf.append、join、json.loads、len、line.startswith、splitlines、strip、text.find
- **复杂度 / 风险**：分支 5；跨度 26 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-78f0060e7a"></a>

#### `_pick_data`

- **ID / 行**：`FUN-78F0060E7A` / `L53`（源码见本单元概览）
- **签名 / 返回**：`_pick_data(result: dict[str, Any] | None)` → `Any`
- **职责**：As-built responsibility derived from `_pick_data` and its owning unit.
- **依赖**：block.get、isinstance、json.loads、result.get
- **复杂度 / 风险**：分支 7；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-84897c5cce"></a>

#### `Jin10McpClient.__init__`

- **ID / 行**：`FUN-84897C5CCE` / `L72`（源码见本单元概览）
- **签名 / 返回**：`Jin10McpClient.__init__(self, *, token: str, url: str=JIN10_MCP_URL, protocol: str=JIN10_MCP_PROTOCOL)` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 6 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-45a198880a"></a>

#### `Jin10McpClient._headers`

- **ID / 行**：`FUN-45A198880A` / `L79`（源码见本单元概览）
- **签名 / 返回**：`Jin10McpClient._headers(self)` → `dict[str, str]`
- **职责**：As-built responsibility derived from `_headers` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9cb066a5e9"></a>

#### `Jin10McpClient._next_id`

- **ID / 行**：`FUN-9CB066A5E9` / `L88`（源码见本单元概览）
- **签名 / 返回**：`Jin10McpClient._next_id(self)` → `int`
- **职责**：As-built responsibility derived from `_next_id` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-48e026a8bb"></a>

#### `Jin10McpClient._post`

- **ID / 行**：`FUN-48E026A8BB` / `L92`（源码见本单元概览）
- **签名 / 返回**：`Jin10McpClient._post(self, body: dict[str, Any], *, expect_response: bool=True)` → `Any`
- **职责**：As-built responsibility derived from `_post` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / external-io / caller-thread
- **依赖**：RuntimeError、_parse_sse、e.get、err.get、next、range、requests.post、resp.content.decode、resp.headers.get、rpc.get、self._headers、time.sleep
- **复杂度 / 风险**：分支 9；跨度 43 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-72bb9b66ce"></a>

#### `Jin10McpClient.connect`

- **ID / 行**：`FUN-72BB9B66CE` / `L136`（源码见本单元概览）
- **签名 / 返回**：`Jin10McpClient.connect(self)` → `None`
- **职责**：As-built responsibility derived from `connect` and its owning unit.
- **依赖**：self._next_id、self._post
- **复杂度 / 风险**：分支 0；跨度 17 行；medium
- **测试 / 验证**：[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py) · direct-dynamic

<a id="fun-f9d2c12d6e"></a>

#### `Jin10McpClient.call_tool`

- **ID / 行**：`FUN-F9D2C12D6E` / `L154`（源码见本单元概览）
- **签名 / 返回**：`Jin10McpClient.call_tool(self, name: str, arguments: dict[str, Any] | None=None)` → `Any`
- **职责**：As-built responsibility derived from `call_tool` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / none-detected / caller-thread
- **依赖**：RuntimeError、_pick_data、isinstance、result.get、self._next_id、self._post
- **复杂度 / 风险**：分支 1；跨度 12 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-6b5241464f"></a>

#### `get_jin10_client`

- **ID / 行**：`FUN-6B5241464F` / `L168`（源码见本单元概览）
- **签名 / 返回**：`get_jin10_client()` → `Jin10McpClient`
- **职责**：As-built responsibility derived from `get_jin10_client` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / external-io / caller-thread
- **依赖**：Jin10McpClient、RuntimeError、_SESSION.get、client.connect、float、time.time
- **复杂度 / 风险**：分支 2；跨度 12 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-57be12ae7a"></a>

#### `jin10_call_tool`

- **ID / 行**：`FUN-57BE12AE7A` / `L182`（源码见本单元概览）
- **签名 / 返回**：`jin10_call_tool(name: str, arguments: dict[str, Any] | None=None)` → `Any`
- **职责**：As-built responsibility derived from `jin10_call_tool` and its owning unit.
- **依赖**：call_tool、get_jin10_client
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-fe5c27c113"></a>

### src/data/sources/macro.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FE5C27C113 |
| 源码 | [src/data/sources/macro.py](../../src/data/sources/macro.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Macro quotes for gold fundamentals — DXY, US10Y via TradingView. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 5 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[_daily_change](#fun-9a59422023) · [_gold_bias_from_change](#fun-e016877e87) · [fetch_dxy_quote](#fun-708b026267) · [fetch_us10y_quote](#fun-7bbbaadf8c) · [fetch_macro_quotes](#fun-777bc4df7e)

<a id="fun-9a59422023"></a>

#### `_daily_change`

- **ID / 行**：`FUN-9A59422023` / `L17`（源码见本单元概览）
- **签名 / 返回**：`_daily_change(df)` → `tuple[float, float, float]`
- **职责**：As-built responsibility derived from `_daily_change` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e016877e87"></a>

#### `_gold_bias_from_change`

- **ID / 行**：`FUN-E016877E87` / `L24`（源码见本单元概览）
- **签名 / 返回**：`_gold_bias_from_change(change_pct: float, *, invert: bool)` → `tuple[str, str]`
- **职责**：Return (impact text fragment, gold bias). invert=True for DXY (up hurts gold).
- **复杂度 / 风险**：分支 5；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-708b026267"></a>

#### `fetch_dxy_quote`

- **ID / 行**：`FUN-708B026267` / `L40`（源码见本单元概览）
- **签名 / 返回**：`fetch_dxy_quote()` → `MacroQuote | None`
- **职责**：As-built responsibility derived from `fetch_dxy_quote` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：MacroQuote、_daily_change、_gold_bias_from_change、fetch_symbol_daily、len、log.warning、round
- **复杂度 / 风险**：分支 4；跨度 25 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-7bbbaadf8c"></a>

#### `fetch_us10y_quote`

- **ID / 行**：`FUN-7BBBAADF8C` / `L67`（源码见本单元概览）
- **签名 / 返回**：`fetch_us10y_quote()` → `MacroQuote | None`
- **职责**：As-built responsibility derived from `fetch_us10y_quote` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：MacroQuote、_daily_change、_gold_bias_from_change、fetch_symbol_daily、len、log.warning、round
- **复杂度 / 风险**：分支 4；跨度 25 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-777bc4df7e"></a>

#### `fetch_macro_quotes`

- **ID / 行**：`FUN-777BC4DF7E` / `L94`（源码见本单元概览）
- **签名 / 返回**：`fetch_macro_quotes()` → `list[MacroQuote]`
- **职责**：As-built responsibility derived from `fetch_macro_quotes` and its owning unit.
- **依赖**：fn、quotes.append
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-603339624c"></a>

### src/data/sources/market.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-603339624C |
| 源码 | [src/data/sources/market.py](../../src/data/sources/market.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Market data source — TradingView OHLCV (primary). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[MarketDataSource.__init__](#fun-55497ef40f) · [MarketDataSource.fetch_evidence](#fun-eeff26c071)

<a id="fun-55497ef40f"></a>

#### `MarketDataSource.__init__`

- **ID / 行**：`FUN-55497EF40F` / `L16`（源码见本单元概览）
- **签名 / 返回**：`MarketDataSource.__init__(self, enriched: dict[str, pd.DataFrame])` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-eeff26c071"></a>

#### `MarketDataSource.fetch_evidence`

- **ID / 行**：`FUN-EEFF26C071` / `L19`（源码见本单元概览）
- **签名 / 返回**：`MarketDataSource.fetch_evidence(self)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `fetch_evidence` and its owning unit.
- **依赖**：EvidenceItem、abs、daily_metrics、float、items.append、min、pd.notna
- **复杂度 / 风险**：分支 3；跨度 37 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-58d6f95301"></a>

### src/data/sources/news.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-58D6F95301 |
| 源码 | [src/data/sources/news.py](../../src/data/sources/news.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | News data source — Jin10 MCP flash, articles, calendar. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 4 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[_bundle_to_external](#fun-495f172db6) · [external_to_evidence](#fun-1e1d7d437a) · [NewsDataSource.fetch_external](#fun-ad19eb744e) · [NewsDataSource.fetch_evidence](#fun-de57fb8e2a)

<a id="fun-495f172db6"></a>

#### `_bundle_to_external`

- **ID / 行**：`FUN-495F172DB6` / `L12`（源码见本单元概览）
- **签名 / 返回**：`_bundle_to_external(bundle: Jin10NewsBundle)` → `ExternalFactors`
- **职责**：As-built responsibility derived from `_bundle_to_external` and its owning unit.
- **依赖**：ExternalFactors、headlines_to_strings、list、sync_external_legacy_fields
- **复杂度 / 风险**：分支 2；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-1e1d7d437a"></a>

#### `external_to_evidence`

- **ID / 行**：`FUN-1E1D7D437A` / `L32`（源码见本单元概览）
- **签名 / 返回**：`external_to_evidence(ext: ExternalFactors, *, is_live: bool)` → `list[EvidenceItem]`
- **职责**：Build news evidence from pre-fetched ExternalFactors (no re-fetch).
- **依赖**：EvidenceItem、any、ev.display、items.append、min
- **复杂度 / 风险**：分支 10；跨度 57 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ad19eb744e"></a>

#### `NewsDataSource.fetch_external`

- **ID / 行**：`FUN-AD19EB744E` / `L94`（源码见本单元概览）
- **签名 / 返回**：`NewsDataSource.fetch_external(self)` → `ExternalFactors`
- **职责**：As-built responsibility derived from `fetch_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_bundle_to_external、fetch_jin10_bundle
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-de57fb8e2a"></a>

#### `NewsDataSource.fetch_evidence`

- **ID / 行**：`FUN-DE57FB8E2A` / `L97`（源码见本单元概览）
- **签名 / 返回**：`NewsDataSource.fetch_evidence(self)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `fetch_evidence` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_bundle_to_external、external_to_evidence、fetch_jin10_bundle
- **复杂度 / 风险**：分支 0；跨度 4 行；high
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-ba8df8a829"></a>

### src/data/sources/social.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-BA8DF8A829 |
| 源码 | [src/data/sources/social.py](../../src/data/sources/social.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Social sentiment — TradingView Ideas + Minds. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[SocialDataSource.fetch_external](#fun-95201e57fd) · [SocialDataSource.fetch_external_summary](#fun-99eafc0124) · [SocialDataSource.fetch_evidence](#fun-aad92ec141)

<a id="fun-95201e57fd"></a>

#### `SocialDataSource.fetch_external`

- **ID / 行**：`FUN-95201E57FD` / `L14`（源码见本单元概览）
- **签名 / 返回**：`SocialDataSource.fetch_external(self)` → `ExternalFactors`
- **职责**：As-built responsibility derived from `fetch_external` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：ExternalFactors、fetch_social_sentiment、refs.get
- **复杂度 / 风险**：分支 3；跨度 13 行；high
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-99eafc0124"></a>

#### `SocialDataSource.fetch_external_summary`

- **ID / 行**：`FUN-99EAFC0124` / `L28`（源码见本单元概览）
- **签名 / 返回**：`SocialDataSource.fetch_external_summary(self)` → `tuple[str, dict]`
- **职责**：As-built responsibility derived from `fetch_external_summary` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：fetch_social_sentiment
- **复杂度 / 风险**：分支 0；跨度 3 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-aad92ec141"></a>

#### `SocialDataSource.fetch_evidence`

- **ID / 行**：`FUN-AAD92EC141` / `L32`（源码见本单元概览）
- **签名 / 返回**：`SocialDataSource.fetch_evidence(self)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `fetch_evidence` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：EvidenceItem、fetch_social_sentiment、int、items.append、min、post.get、refs.get、str
- **复杂度 / 风险**：分支 2；跨度 32 行；high
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-b05f7affa4"></a>

### src/data/sources/social_feed.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B05F7AFFA4 |
| 源码 | [src/data/sources/social_feed.py](../../src/data/sources/social_feed.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Social sentiment — TradingView Ideas + Minds (XAUUSD community). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 11 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) |
| 验证状态 | selected |

#### 函数导航

[_tv_headers](#fun-caabb05bc5) · [_score_text](#fun-a3dfefa187) · [_flatten_ast](#fun-90feed0db0) · [_idea_bias](#fun-73c783a893) · [_mind_bias](#fun-b89e173f01) · [parse_tv_ideas](#fun-f4bb9ead13) · [parse_tv_minds](#fun-b5dc3ce070) · [_fetch_tv_json](#fun-cf2373671f) · [_collect_posts](#fun-b06d0a1526) · [_summarize](#fun-c35dff8bfe) · [fetch_social_sentiment](#fun-e5da3d3910)

<a id="fun-caabb05bc5"></a>

#### `_tv_headers`

- **ID / 行**：`FUN-CAABB05BC5` / `L29`（源码见本单元概览）
- **签名 / 返回**：`_tv_headers(symbol: str)` → `dict[str, str]`
- **职责**：As-built responsibility derived from `_tv_headers` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a3dfefa187"></a>

#### `_score_text`

- **ID / 行**：`FUN-A3DFEFA187` / `L41`（源码见本单元概览）
- **签名 / 返回**：`_score_text(text: str)` → `int`
- **职责**：As-built responsibility derived from `_score_text` and its owning unit.
- **依赖**：_BEAR_WORDS.findall、_BULL_WORDS.findall、len
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-90feed0db0"></a>

#### `_flatten_ast`

- **ID / 行**：`FUN-90FEED0DB0` / `L47`（源码见本单元概览）
- **签名 / 返回**：`_flatten_ast(node: Any)` → `str`
- **职责**：As-built responsibility derived from `_flatten_ast` and its owning unit.
- **依赖**：_flatten_ast、chunks.append、get、isinstance、join、node.get、str、strip
- **复杂度 / 风险**：分支 6；跨度 15 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-73c783a893"></a>

#### `_idea_bias`

- **ID / 行**：`FUN-73C783A893` / `L64`（源码见本单元概览）
- **签名 / 返回**：`_idea_bias(item: dict)` → `int`
- **职责**：As-built responsibility derived from `_idea_bias` and its owning unit.
- **依赖**：_DIRECTION_BIAS.get、_score_text、int、isinstance、item.get、str、symbol.get
- **复杂度 / 风险**：分支 3；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b89e173f01"></a>

#### `_mind_bias`

- **ID / 行**：`FUN-B89E173F01` / `L77`（源码见本单元概览）
- **签名 / 返回**：`_mind_bias(item: dict)` → `int`
- **职责**：As-built responsibility derived from `_mind_bias` and its owning unit.
- **依赖**：_flatten_ast、_score_text、item.get
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f4bb9ead13"></a>

#### `parse_tv_ideas`

- **ID / 行**：`FUN-F4BB9EAD13` / `L81`（源码见本单元概览）
- **签名 / 返回**：`parse_tv_ideas(payload: dict)` → `list[dict]`
- **职责**：As-built responsibility derived from `parse_tv_ideas` and its owning unit.
- **依赖**：_idea_bias、get、ideas.get、inner.get、int、isinstance、item.get、payload.get、posts.append、str、strip、user.get
- **复杂度 / 风险**：分支 7；跨度 26 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-b5dc3ce070"></a>

#### `parse_tv_minds`

- **ID / 行**：`FUN-B5DC3CE070` / `L109`（源码见本单元概览）
- **签名 / 返回**：`parse_tv_minds(payload: dict)` → `list[dict]`
- **职责**：As-built responsibility derived from `parse_tv_minds` and its owning unit.
- **依赖**：_flatten_ast、_mind_bias、author.get、get、int、isinstance、item.get、minds.get、payload.get、posts.append、str、strip
- **复杂度 / 风险**：分支 6；跨度 25 行；medium
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-cf2373671f"></a>

#### `_fetch_tv_json`

- **ID / 行**：`FUN-CF2373671F` / `L136`（源码见本单元概览）
- **签名 / 返回**：`_fetch_tv_json(path: str, symbol: str)` → `dict`
- **职责**：As-built responsibility derived from `_fetch_tv_json` and its owning unit.
- **依赖**：_tv_headers、get_json、isinstance
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-b06d0a1526"></a>

#### `_collect_posts`

- **ID / 行**：`FUN-B06D0A1526` / `L142`（源码见本单元概览）
- **签名 / 返回**：`_collect_posts(symbol: str)` → `list[dict]`
- **职责**：As-built responsibility derived from `_collect_posts` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_fetch_tv_json、parse_tv_ideas、parse_tv_minds、posts.extend
- **复杂度 / 风险**：分支 0；跨度 5 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-c35dff8bfe"></a>

#### `_summarize`

- **ID / 行**：`FUN-C35DFF8BFE` / `L149`（源码见本单元概览）
- **签名 / 返回**：`_summarize(posts: list[dict])` → `tuple[str, str, int, int]`
- **职责**：As-built responsibility derived from `_summarize` and its owning unit.
- **依赖**：int、len、max、post.get
- **复杂度 / 风险**：分支 6；跨度 43 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e5da3d3910"></a>

#### `fetch_social_sentiment`

- **ID / 行**：`FUN-E5DA3D3910` / `L194`（源码见本单元概览）
- **签名 / 返回**：`fetch_social_sentiment()` → `tuple[str, list[dict], dict]`
- **职责**：Return (summary text, evidence rows, refs).
- **依赖**：TV_SOCIAL_SYMBOL.strip、_collect_posts、_summarize、int、len、log.warning、p.get、post.get、samples.append、sorted、str、sum、upper
- **复杂度 / 风险**：分支 10；跨度 47 行；medium
- **测试 / 验证**：[tests/integration/test_external_apis.py](../../tests/integration/test_external_apis.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="unit-c1711535ca"></a>

### src/data/tradingview.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C1711535CA |
| 源码 | [src/data/tradingview.py](../../src/data/tradingview.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | TradingView historical data via tvDatafeed (unofficial WebSocket API). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 15 / 4 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py)、[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) |
| 验证状态 | selected |

#### 函数导航

[_read_system_proxy](#fun-00fc6618ed) · [_setup_proxy](#fun-39e0f0e515) · [get_last_error](#fun-147aba77bf) · [reset_client](#fun-bb3555eebf) · [_report_fetch](#fun-cfbe891cfe) · [_get_client](#fun-71eb929876) · [_normalize](#fun-e022026116) · [_resample](#fun-e5a0c6906a) · [compute_price_drift_1d](#fun-ce47bd6ad9) · [_fetch_bars](#fun-fc45e4816c) · [fetch_symbol_daily](#fun-7ee0f590bb) · [_fetch_htf_or_resample](#fun-c4f6abf085) · [_fetch_multi_timeframe_once](#fun-d99b48f1eb) · [fetch_multi_timeframe](#fun-440d380a28) · [source_label](#fun-b1230c7d4a)

<a id="fun-00fc6618ed"></a>

#### `_read_system_proxy`

- **ID / 行**：`FUN-00FC6618ED` / `L36`（源码见本单元概览）
- **签名 / 返回**：`_read_system_proxy()` → `str | None`
- **职责**：As-built responsibility derived from `_read_system_proxy` and its owning unit.
- **依赖**：read_system_proxy
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-39e0f0e515"></a>

#### `_setup_proxy`

- **ID / 行**：`FUN-39E0F0E515` / `L40`（源码见本单元概览）
- **签名 / 返回**：`_setup_proxy()` → `None`
- **职责**：Configure proxy for WebSocket connections from system settings.
- **依赖**：apply_system_proxy、log.info、redact_url
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-147aba77bf"></a>

#### `get_last_error`

- **ID / 行**：`FUN-147ABA77BF` / `L51`（源码见本单元概览）
- **签名 / 返回**：`get_last_error()` → `str | None`
- **职责**：As-built responsibility derived from `get_last_error` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-bb3555eebf"></a>

#### `reset_client`

- **ID / 行**：`FUN-BB3555EEBF` / `L55`（源码见本单元概览）
- **签名 / 返回**：`reset_client()` → `None`
- **职责**：As-built responsibility derived from `reset_client` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / global-state / caller-thread
- **依赖**：log.debug
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="fun-cfbe891cfe"></a>

#### `_report_fetch`

- **ID / 行**：`FUN-CFBE891CFE` / `L62`（源码见本单元概览）
- **签名 / 返回**：`_report_fetch(detail: str)` → `None`
- **职责**：As-built responsibility derived from `_report_fetch` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：get_progress、update
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-71eb929876"></a>

#### `_get_client`

- **ID / 行**：`FUN-71EB929876` / `L66`（源码见本单元概览）
- **签名 / 返回**：`_get_client()` → `runtime/inferred`
- **职责**：As-built responsibility derived from `_get_client` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / global-state / caller-thread
- **依赖**：TvDatafeed、log.info
- **复杂度 / 风险**：分支 2；跨度 12 行；low
- **测试 / 验证**：[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="fun-e022026116"></a>

#### `_normalize`

- **ID / 行**：`FUN-E022026116` / `L80`（源码见本单元概览）
- **签名 / 返回**：`_normalize(df: pd.DataFrame | None)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `_normalize` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / filesystem / caller-thread
- **依赖**：ValueError、copy、df.copy、out.rename、pd.to_datetime、rename.items
- **复杂度 / 风险**：分支 4；跨度 22 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e5a0c6906a"></a>

#### `_resample`

- **ID / 行**：`FUN-E5A0C6906A` / `L104`（源码见本单元概览）
- **签名 / 返回**：`_resample(df: pd.DataFrame, rule: str)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `_resample` and its owning unit.
- **依赖**：agg、df.resample、ohlcv.dropna
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ce47bd6ad9"></a>

#### `compute_price_drift_1d`

- **ID / 行**：`FUN-CE47BD6AD9` / `L111`（源码见本单元概览）
- **签名 / 返回**：`compute_price_drift_1d(df_5m: pd.DataFrame, df_1d: pd.DataFrame)` → `float`
- **职责**：Difference between independent 1d close and 5m-resampled 1d close (F-005).
- **依赖**：_resample、float、round
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fc45e4816c"></a>

#### `_fetch_bars`

- **ID / 行**：`FUN-FC45E4816C` / `L120`（源码见本单元概览）
- **签名 / 返回**：`_fetch_bars(interval: 'Interval', n_bars: int, *, label: str, retries: int | None=None, exchange: str | None=None, symbol: str | None=None, report_progress: bool=True)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `_fetch_bars` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / global-state / caller-thread
- **依赖**：RuntimeError、_get_client、_normalize、_report_fetch、get_hist、len、log.debug、log.info、log.warning、range、reset_client、str、strftime、time.sleep
- **复杂度 / 风险**：分支 7；跨度 72 行；medium
- **测试 / 验证**：[tests/unit/test_tradingview_retry.py](../../tests/unit/test_tradingview_retry.py) · direct-dynamic

<a id="fun-7ee0f590bb"></a>

#### `fetch_symbol_daily`

- **ID / 行**：`FUN-7EE0F590BB` / `L194`（源码见本单元概览）
- **签名 / 返回**：`fetch_symbol_daily(exchange: str, symbol: str, *, n_bars: int=5, label: str | None=None)` → `pd.DataFrame`
- **职责**：Fetch daily bars for a non-primary symbol (e.g. DXY) without pipeline fetch progress noise.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_fetch_bars
- **复杂度 / 风险**：分支 0；跨度 19 行；high
- **测试 / 验证**：[tests/unit/test_external_sources.py](../../tests/unit/test_external_sources.py) · direct-dynamic

<a id="fun-c4f6abf085"></a>

#### `_fetch_htf_or_resample`

- **ID / 行**：`FUN-C4F6ABF085` / `L219`（源码见本单元概览）
- **签名 / 返回**：`_fetch_htf_or_resample(interval: 'Interval', *, n_bars: int, label: str, df_5m: pd.DataFrame, resample_rule: str)` → `pd.DataFrame`
- **职责**：Prefer native HTF bars so Fixed-360 lookback is reachable; else resample 5m.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_fetch_bars、_report_fetch、_resample、log.warning、time.sleep
- **复杂度 / 风险**：分支 1；跨度 16 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-d99b48f1eb"></a>

#### `_fetch_multi_timeframe_once`

- **ID / 行**：`FUN-D99B48F1EB` / `L237`（源码见本单元概览）
- **签名 / 返回**：`_fetch_multi_timeframe_once()` → `dict[str, pd.DataFrame]`
- **职责**：As-built responsibility derived from `_fetch_multi_timeframe_once` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_fetch_bars、_fetch_htf_or_resample、_report_fetch、float、len、log.info、out.items、time.sleep
- **复杂度 / 风险**：分支 0；跨度 46 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-440d380a28"></a>

#### `fetch_multi_timeframe`

- **ID / 行**：`FUN-440D380A28` / `L285`（源码见本单元概览）
- **签名 / 返回**：`fetch_multi_timeframe()` → `dict[str, pd.DataFrame]`
- **职责**：Fetch 5m + native HTF (≥360) + 1d; HTF falls back to 5m resample on failure.
- **异常 / 副作用 / 并发**：RuntimeError / external-io / caller-thread
- **依赖**：RuntimeError、_fetch_multi_timeframe_once、_report_fetch、log.info、log.warning、range、reset_client、time.sleep
- **复杂度 / 风险**：分支 3；跨度 25 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-b1230c7d4a"></a>

#### `source_label`

- **ID / 行**：`FUN-B1230C7D4A` / `L312`（源码见本单元概览）
- **签名 / 返回**：`source_label()` → `str`
- **职责**：As-built responsibility derived from `source_label` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) · direct-dynamic

<a id="unit-62a1aff305"></a>

### src/data/url_redact.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-62A1AFF305 |
| 源码 | [src/data/url_redact.py](../../src/data/url_redact.py) |
| 架构组件 | ARC-DATA — 行情与外部数据 |
| 职责 | Redact secrets from URLs before logging. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-001](./SWE.1-software-requirements.md#swr-data-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-INTEGRATION-EXTERNAL](./SWE.5-integration-testing.md#vm-integration-external) |
| 动态测试 | [tests/unit/test_url_redact.py](../../tests/unit/test_url_redact.py) |
| 验证状态 | selected |

#### 函数导航

[redact_url](#fun-5d2f35cb3b)

<a id="fun-5d2f35cb3b"></a>

#### `redact_url`

- **ID / 行**：`FUN-5D2F35CB3B` / `L8`（源码见本单元概览）
- **签名 / 返回**：`redact_url(url: str)` → `str`
- **职责**：Strip userinfo and query params; keep scheme, host, port.
- **依赖**：url.strip、urlparse、urlunparse
- **复杂度 / 风险**：分支 2；跨度 10 行；medium
- **测试 / 验证**：[tests/unit/test_url_redact.py](../../tests/unit/test_url_redact.py) · direct-dynamic

<a id="arc-indicators"></a>

## ARC-INDICATORS — 指标计算

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/indicators/__init__.py](#unit-7d2cf26834) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |
| [src/indicators/technical.py](#unit-2f8c299c5b) | 10 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [src/indicators/verify.py](#unit-d35a8017fe) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |

<a id="unit-7d2cf26834"></a>

### src/indicators/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7D2CF26834 |
| 源码 | [src/indicators/__init__.py](../../src/indicators/__init__.py) |
| 架构组件 | ARC-INDICATORS — 指标计算 |
| 职责 | 继承 指标计算 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-2f8c299c5b"></a>

### src/indicators/technical.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F8C299C5B |
| 源码 | [src/indicators/technical.py](../../src/indicators/technical.py) |
| 架构组件 | ARC-INDICATORS — 指标计算 |
| 职责 | Technical indicators: EMA, VWAP, momentum, volatility, Fibonacci. |
| 关联需求 | [SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 10 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) |
| 验证状态 | selected |

#### 函数导航

[add_emas](#fun-8f7e8730d6) · [add_vwap](#fun-c3db0f8450) · [add_atr](#fun-4d1a54987d) · [add_rsi](#fun-3901170d43) · [add_macd](#fun-5299aa4622) · [add_adx](#fun-a8f0fc0306) · [enrich](#fun-3f2d66c862) · [indicator_values](#fun-d44171a8a2) · [ema_relation](#fun-1fcd39f6e9) · [fibonacci_levels](#fun-6537a68fb4)

<a id="fun-8f7e8730d6"></a>

#### `add_emas`

- **ID / 行**：`FUN-8F7E8730D6` / `L10`（源码见本单元概览）
- **签名 / 返回**：`add_emas(df: pd.DataFrame, periods: tuple[int, ...]=(20, 50, 610))` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `add_emas` and its owning unit.
- **依赖**：df.copy、ewm、mean
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c3db0f8450"></a>

#### `add_vwap`

- **ID / 行**：`FUN-C3DB0F8450` / `L17`（源码见本单元概览）
- **签名 / 返回**：`add_vwap(df: pd.DataFrame)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `add_vwap` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：cumsum、df.copy、fillna、replace、tp_vol.groupby、vol.groupby
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4d1a54987d"></a>

#### `add_atr`

- **ID / 行**：`FUN-4D1A54987D` / `L27`（源码见本单元概览）
- **签名 / 返回**：`add_atr(df: pd.DataFrame, period: int=14)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `add_atr` and its owning unit.
- **依赖**：abs、df.copy、max、mean、pd.concat、shift、tr.rolling
- **复杂度 / 风险**：分支 0；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3901170d43"></a>

#### `add_rsi`

- **ID / 行**：`FUN-3901170D43` / `L42`（源码见本单元概览）
- **签名 / 返回**：`add_rsi(df: pd.DataFrame, period: int=14)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `add_rsi` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：delta.clip、df.copy、diff、loss.replace、mean、rolling、rsi.mask
- **复杂度 / 风险**：分支 0；跨度 11 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5299aa4622"></a>

#### `add_macd`

- **ID / 行**：`FUN-5299AA4622` / `L55`（源码见本单元概览）
- **签名 / 返回**：`add_macd(df: pd.DataFrame, *, fast: int=12, slow: int=26, signal: int=9)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `add_macd` and its owning unit.
- **依赖**：df.copy、ewm、mean
- **复杂度 / 风险**：分支 0；跨度 14 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a8f0fc0306"></a>

#### `add_adx`

- **ID / 行**：`FUN-A8F0FC0306` / `L71`（源码见本单元概览）
- **签名 / 返回**：`add_adx(df: pd.DataFrame, period: int=14)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `add_adx` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：abs、df.copy、diff、down_move.where、dx.rolling、max、mean、minus_dm.rolling、pd.concat、plus_dm.rolling、replace、shift、sum、tr.rolling、tr_sum.replace、up_move.where
- **复杂度 / 风险**：分支 0；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3f2d66c862"></a>

#### `enrich`

- **ID / 行**：`FUN-3F2D66C862` / `L95`（源码见本单元概览）
- **签名 / 返回**：`enrich(df: pd.DataFrame)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `enrich` and its owning unit.
- **依赖**：add_adx、add_atr、add_emas、add_macd、add_rsi、add_vwap
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="fun-d44171a8a2"></a>

#### `indicator_values`

- **ID / 行**：`FUN-D44171A8A2` / `L99`（源码见本单元概览）
- **签名 / 返回**：`indicator_values(row: pd.Series)` → `dict[str, float | None]`
- **职责**：As-built responsibility derived from `indicator_values` and its owning unit.
- **依赖**：float、pd.isna、round
- **复杂度 / 风险**：分支 2；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-1fcd39f6e9"></a>

#### `ema_relation`

- **ID / 行**：`FUN-1FCD39F6E9` / `L109`（源码见本单元概览）
- **签名 / 返回**：`ema_relation(price: float, row: pd.Series)` → `dict[str, str]`
- **职责**：As-built responsibility derived from `ema_relation` and its owning unit.
- **依赖**：float、pd.isna
- **复杂度 / 风险**：分支 4；跨度 14 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py) · direct-dynamic

<a id="fun-6537a68fb4"></a>

#### `fibonacci_levels`

- **ID / 行**：`FUN-6537A68FB4` / `L125`（源码见本单元概览）
- **签名 / 返回**：`fibonacci_levels(swing_high: float, swing_low: float)` → `list[dict]`
- **职责**：Retracement from high to low (bearish move).
- **依赖**：levels.append、round
- **复杂度 / 风险**：分支 1；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py) · direct-dynamic

<a id="unit-d35a8017fe"></a>

### src/indicators/verify.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D35A8017FE |
| 源码 | [src/indicators/verify.py](../../src/indicators/verify.py) |
| 架构组件 | ARC-INDICATORS — 指标计算 |
| 职责 | Indicator sanity checks for manual verification against TradingView. |
| 关联需求 | [SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py) |
| 验证状态 | selected |

#### 函数导航

[indicator_snapshot](#fun-c3ec67606c) · [indicator_table_rows](#fun-44ba63c6e8)

<a id="fun-c3ec67606c"></a>

#### `indicator_snapshot`

- **ID / 行**：`FUN-C3EC67606C` / `L10`（源码见本单元概览）
- **签名 / 返回**：`indicator_snapshot(df: pd.DataFrame, timeframe: str)` → `dict`
- **职责**：Return last-bar indicator values and basic sanity notes.
- **依赖**：abs、ema_relation、fillna、float、indicator_values、int、len、notes.append、pd.notna、round、row.get、row.update、str、sum
- **复杂度 / 风险**：分支 13；跨度 58 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py) · direct-dynamic

<a id="fun-44ba63c6e8"></a>

#### `indicator_table_rows`

- **ID / 行**：`FUN-44BA63C6E8` / `L70`（源码见本单元概览）
- **签名 / 返回**：`indicator_table_rows(snapshots: list[dict])` → `list[dict]`
- **职责**：Flatten snapshots for st.table display.
- **依赖**：rows.append、s.get
- **复杂度 / 风险**：分支 2；跨度 26 行；medium
- **测试 / 验证**：[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py) · direct-dynamic

<a id="arc-analysis"></a>

## ARC-ANALYSIS — 事实、结构、信号与报告门禁

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/analysis/__init__.py](#unit-cf43fe46e5) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/audit_summary.py](#unit-9f95d55376) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/chart_sr_filters.py](#unit-271badecbe) | 4 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/chart_zone_filters.py](#unit-070aa8511c) | 8 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/claim_eligibility.py](#unit-67d22a7c31) | 14 | 14 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/data_freshness.py](#unit-3549e9d9b7) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/dgt_price_action.py](#unit-7dfc57faf9) | 10 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/display_labels.py](#unit-3b1598dc1b) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/fact_registry.py](#unit-60e70e7439) | 16 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/field_glossary.py](#unit-c37864f306) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/ict_pa.py](#unit-3962aaac44) | 7 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/level_validator.py](#unit-a9ae5e6696) | 7 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/luxalgo_smc.py](#unit-2f7fedba6f) | 15 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/narrative_combine.py](#unit-4f106aec16) | 15 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/narrative_facts.py](#unit-b5b5d80eb7) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/narrative_sections.py](#unit-0d14c54b60) | 28 | 4 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/plan_signals.py](#unit-406cec1297) | 20 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/price_action_facts.py](#unit-daf97d09e5) | 7 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/proximity.py](#unit-ce01c0290c) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_engine.py](#unit-dad8a91ff9) | 44 | 8 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_facts.py](#unit-cd6da8c4a3) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_invariant_gate.py](#unit-1aecfa1072) | 4 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_invariants.py](#unit-70bd327d9d) | 13 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/report_reliability.py](#unit-07e7315842) | 11 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/risk_gates.py](#unit-0cc0e8d72a) | 6 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/signal_geometry.py](#unit-84723142fa) | 3 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/signal_identity.py](#unit-c8f58d21e1) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/technical_context.py](#unit-7faaa8edca) | 17 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/analysis/tf_snapshot.py](#unit-ebf42549f9) | 4 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-cf43fe46e5"></a>

### src/analysis/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CF43FE46E5 |
| 源码 | [src/analysis/__init__.py](../../src/analysis/__init__.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | 继承 事实、结构、信号与报告门禁 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-9f95d55376"></a>

### src/analysis/audit_summary.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9F95D55376 |
| 源码 | [src/analysis/audit_summary.py](../../src/analysis/audit_summary.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Per-run audit summary for Codex / regression review. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) |
| 验证状态 | selected |

#### 函数导航

[_hash_payload](#fun-18bf7fc28a) · [_llm_usage_summary](#fun-3041827ff4) · [build_audit_summary](#fun-5b705f2cac)

<a id="fun-18bf7fc28a"></a>

#### `_hash_payload`

- **ID / 行**：`FUN-18BF7FC28A` / `L10`（源码见本单元概览）
- **签名 / 返回**：`_hash_payload(payload: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_hash_payload` and its owning unit.
- **依赖**：hashlib.sha256、hexdigest、json.dumps、raw.encode
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-3041827ff4"></a>

#### `_llm_usage_summary`

- **ID / 行**：`FUN-3041827FF4` / `L15`（源码见本单元概览）
- **签名 / 返回**：`_llm_usage_summary(llm_io: list[dict[str, Any]])` → `dict[str, Any]`
- **职责**：Compact per-run LLM telemetry for Runtime Ledger (Issue #37).
- **依赖**：a.get、any、int、len、r.get、retry_reasons.append、round、sum
- **复杂度 / 风险**：分支 5；跨度 32 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5b705f2cac"></a>

#### `build_audit_summary`

- **ID / 行**：`FUN-5B705F2CAC` / `L49`（源码见本单元概览）
- **签名 / 返回**：`build_audit_summary(report: dict[str, Any], *, decision: Any | None=None, stage_meta: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：Compact audit block stored in report meta.
- **依赖**：_hash_payload、_llm_usage_summary、decision.to_dict、decision_dict.get、get、hasattr、isinstance、meta.get、narrative_audit.items、next、report.get、row.get、s.get、top_audit.get、v.get、val.get
- **复杂度 / 风险**：分支 1；跨度 59 行；medium
- **测试 / 验证**：[tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) · direct-dynamic

<a id="unit-271badecbe"></a>

### src/analysis/chart_sr_filters.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-271BADECBE |
| 源码 | [src/analysis/chart_sr_filters.py](../../src/analysis/chart_sr_filters.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Filter DGT S/R levels for chart display (5m main + 4h/1h/15m strips). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) |
| 验证状态 | selected |

#### 函数导航

[_fmt_price](#fun-615e3b9de5) · [_short_chart_title](#fun-cbd491e1bc) · [_merge_nearby](#fun-fbc037e567) · [visible_sr_price_lines](#fun-449394678b)

<a id="fun-615e3b9de5"></a>

#### `_fmt_price`

- **ID / 行**：`FUN-615E3B9DE5` / `L22`（源码见本单元概览）
- **签名 / 返回**：`_fmt_price(price: float)` → `str`
- **职责**：As-built responsibility derived from `_fmt_price` and its owning unit.
- **依赖**：abs、int、round、str
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-cbd491e1bc"></a>

#### `_short_chart_title`

- **ID / 行**：`FUN-CBD491E1BC` / `L29`（源码见本单元概览）
- **签名 / 返回**：`_short_chart_title(lvl: SrLevel)` → `str`
- **职责**：Compact right-axis label to reduce overlap.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：len、replace、strip
- **复杂度 / 风险**：分支 3；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fbc037e567"></a>

#### `_merge_nearby`

- **ID / 行**：`FUN-FBC037E567` / `L47`（源码见本单元概览）
- **签名 / 返回**：`_merge_nearby(levels: list[SrLevel])` → `list[SrLevel]`
- **职责**：Keep the higher-priority level when prices are within tolerance.
- **依赖**：_KIND_PRIORITY.get、abs、enumerate、kept.append、sorted
- **复杂度 / 风险**：分支 6；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-449394678b"></a>

#### `visible_sr_price_lines`

- **ID / 行**：`FUN-449394678B` / `L69`（源码见本单元概览）
- **签名 / 返回**：`visible_sr_price_lines(sr_levels: list[SrLevel] | list[dict[str, Any]], plot_df: pd.DataFrame, *, max_lines: int=_MAX_CHART_LINES, current_price: float | None=None)` → `list[dict[str, Any]]`
- **职责**：Pick nearest, highest-signal S/R lines for the visible range.
- **依赖**：SrLevel、_KIND_PRIORITY.get、_SR_COLORS.get、_fmt_price、_merge_nearby、_short_chart_title、abs、colors.get、float、isinstance、len、lines.append、max、min、parsed.append、pd.Timestamp、picked.extend、row.get、sorted、str
- **复杂度 / 风险**：分支 8；跨度 69 行；medium
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="unit-070aa8511c"></a>

### src/analysis/chart_zone_filters.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-070AA8511C |
| 源码 | [src/analysis/chart_zone_filters.py](../../src/analysis/chart_zone_filters.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Filter FVG/OB by the same visible candle range used on charts. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[chart_plot_df](#fun-5916a45360) · [chart_price_bounds](#fun-77a17f101c) · [zone_overlaps_chart_range](#fun-2b036568fa) · [_align_ts](#fun-feca409ef6) · [visible_order_blocks](#fun-f8e5f51975) · [visible_active_fvgs](#fun-52b596d6f3) · [visible_zone_snapshots](#fun-75356974bc) · [visible_zones_for_chart](#fun-19453dd010)

<a id="fun-5916a45360"></a>

#### `chart_plot_df`

- **ID / 行**：`FUN-5916A45360` / `L18`（源码见本单元概览）
- **签名 / 返回**：`chart_plot_df(df: pd.DataFrame, bars: int)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `chart_plot_df` and its owning unit.
- **依赖**：copy、df.tail、max
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-77a17f101c"></a>

#### `chart_price_bounds`

- **ID / 行**：`FUN-77A17F101C` / `L22`（源码见本单元概览）
- **签名 / 返回**：`chart_price_bounds(plot_df: pd.DataFrame)` → `tuple[float, float]`
- **职责**：As-built responsibility derived from `chart_price_bounds` and its owning unit.
- **依赖**：float、max、min
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2b036568fa"></a>

#### `zone_overlaps_chart_range`

- **ID / 行**：`FUN-2B036568FA` / `L26`（源码见本单元概览）
- **签名 / 返回**：`zone_overlaps_chart_range(low: float, high: float, plot_df: pd.DataFrame)` → `bool`
- **职责**：True when zone overlaps the high/low span of visible candles.
- **依赖**：chart_price_bounds
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-feca409ef6"></a>

#### `_align_ts`

- **ID / 行**：`FUN-FECA409EF6` / `L33`（源码见本单元概览）
- **签名 / 返回**：`_align_ts(ts: pd.Timestamp, ref_index: pd.DatetimeIndex)` → `pd.Timestamp`
- **职责**：As-built responsibility derived from `_align_ts` and its owning unit.
- **依赖**：pd.Timestamp、t.tz_convert、t.tz_localize
- **复杂度 / 风险**：分支 3；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f8e5f51975"></a>

#### `visible_order_blocks`

- **ID / 行**：`FUN-F8E5F51975` / `L44`（源码见本单元概览）
- **签名 / 返回**：`visible_order_blocks(analysis: TimeframeAnalysis, plot_df: pd.DataFrame, *, max_zones: int=MAX_OB_ZONES)` → `list[OrderBlock]`
- **职责**：As-built responsibility derived from `visible_order_blocks` and its owning unit.
- **依赖**：_align_ts、float、plot_df.index.max、visible.sort、zone_overlaps_chart_range
- **复杂度 / 风险**：分支 0；跨度 15 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-52b596d6f3"></a>

#### `visible_active_fvgs`

- **ID / 行**：`FUN-52B596D6F3` / `L61`（源码见本单元概览）
- **签名 / 返回**：`visible_active_fvgs(analysis: TimeframeAnalysis, plot_df: pd.DataFrame, *, max_zones: int=MAX_FVG_ZONES)` → `list[FairValueGap]`
- **职责**：As-built responsibility derived from `visible_active_fvgs` and its owning unit.
- **依赖**：_align_ts、float、plot_df.index.max、visible.sort、zone_overlaps_chart_range
- **复杂度 / 风险**：分支 0；跨度 15 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-75356974bc"></a>

#### `visible_zone_snapshots`

- **ID / 行**：`FUN-75356974BC` / `L78`（源码见本单元概览）
- **签名 / 返回**：`visible_zone_snapshots(analysis: TimeframeAnalysis, plot_df: pd.DataFrame, *, ob_limit: int=MAX_OB_ZONES, fvg_limit: int=MAX_FVG_ZONES)` → `tuple[list[dict[str, object]], list[dict[str, object]]]`
- **职责**：Dict snapshots for report text — same rules as chart overlays.
- **依赖**：visible_active_fvgs、visible_order_blocks
- **复杂度 / 风险**：分支 0；跨度 17 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-19453dd010"></a>

#### `visible_zones_for_chart`

- **ID / 行**：`FUN-19453DD010` / `L97`（源码见本单元概览）
- **签名 / 返回**：`visible_zones_for_chart(analysis: TimeframeAnalysis, df: pd.DataFrame, *, bars: int, ob_limit: int=MAX_OB_ZONES, fvg_limit: int=MAX_FVG_ZONES)` → `tuple[list[dict[str, object]], list[dict[str, object]]]`
- **职责**：As-built responsibility derived from `visible_zones_for_chart` and its owning unit.
- **依赖**：chart_plot_df、visible_zone_snapshots
- **复杂度 / 风险**：分支 0；跨度 10 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-67d22a7c31"></a>

### src/analysis/claim_eligibility.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-67D22A7C31 |
| 源码 | [src/analysis/claim_eligibility.py](../../src/analysis/claim_eligibility.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Citation eligibility for technical claims used as execution rationale. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 14 / 14 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

[ClaimAudit.to_dict](#fun-43c4b237b7) · [ClaimAudit.allows_execution_authorization](#fun-039e702d1a) · [_overlap_amount](#fun-103fa43ff4) · [_zones_near](#fun-49e61c75ae) · [_reaction_index](#fun-ee4367894d) · [_collect_fvgs](#fun-ead4b05709) · [technical_claim_fact_catalog](#fun-8edd654d1e) · [_fact_entity_for_ids](#fun-ae9b1e87f2) · [_fact_direction_supports_trade](#fun-4fb8932cb6) · [_relationship_holds](#fun-a094dfd75f) · [_aligned_fvgs](#fun-582a749531) · [_counter_fvgs](#fun-aff197d9f4) · [adjudicate_level_proposal_claim](#fun-d280cc6eb5) · [claim_allows_execution_authorization](#fun-972700d46f)

<a id="fun-43c4b237b7"></a>

#### `ClaimAudit.to_dict`

- **ID / 行**：`FUN-43C4B237B7` / `L44`（源码见本单元概览）
- **签名 / 返回**：`ClaimAudit.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-039e702d1a"></a>

#### `ClaimAudit.allows_execution_authorization`

- **ID / 行**：`FUN-039E702D1A` / `L48`（源码见本单元概览）
- **签名 / 返回**：`ClaimAudit.allows_execution_authorization(self)` → `bool`
- **职责**：As-built responsibility derived from `allows_execution_authorization` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py) · direct-dynamic

<a id="fun-103fa43ff4"></a>

#### `_overlap_amount`

- **ID / 行**：`FUN-103FA43FF4` / `L52`（源码见本单元概览）
- **签名 / 返回**：`_overlap_amount(a_lo: float, a_hi: float, b_lo: float, b_hi: float)` → `float`
- **职责**：As-built responsibility derived from `_overlap_amount` and its owning unit.
- **依赖**：max、min
- **复杂度 / 风险**：分支 0；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-49e61c75ae"></a>

#### `_zones_near`

- **ID / 行**：`FUN-49E61C75AE` / `L58`（源码见本单元概览）
- **签名 / 返回**：`_zones_near(a_lo: float, a_hi: float, b_lo: float, b_hi: float, *, tol: float)` → `bool`
- **职责**：As-built responsibility derived from `_zones_near` and its owning unit.
- **依赖**：_overlap_amount、max、min
- **复杂度 / 风险**：分支 3；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-ee4367894d"></a>

#### `_reaction_index`

- **ID / 行**：`FUN-EE4367894D` / `L69`（源码见本单元概览）
- **签名 / 返回**：`_reaction_index(reactions: list[dict[str, Any]] | None)` → `dict[str, dict[str, Any]]`
- **职责**：As-built responsibility derived from `_reaction_index` and its owning unit.
- **依赖**：row.get、str、strip
- **复杂度 / 风险**：分支 2；跨度 7 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-ead4b05709"></a>

#### `_collect_fvgs`

- **ID / 行**：`FUN-EAD4B05709` / `L78`（源码见本单元概览）
- **签名 / 返回**：`_collect_fvgs(analyses: dict[str, TimeframeAnalysis])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_collect_fvgs` and its owning unit.
- **依赖**：abs、analyses.items、enumerate、float、isinstance、round、rows.append
- **复杂度 / 风险**：分支 6；跨度 25 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-8edd654d1e"></a>

#### `technical_claim_fact_catalog`

- **ID / 行**：`FUN-8EDD654D1E` / `L105`（源码见本单元概览）
- **签名 / 返回**：`technical_claim_fact_catalog(ctx: MarketContext, *, price_action: dict[str, Any] | None=None)` → `list[dict[str, Any]]`
- **职责**：Return the canonical technical facts an LLM may bind into a reaction.
- **依赖**：block.get、build_price_action_summaries、ctx.analyses.items、enumerate、float、isinstance、level.get、lower、pa_blocks.items、profile.get、rows.append、sorted、str
- **复杂度 / 风险**：分支 16；跨度 92 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-ae9b1e87f2"></a>

#### `_fact_entity_for_ids`

- **ID / 行**：`FUN-AE9B1E87F2` / `L199`（源码见本单元概览）
- **签名 / 返回**：`_fact_entity_for_ids(fact_ids: list[str], catalog: list[dict[str, Any]])` → `dict[str, Any] | None`
- **职责**：As-built responsibility derived from `_fact_entity_for_ids` and its owning unit.
- **依赖**：row.get、str、strip
- **复杂度 / 风险**：分支 3；跨度 11 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-4fb8932cb6"></a>

#### `_fact_direction_supports_trade`

- **ID / 行**：`FUN-4FB8932CB6` / `L212`（源码见本单元概览）
- **签名 / 返回**：`_fact_direction_supports_trade(fact: dict[str, Any], direction: str)` → `bool`
- **职责**：As-built responsibility derived from `_fact_direction_supports_trade` and its owning unit.
- **依赖**：fact.get、lower、str
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-a094dfd75f"></a>

#### `_relationship_holds`

- **ID / 行**：`FUN-A094DFD75F` / `L218`（源码见本单元概览）
- **签名 / 返回**：`_relationship_holds(relation_type: str, left: dict[str, Any], right: dict[str, Any])` → `bool`
- **职责**：As-built responsibility derived from `_relationship_holds` and its owning unit.
- **依赖**：_zones_near、float、left.get、max、min、right.get、str
- **复杂度 / 风险**：分支 3；跨度 32 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-582a749531"></a>

#### `_aligned_fvgs`

- **ID / 行**：`FUN-582A749531` / `L252`（源码见本单元概览）
- **签名 / 返回**：`_aligned_fvgs(*, direction: str, entry_low: float, entry_high: float, zones: list[dict[str, Any]])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_aligned_fvgs` and its owning unit.
- **依赖**：_zones_near
- **复杂度 / 风险**：分支 1；跨度 14 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-aff197d9f4"></a>

#### `_counter_fvgs`

- **ID / 行**：`FUN-AFF197D9F4` / `L268`（源码见本单元概览）
- **签名 / 返回**：`_counter_fvgs(*, direction: str, entry_low: float, entry_high: float, zones: list[dict[str, Any]])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_counter_fvgs` and its owning unit.
- **依赖**：_zones_near
- **复杂度 / 风险**：分支 1；跨度 14 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-d280cc6eb5"></a>

#### `adjudicate_level_proposal_claim`

- **ID / 行**：`FUN-D280CC6EB5` / `L284`（源码见本单元概览）
- **签名 / 返回**：`adjudicate_level_proposal_claim(proposal: LevelProposal, ctx: MarketContext, *, level_reactions: list[dict[str, Any]] | None=None)` → `ClaimAudit`
- **职责**：Decide whether a level proposal's technical thesis may drive execution.
- **依赖**：ClaimAudit、_aligned_fvgs、_collect_fvgs、_counter_fvgs、_fact_direction_supports_trade、_fact_entity_for_ids、_reaction_index、_relationship_holds、_zones_near、any、audit_row.items、bool、counterevidence.append、entry_bound_keys.add、fact_ids.append、fact_ids.extend、float、isinstance、issubset、left.get
- **复杂度 / 风险**：分支 33；跨度 274 行；high
- **测试 / 验证**：[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py) · direct-dynamic

<a id="fun-972700d46f"></a>

#### `claim_allows_execution_authorization`

- **ID / 行**：`FUN-972700D46F` / `L560`（源码见本单元概览）
- **签名 / 返回**：`claim_allows_execution_authorization(signal_or_meta: dict[str, Any] | None)` → `bool`
- **职责**：Rule/engine signals default allow; LLM claims must be core_execution.
- **依赖**：signal_or_meta.get
- **复杂度 / 风险**：分支 2；跨度 9 行；high
- **测试 / 验证**：[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py) · direct-dynamic

<a id="unit-3549e9d9b7"></a>

### src/analysis/data_freshness.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3549E9D9B7 |
| 源码 | [src/analysis/data_freshness.py](../../src/analysis/data_freshness.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Data freshness / as-of contract for reports and analyst inputs. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_data_freshness.py](../../tests/unit/test_data_freshness.py) |
| 验证状态 | selected |

#### 函数导航

[_bar_timestamp](#fun-2b7eb34519) · [build_data_as_of](#fun-4734af977b)

<a id="fun-2b7eb34519"></a>

#### `_bar_timestamp`

- **ID / 行**：`FUN-2B7EB34519` / `L18`（源码见本单元概览）
- **签名 / 返回**：`_bar_timestamp(df: pd.DataFrame | None)` → `datetime | None`
- **职责**：As-built responsibility derived from `_bar_timestamp` and its owning unit.
- **依赖**：isinstance、ts.to_pydatetime、ts.tz_localize
- **复杂度 / 风险**：分支 3；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4734af977b"></a>

#### `build_data_as_of`

- **ID / 行**：`FUN-4734AF977B` / `L29`（源码见本单元概览）
- **签名 / 返回**：`build_data_as_of(raw: dict[str, pd.DataFrame], *, now: datetime | None=None)` → `dict[str, Any]`
- **职责**：Summarize bar freshness and whether prices are safe to treat as live.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：_bar_timestamp、datetime.now、last_bar.replace、last_bar.strftime、len、log.info、now.strftime、now.weekday、raw.get、round、total_seconds、warnings.append
- **复杂度 / 风险**：分支 9；跨度 50 行；medium
- **测试 / 验证**：[tests/unit/test_data_freshness.py](../../tests/unit/test_data_freshness.py) · direct-dynamic

<a id="unit-7dfc57faf9"></a>

### src/analysis/dgt_price_action.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7DFC57FAF9 |
| 源码 | [src/analysis/dgt_price_action.py](../../src/analysis/dgt_price_action.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | DGT Price Action — volume/price S&R, spikes, volatility, volume profile. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 10 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) |
| 验证状态 | selected |

#### 函数导航

[_nz_volume](#fun-a1eb4c5f6a) · [_volume_usable](#fun-8c5d73d5c1) · [_atr](#fun-62894b9526) · [_consecutive_sr](#fun-90d19bf962) · [_spike_and_volatility_levels](#fun-fbf2e7c9de) · [_volume_portion](#fun-16616bf5e6) · [build_volume_profile](#fun-998848a755) · [_dedupe_sr_levels](#fun-692ece3baf) · [analyze_dgt_price_action](#fun-b29e79e520) · [dgt_result_to_dict](#fun-39cf1265fc)

<a id="fun-a1eb4c5f6a"></a>

#### `_nz_volume`

- **ID / 行**：`FUN-A1EB4C5F6A` / `L63`（源码见本单元概览）
- **签名 / 返回**：`_nz_volume(series: pd.Series)` → `pd.Series`
- **职责**：As-built responsibility derived from `_nz_volume` and its owning unit.
- **依赖**：astype、series.fillna
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8c5d73d5c1"></a>

#### `_volume_usable`

- **ID / 行**：`FUN-8C5D73D5C1` / `L67`（源码见本单元概览）
- **签名 / 返回**：`_volume_usable(vol: pd.Series, *, min_ratio: float=0.05)` → `bool`
- **职责**：As-built responsibility derived from `_volume_usable` and its owning unit.
- **依赖**：float、len、sum
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-62894b9526"></a>

#### `_atr`

- **ID / 行**：`FUN-62894B9526` / `L73`（源码见本单元概览）
- **签名 / 返回**：`_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int)` → `pd.Series`
- **职责**：As-built responsibility derived from `_atr` and its owning unit.
- **依赖**：abs、close.shift、max、mean、pd.concat、tr.rolling
- **复杂度 / 风险**：分支 0；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-90d19bf962"></a>

#### `_consecutive_sr`

- **ID / 行**：`FUN-90D19BF962` / `L82`（源码见本单元概览）
- **签名 / 返回**：`_consecutive_sr(window: pd.DataFrame, vol_ma: pd.Series, *, use_volume: bool)` → `list[SrLevel]`
- **职责**：As-built responsibility derived from `_consecutive_sr` and its owning unit.
- **依赖**：SrLevel、_nz_volume、astype、bool、c.shift、float、len、levels.append、range、round、slice_h.max、slice_l.min、v.shift
- **复杂度 / 风险**：分支 5；跨度 68 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fbf2e7c9de"></a>

#### `_spike_and_volatility_levels`

- **ID / 行**：`FUN-FBF2E7C9DE` / `L152`（源码见本单元概览）
- **签名 / 返回**：`_spike_and_volatility_levels(window: pd.DataFrame, vol_ma: pd.Series)` → `tuple[list[SrLevel], int, int]`
- **职责**：As-built responsibility derived from `_spike_and_volatility_levels` and its owning unit.
- **依赖**：SrLevel、_atr、_nz_volume、astype、bool、float、len、levels.append、range、round
- **复杂度 / 风险**：分支 9；跨度 56 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-16616bf5e6"></a>

#### `_volume_portion`

- **ID / 行**：`FUN-16616BF5E6` / `L210`（源码见本单元概览）
- **签名 / 返回**：`_volume_portion(bar_low: float, bar_high: float, row_low: float, row_high: float)` → `float`
- **职责**：As-built responsibility derived from `_volume_portion` and its owning unit.
- **依赖**：max
- **复杂度 / 风险**：分支 3；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-998848a755"></a>

#### `build_volume_profile`

- **ID / 行**：`FUN-998848A755` / `L226`（源码见本单元概览）
- **签名 / 返回**：`build_volume_profile(bars: pd.DataFrame, *, num_rows: int=PROFILE_ROWS, value_area_pct: float=VALUE_AREA_PCT, sd_thresh: float=SUPPLY_DEMAND_THRESH)` → `VolumeProfileResult`
- **职责**：As-built responsibility derived from `build_volume_profile` and its owning unit.
- **依赖**：VolumeProfileResult、_nz_volume、_volume_portion、_volume_usable、bars.iterrows、float、int、max、min、np.isfinite、np.zeros、range、round、sd_zones.append、totals.argmax、totals.max、totals.sum、v.sum
- **复杂度 / 风险**：分支 20；跨度 92 行；medium
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="fun-692ece3baf"></a>

#### `_dedupe_sr_levels`

- **ID / 行**：`FUN-692ECE3BAF` / `L320`（源码见本单元概览）
- **签名 / 返回**：`_dedupe_sr_levels(levels: list[SrLevel], *, tolerance: float=0.35)` → `list[SrLevel]`
- **职责**：Keep newest level when prices cluster (Pine deletes duplicate consecutive lines).
- **依赖**：abs、enumerate、kept.append、sorted
- **复杂度 / 风险**：分支 5；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b29e79e520"></a>

#### `analyze_dgt_price_action`

- **ID / 行**：`FUN-B29E79E520` / `L342`（源码见本单元概览）
- **签名 / 返回**：`analyze_dgt_price_action(df: pd.DataFrame, timeframe: str, *, lookback: int=DEFAULT_LOOKBACK, profile_bars: pd.DataFrame | None=None)` → `DgtPriceActionResult`
- **职责**：Run full DGT metrics on a Fixed-Range lookback (default 360 chart-TF bars).
- **依赖**：DgtPriceActionResult、_consecutive_sr、_dedupe_sr_levels、_nz_volume、_spike_and_volatility_levels、_volume_usable、build_volume_profile、copy、df.tail、len、mean、sr.extend、vol.rolling
- **复杂度 / 风险**：分支 2；跨度 42 行；medium
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="fun-39cf1265fc"></a>

#### `dgt_result_to_dict`

- **ID / 行**：`FUN-39CF1265FC` / `L386`（源码见本单元概览）
- **签名 / 返回**：`dgt_result_to_dict(result: DgtPriceActionResult, *, lookback_requested: int | None=None, lookback_mode: str | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `dgt_result_to_dict` and its owning unit.
- **依赖**：lvl.time.isoformat
- **复杂度 / 风险**：分支 2；跨度 37 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-3b1598dc1b"></a>

### src/analysis/display_labels.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3B1598DC1B |
| 源码 | [src/analysis/display_labels.py](../../src/analysis/display_labels.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Shared Chinese/English labels for Lux structure display (analysis layer). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[liquidity_label](#fun-f519f9a949)

<a id="fun-f519f9a949"></a>

#### `liquidity_label`

- **ID / 行**：`FUN-F519F9A949` / `L22`（源码见本单元概览）
- **签名 / 返回**：`liquidity_label(zone: LiquidityZone)` → `str`
- **职责**：As-built responsibility derived from `liquidity_label` and its owning unit.
- **复杂度 / 风险**：分支 2；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-60e70e7439"></a>

### src/analysis/fact_registry.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-60E70E7439 |
| 源码 | [src/analysis/fact_registry.py](../../src/analysis/fact_registry.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Canonical fact registry with as-of, source and provenance contracts. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 16 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py)、[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_llm_context_fact_refs.py](../../tests/unit/test_llm_context_fact_refs.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[_as_of_utc](#fun-0574dfe158) · [_register_numeric](#fun-0a56af7ead) · [_register_text](#fun-9127544e40) · [_pa_fact_id](#fun-760701887e) · [calendar_state](#fun-7a197e3612) · [_calendar_state](#fun-b21844f1e5) · [_register_timeframes](#fun-98305ca234) · [_register_price_action](#fun-87b173149d) · [_register_technical_claim_facts](#fun-0da621fc3d) · [_register_freshness](#fun-e744014446) · [_register_external](#fun-0d88ff54f8) · [build_fact_registry](#fun-afac55bb24) · [allowed_prices](#fun-f1860a0ed6) · [fact_lookup](#fun-cbacfa1e82) · [fact_ids_for_signal](#fun-e14834ae01) · [compact_fact_index](#fun-91752c5a3c)

<a id="fun-0574dfe158"></a>

#### `_as_of_utc`

- **ID / 行**：`FUN-0574DFE158` / `L11`（源码见本单元概览）
- **签名 / 返回**：`_as_of_utc(report: dict[str, Any])` → `str | None`
- **职责**：As-built responsibility derived from `_as_of_utc` and its owning unit.
- **依赖**：as_of.get、get、report.get
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0a56af7ead"></a>

#### `_register_numeric`

- **ID / 行**：`FUN-0A56AF7EAD` / `L16`（源码见本单元概览）
- **签名 / 返回**：`_register_numeric(facts: dict[str, dict[str, Any]], *, fact_id: str, value: Any, source: str, timeframe: str | None=None, quality: str='verified', as_of: str | None=None, refs: dict[str, Any] | None=None)` → `None`
- **职责**：As-built responsibility derived from `_register_numeric` and its owning unit.
- **依赖**：float、get、round
- **复杂度 / 风险**：分支 4；跨度 34 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9127544e40"></a>

#### `_register_text`

- **ID / 行**：`FUN-9127544E40` / `L52`（源码见本单元概览）
- **签名 / 返回**：`_register_text(facts: dict[str, dict[str, Any]], *, fact_id: str, value: Any, source: str, timeframe: str | None=None, quality: str='verified', as_of: str | None=None, refs: dict[str, Any] | None=None)` → `None`
- **职责**：As-built responsibility derived from `_register_text` and its owning unit.
- **依赖**：get、str、strip
- **复杂度 / 风险**：分支 3；跨度 31 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-760701887e"></a>

#### `_pa_fact_id`

- **ID / 行**：`FUN-760701887E` / `L85`（源码见本单元概览）
- **签名 / 返回**：`_pa_fact_id(tf: str, suffix: str)` → `str`
- **职责**：As-built responsibility derived from `_pa_fact_id` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7a197e3612"></a>

#### `calendar_state`

- **ID / 行**：`FUN-7A197E3612` / `L91`（源码见本单元概览）
- **签名 / 返回**：`calendar_state(report: dict[str, Any])` → `str`
- **职责**：Public alias for report calendar emptiness / fetch status (Issue #38).
- **依赖**：_calendar_state
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py) · direct-dynamic

<a id="fun-b21844f1e5"></a>

#### `_calendar_state`

- **ID / 行**：`FUN-B21844F1E5` / `L96`（源码见本单元概览）
- **签名 / 返回**：`_calendar_state(report: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_calendar_state` and its owning unit.
- **依赖**：any、external.get、lower、report.get、str、strip
- **复杂度 / 风险**：分支 5；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-98305ca234"></a>

#### `_register_timeframes`

- **ID / 行**：`FUN-98305CA234` / `L116`（源码见本单元概览）
- **签名 / 返回**：`_register_timeframes(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None, source: str)` → `None`
- **职责**：As-built responsibility derived from `_register_timeframes` and its owning unit.
- **依赖**：_register_numeric、_register_text、abs、enumerate、float、fvg.get、info.get、isinstance、items、ob.get、report.get、round
- **复杂度 / 风险**：分支 15；跨度 66 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-87b173149d"></a>

#### `_register_price_action`

- **ID / 行**：`FUN-87B173149D` / `L184`（源码见本单元概览）
- **签名 / 返回**：`_register_price_action(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None)` → `None`
- **职责**：As-built responsibility derived from `_register_price_action` and its owning unit.
- **依赖**：_pa_fact_id、_register_numeric、enumerate、get、items、lvl.get、report.get、str、vp.get
- **复杂度 / 风险**：分支 3；跨度 29 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0da621fc3d"></a>

#### `_register_technical_claim_facts`

- **ID / 行**：`FUN-0DA621FC3D` / `L215`（源码见本单元概览）
- **签名 / 返回**：`_register_technical_claim_facts(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None)` → `None`
- **职责**：Register the persisted claim-v2 catalog, including compact-panel omissions.
- **依赖**：_register_numeric、entity.get、fid.endswith、isinstance、report.get、str、strip
- **复杂度 / 风险**：分支 9；跨度 43 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e744014446"></a>

#### `_register_freshness`

- **ID / 行**：`FUN-E744014446` / `L260`（源码见本单元概览）
- **签名 / 返回**：`_register_freshness(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None, source: str)` → `None`
- **职责**：As-built responsibility derived from `_register_freshness` and its owning unit.
- **依赖**：_register_numeric、_register_text、bars.items、bool、data_as_of.get、get、lower、report.get、stats.get、str
- **复杂度 / 风险**：分支 4；跨度 42 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0d88ff54f8"></a>

#### `_register_external`

- **ID / 行**：`FUN-0D88FF54F8` / `L304`（源码见本单元概览）
- **签名 / 返回**：`_register_external(facts: dict[str, dict[str, Any]], report: dict[str, Any], *, as_of: str | None)` → `None`
- **职责**：As-built responsibility derived from `_register_external` and its owning unit.
- **依赖**：_calendar_state、_register_numeric、_register_text、cross.get、enumerate、external.get、headline.get、isinstance、quote.get、report.get、row.get、str
- **复杂度 / 风险**：分支 12；跨度 83 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-afac55bb24"></a>

#### `build_fact_registry`

- **ID / 行**：`FUN-AFAC55BB24` / `L389`（源码见本单元概览）
- **签名 / 返回**：`build_fact_registry(report: dict[str, Any])` → `dict[str, Any]`
- **职责**：Register numeric and text facts referenced by narrative validation and UI.
- **依赖**：_as_of_utc、_register_external、_register_freshness、_register_numeric、_register_price_action、_register_technical_claim_facts、_register_timeframes、append、enumerate、facts.items、float、get、len、metrics.get、price_index.setdefault、report.get、row.get、sentiment.get、sig.get、str
- **复杂度 / 风险**：分支 9；跨度 85 行；medium
- **测试 / 验证**：[tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py)、[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_llm_context_fact_refs.py](../../tests/unit/test_llm_context_fact_refs.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) · direct-dynamic

<a id="fun-f1860a0ed6"></a>

#### `allowed_prices`

- **ID / 行**：`FUN-F1860A0ED6` / `L476`（源码见本单元概览）
- **签名 / 返回**：`allowed_prices(registry: dict[str, Any])` → `set[float]`
- **职责**：As-built responsibility derived from `allowed_prices` and its owning unit.
- **依赖**：float、registry.get、row.get、values
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py) · direct-dynamic

<a id="fun-cbacfa1e82"></a>

#### `fact_lookup`

- **ID / 行**：`FUN-CBACFA1E82` / `L484`（源码见本单元概览）
- **签名 / 返回**：`fact_lookup(registry: dict[str, Any], price: float, *, tolerance: float=0.51)` → `list[str]`
- **职责**：Resolve a displayed price to registered fact IDs.
- **依赖**：abs、float、matches.append、registry.get、row.get、str、values
- **复杂度 / 风险**：分支 3；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py) · direct-dynamic

<a id="fun-e14834ae01"></a>

#### `fact_ids_for_signal`

- **ID / 行**：`FUN-E14834AE01` / `L495`（源码见本单元概览）
- **签名 / 返回**：`fact_ids_for_signal(sig: dict[str, Any], registry: dict[str, Any])` → `dict[str, Any]`
- **职责**：Map signal geometry fields to canonical fact_ids when registered.
- **依赖**：len、mapping.items、range、registry.get、sig.get、str、tp_ids.append
- **复杂度 / 风险**：分支 5；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py) · direct-dynamic

<a id="fun-91752c5a3c"></a>

#### `compact_fact_index`

- **ID / 行**：`FUN-91752C5A3C` / `L518`（源码见本单元概览）
- **签名 / 返回**：`compact_fact_index(registry: dict[str, Any], *, limit: int=120)` → `list[dict[str, Any]]`
- **职责**：Slim fact list for LLM payloads — cite fact_id instead of duplicating numbers.
- **依赖**：list、out.append、r.get、registry.get、row.get、rows.sort、str、values
- **复杂度 / 风险**：分支 2；跨度 19 行；medium
- **测试 / 验证**：[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py) · direct-dynamic

<a id="unit-c37864f306"></a>

### src/analysis/field_glossary.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C37864F306 |
| 源码 | [src/analysis/field_glossary.py](../../src/analysis/field_glossary.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Shared PA/SMC glossary and compact LLM field hints. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3962aaac44"></a>

### src/analysis/ict_pa.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3962AAAC44 |
| 源码 | [src/analysis/ict_pa.py](../../src/analysis/ict_pa.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | ICT / Price Action shared types — LuxAlgo SMC detection via luxalgo_smc. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_coherence.py](../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_luxalgo_smc.py](../../tests/unit/test_luxalgo_smc.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_plan_signals.py](../../tests/unit/test_plan_signals.py)、[tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_tf_snapshot.py](../../tests/unit/test_tf_snapshot.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[_premium_discount](#fun-9d252e677d) · [_volume_signal](#fun-655f9ec66c) · [_last_numeric](#fun-51492ca837) · [_swing_liquidity](#fun-b620f510c7) · [_latest_structure_labels](#fun-dd99d46e1a) · [analyze_timeframe](#fun-caebe97b43) · [sentiment_score](#fun-2279759b7f)

<a id="fun-9d252e677d"></a>

#### `_premium_discount`

- **ID / 行**：`FUN-9D252E677D` / `L80`（源码见本单元概览）
- **签名 / 返回**：`_premium_discount(swing_high: float | None, swing_low: float | None, price: float)` → `tuple[str, float | None]`
- **职责**：As-built responsibility derived from `_premium_discount` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-655f9ec66c"></a>

#### `_volume_signal`

- **ID / 行**：`FUN-655F9EC66C` / `L93`（源码见本单元概览）
- **签名 / 返回**：`_volume_signal(df: pd.DataFrame)` → `str`
- **职责**：As-built responsibility derived from `_volume_signal` and its owning unit.
- **依赖**：astype、float、len、mean
- **复杂度 / 风险**：分支 4；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-51492ca837"></a>

#### `_last_numeric`

- **ID / 行**：`FUN-51492CA837` / `L109`（源码见本单元概览）
- **签名 / 返回**：`_last_numeric(df: pd.DataFrame, column: str)` → `float | None`
- **职责**：As-built responsibility derived from `_last_numeric` and its owning unit.
- **依赖**：float、pd.isna
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b620f510c7"></a>

#### `_swing_liquidity`

- **ID / 行**：`FUN-B620F510C7` / `L118`（源码见本单元概览）
- **签名 / 返回**：`_swing_liquidity(swing_high: float | None, swing_low: float | None)` → `list[LiquidityZone]`
- **职责**：Key liquidity from Lux swing pivots (replaces EQH/EQL for LLM/UI).
- **依赖**：LiquidityZone、float、zones.append
- **复杂度 / 风险**：分支 2；跨度 25 行；low
- **测试 / 验证**：[tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py) · direct-dynamic

<a id="fun-dd99d46e1a"></a>

#### `_latest_structure_labels`

- **ID / 行**：`FUN-DD99D46E1A` / `L145`（源码见本单元概览）
- **签名 / 返回**：`_latest_structure_labels(events: list[StructureEvent], *, scope: Literal['internal', 'swing'] | None=None)` → `tuple[str, str]`
- **职责**：As-built responsibility derived from `_latest_structure_labels` and its owning unit.
- **依赖**：reversed
- **复杂度 / 风险**：分支 3；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-caebe97b43"></a>

#### `analyze_timeframe`

- **ID / 行**：`FUN-CAEBE97B43` / `L161`（源码见本单元概览）
- **签名 / 返回**：`analyze_timeframe(df: pd.DataFrame, timeframe: str)` → `TimeframeAnalysis`
- **职责**：Analyze one timeframe using LuxAlgo SMC detection rules.
- **依赖**：TimeframeAnalysis、_last_numeric、_latest_structure_labels、_premium_discount、_swing_liquidity、_volume_signal、analyze_luxalgo、float、len、max、min
- **复杂度 / 风险**：分支 4；跨度 43 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_luxalgo_smc.py](../../tests/unit/test_luxalgo_smc.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="fun-2279759b7f"></a>

#### `sentiment_score`

- **ID / 行**：`FUN-2279759B7F` / `L206`（源码见本单元概览）
- **签名 / 返回**：`sentiment_score(analyses: dict[str, TimeframeAnalysis])` → `dict[str, float]`
- **职责**：Weighted bear/bull/range probabilities.
- **依赖**：round、weights.items
- **复杂度 / 风险**：分支 4；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-a9ae5e6696"></a>

### src/analysis/level_validator.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A9AE5E6696 |
| 源码 | [src/analysis/level_validator.py](../../src/analysis/level_validator.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Validate LLM proposed levels before they enter trading plans. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py) |
| 验证状态 | selected |

#### 函数导航

[_location_error](#fun-3964465d91) · [_llm_signal_name](#fun-4bc8ff4d21) · [_tp_ladder_error](#fun-153aabf750) · [_geometry_error](#fun-fcbb9c053e) · [_position_size](#fun-a872921e36) · [validate_llm_levels](#fun-89da4d6e6e) · [_grade_force](#fun-fe20142b1a)

<a id="fun-3964465d91"></a>

#### `_location_error`

- **ID / 行**：`FUN-3964465D91` / `L22`（源码见本单元概览）
- **签名 / 返回**：`_location_error(ctx: MarketContext, proposal: LevelProposal)` → `str | None`
- **职责**：As-built responsibility derived from `_location_error` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 2；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4bc8ff4d21"></a>

#### `_llm_signal_name`

- **ID / 行**：`FUN-4BC8FF4D21` / `L37`（源码见本单元概览）
- **签名 / 返回**：`_llm_signal_name(proposal: LevelProposal)` → `str`
- **职责**：As-built responsibility derived from `_llm_signal_name` and its owning unit.
- **依赖**：str、upper
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-153aabf750"></a>

#### `_tp_ladder_error`

- **ID / 行**：`FUN-153AABF750` / `L45`（源码见本单元概览）
- **签名 / 返回**：`_tp_ladder_error(proposal: LevelProposal)` → `str | None`
- **职责**：As-built responsibility derived from `_tp_ladder_error` and its owning unit.
- **依赖**：any、len、zip
- **复杂度 / 风险**：分支 8；跨度 18 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fcbb9c053e"></a>

#### `_geometry_error`

- **ID / 行**：`FUN-FCBB9C053E` / `L65`（源码见本单元概览）
- **签名 / 返回**：`_geometry_error(proposal: LevelProposal)` → `str | None`
- **职责**：As-built responsibility derived from `_geometry_error` and its owning unit.
- **依赖**：_tp_ladder_error
- **复杂度 / 风险**：分支 8；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a872921e36"></a>

#### `_position_size`

- **ID / 行**：`FUN-A872921E36` / `L86`（源码见本单元概览）
- **签名 / 返回**：`_position_size(confidence: float, grade: str, *, eligibility: str)` → `str`
- **职责**：As-built responsibility derived from `_position_size` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-89da4d6e6e"></a>

#### `validate_llm_levels`

- **ID / 行**：`FUN-89DA4D6E6E` / `L96`（源码见本单元概览）
- **签名 / 返回**：`validate_llm_levels(ctx: MarketContext, proposals: list[LevelProposal], *, level_reactions: list[dict[str, Any]] | None=None)` → `tuple[list[TradingSignal], list[dict[str, Any]]]`
- **职责**：Convert valid LLM level proposals into existing TradingSignal objects.
- **依赖**：TradingSignal、_compute_risk_reward、_geometry_error、_grade_force、_llm_signal_name、_location_error、_position_size、_setup_status_and_score、_stop_breached、accepted.append、adjudicate_level_proposal_claim、asdict、audit.append、claim.to_dict、dict、dict.fromkeys、enumerate、join、len、list
- **复杂度 / 风险**：分支 21；跨度 197 行；high
- **测试 / 验证**：[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py) · direct-dynamic

<a id="fun-fe20142b1a"></a>

#### `_grade_force`

- **ID / 行**：`FUN-FE20142B1A` / `L295`（源码见本单元概览）
- **签名 / 返回**：`_grade_force(score: float)` → `str`
- **职责**：As-built responsibility derived from `_grade_force` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-2f7fedba6f"></a>

### src/analysis/luxalgo_smc.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F7FEDBA6F |
| 源码 | [src/analysis/luxalgo_smc.py](../../src/analysis/luxalgo_smc.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | LuxAlgo Smart Money Concepts — Python port of detection rules. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 15 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_luxalgo_smc.py](../../tests/unit/test_luxalgo_smc.py) |
| 验证状态 | selected |

#### 函数导航

[_true_range](#fun-80471dd12f) · [_atr_series](#fun-f820754950) · [_leg_at_bar](#fun-fc6a52d232) · [_parsed_bar](#fun-0a1736195c) · [_fvg_threshold](#fun-8b8bd0c1c0) · [_store_order_block](#fun-2052af2dde) · [_mitigate_obs](#fun-31c7de2cd6) · [_mitigate_fvgs](#fun-a130bd9445) · [_crossover](#fun-603728af0a) · [_crossunder](#fun-0fd674f4f8) · [_internal_confluence_bars](#fun-d33565e210) · [_append_structure_event](#fun-d317d1876f) · [_update_structure_pivots](#fun-5978222f4d) · [_push_ob](#fun-64ef8badda) · [analyze_luxalgo](#fun-08ff07c7e5)

<a id="fun-80471dd12f"></a>

#### `_true_range`

- **ID / 行**：`FUN-80471DD12F` / `L71`（源码见本单元概览）
- **签名 / 返回**：`_true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray)` → `np.ndarray`
- **职责**：As-built responsibility derived from `_true_range` and its owning unit.
- **依赖**：abs、len、max、np.empty、range
- **复杂度 / 风险**：分支 1；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f820754950"></a>

#### `_atr_series`

- **ID / 行**：`FUN-F820754950` / `L80`（源码见本单元概览）
- **签名 / 返回**：`_atr_series(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int)` → `np.ndarray`
- **职责**：As-built responsibility derived from `_atr_series` and its owning unit.
- **依赖**：_true_range、float、len、np.full、np.mean、range
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fc6a52d232"></a>

#### `_leg_at_bar`

- **ID / 行**：`FUN-FC6A52D232` / `L90`（源码见本单元概览）
- **签名 / 返回**：`_leg_at_bar(highs: np.ndarray, lows: np.ndarray, i: int, size: int, prev_leg: int)` → `int`
- **职责**：As-built responsibility derived from `_leg_at_bar` and its owning unit.
- **依赖**：float、np.max、np.min
- **复杂度 / 风险**：分支 3；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0a1736195c"></a>

#### `_parsed_bar`

- **ID / 行**：`FUN-0A1736195C` / `L103`（源码见本单元概览）
- **签名 / 返回**：`_parsed_bar(high: float, low: float, vol: float)` → `tuple[float, float]`
- **职责**：As-built responsibility derived from `_parsed_bar` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8b8bd0c1c0"></a>

#### `_fvg_threshold`

- **ID / 行**：`FUN-8B8BD0C1C0` / `L109`（源码见本单元概览）
- **签名 / 返回**：`_fvg_threshold(cum_abs_delta: float, bar_index: int)` → `float`
- **职责**：As-built responsibility derived from `_fvg_threshold` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2052af2dde"></a>

#### `_store_order_block`

- **ID / 行**：`FUN-2052AF2DDE` / `L115`（源码见本单元概览）
- **签名 / 返回**：`_store_order_block(parsed_highs: list[float], parsed_lows: list[float], times: list[pd.Timestamp], pivot_index: int, current_index: int, bias: Literal['bullish', 'bearish'])` → `OrderBlock | None`
- **职责**：As-built responsibility derived from `_store_order_block` and its owning unit.
- **依赖**：OrderBlock、float、int、np.argmax、np.argmin
- **复杂度 / 风险**：分支 4；跨度 28 行；high
- **测试 / 验证**：[tests/unit/test_luxalgo_smc.py](../../tests/unit/test_luxalgo_smc.py) · direct-dynamic

<a id="fun-31c7de2cd6"></a>

#### `_mitigate_obs`

- **ID / 行**：`FUN-31C7DE2CD6` / `L145`（源码见本单元概览）
- **签名 / 返回**：`_mitigate_obs(obs: list[OrderBlock], high: float, low: float)` → `list[OrderBlock]`
- **职责**：As-built responsibility derived from `_mitigate_obs` and its owning unit.
- **依赖**：kept.append
- **复杂度 / 风险**：分支 3；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a130bd9445"></a>

#### `_mitigate_fvgs`

- **ID / 行**：`FUN-A130BD9445` / `L160`（源码见本单元概览）
- **签名 / 返回**：`_mitigate_fvgs(fvgs: list[FairValueGap], high: float, low: float)` → `list[FairValueGap]`
- **职责**：As-built responsibility derived from `_mitigate_fvgs` and its owning unit.
- **依赖**：kept.append
- **复杂度 / 风险**：分支 3；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-603728af0a"></a>

#### `_crossover`

- **ID / 行**：`FUN-603728AF0A` / `L175`（源码见本单元概览）
- **签名 / 返回**：`_crossover(close_prev: float, close_curr: float, level: float)` → `bool`
- **职责**：As-built responsibility derived from `_crossover` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0fd674f4f8"></a>

#### `_crossunder`

- **ID / 行**：`FUN-0FD674F4F8` / `L179`（源码见本单元概览）
- **签名 / 返回**：`_crossunder(close_prev: float, close_curr: float, level: float)` → `bool`
- **职责**：As-built responsibility derived from `_crossunder` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d33565e210"></a>

#### `_internal_confluence_bars`

- **ID / 行**：`FUN-D33565E210` / `L183`（源码见本单元概览）
- **签名 / 返回**：`_internal_confluence_bars(open_: float, high: float, low: float, close: float)` → `tuple[bool, bool]`
- **职责**：Lux internalFilterConfluence: wick dominance on the signal bar.
- **依赖**：max、min
- **复杂度 / 风险**：分支 0；跨度 11 行；low
- **测试 / 验证**：[tests/unit/test_luxalgo_smc.py](../../tests/unit/test_luxalgo_smc.py) · direct-dynamic

<a id="fun-d317d1876f"></a>

#### `_append_structure_event`

- **ID / 行**：`FUN-D317D1876F` / `L196`（源码见本单元概览）
- **签名 / 返回**：`_append_structure_event(events: list[StructureEvent], *, tag: Literal['BOS', 'CHoCH'], direction: Literal['bullish', 'bearish'], level: float, bar_time: pd.Timestamp, pivot_time: pd.Timestamp | None, scope: Literal['internal', 'swing'])` → `None`
- **职责**：As-built responsibility derived from `_append_structure_event` and its owning unit.
- **依赖**：StructureEvent、events.append
- **复杂度 / 风险**：分支 0；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5978222f4d"></a>

#### `_update_structure_pivots`

- **ID / 行**：`FUN-5978222F4D` / `L218`（源码见本单元概览）
- **签名 / 返回**：`_update_structure_pivots(*, size: int, leg_prev: int, leg_curr: int, highs: np.ndarray, lows: np.ndarray, index: pd.DatetimeIndex, i: int, pivot_high: _Pivot, pivot_low: _Pivot, trailing: _Trailing | None, swings: list[SwingPoint], equal_mode: bool, atr_measure: float, equal_prev_low: _Pivot, equal_prev_high: _Pivot, liquidity: list[LiquidityZone])` → `None`
- **职责**：As-built responsibility derived from `_update_structure_pivots` and its owning unit.
- **依赖**：SwingPoint、abs、float、swings.append
- **复杂度 / 风险**：分支 11；跨度 67 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-64ef8badda"></a>

#### `_push_ob`

- **ID / 行**：`FUN-64EF8BADDA` / `L287`（源码见本单元概览）
- **签名 / 返回**：`_push_ob(blocks: list[OrderBlock], ob: OrderBlock | None)` → `None`
- **职责**：As-built responsibility derived from `_push_ob` and its owning unit.
- **依赖**：blocks.insert、blocks.pop、len
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-08ff07c7e5"></a>

#### `analyze_luxalgo`

- **ID / 行**：`FUN-08FF07C7E5` / `L295`（源码见本单元概览）
- **签名 / 返回**：`analyze_luxalgo(df: pd.DataFrame)` → `LuxAlgoResult`
- **职责**：Run LuxAlgo SMC detection over OHLC bars.
- **依赖**：FairValueGap、LuxAlgoResult、_Pivot、_Trailing、_append_structure_event、_atr_series、_crossover、_crossunder、_fvg_threshold、_internal_confluence_bars、_leg_at_bar、_mitigate_fvgs、_mitigate_obs、_parsed_bar、_push_ob、_store_order_block、_update_structure_pivots、abs、astype、float
- **复杂度 / 风险**：分支 29；跨度 294 行；high
- **测试 / 验证**：[tests/unit/test_luxalgo_smc.py](../../tests/unit/test_luxalgo_smc.py) · direct-dynamic

<a id="unit-4f106aec16"></a>

### src/analysis/narrative_combine.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4F106AEC16 |
| 源码 | [src/analysis/narrative_combine.py](../../src/analysis/narrative_combine.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | SMC + DGT Price Action narrative combination helpers. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 15 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_narrative_combine.py](../../tests/unit/test_narrative_combine.py) |
| 验证状态 | selected |

#### 函数导航

[_fmt](#fun-891202ded4) · [pa_block](#fun-39e6ed0f5b) · [value_zone_position](#fun-411453936c) · [nearest_pa_sr](#fun-98c0107c91) · [zone_midpoint](#fun-9f20c3627c) · [resonance_note](#fun-e61095f39d) · [entry_resonance_text](#fun-9e35377646) · [pa_trend_label](#fun-6d4b2fe2bb) · [liquidity_pa_side_text](#fun-761ec7d9af) · [tf_pa_structure_levels](#fun-59652b92db) · [tf_pa_condition](#fun-0917f96ed2) · [tf_pa_invalidation](#fun-8f862d6445) · [liquidity_side_text](#fun-36832f1f03) · [tf_pa_context_line](#fun-75dd4e0160) · [build_pa_llm_summary](#fun-8a883dd45a)

<a id="fun-891202ded4"></a>

#### `_fmt`

- **ID / 行**：`FUN-891202DED4` / `L29`（源码见本单元概览）
- **签名 / 返回**：`_fmt(value: Any)` → `str`
- **职责**：As-built responsibility derived from `_fmt` and its owning unit.
- **依赖**：float、number.is_integer、rstrip
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-39e6ed0f5b"></a>

#### `pa_block`

- **ID / 行**：`FUN-39E6ED0F5B` / `L37`（源码见本单元概览）
- **签名 / 返回**：`pa_block(report: dict[str, Any], tf: str)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `pa_block` and its owning unit.
- **依赖**：get、report.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-411453936c"></a>

#### `value_zone_position`

- **ID / 行**：`FUN-411453936C` / `L41`（源码见本单元概览）
- **签名 / 返回**：`value_zone_position(price: float | None, vp: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `value_zone_position` and its owning unit.
- **依赖**：float、vp.get
- **复杂度 / 风险**：分支 4；跨度 11 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-98c0107c91"></a>

#### `nearest_pa_sr`

- **ID / 行**：`FUN-98C0107C91` / `L54`（源码见本单元概览）
- **签名 / 返回**：`nearest_pa_sr(sr_levels: list[dict[str, Any]], price: float | None, direction: str, *, limit: int=3)` → `list[str]`
- **职责**：As-built responsibility derived from `nearest_pa_sr` and its owning unit.
- **依赖**：_fmt、float、len、lvl.get、out.append、parsed.sort、round、seen.add、set、str
- **复杂度 / 风险**：分支 5；跨度 32 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9f20c3627c"></a>

#### `zone_midpoint`

- **ID / 行**：`FUN-9F20C3627C` / `L88`（源码见本单元概览）
- **签名 / 返回**：`zone_midpoint(zone: str | None)` → `float | None`
- **职责**：As-built responsibility derived from `zone_midpoint` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：float、split、zone.replace
- **复杂度 / 风险**：分支 2；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e61095f39d"></a>

#### `resonance_note`

- **ID / 行**：`FUN-E61095F39D` / `L98`（源码见本单元概览）
- **签名 / 返回**：`resonance_note(smc_zone: str | None, pa_prices: list[float], *, tolerance: float=RESONANCE_TOLERANCE)` → `str`
- **职责**：As-built responsibility derived from `resonance_note` and its owning unit.
- **依赖**：abs、zone_midpoint
- **复杂度 / 风险**：分支 3；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9e35377646"></a>

#### `entry_resonance_text`

- **ID / 行**：`FUN-9E35377646` / `L113`（源码见本单元概览）
- **签名 / 返回**：`entry_resonance_text(signal: dict[str, Any], pa_block_5m: dict[str, Any], *, tolerance: float=RESONANCE_TOLERANCE)` → `str`
- **职责**：As-built responsibility derived from `entry_resonance_text` and its owning unit.
- **依赖**：abs、dict.fromkeys、float、join、notes.append、pa_block_5m.get、signal.get、vp.get、x.get
- **复杂度 / 风险**：分支 6；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_combine.py](../../tests/unit/test_narrative_combine.py) · direct-dynamic

<a id="fun-6d4b2fe2bb"></a>

#### `pa_trend_label`

- **ID / 行**：`FUN-6D4B2FE2BB` / `L139`（源码见本单元概览）
- **签名 / 返回**：`pa_trend_label(price: float | None, vp: dict[str, Any])` → `str`
- **职责**：Infer trend wording from price vs PA value area only.
- **依赖**：value_zone_position
- **复杂度 / 风险**：分支 3；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-761ec7d9af"></a>

#### `liquidity_pa_side_text`

- **ID / 行**：`FUN-761EC7D9AF` / `L151`（源码见本单元概览）
- **签名 / 返回**：`liquidity_pa_side_text(side_label: str, pa_labels: list[str])` → `str | None`
- **职责**：As-built responsibility derived from `liquidity_pa_side_text` and its owning unit.
- **依赖**：join
- **复杂度 / 风险**：分支 1；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-59652b92db"></a>

#### `tf_pa_structure_levels`

- **ID / 行**：`FUN-59652B92DB` / `L157`（源码见本单元概览）
- **签名 / 返回**：`tf_pa_structure_levels(pa_tf: dict[str, Any], price: float | None, *, tf: str)` → `list[str]`
- **职责**：Up to two PA level lines for 4h/1h/15m panels.
- **依赖**：_fmt、join、len、levels.append、nearest_pa_sr、pa_tf.get、vp.get
- **复杂度 / 风险**：分支 4；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0917f96ed2"></a>

#### `tf_pa_condition`

- **ID / 行**：`FUN-0917F96ED2` / `L182`（源码见本单元概览）
- **签名 / 返回**：`tf_pa_condition(tf: str, *, trend: str, vp: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `tf_pa_condition` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8f862d6445"></a>

#### `tf_pa_invalidation`

- **ID / 行**：`FUN-8F862D6445` / `L192`（源码见本单元概览）
- **签名 / 返回**：`tf_pa_invalidation(trend: str, vp: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `tf_pa_invalidation` and its owning unit.
- **依赖**：_fmt、vp.get
- **复杂度 / 风险**：分支 3；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-36832f1f03"></a>

#### `liquidity_side_text`

- **ID / 行**：`FUN-36832F1F03` / `L203`（源码见本单元概览）
- **签名 / 返回**：`liquidity_side_text(side_label: str, smc_rows: list[dict[str, Any]], pa_labels: list[str])` → `str | None`
- **职责**：As-built responsibility derived from `liquidity_side_text` and its owning unit.
- **依赖**：_fmt、join、parts.append
- **复杂度 / 风险**：分支 3；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-75dd4e0160"></a>

#### `tf_pa_context_line`

- **ID / 行**：`FUN-75DD4E0160` / `L218`（源码见本单元概览）
- **签名 / 返回**：`tf_pa_context_line(tf: str, vp: dict[str, Any], price: float | None)` → `str`
- **职责**：As-built responsibility derived from `tf_pa_context_line` and its owning unit.
- **依赖**：_fmt、value_zone_position、vp.get
- **复杂度 / 风险**：分支 3；跨度 11 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8a883dd45a"></a>

#### `build_pa_llm_summary`

- **ID / 行**：`FUN-8A883DD45A` / `L231`（源码见本单元概览）
- **签名 / 返回**：`build_pa_llm_summary(price_action: dict[str, Any], *, price: float | None)` → `dict[str, Any]`
- **职责**：Compact per-TF PA facts for LLM (technical / narrative / levels).
- **依赖**：block.get、isinstance、len、nearest_pa_sr、price_action.items、value_zone_position、vp.get
- **复杂度 / 风险**：分支 6；跨度 41 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_combine.py](../../tests/unit/test_narrative_combine.py) · direct-dynamic

<a id="unit-b5b5d80eb7"></a>

### src/analysis/narrative_facts.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B5B5D80EB7 |
| 源码 | [src/analysis/narrative_facts.py](../../src/analysis/narrative_facts.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Single builder for narrative LLM facts — shared by context and offline validation. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py) |
| 验证状态 | selected |

#### 函数导航

[build_narrative_facts_for_llm](#fun-5441c0b28d)

<a id="fun-5441c0b28d"></a>

#### `build_narrative_facts_for_llm`

- **ID / 行**：`FUN-5441C0B28D` / `L15`（源码见本单元概览）
- **签名 / 返回**：`build_narrative_facts_for_llm(report: dict[str, Any], *, ctx: MarketContext | None=None, technical_context: dict[str, Any] | None=None, event_limit: int | None=None, compact_for_llm: bool=True)` → `dict[str, Any]`
- **职责**：Build narrative_facts once from report + optional market context.
- **依赖**：build_narrative_facts、build_technical_context
- **复杂度 / 风险**：分支 3；跨度 16 行；medium
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py) · direct-dynamic

<a id="unit-0d14c54b60"></a>

### src/analysis/narrative_sections.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0D14C54B60 |
| 源码 | [src/analysis/narrative_sections.py](../../src/analysis/narrative_sections.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Institutional narrative sections shared by rule and LLM report paths. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 28 / 4 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_combine.py](../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_narrative_top_level.py](../../tests/unit/test_narrative_top_level.py)、[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py) |
| 验证状态 | selected |

#### 函数导航

[_fmt](#fun-cafae2be89) · [_section](#fun-77b59ff6c0) · [_intraday_pa_block](#fun-28571ac483) · [_overview_volume_context](#fun-9b4186d596) · [_liquidity_pa_context](#fun-76ad3fd71d) · [build_rule_narrative_sections](#fun-d63e7f97de) · [section_to_bullets](#fun-7fbc737860) · [overview_bullets_from_sections](#fun-becbd2f758) · [build_narrative_facts](#fun-6ee7e2523c) · [build_narrative_facts.add_context](#fun-0717bfae8a) · [build_narrative_facts.add_execution](#fun-287fb686ea) · [validate_and_merge_llm_sections](#fun-f0ff3fb2e4) · [_confidence](#fun-58e4660f21) · [_coerce_string_list](#fun-e6ef29ff95) · [_capped_section_lists](#fun-ca4fa260dd) · [_section_visible_lines](#fun-3a8882518c) · [_normalize_llm_section](#fun-75bc1eba00) · [_validate_section](#fun-5c22fbf976) · [_expected_bias](#fun-21729c6d78) · [narrative_price_tolerance](#fun-74a552c2a1) · [_price_tolerance](#fun-ea3075165b) · [_unapproved_prices](#fun-ee96ece754) · [_unapproved_calendar_claims](#fun-6cde98503a) · [_executable_wording_on_wait](#fun-870e7671a1) · [_direction_conflict](#fun-b4dcb46a68) · [_execution_authorized](#fun-25aeefe31c) · [validate_llm_top_level_fields](#fun-d7185cbde0) · [validate_llm_top_level](#fun-5260c4fffe)

<a id="fun-cafae2be89"></a>

#### `_fmt`

- **ID / 行**：`FUN-CAFAE2BE89` / `L36`（源码见本单元概览）
- **签名 / 返回**：`_fmt(value: Any)` → `str`
- **职责**：As-built responsibility derived from `_fmt` and its owning unit.
- **依赖**：float、number.is_integer、rstrip
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-77b59ff6c0"></a>

#### `_section`

- **ID / 行**：`FUN-77B59FF6C0` / `L44`（源码见本单元概览）
- **签名 / 返回**：`_section(summary: str, *, context: list[str] | None=None, levels: list[str] | None=None, conditions: list[str] | None=None, invalidation: str='')` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_section` and its owning unit.
- **依赖**：invalidation.strip、summary.strip
- **复杂度 / 风险**：分支 0；跨度 19 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-28571ac483"></a>

#### `_intraday_pa_block`

- **ID / 行**：`FUN-28571AC483` / `L65`（源码见本单元概览）
- **签名 / 返回**：`_intraday_pa_block(report: dict[str, Any])` → `dict[str, Any]`
- **职责**：Session-day PA block when available.
- **依赖**：get、report.get
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9b4186d596"></a>

#### `_overview_volume_context`

- **ID / 行**：`FUN-9B4186D596` / `L70`（源码见本单元概览）
- **签名 / 返回**：`_overview_volume_context(report: dict[str, Any])` → `tuple[dict[str, Any], str]`
- **职责**：Prefer session-day POC/VA; fall back to 15m then 5m.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_intraday_pa_block、block.get、get、pa_block、session.get
- **复杂度 / 风险**：分支 3；跨度 10 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-76ad3fd71d"></a>

#### `_liquidity_pa_context`

- **ID / 行**：`FUN-76AD3FD71D` / `L82`（源码见本单元概览）
- **签名 / 返回**：`_liquidity_pa_context(report: dict[str, Any])` → `tuple[dict[str, Any], str]`
- **职责**：Intraday liquidity narrative uses session S/R; 5m reserved for entry plans only.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_intraday_pa_block、block.get、get、pa_block、session.get
- **复杂度 / 风险**：分支 3；跨度 10 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-d63e7f97de"></a>

#### `build_rule_narrative_sections`

- **ID / 行**：`FUN-D63E7F97DE` / `L94`（源码见本单元概览）
- **签名 / 返回**：`build_rule_narrative_sections(report: dict[str, Any])` → `dict[str, dict[str, Any]]`
- **职责**：Build deterministic, screenshot-density copy from report facts.
- **依赖**：_fmt、_liquidity_pa_context、_overview_volume_context、_section、conclusion.get、entry_resonance_text、extras.append、get、int、join、len、liq_levels.append、liquidity_pa_side_text、max、metrics.get、nearest_pa_sr、next、overview_levels.append、pa_block、pa_liq.get
- **复杂度 / 风险**：分支 17；跨度 109 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_combine.py](../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py) · direct-dynamic

<a id="fun-7fbc737860"></a>

#### `section_to_bullets`

- **ID / 行**：`FUN-7FBC737860` / `L205`（源码见本单元概览）
- **签名 / 返回**：`section_to_bullets(section: dict[str, Any])` → `list[str]`
- **职责**：Flatten one narrative section into legacy bullet lines.
- **依赖**：row.strip、rows.append、rows.extend、section.get、str
- **复杂度 / 风险**：分支 2；跨度 11 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-becbd2f758"></a>

#### `overview_bullets_from_sections`

- **ID / 行**：`FUN-BECBD2F758` / `L218`（源码见本单元概览）
- **签名 / 返回**：`overview_bullets_from_sections(sections: dict[str, dict[str, Any]])` → `list[str]`
- **职责**：Legacy `market_overview` list derived from canonical narrative_sections.
- **依赖**：section_to_bullets、sections.get
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-6ee7e2523c"></a>

#### `build_narrative_facts`

- **ID / 行**：`FUN-6EE7E2523C` / `L223`（源码见本单元概览）
- **签名 / 返回**：`build_narrative_facts(report: dict[str, Any], technical_context: dict[str, Any], *, compact_for_llm: bool=False)` → `dict[str, Any]`
- **职责**：Compact, auditable facts sent to the final narrative LLM.
- **依赖**：add_context、add_execution、allowed_cal_times.add、authorized_execution_levels.append、bool、build_pa_llm_summary、context_levels.append、endswith、enumerate、float、get、info.get、isinstance、items、lvl.get、metrics.get、next、reg_facts.get、reg_facts.items、registry.get
- **复杂度 / 风险**：分支 27；跨度 165 行；high
- **测试 / 验证**：[tests/unit/test_narrative_combine.py](../../tests/unit/test_narrative_combine.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py) · direct-dynamic

<a id="fun-0717bfae8a"></a>

#### `build_narrative_facts.add_context`

- **ID / 行**：`FUN-0717BFAE8A` / `L233`（源码见本单元概览）
- **签名 / 返回**：`build_narrative_facts.add_context(level_id: str, value: Any, source: str, *, timeframe: str | None=None, kind: str='level')` → `None`
- **职责**：As-built responsibility derived from `add_context` and its owning unit.
- **依赖**：context_levels.append、float、round
- **复杂度 / 风险**：分支 2；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-287fb686ea"></a>

#### `build_narrative_facts.add_execution`

- **ID / 行**：`FUN-287FB686EA` / `L244`（源码见本单元概览）
- **签名 / 返回**：`build_narrative_facts.add_execution(level_id: str, value: Any, source: str, *, signal_id: str, kind: str='execution')` → `None`
- **职责**：As-built responsibility derived from `add_execution` and its owning unit.
- **依赖**：authorized_execution_levels.append、float、round
- **复杂度 / 风险**：分支 2；跨度 16 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f0ff3fb2e4"></a>

#### `validate_and_merge_llm_sections`

- **ID / 行**：`FUN-F0FF3FB2E4` / `L390`（源码见本单元概览）
- **签名 / 返回**：`validate_and_merge_llm_sections(raw_sections: Any, *, rule_sections: dict[str, dict[str, Any]], facts: dict[str, Any], mode: str, threshold: float)` → `tuple[dict[str, dict[str, Any]], dict[str, Any]]`
- **职责**：Validate each LLM block independently and fall back only that block.
- **依赖**：_confidence、_expected_bias、_normalize_llm_section、_section、_validate_section、common.get、deepcopy、facts.get、float、isinstance、round、rule_sections.get、str、strip、supplied.get
- **复杂度 / 风险**：分支 4；跨度 48 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py) · direct-dynamic

<a id="fun-58e4660f21"></a>

#### `_confidence`

- **ID / 行**：`FUN-58E4660F21` / `L440`（源码见本单元概览）
- **签名 / 返回**：`_confidence(value: Any)` → `float`
- **职责**：As-built responsibility derived from `_confidence` and its owning unit.
- **依赖**：float、get、max、min
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e6ef29ff95"></a>

#### `_coerce_string_list`

- **ID / 行**：`FUN-E6EF29FF95` / `L447`（源码见本单元概览）
- **签名 / 返回**：`_coerce_string_list(value: Any)` → `list[str] | None`
- **职责**：Normalize LLM list fields: bare string → one-item list; scalar items → str.
- **依赖**：isinstance、item.strip、out.append、str、value.strip
- **复杂度 / 风险**：分支 9；跨度 25 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ca4fa260dd"></a>

#### `_capped_section_lists`

- **ID / 行**：`FUN-CA4FA260DD` / `L474`（源码见本单元概览）
- **签名 / 返回**：`_capped_section_lists(value: dict[str, Any])` → `dict[str, list[str]]`
- **职责**：As-built responsibility derived from `_capped_section_lists` and its owning unit.
- **依赖**：_SECTION_LIST_CAPS.items、_coerce_string_list、value.get
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-3a8882518c"></a>

#### `_section_visible_lines`

- **ID / 行**：`FUN-3A8882518C` / `L484`（源码见本单元概览）
- **签名 / 返回**：`_section_visible_lines(value: dict[str, Any])` → `int`
- **职责**：Count UI rows after the same list caps applied during merge.
- **依赖**：_capped_section_lists、len、str、strip、value.get
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-75bc1eba00"></a>

#### `_normalize_llm_section`

- **ID / 行**：`FUN-75BC1EBA00` / `L492`（源码见本单元概览）
- **签名 / 返回**：`_normalize_llm_section(value: dict[str, Any])` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_normalize_llm_section` and its owning unit.
- **依赖**：_capped_section_lists、_confidence、str、strip
- **复杂度 / 风险**：分支 0；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5c22fbf976"></a>

#### `_validate_section`

- **ID / 行**：`FUN-5C22FBF976` / `L506`（源码见本单元概览）
- **签名 / 返回**：`_validate_section(value: Any, *, allowed: set[float], expected_bias: str, calendar_state: str='', allowed_calendar_times: set[str] | None=None)` → `str | None`
- **职责**：As-built responsibility derived from `_validate_section` and its owning unit.
- **依赖**：_NUMBER_RE.findall、_coerce_string_list、_section_visible_lines、_unapproved_calendar_claims、abs、any、float、isinstance、join、narrative_price_tolerance、set、str、strip、value.get
- **复杂度 / 风险**：分支 13；跨度 55 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-21729c6d78"></a>

#### `_expected_bias`

- **ID / 行**：`FUN-21729C6D78` / `L563`（源码见本单元概览）
- **签名 / 返回**：`_expected_bias(facts: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_expected_bias` and its owning unit.
- **依赖**：common.get、decision.get、facts.get、float、lower、sentiment.get、signal.get、str
- **复杂度 / 风险**：分支 5；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-74a552c2a1"></a>

#### `narrative_price_tolerance`

- **ID / 行**：`FUN-74A552C2A1` / `L581`（源码见本单元概览）
- **签名 / 返回**：`narrative_price_tolerance(token: str, reference: float)` → `float`
- **职责**：Match LLM price tokens to whitelist levels.
- **依赖**：frac.rstrip、len、token.split
- **复杂度 / 风险**：分支 3；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ea3075165b"></a>

#### `_price_tolerance`

- **ID / 行**：`FUN-EA3075165B` / `L602`（源码见本单元概览）
- **签名 / 返回**：`_price_tolerance(reference: float)` → `float`
- **职责**：Legacy helper — prefer :func:`narrative_price_tolerance` with the raw token.
- **依赖**：abs、max
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ee96ece754"></a>

#### `_unapproved_prices`

- **ID / 行**：`FUN-EE96ECE754` / `L607`（源码见本单元概览）
- **签名 / 返回**：`_unapproved_prices(text: str, allowed: set[float])` → `str | None`
- **职责**：As-built responsibility derived from `_unapproved_prices` and its owning unit.
- **依赖**：_NUMBER_RE.findall、abs、any、float、narrative_price_tolerance
- **复杂度 / 风险**：分支 4；跨度 13 行；low
- **测试 / 验证**：[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py) · direct-dynamic

<a id="fun-6cde98503a"></a>

#### `_unapproved_calendar_claims`

- **ID / 行**：`FUN-6CDE98503A` / `L629`（源码见本单元概览）
- **签名 / 返回**：`_unapproved_calendar_claims(text: str, *, calendar_state: str, allowed_times: set[str])` → `str | None`
- **职责**：Reject concrete clock+event claims when calendar is empty or time unregistered (#38).
- **依赖**：_CALENDAR_CLAIM_RE.finditer、any、clock.endswith、match.group、strip、t.endswith、text.strip
- **复杂度 / 风险**：分支 6；跨度 24 行；low
- **测试 / 验证**：[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py) · direct-dynamic

<a id="fun-870e7671a1"></a>

#### `_executable_wording_on_wait`

- **ID / 行**：`FUN-870E7671A1` / `L687`（源码见本单元概览）
- **签名 / 返回**：`_executable_wording_on_wait(text: str)` → `bool`
- **职责**：As-built responsibility derived from `_executable_wording_on_wait` and its owning unit.
- **依赖**：any、re.search
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b4dcb46a68"></a>

#### `_direction_conflict`

- **ID / 行**：`FUN-B4DCB46A68` / `L693`（源码见本单元概览）
- **签名 / 返回**：`_direction_conflict(text: str, expected_bias: str)` → `str | None`
- **职责**：As-built responsibility derived from `_direction_conflict` and its owning unit.
- **依赖**：any
- **复杂度 / 风险**：分支 2；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-25aeefe31c"></a>

#### `_execution_authorized`

- **ID / 行**：`FUN-25AEEFE31C` / `L705`（源码见本单元概览）
- **签名 / 返回**：`_execution_authorized(facts: dict[str, Any])` → `bool`
- **职责**：As-built responsibility derived from `_execution_authorized` and its owning unit.
- **依赖**：common.get、decision.get、facts.get、str
- **复杂度 / 风险**：分支 2；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-d7185cbde0"></a>

#### `validate_llm_top_level_fields`

- **ID / 行**：`FUN-D7185CBDE0` / `L716`（源码见本单元概览）
- **签名 / 返回**：`validate_llm_top_level_fields(llm: dict[str, Any], *, facts: dict[str, Any])` → `dict[str, str | None]`
- **职责**：Per-field validation; value is rejection reason or None when accepted.
- **依赖**：_direction_conflict、_executable_wording_on_wait、_execution_authorized、_expected_bias、_unapproved_calendar_claims、_unapproved_prices、any、common.get、decision.get、facts.get、fields.items、fields.values、float、get、llm.get、round、str、strip、sum、text.strip
- **复杂度 / 风险**：分支 14；跨度 71 行；medium
- **测试 / 验证**：[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py)、[tests/unit/test_narrative_top_level.py](../../tests/unit/test_narrative_top_level.py) · direct-dynamic

<a id="fun-5260c4fffe"></a>

#### `validate_llm_top_level`

- **ID / 行**：`FUN-5260C4FFFE` / `L789`（源码见本单元概览）
- **签名 / 返回**：`validate_llm_top_level(llm: dict[str, Any], *, facts: dict[str, Any])` → `str | None`
- **职责**：Validate market_summary / trade_thesis / action_plan against authorized facts.
- **依赖**：field_reasons.values、validate_llm_top_level_fields
- **复杂度 / 风险**：分支 2；跨度 11 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_top_level.py](../../tests/unit/test_narrative_top_level.py) · direct-dynamic

<a id="unit-406cec1297"></a>

### src/analysis/plan_signals.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-406CEC1297 |
| 源码 | [src/analysis/plan_signals.py](../../src/analysis/plan_signals.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | PA-primary trading plans with SMC as score filter only. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 20 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_plan_signal_targets.py](../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_plan_signals.py](../../tests/unit/test_plan_signals.py) |
| 验证状态 | selected |

#### 函数导航

[pa_usable](#fun-df2b309e7a) · [_rule_sr_level](#fun-edbd519580) · [build_rule_pa_block](#fun-a04f67d803) · [_atr](#fun-d4e38583ee) · [_zone_band](#fun-7820ca9cf2) · [_nearest_pa_sr](#fun-b2869caf10) · [_vah_zone](#fun-0cc973c97b) · [_resistance_zone](#fun-0924b3ca47) · [_val_zone](#fun-2dc7daba92) · [_support_zone](#fun-05d58d82e1) · [_sell_targets](#fun-ce8413dcd6) · [_buy_targets](#fun-e65ed5c0aa) · [_smc_zones](#fun-88ad48e01b) · [_zone_overlaps_entry](#fun-e5ee860a8a) · [_structure_shifted](#fun-9a867fc2bd) · [smc_filter_adjustment](#fun-cd33dcdad5) · [val_sweep_confirmed](#fun-9cd2c897d0) · [build_pa_short_aggressive](#fun-8f66092349) · [build_pa_short_conservative](#fun-f24046f4b0) · [build_pa_long_sweep](#fun-c5a6f97a5f)

<a id="fun-df2b309e7a"></a>

#### `pa_usable`

- **ID / 行**：`FUN-DF2B309E7A` / `L30`（源码见本单元概览）
- **签名 / 返回**：`pa_usable(price_action: dict[str, Any] | None)` → `bool`
- **职责**：As-built responsibility derived from `pa_usable` and its owning unit.
- **依赖**：block.get、bool、price_action.get、vp.get
- **复杂度 / 风险**：分支 2；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-edbd519580"></a>

#### `_rule_sr_level`

- **ID / 行**：`FUN-EDBD519580` / `L41`（源码见本单元概览）
- **签名 / 返回**：`_rule_sr_level(price: float, direction: str, label: str)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_rule_sr_level` and its owning unit.
- **依赖**：float、round
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a04f67d803"></a>

#### `build_rule_pa_block`

- **ID / 行**：`FUN-A04F67D803` / `L51`（源码见本单元概览）
- **签名 / 返回**：`build_rule_pa_block(*, price: float, swing_high: float, swing_low: float, analysis_5m: TimeframeAnalysis, price_action: dict[str, Any] | None=None, metrics: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：Synthesize minimal 5m PA facts from price anchors when DGT output is insufficient.
- **依赖**：_rule_sr_level、abs、any、bool、existing_vp.get、float、get、list、lvl.get、max、metrics.get、min、pa5.get、round、sr_levels.append、vp.get
- **复杂度 / 风险**：分支 10；跨度 74 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d4e38583ee"></a>

#### `_atr`

- **ID / 行**：`FUN-D4E38583EE` / `L127`（源码见本单元概览）
- **签名 / 返回**：`_atr(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` → `float`
- **职责**：As-built responsibility derived from `_atr` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7820ca9cf2"></a>

#### `_zone_band`

- **ID / 行**：`FUN-7820CA9CF2` / `L131`（源码见本单元概览）
- **签名 / 返回**：`_zone_band(center: float, atr: float, *, ratio: float=0.2)` → `tuple[float, float]`
- **职责**：As-built responsibility derived from `_zone_band` and its owning unit.
- **依赖**：max、round
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b2869caf10"></a>

#### `_nearest_pa_sr`

- **ID / 行**：`FUN-B2869CAF10` / `L136`（源码见本单元概览）
- **签名 / 返回**：`_nearest_pa_sr(sr_levels: list[dict[str, Any]], price: float, direction: str)` → `dict[str, Any] | None`
- **职责**：As-built responsibility derived from `_nearest_pa_sr` and its owning unit.
- **依赖**：float、lvl.get、parsed.sort
- **复杂度 / 风险**：分支 2；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0cc973c97b"></a>

#### `_vah_zone`

- **ID / 行**：`FUN-0CC973C97B` / `L156`（源码见本单元概览）
- **签名 / 返回**：`_vah_zone(vp: dict[str, Any], atr: float)` → `_PaZone | None`
- **职责**：As-built responsibility derived from `_vah_zone` and its owning unit.
- **依赖**：_PaZone、_zone_band、float、vp.get
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0924b3ca47"></a>

#### `_resistance_zone`

- **ID / 行**：`FUN-0924B3CA47` / `L164`（源码见本单元概览）
- **签名 / 返回**：`_resistance_zone(sr: dict[str, Any], atr: float)` → `_PaZone`
- **职责**：As-built responsibility derived from `_resistance_zone` and its owning unit.
- **依赖**：_PaZone、_zone_band、float、sr.get、str
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2dc7daba92"></a>

#### `_val_zone`

- **ID / 行**：`FUN-2DC7DABA92` / `L171`（源码见本单元概览）
- **签名 / 返回**：`_val_zone(vp: dict[str, Any], atr: float)` → `_PaZone | None`
- **职责**：As-built responsibility derived from `_val_zone` and its owning unit.
- **依赖**：_PaZone、_zone_band、float、vp.get
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-05d58d82e1"></a>

#### `_support_zone`

- **ID / 行**：`FUN-05D58D82E1` / `L179`（源码见本单元概览）
- **签名 / 返回**：`_support_zone(sr: dict[str, Any], atr: float)` → `_PaZone`
- **职责**：As-built responsibility derived from `_support_zone` and its owning unit.
- **依赖**：_PaZone、_zone_band、float、max、round、sr.get、str
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ce8413dcd6"></a>

#### `_sell_targets`

- **ID / 行**：`FUN-CE8413DCD6` / `L186`（源码见本单元概览）
- **签名 / 返回**：`_sell_targets(entry_low: float, entry_high: float, *, poc: float | None, val: float | None, swing_low: float)` → `tuple[float, float, float] | None`
- **职责**：As-built responsibility derived from `_sell_targets` and its owning unit.
- **依赖**：candidates.append、float、len、max、normalize_take_profits、round
- **复杂度 / 风险**：分支 6；跨度 39 行；low
- **测试 / 验证**：[tests/unit/test_plan_signal_targets.py](../../tests/unit/test_plan_signal_targets.py) · direct-dynamic

<a id="fun-e65ed5c0aa"></a>

#### `_buy_targets`

- **ID / 行**：`FUN-E65ED5C0AA` / `L227`（源码见本单元概览）
- **签名 / 返回**：`_buy_targets(entry_low: float, entry_high: float, *, price: float, poc: float | None, vah: float | None, swing_high: float, swing_low: float)` → `tuple[float, float, float]`
- **职责**：As-built responsibility derived from `_buy_targets` and its owning unit.
- **依赖**：candidates.append、float、len、max、normalize_take_profits、ordered.append、round
- **复杂度 / 风险**：分支 6；跨度 37 行；low
- **测试 / 验证**：[tests/unit/test_plan_signal_targets.py](../../tests/unit/test_plan_signal_targets.py) · direct-dynamic

<a id="fun-88ad48e01b"></a>

#### `_smc_zones`

- **ID / 行**：`FUN-88AD48E01B` / `L266`（源码见本单元概览）
- **签名 / 返回**：`_smc_zones(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` → `list[tuple[float, float, str]]`
- **职责**：As-built responsibility derived from `_smc_zones` and its owning unit.
- **依赖**：zones.append
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e5ee860a8a"></a>

#### `_zone_overlaps_entry`

- **ID / 行**：`FUN-E5EE860A8A` / `L276`（源码见本单元概览）
- **签名 / 返回**：`_zone_overlaps_entry(zone_low: float, zone_high: float, entry_low: float, entry_high: float, *, tolerance: float=RESONANCE_TOLERANCE)` → `bool`
- **职责**：As-built responsibility derived from `_zone_overlaps_entry` and its owning unit.
- **依赖**：abs
- **复杂度 / 风险**：分支 1；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9a867fc2bd"></a>

#### `_structure_shifted`

- **ID / 行**：`FUN-9A867FC2BD` / `L291`（源码见本单元概览）
- **签名 / 返回**：`_structure_shifted(analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, *, direction: str)` → `bool`
- **职责**：As-built responsibility derived from `_structure_shifted` and its owning unit.
- **依赖**：any、direction.lower、lower、upper
- **复杂度 / 风险**：分支 0；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-cd33dcdad5"></a>

#### `smc_filter_adjustment`

- **ID / 行**：`FUN-CD33DCDAD5` / `L306`（源码见本单元概览）
- **签名 / 返回**：`smc_filter_adjustment(*, direction: str, entry_low: float, entry_high: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` → `_SmcFilter`
- **职责**：Score-only SMC filter; never suppresses a PA plan.
- **依赖**：_SmcFilter、_smc_zones、_zone_overlaps_entry、join、reasons.append、sorted、upper
- **复杂度 / 风险**：分支 8；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_plan_signals.py](../../tests/unit/test_plan_signals.py) · direct-dynamic

<a id="fun-9cd2c897d0"></a>

#### `val_sweep_confirmed`

- **ID / 行**：`FUN-9CD2C897D0` / `L352`（源码见本单元概览）
- **签名 / 返回**：`val_sweep_confirmed(*, price: float, val: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` → `tuple[bool, list[str]]`
- **职责**：PA VAL sweep + reclaim; CHoCH/BOS bullish is SMC filter, not hard gate.
- **依赖**：_atr、_structure_shifted、float、max、reasons.append
- **复杂度 / 风险**：分支 5；跨度 30 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8f66092349"></a>

#### `build_pa_short_aggressive`

- **ID / 行**：`FUN-8F66092349` / `L384`（源码见本单元概览）
- **签名 / 返回**：`build_pa_short_aggressive(*, price: float, pa_block: dict[str, Any], swing_low: float, atr: float)` → `tuple[_PaZone, float, list[float]] | None`
- **职责**：As-built responsibility derived from `build_pa_short_aggressive` and its owning unit.
- **依赖**：_nearest_pa_sr、_resistance_zone、_sell_targets、float、list、max、pa_block.get、round、vp.get
- **复杂度 / 风险**：分支 3；跨度 26 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f24046f4b0"></a>

#### `build_pa_short_conservative`

- **ID / 行**：`FUN-F24046F4B0` / `L412`（源码见本单元概览）
- **签名 / 返回**：`build_pa_short_conservative(*, price: float, pa_block: dict[str, Any], swing_low: float, atr: float)` → `tuple[_PaZone, float, list[float]] | None`
- **职责**：As-built responsibility derived from `build_pa_short_conservative` and its owning unit.
- **依赖**：_nearest_pa_sr、_resistance_zone、_sell_targets、_vah_zone、list、max、pa_block.get、round、vp.get
- **复杂度 / 风险**：分支 3；跨度 26 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c5a6f97a5f"></a>

#### `build_pa_long_sweep`

- **ID / 行**：`FUN-C5A6F97A5F` / `L440`（源码见本单元概览）
- **签名 / 返回**：`build_pa_long_sweep(*, price: float, pa_block: dict[str, Any], swing_high: float, swing_low: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis)` → `tuple[_PaZone, float, list[float], bool, list[str]] | None`
- **职责**：As-built responsibility derived from `build_pa_long_sweep` and its owning unit.
- **依赖**：_PaZone、_atr、_buy_targets、_nearest_pa_sr、_support_zone、float、list、max、pa_block.get、round、val_sweep_confirmed、vp.get
- **复杂度 / 风险**：分支 2；跨度 52 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-daf97d09e5"></a>

### src/analysis/price_action_facts.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAF97D09E5 |
| 源码 | [src/analysis/price_action_facts.py](../../src/analysis/price_action_facts.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Assemble DGT price-action facts for report schema and LLM. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) |
| 验证状态 | selected |

#### 函数导航

[_ltf_covers_window](#fun-c06b90a09b) · [_align_timestamp](#fun-bce4e6db5f) · [_bars_for_latest_session_day](#fun-cf1adc9362) · [_session_matches_daily](#fun-a13f4e6eec) · [build_session_price_action_block](#fun-6da9739c93) · [build_price_action_summaries](#fun-c677f127b2) · [chart_sr_levels](#fun-edaa738364)

<a id="fun-c06b90a09b"></a>

#### `_ltf_covers_window`

- **ID / 行**：`FUN-C06B90A09B` / `L24`（源码见本单元概览）
- **签名 / 返回**：`_ltf_covers_window(ltf_slice: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp, *, min_frac: float=_LTF_COVER_FRAC)` → `bool`
- **职责**：True when lower-TF bars span ≥ min_frac of the HTF clock window.
- **依赖**：max、min、pd.Timestamp、total_seconds
- **复杂度 / 风险**：分支 3；跨度 19 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-bce4e6db5f"></a>

#### `_align_timestamp`

- **ID / 行**：`FUN-BCE4E6DB5F` / `L45`（源码见本单元概览）
- **签名 / 返回**：`_align_timestamp(ts: pd.Timestamp, ref: pd.DatetimeIndex)` → `pd.Timestamp`
- **职责**：As-built responsibility derived from `_align_timestamp` and its owning unit.
- **依赖**：pd.Timestamp、ts.tz_convert、ts.tz_localize、tz_convert、tz_localize
- **复杂度 / 风险**：分支 3；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-cf1adc9362"></a>

#### `_bars_for_latest_session_day`

- **ID / 行**：`FUN-CF1ADC9362` / `L56`（源码见本单元概览）
- **签名 / 返回**：`_bars_for_latest_session_day(df_5m: pd.DataFrame, df_1d: pd.DataFrame)` → `pd.DataFrame`
- **职责**：5m bars for the provider daily session anchored at the latest 1d bar open.
- **依赖**：_align_timestamp、isinstance、min、pd.Timedelta
- **复杂度 / 风险**：分支 2；跨度 15 行；low
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="fun-a13f4e6eec"></a>

#### `_session_matches_daily`

- **ID / 行**：`FUN-A13F4E6EEC` / `L73`（源码见本单元概览）
- **签名 / 返回**：`_session_matches_daily(df_session: pd.DataFrame, daily_row: pd.Series, *, tol: float)` → `bool`
- **职责**：As-built responsibility derived from `_session_matches_daily` and its owning unit.
- **依赖**：abs、float、max、min
- **复杂度 / 风险**：分支 1；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6da9739c93"></a>

#### `build_session_price_action_block`

- **ID / 行**：`FUN-6DA9739C93` / `L86`（源码见本单元概览）
- **签名 / 返回**：`build_session_price_action_block(df_5m: pd.DataFrame | None, df_1d: pd.DataFrame | None)` → `dict[str, Any] | None`
- **职责**：Intraday PA block: session-day volume profile + 量价 S/R from all 5m bars that day.
- **依赖**：_bars_for_latest_session_day、_session_matches_daily、analyze_dgt_price_action、dgt_result_to_dict、len
- **复杂度 / 风险**：分支 4；跨度 22 行；medium
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="fun-c677f127b2"></a>

#### `build_price_action_summaries`

- **ID / 行**：`FUN-C677F127B2` / `L110`（源码见本单元概览）
- **签名 / 返回**：`build_price_action_summaries(data: dict[str, pd.DataFrame], *, lookback: int=DEFAULT_LOOKBACK)` → `dict[str, dict[str, Any]]`
- **职责**：Per-TF DGT metrics with Pine Fixed-Range lookback (default 360 bars).
- **依赖**：_ltf_covers_window、analyze_dgt_price_action、build_session_price_action_block、data.get、df.tail、dgt_result_to_dict
- **复杂度 / 风险**：分支 5；跨度 39 行；medium
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="fun-edaa738364"></a>

#### `chart_sr_levels`

- **ID / 行**：`FUN-EDAA738364` / `L151`（源码见本单元概览）
- **签名 / 返回**：`chart_sr_levels(report: dict[str, Any], timeframe: str='5m')` → `list[dict[str, Any]]`
- **职责**：Raw S/R list for chart overlays on the given timeframe.
- **依赖**：block.get、list、pa.get、report.get
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_dgt_price_action.py](../../tests/unit/test_dgt_price_action.py) · direct-dynamic

<a id="unit-ce01c0290c"></a>

### src/analysis/proximity.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CE01C0290C |
| 源码 | [src/analysis/proximity.py](../../src/analysis/proximity.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Price-distance helpers for execution vs context structure levels. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_proximity.py](../../tests/unit/test_proximity.py) |
| 验证状态 | selected |

#### 函数导航

[proximity_threshold](#fun-575ce11369) · [zone_near_price](#fun-914f4d90ea) · [level_near_price](#fun-8793f9d1f1)

<a id="fun-575ce11369"></a>

#### `proximity_threshold`

- **ID / 行**：`FUN-575CE11369` / `L12`（源码见本单元概览）
- **签名 / 返回**：`proximity_threshold(price: float, atr: float | None, *, atr_mult: float=1.0, pct: float=PCT_FALLBACK)` → `float`
- **职责**：As-built responsibility derived from `proximity_threshold` and its owning unit.
- **依赖**：max
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-914f4d90ea"></a>

#### `zone_near_price`

- **ID / 行**：`FUN-914F4D90EA` / `L22`（源码见本单元概览）
- **签名 / 返回**：`zone_near_price(price: float, low: float, high: float, atr: float | None, *, atr_mult: float=1.0, pct: float=PCT_FALLBACK)` → `bool`
- **职责**：True when price is inside the zone or within the ATR/pct band.
- **依赖**：abs、max、min、proximity_threshold
- **复杂度 / 风险**：分支 1；跨度 15 行；medium
- **测试 / 验证**：[tests/unit/test_proximity.py](../../tests/unit/test_proximity.py) · direct-dynamic

<a id="fun-8793f9d1f1"></a>

#### `level_near_price`

- **ID / 行**：`FUN-8793F9D1F1` / `L39`（源码见本单元概览）
- **签名 / 返回**：`level_near_price(level: float, price: float, atr: float | None, *, atr_mult: float=1.0, pct: float=PCT_FALLBACK)` → `bool`
- **职责**：As-built responsibility derived from `level_near_price` and its owning unit.
- **依赖**：abs、proximity_threshold
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_proximity.py](../../tests/unit/test_proximity.py) · direct-dynamic

<a id="unit-dad8a91ff9"></a>

### src/analysis/report_engine.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DAD8A91FF9 |
| 源码 | [src/analysis/report_engine.py](../../src/analysis/report_engine.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Report assembly: trading plans, conclusions, projections. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 44 / 8 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_backtest_simulator.py](../../tests/unit/test_backtest_simulator.py)、[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py)、[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_plan_signals.py](../../tests/unit/test_plan_signals.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[_compute_risk_reward](#fun-46bd20a480) · [_risk_reward_ratio](#fun-dcc89b25ee) · [_grade](#fun-15ed1e142c) · [_zone_relation](#fun-79027dc513) · [_stop_breached](#fun-4edf24baf8) · [_setup_status_and_score](#fun-216988a705) · [compute_trading_signals](#fun-db79153948) · [_apply_smc_filter_score](#fun-c46ab92251) · [_finalize_pa_plan_meta](#fun-b29ba1665b) · [generate_trading_signals](#fun-7b436508b0) · [_generate_pa_signals](#fun-3121795202) · [trend_projections](#fun-570c5667b7) · [build_conclusion](#fun-e3c1c289a1) · [invalidation_rules](#fun-a5ab9c9398) · [parse_risk_events_calendar](#fun-5fd97aa52d) · [build_calendar_events](#fun-fddea7563f) · [calendar_rows_from_external](#fun-c04ff0655e) · [_build_context_levels](#fun-3196d79811) · [build_key_levels](#fun-6ab88c4476) · [build_resistance_support](#fun-0e716fdbd6) · [_signal_value](#fun-666ae14d42) · [_assign_signal_roles](#fun-5dd9e47b1e) · [build_strategy_plans](#fun-a1e1bc8771) · [authorized_position_scale](#fun-b8f52e3dc7) · [format_authorized_position_size](#fun-a43ced947f) · [_normalize_signal_dict_take_profits](#fun-34dce71c07) · [_review_field](#fun-e8ad3336d7) · [_format_risk_veto_lines](#fun-be4a18b71c) · [_format_trader_veto_lines](#fun-4c3a66bdae) · [_format_level_validation_lines](#fun-15ccc085e1) · [build_signal_rejection_notes](#fun-3539753867) · [build_signal_rejection_reason](#fun-3bf762bd92) · [_signal_to_dict](#fun-442599ada0) · [_assign_signal_ids](#fun-9883fd47f5) · [_signal_execution_ready](#fun-435783f2d2) · [apply_manager_authorization](#fun-5d6d01887f) · [apply_manager_authorization._attach_rejection](#fun-91b63c3cae) · [apply_manager_authorization._clear_auth_meta](#fun-6d5b47fa9d) · [_authorized_primary_signal](#fun-358a1e0942) · [_format_entry_zone](#fun-26766e75ae) · [build_final_decision_meta](#fun-f903e47206) · [align_conclusion_with_manager_decision](#fun-db059d9e58) · [build_path_summary](#fun-cc7188b273) · [build_report](#fun-65d3afa4f8)

<a id="fun-46bd20a480"></a>

#### `_compute_risk_reward`

- **ID / 行**：`FUN-46BD20A480` / `L78`（源码见本单元概览）
- **签名 / 返回**：`_compute_risk_reward(*, direction: str, entry_low: float, entry_high: float, stop_loss: float, take_profits: list[float])` → `str`
- **职责**：As-built responsibility derived from `_compute_risk_reward` and its owning unit.
- **复杂度 / 风险**：分支 4；跨度 24 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-dcc89b25ee"></a>

#### `_risk_reward_ratio`

- **ID / 行**：`FUN-DCC89B25EE` / `L104`（源码见本单元概览）
- **签名 / 返回**：`_risk_reward_ratio(*, direction: str, entry_low: float, entry_high: float, stop_loss: float, take_profits: list[float])` → `float`
- **职责**：As-built responsibility derived from `_risk_reward_ratio` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 21 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-15ed1e142c"></a>

#### `_grade`

- **ID / 行**：`FUN-15ED1E142C` / `L127`（源码见本单元概览）
- **签名 / 返回**：`_grade(score: float)` → `str`
- **职责**：As-built responsibility derived from `_grade` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-79027dc513"></a>

#### `_zone_relation`

- **ID / 行**：`FUN-79027DC513` / `L137`（源码见本单元概览）
- **签名 / 返回**：`_zone_relation(*, price: float, direction: str, entry_low: float, entry_high: float)` → `tuple[str, float]`
- **职责**：As-built responsibility derived from `_zone_relation` and its owning unit.
- **复杂度 / 风险**：分支 5；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4edf24baf8"></a>

#### `_stop_breached`

- **ID / 行**：`FUN-4EDF24BAF8` / `L157`（源码见本单元概览）
- **签名 / 返回**：`_stop_breached(*, price: float, direction: str, stop_loss: float)` → `bool`
- **职责**：True when the current price has already crossed the plan invalidation stop.
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-216988a705"></a>

#### `_setup_status_and_score`

- **ID / 行**：`FUN-216988A705` / `L164`（源码见本单元概览）
- **签名 / 返回**：`_setup_status_and_score(*, name: str, direction: str, theme: str, setup_type: str, price: float, entry_low: float, entry_high: float, stop_loss: float, take_profits: list[float], sentiment: dict[str, float], trigger_confirmed: bool=False)` → `tuple[str, bool, str, float, str, list[str]]`
- **职责**：As-built responsibility derived from `_setup_status_and_score` and its owning unit.
- **依赖**：_grade、_risk_reward_ratio、_stop_breached、_zone_relation、min、reasons.append、round、sentiment.get
- **复杂度 / 风险**：分支 18；跨度 91 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-db79153948"></a>

#### `compute_trading_signals`

- **ID / 行**：`FUN-DB79153948` / `L257`（源码见本单元概览）
- **签名 / 返回**：`compute_trading_signals(ctx: MarketContext)` → `list[TradingSignal]`
- **职责**：Single entry point for pipeline signal generation (trader + report share this).
- **依赖**：analyses.get、build_price_action_summaries、generate_trading_signals、sentiment_score
- **复杂度 / 风险**：分支 2；跨度 22 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="fun-c46ab92251"></a>

#### `_apply_smc_filter_score`

- **ID / 行**：`FUN-C46AB92251` / `L281`（源码见本单元概览）
- **签名 / 返回**：`_apply_smc_filter_score(*, direction: str, entry_low: float, entry_high: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, score: float, reasons: list[str])` → `tuple[float, str, list[str]]`
- **职责**：As-built responsibility derived from `_apply_smc_filter_score` and its owning unit.
- **依赖**：_grade、max、min、reasons.extend、round、smc_filter_adjustment
- **复杂度 / 风险**：分支 0；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b29ba1665b"></a>

#### `_finalize_pa_plan_meta`

- **ID / 行**：`FUN-B29BA1665B` / `L303`（源码见本单元概览）
- **签名 / 返回**：`_finalize_pa_plan_meta(*, rule_fallback: bool, setup_type: str, zone_label: str, score: float, grade: str, reasons: list[str], short_note: str | None=None)` → `tuple[str, str, float, str, list[str]]`
- **职责**：As-built responsibility derived from `_finalize_pa_plan_meta` and its owning unit.
- **依赖**：_grade、max、round
- **复杂度 / 风险**：分支 2；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7b436508b0"></a>

#### `generate_trading_signals`

- **ID / 行**：`FUN-7B436508B0` / `L325`（源码见本单元概览）
- **签名 / 返回**：`generate_trading_signals(price: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, swing_high: float, swing_low: float, sentiment: dict[str, float], *, price_action: dict[str, Any] | None=None, metrics: dict[str, Any] | None=None)` → `list[TradingSignal]`
- **职责**：As-built responsibility derived from `generate_trading_signals` and its owning unit.
- **依赖**：_generate_pa_signals、build_rule_pa_block、pa_usable
- **复杂度 / 风险**：分支 2；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_plan_signals.py](../../tests/unit/test_plan_signals.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="fun-3121795202"></a>

#### `_generate_pa_signals`

- **ID / 行**：`FUN-3121795202` / `L371`（源码见本单元概览）
- **签名 / 返回**：`_generate_pa_signals(price: float, analysis_5m: TimeframeAnalysis, analysis_15m: TimeframeAnalysis, swing_high: float, swing_low: float, sentiment: dict[str, float], *, price_action: dict[str, Any], rule_fallback: bool=False)` → `list[TradingSignal]`
- **职责**：As-built responsibility derived from `_generate_pa_signals` and its owning unit.
- **依赖**：TradingSignal、_apply_smc_filter_score、_compute_risk_reward、_finalize_pa_plan_meta、_grade、_setup_status_and_score、build_pa_long_sweep、build_pa_short_aggressive、build_pa_short_conservative、int、max、min、price_action.get、reasons.append、reasons.extend、round、sentiment.get、signals.append
- **复杂度 / 风险**：分支 8；跨度 237 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-570c5667b7"></a>

#### `trend_projections`

- **ID / 行**：`FUN-570C5667B7` / `L610`（源码见本单元概览）
- **签名 / 返回**：`trend_projections(price: float, swing_high: float, swing_low: float, sentiment: dict[str, float])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `trend_projections` and its owning unit.
- **依赖**：max、round、sentiment.get
- **复杂度 / 风险**：分支 3；跨度 118 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py) · direct-dynamic

<a id="fun-e3c1c289a1"></a>

#### `build_conclusion`

- **ID / 行**：`FUN-E3C1C289A1` / `L730`（源码见本单元概览）
- **签名 / 返回**：`build_conclusion(sentiment: dict[str, float], primary_trend: str, signals: list[TradingSignal])` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_conclusion` and its owning unit.
- **依赖**：max、next、sentiment.get
- **复杂度 / 风险**：分支 11；跨度 73 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py) · direct-dynamic

<a id="fun-a5ab9c9398"></a>

#### `invalidation_rules`

- **ID / 行**：`FUN-A5AB9C9398` / `L805`（源码见本单元概览）
- **签名 / 返回**：`invalidation_rules(analysis_15m: TimeframeAnalysis, swing_high: float, signals: list[TradingSignal])` → `list[str]`
- **职责**：As-built responsibility derived from `invalidation_rules` and its owning unit.
- **依赖**：max、round、rules.insert
- **复杂度 / 风险**：分支 5；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5fd97aa52d"></a>

#### `parse_risk_events_calendar`

- **ID / 行**：`FUN-5FD97AA52D` / `L829`（源码见本单元概览）
- **签名 / 返回**：`parse_risk_events_calendar(risk_events: str)` → `list[dict[str, str]]`
- **职责**：Turn scraped calendar text into sidebar calendar rows.
- **依赖**：_CAL_EVENT_RE.match、body.lower、body.upper、events.append、m.group、part.strip、risk_events.split、startswith、strip
- **复杂度 / 风险**：分支 5；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fddea7563f"></a>

#### `build_calendar_events`

- **ID / 行**：`FUN-FDDEA7563F` / `L854`（源码见本单元概览）
- **签名 / 返回**：`build_calendar_events()` → `list[dict[str, str]]`
- **职责**：Legacy helper — returns empty; never inject example macro events.
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py) · direct-dynamic

<a id="fun-c04ff0655e"></a>

#### `calendar_rows_from_external`

- **ID / 行**：`FUN-C04FF0655E` / `L864`（源码见本单元概览）
- **签名 / 返回**：`calendar_rows_from_external(*, calendar_events: list[Any] | None=None, risk_events: str='—')` → `list[dict[str, str]]`
- **职责**：Build report calendar rows from structured events or risk text.
- **依赖**：body.lower、body.strip、body.upper、event.get、getattr、hasattr、isinstance、parse_risk_events_calendar、region.lower、rows.append、startswith、str
- **复杂度 / 风险**：分支 7；跨度 33 行；medium
- **测试 / 验证**：[tests/unit/test_calendar_empty.py](../../tests/unit/test_calendar_empty.py) · direct-dynamic

<a id="fun-3196d79811"></a>

#### `_build_context_levels`

- **ID / 行**：`FUN-3196D79811` / `L899`（源码见本单元概览）
- **签名 / 返回**：`_build_context_levels(price: float, swing_high: float, swing_low: float, swing_tf: str, swing_atr: float | None)` → `list[dict[str, Any]]`
- **职责**：Structure levels kept for decision reference but too far for the 5m execution chart.
- **依赖**：level_near_price、levels.append、round、swing_tf.upper
- **复杂度 / 风险**：分支 2；跨度 33 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6ab88c4476"></a>

#### `build_key_levels`

- **ID / 行**：`FUN-6AB88C4476` / `L934`（源码见本单元概览）
- **签名 / 返回**：`build_key_levels(price: float, metrics: dict, swing_high: float, swing_low: float, fib: list[dict], signals: list[TradingSignal], *, swing_tf: str='4h', swing_atr: float | None=None)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `build_key_levels` and its owning unit.
- **依赖**：len、levels.append、metrics.get、sorted、swing_tf.upper、x.get、zone_near_price
- **复杂度 / 风险**：分支 4；跨度 43 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0e716fdbd6"></a>

#### `build_resistance_support`

- **ID / 行**：`FUN-0E716FDBD6` / `L979`（源码见本单元概览）
- **签名 / 返回**：`build_resistance_support(key_levels: list[dict], liquidity: list[dict])` → `tuple[list[str], list[str]]`
- **职责**：As-built responsibility derived from `build_resistance_support` and its owning unit.
- **依赖**：item.get、lv.get、resist.append、support.append
- **复杂度 / 风险**：分支 6；跨度 25 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-666ae14d42"></a>

#### `_signal_value`

- **ID / 行**：`FUN-666AE14D42` / `L1006`（源码见本单元概览）
- **签名 / 返回**：`_signal_value(signal: TradingSignal | dict[str, Any], key: str, default: Any=None)` → `Any`
- **职责**：As-built responsibility derived from `_signal_value` and its owning unit.
- **依赖**：getattr、isinstance、signal.get
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5dd9e47b1e"></a>

#### `_assign_signal_roles`

- **ID / 行**：`FUN-5DD9E47B1E` / `L1012`（源码见本单元概览）
- **签名 / 返回**：`_assign_signal_roles(signals: list[TradingSignal], sentiment: dict[str, float])` → `None`
- **职责**：Mark one primary plan by dominant sentiment theme; rest are alternates.
- **依赖**：sentiment.get
- **复杂度 / 风险**：分支 3；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a1e1bc8771"></a>

#### `build_strategy_plans`

- **ID / 行**：`FUN-A1E1BC8771` / `L1024`（源码见本单元概览）
- **签名 / 返回**：`build_strategy_plans(signals: list[TradingSignal | dict[str, Any]])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `build_strategy_plans` and its owning unit.
- **依赖**：_signal_value、enumerate、join、len、plans.append、str
- **复杂度 / 风险**：分支 2；跨度 16 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py) · direct-dynamic

<a id="fun-b8f52e3dc7"></a>

#### `authorized_position_scale`

- **ID / 行**：`FUN-B8F52E3DC7` / `L1042`（源码见本单元概览）
- **签名 / 返回**：`authorized_position_scale(reviews: list, decision)` → `float`
- **职责**：Minimum approved risk scale across profiles covering selected indices.
- **依赖**：float、getattr、min、selected.intersection、set
- **复杂度 / 风险**：分支 3；跨度 13 行；high
- **测试 / 验证**：[tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py) · direct-dynamic

<a id="fun-a43ced947f"></a>

#### `format_authorized_position_size`

- **ID / 行**：`FUN-A43CED947F` / `L1057`（源码见本单元概览）
- **签名 / 返回**：`format_authorized_position_size(scale: float, action: str)` → `str`
- **职责**：Qualitative sizing labels — no account/notional model in this repo.
- **复杂度 / 风险**：分支 4；跨度 11 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-34dce71c07"></a>

#### `_normalize_signal_dict_take_profits`

- **ID / 行**：`FUN-34DCE71C07` / `L1070`（源码见本单元概览）
- **签名 / 返回**：`_normalize_signal_dict_take_profits(sig: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `_normalize_signal_dict_take_profits` and its owning unit.
- **依赖**：normalize_signal_take_profits、sig.get
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e8ad3336d7"></a>

#### `_review_field`

- **ID / 行**：`FUN-E8AD3336D7` / `L1086`（源码见本单元概览）
- **签名 / 返回**：`_review_field(review: object, name: str, default: object=None)` → `object`
- **职责**：As-built responsibility derived from `_review_field` and its owning unit.
- **依赖**：getattr、isinstance、review.get
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-be4a18b71c"></a>

#### `_format_risk_veto_lines`

- **ID / 行**：`FUN-BE4A18B71C` / `L1092`（源码见本单元概览）
- **签名 / 返回**：`_format_risk_veto_lines(risk_reviews: list | None, *, candidate_index: int | None)` → `list[str]`
- **职责**：One line per risk profile: pass/fail + full notes.
- **依赖**：_RISK_PROFILE_CN.get、_review_field、bool、float、join、lines.append、list、str、strip
- **复杂度 / 风险**：分支 7；跨度 32 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4c3a66bdae"></a>

#### `_format_trader_veto_lines`

- **ID / 行**：`FUN-4C3A66BDAE` / `L1126`（源码见本单元概览）
- **签名 / 返回**：`_format_trader_veto_lines(proposal: object | None, *, candidate_index: int | None)` → `list[str]`
- **职责**：As-built responsibility derived from `_format_trader_veto_lines` and its owning unit.
- **依赖**：getattr、isinstance、join、lines.append、list、proposal.get、str、strip
- **复杂度 / 风险**：分支 5；跨度 26 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-15ccc085e1"></a>

#### `_format_level_validation_lines`

- **ID / 行**：`FUN-15CCC085E1` / `L1154`（源码见本单元概览）
- **签名 / 返回**：`_format_level_validation_lines(validated_plans: list[dict[str, Any]] | None, sig: dict[str, Any])` → `list[str]`
- **职责**：Attach geometry-validator rejects when this candidate matches an LLM path.
- **依赖**：abs、bool、float、lines.append、prop.get、row.get、sig.get、str、strip、upper
- **复杂度 / 风险**：分支 7；跨度 26 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-3539753867"></a>

#### `build_signal_rejection_notes`

- **ID / 行**：`FUN-3539753867` / `L1182`（源码见本单元概览）
- **签名 / 返回**：`build_signal_rejection_notes(sig: dict[str, Any], *, decision_action: str, observation_mode: bool=False, primary_name: str | None=None, primary_sig: dict[str, Any] | None=None, decision_summary: str='', decision_confidence: float | None=None, risk_reviews: list | None=None, candidate_index: int | None=None, proposal: object | None=None, validated_plans: list[dict[str, Any]] | None=None)` → `list[str]`
- **职责**：Structured veto notes: manager / risk / trader / levels / score.
- **依赖**：_format_level_validation_lines、_format_risk_veto_lines、_format_trader_veto_lines、float、ordered.append、parts.append、parts.extend、primary_sig.get、seen.add、set、sig.get、str、strip、upper
- **复杂度 / 风险**：分支 18；跨度 80 行；medium
- **测试 / 验证**：[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py) · direct-dynamic

<a id="fun-3bf762bd92"></a>

#### `build_signal_rejection_reason`

- **ID / 行**：`FUN-3BF762BD92` / `L1264`（源码见本单元概览）
- **签名 / 返回**：`build_signal_rejection_reason(sig: dict[str, Any], *, decision_action: str, observation_mode: bool=False, primary_name: str | None=None, primary_sig: dict[str, Any] | None=None, decision_summary: str='', decision_confidence: float | None=None, risk_reviews: list | None=None, candidate_index: int | None=None, proposal: object | None=None, validated_plans: list[dict[str, Any]] | None=None)` → `str`
- **职责**：Human-readable why a candidate was not authorized for the delivered plan.
- **依赖**：build_signal_rejection_notes、join
- **复杂度 / 风险**：分支 1；跨度 29 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-442599ada0"></a>

#### `_signal_to_dict`

- **ID / 行**：`FUN-442599ADA0` / `L1295`（源码见本单元概览）
- **签名 / 返回**：`_signal_to_dict(signal: TradingSignal)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_signal_to_dict` and its owning unit.
- **依赖**：_normalize_signal_dict_take_profits、asdict、stable_signal_id
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9883fd47f5"></a>

#### `_assign_signal_ids`

- **ID / 行**：`FUN-9883FD47F5` / `L1302`（源码见本单元概览）
- **签名 / 返回**：`_assign_signal_ids(sig_dicts: list[dict[str, Any]])` → `None`
- **职责**：As-built responsibility derived from `_assign_signal_ids` and its owning unit.
- **依赖**：sig.get、stable_signal_id
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-435783f2d2"></a>

#### `_signal_execution_ready`

- **ID / 行**：`FUN-435783F2D2` / `L1307`（源码见本单元概览）
- **签名 / 返回**：`_signal_execution_ready(sig: dict[str, Any] | None)` → `bool`
- **职责**：Plan may be authorized; execution requires a confirmed trigger.
- **依赖**：bool、sig.get
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5d6d01887f"></a>

#### `apply_manager_authorization`

- **ID / 行**：`FUN-5D6D01887F` / `L1316`（源码见本单元概览）
- **签名 / 返回**：`apply_manager_authorization(report: dict, decision, risk_reviews: list, *, proposal: object | None=None)` → `None`
- **职责**：Map manager decision + risk scales onto report signals (single primary source).
- **依赖**：ManagerDecision、_assign_signal_ids、_attach_rejection、_clear_auth_meta、_normalize_signal_dict_take_profits、_signal_execution_ready、as_of.get、authorized_position_scale、bool、build_signal_rejection_notes、build_strategy_plans、claim_allows_execution_authorization、decision.to_dict、decision_dict.get、dict、enumerate、float、format_authorized_position_size、get、getattr
- **复杂度 / 风险**：分支 21；跨度 162 行；high
- **测试 / 验证**：[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) · direct-dynamic

<a id="fun-91b63c3cae"></a>

#### `apply_manager_authorization._attach_rejection`

- **ID / 行**：`FUN-91B63C3CAE` / `L1353`（源码见本单元概览）
- **签名 / 返回**：`apply_manager_authorization._attach_rejection(sig: dict[str, Any], *, idx: int, primary_name: str | None=None, primary_sig: dict | None=None)` → `None`
- **职责**：As-built responsibility derived from `_attach_rejection` and its owning unit.
- **依赖**：bool、build_signal_rejection_notes、getattr、join、meta.get、str
- **复杂度 / 风险**：分支 1；跨度 22 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-6d5b47fa9d"></a>

#### `apply_manager_authorization._clear_auth_meta`

- **ID / 行**：`FUN-6D5B47FA9D` / `L1376`（源码见本单元概览）
- **签名 / 返回**：`apply_manager_authorization._clear_auth_meta(*, plan_authorized: bool=False)` → `None`
- **职责**：As-built responsibility derived from `_clear_auth_meta` and its owning unit.
- **依赖**：decision.to_dict、dict、hasattr
- **复杂度 / 风险**：分支 1；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-358a1e0942"></a>

#### `_authorized_primary_signal`

- **ID / 行**：`FUN-358A1E0942` / `L1488`（源码见本单元概览）
- **签名 / 返回**：`_authorized_primary_signal(report: dict[str, Any])` → `dict[str, Any] | None`
- **职责**：As-built responsibility derived from `_authorized_primary_signal` and its owning unit.
- **依赖**：next、report.get、s.get
- **复杂度 / 风险**：分支 0；跨度 5 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-26766e75ae"></a>

#### `_format_entry_zone`

- **ID / 行**：`FUN-26766E75AE` / `L1495`（源码见本单元概览）
- **签名 / 返回**：`_format_entry_zone(signal: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_format_entry_zone` and its owning unit.
- **依赖**：float、signal.get
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f903e47206"></a>

#### `build_final_decision_meta`

- **ID / 行**：`FUN-F903E47206` / `L1502`（源码见本单元概览）
- **签名 / 返回**：`build_final_decision_meta(report: dict[str, Any])` → `dict[str, Any]`
- **职责**：Reader-facing verdict block stored on report.meta.final_decision.
- **依赖**：_MANAGER_ACTION_CN.get、_authorized_primary_signal、_format_entry_zone、bool、decision.get、get、lower、meta.get、primary.get、report.get、str、strip
- **复杂度 / 风险**：分支 5；跨度 47 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-db059d9e58"></a>

#### `align_conclusion_with_manager_decision`

- **ID / 行**：`FUN-DB059D9E58` / `L1551`（源码见本单元概览）
- **签名 / 返回**：`align_conclusion_with_manager_decision(report: dict[str, Any])` → `None`
- **职责**：Rewrite conclusion so prose matches manager authorization (wait vs execute).
- **依赖**：_MANAGER_ACTION_CN.get、_authorized_primary_signal、_format_entry_zone、bool、build_final_decision_meta、conclusion.get、decision.get、get、lower、meta.get、primary.get、report.setdefault、str、strip
- **复杂度 / 风险**：分支 14；跨度 75 行；medium
- **测试 / 验证**：[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py) · direct-dynamic

<a id="fun-cc7188b273"></a>

#### `build_path_summary`

- **ID / 行**：`FUN-CC7188B273` / `L1628`（源码见本单元概览）
- **签名 / 返回**：`build_path_summary(projections: list[dict])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `build_path_summary` and its owning unit.
- **依赖**：enumerate、join、out.append、p.get
- **复杂度 / 风险**：分支 1；跨度 14 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-65d3afa4f8"></a>

#### `build_report`

- **ID / 行**：`FUN-65D3AFA4F8` / `L1644`（源码见本单元概览）
- **签名 / 返回**：`build_report(data: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], *, signals: list[TradingSignal] | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_report` and its owning unit.
- **依赖**：_assign_signal_roles、_build_context_levels、_signal_to_dict、analyses.get、build_conclusion、build_key_levels、build_liquidity_entries、build_path_summary、build_price_action_summaries、build_resistance_support、build_rule_narrative_sections、build_strategy_plans、build_tf_summaries、daily_metrics、fibonacci_levels、generate_trading_signals、indicator_notes.append、indicator_snapshot、invalidation_rules、len
- **复杂度 / 风险**：分支 11；跨度 139 行；medium
- **测试 / 验证**：[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="unit-cd6da8c4a3"></a>

### src/analysis/report_facts.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CD6DA8C4A3 |
| 源码 | [src/analysis/report_facts.py](../../src/analysis/report_facts.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Report-level facts assembled from Lux analyses (no human copy). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py) |
| 验证状态 | selected |

#### 函数导航

[build_tf_summaries](#fun-7f2a7da4e4) · [_strong_weak_context_entries](#fun-6ed8e3091f) · [build_liquidity_entries](#fun-c657924e3f)

<a id="fun-7f2a7da4e4"></a>

#### `build_tf_summaries`

- **ID / 行**：`FUN-7F2A7DA4E4` / `L19`（源码见本单元概览）
- **签名 / 返回**：`build_tf_summaries(data: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], *, price: float)` → `dict[str, dict[str, Any]]`
- **职责**：Per-TF Lux snapshots for report schema + narrative_sections.
- **依赖**：build_tf_snapshot、ema_relation
- **复杂度 / 风险**：分支 2；跨度 16 行；medium
- **测试 / 验证**：[tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py) · direct-dynamic

<a id="fun-6ed8e3091f"></a>

#### `_strong_weak_context_entries`

- **ID / 行**：`FUN-6ED8E3091F` / `L37`（源码见本单元概览）
- **签名 / 返回**：`_strong_weak_context_entries(analysis: TimeframeAnalysis, *, price: float, swing_atr: float | None)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_strong_weak_context_entries` and its owning unit.
- **依赖**：build_tf_snapshot、entries.append、float、level_near_price、panel.get、round
- **复杂度 / 风险**：分支 3；跨度 29 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c657924e3f"></a>

#### `build_liquidity_entries`

- **ID / 行**：`FUN-C657924E3F` / `L68`（源码见本单元概览）
- **签名 / 返回**：`build_liquidity_entries(analyses: dict[str, TimeframeAnalysis], *, price: float, swing_tf: str, swing_atr: float | None)` → `list[dict[str, Any]]`
- **职责**：Swing H/L per TF; distant Strong/Weak H/L as context.
- **依赖**：_strong_weak_context_entries、abs、analyses.get、entries.append、entries.extend、entries.sort、float、liquidity_label、round、seen.add、set
- **复杂度 / 风险**：分支 7；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_report_facts.py](../../tests/unit/test_report_facts.py) · direct-dynamic

<a id="unit-1aecfa1072"></a>

### src/analysis/report_invariant_gate.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1AECFA1072 |
| 源码 | [src/analysis/report_invariant_gate.py](../../src/analysis/report_invariant_gate.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Apply deterministic remediations when report invariants fail (final gate). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 4 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py) |
| 验证状态 | selected |

#### 函数导航

[_revoke_execution](#fun-bf2c9119ea) · [_sanitize_llm_fields](#fun-b1bed5ecad) · [_sanitize_conclusion](#fun-0d8ba6c403) · [apply_report_invariant_gate](#fun-2e93cd50fc)

<a id="fun-bf2c9119ea"></a>

#### `_revoke_execution`

- **ID / 行**：`FUN-BF2C9119EA` / `L24`（源码见本单元概览）
- **签名 / 返回**：`_revoke_execution(report: dict[str, Any], remediations: list[str])` → `None`
- **职责**：As-built responsibility derived from `_revoke_execution` and its owning unit.
- **依赖**：remediations.append、report.get、report.setdefault
- **复杂度 / 风险**：分支 1；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b1bed5ecad"></a>

#### `_sanitize_llm_fields`

- **ID / 行**：`FUN-B1BED5ECAD` / `L42`（源码见本单元概览）
- **签名 / 返回**：`_sanitize_llm_fields(report: dict[str, Any], violations: list[dict[str, str]], remediations: list[str])` → `None`
- **职责**：As-built responsibility derived from `_sanitize_llm_fields` and its owning unit.
- **依赖**：_executable_wording_on_wait、code.startswith、llm.get、remediations.append、report.setdefault、row.get、str、strip
- **复杂度 / 风险**：分支 5；跨度 15 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0d8ba6c403"></a>

#### `_sanitize_conclusion`

- **ID / 行**：`FUN-0D8BA6C403` / `L59`（源码见本单元概览）
- **签名 / 返回**：`_sanitize_conclusion(report: dict[str, Any], remediations: list[str])` → `None`
- **职责**：As-built responsibility derived from `_sanitize_conclusion` and its owning unit.
- **依赖**：_executable_wording_on_wait、conclusion.get、conclusion.pop、get、remediations.append、report.get、report.setdefault、str
- **复杂度 / 风险**：分支 2；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2e93cd50fc"></a>

#### `apply_report_invariant_gate`

- **ID / 行**：`FUN-2E93CD50FC` / `L71`（源码见本单元概览）
- **签名 / 返回**：`apply_report_invariant_gate(report: dict[str, Any], invariants: dict[str, Any])` → `dict[str, Any]`
- **职责**：Enforce invariant failures: revoke auth, sanitize fields, mark run degraded.
- **依赖**：_revoke_execution、_sanitize_conclusion、_sanitize_llm_fields、align_conclusion_with_manager_decision、build_final_decision_meta、invariants.get、list、meta.setdefault、report.setdefault、sorted、str、v.get
- **复杂度 / 风险**：分支 2；跨度 34 行；high
- **测试 / 验证**：[tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py) · direct-dynamic

<a id="unit-70bd327d9d"></a>

### src/analysis/report_invariants.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-70BD327D9D |
| 源码 | [src/analysis/report_invariants.py](../../src/analysis/report_invariants.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Deterministic final-report consistency and invariant gate. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 13 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_plan_signal_targets.py](../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[_violation](#fun-c9004b2dc1) · [_manager_wait](#fun-39a8495c0f) · [_observation_mode](#fun-f9403871be) · [_normalize_direction](#fun-6461023713) · [_authorized_signals_for_geometry](#fun-574f6bf2c5) · [_check_signal_geometry](#fun-eb10a8bba7) · [_llm_top_level_active](#fun-202a49097f) · [_check_authorization_narrative](#fun-070be1843c) · [_check_manager_alignment](#fun-f9e30a657b) · [_check_fact_prices](#fun-5a7430694e) · [_check_freshness_language](#fun-26dad09727) · [_check_audit_metadata](#fun-cb762c7ebb) · [validate_report_invariants](#fun-8b2af809d8)

<a id="fun-c9004b2dc1"></a>

#### `_violation`

- **ID / 行**：`FUN-C9004B2DC1` / `L19`（源码见本单元概览）
- **签名 / 返回**：`_violation(code: str, field: str, message: str)` → `dict[str, str]`
- **职责**：As-built responsibility derived from `_violation` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-39a8495c0f"></a>

#### `_manager_wait`

- **ID / 行**：`FUN-39A8495C0F` / `L23`（源码见本单元概览）
- **签名 / 返回**：`_manager_wait(meta: dict[str, Any])` → `bool`
- **职责**：As-built responsibility derived from `_manager_wait` and its owning unit.
- **依赖**：decision.get、meta.get、str
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f9403871be"></a>

#### `_observation_mode`

- **ID / 行**：`FUN-F9403871BE` / `L31`（源码见本单元概览）
- **签名 / 返回**：`_observation_mode(meta: dict[str, Any])` → `bool`
- **职责**：As-built responsibility derived from `_observation_mode` and its owning unit.
- **依赖**：bool、meta.get
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6461023713"></a>

#### `_normalize_direction`

- **ID / 行**：`FUN-6461023713` / `L35`（源码见本单元概览）
- **签名 / 返回**：`_normalize_direction(raw: str)` → `str`
- **职责**：As-built responsibility derived from `_normalize_direction` and its owning unit.
- **依赖**：lower、str、upper
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-574f6bf2c5"></a>

#### `_authorized_signals_for_geometry`

- **ID / 行**：`FUN-574F6BF2C5` / `L44`（源码见本单元概览）
- **签名 / 返回**：`_authorized_signals_for_geometry(report: dict[str, Any])` → `list[dict[str, Any]]`
- **职责**：Only judge the plans the report actually presents / authorizes.
- **依赖**：list、meta.get、report.get、s.get、str
- **复杂度 / 风险**：分支 5；跨度 22 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-eb10a8bba7"></a>

#### `_check_signal_geometry`

- **ID / 行**：`FUN-EB10A8BBA7` / `L68`（源码见本单元概览）
- **签名 / 返回**：`_check_signal_geometry(report: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_check_signal_geometry` and its owning unit.
- **依赖**：LevelProposal、_authorized_signals_for_geometry、_geometry_error、_normalize_direction、_tp_ladder_error、_violation、enumerate、float、get、out.append、report.get、sig.get、str
- **复杂度 / 风险**：分支 5；跨度 28 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-202a49097f"></a>

#### `_llm_top_level_active`

- **ID / 行**：`FUN-202A49097F` / `L98`（源码见本单元概览）
- **签名 / 返回**：`_llm_top_level_active(llm: dict[str, Any])` → `bool`
- **职责**：True when LLM narrative layer is enabled or still carries top-level text to audit.
- **依赖**：any、bool、llm.get、str、strip
- **复杂度 / 风险**：分支 1；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-070be1843c"></a>

#### `_check_authorization_narrative`

- **ID / 行**：`FUN-070BE1843C` / `L108`（源码见本单元概览）
- **签名 / 返回**：`_check_authorization_narrative(report: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_check_authorization_narrative` and its owning unit.
- **依赖**：_executable_wording_on_wait、_llm_top_level_active、_manager_wait、_observation_mode、_violation、build_narrative_facts_for_llm、field_reasons.items、get、llm.get、out.append、report.get、str、strip、validate_llm_top_level_fields
- **复杂度 / 风险**：分支 6；跨度 21 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-f9e30a657b"></a>

#### `_check_manager_alignment`

- **ID / 行**：`FUN-F9E30A657B` / `L131`（源码见本单元概览）
- **签名 / 返回**：`_check_manager_alignment(report: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_check_manager_alignment` and its owning unit.
- **依赖**：_authorized_signals_for_geometry、_violation、conclusion.get、final.get、get、meta.get、out.append、report.get、sig.get、str、strip
- **复杂度 / 风险**：分支 6；跨度 34 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5a7430694e"></a>

#### `_check_fact_prices`

- **ID / 行**：`FUN-5A7430694E` / `L167`（源码见本单元概览）
- **签名 / 返回**：`_check_fact_prices(report: dict[str, Any], registry: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_check_fact_prices` and its owning unit.
- **依赖**：_violation、abs、allowed_prices、any、float、join、llm.get、narrative_price_tolerance、out.append、re.findall、report.get、str
- **复杂度 / 风险**：分支 5；跨度 26 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-26dad09727"></a>

#### `_check_freshness_language`

- **ID / 行**：`FUN-26DAD09727` / `L195`（源码见本单元概览）
- **签名 / 返回**：`_check_freshness_language(report: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_check_freshness_language` and its owning unit.
- **依赖**：_violation、any、as_of.get、blob.lower、join、llm.get、meta.get、out.append、report.get、str
- **复杂度 / 风险**：分支 2；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-cb762c7ebb"></a>

#### `_check_audit_metadata`

- **ID / 行**：`FUN-CB762C7EBB` / `L209`（源码见本单元概览）
- **签名 / 返回**：`_check_audit_metadata(report: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_check_audit_metadata` and its owning unit.
- **依赖**：_violation、get、meta.get、out.append、registry.get、report.get
- **复杂度 / 风险**：分支 2；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8b2af809d8"></a>

#### `validate_report_invariants`

- **ID / 行**：`FUN-8B2AF809D8` / `L227`（源码见本单元概览）
- **签名 / 返回**：`validate_report_invariants(report: dict[str, Any], *, registry: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：Run deterministic invariant checks; returns machine-readable violations.
- **依赖**：_check_audit_metadata、_check_authorization_narrative、_check_fact_prices、_check_freshness_language、_check_manager_alignment、_check_signal_geometry、build_fact_registry、len、violations.extend
- **复杂度 / 风险**：分支 0；跨度 19 行；high
- **测试 / 验证**：[tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_plan_signal_targets.py](../../tests/unit/test_plan_signal_targets.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) · direct-dynamic

<a id="unit-07e7315842"></a>

### src/analysis/report_reliability.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-07E7315842 |
| 源码 | [src/analysis/report_reliability.py](../../src/analysis/report_reliability.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Deterministic report quality score (heuristic — not calibrated win probability). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[_clamp](#fun-c44555ff7c) · [_normalize_source](#fun-276b3e529b) · [_collect_item_sources](#fun-ac8525df31) · [_data_quality](#fun-feb3154c03) · [_freshness_quality](#fun-a8d6008a74) · [_evidence_coverage](#fun-64e7649c32) · [_source_diversity](#fun-f6a742357c) · [_cross_timeframe_agreement](#fun-c83d50260f) · [_bull_bear_separation](#fun-fb32931ed7) · [_schema_quality](#fun-4e2b9ea344) · [compute_report_reliability](#fun-3daba6ffad)

<a id="fun-c44555ff7c"></a>

#### `_clamp`

- **ID / 行**：`FUN-C44555FF7C` / `L23`（源码见本单元概览）
- **签名 / 返回**：`_clamp(value: float)` → `float`
- **职责**：As-built responsibility derived from `_clamp` and its owning unit.
- **依赖**：max、min
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-276b3e529b"></a>

#### `_normalize_source`

- **ID / 行**：`FUN-276B3E529B` / `L27`（源码见本单元概览）
- **签名 / 返回**：`_normalize_source(raw: str)` → `str | None`
- **职责**：As-built responsibility derived from `_normalize_source` and its owning unit.
- **依赖**：lower、str、strip、text.split、text.startswith
- **复杂度 / 风险**：分支 4；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ac8525df31"></a>

#### `_collect_item_sources`

- **ID / 行**：`FUN-AC8525DF31` / `L37`（源码见本单元概览）
- **签名 / 返回**：`_collect_item_sources(item: dict[str, Any])` → `set[str]`
- **职责**：As-built responsibility derived from `_collect_item_sources` and its owning unit.
- **依赖**：_normalize_source、item.get、refs.get、set、sources.add、str
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-feb3154c03"></a>

#### `_data_quality`

- **ID / 行**：`FUN-FEB3154C03` / `L47`（源码见本单元概览）
- **签名 / 返回**：`_data_quality(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_data_quality` and its owning unit.
- **依赖**：as_of.get、get、report.get
- **复杂度 / 风险**：分支 5；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a8d6008a74"></a>

#### `_freshness_quality`

- **ID / 行**：`FUN-A8D6008A74` / `L63`（源码见本单元概览）
- **签名 / 返回**：`_freshness_quality(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_freshness_quality` and its owning unit.
- **依赖**：_data_quality、meta.get、report.get
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-64e7649c32"></a>

#### `_evidence_coverage`

- **ID / 行**：`FUN-64E7649C32` / `L70`（源码见本单元概览）
- **签名 / 返回**：`_evidence_coverage(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_evidence_coverage` and its owning unit.
- **依赖**：_clamp、debate.get、get、len、min、report.get、sum、team.get、trace.get
- **复杂度 / 风险**：分支 0；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f6a742357c"></a>

#### `_source_diversity`

- **ID / 行**：`FUN-F6A742357C` / `L82`（源码见本单元概览）
- **签名 / 返回**：`_source_diversity(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_source_diversity` and its owning unit.
- **依赖**：_clamp、_collect_item_sources、block.get、get、isinstance、len、report.get、set、sources.update、trace.get
- **复杂度 / 风险**：分支 5；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c83d50260f"></a>

#### `_cross_timeframe_agreement`

- **ID / 行**：`FUN-C83D50260F` / `L96`（源码见本单元概览）
- **签名 / 返回**：`_cross_timeframe_agreement(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_cross_timeframe_agreement` and its owning unit.
- **依赖**：_clamp、info.get、isinstance、len、max、report.get、str、sum、tfs.values
- **复杂度 / 风险**：分支 1；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fb32931ed7"></a>

#### `_bull_bear_separation`

- **ID / 行**：`FUN-FB32931ED7` / `L107`（源码见本单元概览）
- **签名 / 返回**：`_bull_bear_separation(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_bull_bear_separation` and its owning unit.
- **依赖**：_clamp、abs、debate.get、float、get、report.get、trace.get
- **复杂度 / 风险**：分支 0；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4e2b9ea344"></a>

#### `_schema_quality`

- **ID / 行**：`FUN-4E2B9EA344` / `L115`（源码见本单元概览）
- **签名 / 返回**：`_schema_quality(report: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_schema_quality` and its owning unit.
- **依赖**：_clamp、get、int、inv.get、report.get
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-3daba6ffad"></a>

#### `compute_report_reliability`

- **ID / 行**：`FUN-3DABA6FFAD` / `L125`（源码见本单元概览）
- **签名 / 返回**：`compute_report_reliability(report: dict[str, Any])` → `dict[str, Any]`
- **职责**：Heuristic report quality score; not calibrated against historical outcomes.
- **依赖**：_bull_bear_separation、_clamp、_cross_timeframe_agreement、_data_quality、_evidence_coverage、_freshness_quality、_schema_quality、_source_diversity、float、llm.get、report.get、round、sum
- **复杂度 / 风险**：分支 0；跨度 31 行；medium
- **测试 / 验证**：[tests/integration/test_offline_report_contract.py](../../tests/integration/test_offline_report_contract.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) · direct-dynamic

<a id="unit-0cc0e8d72a"></a>

### src/analysis/risk_gates.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0CC0E8D72A |
| 源码 | [src/analysis/risk_gates.py](../../src/analysis/risk_gates.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Deterministic risk gates before position scale is applied. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py)、[tests/unit/test_risk_gates_trigger.py](../../tests/unit/test_risk_gates_trigger.py) |
| 验证状态 | selected |

#### 函数导航

[_signal_dict](#fun-8340a338d8) · [_entry_mid](#fun-6ea0957492) · [_risk_reward](#fun-e7212ec1e1) · [signal_trigger_ready](#fun-03ea7fde9d) · [validate_signal_geometry](#fun-8e3c0f41d3) · [apply_risk_gates](#fun-df12984213)

<a id="fun-8340a338d8"></a>

#### `_signal_dict`

- **ID / 行**：`FUN-8340A338D8` / `L18`（源码见本单元概览）
- **签名 / 返回**：`_signal_dict(sig: Any)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_signal_dict` and its owning unit.
- **依赖**：asdict、is_dataclass、isinstance
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6ea0957492"></a>

#### `_entry_mid`

- **ID / 行**：`FUN-6EA0957492` / `L26`（源码见本单元概览）
- **签名 / 返回**：`_entry_mid(sig: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_entry_mid` and its owning unit.
- **依赖**：float、sig.get
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e7212ec1e1"></a>

#### `_risk_reward`

- **ID / 行**：`FUN-E7212EC1E1` / `L30`（源码见本单元概览）
- **签名 / 返回**：`_risk_reward(sig: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `_risk_reward` and its owning unit.
- **依赖**：_entry_mid、float、lower、min、sig.get、str、upper
- **复杂度 / 风险**：分支 3；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-03ea7fde9d"></a>

#### `signal_trigger_ready`

- **ID / 行**：`FUN-03EA7FDE9D` / `L50`（源码见本单元概览）
- **签名 / 返回**：`signal_trigger_ready(sig: Any)` → `bool`
- **职责**：True when the setup has confirmed its trigger (not merely a candidate zone).
- **依赖**：_signal_dict、bool、row.get
- **复杂度 / 风险**：分支 1；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_risk_gates_trigger.py](../../tests/unit/test_risk_gates_trigger.py) · direct-dynamic

<a id="fun-8e3c0f41d3"></a>

#### `validate_signal_geometry`

- **ID / 行**：`FUN-8E3C0F41D3` / `L58`（源码见本单元概览）
- **签名 / 返回**：`validate_signal_geometry(sig: Any, *, current_price: float)` → `list[str]`
- **职责**：Return blocking issues for one signal (empty = pass).
- **依赖**：_entry_mid、_risk_reward、_signal_dict、abs、float、lower、normalize_take_profits、row.get、str、upper
- **复杂度 / 风险**：分支 10；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py) · direct-dynamic

<a id="fun-df12984213"></a>

#### `apply_risk_gates`

- **ID / 行**：`FUN-DF12984213` / `L104`（源码见本单元概览）
- **签名 / 返回**：`apply_risk_gates(reviews: list, proposal, signals: list[Any], *, current_price: float, data_as_of: dict[str, Any] | None=None, observation_mode: bool=False)` → `list`
- **职责**：Filter risk reviews through deterministic gates; may veto approval/scale.
- **依赖**：RiskReview、as_of.get、awaiting_trigger.append、float、gated.append、global_block.append、isinstance、join、kept.append、len、list、log.warning、notes.append、notes.extend、seen.add、set、signal_trigger_ready、validate_signal_geometry
- **复杂度 / 风险**：分支 12；跨度 77 行；medium
- **测试 / 验证**：[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py)、[tests/unit/test_risk_gates_trigger.py](../../tests/unit/test_risk_gates_trigger.py) · direct-dynamic

<a id="unit-84723142fa"></a>

### src/analysis/signal_geometry.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-84723142FA |
| 源码 | [src/analysis/signal_geometry.py](../../src/analysis/signal_geometry.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Direction-aware signal geometry helpers. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 3 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_signal_geometry.py](../../tests/unit/test_signal_geometry.py) |
| 验证状态 | selected |

#### 函数导航

[_dedupe_preserve_order](#fun-35226fd4cc) · [normalize_take_profits](#fun-2abed7854b) · [normalize_signal_take_profits](#fun-f4b66c6737)

<a id="fun-35226fd4cc"></a>

#### `_dedupe_preserve_order`

- **ID / 行**：`FUN-35226FD4CC` / `L8`（源码见本单元概览）
- **签名 / 返回**：`_dedupe_preserve_order(levels: list[float])` → `list[float]`
- **职责**：As-built responsibility derived from `_dedupe_preserve_order` and its owning unit.
- **依赖**：out.append
- **复杂度 / 风险**：分支 2；跨度 6 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-2abed7854b"></a>

#### `normalize_take_profits`

- **ID / 行**：`FUN-2ABED7854B` / `L16`（源码见本单元概览）
- **签名 / 返回**：`normalize_take_profits(*, direction: str, entry_low: float, entry_high: float, take_profits: list[float], theme: str='')` → `list[float]`
- **职责**：Sort take-profit levels from nearest to farthest in trade direction.
- **依赖**：_dedupe_preserve_order、cleaned.append、float、lower、raw.strip、round、sorted
- **复杂度 / 风险**：分支 4；跨度 25 行；medium
- **测试 / 验证**：[tests/unit/test_signal_geometry.py](../../tests/unit/test_signal_geometry.py) · direct-dynamic

<a id="fun-f4b66c6737"></a>

#### `normalize_signal_take_profits`

- **ID / 行**：`FUN-F4B66C6737` / `L43`（源码见本单元概览）
- **签名 / 返回**：`normalize_signal_take_profits(signal: dict[str, Any])` → `list[float]`
- **职责**：Return direction-aware TP ladder for a report/signal dict.
- **依赖**：float、normalize_take_profits、signal.get、str
- **复杂度 / 风险**：分支 1；跨度 12 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-c8f58d21e1"></a>

### src/analysis/signal_identity.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C8F58D21E1 |
| 源码 | [src/analysis/signal_identity.py](../../src/analysis/signal_identity.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Stable signal identifiers derived from plan geometry. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_signal_identity.py](../../tests/unit/test_signal_identity.py) |
| 验证状态 | selected |

#### 函数导航

[stable_signal_id](#fun-515303b30d)

<a id="fun-515303b30d"></a>

#### `stable_signal_id`

- **ID / 行**：`FUN-515303B30D` / `L10`（源码见本单元概览）
- **签名 / 返回**：`stable_signal_id(signal: dict[str, Any])` → `str`
- **职责**：Content-addressed ID — stable across reordering of candidate lists.
- **依赖**：float、hashlib.sha256、hexdigest、json.dumps、raw.encode、round、signal.get、str、upper
- **复杂度 / 风险**：分支 0；跨度 16 行；medium
- **测试 / 验证**：[tests/unit/test_signal_identity.py](../../tests/unit/test_signal_identity.py) · direct-dynamic

<a id="unit-7faaa8edca"></a>

### src/analysis/technical_context.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7FAAA8EDCA |
| 源码 | [src/analysis/technical_context.py](../../src/analysis/technical_context.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Shared technical facts for rule analysts, LLM payloads, and narrative. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 17 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py) |
| 验证状态 | selected |

#### 函数导航

[distance_pct](#fun-86bf8dedc0) · [primary_analysis](#fun-a9814ca00a) · [fibonacci_context](#fun-e2f42619c2) · [support_resistance_context](#fun-e5355cc1ae) · [support_resistance_context.add_level](#fun-67805426ec) · [support_resistance_context.add_zone](#fun-ab952e6029) · [indicator_snapshot](#fun-41bb47141e) · [structure_narrative](#fun-ab37ca5fb2) · [timeframe_context](#fun-8894db4de1) · [technical_quality](#fun-8313bc01b7) · [build_technical_context](#fun-9091131d8f) · [_ready_indicators](#fun-303ba8669b) · [_nonzero_volume_ratio](#fun-42e28caea1) · [_rank_ict_events](#fun-be25278d2d) · [_level_kind](#fun-4a23106463) · [_zone_kind](#fun-41c768d621) · [_dedupe_levels](#fun-c48fb80201)

<a id="fun-86bf8dedc0"></a>

#### `distance_pct`

- **ID / 行**：`FUN-86BF8DEDC0` / `L27`（源码见本单元概览）
- **签名 / 返回**：`distance_pct(price: float, level: float)` → `float`
- **职责**：As-built responsibility derived from `distance_pct` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a9814ca00a"></a>

#### `primary_analysis`

- **ID / 行**：`FUN-A9814CA00A` / `L33`（源码见本单元概览）
- **签名 / 返回**：`primary_analysis(ctx: MarketContext)` → `TimeframeAnalysis | None`
- **职责**：As-built responsibility derived from `primary_analysis` and its owning unit.
- **依赖**：ctx.analyses.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e2f42619c2"></a>

#### `fibonacci_context`

- **ID / 行**：`FUN-E2F42619C2` / `L37`（源码见本单元概览）
- **签名 / 返回**：`fibonacci_context(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：Use the same primary swing selection across rule and LLM paths.
- **依赖**：abs、ctx.metrics.get、distance_pct、fibonacci_levels、float、primary_analysis、round、sorted
- **复杂度 / 风险**：分支 2；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e5355cc1ae"></a>

#### `support_resistance_context`

- **ID / 行**：`FUN-E5355CC1AE` / `L62`（源码见本单元概览）
- **签名 / 返回**：`support_resistance_context(ctx: MarketContext, *, limit: int=12)` → `dict[str, Any]`
- **职责**：Compose auditable S/R levels from price action, ICT zones, and report metrics.
- **依赖**：TF_WEIGHT.items、_dedupe_levels、_level_kind、_zone_kind、abs、add_level、add_zone、ctx.analyses.get、distance_pct、fib.get、fibonacci_context、float、getattr、levels.append、liquidity_label、max、metrics.get、primary_analysis、round、row.get
- **复杂度 / 风险**：分支 14；跨度 127 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-67805426ec"></a>

#### `support_resistance_context.add_level`

- **ID / 行**：`FUN-67805426EC` / `L66`（源码见本单元概览）
- **签名 / 返回**：`support_resistance_context.add_level(*, price: float | None, kind: str | None, label: str, source: str, timeframe: str | None=None, strength: float=0.4)` → `None`
- **职责**：As-built responsibility derived from `add_level` and its owning unit.
- **依赖**：_level_kind、distance_pct、float、levels.append、round
- **复杂度 / 风险**：分支 1；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ab952e6029"></a>

#### `support_resistance_context.add_zone`

- **ID / 行**：`FUN-AB952E6029` / `L90`（源码见本单元概览）
- **签名 / 返回**：`support_resistance_context.add_zone(*, low: float, high: float, preferred_kind: str, label: str, source: str, timeframe: str | None, strength: float)` → `None`
- **职责**：As-built responsibility derived from `add_zone` and its owning unit.
- **依赖**：_zone_kind、distance_pct、float、levels.append、round
- **复杂度 / 风险**：分支 0；跨度 25 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-41bb47141e"></a>

#### `indicator_snapshot`

- **ID / 行**：`FUN-41BB47141E` / `L191`（源码见本单元概览）
- **签名 / 返回**：`indicator_snapshot(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `indicator_snapshot` and its owning unit.
- **依赖**：_nonzero_volume_ratio、_ready_indicators、ctx.enriched.get、ema_relation、indicator_values、len、round
- **复杂度 / 风险**：分支 2；跨度 16 行；medium
- **测试 / 验证**：[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py) · direct-dynamic

<a id="fun-ab37ca5fb2"></a>

#### `structure_narrative`

- **ID / 行**：`FUN-AB37CA5FB2` / `L209`（源码见本单元概览）
- **签名 / 返回**：`structure_narrative(analysis: TimeframeAnalysis, *, max_events: int=2)` → `str`
- **职责**：Human-readable structure summary aligned with Lux internal/swing labels.
- **依赖**：_latest_structure_labels、join、list、parts.append、pd_map.get、reversed、trend_map.get
- **复杂度 / 风险**：分支 9；跨度 34 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-8894db4de1"></a>

#### `timeframe_context`

- **ID / 行**：`FUN-8894DB4DE1` / `L245`（源码见本单元概览）
- **签名 / 返回**：`timeframe_context(tf: str, analysis: TimeframeAnalysis, *, price: float, event_limit: int=8, ob_limit: int=5, fvg_limit: int=5, liquidity_limit: int=6)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `timeframe_context` and its owning unit.
- **依赖**：_rank_ict_events、build_tf_snapshot、distance_pct、liquidity_label、round、structure_narrative
- **复杂度 / 风险**：分支 2；跨度 55 行；medium
- **测试 / 验证**：[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py) · direct-dynamic

<a id="fun-8313bc01b7"></a>

#### `technical_quality`

- **ID / 行**：`FUN-8313BC01B7` / `L302`（源码见本单元概览）
- **签名 / 返回**：`technical_quality(ctx: MarketContext, indicators: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `technical_quality` and its owning unit.
- **依赖**：ctx.analyses.values、ctx.enriched.get、float、get、indicator_snapshot、indicators.get、len、min、ready.intersection、round、scores.append、set、sr.get、sum、support_resistance_context、warnings.append
- **复杂度 / 风险**：分支 7；跨度 47 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9091131d8f"></a>

#### `build_technical_context`

- **ID / 行**：`FUN-9091131D8F` / `L351`（源码见本单元概览）
- **签名 / 返回**：`build_technical_context(ctx: MarketContext, *, event_limit: int=8)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_technical_context` and its owning unit.
- **依赖**：build_price_action_summaries、build_tf_snapshot、ctx.context_stats.get、ctx.derived.get、fibonacci_context、indicator_snapshot、sentiment_score、support_resistance_context、technical_quality、timeframe_context
- **复杂度 / 风险**：分支 0；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py) · direct-dynamic

<a id="fun-303ba8669b"></a>

#### `_ready_indicators`

- **ID / 行**：`FUN-303BA8669B` / `L381`（源码见本单元概览）
- **签名 / 返回**：`_ready_indicators(row: pd.Series)` → `list[str]`
- **职责**：As-built responsibility derived from `_ready_indicators` and its owning unit.
- **依赖**：pd.notna
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-42e28caea1"></a>

#### `_nonzero_volume_ratio`

- **ID / 行**：`FUN-42E28CAEA1` / `L385`（源码见本单元概览）
- **签名 / 返回**：`_nonzero_volume_ratio(df: pd.DataFrame)` → `float`
- **职责**：As-built responsibility derived from `_nonzero_volume_ratio` and its owning unit.
- **依赖**：astype、float、len、sum
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-be25278d2d"></a>

#### `_rank_ict_events`

- **ID / 行**：`FUN-BE25278D2D` / `L392`（源码见本单元概览）
- **签名 / 返回**：`_rank_ict_events(analysis: TimeframeAnalysis, *, limit: int)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_rank_ict_events` and its owning unit.
- **依赖**：lower、priority.get、sorted、str
- **复杂度 / 风险**：分支 0；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4a23106463"></a>

#### `_level_kind`

- **ID / 行**：`FUN-4A23106463` / `L410`（源码见本单元概览）
- **签名 / 返回**：`_level_kind(price: float, level: float)` → `str`
- **职责**：As-built responsibility derived from `_level_kind` and its owning unit.
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-41c768d621"></a>

#### `_zone_kind`

- **ID / 行**：`FUN-41C768D621` / `L418`（源码见本单元概览）
- **签名 / 返回**：`_zone_kind(price: float, low: float, high: float, preferred: str)` → `str`
- **职责**：As-built responsibility derived from `_zone_kind` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c48fb80201"></a>

#### `_dedupe_levels`

- **ID / 行**：`FUN-C48FB80201` / `L428`（源码见本单元概览）
- **签名 / 返回**：`_dedupe_levels(levels: list[dict[str, Any]])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_dedupe_levels` and its owning unit.
- **依赖**：best.get、best.values、float、list、round、str
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-ebf42549f9"></a>

### src/analysis/tf_snapshot.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EBF42549F9 |
| 源码 | [src/analysis/tf_snapshot.py](../../src/analysis/tf_snapshot.py) |
| 架构组件 | ARC-ANALYSIS — 事实、结构、信号与报告门禁 |
| 职责 | Per-timeframe Lux structure snapshot — single fact primitive for report/LLM/UI. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-DATA-002](./SWE.1-software-requirements.md#swr-data-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-ANA-001](./SWE.1-software-requirements.md#swr-ana-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_tf_snapshot.py](../../tests/unit/test_tf_snapshot.py) |
| 验证状态 | selected |

#### 函数导航

[_newest_events](#fun-7354a02bce) · [_serialize_event](#fun-a7616824f7) · [_strong_weak_high_low](#fun-6dedb23061) · [build_tf_snapshot](#fun-c91f12310a)

<a id="fun-7354a02bce"></a>

#### `_newest_events`

- **ID / 行**：`FUN-7354A02BCE` / `L12`（源码见本单元概览）
- **签名 / 返回**：`_newest_events(events: list[StructureEvent], *, kind: str, limit: int=SNAPSHOT_LIMIT)` → `list[StructureEvent]`
- **职责**：As-built responsibility derived from `_newest_events` and its owning unit.
- **依赖**：matched.sort
- **复杂度 / 风险**：分支 0；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a7616824f7"></a>

#### `_serialize_event`

- **ID / 行**：`FUN-A7616824F7` / `L23`（源码见本单元概览）
- **签名 / 返回**：`_serialize_event(event: StructureEvent)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_serialize_event` and its owning unit.
- **依赖**：float、round
- **复杂度 / 风险**：分支 2；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6dedb23061"></a>

#### `_strong_weak_high_low`

- **ID / 行**：`FUN-6DEDB23061` / `L35`（源码见本单元概览）
- **签名 / 返回**：`_strong_weak_high_low(trend: str, swing_high: float | None, swing_low: float | None)` → `dict[str, float | None]`
- **职责**：As-built responsibility derived from `_strong_weak_high_low` and its owning unit.
- **复杂度 / 风险**：分支 2；跨度 25 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c91f12310a"></a>

#### `build_tf_snapshot`

- **ID / 行**：`FUN-C91F12310A` / `L62`（源码见本单元概览）
- **签名 / 返回**：`build_tf_snapshot(analysis: TimeframeAnalysis)` → `dict[str, Any]`
- **职责**：Canonical per-TF facts from full-bar Lux detection (no chart visibility filter).
- **依赖**：_newest_events、_serialize_event、_strong_weak_high_low
- **复杂度 / 风险**：分支 0；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_tf_snapshot.py](../../tests/unit/test_tf_snapshot.py) · direct-dynamic

<a id="arc-agents"></a>

## ARC-AGENTS — 规则/LLM Agent 编排

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/agents/__init__.py](#unit-818fcec908) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/__init__.py](#unit-b6c46ef660) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/base.py](#unit-8110cb5da5) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/evidence_ids.py](#unit-87b2f0bba3) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/evidence_provenance.py](#unit-5e6c877f3b) | 11 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/fundamentals.py](#unit-52003276aa) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/news.py](#unit-3628b84ddf) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/news_bias.py](#unit-b6597d0c34) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/sentiment.py](#unit-8f2897b88a) | 4 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/structure_zones.py](#unit-3363ad337f) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/analysts/technical.py](#unit-8d8fc5eaa1) | 9 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/bearish.py](#unit-8933374b3e) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/bullish.py](#unit-6008a95748) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/debate.py](#unit-34bf03f815) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/factory.py](#unit-f23db48d75) | 20 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/__init__.py](#unit-1606bdc6e2) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/base.py](#unit-3eeb009803) | 5 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/payload.py](#unit-3a49bda3a6) | 25 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/schemas.py](#unit-9b539edeb6) | 18 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/__init__.py](#unit-7226a2379a) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/__init__.py](#unit-1df6497ce4) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/_common.py](#unit-73b0811649) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/fundamentals.py](#unit-fcd3d48fde) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/news.py](#unit-25115c1d6f) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/sentiment.py](#unit-2bf1b61e7e) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/analysts/technical.py](#unit-a3445b9493) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/bearish.py](#unit-2ccd7c4dcb) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/bullish.py](#unit-12bf07eb04) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/debate.py](#unit-3970799e39) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/levels.py](#unit-4fbc2b73a8) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/manager.py](#unit-5ed826be60) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/risk.py](#unit-9038f74287) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/llm/stages/trader.py](#unit-a996419c04) | 2 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/manager.py](#unit-cc665640c2) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/risk.py](#unit-c1468c2396) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/agents/trader.py](#unit-6340c2c541) | 1 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-818fcec908"></a>

### src/agents/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-818FCEC908 |
| 源码 | [src/agents/__init__.py](../../src/agents/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 继承 规则/LLM Agent 编排 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-b6c46ef660"></a>

### src/agents/analysts/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B6C46EF660 |
| 源码 | [src/agents/analysts/__init__.py](../../src/agents/analysts/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | TradingAgents-style Analyst Team — four specialists before bull/bear research. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_analyst_team](#fun-00321f2b4a)

<a id="fun-00321f2b4a"></a>

#### `run_analyst_team`

- **ID / 行**：`FUN-00321F2B4A` / `L20`（源码见本单元概览）
- **签名 / 返回**：`run_analyst_team(ctx: MarketContext)` → `AnalystTeam`
- **职责**：As-built responsibility derived from `run_analyst_team` and its owning unit.
- **依赖**：AnalystTeam、run_fundamentals_analyst、run_news_analyst、run_sentiment_analyst、run_technical_analyst
- **复杂度 / 风险**：分支 0；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="unit-8110cb5da5"></a>

### src/agents/analysts/base.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8110CB5DA5 |
| 源码 | [src/agents/analysts/base.py](../../src/agents/analysts/base.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Shared helpers for the Analyst Team. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) |
| 验证状态 | selected |

#### 函数导航

[confidence_from_items](#fun-c3439bfbe3) · [build_report](#fun-cc65b2503a) · [items_for_direction](#fun-7ef67bfe39)

<a id="fun-c3439bfbe3"></a>

#### `confidence_from_items`

- **ID / 行**：`FUN-C3439BFBE3` / `L11`（源码见本单元概览）
- **签名 / 返回**：`confidence_from_items(items: list[EvidenceItem])` → `float`
- **职责**：As-built responsibility derived from `confidence_from_items` and its owning unit.
- **依赖**：len、min、sum
- **复杂度 / 风险**：分支 1；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-cc65b2503a"></a>

#### `build_report`

- **ID / 行**：`FUN-CC65B2503A` / `L17`（源码见本单元概览）
- **签名 / 返回**：`build_report(*, agent: str, items: list[EvidenceItem], bias: Bias, summary: str | None=None)` → `AnalystReport`
- **职责**：As-built responsibility derived from `build_report` and its owning unit.
- **依赖**：AnalystReport、assign_evidence_ids、confidence_from_items、len
- **复杂度 / 风险**：分支 2；跨度 20 行；medium
- **测试 / 验证**：[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="fun-7ef67bfe39"></a>

#### `items_for_direction`

- **ID / 行**：`FUN-7EF67BFE39` / `L39`（源码见本单元概览）
- **签名 / 返回**：`items_for_direction(team_reports: list[AnalystReport], direction: Bias)` → `list[EvidenceItem]`
- **职责**：Pull evidence from specialist reports aligned with a researcher direction.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：EvidenceItem、max、merged.append、merged.sort、min、report.agent.replace
- **复杂度 / 风险**：分支 3；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) · direct-dynamic

<a id="unit-87b2f0bba3"></a>

### src/agents/analysts/evidence_ids.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-87B2F0BBA3 |
| 源码 | [src/agents/analysts/evidence_ids.py](../../src/agents/analysts/evidence_ids.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Stable evidence identifiers for analyst → research → debate provenance. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[assign_evidence_ids](#fun-736ecac34c)

<a id="fun-736ecac34c"></a>

#### `assign_evidence_ids`

- **ID / 行**：`FUN-736ECAC34C` / `L8`（源码见本单元概览）
- **签名 / 返回**：`assign_evidence_ids(agent: str, items: list[EvidenceItem])` → `list[EvidenceItem]`
- **职责**：Ensure every item has a stable ``{agent}:{index}`` id.
- **依赖**：EvidenceItem、dict、enumerate、out.append、strip
- **复杂度 / 风险**：分支 1；跨度 16 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-5e6c877f3b"></a>

### src/agents/analysts/evidence_provenance.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5E6C877F3B |
| 源码 | [src/agents/analysts/evidence_provenance.py](../../src/agents/analysts/evidence_provenance.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Validate, dedupe and score evidence IDs across analyst → research → debate. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) |
| 验证状态 | selected |

#### 函数导航

[analyst_evidence_ids](#fun-89a55043e0) · [evidence_registry](#fun-c2ce034d09) · [is_new_structure_id](#fun-bc6ab45103) · [_allowed_id](#fun-5138cc692a) · [dedupe_evidence_items](#fun-aea352184d) · [_restore_refs](#fun-dfee2688c2) · [parse_research_items](#fun-43d1351553) · [build_research_provenance_meta](#fun-87a0b32a1c) · [blend_research_confidence](#fun-94884173fc) · [build_debate_provenance_meta](#fun-d72e36ce1e) · [blend_debate_consensus](#fun-1e35c05ea3)

<a id="fun-89a55043e0"></a>

#### `analyst_evidence_ids`

- **ID / 行**：`FUN-89A55043E0` / `L10`（源码见本单元概览）
- **签名 / 返回**：`analyst_evidence_ids(team: AnalystTeam)` → `set[str]`
- **职责**：As-built responsibility derived from `analyst_evidence_ids` and its owning unit.
- **依赖**：getattr、ids.add、set、strip
- **复杂度 / 风险**：分支 3；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c2ce034d09"></a>

#### `evidence_registry`

- **ID / 行**：`FUN-C2CE034D09` / `L20`（源码见本单元概览）
- **签名 / 返回**：`evidence_registry(team: AnalystTeam)` → `dict[str, EvidenceItem]`
- **职责**：As-built responsibility derived from `evidence_registry` and its owning unit.
- **依赖**：getattr、strip
- **复杂度 / 风险**：分支 3；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) · direct-dynamic

<a id="fun-bc6ab45103"></a>

#### `is_new_structure_id`

- **ID / 行**：`FUN-BC6AB45103` / `L30`（源码见本单元概览）
- **签名 / 返回**：`is_new_structure_id(evidence_id: str, agent: str)` → `bool`
- **职责**：Deprecated: Research must not mint structure IDs; kept for tests/docs.
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5138cc692a"></a>

#### `_allowed_id`

- **ID / 行**：`FUN-5138CC692A` / `L35`（源码见本单元概览）
- **签名 / 返回**：`_allowed_id(evidence_id: str, *, agent: str, allowed_ids: set[str])` → `bool`
- **职责**：As-built responsibility derived from `_allowed_id` and its owning unit.
- **依赖**：evidence_id.strip
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-aea352184d"></a>

#### `dedupe_evidence_items`

- **ID / 行**：`FUN-AEA352184D` / `L42`（源码见本单元概览）
- **签名 / 返回**：`dedupe_evidence_items(items: list[EvidenceItem])` → `tuple[list[EvidenceItem], int]`
- **职责**：Keep strongest item per evidence_id.
- **依赖**：best.get、best.values、len、max、sorted、strip
- **复杂度 / 风险**：分支 3；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) · direct-dynamic

<a id="fun-dfee2688c2"></a>

#### `_restore_refs`

- **ID / 行**：`FUN-DFEE2688C2` / `L57`（源码见本单元概览）
- **签名 / 返回**：`_restore_refs(item: EvidenceItem, registry: dict[str, EvidenceItem])` → `EvidenceItem`
- **职责**：As-built responsibility derived from `_restore_refs` and its owning unit.
- **依赖**：EvidenceItem、dict、item.refs.items、merged_refs.get、merged_refs.setdefault、merged_refs.update、registry.get、strip、upstream.refs.get
- **复杂度 / 风险**：分支 2；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-43d1351553"></a>

#### `parse_research_items`

- **ID / 行**：`FUN-43D1351553` / `L77`（源码见本单元概览）
- **签名 / 返回**：`parse_research_items(rows: list[dict[str, Any]], *, agent: str, direction: Bias, allowed_ids: set[str], registry: dict[str, EvidenceItem], item_refs_fn)` → `tuple[list[EvidenceItem], int]`
- **职责**：Parse LLM research items with ID whitelist, ref restore and dedupe.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：EvidenceItem、ValueError、_allowed_id、_restore_refs、dedupe_evidence_items、enumerate、float、isinstance、item_refs_fn、max、min、parsed.append、row.get、str、strip
- **复杂度 / 风险**：分支 7；跨度 46 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-87a0b32a1c"></a>

#### `build_research_provenance_meta`

- **ID / 行**：`FUN-87A0B32A1C` / `L125`（源码见本单元概览）
- **签名 / 返回**：`build_research_provenance_meta(items: list[EvidenceItem], *, allowed_ids: set[str], model_confidence: float, dedupe_dropped: int=0)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_research_provenance_meta` and its owning unit.
- **依赖**：i.refs.get、len、max、min、round、str、sum
- **复杂度 / 风险**：分支 1；跨度 32 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-94884173fc"></a>

#### `blend_research_confidence`

- **ID / 行**：`FUN-94884173FC` / `L159`（源码见本单元概览）
- **签名 / 返回**：`blend_research_confidence(model_confidence: float, meta: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `blend_research_confidence` and its owning unit.
- **依赖**：float、max、meta.get、min
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d72e36ce1e"></a>

#### `build_debate_provenance_meta`

- **ID / 行**：`FUN-D72E36CE1E` / `L164`（源码见本单元概览）
- **签名 / 返回**：`build_debate_provenance_meta(bullish: list[EvidenceItem], bearish: list[EvidenceItem], *, model_consensus_strength: float)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_debate_provenance_meta` and its owning unit.
- **依赖**：len、max、min、round、sorted
- **复杂度 / 风险**：分支 0；跨度 24 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-1e35c05ea3"></a>

#### `blend_debate_consensus`

- **ID / 行**：`FUN-1E35C05EA3` / `L190`（源码见本单元概览）
- **签名 / 返回**：`blend_debate_consensus(model_strength: float, meta: dict[str, Any])` → `float`
- **职责**：As-built responsibility derived from `blend_debate_consensus` and its owning unit.
- **依赖**：float、max、meta.get、min
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-52003276aa"></a>

### src/agents/analysts/fundamentals.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-52003276AA |
| 源码 | [src/agents/analysts/fundamentals.py](../../src/agents/analysts/fundamentals.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Fundamentals Analyst — DXY / US10Y macro drivers for gold. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_bias_from_quotes](#fun-39f851dead) · [_macro_context_evidence](#fun-d0b578d7f2) · [run_fundamentals_analyst](#fun-2dc8e34e80)

<a id="fun-39f851dead"></a>

#### `_bias_from_quotes`

- **ID / 行**：`FUN-39F851DEAD` / `L11`（源码见本单元概览）
- **签名 / 返回**：`_bias_from_quotes(ctx: MarketContext)` → `Bias`
- **职责**：As-built responsibility derived from `_bias_from_quotes` and its owning unit.
- **依赖**：any、votes.get
- **复杂度 / 风险**：分支 5；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d0b578d7f2"></a>

#### `_macro_context_evidence`

- **ID / 行**：`FUN-D0B578D7F2` / `L27`（源码见本单元概览）
- **签名 / 返回**：`_macro_context_evidence(ctx: MarketContext)` → `list[EvidenceItem]`
- **职责**：Turn macro input quality and event timing into auditable evidence.
- **依赖**：EvidenceItem、countdown.get、ctx.derived.get、err.lower、ev.display、items.append、join、len、min、strip
- **复杂度 / 风险**：分支 6；跨度 64 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2dc8e34e80"></a>

#### `run_fundamentals_analyst`

- **ID / 行**：`FUN-2DC8E34E80` / `L93`（源码见本单元概览）
- **签名 / 返回**：`run_fundamentals_analyst(ctx: MarketContext)` → `AnalystReport`
- **职责**：As-built responsibility derived from `run_fundamentals_analyst` and its owning unit.
- **依赖**：_bias_from_quotes、_macro_context_evidence、any、build_report、ctx.context_stats.get、external_macro_evidence、get、i.refs.get、join
- **复杂度 / 风险**：分支 1；跨度 15 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="unit-3628b84ddf"></a>

### src/agents/analysts/news.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3628B84DDF |
| 源码 | [src/agents/analysts/news.py](../../src/agents/analysts/news.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | News Analyst — macro headlines and event risk. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_news_context_evidence](#fun-215c3fb37a) · [run_news_analyst](#fun-b07796dbd7)

<a id="fun-215c3fb37a"></a>

#### `_news_context_evidence`

- **ID / 行**：`FUN-215C3FB37A` / `L12`（源码见本单元概览）
- **签名 / 返回**：`_news_context_evidence(ctx: MarketContext, *, is_live: bool)` → `list[EvidenceItem]`
- **职责**：Add channel/topic/source quality evidence alongside raw headlines.
- **依赖**：EvidenceItem、ctx.derived.get、err.lower、int、items.append、join、len、min、str、sum、topic.get
- **复杂度 / 风险**：分支 7；跨度 63 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-b07796dbd7"></a>

#### `run_news_analyst`

- **ID / 行**：`FUN-B07796DBD7` / `L77`（源码见本单元概览）
- **签名 / 返回**：`run_news_analyst(ctx: MarketContext)` → `AnalystReport`
- **职责**：As-built responsibility derived from `run_news_analyst` and its owning unit.
- **依赖**：_news_context_evidence、any、build_report、external_to_evidence、infer_news_bias、len、sum
- **复杂度 / 风险**：分支 2；跨度 22 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="unit-b6597d0c34"></a>

### src/agents/analysts/news_bias.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B6597D0C34 |
| 源码 | [src/agents/analysts/news_bias.py](../../src/agents/analysts/news_bias.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | News / event bias inference from headlines and calendar. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[infer_news_bias](#fun-8413383608)

<a id="fun-8413383608"></a>

#### `infer_news_bias`

- **ID / 行**：`FUN-8413383608` / `L37`（源码见本单元概览）
- **签名 / 返回**：`infer_news_bias(headlines: list[HeadlineItem], calendar: list[CalendarEvent], *, risk_text: str='')` → `Bias`
- **职责**：As-built responsibility derived from `infer_news_bias` and its owning unit.
- **依赖**：join、k.lower、lower、sum
- **复杂度 / 风险**：分支 4；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-8f2897b88a"></a>

### src/agents/analysts/sentiment.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8F2897B88A |
| 源码 | [src/agents/analysts/sentiment.py](../../src/agents/analysts/sentiment.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Sentiment Analyst — structure vote + TradingView community mood. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_social_note](#fun-853c57015e) · [_social_bias_delta](#fun-e569d3f536) · [_sentiment_context_evidence](#fun-00db5653b2) · [run_sentiment_analyst](#fun-8e5ddab513)

<a id="fun-853c57015e"></a>

#### `_social_note`

- **ID / 行**：`FUN-853C57015E` / `L12`（源码见本单元概览）
- **签名 / 返回**：`_social_note(ext, post_count: int)` → `str`
- **职责**：As-built responsibility derived from `_social_note` and its owning unit.
- **依赖**：len、strip
- **复杂度 / 风险**：分支 4；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e569d3f536"></a>

#### `_social_bias_delta`

- **ID / 行**：`FUN-E569D3F536` / `L23`（源码见本单元概览）
- **签名 / 返回**：`_social_bias_delta(posts: list[dict])` → `float`
- **职责**：As-built responsibility derived from `_social_bias_delta` and its owning unit.
- **依赖**：float、post.get
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-00db5653b2"></a>

#### `_sentiment_context_evidence`

- **ID / 行**：`FUN-00DB5653B2` / `L33`（源码见本单元概览）
- **签名 / 返回**：`_sentiment_context_evidence(ctx: MarketContext, vote: dict[str, float])` → `list[EvidenceItem]`
- **职责**：Capture sample quality and structure/social disagreement for auditability.
- **依赖**：EvidenceItem、_social_bias_delta、abs、ctx.analyses.items、err.lower、int、items.append、join、kind_counts.get、len、max、min、post.get、round、set、sorted、str、trends.items、trends.values
- **复杂度 / 风险**：分支 9；跨度 68 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8e5ddab513"></a>

#### `run_sentiment_analyst`

- **ID / 行**：`FUN-8E5DDAB513` / `L103`（源码见本单元概览）
- **签名 / 返回**：`run_sentiment_analyst(ctx: MarketContext)` → `AnalystReport`
- **职责**：As-built responsibility derived from `run_sentiment_analyst` and its owning unit.
- **依赖**：EvidenceItem、_sentiment_context_evidence、_social_bias_delta、_social_note、abs、any、build_report、items.append、items.extend、len、max、min、post.get、sentiment_score、str
- **复杂度 / 风险**：分支 9；跨度 57 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="unit-3363ad337f"></a>

### src/agents/analysts/structure_zones.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3363AD337F |
| 源码 | [src/agents/analysts/structure_zones.py](../../src/agents/analysts/structure_zones.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | ICT structure zone distance helpers for technical analyst. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[ict_zone_evidence](#fun-6eec9deabd)

<a id="fun-6eec9deabd"></a>

#### `ict_zone_evidence`

- **ID / 行**：`FUN-6EEC9DEABD` / `L11`（源码见本单元概览）
- **签名 / 返回**：`ict_zone_evidence(ctx: MarketContext)` → `list[EvidenceItem]`
- **职责**：FVG / OB proximity to current price.
- **依赖**：EvidenceItem、_TF_ZONE_WEIGHT.items、ctx.analyses.get、float、items.append、round、seen.add、set
- **复杂度 / 风险**：分支 7；跨度 49 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-8d8fc5eaa1"></a>

### src/agents/analysts/technical.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8D8FC5EAA1 |
| 源码 | [src/agents/analysts/technical.py](../../src/agents/analysts/technical.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Technical Analyst — indicators + ICT structure summary. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 9 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) |
| 验证状态 | selected |

#### 函数导航

[_structure_bias](#fun-6bf4e07518) · [_ict_context_evidence](#fun-a800d7efb0) · [_fibonacci_evidence](#fun-047ed2fce9) · [_indicator_evidence](#fun-30c0262d6e) · [_quality_evidence](#fun-efb2eb527e) · [_support_resistance_evidence](#fun-0adaa6f91a) · [_level_price_text](#fun-699a6c41bf) · [_pa_evidence](#fun-5e5145e5af) · [run_technical_analyst](#fun-10ecc215f3)

<a id="fun-6bf4e07518"></a>

#### `_structure_bias`

- **ID / 行**：`FUN-6BF4E07518` / `L19`（源码见本单元概览）
- **签名 / 返回**：`_structure_bias(analyses: dict[str, TimeframeAnalysis])` → `tuple[Bias, list[EvidenceItem]]`
- **职责**：As-built responsibility derived from `_structure_bias` and its owning unit.
- **依赖**：EvidenceItem、TF_WEIGHT.items、analyses.get、items.append
- **复杂度 / 风险**：分支 8；跨度 51 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a800d7efb0"></a>

#### `_ict_context_evidence`

- **ID / 行**：`FUN-A800D7EFB0` / `L72`（源码见本单元概览）
- **签名 / 返回**：`_ict_context_evidence(ctx: MarketContext)` → `tuple[Bias, list[EvidenceItem]]`
- **职责**：Convert computed ICT context into analyst evidence instead of leaving it report-only.
- **依赖**：EvidenceItem、TF_WEIGHT.items、abs、ctx.analyses.get、distance_pct、float、get、getattr、items.append、max、round、sorted
- **复杂度 / 风险**：分支 10；跨度 75 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-047ed2fce9"></a>

#### `_fibonacci_evidence`

- **ID / 行**：`FUN-047ED2FCE9` / `L149`（源码见本单元概览）
- **签名 / 返回**：`_fibonacci_evidence(technical_ctx: dict, price: float)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `_fibonacci_evidence` and its owning unit.
- **依赖**：EvidenceItem、distance_pct、fib.get、float、items.append、round、row.get、technical_ctx.get
- **复杂度 / 风险**：分支 2；跨度 28 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-30c0262d6e"></a>

#### `_indicator_evidence`

- **ID / 行**：`FUN-30C0262D6E` / `L179`（源码见本单元概览）
- **签名 / 返回**：`_indicator_evidence(technical_ctx: dict)` → `tuple[Bias, list[EvidenceItem]]`
- **职责**：As-built responsibility derived from `_indicator_evidence` and its owning unit.
- **依赖**：EvidenceItem、TF_WEIGHT.items、float、indicators.get、items.append、max、round、row.get、technical_ctx.get、values.get
- **复杂度 / 风险**：分支 13；跨度 83 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-efb2eb527e"></a>

#### `_quality_evidence`

- **ID / 行**：`FUN-EFB2EB527E` / `L264`（源码见本单元概览）
- **签名 / 返回**：`_quality_evidence(technical_ctx: dict)` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `_quality_evidence` and its owning unit.
- **依赖**：EvidenceItem、float、join、max、min、quality.get、technical_ctx.get
- **复杂度 / 风险**：分支 2；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0adaa6f91a"></a>

#### `_support_resistance_evidence`

- **ID / 行**：`FUN-0ADAA6F91A` / `L280`（源码见本单元概览）
- **签名 / 返回**：`_support_resistance_evidence(technical_ctx: dict)` → `tuple[Bias, list[EvidenceItem]]`
- **职责**：As-built responsibility derived from `_support_resistance_evidence` and its owning unit.
- **依赖**：EvidenceItem、_level_price_text、abs、float、items.append、level.get、max、min、sr.get、technical_ctx.get
- **复杂度 / 风险**：分支 7；跨度 49 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-699a6c41bf"></a>

#### `_level_price_text`

- **ID / 行**：`FUN-699A6C41BF` / `L331`（源码见本单元概览）
- **签名 / 返回**：`_level_price_text(level: dict)` → `str`
- **职责**：As-built responsibility derived from `_level_price_text` and its owning unit.
- **依赖**：float、level.get
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5e5145e5af"></a>

#### `_pa_evidence`

- **ID / 行**：`FUN-5E5145E5AF` / `L337`（源码见本单元概览）
- **签名 / 返回**：`_pa_evidence(technical_ctx: dict)` → `list[EvidenceItem]`
- **职责**：DGT volume profile / S&R facts for analyst evidence.
- **依赖**：EvidenceItem、block.get、float、items.append、lvl.get、pa.get、technical_ctx.get、vp.get
- **复杂度 / 风险**：分支 4；跨度 35 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-10ecc215f3"></a>

#### `run_technical_analyst`

- **ID / 行**：`FUN-10ECC215F3` / `L374`（源码见本单元概览）
- **签名 / 返回**：`run_technical_analyst(ctx: MarketContext)` → `AnalystReport`
- **职责**：As-built responsibility derived from `run_technical_analyst` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：EvidenceItem、MarketDataSource、TF_WEIGHT.get、_fibonacci_evidence、_ict_context_evidence、_indicator_evidence、_pa_evidence、_quality_evidence、_structure_bias、_support_resistance_evidence、biases.append、biases.count、build_report、build_technical_context、ctx.analyses.get、ctx.enriched.get、ema_items.append、ema_relation、fetch_evidence、float
- **复杂度 / 风险**：分支 14；跨度 105 行；high
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="unit-8933374b3e"></a>

### src/agents/bearish.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8933374B3E |
| 源码 | [src/agents/bearish.py](../../src/agents/bearish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Bearish researcher — structure + Analyst Team evidence for sell side. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) |
| 验证状态 | selected |

#### 函数导航

[_structure_items](#fun-c2054ace2c) · [run_bearish_researcher](#fun-63515361b0)

<a id="fun-c2054ace2c"></a>

#### `_structure_items`

- **ID / 行**：`FUN-C2054ACE2C` / `L12`（源码见本单元概览）
- **签名 / 返回**：`_structure_items(analyses: dict[str, TimeframeAnalysis])` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `_structure_items` and its owning unit.
- **依赖**：EvidenceItem、_TF_WEIGHT.items、items.append
- **复杂度 / 风险**：分支 11；跨度 66 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-63515361b0"></a>

#### `run_bearish_researcher`

- **ID / 行**：`FUN-63515361B0` / `L80`（源码见本单元概览）
- **签名 / 返回**：`run_bearish_researcher(ctx: MarketContext, team: AnalystTeam | None=None)` → `AgentEvidence`
- **职责**：As-built responsibility derived from `run_bearish_researcher` and its owning unit.
- **依赖**：AgentEvidence、_structure_items、items_for_direction、len、max、min、sum
- **复杂度 / 风险**：分支 2；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="unit-6008a95748"></a>

### src/agents/bullish.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6008A95748 |
| 源码 | [src/agents/bullish.py](../../src/agents/bullish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Bullish researcher — structure + Analyst Team evidence for buy side. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) |
| 验证状态 | selected |

#### 函数导航

[_structure_items](#fun-3bd84eeb0a) · [run_bullish_researcher](#fun-87ec3ef32e)

<a id="fun-3bd84eeb0a"></a>

#### `_structure_items`

- **ID / 行**：`FUN-3BD84EEB0A` / `L12`（源码见本单元概览）
- **签名 / 返回**：`_structure_items(analyses: dict[str, TimeframeAnalysis])` → `list[EvidenceItem]`
- **职责**：As-built responsibility derived from `_structure_items` and its owning unit.
- **依赖**：EvidenceItem、_TF_WEIGHT.items、items.append
- **复杂度 / 风险**：分支 9；跨度 56 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-87ec3ef32e"></a>

#### `run_bullish_researcher`

- **ID / 行**：`FUN-87EC3EF32E` / `L70`（源码见本单元概览）
- **签名 / 返回**：`run_bullish_researcher(ctx: MarketContext, team: AnalystTeam | None=None)` → `AgentEvidence`
- **职责**：As-built responsibility derived from `run_bullish_researcher` and its owning unit.
- **依赖**：AgentEvidence、_structure_items、items_for_direction、len、max、min、sum
- **复杂度 / 风险**：分支 2；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="unit-34bf03f815"></a>

### src/agents/debate.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-34BF03F815 |
| 源码 | [src/agents/debate.py](../../src/agents/debate.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Research debate — bull vs bear discussion → consensus. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_debate_coherence.py](../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) |
| 验证状态 | selected |

#### 函数导航

[run_debate](#fun-29aa7948ff)

<a id="fun-29aa7948ff"></a>

#### `run_debate`

- **ID / 行**：`FUN-29AA7948FF` / `L16`（源码见本单元概览）
- **签名 / 返回**：`run_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses, team: AnalystTeam | None=None, ctx: MarketContext | None=None)` → `ResearchDebate`
- **职责**：As-built responsibility derived from `run_debate` and its owning unit.
- **依赖**：ResearchDebate、abs、get、getattr、len、max、min、notes.append、row.get、sentiment.get、sentiment_score、strip
- **复杂度 / 风险**：分支 13；跨度 74 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_debate_coherence.py](../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="unit-f23db48d75"></a>

### src/agents/factory.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F23DB48D75 |
| 源码 | [src/agents/factory.py](../../src/agents/factory.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Agent factory — rule / llm / hybrid dispatch for each pipeline stage. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 20 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_coherence.py](../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) |
| 验证状态 | selected |

#### 函数导航

[_use_llm_stage](#fun-5766bc355b) · [_pick_evidence](#fun-8bd56770da) · [_pick_analyst_report](#fun-69649a77ae) · [_analyst_team_aggregate_source](#fun-61f26f47e9) · [_use_llm_analyst](#fun-590a53a74c) · [_needs_rule_baseline](#fun-c7c1e6f330) · [_llm_stage_ok](#fun-27167e88c9) · [_ensure_rule_baseline](#fun-3e86d74ceb) · [run_analyst_team](#fun-e8a54418d1) · [run_bullish](#fun-7a4ecb2fc6) · [run_bearish](#fun-5113cb3027) · [research_uses_parallel_llm](#fun-91a30f1f5d) · [run_research_team](#fun-70aa2e8b05) · [_pick_debate](#fun-4f354a267b) · [run_debate](#fun-7599e6282b) · [run_level_proposer](#fun-682ee70c11) · [run_trader](#fun-c68a4cf1f3) · [run_risk](#fun-bab0b34f57) · [run_risk._gate](#fun-d6ed0e37d5) · [run_manager](#fun-60d80a7b70)

<a id="fun-5766bc355b"></a>

#### `_use_llm_stage`

- **ID / 行**：`FUN-5766BC355B` / `L60`（源码见本单元概览）
- **签名 / 返回**：`_use_llm_stage(stage_enabled: bool)` → `bool`
- **职责**：As-built responsibility derived from `_use_llm_stage` and its owning unit.
- **依赖**：get_run_config、llm_configured、log.warning
- **复杂度 / 风险**：分支 3；跨度 9 行；low
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="fun-8bd56770da"></a>

#### `_pick_evidence`

- **ID / 行**：`FUN-8BD56770DA` / `L71`（源码见本单元概览）
- **签名 / 返回**：`_pick_evidence(stage: str, rule_result: AgentEvidence, llm_result: AgentEvidence | None, trace, pipeline: AgentPipelineMeta)` → `AgentEvidence`
- **职责**：As-built responsibility derived from `_pick_evidence` and its owning unit.
- **依赖**：StageMeta、get_run_config、pipeline.record
- **复杂度 / 风险**：分支 5；跨度 30 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-69649a77ae"></a>

#### `_pick_analyst_report`

- **ID / 行**：`FUN-69649A77AE` / `L103`（源码见本单元概览）
- **签名 / 返回**：`_pick_analyst_report(stage: str, rule_result: AnalystReport, llm_result: AnalystReport | None, trace, pipeline: AgentPipelineMeta)` → `AnalystReport`
- **职责**：As-built responsibility derived from `_pick_analyst_report` and its owning unit.
- **依赖**：StageMeta、_use_llm_stage、get_run_config、pipeline.record
- **复杂度 / 风险**：分支 6；跨度 32 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-61f26f47e9"></a>

#### `_analyst_team_aggregate_source`

- **ID / 行**：`FUN-61F26F47E9` / `L137`（源码见本单元概览）
- **签名 / 返回**：`_analyst_team_aggregate_source(llm_picked: int, total: int=4)` → `StageSource`
- **职责**：As-built responsibility derived from `_analyst_team_aggregate_source` and its owning unit.
- **依赖**：get_run_config
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-590a53a74c"></a>

#### `_use_llm_analyst`

- **ID / 行**：`FUN-590A53A74C` / `L145`（源码见本单元概览）
- **签名 / 返回**：`_use_llm_analyst(stage: str)` → `bool`
- **职责**：As-built responsibility derived from `_use_llm_analyst` and its owning unit.
- **依赖**：get_run_config
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c7c1e6f330"></a>

#### `_needs_rule_baseline`

- **ID / 行**：`FUN-C7C1E6F330` / `L149`（源码见本单元概览）
- **签名 / 返回**：`_needs_rule_baseline()` → `bool`
- **职责**：Hybrid always needs rule output; pure LLM tries LLM first.
- **依赖**：get_run_config
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-27167e88c9"></a>

#### `_llm_stage_ok`

- **ID / 行**：`FUN-27167E88C9` / `L154`（源码见本单元概览）
- **签名 / 返回**：`_llm_stage_ok(llm_result, trace)` → `bool`
- **职责**：As-built responsibility derived from `_llm_stage_ok` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-3e86d74ceb"></a>

#### `_ensure_rule_baseline`

- **ID / 行**：`FUN-3E86D74CEB` / `L158`（源码见本单元概览）
- **签名 / 返回**：`_ensure_rule_baseline(rule_result, llm_result, trace, compute_rule)` → `runtime/inferred`
- **职责**：Lazy rule baseline: skip in pure LLM mode when LLM already succeeded.
- **依赖**：_llm_stage_ok、compute_rule、get_run_config
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e8a54418d1"></a>

#### `run_analyst_team`

- **ID / 行**：`FUN-E8A54418D1` / `L167`（源码见本单元概览）
- **签名 / 返回**：`run_analyst_team(ctx: MarketContext, pipeline: AgentPipelineMeta)` → `AnalystTeam`
- **职责**：As-built responsibility derived from `run_analyst_team` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：AnalystTeam、StageMeta、_analyst_team_aggregate_source、_llm_stage_ok、_needs_rule_baseline、_pick_analyst_report、_use_llm_analyst、_use_llm_stage、analyst_team_input_payload、fn、get_progress、get_run_config、getattr、int、json.dumps、len、llm_tasks.append、min、pipeline.record、prog.stage_io
- **复杂度 / 风险**：分支 22；跨度 113 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="fun-7a4ecb2fc6"></a>

#### `run_bullish`

- **ID / 行**：`FUN-7A4ECB2FC6` / `L282`（源码见本单元概览）
- **签名 / 返回**：`run_bullish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam)` → `AgentEvidence`
- **职责**：As-built responsibility derived from `run_bullish` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_ensure_rule_baseline、_needs_rule_baseline、_pick_evidence、_use_llm_stage、get_progress、get_run_config、pipeline.record、rule_bullish、run_llm_bullish、update
- **复杂度 / 风险**：分支 3；跨度 18 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5113cb3027"></a>

#### `run_bearish`

- **ID / 行**：`FUN-5113CB3027` / `L302`（源码见本单元概览）
- **签名 / 返回**：`run_bearish(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam)` → `AgentEvidence`
- **职责**：As-built responsibility derived from `run_bearish` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_ensure_rule_baseline、_needs_rule_baseline、_pick_evidence、_use_llm_stage、get_progress、get_run_config、pipeline.record、rule_bearish、run_llm_bearish、update
- **复杂度 / 风险**：分支 3；跨度 18 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-91a30f1f5d"></a>

#### `research_uses_parallel_llm`

- **ID / 行**：`FUN-91A30F1F5D` / `L322`（源码见本单元概览）
- **签名 / 返回**：`research_uses_parallel_llm()` → `bool`
- **职责**：True when bullish/bearish LLM stages should run concurrently (saves wall time).
- **依赖**：_use_llm_stage、get_run_config
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="fun-70aa2e8b05"></a>

#### `run_research_team`

- **ID / 行**：`FUN-70AA2E8B05` / `L332`（源码见本单元概览）
- **签名 / 返回**：`run_research_team(ctx: MarketContext, pipeline: AgentPipelineMeta, team: AnalystTeam)` → `tuple[AgentEvidence, AgentEvidence]`
- **职责**：Run bullish and bearish research in parallel when both stages use LLM.
- **异常 / 副作用 / 并发**：RuntimeError / none-detected / caller-thread
- **依赖**：RuntimeError、StageMeta、_ensure_rule_baseline、_needs_rule_baseline、_pick_evidence、_use_llm_stage、get_run_config、pipeline.record、results.get、rule_bearish、rule_bullish、run_llm_bearish、run_llm_bullish、run_parallel
- **复杂度 / 风险**：分支 5；跨度 45 行；medium
- **测试 / 验证**：[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="fun-4f354a267b"></a>

#### `_pick_debate`

- **ID / 行**：`FUN-4F354A267B` / `L379`（源码见本单元概览）
- **签名 / 返回**：`_pick_debate(rule_result: ResearchDebate, llm_result: ResearchDebate | None, trace, pipeline: AgentPipelineMeta)` → `ResearchDebate`
- **职责**：As-built responsibility derived from `_pick_debate` and its owning unit.
- **依赖**：StageMeta、get_run_config、pipeline.record
- **复杂度 / 风险**：分支 5；跨度 27 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7599e6282b"></a>

#### `run_debate`

- **ID / 行**：`FUN-7599E6282B` / `L408`（源码见本单元概览）
- **签名 / 返回**：`run_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses, pipeline: AgentPipelineMeta, team: AnalystTeam, ctx: MarketContext)` → `ResearchDebate`
- **职责**：As-built responsibility derived from `run_debate` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_needs_rule_baseline、_pick_debate、_use_llm_stage、get_progress、get_run_config、pipeline.record、rule_debate、run_llm_debate、run_parallel、update
- **复杂度 / 风险**：分支 3；跨度 34 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_debate_coherence.py](../../tests/unit/test_debate_coherence.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-682ee70c11"></a>

#### `run_level_proposer`

- **ID / 行**：`FUN-682EE70C11` / `L444`（源码见本单元概览）
- **签名 / 返回**：`run_level_proposer(ctx: MarketContext, team: AnalystTeam, debate: ResearchDebate, pipeline: AgentPipelineMeta, rule_signals: list[TradingSignal])` → `list[LevelProposal]`
- **职责**：As-built responsibility derived from `run_level_proposer` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_use_llm_stage、get_progress、get_run_config、len、log.info、log.warning、pipeline.record、run_llm_level_proposer、update
- **复杂度 / 风险**：分支 2；跨度 25 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-c68a4cf1f3"></a>

#### `run_trader`

- **ID / 行**：`FUN-C68A4CF1F3` / `L471`（源码见本单元概览）
- **签名 / 返回**：`run_trader(ctx: MarketContext, debate: ResearchDebate, pipeline: AgentPipelineMeta, signals: list[TradingSignal], team: AnalystTeam | None=None, *, observation_mode: bool=False)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `run_trader` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_use_llm_stage、get_progress、get_run_config、pipeline.record、rule_trader、run_llm_trader、update
- **复杂度 / 风险**：分支 4；跨度 33 行；high
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-bab0b34f57"></a>

#### `run_risk`

- **ID / 行**：`FUN-BAB0B34F57` / `L506`（源码见本单元概览）
- **签名 / 返回**：`run_risk(proposal: TransactionProposal, signals: list, pipeline: AgentPipelineMeta, *, current_price: float=0.0, data_as_of: dict | None=None, observation_mode: bool=False)` → `list[RiskReview]`
- **职责**：As-built responsibility derived from `run_risk` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_gate、_use_llm_stage、apply_risk_gates、get_progress、get_run_config、len、pipeline.record、rule_risk、run_llm_risk、update
- **复杂度 / 风险**：分支 4；跨度 56 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-d6ed0e37d5"></a>

#### `run_risk._gate`

- **ID / 行**：`FUN-D6ED0E37D5` / `L515`（源码见本单元概览）
- **签名 / 返回**：`run_risk._gate(reviews: list[RiskReview])` → `list[RiskReview]`
- **职责**：As-built responsibility derived from `_gate` and its owning unit.
- **依赖**：apply_risk_gates
- **复杂度 / 风险**：分支 0；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-60d80a7b70"></a>

#### `run_manager`

- **ID / 行**：`FUN-60D80A7B70` / `L564`（源码见本单元概览）
- **签名 / 返回**：`run_manager(proposal: TransactionProposal, reviews: list[RiskReview], pipeline: AgentPipelineMeta)` → `ManagerDecision`
- **职责**：As-built responsibility derived from `run_manager` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：StageMeta、_use_llm_stage、get_progress、get_run_config、pipeline.record、rule_manager、run_llm_manager、update
- **复杂度 / 风险**：分支 4；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) · direct-dynamic

<a id="unit-1606bdc6e2"></a>

### src/agents/llm/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1606BDC6E2 |
| 源码 | [src/agents/llm/__init__.py](../../src/agents/llm/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM agent stages — optional LLM implementations for the pipeline. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3eeb009803"></a>

### src/agents/llm/base.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3EEB009803 |
| 源码 | [src/agents/llm/base.py](../../src/agents/llm/base.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Shared utilities for LLM agent stages. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 5 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_llm_json.py](../../tests/unit/test_llm_json.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py) |
| 验证状态 | selected |

#### 函数导航

[_backoff_seconds](#fun-e3963880ea) · [_parse_llm_json](#fun-b6641135ba) · [_stream_once](#fun-6474c56d9a) · [stream_llm_json](#fun-79e9f3d3c1) · [run_llm_stage](#fun-ddb9984fe6)

<a id="fun-e3963880ea"></a>

#### `_backoff_seconds`

- **ID / 行**：`FUN-E3963880EA` / `L30`（源码见本单元概览）
- **签名 / 返回**：`_backoff_seconds(attempt: int)` → `float`
- **职责**：As-built responsibility derived from `_backoff_seconds` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b6641135ba"></a>

#### `_parse_llm_json`

- **ID / 行**：`FUN-B6641135BA` / `L36`（源码见本单元概览）
- **签名 / 返回**：`_parse_llm_json(raw: str)` → `dict[str, Any]`
- **职责**：Parse LLM JSON output with light repair for truncated / wrapped responses.
- **异常 / 副作用 / 并发**：ValueError;json.JSONDecodeError;last_err / none-detected / caller-thread
- **依赖**：ValueError、attempts.append、isinstance、json.JSONDecodeError、json.loads、list、raw.strip、re.sub、text.find、text.rfind
- **复杂度 / 风险**：分支 6；跨度 27 行；low
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_llm_json.py](../../tests/unit/test_llm_json.py) · direct-dynamic

<a id="fun-6474c56d9a"></a>

#### `_stream_once`

- **ID / 行**：`FUN-6474C56D9A` / `L65`（源码见本单元概览）
- **签名 / 返回**：`_stream_once(client: LLMClient, messages: list[dict[str, str]], *, stage: str, temperature: float)` → `str`
- **职责**：Single upstream SSE request (no retries). Progress chunk updates only.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：client.chat_stream、get_progress、prog.run_llm_stream
- **复杂度 / 风险**：分支 0；跨度 17 行；low
- **测试 / 验证**：[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py) · direct-dynamic

<a id="fun-79e9f3d3c1"></a>

#### `stream_llm_json`

- **ID / 行**：`FUN-79E9F3D3C1` / `L84`（源码见本单元概览）
- **签名 / 返回**：`stream_llm_json(client: LLMClient, messages: list[dict[str, str]], *, stage: str, temperature: float=0.2, max_attempts: int | None=None)` → `str`
- **职责**：Stream JSON with a countable attempt budget (transport only).
- **异常 / 副作用 / 并发**：last_exc / none-detected / caller-thread
- **依赖**：_backoff_seconds、_stream_once、get_stage_policy、int、log.warning、max、min、range、time.sleep
- **复杂度 / 风险**：分支 5；跨度 39 行；medium
- **测试 / 验证**：[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py) · direct-dynamic

<a id="fun-ddb9984fe6"></a>

#### `run_llm_stage`

- **ID / 行**：`FUN-DDB9984FE6` / `L125`（源码见本单元概览）
- **签名 / 返回**：`run_llm_stage(*, stage: str, model: str, client: LLMClient, messages: list[dict[str, str]], parse: Callable[[dict[str, Any]], T], temperature: float=0.2)` → `tuple[T | None, LLMStageTrace]`
- **职责**：Execute one LLM stage with a unified attempt budget and telemetry.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：LLMStageTrace、_backoff_seconds、_parse_llm_json、_stream_once、apply_input_budget、attempt_log.append、bool、budget_meta.get、build_routing_strategy、estimate_text_size、get_progress、get_stage_policy、int、len、log.info、log.warning、min、parse、prog.llm_begin、prog.llm_end
- **复杂度 / 风险**：分支 9；跨度 189 行；high
- **测试 / 验证**：[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) · direct-dynamic

<a id="unit-3a49bda3a6"></a>

### src/agents/llm/payload.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3A49BDA3A6 |
| 源码 | [src/agents/llm/payload.py](../../src/agents/llm/payload.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Build JSON payloads for LLM agent stages (with analyst input budgets). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 25 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) |
| 验证状态 | selected |

#### 函数导航

[_tf_block](#fun-2aeed14a2e) · [_structure_vote](#fun-f3d598c89c) · [_timeframe_trends](#fun-eaa77ee71a) · [_event_risk_block](#fun-6d3cf52f12) · [technical_level_reactions_payload](#fun-c677217758) · [analyst_team_payload](#fun-6c3bfd3baa) · [analyst_team_summaries_payload](#fun-a152bbc0e8) · [analyst_team_input_payload](#fun-6749b95a24) · [_fibonacci_block](#fun-293475f5a3) · [market_payload](#fun-3c9a11e1b3) · [research_payload](#fun-fddf16b339) · [technical_analyst_payload](#fun-081944e744) · [fundamentals_analyst_payload](#fun-f93a6b184d) · [news_analyst_payload](#fun-3fc60de348) · [sentiment_analyst_payload](#fun-e83e383708) · [debate_payload](#fun-3e594bc0fa) · [evidence_payload](#fun-8646951a9c) · [_signal_payload](#fun-35a12d35f4) · [signal_list_payload](#fun-256c7b349e) · [_legacy_trader_payload](#fun-992d8a594f) · [trader_decision_payload](#fun-8ce195cdf3) · [trader_payload](#fun-aac9fbd67b) · [risk_payload](#fun-f44f676424) · [manager_payload](#fun-63914db325) · [level_proposer_payload](#fun-c4847806bf)

<a id="fun-2aeed14a2e"></a>

#### `_tf_block`

- **ID / 行**：`FUN-2AEED14A2E` / `L34`（源码见本单元概览）
- **签名 / 返回**：`_tf_block(tf: str, analysis: TimeframeAnalysis, *, price: float)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_tf_block` and its owning unit.
- **依赖**：timeframe_context
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f3d598c89c"></a>

#### `_structure_vote`

- **ID / 行**：`FUN-F3D598C89C` / `L38`（源码见本单元概览）
- **签名 / 返回**：`_structure_vote(analyses)` → `dict[str, float]`
- **职责**：As-built responsibility derived from `_structure_vote` and its owning unit.
- **依赖**：sentiment_score
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-eaa77ee71a"></a>

#### `_timeframe_trends`

- **ID / 行**：`FUN-EAA77EE71A` / `L42`（源码见本单元概览）
- **签名 / 返回**：`_timeframe_trends(ctx: MarketContext)` → `dict[str, str]`
- **职责**：As-built responsibility derived from `_timeframe_trends` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6d3cf52f12"></a>

#### `_event_risk_block`

- **ID / 行**：`FUN-6D3CF52F12` / `L48`（源码见本单元概览）
- **签名 / 返回**：`_event_risk_block(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_event_risk_block` and its owning unit.
- **依赖**：ctx.derived.get、min
- **复杂度 / 风险**：分支 0；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c677217758"></a>

#### `technical_level_reactions_payload`

- **ID / 行**：`FUN-C677217758` / `L57`（源码见本单元概览）
- **签名 / 返回**：`technical_level_reactions_payload(team: AnalystTeam)` → `list[dict[str, Any]]`
- **职责**：Level-reaction hypotheses from technical analyst for the level proposer.
- **依赖**：float、item.refs.get、list、recovered.append、round、str、strip
- **复杂度 / 风险**：分支 5；跨度 28 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-6c3bfd3baa"></a>

#### `analyst_team_payload`

- **ID / 行**：`FUN-6C3BFD3BAA` / `L87`（源码见本单元概览）
- **签名 / 返回**：`analyst_team_payload(team: AnalystTeam)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `analyst_team_payload` and its owning unit.
- **依赖**：getattr、list、sorted
- **复杂度 / 风险**：分支 2；跨度 25 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a152bbc0e8"></a>

#### `analyst_team_summaries_payload`

- **ID / 行**：`FUN-A152BBC0E8` / `L114`（源码见本单元概览）
- **签名 / 返回**：`analyst_team_summaries_payload(team: AnalystTeam, *, top_items: int=0)` → `dict[str, Any]`
- **职责**：Bias/summary/confidence per role; optional top-N evidence items per role.
- **依赖**：getattr、sorted
- **复杂度 / 风险**：分支 2；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-6749b95a24"></a>

#### `analyst_team_input_payload`

- **ID / 行**：`FUN-6749B95A24` / `L139`（源码见本单元概览）
- **签名 / 返回**：`analyst_team_input_payload(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：Per-specialist inputs actually sent to Analyst Team LLM stages (for stage_io audit).
- **依赖**：fundamentals_analyst_payload、news_analyst_payload、sentiment_analyst_payload、technical_analyst_payload
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-293475f5a3"></a>

#### `_fibonacci_block`

- **ID / 行**：`FUN-293475F5A3` / `L150`（源码见本单元概览）
- **签名 / 返回**：`_fibonacci_block(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：Use the same primary swing selection as rule technical evidence.
- **依赖**：fibonacci_context
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-3c9a11e1b3"></a>

#### `market_payload`

- **ID / 行**：`FUN-3C9A11E1B3` / `L155`（源码见本单元概览）
- **签名 / 返回**：`market_payload(ctx: MarketContext, team: AnalystTeam | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `market_payload` and its owning unit.
- **依赖**：_tf_block、analyst_team_payload、ctx.external.to_dict
- **复杂度 / 风险**：分支 1；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fddf16b339"></a>

#### `research_payload`

- **ID / 行**：`FUN-FDDF16B339` / `L176`（源码见本单元概览）
- **签名 / 返回**：`research_payload(ctx: MarketContext, team: AnalystTeam, direction: str)` → `dict[str, Any]`
- **职责**：Research stage: analyst conclusions primary; minimal structure/event validation.
- **依赖**：_event_risk_block、_structure_vote、_timeframe_trends、analyst_evidence_ids、analyst_team_payload、market_payload、sorted
- **复杂度 / 风险**：分支 1；跨度 19 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-081944e744"></a>

#### `technical_analyst_payload`

- **ID / 行**：`FUN-081944E744` / `L197`（源码见本单元概览）
- **签名 / 返回**：`technical_analyst_payload(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `technical_analyst_payload` and its owning unit.
- **依赖**：_fibonacci_block、base.get、build_pa_llm_summary、build_technical_context、ctx.context_stats.get、ctx.derived.get、ema_relation、technical_claim_fact_catalog
- **复杂度 / 风险**：分支 3；跨度 30 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-f93a6b184d"></a>

#### `fundamentals_analyst_payload`

- **ID / 行**：`FUN-F93A6B184D` / `L229`（源码见本单元概览）
- **签名 / 返回**：`fundamentals_analyst_payload(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `fundamentals_analyst_payload` and its owning unit.
- **依赖**：ctx.derived.get、m.to_dict
- **复杂度 / 风险**：分支 1；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py) · direct-dynamic

<a id="fun-3fc60de348"></a>

#### `news_analyst_payload`

- **ID / 行**：`FUN-3FC60DE348` / `L244`（源码见本单元概览）
- **签名 / 返回**：`news_analyst_payload(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `news_analyst_payload` and its owning unit.
- **依赖**：ctx.derived.get、ext.to_dict、ext_dict.get、len
- **复杂度 / 风险**：分支 1；跨度 40 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-e83e383708"></a>

#### `sentiment_analyst_payload`

- **ID / 行**：`FUN-E83E383708` / `L286`（源码见本单元概览）
- **签名 / 返回**：`sentiment_analyst_payload(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `sentiment_analyst_payload` and its owning unit.
- **依赖**：sentiment_score
- **复杂度 / 风险**：分支 0；跨度 12 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py) · direct-dynamic

<a id="fun-3e594bc0fa"></a>

#### `debate_payload`

- **ID / 行**：`FUN-3E594BC0FA` / `L300`（源码见本单元概览）
- **签名 / 返回**：`debate_payload(bullish: AgentEvidence, bearish: AgentEvidence, analyses, *, ctx: MarketContext | None=None, team: AnalystTeam | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `debate_payload` and its owning unit.
- **依赖**：_event_risk_block、analyst_team_summaries_payload、ctx.derived.get、evidence_payload、getattr、sentiment_score
- **复杂度 / 风险**：分支 4；跨度 38 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-8646951a9c"></a>

#### `evidence_payload`

- **ID / 行**：`FUN-8646951A9C` / `L340`（源码见本单元概览）
- **签名 / 返回**：`evidence_payload(evidence: AgentEvidence)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `evidence_payload` and its owning unit.
- **依赖**：sorted
- **复杂度 / 风险**：分支 0；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-35a12d35f4"></a>

#### `_signal_payload`

- **ID / 行**：`FUN-35A12D35F4` / `L361`（源码见本单元概览）
- **签名 / 返回**：`_signal_payload(signal: Any)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_signal_payload` and its owning unit.
- **依赖**：getattr
- **复杂度 / 风险**：分支 0；跨度 15 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-256c7b349e"></a>

#### `signal_list_payload`

- **ID / 行**：`FUN-256C7B349E` / `L378`（源码见本单元概览）
- **签名 / 返回**：`signal_list_payload(signals: list[Any])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `signal_list_payload` and its owning unit.
- **依赖**：_signal_payload、enumerate
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-992d8a594f"></a>

#### `_legacy_trader_payload`

- **ID / 行**：`FUN-992D8A594F` / `L385`（源码见本单元概览）
- **签名 / 返回**：`_legacy_trader_payload(ctx: MarketContext, debate: ResearchDebate, signals: list[Any])` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_legacy_trader_payload` and its owning unit.
- **依赖**：market_payload、signal_list_payload
- **复杂度 / 风险**：分支 0；跨度 19 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-8ce195cdf3"></a>

#### `trader_decision_payload`

- **ID / 行**：`FUN-8CE195CDF3` / `L406`（源码见本单元概览）
- **签名 / 返回**：`trader_decision_payload(ctx: MarketContext, debate: ResearchDebate, team: AnalystTeam, signals: list[Any])` → `dict[str, Any]`
- **职责**：Trader stage: debate consensus + analyst summaries + candidate signals (no raw market dump).
- **依赖**：_structure_vote、analyst_team_summaries_payload、signal_list_payload
- **复杂度 / 风险**：分支 0；跨度 26 行；high
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-aac9fbd67b"></a>

#### `trader_payload`

- **ID / 行**：`FUN-AAC9FBD67B` / `L434`（源码见本单元概览）
- **签名 / 返回**：`trader_payload(ctx: MarketContext, debate: ResearchDebate, signals: list[Any], team: AnalystTeam | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `trader_payload` and its owning unit.
- **依赖**：_legacy_trader_payload、trader_decision_payload
- **复杂度 / 风险**：分支 1；跨度 9 行；high
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-f44f676424"></a>

#### `risk_payload`

- **ID / 行**：`FUN-F44F676424` / `L445`（源码见本单元概览）
- **签名 / 返回**：`risk_payload(proposal: TransactionProposal, signal_count: int, *, signals: list[Any] | None=None, current_price: float | None=None, data_as_of: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `risk_payload` and its owning unit.
- **依赖**：_signal_payload、float、isinstance、len、proposal.to_dict、round、row.get、selected.append、sig.get
- **复杂度 / 风险**：分支 4；跨度 49 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-63914db325"></a>

#### `manager_payload`

- **ID / 行**：`FUN-63914DB325` / `L496`（源码见本单元概览）
- **签名 / 返回**：`manager_payload(proposal: TransactionProposal, reviews: list[RiskReview])` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `manager_payload` and its owning unit.
- **依赖**：proposal.to_dict、r.to_dict
- **复杂度 / 风险**：分支 0；跨度 15 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="fun-c4847806bf"></a>

#### `level_proposer_payload`

- **ID / 行**：`FUN-C4847806BF` / `L513`（源码见本单元概览）
- **签名 / 返回**：`level_proposer_payload(ctx: MarketContext, team: AnalystTeam, debate: ResearchDebate, rule_signals: list[Any])` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `level_proposer_payload` and its owning unit.
- **依赖**：_signal_payload、analyst_team_payload、build_pa_llm_summary、build_technical_context、market_payload、structure.get、technical_claim_fact_catalog、technical_level_reactions_payload
- **复杂度 / 风险**：分支 1；跨度 70 行；medium
- **测试 / 验证**：[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py) · direct-dynamic

<a id="unit-9b539edeb6"></a>

### src/agents/llm/schemas.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9B539EDEB6 |
| 源码 | [src/agents/llm/schemas.py](../../src/agents/llm/schemas.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Parse LLM JSON into pipeline domain types. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 18 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[_item_refs](#fun-8ec477c06b) · [_clamp_strength](#fun-330aae4a56) · [_string_list](#fun-352076cbe7) · [_index_list](#fun-fefe6cd472) · [_float_field](#fun-d4331ef421) · [_parse_level_reactions](#fun-abc4913591) · [_level_reactions_from_items](#fun-16c25d76d9) · [_merge_level_reactions_into_items](#fun-1aa683b3a6) · [parse_analyst_report](#fun-bb1277c4f9) · [parse_agent_evidence](#fun-5a54aee754) · [parse_research_debate](#fun-c7499346d6) · [_compose_level_deduction_reason](#fun-3f721baec4) · [_level_deduction_quality](#fun-548d3233a2) · [parse_level_proposals](#fun-28618f8314) · [_validate_level_path_contract](#fun-866b1d79aa) · [parse_transaction_proposal](#fun-1cf0104153) · [parse_risk_reviews](#fun-616d649c39) · [parse_manager_decision](#fun-675d6fb6d6)

<a id="fun-8ec477c06b"></a>

#### `_item_refs`

- **ID / 行**：`FUN-8EC477C06B` / `L33`（源码见本单元概览）
- **签名 / 返回**：`_item_refs(row: dict[str, Any], category: str)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_item_refs` and its owning unit.
- **依赖**：_DEFAULT_ITEM_SOURCE.get、isinstance、refs.get、row.get、str
- **复杂度 / 风险**：分支 4；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-330aae4a56"></a>

#### `_clamp_strength`

- **ID / 行**：`FUN-330AAE4A56` / `L46`（源码见本单元概览）
- **签名 / 返回**：`_clamp_strength(v: Any)` → `float`
- **职责**：As-built responsibility derived from `_clamp_strength` and its owning unit.
- **依赖**：float、max、min
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-352076cbe7"></a>

#### `_string_list`

- **ID / 行**：`FUN-352076CBE7` / `L54`（源码见本单元概览）
- **签名 / 返回**：`_string_list(value: Any, *, fallback: list[str] | None=None, limit: int=8)` → `list[str]`
- **职责**：As-built responsibility derived from `_string_list` and its owning unit.
- **依赖**：isinstance、str、strip
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fefe6cd472"></a>

#### `_index_list`

- **ID / 行**：`FUN-FEFE6CD472` / `L64`（源码见本单元概览）
- **签名 / 返回**：`_index_list(value: Any, *, allowed: set[int])` → `list[int]`
- **职责**：As-built responsibility derived from `_index_list` and its owning unit.
- **依赖**：int、isinstance、out.append
- **复杂度 / 风险**：分支 4；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d4331ef421"></a>

#### `_float_field`

- **ID / 行**：`FUN-D4331EF421` / `L78`（源码见本单元概览）
- **签名 / 返回**：`_float_field(row: dict[str, Any], name: str)` → `float`
- **职责**：As-built responsibility derived from `_float_field` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、float
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-abc4913591"></a>

#### `_parse_level_reactions`

- **ID / 行**：`FUN-ABC4913591` / `L85`（源码见本单元概览）
- **签名 / 返回**：`_parse_level_reactions(data: dict[str, Any], *, agent: str)` → `list[dict[str, Any]]`
- **职责**：Technical analyst reaction hypotheses at POC / VA / S/R.
- **依赖**：_clamp_strength、data.get、enumerate、float、isinstance、lower、out.append、relation.get、relationships.append、round、row.get、set、sorted、str、strip
- **复杂度 / 风险**：分支 9；跨度 63 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-16c25d76d9"></a>

#### `_level_reactions_from_items`

- **ID / 行**：`FUN-16C25D76D9` / `L150`（源码见本单元概览）
- **签名 / 返回**：`_level_reactions_from_items(items: list[EvidenceItem])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_level_reactions_from_items` and its owning unit.
- **依赖**：float、item.refs.get、list、recovered.append、round、str、strip
- **复杂度 / 风险**：分支 4；跨度 24 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-1aa683b3a6"></a>

#### `_merge_level_reactions_into_items`

- **ID / 行**：`FUN-1AA683B3A6` / `L176`（源码见本单元概览）
- **签名 / 返回**：`_merge_level_reactions_into_items(items: list[EvidenceItem], reactions: list[dict[str, Any]], *, agent: str)` → `list[EvidenceItem]`
- **职责**：Expose reactions as evidence for research / levels binding.
- **依赖**：EvidenceItem、enumerate、existing_ids.add、float、isinstance、list、merged.append、row.get、str、strip
- **复杂度 / 风险**：分支 6；跨度 41 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-bb1277c4f9"></a>

#### `parse_analyst_report`

- **ID / 行**：`FUN-BB1277C4F9` / `L219`（源码见本单元概览）
- **签名 / 返回**：`parse_analyst_report(data: dict[str, Any], *, agent: str)` → `AnalystReport`
- **职责**：As-built responsibility derived from `parse_analyst_report` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：AnalystReport、EvidenceItem、ValueError、_clamp_strength、_item_refs、_level_reactions_from_items、_merge_level_reactions_into_items、_parse_level_reactions、data.get、enumerate、isinstance、items.append、len、lower、row.get、str、strip
- **复杂度 / 风险**：分支 11；跨度 57 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="fun-5a54aee754"></a>

#### `parse_agent_evidence`

- **ID / 行**：`FUN-5A54AEE754` / `L278`（源码见本单元概览）
- **签名 / 返回**：`parse_agent_evidence(data: dict[str, Any], *, agent: str, direction: Bias, allowed_evidence_ids: set[str] | None=None, evidence_registry: dict[str, EvidenceItem] | None=None)` → `AgentEvidence`
- **职责**：As-built responsibility derived from `parse_agent_evidence` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：AgentEvidence、EvidenceItem、ValueError、_clamp_strength、_item_refs、blend_research_confidence、build_research_provenance_meta、data.get、enumerate、isinstance、items.append、len、parse_research_items、row.get、set、str、strip
- **复杂度 / 风险**：分支 7；跨度 76 行；medium
- **测试 / 验证**：[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) · direct-dynamic

<a id="fun-c7499346d6"></a>

#### `parse_research_debate`

- **ID / 行**：`FUN-C7499346D6` / `L356`（源码见本单元概览）
- **签名 / 返回**：`parse_research_debate(data: dict[str, Any], *, bullish: AgentEvidence, bearish: AgentEvidence)` → `ResearchDebate`
- **职责**：As-built responsibility derived from `parse_research_debate` and its owning unit.
- **依赖**：ResearchDebate、_clamp_strength、blend_debate_consensus、build_debate_provenance_meta、data.get、isinstance、lower、notes.append、round、str、strip
- **复杂度 / 风险**：分支 4；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_evidence_provenance.py](../../tests/unit/test_evidence_provenance.py) · direct-dynamic

<a id="fun-3f721baec4"></a>

#### `_compose_level_deduction_reason`

- **ID / 行**：`FUN-3F721BAEC4` / `L405`（源码见本单元概览）
- **签名 / 返回**：`_compose_level_deduction_reason(*, anchor_level: str, expected_reaction: str, deduction: str, reason: str)` → `str`
- **职责**：Build audit-friendly reason from structured reaction thesis fields.
- **依赖**：join、parts.append
- **复杂度 / 风险**：分支 5；跨度 18 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-548d3233a2"></a>

#### `_level_deduction_quality`

- **ID / 行**：`FUN-548D3233A2` / `L425`（源码见本单元概览）
- **签名 / 返回**：`_level_deduction_quality(*, anchor_level: str, expected_reaction: str, deduction: str, reason: str, reaction_evidence_id: str)` → `bool`
- **职责**：Prefer binding to technical reactions; allow short bind reason or legacy thesis.
- **依赖**：bool、len
- **复杂度 / 风险**：分支 3；跨度 17 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-28618f8314"></a>

#### `parse_level_proposals`

- **ID / 行**：`FUN-28618F8314` / `L444`（源码见本单元概览）
- **签名 / 返回**：`parse_level_proposals(data: dict[str, Any])` → `list[LevelProposal]`
- **职责**：As-built responsibility derived from `parse_level_proposals` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：LevelProposal、ValueError、_clamp_strength、_compose_level_deduction_reason、_float_field、_level_deduction_quality、_validate_level_path_contract、data.get、enumerate、float、isinstance、proposals.append、round、row.get、str、strip、take_profits.append、upper
- **复杂度 / 风险**：分支 11；跨度 86 行；medium
- **测试 / 验证**：[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py) · direct-dynamic

<a id="fun-866b1d79aa"></a>

#### `_validate_level_path_contract`

- **ID / 行**：`FUN-866B1D79AA` / `L532`（源码见本单元概览）
- **签名 / 返回**：`_validate_level_path_contract(proposals: list[LevelProposal])` → `None`
- **职责**：As-built responsibility derived from `_validate_level_path_contract` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、len、sorted
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-1cf0104153"></a>

#### `parse_transaction_proposal`

- **ID / 行**：`FUN-1CF0104153` / `L540`（源码见本单元概览）
- **签名 / 返回**：`parse_transaction_proposal(data: dict[str, Any], *, debate_bias: Bias, signal_count: int)` → `TransactionProposal`
- **职责**：As-built responsibility derived from `parse_transaction_proposal` and its owning unit.
- **依赖**：TransactionProposal、_index_list、_string_list、data.get、lower、max、range、set、str
- **复杂度 / 风险**：分支 2；跨度 25 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-616d649c39"></a>

#### `parse_risk_reviews`

- **ID / 行**：`FUN-616D649C39` / `L567`（源码见本单元概览）
- **签名 / 返回**：`parse_risk_reviews(data: dict[str, Any], *, proposal: TransactionProposal, signal_count: int)` → `list[RiskReview]`
- **职责**：As-built responsibility derived from `parse_risk_reviews` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：RiskReview、ValueError、_clamp_strength、_index_list、_string_list、bool、data.get、isinstance、join、lower、row.get、str
- **复杂度 / 风险**：分支 6；跨度 34 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-675d6fb6d6"></a>

#### `parse_manager_decision`

- **ID / 行**：`FUN-675D6FB6D6` / `L603`（源码见本单元概览）
- **签名 / 返回**：`parse_manager_decision(data: dict[str, Any], *, proposal: TransactionProposal, reviews: list[RiskReview])` → `ManagerDecision`
- **职责**：As-built responsibility derived from `parse_manager_decision` and its owning unit.
- **依赖**：ManagerDecision、_clamp_strength、_index_list、data.get、intersection、lower、min、set、str、strip
- **复杂度 / 风险**：分支 7；跨度 42 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="unit-7226a2379a"></a>

### src/agents/llm/stages/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7226A2379A |
| 源码 | [src/agents/llm/stages/__init__.py](../../src/agents/llm/stages/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | 继承 规则/LLM Agent 编排 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-1df6497ce4"></a>

### src/agents/llm/stages/analysts/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1DF6497CE4 |
| 源码 | [src/agents/llm/stages/analysts/__init__.py](../../src/agents/llm/stages/analysts/__init__.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM stages for Analyst Team specialists. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-73b0811649"></a>

### src/agents/llm/stages/analysts/_common.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-73B0811649 |
| 源码 | [src/agents/llm/stages/analysts/_common.py](../../src/agents/llm/stages/analysts/_common.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Shared LLM runner for Analyst Team specialists. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[run_specialist_llm](#fun-55e3a906bd)

<a id="fun-55e3a906bd"></a>

#### `run_specialist_llm`

- **ID / 行**：`FUN-55E3A906BD` / `L23`（源码见本单元概览）
- **签名 / 返回**：`run_specialist_llm(ctx: MarketContext, *, stage: str, agent: str, system: str, payload_fn: Callable[[MarketContext], dict[str, Any]], user_prefix: str)` → `tuple[AnalystReport | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_specialist_llm` and its owning unit.
- **依赖**：client_for_stage、json.dumps、parse_analyst_report、payload_fn、run_llm_stage
- **复杂度 / 风险**：分支 1；跨度 28 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-fcd3d48fde"></a>

### src/agents/llm/stages/analysts/fundamentals.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FCD3D48FDE |
| 源码 | [src/agents/llm/stages/analysts/fundamentals.py](../../src/agents/llm/stages/analysts/fundamentals.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM Fundamentals Analyst. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_fundamentals_analyst](#fun-039cd9925f)

<a id="fun-039cd9925f"></a>

#### `run_llm_fundamentals_analyst`

- **ID / 行**：`FUN-039CD9925F` / `L16`（源码见本单元概览）
- **签名 / 返回**：`run_llm_fundamentals_analyst(ctx: MarketContext)` → `tuple[AnalystReport | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_fundamentals_analyst` and its owning unit.
- **依赖**：run_specialist_llm
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="unit-25115c1d6f"></a>

### src/agents/llm/stages/analysts/news.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-25115C1D6F |
| 源码 | [src/agents/llm/stages/analysts/news.py](../../src/agents/llm/stages/analysts/news.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM News Analyst. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_news_analyst](#fun-4e10e953f7)

<a id="fun-4e10e953f7"></a>

#### `run_llm_news_analyst`

- **ID / 行**：`FUN-4E10E953F7` / `L20`（源码见本单元概览）
- **签名 / 返回**：`run_llm_news_analyst(ctx: MarketContext)` → `tuple[AnalystReport | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_news_analyst` and its owning unit.
- **依赖**：run_specialist_llm
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="unit-2bf1b61e7e"></a>

### src/agents/llm/stages/analysts/sentiment.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2BF1B61E7E |
| 源码 | [src/agents/llm/stages/analysts/sentiment.py](../../src/agents/llm/stages/analysts/sentiment.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM Sentiment Analyst. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_sentiment_analyst](#fun-417df23078)

<a id="fun-417df23078"></a>

#### `run_llm_sentiment_analyst`

- **ID / 行**：`FUN-417DF23078` / `L17`（源码见本单元概览）
- **签名 / 返回**：`run_llm_sentiment_analyst(ctx: MarketContext)` → `tuple[AnalystReport | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_sentiment_analyst` and its owning unit.
- **依赖**：run_specialist_llm
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="unit-a3445b9493"></a>

### src/agents/llm/stages/analysts/technical.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A3445B9493 |
| 源码 | [src/agents/llm/stages/analysts/technical.py](../../src/agents/llm/stages/analysts/technical.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM Technical Analyst. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_technical_analyst](#fun-c901472c03)

<a id="fun-c901472c03"></a>

#### `run_llm_technical_analyst`

- **ID / 行**：`FUN-C901472C03` / `L61`（源码见本单元概览）
- **签名 / 返回**：`run_llm_technical_analyst(ctx: MarketContext)` → `tuple[AnalystReport | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_technical_analyst` and its owning unit.
- **依赖**：run_specialist_llm
- **复杂度 / 风险**：分支 0；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py) · direct-dynamic

<a id="unit-2ccd7c4dcb"></a>

### src/agents/llm/stages/bearish.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2CCD7C4DCB |
| 源码 | [src/agents/llm/stages/bearish.py](../../src/agents/llm/stages/bearish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM bearish researcher. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_bearish](#fun-1d081c3bb3)

<a id="fun-1d081c3bb3"></a>

#### `run_llm_bearish`

- **ID / 行**：`FUN-1D081C3BB3` / `L34`（源码见本单元概览）
- **签名 / 返回**：`run_llm_bearish(ctx: MarketContext, team: AnalystTeam | None=None)` → `tuple[AgentEvidence | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_bearish` and its owning unit.
- **依赖**：analyst_evidence_ids、client_for_stage、evidence_registry、json.dumps、parse_agent_evidence、research_payload、run_llm_stage
- **复杂度 / 风险**：分支 3；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="unit-12bf07eb04"></a>

### src/agents/llm/stages/bullish.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-12BF07EB04 |
| 源码 | [src/agents/llm/stages/bullish.py](../../src/agents/llm/stages/bullish.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM bullish researcher. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_bullish](#fun-9efeb32d2f)

<a id="fun-9efeb32d2f"></a>

#### `run_llm_bullish`

- **ID / 行**：`FUN-9EFEB32D2F` / `L37`（源码见本单元概览）
- **签名 / 返回**：`run_llm_bullish(ctx: MarketContext, team: AnalystTeam | None=None)` → `tuple[AgentEvidence | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_bullish` and its owning unit.
- **依赖**：analyst_evidence_ids、client_for_stage、evidence_registry、json.dumps、parse_agent_evidence、research_payload、run_llm_stage
- **复杂度 / 风险**：分支 3；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py) · direct-dynamic

<a id="unit-3970799e39"></a>

### src/agents/llm/stages/debate.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3970799E39 |
| 源码 | [src/agents/llm/stages/debate.py](../../src/agents/llm/stages/debate.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM debate moderator. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_debate](#fun-59f17fb960)

<a id="fun-59f17fb960"></a>

#### `run_llm_debate`

- **ID / 行**：`FUN-59F17FB960` / `L29`（源码见本单元概览）
- **签名 / 返回**：`run_llm_debate(bullish: AgentEvidence, bearish: AgentEvidence, analyses, *, ctx: MarketContext | None=None, team: AnalystTeam | None=None)` → `tuple[ResearchDebate | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_debate` and its owning unit.
- **依赖**：client_for_stage、debate_payload、json.dumps、parse_research_debate、run_llm_stage
- **复杂度 / 风险**：分支 1；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py) · direct-dynamic

<a id="unit-4fbc2b73a8"></a>

### src/agents/llm/stages/levels.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4FBC2B73A8 |
| 源码 | [src/agents/llm/stages/levels.py](../../src/agents/llm/stages/levels.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM level proposer stage. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_level_proposer](#fun-cbb3a88b74)

<a id="fun-cbb3a88b74"></a>

#### `run_llm_level_proposer`

- **ID / 行**：`FUN-CBB3A88B74` / `L61`（源码见本单元概览）
- **签名 / 返回**：`run_llm_level_proposer(ctx: MarketContext, team: AnalystTeam, debate: ResearchDebate, rule_signals: list[object])` → `tuple[list[LevelProposal] | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_level_proposer` and its owning unit.
- **依赖**：client_for_stage、json.dumps、len、level_proposer_payload、log.info、log.warning、max、payload.get、run_llm_stage
- **复杂度 / 风险**：分支 2；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="unit-5ed826be60"></a>

### src/agents/llm/stages/manager.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-5ED826BE60 |
| 源码 | [src/agents/llm/stages/manager.py](../../src/agents/llm/stages/manager.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM portfolio manager stage. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_manager](#fun-af30a97dcf)

<a id="fun-af30a97dcf"></a>

#### `run_llm_manager`

- **ID / 行**：`FUN-AF30A97DCF` / `L27`（源码见本单元概览）
- **签名 / 返回**：`run_llm_manager(proposal: TransactionProposal, reviews: list[RiskReview])` → `tuple[ManagerDecision | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_manager` and its owning unit.
- **依赖**：client_for_stage、json.dumps、manager_payload、parse_manager_decision、run_llm_stage
- **复杂度 / 风险**：分支 1；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="unit-9038f74287"></a>

### src/agents/llm/stages/risk.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9038F74287 |
| 源码 | [src/agents/llm/stages/risk.py](../../src/agents/llm/stages/risk.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM risk review stage. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_risk](#fun-836a19ca04) · [run_llm_risk._parse](#fun-31f4ada410)

<a id="fun-836a19ca04"></a>

#### `run_llm_risk`

- **ID / 行**：`FUN-836A19CA04` / `L28`（源码见本单元概览）
- **签名 / 返回**：`run_llm_risk(proposal: TransactionProposal, signal_count: int, *, signals: list[Any] | None=None, current_price: float | None=None, data_as_of: dict[str, Any] | None=None)` → `tuple[list[RiskReview] | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_risk` and its owning unit.
- **依赖**：client_for_stage、data.get、float、json.dumps、max、min、parse_risk_reviews、risk_payload、run_llm_stage
- **复杂度 / 风险**：分支 2；跨度 43 行；medium
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-31f4ada410"></a>

#### `run_llm_risk._parse`

- **ID / 行**：`FUN-31F4ADA410` / `L46`（源码见本单元概览）
- **签名 / 返回**：`run_llm_risk._parse(data: dict)` → `list[RiskReview]`
- **职责**：As-built responsibility derived from `_parse` and its owning unit.
- **依赖**：data.get、float、max、min、parse_risk_reviews
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-a996419c04"></a>

### src/agents/llm/stages/trader.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A996419C04 |
| 源码 | [src/agents/llm/stages/trader.py](../../src/agents/llm/stages/trader.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | LLM trader stage. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) |
| 验证状态 | selected |

#### 函数导航

[run_llm_trader](#fun-ddd80e4bd9) · [run_llm_trader._parse](#fun-839ea81209)

<a id="fun-ddd80e4bd9"></a>

#### `run_llm_trader`

- **ID / 行**：`FUN-DDD80E4BD9` / `L28`（源码见本单元概览）
- **签名 / 返回**：`run_llm_trader(ctx: MarketContext, debate: ResearchDebate, signals: list[TradingSignal], team: AnalystTeam | None=None)` → `tuple[TransactionProposal | None, LLMStageTrace]`
- **职责**：As-built responsibility derived from `run_llm_trader` and its owning unit.
- **依赖**：client_for_stage、data.get、float、json.dumps、len、max、min、parse_transaction_proposal、run_llm_stage、trader_payload
- **复杂度 / 风险**：分支 2；跨度 39 行；high
- **测试 / 验证**：[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py) · direct-dynamic

<a id="fun-839ea81209"></a>

#### `run_llm_trader._parse`

- **ID / 行**：`FUN-839EA81209` / `L38`（源码见本单元概览）
- **签名 / 返回**：`run_llm_trader._parse(data: dict)` → `TransactionProposal`
- **职责**：As-built responsibility derived from `_parse` and its owning unit.
- **依赖**：data.get、float、len、max、min、parse_transaction_proposal
- **复杂度 / 风险**：分支 1；跨度 10 行；high
- **测试 / 验证**：— · static-and-component

<a id="unit-cc665640c2"></a>

### src/agents/manager.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-CC665640C2 |
| 源码 | [src/agents/manager.py](../../src/agents/manager.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Manager — final authorization based on risk reviews. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) |
| 验证状态 | selected |

#### 函数导航

[_scale_for_indices](#fun-8c2914e178) · [_evidence_confidence](#fun-a6411be7ce) · [run_manager](#fun-f7395a9fd5)

<a id="fun-8c2914e178"></a>

#### `_scale_for_indices`

- **ID / 行**：`FUN-8C2914E178` / `L8`（源码见本单元概览）
- **签名 / 返回**：`_scale_for_indices(reviews: list[RiskReview], indices: list[int])` → `float`
- **职责**：As-built responsibility derived from `_scale_for_indices` and its owning unit.
- **依赖**：min、selected.intersection、set
- **复杂度 / 风险**：分支 2；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a6411be7ce"></a>

#### `_evidence_confidence`

- **ID / 行**：`FUN-A6411BE7CE` / `L20`（源码见本单元概览）
- **签名 / 返回**：`_evidence_confidence(reviews: list[RiskReview], proposal: TransactionProposal, *, action: str)` → `float`
- **职责**：Derive manager confidence from how many risk profiles approved the proposal.
- **依赖**：get、max、min、round、sum
- **复杂度 / 风险**：分支 3；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f7395a9fd5"></a>

#### `run_manager`

- **ID / 行**：`FUN-F7395A9FD5` / `L38`（源码见本单元概览）
- **签名 / 返回**：`run_manager(proposal: TransactionProposal, reviews: list[RiskReview])` → `ManagerDecision`
- **职责**：As-built responsibility derived from `run_manager` and its owning unit.
- **依赖**：ManagerDecision、_evidence_confidence、_scale_for_indices、next
- **复杂度 / 风险**：分支 4；跨度 52 行；medium
- **测试 / 验证**：[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_manager_authorization.py](../../tests/unit/test_manager_authorization.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) · direct-dynamic

<a id="unit-c1468c2396"></a>

### src/agents/risk.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C1468C2396 |
| 源码 | [src/agents/risk.py](../../src/agents/risk.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Risk management team — aggressive / neutral / conservative reviews. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) |
| 验证状态 | selected |

#### 函数导航

[_review](#fun-d7ba82b894) · [run_risk_team](#fun-f364bcfeae)

<a id="fun-d7ba82b894"></a>

#### `_review`

- **ID / 行**：`FUN-D7BA82B894` / `L11`（源码见本单元概览）
- **签名 / 返回**：`_review(profile: RiskProfile, proposal: TransactionProposal, signal_count: int)` → `RiskReview`
- **职责**：As-built responsibility derived from `_review` and its owning unit.
- **依赖**：RiskReview、notes.append
- **复杂度 / 风险**：分支 6；跨度 47 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f364bcfeae"></a>

#### `run_risk_team`

- **ID / 行**：`FUN-F364BCFEAE` / `L60`（源码见本单元概览）
- **签名 / 返回**：`run_risk_team(proposal: TransactionProposal, signal_count: int, *, signals: list[Any] | None=None, current_price: float=0.0, data_as_of: dict[str, Any] | None=None, observation_mode: bool=False)` → `list[RiskReview]`
- **职责**：As-built responsibility derived from `run_risk_team` and its owning unit.
- **依赖**：_review、apply_risk_gates
- **复杂度 / 风险**：分支 1；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py)、[tests/unit/test_rule_chain_stability.py](../../tests/unit/test_rule_chain_stability.py) · direct-dynamic

<a id="unit-6340c2c541"></a>

### src/agents/trader.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6340C2C541 |
| 源码 | [src/agents/trader.py](../../src/agents/trader.py) |
| 架构组件 | ARC-AGENTS — 规则/LLM Agent 编排 |
| 职责 | Trader agent — synthesizes debate + structure into transaction proposal. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-ANA-002](./SWE.1-software-requirements.md#swr-ana-002)、[SWR-ANA-003](./SWE.1-software-requirements.md#swr-ana-003)、[SWR-AGT-001](./SWE.1-software-requirements.md#swr-agt-001)、[SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[run_trader_agent](#fun-fee6c661e8)

<a id="fun-fee6c661e8"></a>

#### `run_trader_agent`

- **ID / 行**：`FUN-FEE6C661E8` / `L17`（源码见本单元概览）
- **签名 / 返回**：`run_trader_agent(ctx: MarketContext, debate: ResearchDebate, signals: list[TradingSignal])` → `tuple[TransactionProposal, list[TradingSignal]]`
- **职责**：As-built responsibility derived from `run_trader_agent` and its owning unit.
- **依赖**：TransactionProposal、enumerate、getattr、rationale.append、sentiment.get、sentiment_score
- **复杂度 / 风险**：分支 10；跨度 93 行；high
- **测试 / 验证**：[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) · direct-dynamic

<a id="arc-llm"></a>

## ARC-LLM — LLM 传输、上下文和策略

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/llm/__init__.py](#unit-598812089b) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/analyst.py](#unit-f5cb9d3f8c) | 7 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/client.py](#unit-d7fd07af44) | 8 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/context.py](#unit-6c3fd6c2e5) | 6 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/format_io.py](#unit-deb0d517c6) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/narrative_output.py](#unit-fbf77b94fb) | 11 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/prompts.py](#unit-a605fcb3a9) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/router.py](#unit-6568b95afa) | 7 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/stage_policy.py](#unit-e488978a91) | 8 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-598812089b"></a>

### src/llm/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-598812089B |
| 源码 | [src/llm/__init__.py](../../src/llm/__init__.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | LLM analysis layer — optional natural-language report enhancement. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-f5cb9d3f8c"></a>

### src/llm/analyst.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F5CB9D3F8C |
| 源码 | [src/llm/analyst.py](../../src/llm/analyst.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | LLM analyst — optional narrative layer on top of rule-based pipeline. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py) |
| 验证状态 | selected |

#### 函数导航

[_error_result](#fun-2e761b537c) · [_disabled_result](#fun-7a3c5fbb90) · [_client_from_config](#fun-b472cd2d40) · [_parse_result](#fun-05d603b92f) · [validate_llm_payload](#fun-7722d6583b) · [run_llm_analysis](#fun-c0808d1fd3) · [apply_llm_to_report](#fun-307482df32)

<a id="fun-2e761b537c"></a>

#### `_error_result`

- **ID / 行**：`FUN-2E761B537C` / `L32`（源码见本单元概览）
- **签名 / 返回**：`_error_result(report: dict[str, Any], error: str)` → `LLMAnalysis`
- **职责**：As-built responsibility derived from `_error_result` and its owning unit.
- **依赖**：LLMAnalysis、deepcopy、report.get、sections.items
- **复杂度 / 风险**：分支 1；跨度 15 行；low
- **测试 / 验证**：[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py) · direct-dynamic

<a id="fun-7a3c5fbb90"></a>

#### `_disabled_result`

- **ID / 行**：`FUN-7A3C5FBB90` / `L49`（源码见本单元概览）
- **签名 / 返回**：`_disabled_result(reason: str='LLM 未启用')` → `LLMAnalysis`
- **职责**：As-built responsibility derived from `_disabled_result` and its owning unit.
- **依赖**：LLMAnalysis
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b472cd2d40"></a>

#### `_client_from_config`

- **ID / 行**：`FUN-B472CD2D40` / `L53`（源码见本单元概览）
- **签名 / 返回**：`_client_from_config()` → `LLMClient`
- **职责**：As-built responsibility derived from `_client_from_config` and its owning unit.
- **异常 / 副作用 / 并发**：LLMClientError / none-detected / caller-thread
- **依赖**：LLMClientError、client_for_stage、llm_configured
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-05d603b92f"></a>

#### `_parse_result`

- **ID / 行**：`FUN-05D603B92F` / `L59`（源码见本单元概览）
- **签名 / 返回**：`_parse_result(data: dict[str, Any], *, model: str, provider: str)` → `LLMAnalysis`
- **职责**：As-built responsibility derived from `_parse_result` and its owning unit.
- **依赖**：LLMAnalysis、data.get、float、isinstance、json.dumps、max、min、str、strip
- **复杂度 / 风险**：分支 3；跨度 28 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7722d6583b"></a>

#### `validate_llm_payload`

- **ID / 行**：`FUN-7722D6583B` / `L89`（源码见本单元概览）
- **签名 / 返回**：`validate_llm_payload(data: dict[str, Any], report: dict[str, Any], *, facts: dict[str, Any] | None=None, mode: str | None=None, threshold: float | None=None, model: str | None=None, provider: str | None=None)` → `LLMAnalysis`
- **职责**：Validate parsed LLM JSON against a report without calling the API.
- **依赖**：_parse_result、build_narrative_facts_for_llm、data.get、field_reasons.items、iter、next、rejected.values、report.get、setattr、validate_and_merge_llm_sections、validate_llm_top_level_fields
- **复杂度 / 风险**：分支 4；跨度 39 行；medium
- **测试 / 验证**：[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py) · direct-dynamic

<a id="fun-c0808d1fd3"></a>

#### `run_llm_analysis`

- **ID / 行**：`FUN-C0808D1FD3` / `L130`（源码见本单元概览）
- **签名 / 返回**：`run_llm_analysis(ctx: MarketContext, debate: ResearchDebate, decision: ManagerDecision, report: dict[str, Any])` → `LLMAnalysis`
- **职责**：Call LLM to produce narrative analysis from structured pipeline output.
- **依赖**：_client_from_config、_disabled_result、_error_result、build_llm_context、build_messages、build_narrative_facts_for_llm、context.get、items、len、llm_narrative_enabled、log.exception、log.info、log.warning、report.setdefault、result.top_level_audit.get、run_llm_stage、str、validate_llm_payload
- **复杂度 / 风险**：分支 6；跨度 58 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-307482df32"></a>

#### `apply_llm_to_report`

- **ID / 行**：`FUN-307482DF32` / `L190`（源码见本单元概览）
- **签名 / 返回**：`apply_llm_to_report(report: dict[str, Any], llm: LLMAnalysis)` → `None`
- **职责**：Attach LLM output to report; optionally enhance rule-based conclusion.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：conclusion.get、get、getattr、llm.action_plan.replace、llm.to_dict、report.get、report.setdefault、setdefault、top_audit.get
- **复杂度 / 风险**：分支 12；跨度 44 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py) · direct-dynamic

<a id="unit-d7fd07af44"></a>

### src/llm/client.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D7FD07AF44 |
| 源码 | [src/llm/client.py](../../src/llm/client.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | OpenAI-compatible chat completion client (requests-based). |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../tests/regression/test_aspice_assets.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py)、[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_pipeline_progress_live.py](../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py) |
| 验证状态 | selected |

#### 函数导航

[LLMClient.__init__](#fun-184ed552df) · [LLMClient.timeout](#fun-b3cf019763) · [LLMClient._request_timeout](#fun-6281d0133f) · [LLMClient._headers](#fun-870c1d436c) · [LLMClient._parse_sse_line](#fun-c5e317f9c8) · [LLMClient.chat_stream](#fun-b2c894bd12) · [LLMClient.chat](#fun-feaf06c7c1) · [LLMClient.chat_json](#fun-cc950a51e1)

<a id="fun-184ed552df"></a>

#### `LLMClient.__init__`

- **ID / 行**：`FUN-184ED552DF` / `L24`（源码见本单元概览）
- **签名 / 返回**：`LLMClient.__init__(self, *, api_key: str, base_url: str, model: str, timeout: int | float | None=None, connect_timeout: float | None=None, read_timeout: float | None=None)` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **依赖**：base_url.rstrip、float、min
- **复杂度 / 风险**：分支 4；跨度 28 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-b3cf019763"></a>

#### `LLMClient.timeout`

- **ID / 行**：`FUN-B3CF019763` / `L54`（源码见本单元概览）
- **签名 / 返回**：`LLMClient.timeout(self)` → `float`
- **职责**：Legacy alias — returns read/chunk-idle timeout.
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/regression/test_aspice_assets.py](../../tests/regression/test_aspice_assets.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_http_helpers.py](../../tests/unit/test_http_helpers.py)、[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_pipeline_progress_live.py](../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py) · direct-dynamic

<a id="fun-6281d0133f"></a>

#### `LLMClient._request_timeout`

- **ID / 行**：`FUN-6281D0133F` / `L58`（源码见本单元概览）
- **签名 / 返回**：`LLMClient._request_timeout(self)` → `tuple[float, float]`
- **职责**：As-built responsibility derived from `_request_timeout` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py) · direct-dynamic

<a id="fun-870c1d436c"></a>

#### `LLMClient._headers`

- **ID / 行**：`FUN-870C1D436C` / `L61`（源码见本单元概览）
- **签名 / 返回**：`LLMClient._headers(self)` → `dict[str, str]`
- **职责**：As-built responsibility derived from `_headers` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c5e317f9c8"></a>

#### `LLMClient._parse_sse_line`

- **ID / 行**：`FUN-C5E317F9C8` / `L67`（源码见本单元概览）
- **签名 / 返回**：`LLMClient._parse_sse_line(self, line: str)` → `str | None`
- **职责**：As-built responsibility derived from `_parse_sse_line` and its owning unit.
- **依赖**：delta.get、get、isinstance、json.loads、line.startswith、line.strip、strip
- **复杂度 / 风险**：分支 5；跨度 19 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b2c894bd12"></a>

#### `LLMClient.chat_stream`

- **ID / 行**：`FUN-B2C894BD12` / `L87`（源码见本单元概览）
- **签名 / 返回**：`LLMClient.chat_stream(self, messages: list[dict[str, str]], *, temperature: float=0.3, response_format: dict[str, str] | None=None)` → `Iterator[str]`
- **职责**：Yield text chunks from an OpenAI-compatible SSE stream.
- **异常 / 副作用 / 并发**：LLMClientError / external-io / caller-thread
- **依赖**：LLMClientError、isinstance、log.debug、raw.decode、requests.post、resp.iter_lines、self._headers、self._parse_sse_line、self._request_timeout、str
- **复杂度 / 风险**：分支 8；跨度 57 行；high
- **测试 / 验证**：[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_transport.py](../../tests/unit/test_llm_transport.py) · direct-dynamic

<a id="fun-feaf06c7c1"></a>

#### `LLMClient.chat`

- **ID / 行**：`FUN-FEAF06C7C1` / `L145`（源码见本单元概览）
- **签名 / 返回**：`LLMClient.chat(self, messages: list[dict[str, str]], *, temperature: float=0.3, response_format: dict[str, str] | None=None)` → `str`
- **职责**：As-built responsibility derived from `chat` and its owning unit.
- **异常 / 副作用 / 并发**：LLMClientError / none-detected / caller-thread
- **依赖**：LLMClientError、join、list、self.chat_stream、strip
- **复杂度 / 风险**：分支 1；跨度 18 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-cc950a51e1"></a>

#### `LLMClient.chat_json`

- **ID / 行**：`FUN-CC950A51E1` / `L164`（源码见本单元概览）
- **签名 / 返回**：`LLMClient.chat_json(self, messages: list[dict[str, str]], *, temperature: float=0.2)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `chat_json` and its owning unit.
- **异常 / 副作用 / 并发**：LLMClientError / none-detected / caller-thread
- **依赖**：LLMClientError、isinstance、json.loads、self.chat
- **复杂度 / 风险**：分支 2；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-6c3fd6c2e5"></a>

### src/llm/context.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6C3FD6C2E5 |
| 源码 | [src/llm/context.py](../../src/llm/context.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | Serialize pipeline state into a compact narrative-only LLM context payload. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_llm_context_compact.py](../../tests/unit/test_llm_context_compact.py)、[tests/unit/test_llm_context_fact_refs.py](../../tests/unit/test_llm_context_fact_refs.py) |
| 验证状态 | selected |

#### 函数导航

[_slim_external](#fun-a5b3114ea5) · [_slim_narrative_technical_context](#fun-311efc4821) · [_levels_as_fact_refs](#fun-8860117010) · [_slim_narrative_facts](#fun-8566c1a15c) · [estimate_payload_size](#fun-b49d34199c) · [build_llm_context](#fun-4d78ddfbc7)

<a id="fun-a5b3114ea5"></a>

#### `_slim_external`

- **ID / 行**：`FUN-A5B3114EA5` / `L28`（源码见本单元概览）
- **签名 / 返回**：`_slim_external(external: dict[str, Any], derived: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_slim_external` and its owning unit.
- **依赖**：derived.get、external.get
- **复杂度 / 风险**：分支 2；跨度 15 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-311efc4821"></a>

#### `_slim_narrative_technical_context`

- **ID / 行**：`FUN-311EFC4821` / `L45`（源码见本单元概览）
- **签名 / 返回**：`_slim_narrative_technical_context(ctx: MarketContext)` → `dict[str, Any]`
- **职责**：Quality + S/R labels only — indicator raw numbers live in fact_registry.
- **依赖**：build_technical_context、full.get、isinstance
- **复杂度 / 风险**：分支 2；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8860117010"></a>

#### `_levels_as_fact_refs`

- **ID / 行**：`FUN-8860117010` / `L61`（源码见本单元概览）
- **签名 / 返回**：`_levels_as_fact_refs(levels: list[dict[str, Any]], registry: dict[str, Any])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_levels_as_fact_refs` and its owning unit.
- **依赖**：fact_lookup、float、out.append、row.get
- **复杂度 / 风险**：分支 3；跨度 15 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8566c1a15c"></a>

#### `_slim_narrative_facts`

- **ID / 行**：`FUN-8566C1A15C` / `L78`（源码见本单元概览）
- **签名 / 返回**：`_slim_narrative_facts(facts: dict[str, Any], registry: dict[str, Any])` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_slim_narrative_facts` and its owning unit.
- **依赖**：_levels_as_fact_refs、dict、slim.get
- **复杂度 / 风险**：分支 2；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b49d34199c"></a>

#### `estimate_payload_size`

- **ID / 行**：`FUN-B49D34199C` / `L89`（源码见本单元概览）
- **签名 / 返回**：`estimate_payload_size(payload: dict[str, Any])` → `dict[str, int]`
- **职责**：As-built responsibility derived from `estimate_payload_size` and its owning unit.
- **依赖**：json.dumps、len、round
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_llm_context_compact.py](../../tests/unit/test_llm_context_compact.py) · direct-dynamic

<a id="fun-4d78ddfbc7"></a>

#### `build_llm_context`

- **ID / 行**：`FUN-4D78DDFBC7` / `L95`（源码见本单元概览）
- **签名 / 返回**：`build_llm_context(ctx: MarketContext, debate: ResearchDebate, decision: ManagerDecision, report: dict[str, Any])` → `dict[str, Any]`
- **职责**：Structured facts for the LLM — cite fact_id; no duplicate raw price tables.
- **依赖**：_slim_external、_slim_narrative_facts、_slim_narrative_technical_context、build_narrative_facts_for_llm、compact_fact_index、ctx.external.to_dict、decision.to_dict、estimate_payload_size、fact_ids_for_signal、get、registry.get、report.get、s.get
- **复杂度 / 风险**：分支 1；跨度 83 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_llm_context_compact.py](../../tests/unit/test_llm_context_compact.py)、[tests/unit/test_llm_context_fact_refs.py](../../tests/unit/test_llm_context_fact_refs.py) · direct-dynamic

<a id="unit-deb0d517c6"></a>

### src/llm/format_io.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DEB0D517C6 |
| 源码 | [src/llm/format_io.py](../../src/llm/format_io.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | Format LLM messages for display. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[format_llm_output](#fun-9200a4bf77) · [format_messages](#fun-0d23896651) · [messages_to_dict](#fun-c67d97c1fe)

<a id="fun-9200a4bf77"></a>

#### `format_llm_output`

- **ID / 行**：`FUN-9200A4BF77` / `L9`（源码见本单元概览）
- **签名 / 返回**：`format_llm_output(text: str)` → `str`
- **职责**：Pretty-print JSON output; preserve UTF-8 Chinese.
- **依赖**：json.dumps、json.loads、text.strip
- **复杂度 / 风险**：分支 2；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0d23896651"></a>

#### `format_messages`

- **ID / 行**：`FUN-0D23896651` / `L20`（源码见本单元概览）
- **签名 / 返回**：`format_messages(messages: list[dict[str, str]], *, max_chars: int=12000)` → `str`
- **职责**：As-built responsibility derived from `format_messages` and its owning unit.
- **依赖**：join、len、lines.append、msg.get、strip
- **复杂度 / 风险**：分支 2；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c67d97c1fe"></a>

#### `messages_to_dict`

- **ID / 行**：`FUN-C67D97C1FE` / `L32`（源码见本单元概览）
- **签名 / 返回**：`messages_to_dict(messages: list[dict[str, str]])` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `messages_to_dict` and its owning unit.
- **依赖**：m.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-fbf77b94fb"></a>

### src/llm/narrative_output.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FBF77B94FB |
| 源码 | [src/llm/narrative_output.py](../../src/llm/narrative_output.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | Turn LLM JSON responses into readable Chinese summaries. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_narrative_output.py](../../tests/unit/test_narrative_output.py) |
| 验证状态 | selected |

#### 函数导航

[_try_parse_json](#fun-5605d6120b) · [_pct](#fun-8d01609c7d) · [_lines_to_html](#fun-80154bbc17) · [_fmt_evidence](#fun-2145bad99e) · [_fmt_debate](#fun-1e02af4dd5) · [_fmt_narrative](#fun-76a10bccd6) · [_fmt_generic](#fun-ac5a907908) · [_fmt_analyst_report](#fun-6dab1399aa) · [_fmt_analyst_team](#fun-ebf3493e57) · [_fmt_context](#fun-8d05235fca) · [format_llm_narrative](#fun-3b28d5a15c)

<a id="fun-5605d6120b"></a>

#### `_try_parse_json`

- **ID / 行**：`FUN-5605D6120B` / `L19`（源码见本单元概览）
- **签名 / 返回**：`_try_parse_json(text: str)` → `dict[str, Any] | None`
- **职责**：As-built responsibility derived from `_try_parse_json` and its owning unit.
- **依赖**：attempts.append、isinstance、json.loads、re.sub、text.find、text.rfind、text.strip
- **复杂度 / 风险**：分支 7；跨度 22 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8d01609c7d"></a>

#### `_pct`

- **ID / 行**：`FUN-8D01609C7D` / `L43`（源码见本单元概览）
- **签名 / 返回**：`_pct(v: Any)` → `str`
- **职责**：As-built responsibility derived from `_pct` and its owning unit.
- **依赖**：float、max、min
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-80154bbc17"></a>

#### `_lines_to_html`

- **ID / 行**：`FUN-80154BBC17` / `L51`（源码见本单元概览）
- **签名 / 返回**：`_lines_to_html(lines: list[str])` → `str`
- **职责**：As-built responsibility derived from `_lines_to_html` and its owning unit.
- **依赖**：escape、join
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2145bad99e"></a>

#### `_fmt_evidence`

- **ID / 行**：`FUN-2145BAD99E` / `L57`（源码见本单元概览）
- **签名 / 返回**：`_fmt_evidence(direction: str, data: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_evidence` and its owning unit.
- **依赖**：_CATEGORY_CN.get、_lines_to_html、_pct、bullets.append、data.get、escape、isinstance、join、parts.append、row.get、str、strip
- **复杂度 / 风险**：分支 7；跨度 25 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-1e02af4dd5"></a>

#### `_fmt_debate`

- **ID / 行**：`FUN-1E02AF4DD5` / `L84`（源码见本单元概览）
- **签名 / 返回**：`_fmt_debate(data: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_debate` and its owning unit.
- **依赖**：_BIAS_CN.get、_lines_to_html、_pct、data.get、escape、isinstance、join、lower、parts.append、str、strip
- **复杂度 / 风险**：分支 3；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-76a10bccd6"></a>

#### `_fmt_narrative`

- **ID / 行**：`FUN-76A10BCCD6` / `L100`（源码见本单元概览）
- **签名 / 返回**：`_fmt_narrative(data: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_narrative` and its owning unit.
- **依赖**：_lines_to_html、_pct、data.get、escape、isinstance、join、ln.strip、parts.append、str、strip、v.splitlines
- **复杂度 / 风险**：分支 7；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ac5a907908"></a>

#### `_fmt_generic`

- **ID / 行**：`FUN-AC5A907908` / `L122`（源码见本单元概览）
- **签名 / 返回**：`_fmt_generic(data: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_generic` and its owning unit.
- **依赖**：_lines_to_html、data.items、isinstance、lines.append、str、strip
- **复杂度 / 风险**：分支 4；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6dab1399aa"></a>

#### `_fmt_analyst_report`

- **ID / 行**：`FUN-6DAB1399AA` / `L135`（源码见本单元概览）
- **签名 / 返回**：`_fmt_analyst_report(title: str, data: dict[str, Any])` → `str`
- **职责**：Single AnalystReport JSON (technical / fundamentals / news / sentiment).
- **依赖**：_BIAS_CN.get、_CATEGORY_CN.get、_lines_to_html、_pct、bullets.append、data.get、escape、isinstance、join、lower、parts.append、row.get、str、strip
- **复杂度 / 风险**：分支 7；跨度 27 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ebf3493e57"></a>

#### `_fmt_analyst_team`

- **ID / 行**：`FUN-EBF3493E57` / `L172`（源码见本单元概览）
- **签名 / 返回**：`_fmt_analyst_team(data: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_analyst_team` and its owning unit.
- **依赖**：_BIAS_CN.get、_pct、data.get、escape、isinstance、join、labels.items、len、lower、parts.append、report.get、str、strip
- **复杂度 / 风险**：分支 4；跨度 22 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8d05235fca"></a>

#### `_fmt_context`

- **ID / 行**：`FUN-8D05235FCA` / `L196`（源码见本单元概览）
- **签名 / 返回**：`_fmt_context(data: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_context` and its owning unit.
- **依赖**：data.get、escape、ext.get、int、isinstance、join、len、p.get、parts.append、str、strip
- **复杂度 / 风险**：分支 6；跨度 43 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3b28d5a15c"></a>

#### `format_llm_narrative`

- **ID / 行**：`FUN-3B28D5A15C` / `L241`（源码见本单元概览）
- **签名 / 返回**：`format_llm_narrative(stage: str, raw: str)` → `str`
- **职责**：Return HTML for the human-readable summary box.
- **依赖**：_fmt_analyst_report、_fmt_analyst_team、_fmt_context、_fmt_debate、_fmt_evidence、_fmt_generic、_fmt_narrative、_try_parse_json、escape、len、raw.strip
- **复杂度 / 风险**：分支 10；跨度 29 行；medium
- **测试 / 验证**：[tests/unit/test_narrative_output.py](../../tests/unit/test_narrative_output.py) · direct-dynamic

<a id="unit-a605fcb3a9"></a>

### src/llm/prompts.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A605FCB3A9 |
| 源码 | [src/llm/prompts.py](../../src/llm/prompts.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | Prompt templates for XAUUSD institutional analysis. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[_observation_hint](#fun-ec14c06c57) · [build_messages](#fun-b5e78a9a6d)

<a id="fun-ec14c06c57"></a>

#### `_observation_hint`

- **ID / 行**：`FUN-EC14C06C57` / `L63`（源码见本单元概览）
- **签名 / 返回**：`_observation_hint(context: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_observation_hint` and its owning unit.
- **依赖**：context.get
- **复杂度 / 风险**：分支 1；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b5e78a9a6d"></a>

#### `build_messages`

- **ID / 行**：`FUN-B5E78A9A6D` / `L74`（源码见本单元概览）
- **签名 / 返回**：`build_messages(context: dict[str, Any])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `build_messages` and its owning unit.
- **依赖**：_observation_hint、json.dumps
- **复杂度 / 风险**：分支 0；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-6568b95afa"></a>

### src/llm/router.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6568B95AFA |
| 源码 | [src/llm/router.py](../../src/llm/router.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | Model routing for agent stages. |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py) |
| 验证状态 | selected |

#### 函数导航

[client_for_model](#fun-1b26737be4) · [get_fast_client](#fun-c1648afe95) · [get_strong_client](#fun-b6cefe1540) · [get_debate_client](#fun-99cb06f377) · [client_for_stage](#fun-4719de86ff) · [routing_meta](#fun-dc9786297e) · [llm_configured](#fun-32ab5acbe0)

<a id="fun-1b26737be4"></a>

#### `client_for_model`

- **ID / 行**：`FUN-1B26737BE4` / `L19`（源码见本单元概览）
- **签名 / 返回**：`client_for_model(model: str)` → `LLMClient`
- **职责**：Build an OpenAI-compatible client using app timeout settings.
- **依赖**：LLMClient
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c1648afe95"></a>

#### `get_fast_client`

- **ID / 行**：`FUN-C1648AFE95` / `L30`（源码见本单元概览）
- **签名 / 返回**：`get_fast_client()` → `LLMClient`
- **职责**：As-built responsibility derived from `get_fast_client` and its owning unit.
- **依赖**：client_for_model
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py) · direct-dynamic

<a id="fun-b6cefe1540"></a>

#### `get_strong_client`

- **ID / 行**：`FUN-B6CEFE1540` / `L34`（源码见本单元概览）
- **签名 / 返回**：`get_strong_client()` → `LLMClient`
- **职责**：As-built responsibility derived from `get_strong_client` and its owning unit.
- **依赖**：client_for_model
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py) · direct-dynamic

<a id="fun-99cb06f377"></a>

#### `get_debate_client`

- **ID / 行**：`FUN-99CB06F377` / `L38`（源码见本单元概览）
- **签名 / 返回**：`get_debate_client()` → `LLMClient`
- **职责**：Debate moderator: STRONG by default; FAST when LLM_DEBATE_USE_FAST=true.
- **依赖**：get_fast_client、get_strong_client
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py) · direct-dynamic

<a id="fun-4719de86ff"></a>

#### `client_for_stage`

- **ID / 行**：`FUN-4719DE86FF` / `L45`（源码见本单元概览）
- **签名 / 返回**：`client_for_stage(stage: str)` → `LLMClient`
- **职责**：Resolve client from the auditable stage policy table (Issue #37).
- **依赖**：client_for_model、get_debate_client、get_fast_client、get_stage_policy、get_strong_client
- **复杂度 / 风险**：分支 3；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-dc9786297e"></a>

#### `routing_meta`

- **ID / 行**：`FUN-DC9786297E` / `L57`（源码见本单元概览）
- **签名 / 返回**：`routing_meta()` → `dict`
- **职责**：Archive-friendly snapshot of FAST/STRONG/REPORT strategy.
- **依赖**：build_routing_strategy
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-32ab5acbe0"></a>

#### `llm_configured`

- **ID / 行**：`FUN-32AB5ACBE0` / `L62`（源码见本单元概览）
- **签名 / 返回**：`llm_configured()` → `bool`
- **职责**：As-built responsibility derived from `llm_configured` and its owning unit.
- **依赖**：bool
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-e488978a91"></a>

### src/llm/stage_policy.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E488978A91 |
| 源码 | [src/llm/stage_policy.py](../../src/llm/stage_policy.py) |
| 架构组件 | ARC-LLM — LLM 传输、上下文和策略 |
| 职责 | Auditable per-stage LLM routing, attempt budget, and input size policy (Issue #37). |
| 关联需求 | [SWR-LLM-001](./SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](./SWE.1-software-requirements.md#swr-llm-002)、[SWR-LLM-003](./SWE.1-software-requirements.md#swr-llm-003)、[SWR-CFG-001](./SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](./SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 8 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

[StagePolicy.to_dict](#fun-8a092a53c7) · [_default_attempts](#fun-16718e4e98) · [_policies](#fun-500b8f3420) · [get_stage_policy](#fun-1d1021888e) · [estimate_messages_size](#fun-931519418f) · [estimate_text_size](#fun-288812bac3) · [apply_input_budget](#fun-639af5aafb) · [build_routing_strategy](#fun-e3b03c5e15)

<a id="fun-8a092a53c7"></a>

#### `StagePolicy.to_dict`

- **ID / 行**：`FUN-8A092A53C7` / `L39`（源码见本单元概览）
- **签名 / 返回**：`StagePolicy.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-16718e4e98"></a>

#### `_default_attempts`

- **ID / 行**：`FUN-16718E4E98` / `L43`（源码见本单元概览）
- **签名 / 返回**：`_default_attempts()` → `int`
- **职责**：Unified upstream budget: 1 + LLM_MAX_RETRIES (capped 1..6).
- **依赖**：int、max、min
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-500b8f3420"></a>

#### `_policies`

- **ID / 行**：`FUN-500B8F3420` / `L48`（源码见本单元概览）
- **签名 / 返回**：`_policies()` → `dict[str, StagePolicy]`
- **职责**：As-built responsibility derived from `_policies` and its owning unit.
- **依赖**：StagePolicy、_default_attempts、int
- **复杂度 / 风险**：分支 0；跨度 41 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-1d1021888e"></a>

#### `get_stage_policy`

- **ID / 行**：`FUN-1D1021888E` / `L91`（源码见本单元概览）
- **签名 / 返回**：`get_stage_policy(stage: str)` → `StagePolicy`
- **职责**：As-built responsibility derived from `get_stage_policy` and its owning unit.
- **依赖**：StagePolicy、_default_attempts、_policies、int
- **复杂度 / 风险**：分支 1；跨度 14 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_llm_client_timeouts.py](../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) · direct-dynamic

<a id="fun-931519418f"></a>

#### `estimate_messages_size`

- **ID / 行**：`FUN-931519418F` / `L107`（源码见本单元概览）
- **签名 / 返回**：`estimate_messages_size(messages: list[dict[str, str]])` → `dict[str, int]`
- **职责**：As-built responsibility derived from `estimate_messages_size` and its owning unit.
- **依赖**：int、len、m.get、round、str、sum
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-288812bac3"></a>

#### `estimate_text_size`

- **ID / 行**：`FUN-288812BAC3` / `L115`（源码见本单元概览）
- **签名 / 返回**：`estimate_text_size(text: str)` → `dict[str, int]`
- **职责**：As-built responsibility derived from `estimate_text_size` and its owning unit.
- **依赖**：int、len、round
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-639af5aafb"></a>

#### `apply_input_budget`

- **ID / 行**：`FUN-639AF5AAFB` / `L123`（源码见本单元概览）
- **签名 / 返回**：`apply_input_budget(messages: list[dict[str, str]], policy: StagePolicy)` → `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]`
- **职责**：Enforce soft/hard input budgets without silently dropping auth facts.
- **依赖**：dict、enumerate、estimate_messages_size、get、len、list、m.get、max、meta.update、range、str
- **复杂度 / 风险**：分支 5；跨度 54 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) · direct-dynamic

<a id="fun-e3b03c5e15"></a>

#### `build_routing_strategy`

- **ID / 行**：`FUN-E3B03C5E15` / `L179`（源码见本单元概览）
- **签名 / 返回**：`build_routing_strategy()` → `dict[str, Any]`
- **职责**：Explicit FAST/STRONG/REPORT layering status for archive / Runtime Ledger.
- **依赖**：_policies、items、p.to_dict
- **复杂度 / 风险**：分支 1；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py) · direct-dynamic

<a id="arc-run"></a>

## ARC-RUN — 运行上下文与归档

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/run/__init__.py](#unit-3d26d1ec62) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/__init__.py](#unit-6c61c7bbf5) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/compat.py](#unit-2f300feed2) | 9 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/completion.py](#unit-af0b99f0b7) | 3 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/index.py](#unit-969bf3943a) | 7 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/prune.py](#unit-038535558b) | 2 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/schema.py](#unit-ea2375efd1) | 5 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/store.py](#unit-d3d34bc712) | 40 | 15 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/archive/transfer.py](#unit-3365be69b6) | 2 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/config.py](#unit-e124606847) | 11 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/context.py](#unit-8a8bc190aa) | 6 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/run/pipeline_run.py](#unit-7df4993ab3) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-3d26d1ec62"></a>

### src/run/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3D26D1EC62 |
| 源码 | [src/run/__init__.py](../../src/run/__init__.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Run lifecycle — config, context, and archive replay. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-6c61c7bbf5"></a>

### src/run/archive/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6C61C7BBF5 |
| 源码 | [src/run/archive/__init__.py](../../src/run/archive/__init__.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Run archive — persist and replay pipeline bundles. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-2f300feed2"></a>

### src/run/archive/compat.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2F300FEED2 |
| 源码 | [src/run/archive/compat.py](../../src/run/archive/compat.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Compatibility layer — inspect, migrate, and normalize archived pipeline runs. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 9 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) |
| 验证状态 | selected |

#### 函数导航

[_read_json](#fun-1bfdad92bb) · [synthesize_manifest_from_legacy](#fun-9b86f7a9e8) · [load_manifest](#fun-4abec90c24) · [inspect_archive](#fun-8186a770f5) · [normalize_report](#fun-6792cfea90) · [migrate_fetch_payload](#fun-e54bdf4478) · [migrate_analyses_payload](#fun-47ef0675a6) · [migrate_frame_payload](#fun-8a37d9c11c) · [upgrade_manifest_if_needed](#fun-5bc6d37ce9)

<a id="fun-1bfdad92bb"></a>

#### `_read_json`

- **ID / 行**：`FUN-1BFDAD92BB` / `L37`（源码见本单元概览）
- **签名 / 返回**：`_read_json(path: Path)` → `Any`
- **职责**：As-built responsibility derived from `_read_json` and its owning unit.
- **依赖**：json.loads、path.read_text
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9b86f7a9e8"></a>

#### `synthesize_manifest_from_legacy`

- **ID / 行**：`FUN-9B86F7A9E8` / `L41`（源码见本单元概览）
- **签名 / 返回**：`synthesize_manifest_from_legacy(run_id: str, directory: Path)` → `dict[str, Any]`
- **职责**：Build a v2 manifest from pre-manifest archives (schema v1 folders).
- **依赖**：_read_json、build_manifest、int、isinstance、meta.get、meta_path.is_file、str
- **复杂度 / 风险**：分支 2；跨度 19 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="fun-4abec90c24"></a>

#### `load_manifest`

- **ID / 行**：`FUN-4ABEC90C24` / `L62`（源码见本单元概览）
- **签名 / 返回**：`load_manifest(run_id: str, directory: Path)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `load_manifest` and its owning unit.
- **异常 / 副作用 / 并发**：FileNotFoundError;ValueError / none-detected / caller-thread
- **依赖**：FileNotFoundError、ValueError、_read_json、is_file、isinstance、log.info、manifest.setdefault、manifest_path.is_file、synthesize_manifest_from_legacy
- **复杂度 / 风险**：分支 3；跨度 12 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8186a770f5"></a>

#### `inspect_archive`

- **ID / 行**：`FUN-8186A770F5` / `L76`（源码见本单元概览）
- **签名 / 返回**：`inspect_archive(run_id: str, directory: Path)` → `ArchiveInspection`
- **职责**：As-built responsibility derived from `inspect_archive` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：ArchiveInspection、_read_json、analyses_path.is_file、any、artifacts.get、enriched_dir.glob、enriched_dir.is_dir、errors.append、fetch_path.is_file、generation_step_statuses、get、int、is_file、isinstance、load_manifest、manifest.get、pipeline_replay_errors、replay.get、report_path.is_file、str
- **复杂度 / 风险**：分支 22；跨度 108 行；high
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="fun-6792cfea90"></a>

#### `normalize_report`

- **ID / 行**：`FUN-6792CFEA90` / `L186`（源码见本单元概览）
- **签名 / 返回**：`normalize_report(report: Any, *, contract_version: int=REPORT_CONTRACT_VERSION)` → `tuple[dict[str, Any], list[str]]`
- **职责**：Fill missing top-level report keys so UI code survives schema drift.
- **依赖**：REPORT_TOP_LEVEL_DEFAULTS.items、callable、default、dict、isinstance、meta.setdefault、normalized.get、normalized.setdefault、sections.get、warnings.append
- **复杂度 / 风险**：分支 9；跨度 38 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="fun-e54bdf4478"></a>

#### `migrate_fetch_payload`

- **ID / 行**：`FUN-E54BDF4478` / `L226`（源码见本单元概览）
- **签名 / 返回**：`migrate_fetch_payload(raw: Any)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `migrate_fetch_payload` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、isinstance、log.warning、unwrap_artifact
- **复杂度 / 风险**：分支 3；跨度 10 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="fun-47ef0675a6"></a>

#### `migrate_analyses_payload`

- **ID / 行**：`FUN-47EF0675A6` / `L238`（源码见本单元概览）
- **签名 / 返回**：`migrate_analyses_payload(raw: Any)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `migrate_analyses_payload` and its owning unit.
- **依赖**：isinstance、log.warning、unwrap_artifact
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8a37d9c11c"></a>

#### `migrate_frame_payload`

- **ID / 行**：`FUN-8A37D9C11C` / `L247`（源码见本单元概览）
- **签名 / 返回**：`migrate_frame_payload(raw: Any)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `migrate_frame_payload` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、isinstance、log.warning、unwrap_artifact
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5bc6d37ce9"></a>

#### `upgrade_manifest_if_needed`

- **ID / 行**：`FUN-5BC6D37CE9` / `L256`（源码见本单元概览）
- **签名 / 返回**：`upgrade_manifest_if_needed(manifest: dict[str, Any], run_id: str, directory: Path)` → `dict[str, Any]`
- **职责**：Persist synthesized/upgraded manifest so future reads skip legacy detection.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：dict、int、json.dumps、log.info、manifest.get、path.is_file、path.write_text、upgraded.get
- **复杂度 / 风险**：分支 3；跨度 19 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="unit-af0b99f0b7"></a>

### src/run/archive/completion.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-AF0B99F0B7 |
| 源码 | [src/run/archive/completion.py](../../src/run/archive/completion.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Pipeline completion checks — only fully finished runs are replayable. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 3 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) |
| 验证状态 | selected |

#### 函数导航

[generation_step_statuses](#fun-57dfc7a96b) · [pipeline_replay_errors](#fun-d7f6e6e3b1) · [assert_pipeline_replay_ready](#fun-0bb8a53ce4)

<a id="fun-57dfc7a96b"></a>

#### `generation_step_statuses`

- **ID / 行**：`FUN-57DFC7A96B` / `L35`（源码见本单元概览）
- **签名 / 返回**：`generation_step_statuses(report: dict[str, Any])` → `dict[str, str]`
- **职责**：As-built responsibility derived from `generation_step_statuses` and its owning unit.
- **依赖**：get、isinstance、lower、report.get、row.get、str、strip
- **复杂度 / 风险**：分支 4；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d7f6e6e3b1"></a>

#### `pipeline_replay_errors`

- **ID / 行**：`FUN-D7F6E6E3B1` / `L50`（源码见本单元概览）
- **签名 / 返回**：`pipeline_replay_errors(report: dict[str, Any], manifest: dict[str, Any] | None=None)` → `list[str]`
- **职责**：Return human-readable errors when a saved run must not be replayed.
- **依赖**：errors.append、generation_step_statuses、get、lower、step_map.get、str、strip、summary.get
- **复杂度 / 风险**：分支 6；跨度 26 行；high
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="fun-0bb8a53ce4"></a>

#### `assert_pipeline_replay_ready`

- **ID / 行**：`FUN-0BB8A53CE4` / `L78`（源码见本单元概览）
- **签名 / 返回**：`assert_pipeline_replay_ready(report: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `assert_pipeline_replay_ready` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、join、pipeline_replay_errors
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="unit-969bf3943a"></a>

### src/run/archive/index.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-969BF3943A |
| 源码 | [src/run/archive/index.py](../../src/run/archive/index.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Global index for run archives — avoids scanning every folder on list. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

[index_path](#fun-9a9d39921e) · [load_index](#fun-0ecea1344b) · [save_index](#fun-c4f5638491) · [upsert_index_entry](#fun-081a82e5e4) · [remove_index_entries](#fun-2f44aef037) · [list_index_entries](#fun-5115315dfe) · [rebuild_index_from_disk](#fun-9b663ef8e0)

<a id="fun-9a9d39921e"></a>

#### `index_path`

- **ID / 行**：`FUN-9A9D39921E` / `L19`（源码见本单元概览）
- **签名 / 返回**：`index_path(root: Path)` → `Path`
- **职责**：As-built responsibility derived from `index_path` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0ecea1344b"></a>

#### `load_index`

- **ID / 行**：`FUN-0ECEA1344B` / `L23`（源码见本单元概览）
- **签名 / 返回**：`load_index(root: Path)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `load_index` and its owning unit.
- **依赖**：index_path、isinstance、json.loads、path.is_file、path.read_text、payload.setdefault
- **复杂度 / 风险**：分支 3；跨度 12 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c4f5638491"></a>

#### `save_index`

- **ID / 行**：`FUN-C4F5638491` / `L37`（源码见本单元概览）
- **签名 / 返回**：`save_index(root: Path, index: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `save_index` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：datetime.now、index_path、isoformat、json.dumps、root.mkdir、write_text
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-081a82e5e4"></a>

#### `upsert_index_entry`

- **ID / 行**：`FUN-081A82E5E4` / `L48`（源码见本单元概览）
- **签名 / 返回**：`upsert_index_entry(root: Path, entry: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `upsert_index_entry` and its owning unit.
- **依赖**：entry.get、index.get、list、load_index、row.get、runs.append、runs.sort、save_index、str
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2f44aef037"></a>

#### `remove_index_entries`

- **ID / 行**：`FUN-2F44AEF037` / `L59`（源码见本单元概览）
- **签名 / 返回**：`remove_index_entries(root: Path, run_ids: set[str])` → `None`
- **职责**：As-built responsibility derived from `remove_index_entries` and its owning unit.
- **依赖**：index.get、load_index、row.get、save_index、str
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5115315dfe"></a>

#### `list_index_entries`

- **ID / 行**：`FUN-5115315DFE` / `L68`（源码见本单元概览）
- **签名 / 返回**：`list_index_entries(root: Path, *, limit: int=100)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `list_index_entries` and its owning unit.
- **依赖**：index.get、list、load_index、row.get、runs.sort、str
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) · direct-dynamic

<a id="fun-9b663ef8e0"></a>

#### `rebuild_index_from_disk`

- **ID / 行**：`FUN-9B663EF8E0` / `L75`（源码见本单元概览）
- **签名 / 返回**：`rebuild_index_from_disk(root: Path, rows: list[dict[str, Any]])` → `None`
- **职责**：Replace index contents from freshly scanned archive rows.
- **依赖**：load_index、row.get、save_index、sorted、str
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) · direct-dynamic

<a id="unit-038535558b"></a>

### src/run/archive/prune.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-038535558B |
| 源码 | [src/run/archive/prune.py](../../src/run/archive/prune.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | LRU pruning for run archive folders. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) |
| 验证状态 | selected |

#### 函数导航

[_dir_size_bytes](#fun-f03125cdf0) · [prune_archives](#fun-a1476b11ab)

<a id="fun-f03125cdf0"></a>

#### `_dir_size_bytes`

- **ID / 行**：`FUN-F03125CDF0` / `L16`（源码见本单元概览）
- **签名 / 返回**：`_dir_size_bytes(path: Path)` → `int`
- **职责**：As-built responsibility derived from `_dir_size_bytes` and its owning unit.
- **依赖**：child.is_file、child.stat、path.rglob
- **复杂度 / 风险**：分支 3；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a1476b11ab"></a>

#### `prune_archives`

- **ID / 行**：`FUN-A1476B11AB` / `L27`（源码见本单元概览）
- **签名 / 返回**：`prune_archives(root: Path, rows: list[dict[str, Any]], *, max_count: int | None=None, max_mb: int | None=None)` → `list[str]`
- **职责**：Delete oldest archives when count or total size exceeds limits. Returns removed run_ids.
- **依赖**：_dir_size_bytes、dict.fromkeys、folder.is_dir、len、log.info、log.warning、ordered.pop、remove_index_entries、removed.append、row.get、set、shutil.rmtree、sizes.get、sorted、str、to_remove.append、victim.get
- **复杂度 / 风险**：分支 15；跨度 57 行；high
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) · direct-dynamic

<a id="unit-ea2375efd1"></a>

### src/run/archive/schema.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EA2375EFD1 |
| 源码 | [src/run/archive/schema.py](../../src/run/archive/schema.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Run archive schema — versioned manifest and artifact envelopes. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 5 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[ArchiveInspection.loadable](#fun-4d1e837774) · [app_build_version](#fun-0fd63f4847) · [artifact_envelope](#fun-350588b114) · [unwrap_artifact](#fun-9ed5b56457) · [build_manifest](#fun-a7f6be3e0f)

<a id="fun-4d1e837774"></a>

#### `ArchiveInspection.loadable`

- **ID / 行**：`FUN-4D1E837774` / `L84`（源码见本单元概览）
- **签名 / 返回**：`ArchiveInspection.loadable(self)` → `bool`
- **职责**：As-built responsibility derived from `loadable` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-0fd63f4847"></a>

#### `app_build_version`

- **ID / 行**：`FUN-0FD63F4847` / `L88`（源码见本单元概览）
- **签名 / 返回**：`app_build_version()` → `str`
- **职责**：Best-effort build id for manifest (git short sha or 'dev').
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：__file__.replace、rsplit、strip、subprocess.check_output
- **复杂度 / 风险**：分支 2；跨度 16 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-350588b114"></a>

#### `artifact_envelope`

- **ID / 行**：`FUN-350588B114` / `L106`（源码见本单元概览）
- **签名 / 返回**：`artifact_envelope(*, kind: str, artifact_version: int, payload: Any)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `artifact_envelope` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-9ed5b56457"></a>

#### `unwrap_artifact`

- **ID / 行**：`FUN-9ED5B56457` / `L114`（源码见本单元概览）
- **签名 / 返回**：`unwrap_artifact(raw: Any, *, kind: str, default_version: int)` → `tuple[int, Any]`
- **职责**：Return (artifact_version, payload) for enveloped or legacy bare payloads.
- **依赖**：int、isinstance、raw.get
- **复杂度 / 风险**：分支 5；跨度 17 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py) · direct-dynamic

<a id="fun-a7f6be3e0f"></a>

#### `build_manifest`

- **ID / 行**：`FUN-A7F6BE3E0F` / `L133`（源码见本单元概览）
- **签名 / 返回**：`build_manifest(*, run_id: str, saved_at: str | None=None, run_config: dict[str, Any] | None=None, summary: dict[str, Any] | None=None, legacy: dict[str, Any] | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `build_manifest` and its owning unit.
- **依赖**：app_build_version、datetime.now、isoformat
- **复杂度 / 风险**：分支 0；跨度 50 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-d3d34bc712"></a>

### src/run/archive/store.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D3D34BC712 |
| 源码 | [src/run/archive/store.py](../../src/run/archive/store.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Persist each pipeline run under its own folder; replay loads the saved bundle as-is. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 40 / 15 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[archives_root](#fun-1c86ff94a1) · [run_dir](#fun-5374bbe5e8) · [_sanitize_json](#fun-4433fa9140) · [allocate_run_id](#fun-681db272f7) · [inspect_run_archive](#fun-ed26b4ee99) · [_archive_row_from_path](#fun-c1c36bd8f4) · [_scan_archives](#fun-1ecbdf7dbe) · [list_archives](#fun-9e74461596) · [archives_exist](#fun-02080aaef3) · [archive_label](#fun-a95b39bc72) · [_ts_to_str](#fun-9ae985d283) · [_ts_from_str](#fun-85ef9fd874) · [_encode_order_block](#fun-37471cb30f) · [_decode_order_block](#fun-aef3d9744a) · [_encode_fvg](#fun-b2731107dd) · [_decode_fvg](#fun-55b5b5693e) · [_encode_structure_event](#fun-0b04667d7d) · [_decode_structure_event](#fun-5ade499def) · [_encode_liquidity](#fun-57b7676118) · [_decode_liquidity](#fun-ad119574f9) · [encode_analysis](#fun-4982e87c7f) · [decode_analysis](#fun-6c9f997021) · [_frame_to_json](#fun-789e3f37fa) · [_frame_from_json](#fun-8a5c077425) · [_external_to_json](#fun-ff14e13c2d) · [_external_from_json](#fun-a2a4e2c638) · [_fetch_payload](#fun-31c24783fe) · [load_fetch](#fun-76805b2fc9) · [load_enriched](#fun-a0b5f157c2) · [load_analyses](#fun-e23a10f8ee) · [load_archive_meta](#fun-2c07f0c57c) · [load_report](#fun-426b01b9bc) · [load_bundle](#fun-d5f0d013d7) · [load_archive_5m_bars](#fun-57bbeb8ec6) · [_failure_payload](#fun-5b44894270) · [_stub_failure_report](#fun-8665b343fa) · [_persist_archive_folder](#fun-70ced3edba) · [archive_failure_run](#fun-b471df422d) · [load_forensic_bundle](#fun-4dda0d21b3) · [archive_run](#fun-7d1305aec2)

<a id="fun-1c86ff94a1"></a>

#### `archives_root`

- **ID / 行**：`FUN-1C86FF94A1` / `L58`（源码见本单元概览）
- **签名 / 返回**：`archives_root()` → `Path`
- **职责**：As-built responsibility derived from `archives_root` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-5374bbe5e8"></a>

#### `run_dir`

- **ID / 行**：`FUN-5374BBE5E8` / `L62`（源码见本单元概览）
- **签名 / 返回**：`run_dir(run_id: str)` → `Path`
- **职责**：As-built responsibility derived from `run_dir` and its owning unit.
- **依赖**：archives_root
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-4433fa9140"></a>

#### `_sanitize_json`

- **ID / 行**：`FUN-4433FA9140` / `L66`（源码见本单元概览）
- **签名 / 返回**：`_sanitize_json(obj: Any)` → `Any`
- **职责**：As-built responsibility derived from `_sanitize_json` and its owning unit.
- **依赖**：_sanitize_json、abs、isinstance、math.isinf、math.isnan、obj.items、round
- **复杂度 / 风险**：分支 5；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-681db272f7"></a>

#### `allocate_run_id`

- **ID / 行**：`FUN-681DB272F7` / `L78`（源码见本单元概览）
- **签名 / 返回**：`allocate_run_id()` → `str`
- **职责**：As-built responsibility derived from `allocate_run_id` and its owning unit.
- **依赖**：datetime.now、exists、run_dir、strftime
- **复杂度 / 风险**：分支 1；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-ed26b4ee99"></a>

#### `inspect_run_archive`

- **ID / 行**：`FUN-ED26B4EE99` / `L88`（源码见本单元概览）
- **签名 / 返回**：`inspect_run_archive(run_id: str)` → `Any`
- **职责**：As-built responsibility derived from `inspect_run_archive` and its owning unit.
- **依赖**：inspect_archive、run_dir
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-c1c36bd8f4"></a>

#### `_archive_row_from_path`

- **ID / 行**：`FUN-C1C36BD8F4` / `L92`（源码见本单元概览）
- **签名 / 返回**：`_archive_row_from_path(run_id: str, path: Path)` → `dict[str, Any] | None`
- **职责**：As-built responsibility derived from `_archive_row_from_path` and its owning unit.
- **依赖**：inspect_archive、is_file、json.loads、legacy_meta.get、manifest.get、meta_path.is_file、meta_path.read_text、path.is_dir、row.setdefault、str、summary.get
- **复杂度 / 风险**：分支 5；跨度 36 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-1ecbdf7dbe"></a>

#### `_scan_archives`

- **ID / 行**：`FUN-1ECBDF7DBE` / `L130`（源码见本单元概览）
- **签名 / 返回**：`_scan_archives(*, limit: int=100)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `_scan_archives` and its owning unit.
- **依赖**：_archive_row_from_path、archives_root、path.is_dir、root.is_dir、root.iterdir、row.get、rows.append、rows.sort、str
- **复杂度 / 风险**：分支 4；跨度 13 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-9e74461596"></a>

#### `list_archives`

- **ID / 行**：`FUN-9E74461596` / `L145`（源码见本单元概览）
- **签名 / 返回**：`list_archives(*, limit: int=100)` → `list[dict[str, Any]]`
- **职责**：As-built responsibility derived from `list_archives` and its owning unit.
- **依赖**：_scan_archives、archives_root、list_index_entries、max、rebuild_index_from_disk、root.is_dir
- **复杂度 / 风险**：分支 3；跨度 11 行；high
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-02080aaef3"></a>

#### `archives_exist`

- **ID / 行**：`FUN-02080AAEF3` / `L158`（源码见本单元概览）
- **签名 / 返回**：`archives_exist()` → `bool`
- **职责**：As-built responsibility derived from `archives_exist` and its owning unit.
- **依赖**：bool、list_archives
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-a95b39bc72"></a>

#### `archive_label`

- **ID / 行**：`FUN-A95B39BC72` / `L162`（源码见本单元概览）
- **签名 / 返回**：`archive_label(meta: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `archive_label` and its owning unit.
- **依赖**：bars.get、float、format_utc8、get、isinstance、meta.get、str
- **复杂度 / 风险**：分支 5；跨度 20 行；high
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-9ae985d283"></a>

#### `_ts_to_str`

- **ID / 行**：`FUN-9AE985D283` / `L184`（源码见本单元概览）
- **签名 / 返回**：`_ts_to_str(value: Any)` → `str`
- **职责**：As-built responsibility derived from `_ts_to_str` and its owning unit.
- **依赖**：isoformat、pd.Timestamp
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-85ef9fd874"></a>

#### `_ts_from_str`

- **ID / 行**：`FUN-85EF9FD874` / `L188`（源码见本单元概览）
- **签名 / 返回**：`_ts_from_str(value: str | None)` → `pd.Timestamp | None`
- **职责**：As-built responsibility derived from `_ts_from_str` and its owning unit.
- **依赖**：pd.Timestamp
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-37471cb30f"></a>

#### `_encode_order_block`

- **ID / 行**：`FUN-37471CB30F` / `L194`（源码见本单元概览）
- **签名 / 返回**：`_encode_order_block(row: OrderBlock)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_encode_order_block` and its owning unit.
- **依赖**：_ts_to_str
- **复杂度 / 风险**：分支 0；跨度 8 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-aef3d9744a"></a>

#### `_decode_order_block`

- **ID / 行**：`FUN-AEF3D9744A` / `L204`（源码见本单元概览）
- **签名 / 返回**：`_decode_order_block(payload: dict[str, Any])` → `OrderBlock`
- **职责**：As-built responsibility derived from `_decode_order_block` and its owning unit.
- **依赖**：OrderBlock、_ts_from_str、float、payload.get、pd.Timestamp.utcnow、str
- **复杂度 / 风险**：分支 0；跨度 8 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-b2731107dd"></a>

#### `_encode_fvg`

- **ID / 行**：`FUN-B2731107DD` / `L214`（源码见本单元概览）
- **签名 / 返回**：`_encode_fvg(row: FairValueGap)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_encode_fvg` and its owning unit.
- **依赖**：_ts_to_str
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-55b5b5693e"></a>

#### `_decode_fvg`

- **ID / 行**：`FUN-55B5B5693E` / `L224`（源码见本单元概览）
- **签名 / 返回**：`_decode_fvg(payload: dict[str, Any])` → `FairValueGap`
- **职责**：As-built responsibility derived from `_decode_fvg` and its owning unit.
- **依赖**：FairValueGap、_ts_from_str、float、payload.get、pd.Timestamp.utcnow、str
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0b04667d7d"></a>

#### `_encode_structure_event`

- **ID / 行**：`FUN-0B04667D7D` / `L234`（源码见本单元概览）
- **签名 / 返回**：`_encode_structure_event(row: StructureEvent)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_encode_structure_event` and its owning unit.
- **依赖**：_ts_to_str
- **复杂度 / 风险**：分支 1；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-5ade499def"></a>

#### `_decode_structure_event`

- **ID / 行**：`FUN-5ADE499DEF` / `L245`（源码见本单元概览）
- **签名 / 返回**：`_decode_structure_event(payload: dict[str, Any])` → `StructureEvent`
- **职责**：As-built responsibility derived from `_decode_structure_event` and its owning unit.
- **依赖**：StructureEvent、_ts_from_str、float、payload.get、pd.Timestamp.utcnow
- **复杂度 / 风险**：分支 0；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-57b7676118"></a>

#### `_encode_liquidity`

- **ID / 行**：`FUN-57B7676118` / `L256`（源码见本单元概览）
- **签名 / 返回**：`_encode_liquidity(row: LiquidityZone)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_encode_liquidity` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ad119574f9"></a>

#### `_decode_liquidity`

- **ID / 行**：`FUN-AD119574F9` / `L266`（源码见本单元概览）
- **签名 / 返回**：`_decode_liquidity(payload: dict[str, Any])` → `LiquidityZone`
- **职责**：As-built responsibility derived from `_decode_liquidity` and its owning unit.
- **依赖**：LiquidityZone、bool、float、payload.get、str
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4982e87c7f"></a>

#### `encode_analysis`

- **ID / 行**：`FUN-4982E87C7F` / `L276`（源码见本单元概览）
- **签名 / 返回**：`encode_analysis(analysis: TimeframeAnalysis)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `encode_analysis` and its owning unit.
- **依赖**：_encode_fvg、_encode_liquidity、_encode_order_block、_encode_structure_event
- **复杂度 / 风险**：分支 0；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-6c9f997021"></a>

#### `decode_analysis`

- **ID / 行**：`FUN-6C9F997021` / `L299`（源码见本单元概览）
- **签名 / 返回**：`decode_analysis(payload: dict[str, Any])` → `TimeframeAnalysis`
- **职责**：As-built responsibility derived from `decode_analysis` and its owning unit.
- **依赖**：TimeframeAnalysis、_decode_fvg、_decode_liquidity、_decode_order_block、_decode_structure_event、isinstance、payload.get、str
- **复杂度 / 风险**：分支 0；跨度 21 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-789e3f37fa"></a>

#### `_frame_to_json`

- **ID / 行**：`FUN-789E3F37FA` / `L322`（源码见本单元概览）
- **签名 / 返回**：`_frame_to_json(df: pd.DataFrame)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_frame_to_json` and its owning unit.
- **依赖**：df.copy、getattr、out.index.tz_convert、out.where、pd.notna、pd.to_datetime、str、ts.isoformat、values.tolist
- **复杂度 / 风险**：分支 1；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8a5c077425"></a>

#### `_frame_from_json`

- **ID / 行**：`FUN-8A5C077425` / `L334`（源码见本单元概览）
- **签名 / 返回**：`_frame_from_json(payload: dict[str, Any])` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `_frame_from_json` and its owning unit.
- **依赖**：pd.DataFrame、pd.to_datetime
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ff14e13c2d"></a>

#### `_external_to_json`

- **ID / 行**：`FUN-FF14E13C2D` / `L340`（源码见本单元概览）
- **签名 / 返回**：`_external_to_json(external: ExternalFactors)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_external_to_json` and its owning unit.
- **依赖**：event.to_dict、item.to_dict、list、quote.to_dict
- **复杂度 / 风险**：分支 0；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a2a4e2c638"></a>

#### `_external_from_json`

- **ID / 行**：`FUN-A2A4E2C638` / `L355`（源码见本单元概览）
- **签名 / 返回**：`_external_from_json(payload: dict[str, Any])` → `ExternalFactors`
- **职责**：As-built responsibility derived from `_external_from_json` and its owning unit.
- **依赖**：CalendarEvent、ExternalFactors、HeadlineItem、MacroQuote、float、isinstance、payload.get、row.get、str
- **复杂度 / 风险**：分支 0；跨度 47 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-31c24783fe"></a>

#### `_fetch_payload`

- **ID / 行**：`FUN-31C24783FE` / `L404`（源码见本单元概览）
- **签名 / 返回**：`_fetch_payload(fetched: DataFetchResult)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_fetch_payload` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：_external_to_json、_frame_to_json、artifact_envelope、fetched.raw.items
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-76805b2fc9"></a>

#### `load_fetch`

- **ID / 行**：`FUN-76805B2FC9` / `L414`（源码见本单元概览）
- **签名 / 返回**：`load_fetch(run_id: str)` → `DataFetchResult`
- **职责**：As-built responsibility derived from `load_fetch` and its owning unit.
- **异常 / 副作用 / 并发**：FileNotFoundError / external-io / caller-thread
- **依赖**：DataFetchResult、FileNotFoundError、_external_from_json、_frame_from_json、get、json.loads、load_manifest、manifest.get、migrate_fetch_payload、migrate_frame_payload、path.is_file、path.read_text、payload.get、raw_payload.items、run_dir、str
- **复杂度 / 风险**：分支 1；跨度 16 行；high
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-a0b5f157c2"></a>

#### `load_enriched`

- **ID / 行**：`FUN-A0B5F157C2` / `L432`（源码见本单元概览）
- **签名 / 返回**：`load_enriched(run_id: str)` → `dict[str, pd.DataFrame]`
- **职责**：As-built responsibility derived from `load_enriched` and its owning unit.
- **异常 / 副作用 / 并发**：FileNotFoundError / none-detected / caller-thread
- **依赖**：FileNotFoundError、_frame_from_json、enriched_dir.glob、enriched_dir.is_dir、enriched_spec.get、get、json.loads、load_manifest、manifest.get、migrate_frame_payload、path.read_text、run_dir、sorted、str
- **复杂度 / 风险**：分支 3；跨度 15 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e23a10f8ee"></a>

#### `load_analyses`

- **ID / 行**：`FUN-E23A10F8EE` / `L449`（源码见本单元概览）
- **签名 / 返回**：`load_analyses(run_id: str, enriched: dict[str, pd.DataFrame])` → `dict[str, TimeframeAnalysis]`
- **职责**：As-built responsibility derived from `load_analyses` and its owning unit.
- **依赖**：analyze_timeframe、decode_analysis、enriched.items、get、isinstance、json.loads、load_manifest、log.warning、manifest.get、migrate_analyses_payload、path.is_file、path.read_text、payload.items、run_dir、str
- **复杂度 / 风险**：分支 1；跨度 17 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-2c07f0c57c"></a>

#### `load_archive_meta`

- **ID / 行**：`FUN-2C07F0C57C` / `L468`（源码见本单元概览）
- **签名 / 返回**：`load_archive_meta(run_id: str)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `load_archive_meta` and its owning unit.
- **依赖**：json.loads、load_manifest、meta_path.is_file、meta_path.read_text、run_dir、upgrade_manifest_if_needed
- **复杂度 / 风险**：分支 1；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-426b01b9bc"></a>

#### `load_report`

- **ID / 行**：`FUN-426B01B9BC` / `L479`（源码见本单元概览）
- **签名 / 返回**：`load_report(run_id: str)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `load_report` and its owning unit.
- **异常 / 副作用 / 并发**：FileNotFoundError / none-detected / caller-thread
- **依赖**：FileNotFoundError、get、json.loads、load_manifest、manifest.get、path.is_file、path.read_text、run_dir、str
- **复杂度 / 风险**：分支 1；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-d5f0d013d7"></a>

#### `load_bundle`

- **ID / 行**：`FUN-D5F0D013D7` / `L489`（源码见本单元概览）
- **签名 / 返回**：`load_bundle(run_id: str)` → `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]`
- **职责**：Load saved (report, enriched, analyses) without re-running the pipeline.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、get、inspect_archive、int、join、list、load_analyses、load_enriched、load_report、load_warnings.extend、log.warning、manifest.get、normalize_report、report.setdefault、run_dir、upgrade_manifest_if_needed
- **复杂度 / 风险**：分支 2；跨度 39 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="fun-57bbeb8ec6"></a>

#### `load_archive_5m_bars`

- **ID / 行**：`FUN-57BBEB8EC6` / `L530`（源码见本单元概览）
- **签名 / 返回**：`load_archive_5m_bars(run_id: str)` → `pd.DataFrame`
- **职责**：Load 5m OHLCV from a saved run archive (shared contract with backtest).
- **异常 / 副作用 / 并发**：FileNotFoundError / none-detected / caller-thread
- **依赖**：FileNotFoundError、load_fetch
- **复杂度 / 风险**：分支 1；跨度 6 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-5b44894270"></a>

#### `_failure_payload`

- **ID / 行**：`FUN-5B44894270` / `L538`（源码见本单元概览）
- **签名 / 返回**：`_failure_payload(reason: str, *, step: str | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_failure_payload` and its owning unit.
- **依赖**：datetime.now、isoformat
- **复杂度 / 风险**：分支 0；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8665b343fa"></a>

#### `_stub_failure_report`

- **ID / 行**：`FUN-8665B343FA` / `L546`（源码见本单元概览）
- **签名 / 返回**：`_stub_failure_report(*, run_config: RunConfig, reason: str, generation_steps: list[dict] | None=None, llm_io: list[dict] | None=None, current_price: float | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_stub_failure_report` and its owning unit.
- **依赖**：cfg.fingerprint、cfg.to_dict、datetime.now、format_utc8、isoformat、run_config.normalized
- **复杂度 / 风险**：分支 1；跨度 26 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-70ced3edba"></a>

#### `_persist_archive_folder`

- **ID / 行**：`FUN-70CED3EDBA` / `L574`（源码见本单元概览）
- **签名 / 返回**：`_persist_archive_folder(run_id: str, *, run_config: RunConfig, summary: dict[str, Any], report: dict[str, Any], fetched: DataFetchResult | None=None, enriched: dict[str, pd.DataFrame] | None=None, analyses: dict[str, TimeframeAnalysis] | None=None, failure: dict[str, Any] | None=None)` → `Path`
- **职责**：As-built responsibility derived from `_persist_archive_folder` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io;filesystem / caller-thread
- **依赖**：_fetch_payload、_frame_to_json、_sanitize_json、analyses.items、archives_root、artifact_envelope、build_manifest、cfg.fingerprint、cfg.to_dict、datetime.now、encode_analysis、enriched.items、enriched_dir.mkdir、inspect_archive、isoformat、json.dumps、list_archives、log.info、prune_archives、run_config.normalized
- **复杂度 / 风险**：分支 5；跨度 102 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-b471df422d"></a>

#### `archive_failure_run`

- **ID / 行**：`FUN-B471DF422D` / `L678`（源码见本单元概览）
- **签名 / 返回**：`archive_failure_run(run_id: str, reason: str, *, run_config: RunConfig, elapsed_s: float, fetched: DataFetchResult | None=None, enriched: dict[str, pd.DataFrame] | None=None, analyses: dict[str, TimeframeAnalysis] | None=None, report: dict[str, Any] | None=None, failure_step: str | None=None)` → `Path | None`
- **职责**：Persist a partial/failed run for forensics (not full replay).
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_failure_payload、_persist_archive_folder、_stub_failure_report、existing.get、fetched.raw.get、float、get、get_progress、load_archive_meta、prog.llm_io_snapshot、prog.snapshot、report.get、report.setdefault、round、run_dir、s.get、str、target.exists
- **复杂度 / 风险**：分支 11；跨度 70 行；high
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) · direct-dynamic

<a id="fun-4dda0d21b3"></a>

#### `load_forensic_bundle`

- **ID / 行**：`FUN-4DDA0D21B3` / `L750`（源码见本单元概览）
- **签名 / 返回**：`load_forensic_bundle(run_id: str)` → `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, TimeframeAnalysis]]`
- **职责**：Load a partial/failed archive for problem-scene review (not full chart replay).
- **异常 / 副作用 / 并发**：FileNotFoundError / none-detected / caller-thread
- **依赖**：FileNotFoundError、RunConfig.from_dict、_stub_failure_report、directory.is_dir、failure.get、failure_path.is_file、failure_path.read_text、get、inspect_archive、int、isinstance、json.loads、list、load_analyses、load_enriched、load_report、load_warnings.append、manifest.get、normalize_report、report.setdefault
- **复杂度 / 风险**：分支 9；跨度 57 行；medium
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) · direct-dynamic

<a id="fun-7d1305aec2"></a>

#### `archive_run`

- **ID / 行**：`FUN-7D1305AEC2` / `L809`（源码见本单元概览）
- **签名 / 返回**：`archive_run(run_id: str, *, fetched: DataFetchResult, report: dict[str, Any], enriched: dict[str, pd.DataFrame], analyses: dict[str, TimeframeAnalysis], run_config: RunConfig, elapsed_s: float)` → `Path`
- **职责**：As-built responsibility derived from `archive_run` and its owning unit.
- **依赖**：_persist_archive_folder、assert_pipeline_replay_ready、get、meta.get、report.get、round、run_config.normalized、str
- **复杂度 / 风险**：分支 1；跨度 32 行；high
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="unit-3365be69b6"></a>

### src/run/archive/transfer.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3365BE69B6 |
| 源码 | [src/run/archive/transfer.py](../../src/run/archive/transfer.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Export/import run archive folders as portable zip bundles. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) |
| 验证状态 | selected |

#### 函数导航

[export_archive_zip](#fun-8992fe197d) · [import_archive_zip](#fun-41bb437461)

<a id="fun-8992fe197d"></a>

#### `export_archive_zip`

- **ID / 行**：`FUN-8992FE197D` / `L22`（源码见本单元概览）
- **签名 / 返回**：`export_archive_zip(run_id: str)` → `bytes`
- **职责**：Zip an entire run folder for sharing or backup.
- **异常 / 副作用 / 并发**：FileNotFoundError / none-detected / caller-thread
- **依赖**：FileNotFoundError、as_posix、buf.getvalue、directory.is_dir、directory.rglob、io.BytesIO、json.dumps、path.is_file、path.relative_to、run_dir、sorted、zf.write、zf.writestr、zipfile.ZipFile
- **复杂度 / 风险**：分支 3；跨度 21 行；high
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) · direct-dynamic

<a id="fun-41bb437461"></a>

#### `import_archive_zip`

- **ID / 行**：`FUN-41BB437461` / `L45`（源码见本单元概览）
- **签名 / 返回**：`import_archive_zip(data: bytes, *, run_id: str | None=None, overwrite: bool=False)` → `str`
- **职责**：Extract a bundle zip into ``.cache/run_archives/`` and refresh the index.
- **异常 / 副作用 / 并发**：FileExistsError;ValueError / filesystem / caller-thread
- **依赖**：FileExistsError、ValueError、_archive_row_from_path、archives_root、bundle_meta.get、decode、inspect_archive、io.BytesIO、iter、json.loads、len、log.info、name.endswith、name.split、name.startswith、next、out_path.parent.mkdir、out_path.write_bytes、rel.endswith、root.mkdir
- **复杂度 / 风险**：分支 10；跨度 50 行；high
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py) · direct-dynamic

<a id="unit-e124606847"></a>

### src/run/config.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E124606847 |
| 源码 | [src/run/config.py](../../src/run/config.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Runtime report-generation configuration. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 11 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[RunConfig.normalized](#fun-b62302b4ee) · [RunConfig.to_dict](#fun-f162ed7246) · [RunConfig.fingerprint](#fun-64a2707a8e) · [RunConfig.from_dict](#fun-b640f9deec) · [coerce_run_config](#fun-f263af19a6) · [run_config_widget_state](#fun-bb1b3b8b1f) · [is_advanced_run_config](#fun-6f8a6a5aa4) · [default_panel_run_config](#fun-3913f92b96) · [run_config_from_env](#fun-168d3dbada) · [run_config_for_mode](#fun-529864dac4) · [apply_run_config](#fun-4a55d80b54)

<a id="fun-b62302b4ee"></a>

#### `RunConfig.normalized`

- **ID / 行**：`FUN-B62302B4EE` / `L49`（源码见本单元概览）
- **签名 / 返回**：`RunConfig.normalized(self)` → `'RunConfig'`
- **职责**：As-built responsibility derived from `normalized` and its owning unit.
- **依赖**：ANALYST_ONLY_ALIASES.get、RunConfig、bool、lower、strip
- **复杂度 / 风险**：分支 4；跨度 40 行；medium
- **测试 / 验证**：[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) · direct-dynamic

<a id="fun-f162ed7246"></a>

#### `RunConfig.to_dict`

- **ID / 行**：`FUN-F162ED7246` / `L90`（源码见本单元概览）
- **签名 / 返回**：`RunConfig.to_dict(self)` → `dict[str, object]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict、self.normalized
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-64a2707a8e"></a>

#### `RunConfig.fingerprint`

- **ID / 行**：`FUN-64A2707A8E` / `L93`（源码见本单元概览）
- **签名 / 返回**：`RunConfig.fingerprint(self)` → `str`
- **职责**：As-built responsibility derived from `fingerprint` and its owning unit.
- **依赖**：cfg.to_dict、hashlib.sha256、hexdigest、json.dumps、raw.encode、self.normalized
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) · direct-dynamic

<a id="fun-b640f9deec"></a>

#### `RunConfig.from_dict`

- **ID / 行**：`FUN-B640F9DEEC` / `L102`（源码见本单元概览）
- **签名 / 返回**：`RunConfig.from_dict(cls, data: dict[str, Any] | None)` → `'RunConfig'`
- **职责**：As-built responsibility derived from `from_dict` and its owning unit.
- **依赖**：RunConfig、cls、data.items、fields、normalized
- **复杂度 / 风险**：分支 1；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f263af19a6"></a>

#### `coerce_run_config`

- **ID / 行**：`FUN-F263AF19A6` / `L110`（源码见本单元概览）
- **签名 / 返回**：`coerce_run_config(value: object)` → `RunConfig | None`
- **职责**：Accept RunConfig instances or dict snapshots from session / report meta.
- **依赖**：RunConfig.from_dict、isinstance、value.normalized
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-bb1b3b8b1f"></a>

#### `run_config_widget_state`

- **ID / 行**：`FUN-BB1B3B8B1F` / `L126`（源码见本单元概览）
- **签名 / 返回**：`run_config_widget_state(config: RunConfig)` → `dict[str, object]`
- **职责**：Pure mapping from RunConfig to Streamlit widget session keys.
- **依赖**：_MODE_UI_LABELS.get、bool、cfg.fingerprint、config.normalized、preset.fingerprint、run_config_for_mode
- **复杂度 / 风险**：分支 2；跨度 33 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-6f8a6a5aa4"></a>

#### `is_advanced_run_config`

- **ID / 行**：`FUN-6F8A6A5AA4` / `L161`（源码见本单元概览）
- **签名 / 返回**：`is_advanced_run_config(config: RunConfig)` → `bool`
- **职责**：As-built responsibility derived from `is_advanced_run_config` and its owning unit.
- **依赖**：cfg.fingerprint、config.normalized、preset.fingerprint、run_config_for_mode
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-3913f92b96"></a>

#### `default_panel_run_config`

- **ID / 行**：`FUN-3913F92B96` / `L167`（源码见本单元概览）
- **签名 / 返回**：`default_panel_run_config()` → `RunConfig`
- **职责**：Default prefill when the Streamlit config panel is shown (cold start / reconfigure).
- **依赖**：run_config_for_mode
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-168d3dbada"></a>

#### `run_config_from_env`

- **ID / 行**：`FUN-168D3DBADA` / `L172`（源码见本单元概览）
- **签名 / 返回**：`run_config_from_env()` → `RunConfig`
- **职责**：Build defaults from imported environment configuration.
- **依赖**：RunConfig、normalized
- **复杂度 / 风险**：分支 0；跨度 17 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-529864dac4"></a>

#### `run_config_for_mode`

- **ID / 行**：`FUN-529864DAC4` / `L191`（源码见本单元概览）
- **签名 / 返回**：`run_config_for_mode(mode: AgentMode, *, llm_enabled: bool=True, llm_analyst_only: str='')` → `RunConfig`
- **职责**：Create the simple UI presets: rule, llm, or hybrid.
- **依赖**：RunConfig、normalized
- **复杂度 / 风险**：分支 1；跨度 17 行；medium
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-4a55d80b54"></a>

#### `apply_run_config`

- **ID / 行**：`FUN-4A55D80B54` / `L210`（源码见本单元概览）
- **签名 / 返回**：`apply_run_config(run_config: RunConfig)` → `None`
- **职责**：Bind run config to the current worker thread (immutable, no module globals).
- **依赖**：run_config.normalized、set_run_config
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="unit-8a8bc190aa"></a>

### src/run/context.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8A8BC190AA |
| 源码 | [src/run/context.py](../../src/run/context.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Thread-local runtime configuration for pipeline runs (no module-global mutation). |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_config_summary.py](../../tests/unit/test_archive_config_summary.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) |
| 验证状态 | selected |

#### 函数导航

[set_run_config](#fun-2ed9157cf0) · [reset_run_config](#fun-68bfb62aad) · [get_run_config](#fun-30b017175d) · [run_config_scope](#fun-d24ed90856) · [agent_mode](#fun-7d87b82d39) · [llm_narrative_enabled](#fun-9f09ace833)

<a id="fun-2ed9157cf0"></a>

#### `set_run_config`

- **ID / 行**：`FUN-2ED9157CF0` / `L14`（源码见本单元概览）
- **签名 / 返回**：`set_run_config(config: RunConfig)` → `Token`
- **职责**：Bind immutable run config to the current thread / async context.
- **依赖**：_run_config.set、config.normalized
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-68bfb62aad"></a>

#### `reset_run_config`

- **ID / 行**：`FUN-68BFB62AAD` / `L19`（源码见本单元概览）
- **签名 / 返回**：`reset_run_config(token: Token)` → `None`
- **职责**：As-built responsibility derived from `reset_run_config` and its owning unit.
- **依赖**：_run_config.reset
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-30b017175d"></a>

#### `get_run_config`

- **ID / 行**：`FUN-30B017175D` / `L23`（源码见本单元概览）
- **签名 / 返回**：`get_run_config()` → `RunConfig`
- **职责**：As-built responsibility derived from `get_run_config` and its owning unit.
- **依赖**：_run_config.get、run_config_from_env
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-d24ed90856"></a>

#### `run_config_scope`

- **ID / 行**：`FUN-D24ED90856` / `L31`（源码见本单元概览）
- **签名 / 返回**：`run_config_scope(config: RunConfig)` → `Iterator[RunConfig]`
- **职责**：Context manager for tests and background workers.
- **依赖**：config.normalized、reset_run_config、set_run_config
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-7d87b82d39"></a>

#### `agent_mode`

- **ID / 行**：`FUN-7D87B82D39` / `L40`（源码见本单元概览）
- **签名 / 返回**：`agent_mode()` → `str`
- **职责**：As-built responsibility derived from `agent_mode` and its owning unit.
- **依赖**：get_run_config
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_config_summary.py](../../tests/unit/test_archive_config_summary.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_audit_summary.py](../../tests/unit/test_audit_summary.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_llm_trade_stages.py](../../tests/unit/test_llm_trade_stages.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) · direct-dynamic

<a id="fun-9f09ace833"></a>

#### `llm_narrative_enabled`

- **ID / 行**：`FUN-9F09ACE833` / `L44`（源码见本单元概览）
- **签名 / 返回**：`llm_narrative_enabled()` → `bool`
- **职责**：As-built responsibility derived from `llm_narrative_enabled` and its owning unit.
- **依赖**：bool、get_run_config
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-7df4993ab3"></a>

### src/run/pipeline_run.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7DF4993AB3 |
| 源码 | [src/run/pipeline_run.py](../../src/run/pipeline_run.py) |
| 架构组件 | ARC-RUN — 运行上下文与归档 |
| 职责 | Active pipeline run id — for partial/failure archives from worker/orchestrator. |
| 关联需求 | [SWR-CORE-001](./SWE.1-software-requirements.md#swr-core-001)、[SWR-CORE-002](./SWE.1-software-requirements.md#swr-core-002)、[SWR-DATA-003](./SWE.1-software-requirements.md#swr-data-003)、[SWR-REP-001](./SWE.1-software-requirements.md#swr-rep-001)、[SWR-REP-002](./SWE.1-software-requirements.md#swr-rep-002)、[SWR-REP-003](./SWE.1-software-requirements.md#swr-rep-003)、[SWR-ARC-001](./SWE.1-software-requirements.md#swr-arc-001)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](./SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](./SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[set_current_run_id](#fun-018351c88a) · [get_current_run_id](#fun-7ab49a40bf)

<a id="fun-018351c88a"></a>

#### `set_current_run_id`

- **ID / 行**：`FUN-018351C88A` / `L10`（源码见本单元概览）
- **签名 / 返回**：`set_current_run_id(run_id: str | None)` → `None`
- **职责**：As-built responsibility derived from `set_current_run_id` and its owning unit.
- **依赖**：_current_run_id.set
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-7ab49a40bf"></a>

#### `get_current_run_id`

- **ID / 行**：`FUN-7AB49A40BF` / `L14`（源码见本单元概览）
- **签名 / 返回**：`get_current_run_id()` → `str | None`
- **职责**：As-built responsibility derived from `get_current_run_id` and its owning unit.
- **依赖**：_current_run_id.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="arc-backtest"></a>

## ARC-BACKTEST — Point-in-time 回测

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/backtest/__init__.py](#unit-d4fb321d1e) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/engine.py](#unit-b336aa1943) | 10 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/macro.py](#unit-d40a0640bf) | 6 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/metrics.py](#unit-a92846cf7a) | 3 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/simulator.py](#unit-d6d81aa6c4) | 10 | 10 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) | selected |
| [src/backtest/types.py](#unit-a71e1f8ce9) | 5 | 3 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) | selected |

<a id="unit-d4fb321d1e"></a>

### src/backtest/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D4FB321D1E |
| 源码 | [src/backtest/__init__.py](../../src/backtest/__init__.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | Backtesting primitives for the rule-based XAUUSD analysis system. |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[__getattr__](#fun-3eb645c6d9)

<a id="fun-3eb645c6d9"></a>

#### `__getattr__`

- **ID / 行**：`FUN-3EB645C6D9` / `L17`（源码见本单元概览）
- **签名 / 返回**：`__getattr__(name: str)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `__getattr__` and its owning unit.
- **异常 / 副作用 / 并发**：AttributeError / none-detected / caller-thread
- **依赖**：AttributeError
- **复杂度 / 风险**：分支 1；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-b336aa1943"></a>

### src/backtest/engine.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B336AA1943 |
| 源码 | [src/backtest/engine.py](../../src/backtest/engine.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | Historical replay engine for the existing rule analysis stack. |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 10 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_backtest_engine.py](../../tests/unit/test_backtest_engine.py) |
| 验证状态 | selected |

#### 函数导航

[normalize_ohlcv](#fun-9b29434b63) · [resample_ohlcv](#fun-7de676802f) · [make_multitimeframe](#fun-a04b254b5f) · [_enough_data](#fun-18097428b1) · [_selected_signals](#fun-e547fb0bfe) · [_iter_signal_points](#fun-0ed117c7ab) · [_macro_data_for_run](#fun-f28876ab16) · [run_backtest](#fun-96250d4b68) · [run_random_window_backtest](#fun-2ce7bcc851) · [run_backtest_from_archive](#fun-ee64e9ff2e)

<a id="fun-9b29434b63"></a>

#### `normalize_ohlcv`

- **ID / 行**：`FUN-9B29434B63` / `L17`（源码见本单元概览）
- **签名 / 返回**：`normalize_ohlcv(df: pd.DataFrame)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `normalize_ohlcv` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / filesystem / caller-thread
- **依赖**：ValueError、astype、df.copy、dropna、out.pop、out.rename、out.sort_index、pd.to_datetime、rename.items
- **复杂度 / 风险**：分支 4；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_backtest_engine.py](../../tests/unit/test_backtest_engine.py) · direct-dynamic

<a id="fun-7de676802f"></a>

#### `resample_ohlcv`

- **ID / 行**：`FUN-7DE676802F` / `L43`（源码见本单元概览）
- **签名 / 返回**：`resample_ohlcv(df_5m: pd.DataFrame, rule: str)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `resample_ohlcv` and its owning unit.
- **依赖**：agg、df_5m.resample、out.dropna
- **复杂度 / 风险**：分支 0；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a04b254b5f"></a>

#### `make_multitimeframe`

- **ID / 行**：`FUN-A04B254B5F` / `L50`（源码见本单元概览）
- **签名 / 返回**：`make_multitimeframe(df_5m: pd.DataFrame)` → `dict[str, pd.DataFrame]`
- **职责**：As-built responsibility derived from `make_multitimeframe` and its owning unit.
- **依赖**：resample_ohlcv
- **复杂度 / 风险**：分支 0；跨度 8 行；medium
- **测试 / 验证**：[tests/unit/test_backtest_engine.py](../../tests/unit/test_backtest_engine.py) · direct-dynamic

<a id="fun-18097428b1"></a>

#### `_enough_data`

- **ID / 行**：`FUN-18097428B1` / `L60`（源码见本单元概览）
- **签名 / 返回**：`_enough_data(data: dict[str, pd.DataFrame])` → `bool`
- **职责**：As-built responsibility derived from `_enough_data` and its owning unit.
- **依赖**：all、data.get、len、required.items
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e547fb0bfe"></a>

#### `_selected_signals`

- **ID / 行**：`FUN-E547FB0BFE` / `L65`（源码见本单元概览）
- **签名 / 返回**：`_selected_signals(data_5m: pd.DataFrame, *, config: BacktestConfig, dxy_daily: pd.DataFrame | None=None)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `_selected_signals` and its owning unit.
- **依赖**：AgentEvidence、EvidenceItem、ExternalFactors、MarketContext、ResearchDebate、_enough_data、analyze_timeframe、apply_macro_to_signals、compute_trading_signals、daily_metrics、data.items、decision.to_dict、enrich、float、len、macro_notes.append、macro_state.to_dict、macro_state_at、make_multitimeframe、max
- **复杂度 / 风险**：分支 11；跨度 102 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0ed117c7ab"></a>

#### `_iter_signal_points`

- **ID / 行**：`FUN-0ED117C7AB` / `L169`（源码见本单元概览）
- **签名 / 返回**：`_iter_signal_points(df_5m: pd.DataFrame, config: BacktestConfig)` → `Iterable[int]`
- **职责**：As-built responsibility derived from `_iter_signal_points` and its owning unit.
- **依赖**：len、max、range
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f28876ab16"></a>

#### `_macro_data_for_run`

- **ID / 行**：`FUN-F28876AB16` / `L174`（源码见本单元概览）
- **签名 / 返回**：`_macro_data_for_run(config: BacktestConfig, dxy_daily: pd.DataFrame | None)` → `tuple[pd.DataFrame | None, str | None]`
- **职责**：As-built responsibility derived from `_macro_data_for_run` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：fetch_historical_dxy、normalize_macro_ohlcv、str
- **复杂度 / 风险**：分支 3；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-96250d4b68"></a>

#### `run_backtest`

- **ID / 行**：`FUN-96250D4B68` / `L185`（源码见本单元概览）
- **签名 / 返回**：`run_backtest(df_5m: pd.DataFrame, config: BacktestConfig | None=None, *, dxy_daily: pd.DataFrame | None=None)` → `BacktestResult`
- **职责**：As-built responsibility derived from `run_backtest` and its owning unit.
- **依赖**：BacktestConfig、BacktestResult、_iter_signal_points、_macro_data_for_run、_selected_signals、float、getattr、group_trades、len、metadata.get、normalize_ohlcv、simulate_signal、str、summarize_trades、trades.append
- **复杂度 / 风险**：分支 7；跨度 54 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2ce7bcc851"></a>

#### `run_random_window_backtest`

- **ID / 行**：`FUN-2CE7BCC851` / `L241`（源码见本单元概览）
- **签名 / 返回**：`run_random_window_backtest(df_5m: pd.DataFrame, config: BacktestConfig | None=None, *, dxy_daily: pd.DataFrame | None=None)` → `BacktestResult`
- **职责**：As-built responsibility derived from `run_random_window_backtest` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：BacktestConfig、BacktestResult、_macro_data_for_run、all_trades.append、all_trades.sort、group_trades、int、len、max、normalize_ohlcv、random.Random、range、replace、rng.randint、round、run_backtest、seen.add、set、sorted、str
- **复杂度 / 风险**：分支 6；跨度 60 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ee64e9ff2e"></a>

#### `run_backtest_from_archive`

- **ID / 行**：`FUN-EE64E9FF2E` / `L303`（源码见本单元概览）
- **签名 / 返回**：`run_backtest_from_archive(run_id: str, config: BacktestConfig | None=None, *, dxy_daily: pd.DataFrame | None=None)` → `BacktestResult`
- **职责**：Run rule backtest on 5m bars stored in a run archive (same artifact contract as UI replay).
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：BacktestConfig、dict、load_archive_5m_bars、replace、run_backtest
- **复杂度 / 风险**：分支 0；跨度 16 行；high
- **测试 / 验证**：[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py) · direct-dynamic

<a id="unit-d40a0640bf"></a>

### src/backtest/macro.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D40A0640BF |
| 源码 | [src/backtest/macro.py](../../src/backtest/macro.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | Historical macro replay helpers for backtests. |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 6 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_macro.py](../../tests/unit/test_backtest_macro.py) |
| 验证状态 | selected |

#### 函数导航

[fetch_historical_dxy](#fun-ba325106f2) · [normalize_macro_ohlcv](#fun-0012d514e3) · [macro_state_at](#fun-3652f686d6) · [macro_state_at.pct_change](#fun-9797b95972) · [apply_macro_to_signals](#fun-d64ad4df14) · [_grade](#fun-81f066d179)

<a id="fun-ba325106f2"></a>

#### `fetch_historical_dxy`

- **ID / 行**：`FUN-BA325106F2` / `L10`（源码见本单元概览）
- **签名 / 返回**：`fetch_historical_dxy(n_bars: int=1500)` → `pd.DataFrame`
- **职责**：Fetch DXY daily history once for a backtest run.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_fetch_bars
- **复杂度 / 风险**：分支 0；跨度 15 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-0012d514e3"></a>

#### `normalize_macro_ohlcv`

- **ID / 行**：`FUN-0012D514E3` / `L27`（源码见本单元概览）
- **签名 / 返回**：`normalize_macro_ohlcv(df: pd.DataFrame)` → `pd.DataFrame`
- **职责**：As-built responsibility derived from `normalize_macro_ohlcv` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / filesystem / caller-thread
- **依赖**：ValueError、df.copy、out.pop、out.rename、out.sort_index、pd.to_datetime、rename.items
- **复杂度 / 风险**：分支 2；跨度 20 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3652f686d6"></a>

#### `macro_state_at`

- **ID / 行**：`FUN-3652F686D6` / `L49`（源码见本单元概览）
- **签名 / 返回**：`macro_state_at(dxy_daily: pd.DataFrame | None, timestamp: pd.Timestamp)` → `MacroReplayState`
- **职责**：As-built responsibility derived from `macro_state_at` and its owning unit.
- **依赖**：MacroReplayState、abs、float、len、min、normalize_macro_ohlcv、pct_change、pd.Timestamp、round、ts.floor、ts.tz_convert、ts.tz_localize
- **复杂度 / 风险**：分支 22；跨度 84 行；medium
- **测试 / 验证**：[tests/unit/test_backtest_macro.py](../../tests/unit/test_backtest_macro.py) · direct-dynamic

<a id="fun-9797b95972"></a>

#### `macro_state_at.pct_change`

- **ID / 行**：`FUN-9797B95972` / `L90`（源码见本单元概览）
- **签名 / 返回**：`macro_state_at.pct_change(periods: int)` → `float | None`
- **职责**：As-built responsibility derived from `pct_change` and its owning unit.
- **依赖**：float、len
- **复杂度 / 风险**：分支 2；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d64ad4df14"></a>

#### `apply_macro_to_signals`

- **ID / 行**：`FUN-D64AD4DF14` / `L135`（源码见本单元概览）
- **签名 / 返回**：`apply_macro_to_signals(signals: list, state: MacroReplayState, weight: float)` → `list`
- **职责**：As-built responsibility derived from `apply_macro_to_signals` and its owning unit.
- **依赖**：_grade、float、getattr、max、min、round、setattr、signal.score_reasons.append、sorted、str
- **复杂度 / 风险**：分支 5；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-81f066d179"></a>

#### `_grade`

- **ID / 行**：`FUN-81F066D179` / `L159`（源码见本单元概览）
- **签名 / 返回**：`_grade(score: float)` → `str`
- **职责**：As-built responsibility derived from `_grade` and its owning unit.
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="unit-a92846cf7a"></a>

### src/backtest/metrics.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A92846CF7A |
| 源码 | [src/backtest/metrics.py](../../src/backtest/metrics.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | Performance statistics for backtest runs. |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 3 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_metrics.py](../../tests/unit/test_backtest_metrics.py) |
| 验证状态 | selected |

#### 函数导航

[_max_drawdown](#fun-b0fc151afd) · [summarize_trades](#fun-b1a235a7d0) · [group_trades](#fun-da4189939e)

<a id="fun-b0fc151afd"></a>

#### `_max_drawdown`

- **ID / 行**：`FUN-B0FC151AFD` / `L11`（源码见本单元概览）
- **签名 / 返回**：`_max_drawdown(values: list[float])` → `float`
- **职责**：As-built responsibility derived from `_max_drawdown` and its owning unit.
- **依赖**：max、min、round
- **复杂度 / 风险**：分支 1；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b1a235a7d0"></a>

#### `summarize_trades`

- **ID / 行**：`FUN-B1A235A7D0` / `L22`（源码见本单元概览）
- **签名 / 返回**：`summarize_trades(trades: list[TradeResult])` → `dict`
- **职责**：As-built responsibility derived from `summarize_trades` and its owning unit.
- **依赖**：_max_drawdown、abs、len、round、sum、t.exit_reason.startswith
- **复杂度 / 风险**：分支 11；跨度 27 行；high
- **测试 / 验证**：[tests/unit/test_backtest_metrics.py](../../tests/unit/test_backtest_metrics.py) · direct-dynamic

<a id="fun-da4189939e"></a>

#### `group_trades`

- **ID / 行**：`FUN-DA4189939E` / `L51`（源码见本单元概览）
- **签名 / 返回**：`group_trades(trades: Iterable[TradeResult], key: str)` → `list[dict]`
- **职责**：As-built responsibility derived from `group_trades` and its owning unit.
- **依赖**：append、buckets.items、defaultdict、getattr、rows.append、sorted、str、summarize_trades
- **复杂度 / 风险**：分支 2；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="unit-d6d81aa6c4"></a>

### src/backtest/simulator.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D6D81AA6C4 |
| 源码 | [src/backtest/simulator.py](../../src/backtest/simulator.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | Execution simulator with conservative OHLC assumptions. |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 10 / 10 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_simulator.py](../../tests/unit/test_backtest_simulator.py) |
| 验证状态 | selected |

#### 函数导航

[_signal_value](#fun-45cf111f4c) · [_entry_price](#fun-c8726a960a) · [_fillable](#fun-45fe26e9d1) · [_risk_points](#fun-49b51b8f5c) · [_entered](#fun-fbd39fd99d) · [_hit_stop](#fun-c957603ed9) · [_hit_tp](#fun-082bf9ce12) · [_pnl_points](#fun-23462233b9) · [_signal_metadata](#fun-58d5ab9bc5) · [simulate_signal](#fun-203e3a1ea2)

<a id="fun-45cf111f4c"></a>

#### `_signal_value`

- **ID / 行**：`FUN-45CF111F4C` / `L11`（源码见本单元概览）
- **签名 / 返回**：`_signal_value(signal: TradingSignal | dict, key: str, default=None)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `_signal_value` and its owning unit.
- **依赖**：getattr、isinstance、signal.get
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-c8726a960a"></a>

#### `_entry_price`

- **ID / 行**：`FUN-C8726A960A` / `L17`（源码见本单元概览）
- **签名 / 返回**：`_entry_price(signal: TradingSignal | dict, direction: str, slippage: float)` → `float`
- **职责**：As-built responsibility derived from `_entry_price` and its owning unit.
- **依赖**：_signal_value、float
- **复杂度 / 风险**：分支 1；跨度 6 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-45fe26e9d1"></a>

#### `_fillable`

- **ID / 行**：`FUN-45FE26E9D1` / `L25`（源码见本单元概览）
- **签名 / 返回**：`_fillable(row: pd.Series, entry: float)` → `bool`
- **职责**：As-built responsibility derived from `_fillable` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-49b51b8f5c"></a>

#### `_risk_points`

- **ID / 行**：`FUN-49B51B8F5C` / `L29`（源码见本单元概览）
- **签名 / 返回**：`_risk_points(entry: float, stop: float, direction: str)` → `float`
- **职责**：As-built responsibility derived from `_risk_points` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-fbd39fd99d"></a>

#### `_entered`

- **ID / 行**：`FUN-FBD39FD99D` / `L35`（源码见本单元概览）
- **签名 / 返回**：`_entered(row: pd.Series, entry: float)` → `bool`
- **职责**：As-built responsibility derived from `_entered` and its owning unit.
- **依赖**：_fillable
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-c957603ed9"></a>

#### `_hit_stop`

- **ID / 行**：`FUN-C957603ED9` / `L39`（源码见本单元概览）
- **签名 / 返回**：`_hit_stop(row: pd.Series, stop: float, direction: str)` → `bool`
- **职责**：As-built responsibility derived from `_hit_stop` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-082bf9ce12"></a>

#### `_hit_tp`

- **ID / 行**：`FUN-082BF9CE12` / `L45`（源码见本单元概览）
- **签名 / 返回**：`_hit_tp(row: pd.Series, tp: float, direction: str)` → `bool`
- **职责**：As-built responsibility derived from `_hit_tp` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-23462233b9"></a>

#### `_pnl_points`

- **ID / 行**：`FUN-23462233B9` / `L51`（源码见本单元概览）
- **签名 / 返回**：`_pnl_points(entry: float, exit_price: float, direction: str, fee_points: float)` → `float`
- **职责**：As-built responsibility derived from `_pnl_points` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 3 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-58d5ab9bc5"></a>

#### `_signal_metadata`

- **ID / 行**：`FUN-58D5AB9BC5` / `L56`（源码见本单元概览）
- **签名 / 返回**：`_signal_metadata(signal: TradingSignal | dict)` → `dict`
- **职责**：As-built responsibility derived from `_signal_metadata` and its owning unit.
- **依赖**：_signal_value
- **复杂度 / 风险**：分支 0；跨度 7 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-203e3a1ea2"></a>

#### `simulate_signal`

- **ID / 行**：`FUN-203E3A1EA2` / `L65`（源码见本单元概览）
- **签名 / 返回**：`simulate_signal(signal: TradingSignal | dict, future_5m: pd.DataFrame, signal_time: pd.Timestamp, config: BacktestConfig)` → `TradeResult`
- **职责**：Simulate one signal using future 5m bars only.
- **依赖**：TradeResult、_entered、_entry_price、_hit_stop、_hit_tp、_pnl_points、_risk_points、_signal_metadata、_signal_value、active.iterrows、bars.iterrows、enumerate、float、len、next、round、str、upper
- **复杂度 / 风险**：分支 8；跨度 156 行；high
- **测试 / 验证**：[tests/unit/test_backtest_simulator.py](../../tests/unit/test_backtest_simulator.py) · direct-dynamic

<a id="unit-a71e1f8ce9"></a>

### src/backtest/types.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A71E1F8CE9 |
| 源码 | [src/backtest/types.py](../../src/backtest/types.py) |
| 架构组件 | ARC-BACKTEST — Point-in-time 回测 |
| 职责 | Typed data structures for institutional-style backtesting. |
| 关联需求 | [SWR-BT-001](./SWE.1-software-requirements.md#swr-bt-001) |
| 函数 / 高风险函数 | 5 / 3 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-BACKTEST](./SWE.5-integration-testing.md#vm-backtest) |
| 动态测试 | [tests/unit/test_backtest_metrics.py](../../tests/unit/test_backtest_metrics.py)、[tests/unit/test_backtest_simulator.py](../../tests/unit/test_backtest_simulator.py)、[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

[MacroReplayState.to_dict](#fun-e85e437686) · [TradeResult.triggered](#fun-56d05c06ee) · [TradeResult.won](#fun-e8ac0554d3) · [TradeResult.to_dict](#fun-f9db9c8f7c) · [BacktestResult.to_dict](#fun-8075ec23fd)

<a id="fun-e85e437686"></a>

#### `MacroReplayState.to_dict`

- **ID / 行**：`FUN-E85E437686` / `L53`（源码见本单元概览）
- **签名 / 返回**：`MacroReplayState.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict、str
- **复杂度 / 风险**：分支 1；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-56d05c06ee"></a>

#### `TradeResult.triggered`

- **ID / 行**：`FUN-56D05C06EE` / `L81`（源码见本单元概览）
- **签名 / 返回**：`TradeResult.triggered(self)` → `bool`
- **职责**：As-built responsibility derived from `triggered` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-e8ac0554d3"></a>

#### `TradeResult.won`

- **ID / 行**：`FUN-E8AC0554D3` / `L85`（源码见本单元概览）
- **签名 / 返回**：`TradeResult.won(self)` → `bool`
- **职责**：As-built responsibility derived from `won` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-f9db9c8f7c"></a>

#### `TradeResult.to_dict`

- **ID / 行**：`FUN-F9DB9C8F7C` / `L88`（源码见本单元概览）
- **签名 / 返回**：`TradeResult.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict、str
- **复杂度 / 风险**：分支 2；跨度 6 行；high
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="fun-8075ec23fd"></a>

#### `BacktestResult.to_dict`

- **ID / 行**：`FUN-8075EC23FD` / `L105`（源码见本单元概览）
- **签名 / 返回**：`BacktestResult.to_dict(self)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `to_dict` and its owning unit.
- **依赖**：asdict、t.to_dict
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：[tests/unit/test_run_config.py](../../tests/unit/test_run_config.py) · direct-dynamic

<a id="arc-viz"></a>

## ARC-VIZ — Streamlit 展示

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/viz/__init__.py](#unit-3ec85337ca) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/agent_trace_view.py](#unit-986f7077ab) | 8 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/archive_config_summary.py](#unit-6a590d74f1) | 2 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/charts.py](#unit-7301a06e0a) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/dashboard_components.py](#unit-c8a82e7519) | 38 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/decision_page.py](#unit-003f08decb) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/display_labels.py](#unit-9b624c52d7) | 10 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/external_data_view.py](#unit-8b3827f5ec) | 6 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/generation_state.py](#unit-e27519993b) | 7 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/generation_worker.py](#unit-4c9db5733a) | 16 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/lightweight_chart.py](#unit-abbedfd349) | 15 | 15 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/llm_meta.py](#unit-f5c8e9bf82) | 4 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/llm_view.py](#unit-e782e5b762) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/page_layout.py](#unit-d8ab5e90b4) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/pipeline_progress.py](#unit-87ec9bc982) | 19 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/replay_loader.py](#unit-a63d87a7bb) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/report_views.py](#unit-4e47421947) | 4 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/run_config_panel.py](#unit-ee18de86b2) | 20 | 2 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/session_keys.py](#unit-6fa4e87f8a) | 5 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/source_labels.py](#unit-f568ea7ece) | 8 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [src/viz/streamlit_common.py](#unit-202db41fe0) | 20 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) | selected |

<a id="unit-3ec85337ca"></a>

### src/viz/__init__.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3EC85337CA |
| 源码 | [src/viz/__init__.py](../../src/viz/__init__.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | 继承 Streamlit 展示 组件设计；模块职责由公开符号和调用关系约束 |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-986f7077ab"></a>

### src/viz/agent_trace_view.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-986F7077AB |
| 源码 | [src/viz/agent_trace_view.py](../../src/viz/agent_trace_view.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Agent decision chain panel (main content area). |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 8 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) |
| 验证状态 | selected |

#### 函数导航

[_badge_md](#fun-1b8f11eeeb) · [_stage_source_text](#fun-f0fee40c1c) · [_short_text](#fun-4971a29fae) · [_stage_card](#fun-c7d1fa8bc5) · [_render_stage_summary_grid](#fun-f93c1a5bee) · [_decision_flow_markdown](#fun-d0d9c7226c) · [render_agent_trace_panel](#fun-8765e21451) · [render_agent_trace_sidebar](#fun-1d4ae30fbd)

<a id="fun-1b8f11eeeb"></a>

#### `_badge_md`

- **ID / 行**：`FUN-1B8F11EEEB` / `L26`（源码见本单元概览）
- **签名 / 返回**：`_badge_md(meta: dict)` → `str`
- **职责**：As-built responsibility derived from `_badge_md` and its owning unit.
- **依赖**：llm_was_invoked、stage_meta_label
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f0fee40c1c"></a>

#### `_stage_source_text`

- **ID / 行**：`FUN-F0FEE40C1C` / `L33`（源码见本单元概览）
- **签名 / 返回**：`_stage_source_text(stage_meta: dict, stage: str)` → `str`
- **职责**：As-built responsibility derived from `_stage_source_text` and its owning unit.
- **依赖**：meta.get、stage_meta.get、stage_meta_label
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4971a29fae"></a>

#### `_short_text`

- **ID / 行**：`FUN-4971A29FAE` / `L41`（源码见本单元概览）
- **签名 / 返回**：`_short_text(value: object, limit: int=72)` → `str`
- **职责**：As-built responsibility derived from `_short_text` and its owning unit.
- **依赖**：len、str、strip
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c7d1fa8bc5"></a>

#### `_stage_card`

- **ID / 行**：`FUN-C7D1FA8BC5` / `L48`（源码见本单元概览）
- **签名 / 返回**：`_stage_card(stage: str, meta: dict, main: str, sub: str='')` → `str`
- **职责**：As-built responsibility derived from `_stage_card` and its owning unit.
- **依赖**：STAGE_LABELS.get、_short_text、html.escape、llm_was_invoked、render_stage_meta_badge
- **复杂度 / 风险**：分支 1；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-f93c1a5bee"></a>

#### `_render_stage_summary_grid`

- **ID / 行**：`FUN-F93C1A5BEE` / `L60`（源码见本单元概览）
- **签名 / 返回**：`_render_stage_summary_grid(report: dict, trace: dict)` → `str`
- **职责**：As-built responsibility derived from `_render_stage_summary_grid` and its owning unit.
- **依赖**：STAGE_LABELS.get、_stage_card、analyst_biases.append、analyst_team.get、debate.get、decision.get、float、join、label_action、label_bias、label_trade_direction、len、primary_signal.get、report.get、row.get、stage_meta.get、sum、trace.get
- **复杂度 / 风险**：分支 3；跨度 48 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d0d9c7226c"></a>

#### `_decision_flow_markdown`

- **ID / 行**：`FUN-D0D9C7226C` / `L110`（源码见本单元概览）
- **签名 / 返回**：`_decision_flow_markdown(report: dict, trace: dict)` → `str`
- **职责**：As-built responsibility derived from `_decision_flow_markdown` and its owning unit.
- **依赖**：_stage_source_text、analyst_bits.append、conclusion.get、debate.get、decision.get、enumerate、float、join、label_action、label_bias、label_trade_direction、len、meta.get、metrics.get、proposal.get、report.get、row.get、sentiment.get、sig.get、signal_bits.append
- **复杂度 / 风险**：分支 3；跨度 78 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-8765e21451"></a>

#### `render_agent_trace_panel`

- **ID / 行**：`FUN-8765E21451` / `L190`（源码见本单元概览）
- **签名 / 返回**：`render_agent_trace_panel(report: dict)` → `None`
- **职责**：As-built responsibility derived from `render_agent_trace_panel` and its owning unit.
- **依赖**：STAGE_LABELS.get、_badge_md、_decision_flow_markdown、_render_stage_summary_grid、analyst_meta.get、analyst_report.get、analyst_team.get、bear.get、bear_meta.get、bull.get、bull_meta.get、debate.get、decision.get、float、format_latency_ms、get、invariants.get、join、json.dumps、label_action
- **复杂度 / 风险**：分支 45；跨度 266 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-1d4ae30fbd"></a>

#### `render_agent_trace_sidebar`

- **ID / 行**：`FUN-1D4AE30FBD` / `L458`（源码见本单元概览）
- **签名 / 返回**：`render_agent_trace_sidebar(report: dict)` → `None`
- **职责**：Legacy sidebar entry — delegates to panel.
- **依赖**：render_agent_trace_panel
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-6a590d74f1"></a>

### src/viz/archive_config_summary.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6A590D74F1 |
| 源码 | [src/viz/archive_config_summary.py](../../src/viz/archive_config_summary.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Format archived run configuration for replay / forensic banners. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_archive_config_summary.py](../../tests/unit/test_archive_config_summary.py) |
| 验证状态 | selected |

#### 函数导航

[format_archived_run_config](#fun-e73bf3a018) · [pipeline_status_label](#fun-acfcd5eef4)

<a id="fun-e73bf3a018"></a>

#### `format_archived_run_config`

- **ID / 行**：`FUN-E73BF3A018` / `L8`（源码见本单元概览）
- **签名 / 返回**：`format_archived_run_config(run_config: dict[str, Any] | None)` → `str`
- **职责**：As-built responsibility derived from `format_archived_run_config` and its owning unit.
- **依赖**：cfg.get、join、stages.append、str、strip
- **复杂度 / 风险**：分支 5；跨度 22 行；high
- **测试 / 验证**：[tests/unit/test_archive_config_summary.py](../../tests/unit/test_archive_config_summary.py) · direct-dynamic

<a id="fun-acfcd5eef4"></a>

#### `pipeline_status_label`

- **ID / 行**：`FUN-ACFCD5EEF4` / `L32`（源码见本单元概览）
- **签名 / 返回**：`pipeline_status_label(status: str | None)` → `str`
- **职责**：As-built responsibility derived from `pipeline_status_label` and its owning unit.
- **依赖**：lower、mapping.get、str、strip
- **复杂度 / 风险**：分支 0；跨度 7 行；high
- **测试 / 验证**：[tests/unit/test_archive_config_summary.py](../../tests/unit/test_archive_config_summary.py) · direct-dynamic

<a id="unit-7301a06e0a"></a>

### src/viz/charts.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-7301A06E0A |
| 源码 | [src/viz/charts.py](../../src/viz/charts.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Plotly chart builder for the analysis dashboard. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) |
| 验证状态 | selected |

#### 函数导航

[build_sentiment_donut](#fun-508ae8715d) · [build_projection_chart](#fun-25d919a083)

<a id="fun-508ae8715d"></a>

#### `build_sentiment_donut`

- **ID / 行**：`FUN-508AE8715D` / `L10`（源码见本单元概览）
- **签名 / 返回**：`build_sentiment_donut(sentiment: dict[str, float])` → `go.Figure`
- **职责**：As-built responsibility derived from `build_sentiment_donut` and its owning unit.
- **依赖**：dict、fig.update_layout、go.Figure、go.Pie
- **复杂度 / 风险**：分支 0；跨度 24 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-25d919a083"></a>

#### `build_projection_chart`

- **ID / 行**：`FUN-25D919A083` / `L36`（源码见本单元概览）
- **签名 / 返回**：`build_projection_chart(projections: list[dict])` → `go.Figure`
- **职责**：As-built responsibility derived from `build_projection_chart` and its owning unit.
- **依赖**：dict、fig.add_trace、fig.update_layout、fig.update_yaxes、go.Figure、go.Scatter
- **复杂度 / 风险**：分支 1；跨度 24 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-c8a82e7519"></a>

### src/viz/dashboard_components.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C8A82E7519 |
| 源码 | [src/viz/dashboard_components.py](../../src/viz/dashboard_components.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Extended dashboard components — institutional + strategy map (white theme). |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 38 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py) |
| 验证状态 | selected |

#### 函数导航

[_is_placeholder_source](#fun-86e2359125) · [_chg_class](#fun-0059ca3d67) · [_truncate](#fun-2d55219a60) · [_source_tags](#fun-550f755267) · [render_external_data_panel](#fun-85e277e655) · [render_header](#fun-64dfaecbb9) · [_fmt_price](#fun-725d5a8f44) · [_primary_signal](#fun-72ca74c7a9) · [_status_meta](#fun-389fe568ee) · [_direction_class](#fun-23bf7fa077) · [_signal_zone](#fun-0010bc2852) · [_signal_targets](#fun-d398c927e4) · [_first_text](#fun-133e6e54c6) · [render_final_decision_banner](#fun-e962207ce2) · [render_decision_summary](#fun-c819f0daf5) · [_display_plan_signals](#fun-937765293d) · [_confidence_text](#fun-d3d7244ace) · [_minify_plan_html](#fun-2f9b45e4cd) · [_render_plan_card](#fun-e6d39c08cf) · [render_rejected_plan_details](#fun-9c21a8d1a7) · [render_primary_plan_focus](#fun-3bfb666a67) · [render_top_overview_row](#fun-1308a20c4f) · [render_tf_stack](#fun-d69f968c9e) · [render_bottom_row](#fun-1fb9420507) · [_fmt_zone](#fun-2dd042625f) · [_fmt_event_list](#fun-eab2c95485) · [_fmt_prices](#fun-48fc0fd2b1) · [_fmt_strong_weak](#fun-6d789b868b) · [render_tf_panel](#fun-854dcce0eb) · [render_narrative_section](#fun-ce51fb1d21) · [_narrative_fallback_hint](#fun-18e3bf98ae) · [render_key_levels](#fun-1e810a3b0e) · [render_strategy_sections](#fun-b460f224ca) · [render_path_cards](#fun-60b752029b) · [render_calendar](#fun-f129f84b90) · [render_trading_plans](#fun-94c9558228) · [render_liquidity](#fun-5e89771732) · [render_footer](#fun-aaaaeceb82)

<a id="fun-86e2359125"></a>

#### `_is_placeholder_source`

- **ID / 行**：`FUN-86E2359125` / `L23`（源码见本单元概览）
- **签名 / 返回**：`_is_placeholder_source(src: str)` → `bool`
- **职责**：As-built responsibility derived from `_is_placeholder_source` and its owning unit.
- **依赖**：src.endswith、src.lower
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0059ca3d67"></a>

#### `_chg_class`

- **ID / 行**：`FUN-0059CA3D67` / `L632`（源码见本单元概览）
- **签名 / 返回**：`_chg_class(change: float)` → `str`
- **职责**：As-built responsibility derived from `_chg_class` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2d55219a60"></a>

#### `_truncate`

- **ID / 行**：`FUN-2D55219A60` / `L636`（源码见本单元概览）
- **签名 / 返回**：`_truncate(text: str, n: int)` → `str`
- **职责**：As-built responsibility derived from `_truncate` and its owning unit.
- **依赖**：len、str
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-550f755267"></a>

#### `_source_tags`

- **ID / 行**：`FUN-550F755267` / `L641`（源码见本单元概览）
- **签名 / 返回**：`_source_tags(sources: list[str])` → `str`
- **职责**：As-built responsibility derived from `_source_tags` and its owning unit.
- **依赖**：_SOURCE_LABELS.get、_is_placeholder_source、chips.append、html.escape、join
- **复杂度 / 风险**：分支 3；跨度 11 行；low
- **测试 / 验证**：[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py) · direct-dynamic

<a id="fun-85e277e655"></a>

#### `render_external_data_panel`

- **ID / 行**：`FUN-85E277E655` / `L654`（源码见本单元概览）
- **签名 / 返回**：`render_external_data_panel(ext: dict[str, Any])` → `str`
- **职责**：Live external feed: DXY, headlines, calendar, TV social.
- **依赖**：_source_tags、e.get、ext.get、html.escape、isinstance、join、p.get、parse_risk_events_calendar、str
- **复杂度 / 风险**：分支 8；跨度 62 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-64dfaecbb9"></a>

#### `render_header`

- **ID / 行**：`FUN-64DFAECBB9` / `L718`（源码见本单元概览）
- **签名 / 返回**：`render_header(report: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `render_header` and its owning unit.
- **依赖**：_chg_class、join、metric_html.append
- **复杂度 / 风险**：分支 2；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-725d5a8f44"></a>

#### `_fmt_price`

- **ID / 行**：`FUN-725D5A8F44` / `L742`（源码见本单元概览）
- **签名 / 返回**：`_fmt_price(value: Any)` → `str`
- **职责**：As-built responsibility derived from `_fmt_price` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-72ca74c7a9"></a>

#### `_primary_signal`

- **ID / 行**：`FUN-72CA74C7A9` / `L749`（源码见本单元概览）
- **签名 / 返回**：`_primary_signal(signals: list[dict[str, Any]])` → `dict[str, Any] | None`
- **职责**：As-built responsibility derived from `_primary_signal` and its owning unit.
- **依赖**：sig.get
- **复杂度 / 风险**：分支 3；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-389fe568ee"></a>

#### `_status_meta`

- **ID / 行**：`FUN-389FE568EE` / `L758`（源码见本单元概览）
- **签名 / 返回**：`_status_meta(status: str)` → `tuple[str, str]`
- **职责**：As-built responsibility derived from `_status_meta` and its owning unit.
- **依赖**：status_map.get
- **复杂度 / 风险**：分支 0；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-23bf7fa077"></a>

#### `_direction_class`

- **ID / 行**：`FUN-23BF7FA077` / `L769`（源码见本单元概览）
- **签名 / 返回**：`_direction_class(signal: dict[str, Any] | None, conclusion: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_direction_class` and its owning unit.
- **依赖**：conclusion.get、infer_trade_theme、lower、signal.get、str
- **复杂度 / 风险**：分支 3；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0010bc2852"></a>

#### `_signal_zone`

- **ID / 行**：`FUN-0010BC2852` / `L785`（源码见本单元概览）
- **签名 / 返回**：`_signal_zone(sig: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_signal_zone` and its owning unit.
- **依赖**：_fmt_price、sig.get
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d398c927e4"></a>

#### `_signal_targets`

- **ID / 行**：`FUN-D398C927E4` / `L789`（源码见本单元概览）
- **签名 / 返回**：`_signal_targets(sig: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_signal_targets` and its owning unit.
- **依赖**：_fmt_price、join、sig.get
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-133e6e54c6"></a>

#### `_first_text`

- **ID / 行**：`FUN-133E6E54C6` / `L796`（源码见本单元概览）
- **签名 / 返回**：`_first_text(items: list[Any], fallback: str='—')` → `str`
- **职责**：As-built responsibility derived from `_first_text` and its owning unit.
- **依赖**：str、strip
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e962207ce2"></a>

#### `render_final_decision_banner`

- **ID / 行**：`FUN-E962207CE2` / `L804`（源码见本单元概览）
- **签名 / 返回**：`render_final_decision_banner(report: dict[str, Any])` → `str`
- **职责**：Prominent one-line verdict: execute / reduce / wait.
- **依赖**：bool、build_final_decision_meta、final.get、html.escape、label_action、lower、meta.get、plan.get、report.get、str、strip
- **复杂度 / 风险**：分支 9；跨度 54 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-c819f0daf5"></a>

#### `render_decision_summary`

- **ID / 行**：`FUN-C819F0DAF5` / `L860`（源码见本单元概览）
- **签名 / 返回**：`render_decision_summary(report: dict[str, Any])` → `str`
- **职责**：First-screen decision strip: price, bias, executable state, and main risk.
- **依赖**：_direction_class、_first_text、_fmt_price、_primary_signal、_status_meta、bool、conclusion.get、execution_banner、float、get、html.escape、label_action、list、meta.get、metrics.get、render_source_badge、report.get、stage_source、str
- **复杂度 / 风险**：分支 4；跨度 69 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-937765293d"></a>

#### `_display_plan_signals`

- **ID / 行**：`FUN-937765293D` / `L931`（源码见本单元概览）
- **签名 / 返回**：`_display_plan_signals(signals: list[dict[str, Any]], *, limit: int=3)` → `list[dict[str, Any]]`
- **职责**：Up to three plans for UI; invalid plans sink to the end but still show when needed.
- **依赖**：sig.get
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d3d7244ace"></a>

#### `_confidence_text`

- **ID / 行**：`FUN-D3D7244ACE` / `L938`（源码见本单元概览）
- **签名 / 返回**：`_confidence_text(sig: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_confidence_text` and its owning unit.
- **依赖**：float、sig.get、str
- **复杂度 / 风险**：分支 3；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2f9b45e4cd"></a>

#### `_minify_plan_html`

- **ID / 行**：`FUN-2F9B45E4CD` / `L948`（源码见本单元概览）
- **签名 / 返回**：`_minify_plan_html(markup: str)` → `str`
- **职责**：Collapse indentation so Streamlit markdown won't treat the card as a code fence.
- **依赖**：join、ln.strip、markup.splitlines
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e6d39c08cf"></a>

#### `_render_plan_card`

- **ID / 行**：`FUN-E6D39C08CF` / `L954`（源码见本单元概览）
- **签名 / 返回**：`_render_plan_card(sig: dict[str, Any], *, plan_label: str, is_primary: bool=False, unauthorized: bool=False, rejected: bool=False)` → `str`
- **职责**：As-built responsibility derived from `_render_plan_card` and its owning unit.
- **依赖**：_confidence_text、_fmt_price、_minify_plan_html、_signal_targets、_signal_zone、_status_meta、html.escape、infer_trade_theme、join、sig.get、startswith、str、strip
- **复杂度 / 风险**：分支 16；跨度 90 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9c21a8d1a7"></a>

#### `render_rejected_plan_details`

- **ID / 行**：`FUN-9C21A8D1A7` / `L1046`（源码见本单元概览）
- **签名 / 返回**：`render_rejected_plan_details(signals: list[dict], *, meta: dict | None=None, validated_plans: list[dict] | None=None)` → `str`
- **职责**：Collapsible inventory of manager-rejected / unused / geometry-failed candidates.
- **依赖**：_minify_plan_html、_render_plan_card、any、cards.append、enumerate、join、len、prop.get、row.get、s.get、str、upper
- **复杂度 / 风险**：分支 8；跨度 58 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3bfb666a67"></a>

#### `render_primary_plan_focus`

- **ID / 行**：`FUN-3BFB666A67` / `L1106`（源码见本单元概览）
- **签名 / 返回**：`render_primary_plan_focus(report: dict[str, Any])` → `str`
- **职责**：Backward-compatible wrapper: first plan card only.
- **依赖**：_display_plan_signals、_render_plan_card、enumerate、len、next、report.get、sig.get
- **复杂度 / 风险**：分支 2；跨度 11 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-1308a20c4f"></a>

#### `render_top_overview_row`

- **ID / 行**：`FUN-1308A20C4F` / `L1119`（源码见本单元概览）
- **签名 / 返回**：`render_top_overview_row(report: dict[str, Any])` → `str`
- **职责**：Top row: overview | (donut slot) | liquidity | today — 4 columns, 3 HTML panels.
- **依赖**：conclusion_display_lines、html.escape、join、render_source_badge、report.get、stage_source、str
- **复杂度 / 风险**：分支 0；跨度 27 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d69f968c9e"></a>

#### `render_tf_stack`

- **ID / 行**：`FUN-D69F968C9E` / `L1148`（源码见本单元概览）
- **签名 / 返回**：`render_tf_stack(report: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `render_tf_stack` and its owning unit.
- **依赖**：join、render_tf_panel
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-1fb9420507"></a>

#### `render_bottom_row`

- **ID / 行**：`FUN-1FB9420507` / `L1156`（源码见本单元概览）
- **签名 / 返回**：`render_bottom_row(report: dict[str, Any], conclusion: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `render_bottom_row` and its owning unit.
- **依赖**：conclusion.get、html.escape、join、list、p.get、report.get、str
- **复杂度 / 风险**：分支 0；跨度 28 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-2dd042625f"></a>

#### `_fmt_zone`

- **ID / 行**：`FUN-2DD042625F` / `L1186`（源码见本单元概览）
- **签名 / 返回**：`_fmt_zone(items: list[dict], direction: str | None=None, *, limit: int=5)` → `str`
- **职责**：As-built responsibility derived from `_fmt_zone` and its owning unit.
- **依赖**：i.get、join
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-eab2c95485"></a>

#### `_fmt_event_list`

- **ID / 行**：`FUN-EAB2C95485` / `L1193`（源码见本单元概览）
- **签名 / 返回**：`_fmt_event_list(items: list[dict])` → `str`
- **职责**：As-built responsibility derived from `_fmt_event_list` and its owning unit.
- **依赖**：i.get、join
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-48fc0fd2b1"></a>

#### `_fmt_prices`

- **ID / 行**：`FUN-48FC0FD2B1` / `L1199`（源码见本单元概览）
- **签名 / 返回**：`_fmt_prices(prices: list[float])` → `str`
- **职责**：As-built responsibility derived from `_fmt_prices` and its owning unit.
- **依赖**：join
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6d789b868b"></a>

#### `_fmt_strong_weak`

- **ID / 行**：`FUN-6D789B868B` / `L1205`（源码见本单元概览）
- **签名 / 返回**：`_fmt_strong_weak(info: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_fmt_strong_weak` and its owning unit.
- **依赖**：info.get、join、parts.append
- **复杂度 / 风险**：分支 5；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-854dcce0eb"></a>

#### `render_tf_panel`

- **ID / 行**：`FUN-854DCCE0EB` / `L1218`（源码见本单元概览）
- **签名 / 返回**：`render_tf_panel(tf: str, info: dict[str, Any], *, compact: bool=False)` → `str`
- **职责**：As-built responsibility derived from `render_tf_panel` and its owning unit.
- **依赖**：TF_LABELS.get、TREND_CN.get、_fmt_event_list、_fmt_prices、_fmt_strong_weak、_fmt_zone、ema.items、info.get、join、pd_map.get
- **复杂度 / 风险**：分支 4；跨度 47 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ce51fb1d21"></a>

#### `render_narrative_section`

- **ID / 行**：`FUN-CE51FB1D21` / `L1267`（源码见本单元概览）
- **签名 / 返回**：`render_narrative_section(section: dict[str, Any] | None)` → `str`
- **职责**：Render one compact institutional-copy block from the shared contract.
- **依赖**：NARRATIVE_SOURCE_CN.get、_narrative_fallback_hint、html.escape、join、rows.append、section.get、str、strip
- **复杂度 / 风险**：分支 10；跨度 29 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-18e3bf98ae"></a>

#### `_narrative_fallback_hint`

- **ID / 行**：`FUN-18E3BF98AE` / `L1298`（源码见本单元概览）
- **签名 / 返回**：`_narrative_fallback_hint(section: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_narrative_fallback_hint` and its owning unit.
- **依赖**：html.escape、humanize_narrative_fallback、section.get、str、strip
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-1e810a3b0e"></a>

#### `render_key_levels`

- **ID / 行**：`FUN-1E810A3B0E` / `L1307`（源码见本单元概览）
- **签名 / 返回**：`render_key_levels(levels: list[dict])` → `str`
- **职责**：As-built responsibility derived from `render_key_levels` and its owning unit.
- **依赖**：items.append、join、lv.get
- **复杂度 / 风险**：分支 3；跨度 14 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-b460f224ca"></a>

#### `render_strategy_sections`

- **ID / 行**：`FUN-B460F224CA` / `L1323`（源码见本单元概览）
- **签名 / 返回**：`render_strategy_sections(report: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `render_strategy_sections` and its owning unit.
- **依赖**：join、parts.append、render_trading_plans、report.get、title.split
- **复杂度 / 风险**：分支 1；跨度 14 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-60b752029b"></a>

#### `render_path_cards`

- **ID / 行**：`FUN-60B752029B` / `L1340`（源码见本单元概览）
- **签名 / 返回**：`render_path_cards(paths: list[dict])` → `str`
- **职责**：As-built responsibility derived from `render_path_cards` and its owning unit.
- **依赖**：join
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f129f84b90"></a>

#### `render_calendar`

- **ID / 行**：`FUN-F129F84B90` / `L1348`（源码见本单元概览）
- **签名 / 返回**：`render_calendar(events: list[dict])` → `str`
- **职责**：As-built responsibility derived from `render_calendar` and its owning unit.
- **依赖**：e.get、html.escape、join、str
- **复杂度 / 风险**：分支 1；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-94c9558228"></a>

#### `render_trading_plans`

- **ID / 行**：`FUN-94C9558228` / `L1358`（源码见本单元概览）
- **签名 / 返回**：`render_trading_plans(signals: list[dict], *, meta: dict | None=None, include_primary: bool=True, validated_plans: list[dict] | None=None)` → `str`
- **职责**：Unified A/B/C plan cards; separates authorized vs rule-only candidates.
- **依赖**：_display_plan_signals、_render_plan_card、any、bool、cards.append、enumerate、execution_banner、html.escape、join、len、meta.get、render_rejected_plan_details、row.get、s.get、sig.get
- **复杂度 / 风险**：分支 6；跨度 43 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_financial_review.py](../../tests/unit/test_financial_review.py) · direct-dynamic

<a id="fun-5e89771732"></a>

#### `render_liquidity`

- **ID / 行**：`FUN-5E89771732` / `L1403`（源码见本单元概览）
- **签名 / 返回**：`render_liquidity(items: list[dict])` → `str`
- **职责**：As-built responsibility derived from `render_liquidity` and its owning unit.
- **依赖**：join、label_map.get、lines.append
- **复杂度 / 风险**：分支 1；跨度 12 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-aaaaeceb82"></a>

#### `render_footer`

- **ID / 行**：`FUN-AAAAECEB82` / `L1417`（源码见本单元概览）
- **签名 / 返回**：`render_footer(report: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `render_footer` and its owning unit.
- **依赖**：join、report.get
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="unit-003f08decb"></a>

### src/viz/decision_page.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-003F08DECB |
| 源码 | [src/viz/decision_page.py](../../src/viz/decision_page.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Full-page LLM decision chain + I/O history. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) |
| 验证状态 | selected |

#### 函数导航

[_render_generation_and_llm_io](#fun-77f3e3eb2d) · [render_live_generation_panel](#fun-4d76920cc8) · [render_llm_decision_page](#fun-0871294ede)

<a id="fun-77f3e3eb2d"></a>

#### `_render_generation_and_llm_io`

- **ID / 行**：`FUN-77F3E3EB2D` / `L20`（源码见本单元概览）
- **签名 / 返回**：`_render_generation_and_llm_io(*, steps: list[dict], records: list[dict], stage_sources: dict | None=None, expand_last: bool=False, empty_steps_msg: str='暂无生成步骤记录', empty_io_msg: str='暂无 LLM 调用记录', live_streaming: bool=False, show_steps: bool=True)` → `None`
- **职责**：Single panel: pipeline steps on top, LLM I/O below.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：merge_llm_io_with_stage_sources、partition_llm_records_for_live、render_live_llm_streams、render_llm_io_history、render_progress_steps、st.divider、st.info
- **复杂度 / 风险**：分支 10；跨度 47 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4d76920cc8"></a>

#### `render_live_generation_panel`

- **ID / 行**：`FUN-4D76920CC8` / `L69`（源码见本单元概览）
- **签名 / 返回**：`render_live_generation_panel(live: dict, *, show_steps: bool=True)` → `None`
- **职责**：Same tab layout as the decision page, fed by in-flight pipeline snapshots.
- **依赖**：_render_generation_and_llm_io、live.get、st.info、st.tabs
- **复杂度 / 风险**：分支 0；跨度 25 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0871294ede"></a>

#### `render_llm_decision_page`

- **ID / 行**：`FUN-0871294EDE` / `L96`（源码见本单元概览）
- **签名 / 返回**：`render_llm_decision_page(report: dict)` → `None`
- **职责**：As-built responsibility derived from `render_llm_decision_page` and its owning unit.
- **依赖**：_render_generation_and_llm_io、meta.get、render_agent_source_banner、render_agent_trace_panel、render_llm_panel、render_page_hero、report.get、st.markdown、st.tabs
- **复杂度 / 风险**：分支 0；跨度 25 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-9b624c52d7"></a>

### src/viz/display_labels.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9B624C52D7 |
| 源码 | [src/viz/display_labels.py](../../src/viz/display_labels.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Chinese display labels for agent trace and decision UI. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 10 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) |
| 验证状态 | selected |

#### 函数导航

[format_report_branding](#fun-7d9904747d) · [humanize_narrative_fallback](#fun-c22c609a56) · [label_bias](#fun-49e5ad57e6) · [label_action](#fun-5a683dd3d4) · [label_trade_direction](#fun-32cef2320f) · [label_risk_profile](#fun-3c82dc7efd) · [label_position_scale](#fun-32db70ee85) · [infer_trade_theme](#fun-9cdbf9137f) · [execution_banner](#fun-1e94d60636) · [conclusion_display_lines](#fun-493ef2091a)

<a id="fun-7d9904747d"></a>

#### `format_report_branding`

- **ID / 行**：`FUN-7D9904747D` / `L44`（源码见本单元概览）
- **签名 / 返回**：`format_report_branding(text: object)` → `str`
- **职责**：Normalize legacy LuxAlgo strings for reader-facing UI (incl. replay archives).
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：out.replace、str
- **复杂度 / 风险**：分支 1；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-c22c609a56"></a>

#### `humanize_narrative_fallback`

- **ID / 行**：`FUN-C22C609A56` / `L52`（源码见本单元概览）
- **签名 / 返回**：`humanize_narrative_fallback(reason: object)` → `str`
- **职责**：Short Chinese hint for narrative block fallback reasons shown in UI.
- **依赖**：raw.removeprefix、raw.startswith、str、strip
- **复杂度 / 风险**：分支 2；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-49e5ad57e6"></a>

#### `label_bias`

- **ID / 行**：`FUN-49E5AD57E6` / `L67`（源码见本单元概览）
- **签名 / 返回**：`label_bias(value: object)` → `str`
- **职责**：As-built responsibility derived from `label_bias` and its owning unit.
- **依赖**：BIAS_CN.get、lower、str、strip
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-5a683dd3d4"></a>

#### `label_action`

- **ID / 行**：`FUN-5A683DD3D4` / `L72`（源码见本单元概览）
- **签名 / 返回**：`label_action(value: object)` → `str`
- **职责**：As-built responsibility derived from `label_action` and its owning unit.
- **依赖**：ACTION_CN.get、lower、str、strip
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-32cef2320f"></a>

#### `label_trade_direction`

- **ID / 行**：`FUN-32CEF2320F` / `L77`（源码见本单元概览）
- **签名 / 返回**：`label_trade_direction(value: object)` → `str`
- **职责**：As-built responsibility derived from `label_trade_direction` and its owning unit.
- **依赖**：TRADE_DIRECTION_CN.get、lower、str、strip
- **复杂度 / 风险**：分支 0；跨度 3 行；high
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-3c82dc7efd"></a>

#### `label_risk_profile`

- **ID / 行**：`FUN-3C82DC7EFD` / `L82`（源码见本单元概览）
- **签名 / 返回**：`label_risk_profile(value: object)` → `str`
- **职责**：As-built responsibility derived from `label_risk_profile` and its owning unit.
- **依赖**：RISK_PROFILE_CN.get、lower、str、strip
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-32db70ee85"></a>

#### `label_position_scale`

- **ID / 行**：`FUN-32DB70EE85` / `L87`（源码见本单元概览）
- **签名 / 返回**：`label_position_scale(scale: object)` → `str`
- **职责**：As-built responsibility derived from `label_position_scale` and its owning unit.
- **依赖**：float
- **复杂度 / 风险**：分支 4；跨度 12 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9cdbf9137f"></a>

#### `infer_trade_theme`

- **ID / 行**：`FUN-9CDBF9137F` / `L107`（源码见本单元概览）
- **签名 / 返回**：`infer_trade_theme(*, theme: str='', direction: str='', direction_cn: str='')` → `str`
- **职责**：Return ``short`` or ``long`` for plan cards and decision styling.
- **依赖**：any、lower、raw.strip、str、strip
- **复杂度 / 风险**：分支 3；跨度 16 行；high
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-1e94d60636"></a>

#### `execution_banner`

- **ID / 行**：`FUN-1E94D60636` / `L125`（源码见本单元概览）
- **签名 / 返回**：`execution_banner(meta: dict | None)` → `str`
- **职责**：Explain why trading plans may differ from trader/manager rows.
- **依赖**：decision.get、join、lower、meta.get、parts.append、str、strip、trigger.get
- **复杂度 / 风险**：分支 7；跨度 27 行；medium
- **测试 / 验证**：[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="fun-493ef2091a"></a>

#### `conclusion_display_lines`

- **ID / 行**：`FUN-493EF2091A` / `L154`（源码见本单元概览）
- **签名 / 返回**：`conclusion_display_lines(conclusion: dict[str, Any] | None)` → `list[str]`
- **职责**：De-duplicated lines for 结论要点 panels (header + direction_summary).
- **依赖**：conclusion.get、header.startswith、lines.append、str、strip、summary.rstrip
- **复杂度 / 风险**：分支 4；跨度 16 行；medium
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_display_labels.py](../../tests/unit/test_display_labels.py) · direct-dynamic

<a id="unit-8b3827f5ec"></a>

### src/viz/external_data_view.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8B3827F5EC |
| 源码 | [src/viz/external_data_view.py](../../src/viz/external_data_view.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | External data page — news, calendar, DXY, social; available right after fetch. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) |
| 验证状态 | selected |

#### 函数导航

[external_snapshot_from_fetch](#fun-1e2febd33e) · [external_payload_from_report](#fun-73c9145028) · [_render_headline_list](#fun-75474c9286) · [_render_calendar_rows](#fun-15a26b9540) · [render_external_data_content](#fun-6cdbb0b77d) · [render_external_data_page](#fun-6b50c51729)

<a id="fun-1e2febd33e"></a>

#### `external_snapshot_from_fetch`

- **ID / 行**：`FUN-1E2FEBD33E` / `L16`（源码见本单元概览）
- **签名 / 返回**：`external_snapshot_from_fetch(fetched: DataFetchResult)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `external_snapshot_from_fetch` and its owning unit.
- **依赖**：h.to_dict、list、m.to_dict、parse_risk_events_calendar
- **复杂度 / 风险**：分支 1；跨度 20 行；medium
- **测试 / 验证**：[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py) · direct-dynamic

<a id="fun-73c9145028"></a>

#### `external_payload_from_report`

- **ID / 行**：`FUN-73C9145028` / `L38`（源码见本单元概览）
- **签名 / 返回**：`external_payload_from_report(report: dict, data: dict | None=None)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `external_payload_from_report` and its owning unit.
- **依赖**：data.items、dict、ext.get、ext.setdefault、get、len、list、report.get
- **复杂度 / 风险**：分支 2；跨度 14 行；medium
- **测试 / 验证**：[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py) · direct-dynamic

<a id="fun-75474c9286"></a>

#### `_render_headline_list`

- **ID / 行**：`FUN-75474C9286` / `L54`（源码见本单元概览）
- **签名 / 返回**：`_render_headline_list(items: list[dict], *, empty: str)` → `str`
- **职责**：As-built responsibility derived from `_render_headline_list` and its owning unit.
- **依赖**：h.get、html.escape、join、rows.append、str
- **复杂度 / 风险**：分支 4；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-15a26b9540"></a>

#### `_render_calendar_rows`

- **ID / 行**：`FUN-15A26B9540` / `L68`（源码见本单元概览）
- **签名 / 返回**：`_render_calendar_rows(payload: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_render_calendar_rows` and its owning unit.
- **依赖**：e.get、html.escape、join、parse_risk_events_calendar、payload.get、str
- **复杂度 / 风险**：分支 5；跨度 24 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6cdbb0b77d"></a>

#### `render_external_data_content`

- **ID / 行**：`FUN-6CDBB0B77D` / `L94`（源码见本单元概览）
- **签名 / 返回**：`render_external_data_content(payload: dict[str, Any])` → `None`
- **职责**：Render external feed panels from fetch snapshot or full report payload.
- **依赖**：_render_calendar_rows、_render_headline_list、_source_tags、bars.items、derived_bits.append、html.escape、isinstance、join、m.get、p.get、payload.get、sorted、st.markdown、str
- **复杂度 / 风险**：分支 11；跨度 94 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-6b50c51729"></a>

#### `render_external_data_page`

- **ID / 行**：`FUN-6B50C51729` / `L190`（源码见本单元概览）
- **签名 / 返回**：`render_external_data_page(payload: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `render_external_data_page` and its owning unit.
- **依赖**：payload.get、render_external_data_content、render_page_hero
- **复杂度 / 风险**：分支 1；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-e27519993b"></a>

### src/viz/generation_state.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E27519993B |
| 源码 | [src/viz/generation_state.py](../../src/viz/generation_state.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Background report generation jobs — keyed by session + generation UUID. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 7 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[GenerationJob.key](#fun-91dd83b0a6) · [purge_expired](#fun-a28f3ce7db) · [access_job](#fun-fab2a1bb76) · [get_job](#fun-bcb1df87b1) · [create_job](#fun-e4ee868b95) · [drop_job](#fun-0d53c85f3b) · [update_live](#fun-5614348eb6)

<a id="fun-91dd83b0a6"></a>

#### `GenerationJob.key`

- **ID / 行**：`FUN-91DD83B0A6` / `L24`（源码见本单元概览）
- **签名 / 返回**：`GenerationJob.key(self)` → `str`
- **职责**：As-built responsibility derived from `key` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_fact_registry.py](../../tests/unit/test_fact_registry.py)、[tests/unit/test_indicators.py](../../tests/unit/test_indicators.py)、[tests/unit/test_narrative_sections.py](../../tests/unit/test_narrative_sections.py)、[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) · direct-dynamic

<a id="fun-a28f3ce7db"></a>

#### `purge_expired`

- **ID / 行**：`FUN-A28F3CE7DB` / `L32`（源码见本单元概览）
- **签名 / 返回**：`purge_expired()` → `None`
- **职责**：As-built responsibility derived from `purge_expired` and its owning unit.
- **依赖**：_STORE.items、_STORE.pop、time.monotonic
- **复杂度 / 风险**：分支 1；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fab2a1bb76"></a>

#### `access_job`

- **ID / 行**：`FUN-FAB2A1BB76` / `L40`（源码见本单元概览）
- **签名 / 返回**：`access_job(job_key: str)` → `GenerationJob | None`
- **职责**：As-built responsibility derived from `access_job` and its owning unit.
- **依赖**：_STORE.get、purge_expired
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-bcb1df87b1"></a>

#### `get_job`

- **ID / 行**：`FUN-BCB1DF87B1` / `L46`（源码见本单元概览）
- **签名 / 返回**：`get_job(job_key: str, *, session_id: str)` → `GenerationJob | None`
- **职责**：As-built responsibility derived from `get_job` and its owning unit.
- **依赖**：_STORE.get、purge_expired
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-e4ee868b95"></a>

#### `create_job`

- **ID / 行**：`FUN-E4EE868B95` / `L55`（源码见本单元概览）
- **签名 / 返回**：`create_job(session_id: str, generation_id: str)` → `GenerationJob`
- **职责**：As-built responsibility derived from `create_job` and its owning unit.
- **依赖**：GenerationJob、purge_expired
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-0d53c85f3b"></a>

#### `drop_job`

- **ID / 行**：`FUN-0D53C85F3B` / `L63`（源码见本单元概览）
- **签名 / 返回**：`drop_job(job_key: str, *, session_id: str)` → `None`
- **职责**：As-built responsibility derived from `drop_job` and its owning unit.
- **依赖**：_STORE.get、_STORE.pop
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5614348eb6"></a>

#### `update_live`

- **ID / 行**：`FUN-5614348EB6` / `L70`（源码见本单元概览）
- **签名 / 返回**：`update_live(job_key: str, snapshot: dict[str, Any])` → `None`
- **职责**：As-built responsibility derived from `update_live` and its owning unit.
- **依赖**：_STORE.get
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py) · direct-dynamic

<a id="unit-4c9db5733a"></a>

### src/viz/generation_worker.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4C9DB5733A |
| 源码 | [src/viz/generation_worker.py](../../src/viz/generation_worker.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Background report generation worker for Streamlit. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 16 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/regression/test_doc_pipeline_sync.py](../../tests/regression/test_doc_pipeline_sync.py)、[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_live_progress_ui.py](../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py)、[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[_is_streaming_llm_record](#fun-2029e693a6) · [compact_llm_io_for_live](#fun-52fe00a287) · [ModuleSyncProgressReporter.__init__](#fun-2fae0caf3c) · [ModuleSyncProgressReporter._sync](#fun-309bcf8879) · [ModuleSyncProgressReporter._headline_from_steps](#fun-a85c4e4bb0) · [ModuleSyncProgressReporter._on_change](#fun-16cab352ce) · [ModuleSyncProgressReporter._on_llm_chunk](#fun-db5d7a17a9) · [ModuleSyncProgressReporter.llm_begin](#fun-328cc0f106) · [ModuleSyncProgressReporter.llm_end](#fun-b1681a5a0b) · [ModuleSyncProgressReporter.fail](#fun-40bbcb7294) · [ModuleSyncProgressReporter.done](#fun-00ca768fe8) · [ModuleSyncProgressReporter.update](#fun-f475f6a25b) · [ModuleSyncProgressReporter.stage_io](#fun-b77c2c5b77) · [format_generation_error](#fun-4adbbae6f8) · [start_generation](#fun-de0806140c) · [start_generation.worker](#fun-eadc84cc44)

<a id="fun-2029e693a6"></a>

#### `_is_streaming_llm_record`

- **ID / 行**：`FUN-2029E693A6` / `L24`（源码见本单元概览）
- **签名 / 返回**：`_is_streaming_llm_record(rec: dict)` → `bool`
- **职责**：As-built responsibility derived from `_is_streaming_llm_record` and its owning unit.
- **依赖**：rec.get
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-52fe00a287"></a>

#### `compact_llm_io_for_live`

- **ID / 行**：`FUN-52FE00A287` / `L32`（源码见本单元概览）
- **签名 / 返回**：`compact_llm_io_for_live(records: list[dict])` → `list[dict]`
- **职责**：Trim LLM I/O for polling UI — avoids multi-MB widget payloads during streaming.
- **依赖**：_is_streaming_llm_record、compacted.append、len、msg.get、rec.get、str、trimmed_msgs.append
- **复杂度 / 风险**：分支 5；跨度 39 行；medium
- **测试 / 验证**：[tests/unit/test_live_progress_ui.py](../../tests/unit/test_live_progress_ui.py) · direct-dynamic

<a id="fun-2fae0caf3c"></a>

#### `ModuleSyncProgressReporter.__init__`

- **ID / 行**：`FUN-2FAE0CAF3C` / `L76`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.__init__(self, job_key: str)` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **依赖**：__init__、self._sync、super
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-309bcf8879"></a>

#### `ModuleSyncProgressReporter._sync`

- **ID / 行**：`FUN-309BCF8879` / `L82`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter._sync(self)` → `None`
- **职责**：As-built responsibility derived from `_sync` and its owning unit.
- **依赖**：access_job、compact_llm_io_for_live、prev.get、self._headline_from_steps、self.llm_io_snapshot、self.snapshot、update_live
- **复杂度 / 风险**：分支 1；跨度 15 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a85c4e4bb0"></a>

#### `ModuleSyncProgressReporter._headline_from_steps`

- **ID / 行**：`FUN-A85C4E4BB0` / `L99`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter._headline_from_steps(steps: list[dict])` → `str`
- **职责**：As-built responsibility derived from `_headline_from_steps` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：pipeline_progress_headline
- **复杂度 / 风险**：分支 0；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-16cab352ce"></a>

#### `ModuleSyncProgressReporter._on_change`

- **ID / 行**：`FUN-16CAB352CE` / `L104`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter._on_change(self)` → `None`
- **职责**：As-built responsibility derived from `_on_change` and its owning unit.
- **依赖**：self._sync
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-db5d7a17a9"></a>

#### `ModuleSyncProgressReporter._on_llm_chunk`

- **ID / 行**：`FUN-DB5D7A17A9` / `L107`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter._on_llm_chunk(self, stage: str, chunk: str)` → `None`
- **职责**：As-built responsibility derived from `_on_llm_chunk` and its owning unit.
- **依赖**：_on_llm_chunk、self._sync、super、time.monotonic
- **复杂度 / 风险**：分支 1；跨度 6 行；low
- **测试 / 验证**：[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-328cc0f106"></a>

#### `ModuleSyncProgressReporter.llm_begin`

- **ID / 行**：`FUN-328CC0F106` / `L114`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], *, telemetry: dict | None=None)` → `None`
- **职责**：As-built responsibility derived from `llm_begin` and its owning unit.
- **依赖**：llm_begin、self._sync、super
- **复杂度 / 风险**：分支 0；跨度 10 行；medium
- **测试 / 验证**：[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-b1681a5a0b"></a>

#### `ModuleSyncProgressReporter.llm_end`

- **ID / 行**：`FUN-B1681A5A0B` / `L125`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.llm_end(self, stage: str, output: str, *, error: str | None=None, latency_ms: int | None=None, telemetry: dict | None=None)` → `None`
- **职责**：As-built responsibility derived from `llm_end` and its owning unit.
- **依赖**：llm_end、self._sync、super
- **复杂度 / 风险**：分支 0；跨度 11 行；medium
- **测试 / 验证**：[tests/unit/test_module_sync_telemetry.py](../../tests/unit/test_module_sync_telemetry.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="fun-40bbcb7294"></a>

#### `ModuleSyncProgressReporter.fail`

- **ID / 行**：`FUN-40BBCB7294` / `L137`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.fail(self, step_id: str, detail: str='')` → `None`
- **职责**：As-built responsibility derived from `fail` and its owning unit.
- **依赖**：fail、self._sync、super
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_llm_stage_policy.py](../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_report_invariants.py](../../tests/unit/test_report_invariants.py) · direct-dynamic

<a id="fun-00ca768fe8"></a>

#### `ModuleSyncProgressReporter.done`

- **ID / 行**：`FUN-00CA768FE8` / `L141`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.done(self, step_id: str, detail: str='')` → `None`
- **职责**：As-built responsibility derived from `done` and its owning unit.
- **依赖**：done、self._sync、super
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/integration/test_pipeline.py](../../tests/integration/test_pipeline.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_live_progress_ui.py](../../tests/unit/test_live_progress_ui.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-f475f6a25b"></a>

#### `ModuleSyncProgressReporter.update`

- **ID / 行**：`FUN-F475F6A25B` / `L145`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.update(self, step_id: str, *, detail: str | None=None, label: str | None=None)` → `None`
- **职责**：As-built responsibility derived from `update` and its owning unit.
- **依赖**：self._sync、super、update
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：[tests/regression/test_doc_pipeline_sync.py](../../tests/regression/test_doc_pipeline_sync.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_risk_gates.py](../../tests/unit/test_risk_gates.py) · direct-dynamic

<a id="fun-b77c2c5b77"></a>

#### `ModuleSyncProgressReporter.stage_io`

- **ID / 行**：`FUN-B77C2C5B77` / `L149`（源码见本单元概览）
- **签名 / 返回**：`ModuleSyncProgressReporter.stage_io(self, stage: str, *, input_text: str, output_text: str, latency_ms: int | None=None, label: str | None=None)` → `None`
- **职责**：As-built responsibility derived from `stage_io` and its owning unit.
- **依赖**：self._sync、stage_io、super
- **复杂度 / 风险**：分支 0；跨度 17 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4adbbae6f8"></a>

#### `format_generation_error`

- **ID / 行**：`FUN-4ADBBAE6F8` / `L168`（源码见本单元概览）
- **签名 / 返回**：`format_generation_error(exc: BaseException)` → `str`
- **职责**：As-built responsibility derived from `format_generation_error` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：getattr、isinstance、raw.replace、str、strip、type
- **复杂度 / 风险**：分支 5；跨度 20 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) · direct-dynamic

<a id="fun-de0806140c"></a>

#### `start_generation`

- **ID / 行**：`FUN-DE0806140C` / `L190`（源码见本单元概览）
- **签名 / 返回**：`start_generation(job_key: str, run_config: RunConfig, *, session_id: str)` → `None`
- **职责**：As-built responsibility derived from `start_generation` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：ModuleSyncProgressReporter、access_job、archive_failure_run、clear_cache、create_job、format_generation_error、get_current_run_id、get_job、job.thread.is_alive、job_key.split、load_replay_bundle、log.exception、log.info、reset_progress、reset_run_config、run_analysis、run_config.fingerprint、run_config.normalized、run_config.to_dict、set_current_run_id
- **复杂度 / 风险**：分支 12；跨度 73 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) · direct-dynamic

<a id="fun-eadc84cc44"></a>

#### `start_generation.worker`

- **ID / 行**：`FUN-EADC84CC44` / `L217`（源码见本单元概览）
- **签名 / 返回**：`start_generation.worker()` → `None`
- **职责**：As-built responsibility derived from `worker` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：ModuleSyncProgressReporter、access_job、archive_failure_run、clear_cache、format_generation_error、get_current_run_id、log.exception、log.info、reset_progress、reset_run_config、run_analysis、run_config.fingerprint、run_config.normalized、run_config.to_dict、set_current_run_id、set_progress、set_run_config、setdefault、time.perf_counter
- **复杂度 / 风险**：分支 5；跨度 42 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_progress.py](../../tests/unit/test_progress.py) · direct-dynamic

<a id="unit-abbedfd349"></a>

### src/viz/lightweight_chart.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-ABBEDFD349 |
| 源码 | [src/viz/lightweight_chart.py](../../src/viz/lightweight_chart.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | TradingView Lightweight Charts renderer with SMC overlays. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 15 / 15 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_tf_short](#fun-092ce9f86b) · [_zone_title](#fun-f95e2508fa) · [_align_ts](#fun-3733752cf4) · [_to_unix](#fun-8e3f539bdd) · [_bar_delta](#fun-44a30a06ef) · [_zone_future_end](#fun-f4069a84ad) · [_zone_box_data](#fun-fa95eaff48) · [_ob_display_end_time](#fun-19260207ff) · [_append_zone_box](#fun-ff5b159787) · [_append_lux_fvg](#fun-3ce37e5cc0) · [_append_lux_ob](#fun-c590a6c0d5) · [_serialize_overlays](#fun-af5e00ed83) · [_build_projections](#fun-501852c2a0) · [build_lightweight_chart_html](#fun-540615a0fd) · [chart_iframe_height](#fun-ac67fe2b86)

<a id="fun-092ce9f86b"></a>

#### `_tf_short`

- **ID / 行**：`FUN-092CE9F86B` / `L115`（源码见本单元概览）
- **签名 / 返回**：`_tf_short(timeframe: str)` → `str`
- **职责**：As-built responsibility derived from `_tf_short` and its owning unit.
- **依赖**：TF_SHORT.get、timeframe.upper
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-f95e2508fa"></a>

#### `_zone_title`

- **ID / 行**：`FUN-F95E2508FA` / `L119`（源码见本单元概览）
- **签名 / 返回**：`_zone_title(kind: str, direction: str, low: float, high: float, *, half: str | None=None, source_tf: str | None=None)` → `str`
- **职责**：As-built responsibility derived from `_zone_title` and its owning unit.
- **依赖**：_tf_short、int、round
- **复杂度 / 风险**：分支 5；跨度 21 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-3733752cf4"></a>

#### `_align_ts`

- **ID / 行**：`FUN-3733752CF4` / `L142`（源码见本单元概览）
- **签名 / 返回**：`_align_ts(ts: pd.Timestamp, ref_index: pd.DatetimeIndex)` → `pd.Timestamp`
- **职责**：As-built responsibility derived from `_align_ts` and its owning unit.
- **依赖**：pd.Timestamp、t.tz_convert、t.tz_localize
- **复杂度 / 风险**：分支 3；跨度 9 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-8e3f539bdd"></a>

#### `_to_unix`

- **ID / 行**：`FUN-8E3F539BDD` / `L153`（源码见本单元概览）
- **签名 / 返回**：`_to_unix(ts: pd.Timestamp)` → `int`
- **职责**：As-built responsibility derived from `_to_unix` and its owning unit.
- **依赖**：int、pd.Timestamp、timestamp
- **复杂度 / 风险**：分支 0；跨度 2 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-44a30a06ef"></a>

#### `_bar_delta`

- **ID / 行**：`FUN-44A30A06EF` / `L157`（源码见本单元概览）
- **签名 / 返回**：`_bar_delta(plot_df: pd.DataFrame)` → `pd.Timedelta`
- **职责**：As-built responsibility derived from `_bar_delta` and its owning unit.
- **依赖**：len、pd.Timedelta
- **复杂度 / 风险**：分支 1；跨度 4 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-f4069a84ad"></a>

#### `_zone_future_end`

- **ID / 行**：`FUN-F4069A84AD` / `L163`（源码见本单元概览）
- **签名 / 返回**：`_zone_future_end(plot_df: pd.DataFrame, start_time: pd.Timestamp)` → `pd.Timestamp`
- **职责**：Extend Lux zones/lines far to the right so panning does not clip them.
- **依赖**：_align_ts、_bar_delta、len、max
- **复杂度 / 风险**：分支 0；跨度 5 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-fa95eaff48"></a>

#### `_zone_box_data`

- **ID / 行**：`FUN-FA95EAFF48` / `L170`（源码见本单元概览）
- **签名 / 返回**：`_zone_box_data(plot_df: pd.DataFrame, start_time: pd.Timestamp, high: float, *, end_time: pd.Timestamp | None=None)` → `list[dict[str, float | int]]`
- **职责**：Lux-style band top line from start_time through end_time (may extend past last candle).
- **依赖**：_align_ts、_to_unix、_zone_future_end、round
- **复杂度 / 风险**：分支 2；跨度 21 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-19260207ff"></a>

#### `_ob_display_end_time`

- **ID / 行**：`FUN-19260207FF` / `L193`（源码见本单元概览）
- **签名 / 返回**：`_ob_display_end_time(plot_df: pd.DataFrame)` → `pd.Timestamp`
- **职责**：Lux draws each OB box to last_bar_time with extend.right.
- **依赖**：_zone_future_end
- **复杂度 / 风险**：分支 0；跨度 3 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-ff5b159787"></a>

#### `_append_zone_box`

- **ID / 行**：`FUN-FF5B159787` / `L198`（源码见本单元概览）
- **签名 / 返回**：`_append_zone_box(zones: list[dict[str, Any]], *, kind: str, direction: str, low: float, high: float, start_time: pd.Timestamp, plot_df: pd.DataFrame, source_tf: str, colors: dict[str, str], title: str | None=None, show_label: bool=True, end_time: pd.Timestamp | None=None)` → `None`
- **职责**：As-built responsibility derived from `_append_zone_box` and its owning unit.
- **依赖**：_zone_box_data、round、zones.append
- **复杂度 / 风险**：分支 2；跨度 29 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-3ce37e5cc0"></a>

#### `_append_lux_fvg`

- **ID / 行**：`FUN-3CE37E5CC0` / `L229`（源码见本单元概览）
- **签名 / 返回**：`_append_lux_fvg(zones: list[dict[str, Any]], fvg, plot_df: pd.DataFrame, source_tf: str)` → `None`
- **职责**：Lux FVG: two stacked boxes split at midpoint, extending right until mitigated.
- **依赖**：_append_zone_box、_zone_future_end、_zone_title、float
- **复杂度 / 风险**：分支 1；跨度 40 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-c590a6c0d5"></a>

#### `_append_lux_ob`

- **ID / 行**：`FUN-C590A6C0D5` / `L271`（源码见本单元概览）
- **签名 / 返回**：`_append_lux_ob(zones: list[dict[str, Any]], ob, plot_df: pd.DataFrame, source_tf: str, *, end_time: pd.Timestamp)` → `None`
- **职责**：As-built responsibility derived from `_append_lux_ob` and its owning unit.
- **依赖**：_append_zone_box、_zone_title
- **复杂度 / 风险**：分支 1；跨度 22 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-af5e00ed83"></a>

#### `_serialize_overlays`

- **ID / 行**：`FUN-AF5E00ED83` / `L295`（源码见本单元概览）
- **签名 / 返回**：`_serialize_overlays(analysis: TimeframeAnalysis, report: dict[str, Any], plot_df: pd.DataFrame, *, timeframe: str='1h', include_projections: bool=True, variant: str='main')` → `dict[str, Any]`
- **职责**：Build Lux-style zones for the chart's own timeframe only (no BOS/CHoCH overlays).
- **依赖**：_append_lux_fvg、_append_lux_ob、_build_projections、_ob_display_end_time、chart_sr_levels、float、price_lines.extend、visible_active_fvgs、visible_order_blocks、visible_sr_price_lines
- **复杂度 / 风险**：分支 6；跨度 46 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-501852c2a0"></a>

#### `_build_projections`

- **ID / 行**：`FUN-501852C2A0` / `L343`（源码见本单元概览）
- **签名 / 返回**：`_build_projections(plot_df: pd.DataFrame, report: dict[str, Any] | None, *, timeframe: str='5m')` → `list[dict[str, Any]]`
- **职责**：Future dashed path overlays — no probability labels (shown in path cards / Plotly only).
- **依赖**：_PROJECTION_STEP_GAP.get、_to_unix、enumerate、float、len、lines.append、pd.Timedelta、points.append、round
- **复杂度 / 风险**：分支 5；跨度 27 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-540615a0fd"></a>

#### `build_lightweight_chart_html`

- **ID / 行**：`FUN-540615A0FD` / `L372`（源码见本单元概览）
- **签名 / 返回**：`build_lightweight_chart_html(df: pd.DataFrame, analysis: TimeframeAnalysis | None=None, report: dict[str, Any] | None=None, *, timeframe: str='1h', symbol: str='XAUUSD', symbol_name: str='黄金/美元', exchange: str='OANDA', height: int | None=None, bars: int | None=None, variant: str='main', watermark: str | None=None, show_projections: bool | None=None)` → `str`
- **职责**：Build HTML/JS for TradingView Lightweight Charts with volume + SMC zones.
- **依赖**：CHART_VARIANTS.get、LINE_COLORS.items、TF_LABELS.get、_serialize_overlays、_to_unix、body_parts.extend、bool、candles.append、copy、df.tail、float、get、int、join、json.dumps、len、pd.notna、plot_df.iterrows、points.append、preset.get
- **复杂度 / 风险**：分支 42；跨度 478 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="fun-ac67fe2b86"></a>

#### `chart_iframe_height`

- **ID / 行**：`FUN-AC67FE2B86` / `L852`（源码见本单元概览）
- **签名 / 返回**：`chart_iframe_height(variant: str='main', height: int | None=None)` → `int`
- **职责**：As-built responsibility derived from `chart_iframe_height` and its owning unit.
- **依赖**：CHART_VARIANTS.get、int、preset.get
- **复杂度 / 风险**：分支 3；跨度 9 行；high
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="unit-f5c8e9bf82"></a>

### src/viz/llm_meta.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F5C8E9BF82 |
| 源码 | [src/viz/llm_meta.py](../../src/viz/llm_meta.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | LLM display helpers — model names, latency, record dedupe. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[format_latency_ms](#fun-58b0856420) · [dedupe_llm_io_records](#fun-2eacce73e8) · [merge_llm_io_with_stage_sources](#fun-cfe09c603f) · [stage_llm_caption](#fun-f3a683bcda)

<a id="fun-58b0856420"></a>

#### `format_latency_ms`

- **ID / 行**：`FUN-58B0856420` / `L8`（源码见本单元概览）
- **签名 / 返回**：`format_latency_ms(ms: int | None)` → `str`
- **职责**：As-built responsibility derived from `format_latency_ms` and its owning unit.
- **复杂度 / 风险**：分支 2；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2eacce73e8"></a>

#### `dedupe_llm_io_records`

- **ID / 行**：`FUN-2EACCE73E8` / `L16`（源码见本单元概览）
- **签名 / 返回**：`dedupe_llm_io_records(records: list[dict])` → `list[dict]`
- **职责**：Keep the latest record per stage (JSON retries append duplicates).
- **依赖**：order.append、rec.get
- **复杂度 / 风险**：分支 2；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-cfe09c603f"></a>

#### `merge_llm_io_with_stage_sources`

- **ID / 行**：`FUN-CFE09C603F` / `L28`（源码见本单元概览）
- **签名 / 返回**：`merge_llm_io_with_stage_sources(records: list[dict], stage_sources: dict)` → `list[dict]`
- **职责**：Prefer orchestrator trace model/latency (total wall time) over per-attempt stream timing.
- **依赖**：dedupe_llm_io_records、dict、get、merged.append、rec.get、stage_sources.get、trace.get
- **复杂度 / 风险**：分支 3；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f3a683bcda"></a>

#### `stage_llm_caption`

- **ID / 行**：`FUN-F3A683BCDA` / `L43`（源码见本单元概览）
- **签名 / 返回**：`stage_llm_caption(stage_sources: dict, stage: str)` → `str`
- **职责**：As-built responsibility derived from `stage_llm_caption` and its owning unit.
- **依赖**：format_latency_ms、get、short_model_name、stage_sources.get、trace.get
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-e782e5b762"></a>

### src/viz/llm_view.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E782E5B762 |
| 源码 | [src/viz/llm_view.py](../../src/viz/llm_view.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | LLM narrative panel. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[render_llm_panel](#fun-2bb63dcf3d) · [render_llm_sidebar](#fun-d200c30db1)

<a id="fun-2bb63dcf3d"></a>

#### `render_llm_panel`

- **ID / 行**：`FUN-2BB63DCF3D` / `L10`（源码见本单元概览）
- **签名 / 返回**：`render_llm_panel(report: dict)` → `None`
- **职责**：As-built responsibility derived from `render_llm_panel` and its owning unit.
- **依赖**：action_plan.split、bool、get、line.strip、llm.get、meta.get、reliability.get、report.get、st.caption、st.columns、st.error、st.info、st.markdown、st.write、str、strip、top_audit.get
- **复杂度 / 风险**：分支 17；跨度 66 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d200c30db1"></a>

#### `render_llm_sidebar`

- **ID / 行**：`FUN-D200C30DB1` / `L78`（源码见本单元概览）
- **签名 / 返回**：`render_llm_sidebar(report: dict)` → `None`
- **职责**：As-built responsibility derived from `render_llm_sidebar` and its owning unit.
- **依赖**：render_llm_panel
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-d8ab5e90b4"></a>

### src/viz/page_layout.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D8AB5E90B4 |
| 源码 | [src/viz/page_layout.py](../../src/viz/page_layout.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Shared Streamlit page chrome. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) |
| 验证状态 | selected |

#### 函数导航

[render_page_hero](#fun-0e7ecec1bd)

<a id="fun-0e7ecec1bd"></a>

#### `render_page_hero`

- **ID / 行**：`FUN-0E7ECEC1BD` / `L8`（源码见本单元概览）
- **签名 / 返回**：`render_page_hero(title: str, subtitle: str='')` → `None`
- **职责**：As-built responsibility derived from `render_page_hero` and its owning unit.
- **依赖**：st.markdown
- **复杂度 / 风险**：分支 1；跨度 6 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) · direct-dynamic

<a id="unit-87ec9bc982"></a>

### src/viz/pipeline_progress.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-87EC9BC982 |
| 源码 | [src/viz/pipeline_progress.py](../../src/viz/pipeline_progress.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Streamlit UI for pipeline step progress and live LLM I/O. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 19 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py)、[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py)、[tests/unit/test_pipeline_progress_live.py](../../tests/unit/test_pipeline_progress_live.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[pipeline_progress_headline](#fun-0b8c70cae4) · [_format_step](#fun-c1629a4de1) · [render_progress_steps](#fun-311ae39ba2) · [_render_llm_io_text](#fun-ad1fa5e595) · [_render_llm_output_panel](#fun-7dcbcf149d) · [is_streaming_llm_record](#fun-17c606facf) · [partition_llm_records_for_live](#fun-d82430a62e) · [render_live_llm_status_lightweight](#fun-4d69bae96d) · [render_live_llm_streams](#fun-c7365fb901) · [_filter_llm_io_records](#fun-c8f614ea56) · [render_llm_io_history](#fun-fa5a1c7f41) · [StreamlitProgressReporter.__init__](#fun-0d15b0afcc) · [StreamlitProgressReporter._paint](#fun-cf6dff11c9) · [StreamlitProgressReporter._on_change](#fun-518e29c44c) · [StreamlitProgressReporter._on_llm_begin](#fun-25b5bbb645) · [StreamlitProgressReporter.run_llm_stream](#fun-4d2f1f7990) · [StreamlitProgressReporter.run_llm_stream._gen](#fun-f822a4e8cf) · [StreamlitProgressReporter._on_llm_end](#fun-85e51e2ba9) · [StreamlitProgressReporter.complete](#fun-a18a4822f2)

<a id="fun-0b8c70cae4"></a>

#### `pipeline_progress_headline`

- **ID / 行**：`FUN-0B8C70CAE4` / `L21`（源码见本单元概览）
- **签名 / 返回**：`pipeline_progress_headline(steps: list[dict] | None)` → `str`
- **职责**：Human-readable summary of the current pipeline step for waiting UI.
- **依赖**：join、last.get、parts.append、s.get、step.get、str、strip
- **复杂度 / 风险**：分支 7；跨度 21 行；high
- **测试 / 验证**：[tests/unit/test_pipeline_progress_headline.py](../../tests/unit/test_pipeline_progress_headline.py) · direct-dynamic

<a id="fun-c1629a4de1"></a>

#### `_format_step`

- **ID / 行**：`FUN-C1629A4DE1` / `L44`（源码见本单元概览）
- **签名 / 返回**：`_format_step(step: PipelineProgressStep)` → `str`
- **职责**：As-built responsibility derived from `_format_step` and its owning unit.
- **依赖**：_STATUS_ICONS.get
- **复杂度 / 风险**：分支 6；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-311ae39ba2"></a>

#### `render_progress_steps`

- **ID / 行**：`FUN-311AE39BA2` / `L60`（源码见本单元概览）
- **签名 / 返回**：`render_progress_steps(steps: list[dict], *, title: str='生成步骤')` → `None`
- **职责**：As-built responsibility derived from `render_progress_steps` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：PipelineProgressStep、_format_step、raw.get、st.markdown
- **复杂度 / 风险**：分支 3；跨度 14 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-ad1fa5e595"></a>

#### `_render_llm_io_text`

- **ID / 行**：`FUN-AD1FA5E595` / `L76`（源码见本单元概览）
- **签名 / 返回**：`_render_llm_io_text(*, label: str, key: str, text: str, height: int=360)` → `None`
- **职责**：As-built responsibility derived from `_render_llm_io_text` and its owning unit.
- **依赖**：st.markdown、st.text_area
- **复杂度 / 风险**：分支 1；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7dcbcf149d"></a>

#### `_render_llm_output_panel`

- **ID / 行**：`FUN-7DCBCF149D` / `L89`（源码见本单元概览）
- **签名 / 返回**：`_render_llm_output_panel(*, stage: str, output: str, error: str | None=None, json_height: int=320, widget_key: str | None=None)` → `None`
- **职责**：As-built responsibility derived from `_render_llm_output_panel` and its owning unit.
- **依赖**：_render_llm_io_text、format_llm_narrative、format_llm_output、len、st.caption、st.error、st.markdown
- **复杂度 / 风险**：分支 2；跨度 22 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-17c606facf"></a>

#### `is_streaming_llm_record`

- **ID / 行**：`FUN-17C606FACF` / `L113`（源码见本单元概览）
- **签名 / 返回**：`is_streaming_llm_record(rec: dict)` → `bool`
- **职责**：True while an LLM call is in flight (begin → end, including partial output).
- **依赖**：rec.get
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_pipeline_progress_live.py](../../tests/unit/test_pipeline_progress_live.py) · direct-dynamic

<a id="fun-d82430a62e"></a>

#### `partition_llm_records_for_live`

- **ID / 行**：`FUN-D82430A62E` / `L122`（源码见本单元概览）
- **签名 / 返回**：`partition_llm_records_for_live(records: list[dict])` → `tuple[list[dict], list[dict]]`
- **职责**：Split in-flight LLM records from completed ones for the live generation panel.
- **依赖**：_filter_llm_io_records、is_streaming_llm_record
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：[tests/unit/test_pipeline_progress_live.py](../../tests/unit/test_pipeline_progress_live.py) · direct-dynamic

<a id="fun-4d69bae96d"></a>

#### `render_live_llm_status_lightweight`

- **ID / 行**：`FUN-4D69BAE96D` / `L130`（源码见本单元概览）
- **签名 / 返回**：`render_live_llm_status_lightweight(live: dict)` → `None`
- **职责**：Minimal LLM status for waiting UI — no text_area widgets (prevents Streamlit blank-screen).
- **依赖**：len、live.get、partition_llm_records_for_live、rec.get、st.caption、st.markdown、str
- **复杂度 / 风险**：分支 5；跨度 18 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) · direct-dynamic

<a id="fun-c7365fb901"></a>

#### `render_live_llm_streams`

- **ID / 行**：`FUN-C7365FB901` / `L150`（源码见本单元概览）
- **签名 / 返回**：`render_live_llm_streams(active: list[dict])` → `None`
- **职责**：Prominent streaming panel fed by background-thread chunk snapshots.
- **依赖**：_render_llm_io_text、enumerate、format_llm_output、format_messages、len、rec.get、st.caption、st.container、st.markdown
- **复杂度 / 风险**：分支 5；跨度 34 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c8f614ea56"></a>

#### `_filter_llm_io_records`

- **ID / 行**：`FUN-C8F614EA56` / `L186`（源码见本单元概览）
- **签名 / 返回**：`_filter_llm_io_records(records: list[dict])` → `list[dict]`
- **职责**：As-built responsibility derived from `_filter_llm_io_records` and its owning unit.
- **依赖**：any、r.get
- **复杂度 / 风险**：分支 1；跨度 17 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fa5a1c7f41"></a>

#### `render_llm_io_history`

- **ID / 行**：`FUN-FA5A1C7F41` / `L205`（源码见本单元概览）
- **签名 / 返回**：`render_llm_io_history(records: list[dict], *, title: str='智能体 I/O', expand_last: bool=False)` → `None`
- **职责**：Full-width LLM call history.
- **依赖**：_filter_llm_io_records、_render_llm_io_text、enumerate、format_latency_ms、format_llm_narrative、format_llm_output、format_messages、len、rec.get、st.caption、st.error、st.expander、st.markdown、str
- **复杂度 / 风险**：分支 13；跨度 48 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0d15b0afcc"></a>

#### `StreamlitProgressReporter.__init__`

- **ID / 行**：`FUN-0D15B0AFCC` / `L258`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter.__init__(self, *, progress_slot=None, llm_slot=None)` → `None`
- **职责**：As-built responsibility derived from `__init__` and its owning unit.
- **依赖**：__init__、self._paint、st.empty、super
- **复杂度 / 风险**：分支 0；跨度 7 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-cf6dff11c9"></a>

#### `StreamlitProgressReporter._paint`

- **ID / 行**：`FUN-CF6DFF11C9` / `L266`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter._paint(self, headline: str)` → `None`
- **职责**：As-built responsibility derived from `_paint` and its owning unit.
- **依赖**：_format_step、join、self._slot.info
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-518e29c44c"></a>

#### `StreamlitProgressReporter._on_change`

- **ID / 行**：`FUN-518E29C44C` / `L271`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter._on_change(self)` → `None`
- **职责**：As-built responsibility derived from `_on_change` and its owning unit.
- **依赖**：next、reversed、self._paint
- **复杂度 / 风险**：分支 3；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-25b5bbb645"></a>

#### `StreamlitProgressReporter._on_llm_begin`

- **ID / 行**：`FUN-25B5BBB645` / `L283`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter._on_llm_begin(self, stage: str, model: str, messages: list[dict[str, str]], label: str)` → `None`
- **职责**：As-built responsibility derived from `_on_llm_begin` and its owning unit.
- **依赖**：expander.caption、expander.empty、expander.text_area、format_messages、output_box.markdown、st.expander、st.markdown
- **复杂度 / 风险**：分支 2；跨度 21 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4d2f1f7990"></a>

#### `StreamlitProgressReporter.run_llm_stream`

- **ID / 行**：`FUN-4D2F1F7990` / `L305`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter.run_llm_stream(self, stage: str, chunk_iter)` → `str`
- **职责**：As-built responsibility derived from `run_llm_stream` and its owning unit.
- **依赖**：_gen、run_llm_stream、self._llm_blocks.get、st.write_stream、super
- **复杂度 / 风险**：分支 2；跨度 13 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f822a4e8cf"></a>

#### `StreamlitProgressReporter.run_llm_stream._gen`

- **ID / 行**：`FUN-F822A4E8CF` / `L310`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter.run_llm_stream._gen()` → `runtime/inferred`
- **职责**：As-built responsibility derived from `_gen` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-85e51e2ba9"></a>

#### `StreamlitProgressReporter._on_llm_end`

- **ID / 行**：`FUN-85E51E2BA9` / `L319`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter._on_llm_end(self, stage: str, output: str, *, error: str | None=None)` → `None`
- **职责**：As-built responsibility derived from `_on_llm_end` and its owning unit.
- **依赖**：_render_llm_output_panel、container、error、format_latency_ms、markdown、self._find_llm、self._llm_blocks.get
- **复杂度 / 风险**：分支 7；跨度 22 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a18a4822f2"></a>

#### `StreamlitProgressReporter.complete`

- **ID / 行**：`FUN-A18A4822F2` / `L342`（源码见本单元概览）
- **签名 / 返回**：`StreamlitProgressReporter.complete(self, *, ok: bool=True)` → `None`
- **职责**：As-built responsibility derived from `complete` and its owning unit.
- **依赖**：next、reversed、self._paint、self._slot.error、self._slot.success
- **复杂度 / 风险**：分支 3；跨度 11 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_archive_compat.py](../../tests/unit/test_archive_compat.py)、[tests/unit/test_report_invariant_gate.py](../../tests/unit/test_report_invariant_gate.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py) · direct-dynamic

<a id="unit-a63d87a7bb"></a>

### src/viz/replay_loader.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-A63D87A7BB |
| 源码 | [src/viz/replay_loader.py](../../src/viz/replay_loader.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Single entry point for UI replay — inspect + load_bundle or forensic snapshot. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) |
| 验证状态 | selected |

#### 函数导航

[load_replay_bundle](#fun-2838d79653)

<a id="fun-2838d79653"></a>

#### `load_replay_bundle`

- **ID / 行**：`FUN-2838D79653` / `L14`（源码见本单元概览）
- **签名 / 返回**：`load_replay_bundle(run_config: RunConfig)` → `tuple[dict[str, Any], dict[str, pd.DataFrame], dict[str, Any]]`
- **职责**：Load a saved run for replay or forensic review.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、inspect_run_archive、join、load_bundle、load_forensic_bundle、run_config.normalized
- **复杂度 / 风险**：分支 5；跨度 21 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py) · direct-dynamic

<a id="unit-4e47421947"></a>

### src/viz/report_views.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-4E47421947 |
| 源码 | [src/viz/report_views.py](../../src/viz/report_views.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Streamlit view renderers for institutional report and strategy map. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 4 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) |
| 验证状态 | selected |

#### 函数导航

[_embed_chart](#fun-6a488ebc85) · [_top_text_panel](#fun-d4c3b6faa5) · [render_institutional_report](#fun-c6d32e207c) · [render_strategy_map](#fun-3c8ba1f22e)

<a id="fun-6a488ebc85"></a>

#### `_embed_chart`

- **ID / 行**：`FUN-6A488EBC85` / `L31`（源码见本单元概览）
- **签名 / 返回**：`_embed_chart(data, analysis, report, tf, *, variant: str='main', watermark=None, projections=True, show_title: bool=True, iframe_height: int | None=None, chart_height: int | None=None)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `_embed_chart` and its owning unit.
- **依赖**：build_lightweight_chart_html、chart_iframe_height、get、max、st.iframe、st.markdown
- **复杂度 / 风险**：分支 3；跨度 39 行；low
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-d4c3b6faa5"></a>

#### `_top_text_panel`

- **ID / 行**：`FUN-D4C3B6FAA5` / `L72`（源码见本单元概览）
- **签名 / 返回**：`_top_text_panel(title: str, body_html: str)` → `None`
- **职责**：As-built responsibility derived from `_top_text_panel` and its owning unit.
- **依赖**：st.markdown
- **复杂度 / 风险**：分支 0；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c6d32e207c"></a>

#### `render_institutional_report`

- **ID / 行**：`FUN-C6D32E207C` / `L79`（源码见本单元概览）
- **签名 / 返回**：`render_institutional_report(report, data, analyses, *, hide_title: bool=False)` → `None`
- **职责**：One-page dashboard layout (reference: 4 top panels + 3-col body + 4 bottom panels).
- **依赖**：_embed_chart、_top_text_panel、bool、build_sentiment_donut、chart_iframe_height、conclusion_display_lines、dict、fig.update_layout、format_archived_run_config、format_report_branding、format_utc8、get、html.escape、item.get、join、meta.get、narratives.get、pipeline_status_label、render_bottom_row、render_decision_summary
- **复杂度 / 风险**：分支 12；跨度 153 行；high
- **测试 / 验证**：[tests/unit/test_aspice_high_risk_contracts.py](../../tests/unit/test_aspice_high_risk_contracts.py) · direct-dynamic

<a id="fun-3c8ba1f22e"></a>

#### `render_strategy_map`

- **ID / 行**：`FUN-3C8BA1F22E` / `L234`（源码见本单元概览）
- **签名 / 返回**：`render_strategy_map(report, data, analyses)` → `None`
- **职责**：As-built responsibility derived from `render_strategy_map` and its owning unit.
- **依赖**：_embed_chart、format_report_branding、render_decision_summary、render_final_decision_banner、render_footer、render_key_levels、render_strategy_sections、report.get、st.columns、st.markdown
- **复杂度 / 风险**：分支 1；跨度 21 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-ee18de86b2"></a>

### src/viz/run_config_panel.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EE18DE86B2 |
| 源码 | [src/viz/run_config_panel.py](../../src/viz/run_config_panel.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Streamlit run-config panel and replay controls. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 20 / 2 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) |
| 验证状态 | selected |

#### 函数导航

[mode_label_to_value](#fun-6478ef0ef9) · [mode_value_to_label](#fun-9df4825093) · [_apply_widget_state_from_run_config](#fun-a29290a4a9) · [_seed_run_config_widgets_if_needed](#fun-368d7e0325) · [_ensure_default_replay_run_id](#fun-dfbacecc76) · [_set_all_agent_llm_widgets](#fun-e60fed8b36) · [_analyst_checkbox_state](#fun-67955d3f49) · [_sync_stage_widgets_from_mode_preset](#fun-ac911b85c4) · [_on_advanced_toggle](#fun-fc0e4c8d13) · [_apply_mode_preset_to_widgets](#fun-4562c0a4e8) · [_advanced_core_stages_all_off](#fun-b8de98a787) · [selected_run_config](#fun-4712d21b11) · [_render_run_mode_guide](#fun-a56ca0818f) · [_on_open_replay_config](#fun-d6653fc459) · [render_sidebar_replay](#fun-8d7f136545) · [_render_replay_controls](#fun-fea885853a) · [_render_archive_import_only](#fun-302db0d19b) · [_render_archive_transfer_controls](#fun-c8de0e7538) · [_render_run_config_advanced_controls](#fun-5b83f91b90) · [render_run_config_panel](#fun-de6787dacc)

<a id="fun-6478ef0ef9"></a>

#### `mode_label_to_value`

- **ID / 行**：`FUN-6478EF0EF9` / `L45`（源码见本单元概览）
- **签名 / 返回**：`mode_label_to_value(label: str)` → `str`
- **职责**：As-built responsibility derived from `mode_label_to_value` and its owning unit.
- **依赖**：_MODE_LABEL_TO_VALUE.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9df4825093"></a>

#### `mode_value_to_label`

- **ID / 行**：`FUN-9DF4825093` / `L49`（源码见本单元概览）
- **签名 / 返回**：`mode_value_to_label(value: str)` → `str`
- **职责**：As-built responsibility derived from `mode_value_to_label` and its owning unit.
- **依赖**：_MODE_VALUE_TO_LABEL.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-a29290a4a9"></a>

#### `_apply_widget_state_from_run_config`

- **ID / 行**：`FUN-A29290A4A9` / `L53`（源码见本单元概览）
- **签名 / 返回**：`_apply_widget_state_from_run_config(config: RunConfig)` → `None`
- **职责**：As-built responsibility derived from `_apply_widget_state_from_run_config` and its owning unit.
- **依赖**：items、run_config_widget_state
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-368d7e0325"></a>

#### `_seed_run_config_widgets_if_needed`

- **ID / 行**：`FUN-368D7E0325` / `L58`（源码见本单元概览）
- **签名 / 返回**：`_seed_run_config_widgets_if_needed(seed: RunConfig, *, force: bool=False)` → `None`
- **职责**：As-built responsibility derived from `_seed_run_config_widgets_if_needed` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_ensure_default_replay_run_id、bool、run_config_widget_state、st.session_state.get、state.items、state.pop
- **复杂度 / 风险**：分支 4；跨度 13 行；low
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py) · direct-dynamic

<a id="fun-dfbacecc76"></a>

#### `_ensure_default_replay_run_id`

- **ID / 行**：`FUN-DFBACECC76` / `L73`（源码见本单元概览）
- **签名 / 返回**：`_ensure_default_replay_run_id()` → `None`
- **职责**：Pick first archive when replay is on but run_id missing — call before replay widgets.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：list_archives、row.get、st.session_state.get、str
- **复杂度 / 风险**：分支 2；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e60fed8b36"></a>

#### `_set_all_agent_llm_widgets`

- **ID / 行**：`FUN-E60FED8B36` / `L86`（源码见本单元概览）
- **签名 / 返回**：`_set_all_agent_llm_widgets(select: bool)` → `None`
- **职责**：As-built responsibility derived from `_set_all_agent_llm_widgets` and its owning unit.
- **复杂度 / 风险**：分支 2；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-67955d3f49"></a>

#### `_analyst_checkbox_state`

- **ID / 行**：`FUN-67955D3F49` / `L94`（源码见本单元概览）
- **签名 / 返回**：`_analyst_checkbox_state()` → `tuple[str, int]`
- **职责**：As-built responsibility derived from `_analyst_checkbox_state` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：len、st.session_state.get
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ac911b85c4"></a>

#### `_sync_stage_widgets_from_mode_preset`

- **ID / 行**：`FUN-AC911B85C4` / `L114`（源码见本单元概览）
- **签名 / 返回**：`_sync_stage_widgets_from_mode_preset()` → `None`
- **职责**：When advanced controls open, align stage/analyst widgets with the mode preset.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_MODE_LABEL_TO_VALUE.get、bool、items、key.startswith、run_config_for_mode、run_config_widget_state、st.session_state.get
- **复杂度 / 风险**：分支 3；跨度 11 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-fc0e4c8d13"></a>

#### `_on_advanced_toggle`

- **ID / 行**：`FUN-FC0E4C8D13` / `L127`（源码见本单元概览）
- **签名 / 返回**：`_on_advanced_toggle()` → `None`
- **职责**：As-built responsibility derived from `_on_advanced_toggle` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_sync_stage_widgets_from_mode_preset、st.session_state.get
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4562c0a4e8"></a>

#### `_apply_mode_preset_to_widgets`

- **ID / 行**：`FUN-4562C0A4E8` / `L132`（源码见本单元概览）
- **签名 / 返回**：`_apply_mode_preset_to_widgets(mode: str)` → `None`
- **职责**：When mode radio changes, re-seed LLM stage widgets from the mode preset.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：bool、items、run_config_for_mode、run_config_widget_state、st.session_state.get
- **复杂度 / 风险**：分支 3；跨度 12 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b8de98a787"></a>

#### `_advanced_core_stages_all_off`

- **ID / 行**：`FUN-B8DE98A787` / `L146`（源码见本单元概览）
- **签名 / 返回**：`_advanced_core_stages_all_off()` → `bool`
- **职责**：As-built responsibility derived from `_advanced_core_stages_all_off` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：any、st.session_state.get
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4712d21b11"></a>

#### `selected_run_config`

- **ID / 行**：`FUN-4712D21B11` / `L150`（源码见本单元概览）
- **签名 / 返回**：`selected_run_config()` → `RunConfig`
- **职责**：As-built responsibility derived from `selected_run_config` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：RunConfig、_MODE_LABEL_TO_VALUE.get、_advanced_core_stages_all_off、_analyst_checkbox_state、bool、normalized、run_config_for_mode、st.session_state.get、str、strip
- **复杂度 / 风险**：分支 7；跨度 60 行；medium
- **测试 / 验证**：[tests/unit/test_run_config_panel.py](../../tests/unit/test_run_config_panel.py) · direct-dynamic

<a id="fun-a56ca0818f"></a>

#### `_render_run_mode_guide`

- **ID / 行**：`FUN-A56CA0818F` / `L212`（源码见本单元概览）
- **签名 / 返回**：`_render_run_mode_guide()` → `None`
- **职责**：As-built responsibility derived from `_render_run_mode_guide` and its owning unit.
- **依赖**：st.markdown
- **复杂度 / 风险**：分支 0；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d6653fc459"></a>

#### `_on_open_replay_config`

- **ID / 行**：`FUN-D6653FC459` / `L234`（源码见本单元概览）
- **签名 / 返回**：`_on_open_replay_config()` → `None`
- **职责**：Sidebar — jump to config panel with replay mode pre-selected.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：st.session_state.pop
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-8d7f136545"></a>

#### `render_sidebar_replay`

- **ID / 行**：`FUN-8D7F136545` / `L244`（源码见本单元概览）
- **签名 / 返回**：`render_sidebar_replay()` → `None`
- **职责**：Always visible in sidebar — entry point for historical replay.
- **依赖**：len、list_archives、st.sidebar.button、st.sidebar.caption、st.sidebar.markdown
- **复杂度 / 风险**：分支 1；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fea885853a"></a>

#### `_render_replay_controls`

- **ID / 行**：`FUN-FEA885853A` / `L265`（源码见本单元概览）
- **签名 / 返回**：`_render_replay_controls()` → `None`
- **职责**：As-built responsibility derived from `_render_replay_controls` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_ensure_default_replay_run_id、_render_archive_import_only、_render_archive_transfer_controls、archive_label、len、list、list_archives、next、options.get、options.keys、row.get、selected.get、st.caption、st.checkbox、st.info、st.markdown、st.selectbox、st.session_state.get、st.warning、str
- **复杂度 / 风险**：分支 5；跨度 50 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-302db0d19b"></a>

#### `_render_archive_import_only`

- **ID / 行**：`FUN-302DB0D19B` / `L317`（源码见本单元概览）
- **签名 / 返回**：`_render_archive_import_only()` → `None`
- **职责**：As-built responsibility derived from `_render_archive_import_only` and its owning unit.
- **依赖**：import_archive_zip、st.button、st.error、st.file_uploader、st.rerun、st.success、str、uploaded.getvalue
- **复杂度 / 风险**：分支 2；跨度 16 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-c8de0e7538"></a>

#### `_render_archive_transfer_controls`

- **ID / 行**：`FUN-C8DE0E7538` / `L335`（源码见本单元概览）
- **签名 / 返回**：`_render_archive_transfer_controls(selected_id: str)` → `None`
- **职责**：As-built responsibility derived from `_render_archive_transfer_controls` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：export_archive_zip、import_archive_zip、st.button、st.caption、st.columns、st.download_button、st.error、st.file_uploader、st.rerun、st.success、str、uploaded.getvalue
- **复杂度 / 风险**：分支 4；跨度 34 行；high
- **测试 / 验证**：— · static-and-component

<a id="fun-5b83f91b90"></a>

#### `_render_run_config_advanced_controls`

- **ID / 行**：`FUN-5B83F91B90` / `L371`（源码见本单元概览）
- **签名 / 返回**：`_render_run_config_advanced_controls()` → `None`
- **职责**：As-built responsibility derived from `_render_run_config_advanced_controls` and its owning unit.
- **依赖**：_analyst_checkbox_state、enumerate、st.button、st.checkbox、st.columns、st.markdown、st.warning
- **复杂度 / 风险**：分支 5；跨度 38 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-de6787dacc"></a>

#### `render_run_config_panel`

- **ID / 行**：`FUN-DE6787DACC` / `L411`（源码见本单元概览）
- **签名 / 返回**：`render_run_config_panel()` → `None`
- **职责**：As-built responsibility derived from `render_run_config_panel` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_MODE_LABEL_TO_VALUE.get、_analyst_checkbox_state、_apply_mode_preset_to_widgets、_render_replay_controls、_render_run_config_advanced_controls、_render_run_mode_guide、_seed_run_config_widgets_if_needed、bool、config.fingerprint、config.to_dict、default_panel_run_config、get、inspect_run_archive、inspection.manifest.get、invalidate_report_cache、list、llm_configured、log.info、render_page_hero、seed.fingerprint
- **复杂度 / 风险**：分支 14；跨度 104 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-6fa4e87f8a"></a>

### src/viz/session_keys.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6FA4E87F8A |
| 源码 | [src/viz/session_keys.py](../../src/viz/session_keys.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Streamlit session keys and report cache helpers. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 5 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[session_id](#fun-0eec7855b3) · [generation_id](#fun-ba937173ed) · [job_key](#fun-4d0107c2b8) · [rotate_generation_id](#fun-47ff82aecf) · [invalidate_report_cache](#fun-35b294ebf2)

<a id="fun-0eec7855b3"></a>

#### `session_id`

- **ID / 行**：`FUN-0EEC7855B3` / `L23`（源码见本单元概览）
- **签名 / 返回**：`session_id()` → `str`
- **职责**：As-built responsibility derived from `session_id` and its owning unit.
- **依赖**：str、uuid.uuid4
- **复杂度 / 风险**：分支 1；跨度 4 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-ba937173ed"></a>

#### `generation_id`

- **ID / 行**：`FUN-BA937173ED` / `L29`（源码见本单元概览）
- **签名 / 返回**：`generation_id()` → `str`
- **职责**：As-built responsibility derived from `generation_id` and its owning unit.
- **依赖**：str、uuid.uuid4
- **复杂度 / 风险**：分支 1；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4d0107c2b8"></a>

#### `job_key`

- **ID / 行**：`FUN-4D0107C2B8` / `L35`（源码见本单元概览）
- **签名 / 返回**：`job_key()` → `str`
- **职责**：As-built responsibility derived from `job_key` and its owning unit.
- **依赖**：generation_id、session_id
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_generation_worker.py](../../tests/unit/test_generation_worker.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-47ff82aecf"></a>

#### `rotate_generation_id`

- **ID / 行**：`FUN-47FF82AECF` / `L39`（源码见本单元概览）
- **签名 / 返回**：`rotate_generation_id()` → `str`
- **职责**：As-built responsibility derived from `rotate_generation_id` and its owning unit.
- **依赖**：str、uuid.uuid4
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-35b294ebf2"></a>

#### `invalidate_report_cache`

- **ID / 行**：`FUN-35B294EBF2` / `L45`（源码见本单元概览）
- **签名 / 返回**：`invalidate_report_cache()` → `None`
- **职责**：As-built responsibility derived from `invalidate_report_cache` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：drop_job、job_key、rotate_generation_id、session_id、st.session_state.pop
- **复杂度 / 风险**：分支 0；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-f568ea7ece"></a>

### src/viz/source_labels.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-F568EA7ECE |
| 源码 | [src/viz/source_labels.py](../../src/viz/source_labels.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Source badge helpers — label rule vs LLM outputs. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 8 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) |
| 验证状态 | selected |

#### 函数导航

[is_llm_source](#fun-6c5c91dc85) · [llm_was_invoked](#fun-198b94558c) · [stage_meta_label](#fun-e190f43fff) · [source_label](#fun-7203478796) · [stage_source](#fun-154472495a) · [render_source_badge](#fun-757465430c) · [render_stage_meta_badge](#fun-405b8cf26d) · [render_agent_source_banner](#fun-0149440496)

<a id="fun-6c5c91dc85"></a>

#### `is_llm_source`

- **ID / 行**：`FUN-6C5C91DC85` / `L35`（源码见本单元概览）
- **签名 / 返回**：`is_llm_source(source: str | None)` → `bool`
- **职责**：As-built responsibility derived from `is_llm_source` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-198b94558c"></a>

#### `llm_was_invoked`

- **ID / 行**：`FUN-198B94558C` / `L39`（源码见本单元概览）
- **签名 / 返回**：`llm_was_invoked(meta: dict)` → `bool`
- **职责**：True if an LLM call was made for this stage (even when rule output was chosen).
- **依赖**：bool、llm.get、meta.get
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py) · direct-dynamic

<a id="fun-e190f43fff"></a>

#### `stage_meta_label`

- **ID / 行**：`FUN-E190F43FFF` / `L48`（源码见本单元概览）
- **签名 / 返回**：`stage_meta_label(meta: dict)` → `str`
- **职责**：Human label for a stage_sources / stage_meta entry.
- **依赖**：llm.get、llm_was_invoked、meta.get、strip
- **复杂度 / 风险**：分支 5；跨度 13 行；medium
- **测试 / 验证**：[tests/unit/test_source_labels.py](../../tests/unit/test_source_labels.py) · direct-dynamic

<a id="fun-7203478796"></a>

#### `source_label`

- **ID / 行**：`FUN-7203478796` / `L63`（源码见本单元概览）
- **签名 / 返回**：`source_label(source: str | None)` → `str`
- **职责**：As-built responsibility derived from `source_label` and its owning unit.
- **依赖**：SOURCE_LABELS.get
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_agent_chain.py](../../tests/unit/test_agent_chain.py)、[tests/unit/test_analyst_input_density.py](../../tests/unit/test_analyst_input_density.py)、[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_archive_optimizations.py](../../tests/unit/test_archive_optimizations.py)、[tests/unit/test_archive_transfer.py](../../tests/unit/test_archive_transfer.py)、[tests/unit/test_claim_eligibility.py](../../tests/unit/test_claim_eligibility.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_external_data_view.py](../../tests/unit/test_external_data_view.py)、[tests/unit/test_llm_levels.py](../../tests/unit/test_llm_levels.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_authorization.py](../../tests/unit/test_narrative_authorization.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_orchestrator_hooks.py](../../tests/unit/test_orchestrator_hooks.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_run_archive.py](../../tests/unit/test_run_archive.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py)、[tests/unit/test_technical_context_lux.py](../../tests/unit/test_technical_context_lux.py)、[tests/unit/test_trader_sentiment.py](../../tests/unit/test_trader_sentiment.py) · direct-dynamic

<a id="fun-154472495a"></a>

#### `stage_source`

- **ID / 行**：`FUN-154472495A` / `L67`（源码见本单元概览）
- **签名 / 返回**：`stage_source(report: dict, stage: str)` → `str`
- **职责**：As-built responsibility derived from `stage_source` and its owning unit.
- **依赖**：entry.get、get、meta.get、report.get
- **复杂度 / 风险**：分支 0；跨度 4 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-757465430c"></a>

#### `render_source_badge`

- **ID / 行**：`FUN-757465430C` / `L73`（源码见本单元概览）
- **签名 / 返回**：`render_source_badge(source: str | None, *, small: bool=False)` → `str`
- **职责**：As-built responsibility derived from `render_source_badge` and its owning unit.
- **依赖**：is_llm_source、source_label
- **复杂度 / 风险**：分支 2；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-405b8cf26d"></a>

#### `render_stage_meta_badge`

- **ID / 行**：`FUN-405B8CF26D` / `L81`（源码见本单元概览）
- **签名 / 返回**：`render_stage_meta_badge(meta: dict, *, small: bool=False)` → `str`
- **职责**：As-built responsibility derived from `render_stage_meta_badge` and its owning unit.
- **依赖**：llm_was_invoked、stage_meta_label
- **复杂度 / 风险**：分支 2；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-0149440496"></a>

#### `render_agent_source_banner`

- **ID / 行**：`FUN-0149440496` / `L89`（源码见本单元概览）
- **签名 / 返回**：`render_agent_source_banner(report: dict)` → `str`
- **职责**：Horizontal strip showing each pipeline stage source.
- **依赖**：MODE_LABELS.get、STAGE_LABELS.get、chips.append、entry.get、join、llm.get、llm_was_invoked、meta.get、render_source_badge、render_stage_meta_badge、report.get、short_model_name
- **复杂度 / 风险**：分支 5；跨度 49 行；medium
- **测试 / 验证**：— · static-and-component

<a id="unit-202db41fe0"></a>

### src/viz/streamlit_common.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-202DB41FE0 |
| 源码 | [src/viz/streamlit_common.py](../../src/viz/streamlit_common.py) |
| 架构组件 | ARC-VIZ — Streamlit 展示 |
| 职责 | Shared Streamlit bootstrap, report session cache, sidebar. |
| 关联需求 | [SWR-REP-004](./SWE.1-software-requirements.md#swr-rep-004)、[SWR-ARC-002](./SWE.1-software-requirements.md#swr-arc-002)、[SWR-UI-001](./SWE.1-software-requirements.md#swr-ui-001)、[SWR-UI-002](./SWE.1-software-requirements.md#swr-ui-002)、[SWR-NFR-002](./SWE.1-software-requirements.md#swr-nfr-002) |
| 函数 / 高风险函数 | 20 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](./SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) |
| 验证状态 | selected |

#### 函数导航

[_session_id](#fun-2fd5708c36) · [_generation_id](#fun-b7dfde89b4) · [_job_key](#fun-675c7168fc) · [bootstrap_env](#fun-4bd443c8f3) · [missing_runtime_dependencies](#fun-cd1e50e1de) · [render_runtime_dependency_banner](#fun-86e5501024) · [page_setup](#fun-d2be30af9f) · [init_page](#fun-aff4dbd771) · [_on_request_reconfigure](#fun-4a59a3158d) · [render_sidebar_refresh_button](#fun-4a02ec5564) · [render_sidebar_header](#fun-e229df7619) · [render_sidebar_footer](#fun-943d58e197) · [_resolve_confirmed_run_config](#fun-460dffdb7c) · [_render_waiting_ui](#fun-9a85354a87) · [_render_waiting_ui._live_poll](#fun-19d89f3693) · [_render_external_waiting](#fun-db56a44e6c) · [_render_external_waiting._poll](#fun-4cb4b42e37) · [ensure_external_data](#fun-cd1636a5b5) · [ensure_report](#fun-2543fa4f8f) · [_store_report_bundle](#fun-2268bf01ca)

<a id="fun-2fd5708c36"></a>

#### `_session_id`

- **ID / 行**：`FUN-2FD5708C36` / `L57`（源码见本单元概览）
- **签名 / 返回**：`_session_id()` → `str`
- **职责**：As-built responsibility derived from `_session_id` and its owning unit.
- **依赖**：str、uuid.uuid4
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b7dfde89b4"></a>

#### `_generation_id`

- **ID / 行**：`FUN-B7DFDE89B4` / `L63`（源码见本单元概览）
- **签名 / 返回**：`_generation_id()` → `str`
- **职责**：As-built responsibility derived from `_generation_id` and its owning unit.
- **依赖**：str、uuid.uuid4
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-675c7168fc"></a>

#### `_job_key`

- **ID / 行**：`FUN-675C7168FC` / `L69`（源码见本单元概览）
- **签名 / 返回**：`_job_key()` → `str`
- **职责**：As-built responsibility derived from `_job_key` and its owning unit.
- **依赖**：_generation_id、_session_id
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4bd443c8f3"></a>

#### `bootstrap_env`

- **ID / 行**：`FUN-4BD443C8F3` / `L73`（源码见本单元概览）
- **签名 / 返回**：`bootstrap_env()` → `None`
- **职责**：As-built responsibility derived from `bootstrap_env` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem;shared-state / caller-thread
- **依赖**：Path、env_path.exists、env_path.read_text、key.strip、line.split、line.startswith、line.strip、os.environ.get、os.environ.setdefault、resolve、server.split、splitlines、strip、val.strip、winreg.CloseKey、winreg.OpenKey、winreg.QueryValueEx
- **复杂度 / 风险**：分支 8；跨度 32 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-cd1e50e1de"></a>

#### `missing_runtime_dependencies`

- **ID / 行**：`FUN-CD1E50E1DE` / `L107`（源码见本单元概览）
- **签名 / 返回**：`missing_runtime_dependencies()` → `list[str]`
- **职责**：Packages required for live report generation (not replay-only).
- **依赖**：missing.append
- **复杂度 / 风险**：分支 1；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-86e5501024"></a>

#### `render_runtime_dependency_banner`

- **ID / 行**：`FUN-86E5501024` / `L117`（源码见本单元概览）
- **签名 / 返回**：`render_runtime_dependency_banner()` → `None`
- **职责**：As-built responsibility derived from `render_runtime_dependency_banner` and its owning unit.
- **依赖**：join、missing_runtime_dependencies、st.error
- **复杂度 / 风险**：分支 1；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d2be30af9f"></a>

#### `page_setup`

- **ID / 行**：`FUN-D2BE30AF9F` / `L129`（源码见本单元概览）
- **签名 / 返回**：`page_setup()` → `None`
- **职责**：As-built responsibility derived from `page_setup` and its owning unit.
- **依赖**：bootstrap_env、setup_logging、st.markdown
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-aff4dbd771"></a>

#### `init_page`

- **ID / 行**：`FUN-AFF4DBD771` / `L137`（源码见本单元概览）
- **签名 / 返回**：`init_page(*, title_suffix: str='')` → `None`
- **职责**：As-built responsibility derived from `init_page` and its owning unit.
- **依赖**：bootstrap_env、setup_logging、st.markdown、st.set_page_config
- **复杂度 / 风险**：分支 1；跨度 10 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4a59a3158d"></a>

#### `_on_request_reconfigure`

- **ID / 行**：`FUN-4A59A3158D` / `L149`（源码见本单元概览）
- **签名 / 返回**：`_on_request_reconfigure()` → `None`
- **职责**：As-built responsibility derived from `_on_request_reconfigure` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：log.info、st.session_state.pop
- **复杂度 / 风险**：分支 0；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4a02ec5564"></a>

#### `render_sidebar_refresh_button`

- **ID / 行**：`FUN-4A02EC5564` / `L158`（源码见本单元概览）
- **签名 / 返回**：`render_sidebar_refresh_button()` → `None`
- **职责**：As-built responsibility derived from `render_sidebar_refresh_button` and its owning unit.
- **依赖**：st.sidebar.button
- **复杂度 / 风险**：分支 0；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e229df7619"></a>

#### `render_sidebar_header`

- **ID / 行**：`FUN-E229DF7619` / `L167`（源码见本单元概览）
- **签名 / 返回**：`render_sidebar_header()` → `None`
- **职责**：As-built responsibility derived from `render_sidebar_header` and its owning unit.
- **依赖**：render_sidebar_refresh_button、render_sidebar_replay、short_model_name、st.sidebar.caption、st.sidebar.markdown
- **复杂度 / 风险**：分支 2；跨度 18 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-943d58e197"></a>

#### `render_sidebar_footer`

- **ID / 行**：`FUN-943D58E197` / `L187`（源码见本单元概览）
- **签名 / 返回**：`render_sidebar_footer(data: dict | None=None)` → `None`
- **职责**：As-built responsibility derived from `render_sidebar_footer` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：active_config.fingerprint、coerce_run_config、indicator_snapshot、indicator_table_rows、mode_value_to_label、st.session_state.get、st.sidebar.caption、st.sidebar.expander、st.table
- **复杂度 / 风险**：分支 2；跨度 11 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-460dffdb7c"></a>

#### `_resolve_confirmed_run_config`

- **ID / 行**：`FUN-460DFFDB7C` / `L200`（源码见本单元概览）
- **签名 / 返回**：`_resolve_confirmed_run_config()` → `RunConfig | None`
- **职责**：As-built responsibility derived from `_resolve_confirmed_run_config` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：coerce_run_config、st.session_state.get
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9a85354a87"></a>

#### `_render_waiting_ui`

- **ID / 行**：`FUN-9A85354A87` / `L204`（源码见本单元概览）
- **签名 / 返回**：`_render_waiting_ui(job_key_str: str, *, show_generation_ui: bool)` → `None`
- **职责**：As-built responsibility derived from `_render_waiting_ui` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_live_poll、_session_id、get_job、live.get、llm_slot.container、log.exception、pipeline_progress_headline、render_live_llm_status_lightweight、render_page_hero、render_progress_steps、st.caption、st.empty、st.fragment、st.rerun、st.warning、steps_slot.container、timedelta
- **复杂度 / 风险**：分支 6；跨度 37 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-19d89f3693"></a>

#### `_render_waiting_ui._live_poll`

- **ID / 行**：`FUN-19D89F3693` / `L220`（源码见本单元概览）
- **签名 / 返回**：`_render_waiting_ui._live_poll()` → `None`
- **职责**：As-built responsibility derived from `_live_poll` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_session_id、get_job、live.get、llm_slot.container、log.exception、pipeline_progress_headline、render_live_llm_status_lightweight、render_progress_steps、st.caption、st.fragment、st.rerun、st.warning、steps_slot.container、timedelta
- **复杂度 / 风险**：分支 5；跨度 19 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-db56a44e6c"></a>

#### `_render_external_waiting`

- **ID / 行**：`FUN-DB56A44E6C` / `L243`（源码见本单元概览）
- **签名 / 返回**：`_render_external_waiting(job_key_str: str)` → `None`
- **职责**：As-built responsibility derived from `_render_external_waiting` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_poll、_session_id、get_job、live.get、llm_slot.container、log.exception、pipeline_progress_headline、render_live_llm_status_lightweight、render_page_hero、render_progress_steps、st.empty、st.fragment、st.info、st.rerun、st.warning、steps_slot.container、timedelta
- **复杂度 / 风险**：分支 5；跨度 37 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-4cb4b42e37"></a>

#### `_render_external_waiting._poll`

- **ID / 行**：`FUN-4CB4B42E37` / `L258`（源码见本单元概览）
- **签名 / 返回**：`_render_external_waiting._poll()` → `None`
- **职责**：As-built responsibility derived from `_poll` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_session_id、get_job、live.get、llm_slot.container、log.exception、pipeline_progress_headline、render_live_llm_status_lightweight、render_progress_steps、st.fragment、st.info、st.rerun、st.warning、steps_slot.container、timedelta
- **复杂度 / 风险**：分支 5；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-cd1636a5b5"></a>

#### `ensure_external_data`

- **ID / 行**：`FUN-CD1636A5B5` / `L282`（源码见本单元概览）
- **签名 / 返回**：`ensure_external_data()` → `dict`
- **职责**：As-built responsibility derived from `ensure_external_data` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_generation_id、_job_key、_render_external_waiting、_resolve_confirmed_run_config、_session_id、external_payload_from_report、format_generation_error、get_job、invalidate_report_cache、job.live.get、load_replay_bundle、log.exception、purge_expired、render_run_config_panel、run_config.fingerprint、st.error、st.session_state.get、st.session_state.pop、st.stop、start_generation
- **复杂度 / 风险**：分支 10；跨度 56 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2543fa4f8f"></a>

#### `ensure_report`

- **ID / 行**：`FUN-2543FA4F8F` / `L340`（源码见本单元概览）
- **签名 / 返回**：`ensure_report(*, show_generation_ui: bool=True)` → `tuple[dict, dict, dict]`
- **职责**：As-built responsibility derived from `ensure_report` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / shared-state / caller-thread
- **依赖**：_generation_id、_job_key、_render_waiting_ui、_resolve_confirmed_run_config、_session_id、_store_report_bundle、format_generation_error、get_job、invalidate_report_cache、job.live.get、log.exception、purge_expired、render_progress_steps、render_run_config_panel、run_config.fingerprint、st.caption、st.error、st.markdown、st.session_state.get、st.session_state.pop
- **复杂度 / 风险**：分支 8；跨度 49 行；medium
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="fun-2268bf01ca"></a>

#### `_store_report_bundle`

- **ID / 行**：`FUN-2268BF01CA` / `L391`（源码见本单元概览）
- **签名 / 返回**：`_store_report_bundle(job_key_str: str, bundle: tuple[dict, dict, dict], run_config_fingerprint: str)` → `tuple[dict, dict, dict]`
- **职责**：As-built responsibility derived from `_store_report_bundle` and its owning unit.
- **依赖**：_generation_id、_session_id、drop_job
- **复杂度 / 风险**：分支 0；跨度 10 行；low
- **测试 / 验证**：[tests/regression/test_fixes.py](../../tests/regression/test_fixes.py)、[tests/unit/test_streamlit_ensure_report.py](../../tests/unit/test_streamlit_ensure_report.py) · direct-dynamic

<a id="arc-tools"></a>

## ARC-TOOLS — 开发、审核与运维工具

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [scripts/chart_compare_test.py](#unit-670f7f7454) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/check_aspice_assets.py](#unit-de82d6e44b) | 20 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/check_mt5_connection.py](#unit-d4b396b36e) | 1 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/close_fixed_issues.py](#unit-9572f90802) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/compare_pa_5m_tv.py](#unit-b4a1accfa2) | 1 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/compare_pa_tv.py](#unit-8e5050cae9) | 2 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/create_system_test_issues.py](#unit-eefb367071) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/estimate_llm_tokens.py](#unit-3fa67ae3bf) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/export_sample_report.py](#unit-2781538ff5) | 3 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/generate_aspice_readable_docs.py](#unit-44da65110b) | 22 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/generate_aspice_software_evidence.py](#unit-70ee096332) | 13 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/inspect_archive.py](#unit-37e036c51b) | 6 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/regression_test.py](#unit-ebde8e6443) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/replay_llm_narrative.py](#unit-3960e281ab) | 4 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/run_pipeline_test.py](#unit-d538889607) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |
| [scripts/show_utf8.py](#unit-8f71f01664) | 2 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/test_live_fetch.py](#unit-c913c2495c) | 2 | 1 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) | selected |
| [scripts/test_llm_json_fix.py](#unit-76c5f6645c) | 0 | 0 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) | selected |

<a id="unit-670f7f7454"></a>

### scripts/chart_compare_test.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-670F7F7454 |
| 源码 | [scripts/chart_compare_test.py](../../scripts/chart_compare_test.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Backward-compatible shim → tests/tools/chart_compare.py |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-de82d6e44b"></a>

### scripts/check_aspice_assets.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DE82D6E44B |
| 源码 | [scripts/check_aspice_assets.py](../../scripts/check_aspice_assets.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Generate and validate Automotive SPICE governance assets. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 20 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../tests/regression/test_aspice_assets.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) |
| 验证状态 | selected |

#### 函数导航

[stable_id](#fun-be28bb75d8) · [read_yaml](#fun-04a944fece) · [rel](#fun-6d47944494) · [source_files](#fun-6175ef47cc) · [document_files](#fun-7b527c5c90) · [document_classification](#fun-5ae4fdb3fc) · [document_title](#fun-64eed0d566) · [build_document_register](#fun-fc561d92db) · [component_for](#fun-3c97caee46) · [module_doc](#fun-f9f01026c2) · [build_units](#fun-d410be7a27) · [build_trace_rows](#fun-2ceb1f60f7) · [dependency_outputs](#fun-beae13cf69) · [csv_text](#fun-c861d95e3c) · [process_index](#fun-cee22c60cc) · [expected_outputs](#fun-e18bb2dfa3) · [validate_model](#fun-3c81471a20) · [write_outputs](#fun-f855325a7a) · [check_outputs](#fun-e57502a017) · [main](#fun-4aa307b1b4)

<a id="fun-be28bb75d8"></a>

#### `stable_id`

- **ID / 行**：`FUN-BE28BB75D8` / `L55`（源码见本单元概览）
- **签名 / 返回**：`stable_id(prefix: str, value: str)` → `str`
- **职责**：As-built responsibility derived from `stable_id` and its owning unit.
- **依赖**：hashlib.sha1、hexdigest、upper、value.encode
- **复杂度 / 风险**：分支 0；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-04a944fece"></a>

#### `read_yaml`

- **ID / 行**：`FUN-04A944FECE` / `L60`（源码见本单元概览）
- **签名 / 返回**：`read_yaml(path: Path)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `read_yaml` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、isinstance、path.read_text、path.relative_to、yaml.safe_load
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-6d47944494"></a>

#### `rel`

- **ID / 行**：`FUN-6D47944494` / `L67`（源码见本单元概览）
- **签名 / 返回**：`rel(path: Path)` → `str`
- **职责**：As-built responsibility derived from `rel` and its owning unit.
- **依赖**：as_posix、path.relative_to
- **复杂度 / 风险**：分支 0；跨度 2 行；medium
- **测试 / 验证**：[tests/unit/test_golden_report_benchmark.py](../../tests/unit/test_golden_report_benchmark.py)、[tests/unit/test_report_reliability.py](../../tests/unit/test_report_reliability.py) · direct-dynamic

<a id="fun-6175ef47cc"></a>

#### `source_files`

- **ID / 行**：`FUN-6175EF47CC` / `L71`（源码见本单元概览）
- **签名 / 返回**：`source_files()` → `list[Path]`
- **职责**：As-built responsibility derived from `source_files` and its owning unit.
- **依赖**：ROOT.rglob、any、casefold、path.relative_to、rel、sorted
- **复杂度 / 风险**：分支 0；跨度 9 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-7b527c5c90"></a>

#### `document_files`

- **ID / 行**：`FUN-7B527C5C90` / `L82`（源码见本单元概览）
- **签名 / 返回**：`document_files()` → `list[Path]`
- **职责**：As-built responsibility derived from `document_files` and its owning unit.
- **依赖**：ROOT.glob、casefold、path.exists、path.is_file、paths.update、rel、rglob、sorted
- **复杂度 / 风险**：分支 1；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-5ae4fdb3fc"></a>

#### `document_classification`

- **ID / 行**：`FUN-5AE4FDB3FC` / `L91`（源码见本单元概览）
- **签名 / 返回**：`document_classification(path: Path)` → `tuple[str, str, str, str]`
- **职责**：As-built responsibility derived from `document_classification` and its owning unit.
- **依赖**：path_str.startswith、rel
- **复杂度 / 风险**：分支 23；跨度 65 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-64eed0d566"></a>

#### `document_title`

- **ID / 行**：`FUN-64EED0D566` / `L158`（源码见本单元概览）
- **签名 / 返回**：`document_title(path: Path)` → `str`
- **职责**：As-built responsibility derived from `document_title` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：match.group、path.exists、path.read_text、path.stem.replace、path.suffix.lower、re.search、replace、strip
- **复杂度 / 风险**：分支 2；跨度 7 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-fc561d92db"></a>

#### `build_document_register`

- **ID / 行**：`FUN-FC561D92DB` / `L167`（源码见本单元概览）
- **签名 / 返回**：`build_document_register()` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `build_document_register` and its owning unit.
- **依赖**：document_classification、document_files、document_title、rel、rows.append、stable_id
- **复杂度 / 风险**：分支 3；跨度 20 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3c97caee46"></a>

#### `component_for`

- **ID / 行**：`FUN-3C97CAEE46` / `L189`（源码见本单元概览）
- **签名 / 返回**：`component_for(path: Path)` → `str`
- **职责**：As-built responsibility derived from `component_for` and its owning unit.
- **依赖**：rel、value.startswith
- **复杂度 / 风险**：分支 10；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f9f01026c2"></a>

#### `module_doc`

- **ID / 行**：`FUN-F9F01026C2` / `L214`（源码见本单元概览）
- **签名 / 返回**：`module_doc(tree: ast.AST, component_name: str)` → `str`
- **职责**：As-built responsibility derived from `module_doc` and its owning unit.
- **依赖**：ast.get_docstring、doc.splitlines
- **复杂度 / 风险**：分支 1；跨度 3 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-d410be7a27"></a>

#### `build_units`

- **ID / 行**：`FUN-D410BE7A27` / `L219`（源码见本单元概览）
- **签名 / 返回**：`build_units(arch: dict[str, Any])` → `tuple[list[dict[str, str]], list[dict[str, str]]]`
- **职责**：As-built responsibility derived from `build_units` and its owning unit.
- **依赖**：ast.iter_child_nodes、ast.parse、ast.walk、component_for、functions.append、int、isinstance、join、module_doc、node.name.startswith、owners.append、parents.get、path.read_text、rel、reversed、sorted、source_files、stable_id、str、units.append
- **复杂度 / 风险**：分支 8；跨度 57 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-2ceb1f60f7"></a>

#### `build_trace_rows`

- **ID / 行**：`FUN-2CEB1F60F7` / `L278`（源码见本单元概览）
- **签名 / 返回**：`build_trace_rows(reqs: dict[str, Any], units: list[dict[str, str]])` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `build_trace_rows` and its owning unit.
- **依赖**：append、defaultdict、join、rows.append、sorted
- **复杂度 / 风险**：分支 2；跨度 19 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-beae13cf69"></a>

#### `dependency_outputs`

- **ID / 行**：`FUN-BEAE13CF69` / `L299`（源码见本单元概览）
- **签名 / 返回**：`dependency_outputs(report: dict[str, Any])` → `tuple[str, str]`
- **职责**：As-built responsibility derived from `dependency_outputs` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：archive.get、components.append、get、hashes.get、item.get、join、json.dumps、lock_lines.append、lower、name.lower、replace、report.get、sorted
- **复杂度 / 风险**：分支 3；跨度 35 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-c861d95e3c"></a>

#### `csv_text`

- **ID / 行**：`FUN-C861D95E3C` / `L336`（源码见本单元概览）
- **签名 / 返回**：`csv_text(rows: list[dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `csv_text` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、buffer.getvalue、csv.DictWriter、io.StringIO、list、writer.writeheader、writer.writerows
- **复杂度 / 风险**：分支 1；跨度 8 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-cee22c60cc"></a>

#### `process_index`

- **ID / 行**：`FUN-CEE22C60CC` / `L346`（源码见本单元概览）
- **签名 / 返回**：`process_index(rows: list[dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `process_index` and its owning unit.
- **依赖**：append、defaultdict、join、lines.append、lines.extend、removeprefix、sorted、startswith
- **复杂度 / 风险**：分支 5；跨度 24 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e18bb2dfa3"></a>

#### `expected_outputs`

- **ID / 行**：`FUN-E18BB2DFA3` / `L372`（源码见本单元概览）
- **签名 / 返回**：`expected_outputs()` → `dict[Path, str]`
- **职责**：As-built responsibility derived from `expected_outputs` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：PIP_REPORT_PATH.exists、ValueError、build_document_register、build_trace_rows、build_units、csv_text、dependency_outputs、json.dumps、json.loads、process_index、read_yaml、report_path.exists、report_path.read_text
- **复杂度 / 风险**：分支 3；跨度 23 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-3c81471a20"></a>

#### `validate_model`

- **ID / 行**：`FUN-3C81471A20` / `L397`（源码见本单元概览）
- **签名 / 返回**：`validate_model(*, allow_generated_missing: bool=False)` → `list[str]`
- **职责**：As-built responsibility derived from `validate_model` and its owning unit.
- **依赖**：arch.get、arch_map.items、cm.get、component.get、errors.append、get、item_path.exists、len、read_yaml、req.get、req_map.items、reqs.get、reverse_ver.get、reverse_ver.items、ver.get
- **复杂度 / 风险**：分支 21；跨度 46 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-f855325a7a"></a>

#### `write_outputs`

- **ID / 行**：`FUN-F855325A7A` / `L445`（源码见本单元概览）
- **签名 / 返回**：`write_outputs(outputs: dict[Path, str])` → `None`
- **职责**：As-built responsibility derived from `write_outputs` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：ASPICE.mkdir、outputs.items、path.parent.mkdir、path.write_text
- **复杂度 / 风险**：分支 1；跨度 5 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-e57502a017"></a>

#### `check_outputs`

- **ID / 行**：`FUN-E57502A017` / `L452`（源码见本单元概览）
- **签名 / 返回**：`check_outputs(outputs: dict[Path, str])` → `list[str]`
- **职责**：As-built responsibility derived from `check_outputs` and its owning unit.
- **依赖**：build_document_register、document_files、errors.append、outputs.items、path.exists、path.read_text、rel
- **复杂度 / 风险**：分支 4；跨度 14 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4aa307b1b4"></a>

#### `main`

- **ID / 行**：`FUN-4AA307B1B4` / `L468`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **依赖**：argparse.ArgumentParser、build_units、check_outputs、document_files、errors.extend、expected_outputs、group.add_argument、join、len、parser.add_mutually_exclusive_group、parser.parse_args、print、read_yaml、validate_model、write_outputs
- **复杂度 / 风险**：分支 3；跨度 27 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-d4b396b36e"></a>

### scripts/check_mt5_connection.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D4B396B36E |
| 源码 | [scripts/check_mt5_connection.py](../../scripts/check_mt5_connection.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Smoke-test the optional MT5 connection. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[main](#fun-8efe0f5793)

<a id="fun-8efe0f5793"></a>

#### `main`

- **ID / 行**：`FUN-8EFE0F5793` / `L19`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **依赖**：MT5Config、get_mt5_provider、info.get、print、provider.account_info、provider.shutdown
- **复杂度 / 风险**：分支 2；跨度 27 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-9572f90802"></a>

### scripts/close_fixed_issues.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-9572F90802 |
| 源码 | [scripts/close_fixed_issues.py](../../scripts/close_fixed_issues.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Backward-compatible shim → tests/tools/github/close_issues.py |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-b4a1accfa2"></a>

### scripts/compare_pa_5m_tv.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B4A1ACCFA2 |
| 源码 | [scripts/compare_pa_5m_tv.py](../../scripts/compare_pa_5m_tv.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Quick 5m PA vs TV screenshot. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 1 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[main](#fun-406938ab22)

<a id="fun-406938ab22"></a>

#### `main`

- **ID / 行**：`FUN-406938AB22` / `L26`（源码见本单元概览）
- **签名 / 返回**：`main()` → `None`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：analyze_dgt_price_action、analyze_timeframe、build_price_action_summaries、enrich、fetch_all_data、fetched.raw.items、float、lvl.get、print、round、vp.get
- **复杂度 / 风险**：分支 4；跨度 29 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-8e5050cae9"></a>

### scripts/compare_pa_tv.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8E5050CAE9 |
| 源码 | [scripts/compare_pa_tv.py](../../scripts/compare_pa_tv.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Compare DGT PA output with TradingView screenshot reference. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_delta](#fun-818471ea1d) · [main](#fun-d24395608c)

<a id="fun-818471ea1d"></a>

#### `_delta`

- **ID / 行**：`FUN-818471EA1D` / `L26`（源码见本单元概览）
- **签名 / 返回**：`_delta(ours: float | None, tv: float)` → `str`
- **职责**：As-built responsibility derived from `_delta` and its owning unit.
- **复杂度 / 风险**：分支 1；跨度 4 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d24395608c"></a>

#### `main`

- **ID / 行**：`FUN-D24395608C` / `L32`（源码见本单元概览）
- **签名 / 返回**：`main()` → `None`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：_delta、abs、analyze_dgt_price_action、analyze_timeframe、build_price_action_summaries、build_volume_profile、df15.tail、enrich、fetch_all_data、fetched.raw.items、float、generate_trading_signals、get、len、pa.get、print、sentiment_score、vp.get、x.get
- **复杂度 / 风险**：分支 7；跨度 81 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-eefb367071"></a>

### scripts/create_system_test_issues.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EEFB367071 |
| 源码 | [scripts/create_system_test_issues.py](../../scripts/create_system_test_issues.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Backward-compatible shim → tests/tools/github/create_issues.py |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3fa67ae3bf"></a>

### scripts/estimate_llm_tokens.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3FA67AE3BF |
| 源码 | [scripts/estimate_llm_tokens.py](../../scripts/estimate_llm_tokens.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Rough per-stage LLM token budget (offline, sample context). |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_sys](#fun-85a3e4b3a3) · [_est](#fun-487ef18d78) · [main](#fun-7143a40322)

<a id="fun-85a3e4b3a3"></a>

#### `_sys`

- **ID / 行**：`FUN-85A3E4B3A3` / `L39`（源码见本单元概览）
- **签名 / 返回**：`_sys(mod: str)` → `str`
- **职责**：As-built responsibility derived from `_sys` and its owning unit.
- **依赖**：getattr、importlib.import_module
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-487ef18d78"></a>

#### `_est`

- **ID / 行**：`FUN-487EF18D78` / `L43`（源码见本单元概览）
- **签名 / 返回**：`_est(chars: int)` → `int`
- **职责**：As-built responsibility derived from `_est` and its owning unit.
- **依赖**：int
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-7143a40322"></a>

#### `main`

- **ID / 行**：`FUN-7143A40322` / `L47`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **依赖**：_est、_sample_context、_sys、build_llm_context、build_report、compute_trading_signals、debate_payload、fundamentals_analyst_payload、json.dumps、len、level_proposer_payload、manager_payload、news_analyst_payload、print、research_payload、risk_payload、run_analyst_team、run_bearish_researcher、run_bullish_researcher、run_debate
- **复杂度 / 风险**：分支 1；跨度 57 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-2781538ff5"></a>

### scripts/export_sample_report.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-2781538FF5 |
| 源码 | [scripts/export_sample_report.py](../../scripts/export_sample_report.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Export a脱敏 sample report JSON for docs/reference/examples/ (no network). |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) |
| 验证状态 | selected |

#### 函数导航

[_sanitize](#fun-a27c77a1d3) · [_sample_context](#fun-b0ffdeb50d) · [main](#fun-8b24cef8e4)

<a id="fun-a27c77a1d3"></a>

#### `_sanitize`

- **ID / 行**：`FUN-A27C77A1D3` / `L43`（源码见本单元概览）
- **签名 / 返回**：`_sanitize(obj)` → `runtime/inferred`
- **职责**：As-built responsibility derived from `_sanitize` and its owning unit.
- **依赖**：_sanitize、abs、isinstance、math.isinf、math.isnan、obj.items、round
- **复杂度 / 风险**：分支 5；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b0ffdeb50d"></a>

#### `_sample_context`

- **ID / 行**：`FUN-B0FFDEB50D` / `L55`（源码见本单元概览）
- **签名 / 返回**：`_sample_context()` → `MarketContext`
- **职责**：As-built responsibility derived from `_sample_context` and its owning unit.
- **依赖**：ExternalFactors、HeadlineItem、MacroQuote、MarketContext、analyze_timeframe、enrich、float、pd.DataFrame、pd.Series、pd.date_range、range、round、to_numpy
- **复杂度 / 风险**：分支 0；跨度 61 行；medium
- **测试 / 验证**：[tests/unit/test_analyst_team.py](../../tests/unit/test_analyst_team.py)、[tests/unit/test_analyst_team_llm.py](../../tests/unit/test_analyst_team_llm.py)、[tests/unit/test_debate_parallel.py](../../tests/unit/test_debate_parallel.py)、[tests/unit/test_llm_payload_funnel.py](../../tests/unit/test_llm_payload_funnel.py)、[tests/unit/test_narrative_facts.py](../../tests/unit/test_narrative_facts.py)、[tests/unit/test_research_parallel.py](../../tests/unit/test_research_parallel.py)、[tests/unit/test_signal_dedup.py](../../tests/unit/test_signal_dedup.py) · direct-dynamic

<a id="fun-8b24cef8e4"></a>

#### `main`

- **ID / 行**：`FUN-8B24CEF8E4` / `L118`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：RuntimeError / filesystem / caller-thread
- **依赖**：AgentPipelineMeta、AgentTrace、OUT.parent.mkdir、OUT.stat、OUT.write_text、RuntimeError、_sample_context、_sanitize、build_report、build_rule_narrative_sections、compute_trading_signals、debate.to_dict、decision.to_dict、get、isinstance、json.dumps、len、m.to_dict、math.isnan、pipeline_meta.to_dict
- **复杂度 / 风险**：分支 1；跨度 60 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-44da65110b"></a>

### scripts/generate_aspice_readable_docs.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-44DA65110B |
| 源码 | [scripts/generate_aspice_readable_docs.py](../../scripts/generate_aspice_readable_docs.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Render the ASPICE software-domain evidence as reviewable Markdown. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 22 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../tests/regression/test_aspice_assets.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_yaml](#fun-8e0ae30e6f) · [_csv](#fun-b8135ddcb1) · [_cell](#fun-211336c6ae) · [_list](#fun-36e6a8909a) · [_anchor](#fun-0ad419ab09) · [_req_links](#fun-2631f769a2) · [_arch_links](#fun-532ec35635) · [_measure_links](#fun-a9d2621b2a) · [_test_links](#fun-0aee39f96b) · [_table](#fun-84d7ee0257) · [_front](#fun-6a04465af3) · [_requirements_doc](#fun-1839614189) · [_architecture_doc](#fun-73cd1d7b70) · [_design_doc](#fun-aa8fad0df6) · [_unit_section](#fun-4e2eb68af0) · [_unit_verification_doc](#fun-34bbf83058) · [_integration_doc](#fun-be2fd65386) · [_qualification_doc](#fun-2336ffb14c) · [_configuration_doc](#fun-009efeb3d5) · [_traceability_doc](#fun-48fe08d05f) · [expected_outputs](#fun-a614f5b1a4) · [main](#fun-1ea9f2053e)

<a id="fun-8e0ae30e6f"></a>

#### `_yaml`

- **ID / 行**：`FUN-8E0AE30E6F` / `L27`（源码见本单元概览）
- **签名 / 返回**：`_yaml(name: str)` → `dict[str, Any]`
- **职责**：As-built responsibility derived from `_yaml` and its owning unit.
- **异常 / 副作用 / 并发**：ValueError / none-detected / caller-thread
- **依赖**：ValueError、isinstance、read_text、yaml.safe_load
- **复杂度 / 风险**：分支 1；跨度 5 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-b8135ddcb1"></a>

#### `_csv`

- **ID / 行**：`FUN-B8135DDCB1` / `L34`（源码见本单元概览）
- **签名 / 返回**：`_csv(name: str)` → `list[dict[str, str]]`
- **职责**：As-built responsibility derived from `_csv` and its owning unit.
- **依赖**：csv.DictReader、list、open
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-211336c6ae"></a>

#### `_cell`

- **ID / 行**：`FUN-211336C6AE` / `L39`（源码见本单元概览）
- **签名 / 返回**：`_cell(value: object)` → `str`
- **职责**：As-built responsibility derived from `_cell` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：isinstance、join、replace、str、strip、text.replace
- **复杂度 / 风险**：分支 2；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-36e6a8909a"></a>

#### `_list`

- **ID / 行**：`FUN-36E6A8909A` / `L48`（源码见本单元概览）
- **签名 / 返回**：`_list(value: str)` → `str`
- **职责**：As-built responsibility derived from `_list` and its owning unit.
- **依赖**：join、value.split
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0ad419ab09"></a>

#### `_anchor`

- **ID / 行**：`FUN-0AD419AB09` / `L52`（源码见本单元概览）
- **签名 / 返回**：`_anchor(value: str)` → `str`
- **职责**：As-built responsibility derived from `_anchor` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：replace、value.lower
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2631f769a2"></a>

#### `_req_links`

- **ID / 行**：`FUN-2631F769A2` / `L56`（源码见本单元概览）
- **签名 / 返回**：`_req_links(values: list[str] | str)` → `str`
- **职责**：As-built responsibility derived from `_req_links` and its owning unit.
- **依赖**：_anchor、isinstance、join、values.split
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-532ec35635"></a>

#### `_arch_links`

- **ID / 行**：`FUN-532EC35635` / `L61`（源码见本单元概览）
- **签名 / 返回**：`_arch_links(values: list[str] | str)` → `str`
- **职责**：As-built responsibility derived from `_arch_links` and its owning unit.
- **依赖**：_anchor、isinstance、join、values.split
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a9d2621b2a"></a>

#### `_measure_links`

- **ID / 行**：`FUN-A9D2621B2A` / `L66`（源码见本单元概览）
- **签名 / 返回**：`_measure_links(values: list[str] | str)` → `str`
- **职责**：As-built responsibility derived from `_measure_links` and its owning unit.
- **依赖**：_anchor、isinstance、item.startswith、join、rendered.append、values.split
- **复杂度 / 风险**：分支 5；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0aee39f96b"></a>

#### `_test_links`

- **ID / 行**：`FUN-0AEE39F96B` / `L77`（源码见本单元概览）
- **签名 / 返回**：`_test_links(value: list[str] | str)` → `str`
- **职责**：As-built responsibility derived from `_test_links` and its owning unit.
- **依赖**：isinstance、join、value.split
- **复杂度 / 风险**：分支 1；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-84d7ee0257"></a>

#### `_table`

- **ID / 行**：`FUN-84D7EE0257` / `L82`（源码见本单元概览）
- **签名 / 返回**：`_table(headers: list[str], rows: list[list[object]])` → `list[str]`
- **职责**：As-built responsibility derived from `_table` and its owning unit.
- **依赖**：_cell、join、lines.extend
- **复杂度 / 风险**：分支 0；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6a04465af3"></a>

#### `_front`

- **ID / 行**：`FUN-6A04465AF3` / `L91`（源码见本单元概览）
- **签名 / 返回**：`_front(title: str, process: str, purpose: str)` → `list[str]`
- **职责**：As-built responsibility derived from `_front` and its owning unit.
- **复杂度 / 风险**：分支 0；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-1839614189"></a>

#### `_requirements_doc`

- **ID / 行**：`FUN-1839614189` / `L107`（源码见本单元概览）
- **签名 / 返回**：`_requirements_doc(reqs: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_requirements_doc` and its owning unit.
- **依赖**：_anchor、_arch_links、_front、_measure_links、_table、defaultdict、join、len、lower、sorted
- **复杂度 / 风险**：分支 2；跨度 40 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-73cd1d7b70"></a>

#### `_architecture_doc`

- **ID / 行**：`FUN-73CD1D7B70` / `L149`（源码见本单元概览）
- **签名 / 返回**：`_architecture_doc(arch: dict[str, Any], units: list[dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `_architecture_doc` and its owning unit.
- **依赖**：_anchor、_front、_req_links、_table、append、defaultdict、join、len、lower
- **复杂度 / 风险**：分支 2；跨度 30 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-aa8fad0df6"></a>

#### `_design_doc`

- **ID / 行**：`FUN-AA8FAD0DF6` / `L181`（源码见本单元概览）
- **签名 / 返回**：`_design_doc(arch: dict[str, Any], units: list[dict[str, str]], functions: list[dict[str, str]], verification: dict[str, dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `_design_doc` and its owning unit.
- **依赖**：_anchor、_front、_measure_links、_table、_unit_section、append、casefold、defaultdict、int、join、len、sorted
- **复杂度 / 风险**：分支 4；跨度 56 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-4e2eb68af0"></a>

#### `_unit_section`

- **ID / 行**：`FUN-4E2EB68AF0` / `L239`（源码见本单元概览）
- **签名 / 返回**：`_unit_section(unit: dict[str, str], functions: list[dict[str, str]], verification: dict[str, str], component_name: str)` → `list[str]`
- **职责**：As-built responsibility derived from `_unit_section` and its owning unit.
- **依赖**：_anchor、_list、_measure_links、_req_links、_table、_test_links、card.append、join、lines.append
- **复杂度 / 风险**：分支 4；跨度 58 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-34bbf83058"></a>

#### `_unit_verification_doc`

- **ID / 行**：`FUN-34BBF83058` / `L299`（源码见本单元概览）
- **签名 / 返回**：`_unit_verification_doc(arch: dict[str, Any], rows: list[dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `_unit_verification_doc` and its owning unit.
- **依赖**：_anchor、_front、_measure_links、_table、_test_links、append、casefold、defaultdict、int、join、len、sorted、sum
- **复杂度 / 风险**：分支 2；跨度 24 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-be2fd65386"></a>

#### `_integration_doc`

- **ID / 行**：`FUN-BE2FD65386` / `L325`（源码见本单元概览）
- **签名 / 返回**：`_integration_doc(plan: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_integration_doc` and its owning unit.
- **依赖**：_anchor、_front、_measure_links、_req_links、_table、_test_links、enumerate、join
- **复杂度 / 风险**：分支 1；跨度 24 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-2336ffb14c"></a>

#### `_qualification_doc`

- **ID / 行**：`FUN-2336FFB14C` / `L351`（源码见本单元概览）
- **签名 / 返回**：`_qualification_doc(measures: dict[str, Any], coverage: list[dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `_qualification_doc` and its owning unit.
- **依赖**：_anchor、_arch_links、_front、_measure_links、_req_links、_table、join、len、policy.items、sum
- **复杂度 / 风险**：分支 0；跨度 20 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-009efeb3d5"></a>

#### `_configuration_doc`

- **ID / 行**：`FUN-009EFEB3D5` / `L373`（源码见本单元概览）
- **签名 / 返回**：`_configuration_doc(cm: dict[str, Any])` → `str`
- **职责**：As-built responsibility derived from `_configuration_doc` and its owning unit.
- **依赖**：_front、_table、item.get、items、join、json.loads、len、read_text、sbom.get
- **复杂度 / 风险**：分支 0；跨度 16 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-48fe08d05f"></a>

#### `_traceability_doc`

- **ID / 行**：`FUN-48FE08D05F` / `L391`（源码见本单元概览）
- **签名 / 返回**：`_traceability_doc(reqs: dict[str, Any], coverage: list[dict[str, str]])` → `str`
- **职责**：As-built responsibility derived from `_traceability_doc` and its owning unit.
- **依赖**：_arch_links、_front、_measure_links、_req_links、_table、join
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-a614f5b1a4"></a>

#### `expected_outputs`

- **ID / 行**：`FUN-A614F5B1A4` / `L401`（源码见本单元概览）
- **签名 / 返回**：`expected_outputs()` → `dict[Path, str]`
- **职责**：As-built responsibility derived from `expected_outputs` and its owning unit.
- **依赖**：_architecture_doc、_configuration_doc、_csv、_design_doc、_integration_doc、_qualification_doc、_requirements_doc、_traceability_doc、_unit_verification_doc、_yaml
- **复杂度 / 风险**：分支 0；跨度 22 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-1ea9f2053e"></a>

#### `main`

- **ID / 行**：`FUN-1EA9F2053E` / `L425`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：argparse.ArgumentParser、as_posix、errors.append、expected_outputs、join、len、mode.add_argument、outputs.items、parser.add_mutually_exclusive_group、parser.parse_args、path.exists、path.parent.mkdir、path.read_text、path.relative_to、path.write_text、print
- **复杂度 / 风险**：分支 5；跨度 22 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-70ee096332"></a>

### scripts/generate_aspice_software_evidence.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-70EE096332 |
| 源码 | [scripts/generate_aspice_software_evidence.py](../../scripts/generate_aspice_software_evidence.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Generate SWE.3-SWE.6 as-built design and verification evidence. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 13 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../tests/regression/test_aspice_assets.py)、[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_rel](#fun-39773424a2) · [_stable_id](#fun-dd062cff6e) · [_source_files](#fun-bed0de409d) · [_test_corpus](#fun-86730c4fbc) · [_token_references](#fun-d937d4a0bb) · [_component_for](#fun-c81b19f40e) · [_qualname](#fun-6e9b981dfb) · [_call_name](#fun-97fbbac4cf) · [_node_contract](#fun-df98642acc) · [_risk](#fun-966d638362) · [_csv](#fun-840dd814ad) · [expected_outputs](#fun-6b5f339e4d) · [main](#fun-9c060dbc51)

<a id="fun-39773424a2"></a>

#### `_rel`

- **ID / 行**：`FUN-39773424A2` / `L41`（源码见本单元概览）
- **签名 / 返回**：`_rel(path: Path)` → `str`
- **职责**：As-built responsibility derived from `_rel` and its owning unit.
- **依赖**：as_posix、path.relative_to
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-dd062cff6e"></a>

#### `_stable_id`

- **ID / 行**：`FUN-DD062CFF6E` / `L45`（源码见本单元概览）
- **签名 / 返回**：`_stable_id(prefix: str, value: str)` → `str`
- **职责**：As-built responsibility derived from `_stable_id` and its owning unit.
- **依赖**：hashlib.sha1、hexdigest、upper、value.encode
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-bed0de409d"></a>

#### `_source_files`

- **ID / 行**：`FUN-BED0DE409D` / `L50`（源码见本单元概览）
- **签名 / 返回**：`_source_files()` → `list[Path]`
- **职责**：As-built responsibility derived from `_source_files` and its owning unit.
- **依赖**：ROOT.rglob、_rel、any、casefold、path.relative_to、sorted
- **复杂度 / 风险**：分支 0；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-86730c4fbc"></a>

#### `_test_corpus`

- **ID / 行**：`FUN-86730C4FBC` / `L61`（源码见本单元概览）
- **签名 / 返回**：`_test_corpus()` → `dict[str, str]`
- **职责**：As-built responsibility derived from `_test_corpus` and its owning unit.
- **依赖**：_rel、casefold、path.read_text、rglob、sorted
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-d937d4a0bb"></a>

#### `_token_references`

- **ID / 行**：`FUN-D937D4A0BB` / `L71`（源码见本单元概览）
- **签名 / 返回**：`_token_references(token: str, corpus: dict[str, str])` → `list[str]`
- **职责**：As-built responsibility derived from `_token_references` and its owning unit.
- **依赖**：corpus.items、pattern.search、re.compile、re.escape
- **复杂度 / 风险**：分支 0；跨度 3 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-c81b19f40e"></a>

#### `_component_for`

- **ID / 行**：`FUN-C81B19F40E` / `L76`（源码见本单元概览）
- **签名 / 返回**：`_component_for(path: str)` → `str`
- **职责**：As-built responsibility derived from `_component_for` and its owning unit.
- **依赖**：path.startswith
- **复杂度 / 风险**：分支 3；跨度 17 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6e9b981dfb"></a>

#### `_qualname`

- **ID / 行**：`FUN-6E9B981DFB` / `L95`（源码见本单元概览）
- **签名 / 返回**：`_qualname(node: ast.FunctionDef | ast.AsyncFunctionDef, parents: dict[ast.AST, ast.AST])` → `str`
- **职责**：As-built responsibility derived from `_qualname` and its owning unit.
- **依赖**：isinstance、join、owners.append、parents.get、reversed
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-97fbbac4cf"></a>

#### `_call_name`

- **ID / 行**：`FUN-97FBBAC4CF` / `L105`（源码见本单元概览）
- **签名 / 返回**：`_call_name(call: ast.Call)` → `str`
- **职责**：As-built responsibility derived from `_call_name` and its owning unit.
- **依赖**：isinstance、join、parts.append、reversed
- **复杂度 / 风险**：分支 2；跨度 9 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-df98642acc"></a>

#### `_node_contract`

- **ID / 行**：`FUN-DF98642ACC` / `L116`（源码见本单元概览）
- **签名 / 返回**：`_node_contract(node: ast.FunctionDef | ast.AsyncFunctionDef)` → `dict[str, str | int]`
- **职责**：As-built responsibility derived from `_node_contract` and its owning unit.
- **依赖**：_call_name、any、ast.get_docstring、ast.unparse、ast.walk、doc.splitlines、effects.append、getattr、isinstance、join、lower、max、re.search、set、sorted、sum
- **复杂度 / 风险**：分支 9；跨度 41 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-966d638362"></a>

#### `_risk`

- **ID / 行**：`FUN-966D638362` / `L159`（源码见本单元概览）
- **签名 / 返回**：`_risk(path: str, name: str, contract: dict[str, str | int])` → `str`
- **职责**：As-built responsibility derived from `_risk` and its owning unit.
- **依赖**：int、name.split、re.search、startswith、str
- **复杂度 / 风险**：分支 2；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-840dd814ad"></a>

#### `_csv`

- **ID / 行**：`FUN-840DD814AD` / `L169`（源码见本单元概览）
- **签名 / 返回**：`_csv(rows: list[dict[str, object]])` → `str`
- **职责**：As-built responsibility derived from `_csv` and its owning unit.
- **依赖**：buffer.getvalue、csv.DictWriter、io.StringIO、list、writer.writeheader、writer.writerows
- **复杂度 / 风险**：分支 0；跨度 6 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-6b5f339e4d"></a>

#### `expected_outputs`

- **ID / 行**：`FUN-6B5F339E4D` / `L177`（源码见本单元概览）
- **签名 / 返回**：`expected_outputs()` → `tuple[dict[Path, str], dict[str, int]]`
- **职责**：As-built responsibility derived from `expected_outputs` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：ARCH_PATH.read_text、REQ_PATH.read_text、RESULT_PATH.read_text、_component_for、_csv、_node_contract、_qualname、_rel、_risk、_source_files、_stable_id、_test_corpus、_token_references、append、ast.iter_child_nodes、ast.parse、ast.walk、bool、defaultdict、dict.fromkeys
- **复杂度 / 风险**：分支 17；跨度 139 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9c060dbc51"></a>

#### `main`

- **ID / 行**：`FUN-9C060DBC51` / `L318`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：_rel、argparse.ArgumentParser、errors.append、expected_outputs、join、mode.add_argument、outputs.items、parser.add_mutually_exclusive_group、parser.parse_args、path.exists、path.read_text、path.write_text、print
- **复杂度 / 风险**：分支 7；跨度 26 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-37e036c51b"></a>

### scripts/inspect_archive.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-37E036C51B |
| 源码 | [scripts/inspect_archive.py](../../scripts/inspect_archive.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Inspect, list, and validate run archives without opening Streamlit. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 6 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_cmd_list](#fun-000d721083) · [_cmd_inspect](#fun-747a7a71ca) · [_cmd_validate](#fun-63ae1e91d4) · [_cmd_export](#fun-e505b92782) · [_cmd_import](#fun-ca79779a11) · [main](#fun-80a2a844ca)

<a id="fun-000d721083"></a>

#### `_cmd_list`

- **ID / 行**：`FUN-000D721083` / `L16`（源码见本单元概览）
- **签名 / 返回**：`_cmd_list(args: argparse.Namespace)` → `int`
- **职责**：As-built responsibility derived from `_cmd_list` and its owning unit.
- **依赖**：archive_label、list_archives、print
- **复杂度 / 风险**：分支 2；跨度 10 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-747a7a71ca"></a>

#### `_cmd_inspect`

- **ID / 行**：`FUN-747A7A71CA` / `L28`（源码见本单元概览）
- **签名 / 返回**：`_cmd_inspect(args: argparse.Namespace)` → `int`
- **职责**：As-built responsibility derived from `_cmd_inspect` and its owning unit.
- **依赖**：inspect_run_archive、json.dumps、print
- **复杂度 / 风险**：分支 1；跨度 14 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-63ae1e91d4"></a>

#### `_cmd_validate`

- **ID / 行**：`FUN-63AE1E91D4` / `L44`（源码见本单元概览）
- **签名 / 返回**：`_cmd_validate(args: argparse.Namespace)` → `int`
- **职责**：As-built responsibility derived from `_cmd_validate` and its owning unit.
- **依赖**：RunConfig、analyses.keys、bool、enriched.keys、get、json.dumps、load_replay_bundle、normalized、print、report.get、sorted
- **复杂度 / 风险**：分支 0；跨度 21 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-e505b92782"></a>

#### `_cmd_export`

- **ID / 行**：`FUN-E505B92782` / `L67`（源码见本单元概览）
- **签名 / 返回**：`_cmd_export(args: argparse.Namespace)` → `int`
- **职责**：As-built responsibility derived from `_cmd_export` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / filesystem / caller-thread
- **依赖**：Path、export_archive_zip、len、out.write_bytes、print
- **复杂度 / 风险**：分支 0；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-ca79779a11"></a>

#### `_cmd_import`

- **ID / 行**：`FUN-CA79779A11` / `L77`（源码见本单元概览）
- **签名 / 返回**：`_cmd_import(args: argparse.Namespace)` → `int`
- **职责**：As-built responsibility derived from `_cmd_import` and its owning unit.
- **依赖**：Path、import_archive_zip、print、read_bytes
- **复杂度 / 风险**：分支 0；跨度 7 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-80a2a844ca"></a>

#### `main`

- **ID / 行**：`FUN-80A2A844CA` / `L86`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **依赖**：argparse.ArgumentParser、args.func、export_p.add_argument、export_p.set_defaults、import_p.add_argument、import_p.set_defaults、inspect_p.add_argument、inspect_p.set_defaults、list_p.add_argument、list_p.set_defaults、parser.add_subparsers、parser.parse_args、sub.add_parser、validate_p.add_argument、validate_p.set_defaults
- **复杂度 / 风险**：分支 0；跨度 29 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-ebde8e6443"></a>

### scripts/regression_test.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-EBDE8E6443 |
| 源码 | [scripts/regression_test.py](../../scripts/regression_test.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Backward-compatible shim → tests/run.py --fast |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-3960e281ab"></a>

### scripts/replay_llm_narrative.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-3960E281AB |
| 源码 | [scripts/replay_llm_narrative.py](../../scripts/replay_llm_narrative.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Replay saved LLM narrative JSON against report validators (zero API tokens). |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 4 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py)、[tests/unit/test_replay_llm_narrative.py](../../tests/unit/test_replay_llm_narrative.py) |
| 验证状态 | selected |

#### 函数导航

[_load_json](#fun-2a9ad18e99) · [_load_llm_payload](#fun-0b702bf5f4) · [_print_audit](#fun-89b0c24609) · [main](#fun-06a7e09133)

<a id="fun-2a9ad18e99"></a>

#### `_load_json`

- **ID / 行**：`FUN-2A9AD18E99` / `L18`（源码见本单元概览）
- **签名 / 返回**：`_load_json(path: Path)` → `dict`
- **职责**：As-built responsibility derived from `_load_json` and its owning unit.
- **依赖**：json.loads、path.read_text
- **复杂度 / 风险**：分支 0；跨度 2 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-0b702bf5f4"></a>

#### `_load_llm_payload`

- **ID / 行**：`FUN-0B702BF5F4` / `L22`（源码见本单元概览）
- **签名 / 返回**：`_load_llm_payload(report: dict, llm_path: Path | None)` → `dict`
- **职责**：As-built responsibility derived from `_load_llm_payload` and its owning unit.
- **异常 / 副作用 / 并发**：SystemExit / none-detected / caller-thread
- **依赖**：SystemExit、_load_json、isinstance、json.loads、llm.get、report.get
- **复杂度 / 风险**：分支 3；跨度 13 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-89b0c24609"></a>

#### `_print_audit`

- **ID / 行**：`FUN-89B0C24609` / `L37`（源码见本单元概览）
- **签名 / 返回**：`_print_audit(result)` → `None`
- **职责**：As-built responsibility derived from `_print_audit` and its owning unit.
- **依赖**：audit.get、get、items、len、print、section.get、sum、top.get
- **复杂度 / 风险**：分支 6；跨度 27 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-06a7e09133"></a>

#### `main`

- **ID / 行**：`FUN-06A7E09133` / `L66`（源码见本单元概览）
- **签名 / 返回**：`main()` → `None`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **依赖**：_load_json、_load_llm_payload、_print_audit、apply_llm_to_report、argparse.ArgumentParser、build_rule_narrative_sections、parser.add_argument、parser.parse_args、print、report.get、validate_llm_payload
- **复杂度 / 风险**：分支 2；跨度 32 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-d538889607"></a>

### scripts/run_pipeline_test.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D538889607 |
| 源码 | [scripts/run_pipeline_test.py](../../scripts/run_pipeline_test.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Backward-compatible shim → tests/run.py |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-8f71f01664"></a>

### scripts/show_utf8.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-8F71F01664 |
| 源码 | [scripts/show_utf8.py](../../scripts/show_utf8.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Print UTF-8 text files with stable line numbers. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[parse_args](#fun-fdec2f3b6b) · [main](#fun-9302f1289e)

<a id="fun-fdec2f3b6b"></a>

#### `parse_args`

- **ID / 行**：`FUN-FDEC2F3B6B` / `L16`（源码见本单元概览）
- **签名 / 返回**：`parse_args()` → `argparse.Namespace`
- **职责**：As-built responsibility derived from `parse_args` and its owning unit.
- **依赖**：argparse.ArgumentParser、parser.add_argument、parser.parse_args
- **复杂度 / 风险**：分支 0；跨度 6 行；medium
- **测试 / 验证**：— · static-and-component

<a id="fun-9302f1289e"></a>

#### `main`

- **ID / 行**：`FUN-9302F1289E` / `L24`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **依赖**：Path、len、max、min、parse_args、path.read_text、print、range、sys.stdout.reconfigure、text.splitlines
- **复杂度 / 风险**：分支 1；跨度 11 行；medium
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-c913c2495c"></a>

### scripts/test_live_fetch.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-C913C2495C |
| 源码 | [scripts/test_live_fetch.py](../../scripts/test_live_fetch.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Quick live fetch smoke test for external data sources. |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 2 / 1 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static)、[VM-UNIT](./SWE.4-unit-testing.md#vm-unit) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[_block](#fun-2e85c86a01) · [main](#fun-9c22b2b4e5)

<a id="fun-2e85c86a01"></a>

#### `_block`

- **ID / 行**：`FUN-2E85C86A01` / `L20`（源码见本单元概览）
- **签名 / 返回**：`_block(title: str, body: object)` → `None`
- **职责**：As-built responsibility derived from `_block` and its owning unit.
- **依赖**：isinstance、json.dumps、print
- **复杂度 / 风险**：分支 1；跨度 8 行；low
- **测试 / 验证**：— · static-and-component

<a id="fun-9c22b2b4e5"></a>

#### `main`

- **ID / 行**：`FUN-9C22B2B4E5` / `L30`（源码见本单元概览）
- **签名 / 返回**：`main()` → `int`
- **职责**：As-built responsibility derived from `main` and its owning unit.
- **异常 / 副作用 / 并发**：none-explicit / external-io / caller-thread
- **依赖**：FundamentalsDataSource、NewsDataSource、SocialDataSource、_block、bool、dxy_refs.get、fetch_dxy_impact、fetch_external、fetch_jin10_bundle、fetch_jin10_kline、fetch_jin10_quote、fetch_social_sentiment、len、merge_external、print、social_refs.get、sum
- **复杂度 / 风险**：分支 1；跨度 72 行；high
- **测试 / 验证**：[tests/unit/test_chart_projections.py](../../tests/unit/test_chart_projections.py) · direct-dynamic

<a id="unit-76c5f6645c"></a>

### scripts/test_llm_json_fix.py — 软件单元详细设计

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-76C5F6645C |
| 源码 | [scripts/test_llm_json_fix.py](../../scripts/test_llm_json_fix.py) |
| 架构组件 | ARC-TOOLS — 开发、审核与运维工具 |
| 职责 | Backward-compatible shim → pytest tests/unit/test_llm_json.py |
| 关联需求 | [SWR-NFR-003](./SWE.1-software-requirements.md#swr-nfr-003)、[SWR-NFR-004](./SWE.1-software-requirements.md#swr-nfr-004) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](./SWE.6-validation-testing.md#vm-static) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。
