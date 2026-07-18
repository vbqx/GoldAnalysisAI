# ARC-APP — 应用入口与运行配置

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-app)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [app.py](#unit-13cce7fd07) | 1 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [run_app.py](#unit-b2a1584dad) | 13 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/1_机构级分析报告.py](#unit-02d5d8e12e) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/2_短线策略.py](#unit-0e03ccecca) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/3_LLM决策链.py](#unit-74cd83898f) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |
| [views/4_外部数据.py](#unit-1fe6319d7a) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) | selected |

<a id="unit-13cce7fd07"></a>

### UNIT-13CCE7FD07

**模块**：`app.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-13CCE7FD07 |
| 源码 | [app.py](../../../app.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | GoldAnalysisAI — Streamlit 入口（纯导航，不显示为侧边栏页面）。 |
| 关联需求 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 1 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_run_archive.py](../../../tests/unit/test_run_archive.py) |
| 验证状态 | selected |

#### 函数导航

[_ensure_streamlit_runtime](#fun-188c32a8d7)

<a id="fun-188c32a8d7"></a>

#### FUN-188C32A8D7

| 设计项 | 说明 |
|---|---|
| 函数 | `_ensure_streamlit_runtime` |
| 源码位置 | [app.py](../../../app.py) · `L29` |
| 签名 | `_ensure_streamlit_runtime()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 确保Streamlit 运行时上下文；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `get_script_run_ctx` → `print` → `SystemExit`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | SystemExit |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_script_run_ctx、print、SystemExit |
| 复杂度 / 风险 | 分支 2；跨度 17 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-b2a1584dad"></a>

### UNIT-B2A1584DAD

**模块**：`run_app.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-B2A1584DAD |
| 源码 | [run_app.py](../../../run_app.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 实现“应用入口与运行配置”组件中 `run_app.py` 的职责，通过 `load_dotenv`、`init_dev_env`、`ensure_streamlit_config`、`resolve_python`、`stop_stale_streamlit`、`parse_args`、`main` 提供该模块的公开能力。 |
| 关联需求 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 13 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) |
| 验证状态 | selected |

#### 函数导航

[load_dotenv](#fun-dccdace066) · [init_dev_env](#fun-79cfc89b7c) · [ensure_streamlit_config](#fun-acd09c876b) · [_python_is_usable](#fun-8991377fd4) · [resolve_python](#fun-50c4f81dd9) · [_pids_listening_on_port](#fun-40c14bb01b) · [_command_line_for_pid](#fun-efea1102a6) · [_is_project_streamlit_pid](#fun-5f95c44360) · [_streamlit_pids](#fun-e5e889737f) · [_terminate_pid](#fun-2f41b39115) · [stop_stale_streamlit](#fun-93afb64487) · [parse_args](#fun-5749848613) · [main](#fun-8c169563e6)

<a id="fun-dccdace066"></a>

#### FUN-DCCDACE066

| 设计项 | 说明 |
|---|---|
| 函数 | `load_dotenv` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L27` |
| 签名 | `load_dotenv(path: Path)` |
| 参数 | `path`（Path）：文件或目录路径 |
| 返回 | 无返回值（None） |
| 职责 | 加载.env 环境变量；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `path.is_file` → `print` → `splitlines` → `path.read_text` → `raw.strip` → `line.startswith` → `line.split` → `key.strip`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | path.is_file、print、splitlines、path.read_text、raw.strip、line.startswith、line.split、key.strip、val.strip、len |
| 复杂度 / 风险 | 分支 4；跨度 15 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-79cfc89b7c"></a>

#### FUN-79CFC89B7C

| 设计项 | 说明 |
|---|---|
| 函数 | `init_dev_env` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L44` |
| 签名 | `init_dev_env()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 初始化开发环境变量；可能影响共享状态；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `os.environ.setdefault`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | os.environ.setdefault |
| 复杂度 / 风险 | 分支 0；跨度 5 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-acd09c876b"></a>

#### FUN-ACD09C876B

| 设计项 | 说明 |
|---|---|
| 函数 | `ensure_streamlit_config` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L51` |
| 签名 | `ensure_streamlit_config()` |
| 参数 | 无显式输入参数 |
| 返回 | 无返回值（None） |
| 职责 | 确保Streamlit 配置文件；可能影响文件系统；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `cfg_dir.mkdir` → `config_path.is_file` → `config_path.write_text` → `cred_path.is_file` → `cred_path.write_text`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束；相关路径满足读取或写入权限及目录边界 |
| 后置条件 | 无返回值（None）；可观察变化限于文件系统 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 文件系统读写 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | cfg_dir.mkdir、config_path.is_file、config_path.write_text、cred_path.is_file、cred_path.write_text |
| 复杂度 / 风险 | 分支 2；跨度 15 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8991377fd4"></a>

#### FUN-8991377FD4

| 设计项 | 说明 |
|---|---|
| 函数 | `_python_is_usable` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L68` |
| 签名 | `_python_is_usable(candidate: Path)` |
| 参数 | `candidate`（Path）：由调用方提供的 `candidate` 输入对象 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断Python 解释器可用性；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `subprocess.run`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | subprocess.run、str |
| 复杂度 / 风险 | 分支 1；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-50c4f81dd9"></a>

#### FUN-50C4F81DD9

| 设计项 | 说明 |
|---|---|
| 函数 | `resolve_python` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L82` |
| 签名 | `resolve_python()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `Path \| str` 类型结果 |
| 职责 | 解析并选择Python 解释器；返回 `Path \| str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `candidate.is_file` → `_python_is_usable`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `Path \| str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | candidate.is_file、_python_is_usable |
| 复杂度 / 风险 | 分支 3；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-40c14bb01b"></a>

#### FUN-40C14BB01B

| 设计项 | 说明 |
|---|---|
| 函数 | `_pids_listening_on_port` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L90` |
| 签名 | `_pids_listening_on_port(port: int)` |
| 参数 | `port`（int）：监听端口 |
| 返回 | 返回 `list[int]` 类型结果 |
| 职责 | 构建监听指定端口的进程标识集合；返回 `list[int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `os.getpid` → `subprocess.check_output` → `out.splitlines` → `line.upper` → `line.split` → `pids.append` → `out.split` → `token.isdigit`；包含 13 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | os.getpid、subprocess.check_output、out.splitlines、line.upper、line.split、int、pids.append、out.split、token.isdigit |
| 复杂度 / 风险 | 分支 13；跨度 42 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-efea1102a6"></a>

#### FUN-EFEA1102A6

| 设计项 | 说明 |
|---|---|
| 函数 | `_command_line_for_pid` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L134` |
| 签名 | `_command_line_for_pid(pid: int)` |
| 参数 | `pid`（int）：进程标识 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成指定进程的命令行文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `subprocess.check_output`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、subprocess.check_output、str |
| 复杂度 / 风险 | 分支 3；跨度 25 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5f95c44360"></a>

#### FUN-5F95C44360

| 设计项 | 说明 |
|---|---|
| 函数 | `_is_project_streamlit_pid` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L161` |
| 签名 | `_is_project_streamlit_pid(pid: int, root: Path)` |
| 参数 | `pid`（int）：进程标识<br>`root`（Path）：项目根目录 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断本项目 Streamlit 进程；返回 `bool` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `lower` → `_command_line_for_pid`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | lower、_command_line_for_pid、str |
| 复杂度 / 风险 | 分支 1；跨度 6 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-e5e889737f"></a>

#### FUN-E5E889737F

| 设计项 | 说明 |
|---|---|
| 函数 | `_streamlit_pids` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L169` |
| 签名 | `_streamlit_pids(root: Path)` |
| 参数 | `root`（Path）：项目根目录 |
| 返回 | 返回 `list[int]` 类型结果 |
| 职责 | 构建本项目 Streamlit 进程标识集合；返回 `list[int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `os.getpid` → `lower` → `root_marker.replace` → `chr` → `subprocess.check_output` → `out.splitlines` → `line.strip` → `line.isdigit`；包含 9 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | os.getpid、lower、str、root_marker.replace、chr、subprocess.check_output、out.splitlines、line.strip、line.isdigit、int、pids.append |
| 复杂度 / 风险 | 分支 9；跨度 46 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-2f41b39115"></a>

#### FUN-2F41B39115

| 设计项 | 说明 |
|---|---|
| 函数 | `_terminate_pid` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L217` |
| 签名 | `_terminate_pid(pid: int)` |
| 参数 | `pid`（int）：进程标识 |
| 返回 | 无返回值（None） |
| 职责 | 终止`pid`；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `subprocess.run` → `os.kill`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | subprocess.run、str、os.kill |
| 复杂度 / 风险 | 分支 3；跨度 16 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-93afb64487"></a>

#### FUN-93AFB64487

| 设计项 | 说明 |
|---|---|
| 函数 | `stop_stale_streamlit` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L235` |
| 签名 | `stop_stale_streamlit(port: int)` |
| 参数 | `port`（int）：监听端口 |
| 返回 | 无返回值（None） |
| 职责 | 停止遗留 Streamlit 进程；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `_pids_listening_on_port` → `_is_project_streamlit_pid` → `targets.append` → `print` → `_terminate_pid`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _pids_listening_on_port、_is_project_streamlit_pid、targets.append、print、_terminate_pid |
| 复杂度 / 风险 | 分支 4；跨度 16 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-5749848613"></a>

#### FUN-5749848613

| 设计项 | 说明 |
|---|---|
| 函数 | `parse_args` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L253` |
| 签名 | `parse_args()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `argparse.Namespace` 类型结果 |
| 职责 | 解析命令行参数；返回 `argparse.Namespace` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `argparse.ArgumentParser` → `parser.add_argument` → `parser.parse_args`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `argparse.Namespace` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | argparse.ArgumentParser、parser.add_argument、parser.parse_args |
| 复杂度 / 风险 | 分支 0；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-8c169563e6"></a>

#### FUN-8C169563E6

| 设计项 | 说明 |
|---|---|
| 函数 | `main` |
| 源码位置 | [run_app.py](../../../run_app.py) · `L264` |
| 签名 | `main()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 执行 `run_app.py` 的主流程；可能影响共享状态；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `os.chdir` → `parse_args` → `init_dev_env` → `load_dotenv` → `ensure_streamlit_config` → `os.environ.get` → `stop_stale_streamlit` → `resolve_python`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | os.chdir、parse_args、init_dev_env、load_dotenv、ensure_streamlit_config、int、os.environ.get、stop_stale_streamlit、resolve_python、subprocess.run、str、print、subprocess.call |
| 复杂度 / 风险 | 分支 4；跨度 49 行；中 |
| 测试 / 验证 | [tests/unit/test_chart_projections.py](../../../tests/unit/test_chart_projections.py) · 直接动态测试 |

<a id="unit-02d5d8e12e"></a>

### UNIT-02D5D8E12E

**模块**：`views/1_机构级分析报告.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-02D5D8E12E |
| 源码 | [views/1_机构级分析报告.py](../../../views/1_机构级分析报告.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 机构级分析报告 — 主页面。 |
| 关联需求 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-0e03ccecca"></a>

### UNIT-0E03CCECCA

**模块**：`views/2_短线策略.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-0E03CCECCA |
| 源码 | [views/2_短线策略.py](../../../views/2_短线策略.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 短线策略图 — 独立页面。 |
| 关联需求 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-74cd83898f"></a>

### UNIT-74CD83898F

**模块**：`views/3_LLM决策链.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-74CD83898F |
| 源码 | [views/3_LLM决策链.py](../../../views/3_LLM决策链.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | LLM 决策链 — 独立页面。 |
| 关联需求 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-1fe6319d7a"></a>

### UNIT-1FE6319D7A

**模块**：`views/4_外部数据.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-1FE6319D7A |
| 源码 | [views/4_外部数据.py](../../../views/4_外部数据.py) |
| 架构组件 | ARC-APP — 应用入口与运行配置 |
| 职责 | 外部数据 — 新闻、日历、DXY、社媒；fetch 完成后即可查看。 |
| 关联需求 | [SWR-CORE-002](../SWE.1-software-requirements.md#swr-core-002)、[SWR-UI-001](../SWE.1-software-requirements.md#swr-ui-001)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-MANUAL-UI](../SWE.6-validation-testing.md#vm-manual-ui) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。
