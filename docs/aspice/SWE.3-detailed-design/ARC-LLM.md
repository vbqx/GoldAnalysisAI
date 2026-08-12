# ARC-LLM — Optional advice wording service

| 属性 | 内容 |
|---|---|
| ASPICE 过程 | SWE.3 |
| 状态 | 受控基线 |
| 用途 | 阅读该架构组件的软件单元、函数职责、契约、风险与验证引用 |

> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于
> `_machine/`，普通评审无需直接阅读机器文件。

[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#arc-llm)

## 组件概览

| 模块 | 函数 | 高风险 | 验证措施 | 状态 |
|---|---|---|---|---|
| [src/llm/__init__.py](#unit-598812089b) | 0 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/client.py](#unit-d7fd07af44) | 10 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/format_io.py](#unit-deb0d517c6) | 3 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/narrative_output.py](#unit-fbf77b94fb) | 5 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/router.py](#unit-6568b95afa) | 2 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/stage.py](#unit-31083eb5d0) | 6 | 1 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |
| [src/llm/stage_policy.py](#unit-e488978a91) | 8 | 0 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) | selected |

<a id="unit-598812089b"></a>

### UNIT-598812089B

**模块**：`src/llm/__init__.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-598812089B |
| 源码 | [src/llm/__init__.py](../../../src/llm/__init__.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/__init__.py` 的职责，通过 模块内部实现 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 0 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

本模块没有函数或方法定义。

<a id="unit-d7fd07af44"></a>

### UNIT-D7FD07AF44

**模块**：`src/llm/client.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-D7FD07AF44 |
| 源码 | [src/llm/client.py](../../../src/llm/client.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/client.py` 的职责，通过 `LLMClientError`、`normalize_provider_usage`、`LLMClient` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 10 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [LLMClient.chat_stream](#fun-b2c894bd12) | 生成`chat_stream`文本；可能影响外部接口；返回 `Iterator[str]` 类型结果。 | 外部接口 I/O | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) |

#### 函数导航

[normalize_provider_usage](#fun-8ec658e9d5) · [LLMClient.__init__](#fun-184ed552df) · [LLMClient.timeout](#fun-b3cf019763) · [LLMClient._request_timeout](#fun-6281d0133f) · [LLMClient._headers](#fun-870c1d436c) · [LLMClient._parse_sse_event](#fun-89b4063b63) · [LLMClient._parse_sse_line](#fun-c5e317f9c8) · [LLMClient.chat_stream](#fun-b2c894bd12) · [LLMClient.chat](#fun-feaf06c7c1) · [LLMClient.chat_json](#fun-cc950a51e1)

<a id="fun-8ec658e9d5"></a>

#### FUN-8EC658E9D5

| 设计项 | 说明 |
|---|---|
| 函数 | `normalize_provider_usage` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L21` |
| 签名 | `normalize_provider_usage(raw: Any)` |
| 参数 | `raw`（Any）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, int] \| None` 类型结果 |
| 职责 | 标准化`provider_usage`；返回 `dict[str, int] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `isinstance` → `raw.get`；包含 12 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | isinstance、raw.get、int |
| 复杂度 / 风险 | 分支 12；跨度 32 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-184ed552df"></a>

#### FUN-184ED552DF

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.__init__` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L58` |
| 签名 | `LLMClient.__init__(self, *, api_key: str, base_url: str, model: str, timeout: int \| float \| None=None, connect_timeout: float \| None=None, read_timeout: float \| None=None)` |
| 参数 | `api_key`（str）：索引键<br>`base_url`（str）：外部资源地址<br>`model`（str）：模型名称或模型对象<br>`timeout`（int \| float \| None）：超时秒数；默认值 `None`<br>`connect_timeout`（float \| None）：超时秒数；默认值 `None`<br>`read_timeout`（float \| None）：超时秒数；默认值 `None` |
| 返回 | 无返回值（None） |
| 职责 | 初始化当前类实例并建立字段约束；无返回值（None）。 |
| 处理逻辑 | 按源码执行顺序经过 `base_url.rstrip` → `min`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 无返回值（None）；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | base_url.rstrip、float、min |
| 复杂度 / 风险 | 分支 4；跨度 30 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b3cf019763"></a>

#### FUN-B3CF019763

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.timeout` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L90` |
| 签名 | `LLMClient.timeout(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`timeout`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 3 行；中 |
| 测试 / 验证 | [tests/regression/test_aspice_assets.py](../../../tests/regression/test_aspice_assets.py)、[tests/unit/test_archive_transfer.py](../../../tests/unit/test_archive_transfer.py)、[tests/unit/test_generation_worker.py](../../../tests/unit/test_generation_worker.py)、[tests/unit/test_http_helpers.py](../../../tests/unit/test_http_helpers.py)、[tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py)、[tests/unit/test_pipeline_progress_live.py](../../../tests/unit/test_pipeline_progress_live.py) · 直接动态测试 |

<a id="fun-6281d0133f"></a>

#### FUN-6281D0133F

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._request_timeout` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L94` |
| 签名 | `LLMClient._request_timeout(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `tuple[float, float]` 类型结果 |
| 职责 | 构建`request_timeout`；返回 `tuple[float, float]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[float, float]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 2 行；低 |
| 测试 / 验证 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py) · 直接动态测试 |

<a id="fun-870c1d436c"></a>

#### FUN-870C1D436C

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._headers` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L97` |
| 签名 | `LLMClient._headers(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, str]` 类型结果 |
| 职责 | 构建`headers`；返回 `dict[str, str]` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, str]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 5 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-89b4063b63"></a>

#### FUN-89B4063B63

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._parse_sse_event` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L103` |
| 签名 | `LLMClient._parse_sse_event(self, line: str)` |
| 参数 | `line`（str）：由 `line` 表示的文本或标识 |
| 返回 | 返回 `tuple[str \| None, dict[str, int] \| None]` 类型结果 |
| 职责 | 解析`sse_event`；返回 `tuple[str \| None, dict[str, int] \| None]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `line.strip` → `line.startswith` → `strip` → `json.loads` → `isinstance` → `normalize_provider_usage` → `data.get` → `get`；包含 7 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[str \| None, dict[str, int] \| None]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | line.strip、line.startswith、strip、json.loads、isinstance、normalize_provider_usage、data.get、get、delta.get |
| 复杂度 / 风险 | 分支 7；跨度 27 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c5e317f9c8"></a>

#### FUN-C5E317F9C8

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient._parse_sse_line` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L131` |
| 签名 | `LLMClient._parse_sse_line(self, line: str)` |
| 参数 | `line`（str）：由 `line` 表示的文本或标识 |
| 返回 | 返回 `str \| None` 类型结果 |
| 职责 | 解析`sse_line`；返回 `str \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self._parse_sse_event`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self._parse_sse_event |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-b2c894bd12"></a>

#### FUN-B2C894BD12

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.chat_stream` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L136` |
| 签名 | `LLMClient.chat_stream(self, messages: list[dict[str, str]], *, temperature: float=0.3, response_format: dict[str, str] \| None=None, include_usage: bool \| None=None)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`temperature`（float）：模型采样温度；默认值 `0.3`<br>`response_format`（dict[str, str] \| None）：由 `response_format` 表示的键值映射；默认值 `None`<br>`include_usage`（bool \| None）：由调用方提供的 `include_usage` 输入对象；默认值 `None` |
| 返回 | 返回 `Iterator[str]` 类型结果 |
| 职责 | 生成`chat_stream`文本；可能影响外部接口；返回 `Iterator[str]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `log.debug` → `requests.post` → `self._headers` → `self._request_timeout` → `LLMClientError` → `resp.iter_lines` → `raw.decode` → `isinstance`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束；外部客户端、凭据、网络和超时策略已按运行配置准备 |
| 后置条件 | 返回 `Iterator[str]` 类型结果；可观察变化限于外部接口 |
| 显式异常 | LLMClientError |
| 副作用 | 外部接口 I/O |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool、log.debug、requests.post、self._headers、self._request_timeout、LLMClientError、resp.iter_lines、raw.decode、isinstance、str、self._parse_sse_event |
| 复杂度 / 风险 | 分支 11；跨度 74 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) · 直接动态测试 |

<a id="fun-feaf06c7c1"></a>

#### FUN-FEAF06C7C1

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.chat` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L211` |
| 签名 | `LLMClient.chat(self, messages: list[dict[str, str]], *, temperature: float=0.3, response_format: dict[str, str] \| None=None)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`temperature`（float）：模型采样温度；默认值 `0.3`<br>`response_format`（dict[str, str] \| None）：由 `response_format` 表示的键值映射；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`chat`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.chat_stream` → `strip` → `join` → `LLMClientError`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | LLMClientError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | list、self.chat_stream、strip、join、LLMClientError |
| 复杂度 / 风险 | 分支 1；跨度 18 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-cc950a51e1"></a>

#### FUN-CC950A51E1

| 设计项 | 说明 |
|---|---|
| 函数 | `LLMClient.chat_json` |
| 源码位置 | [src/llm/client.py](../../../src/llm/client.py) · `L230` |
| 签名 | `LLMClient.chat_json(self, messages: list[dict[str, str]], *, temperature: float=0.2)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`temperature`（float）：模型采样温度；默认值 `0.2` |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`chat_json`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `self.chat` → `json.loads` → `LLMClientError` → `isinstance`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | LLMClientError |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | self.chat、json.loads、LLMClientError、isinstance |
| 复杂度 / 风险 | 分支 2；跨度 13 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-deb0d517c6"></a>

### UNIT-DEB0D517C6

**模块**：`src/llm/format_io.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-DEB0D517C6 |
| 源码 | [src/llm/format_io.py](../../../src/llm/format_io.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/format_io.py` 的职责，通过 `format_llm_output`、`format_messages`、`messages_to_dict` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 3 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[format_llm_output](#fun-9200a4bf77) · [format_messages](#fun-0d23896651) · [messages_to_dict](#fun-c67d97c1fe)

<a id="fun-9200a4bf77"></a>

#### FUN-9200A4BF77

| 设计项 | 说明 |
|---|---|
| 函数 | `format_llm_output` |
| 源码位置 | [src/llm/format_io.py](../../../src/llm/format_io.py) · `L9` |
| 签名 | `format_llm_output(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`llm_output`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `text.strip` → `json.dumps` → `json.loads`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | text.strip、json.dumps、json.loads |
| 复杂度 / 风险 | 分支 2；跨度 9 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-0d23896651"></a>

#### FUN-0D23896651

| 设计项 | 说明 |
|---|---|
| 函数 | `format_messages` |
| 源码位置 | [src/llm/format_io.py](../../../src/llm/format_io.py) · `L20` |
| 签名 | `format_messages(messages: list[dict[str, str]], *, max_chars: int=12000)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`max_chars`（int）：由 `max_chars` 表示的数值参数；默认值 `12000` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化LLM 消息集合；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `msg.get` → `strip` → `lines.append` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | msg.get、strip、lines.append、join、len |
| 复杂度 / 风险 | 分支 2；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-c67d97c1fe"></a>

#### FUN-C67D97C1FE

| 设计项 | 说明 |
|---|---|
| 函数 | `messages_to_dict` |
| 源码位置 | [src/llm/format_io.py](../../../src/llm/format_io.py) · `L32` |
| 签名 | `messages_to_dict(messages: list[dict[str, str]])` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列 |
| 返回 | 返回 `list[dict[str, Any]]` 类型结果 |
| 职责 | 构建`messages_to_dict`；返回 `list[dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `m.get`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `list[dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | m.get |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-fbf77b94fb"></a>

### UNIT-FBF77B94FB

**模块**：`src/llm/narrative_output.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-FBF77B94FB |
| 源码 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/narrative_output.py` 的职责，通过 `format_llm_narrative` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 5 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[_try_parse_json](#fun-5605d6120b) · [_bullet_list](#fun-65868418a4) · [_fmt_advisor_wording](#fun-4cd834dcdc) · [_fmt_generic](#fun-ac5a907908) · [format_llm_narrative](#fun-3b28d5a15c)

<a id="fun-5605d6120b"></a>

#### FUN-5605D6120B

| 设计项 | 说明 |
|---|---|
| 函数 | `_try_parse_json` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L10` |
| 签名 | `_try_parse_json(raw: str)` |
| 参数 | `raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, Any] \| None` 类型结果 |
| 职责 | 解析`try_json`；返回 `dict[str, Any] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `json.loads` → `isinstance`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、json.loads、isinstance |
| 复杂度 / 风险 | 分支 3；跨度 9 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-65868418a4"></a>

#### FUN-65868418A4

| 设计项 | 说明 |
|---|---|
| 函数 | `_bullet_list` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L21` |
| 签名 | `_bullet_list(items: list[Any], *, limit: int=8)` |
| 参数 | `items`（list[Any]）：输入项集合<br>`limit`（int）：返回或处理数量上限；默认值 `8` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`bullet_list`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `escape` → `strip` → `join`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | escape、str、strip、join |
| 复杂度 / 风险 | 分支 1；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4cd834dcdc"></a>

#### FUN-4CD834DCDC

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_advisor_wording` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L26` |
| 签名 | `_fmt_advisor_wording(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_advisor_wording`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `escape` → `data.get` → `_bullet_list` → `parts.append` → `join`；包含 2 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | escape、str、data.get、_bullet_list、list、parts.append、join |
| 复杂度 / 风险 | 分支 2；跨度 13 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-ac5a907908"></a>

#### FUN-AC5A907908

| 设计项 | 说明 |
|---|---|
| 函数 | `_fmt_generic` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L41` |
| 签名 | `_fmt_generic(data: dict[str, Any])` |
| 参数 | `data`（dict[str, Any]）：输入数据 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`fmt_generic`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `escape` → `json.dumps`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | escape、json.dumps |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-3b28d5a15c"></a>

#### FUN-3B28D5A15C

| 设计项 | 说明 |
|---|---|
| 函数 | `format_llm_narrative` |
| 源码位置 | [src/llm/narrative_output.py](../../../src/llm/narrative_output.py) · `L46` |
| 签名 | `format_llm_narrative(stage: str, raw: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 格式化`llm_narrative`；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `strip` → `_try_parse_json` → `escape` → `_fmt_advisor_wording` → `_fmt_generic`；包含 4 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | strip、_try_parse_json、escape、len、_fmt_advisor_wording、_fmt_generic |
| 复杂度 / 风险 | 分支 4；跨度 17 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-6568b95afa"></a>

### UNIT-6568B95AFA

**模块**：`src/llm/router.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-6568B95AFA |
| 源码 | [src/llm/router.py](../../../src/llm/router.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/router.py` 的职责，通过 `client_for_stage`、`llm_configured` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 2 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | — |
| 验证状态 | selected |

#### 函数导航

[client_for_stage](#fun-4719de86ff) · [llm_configured](#fun-32ab5acbe0)

<a id="fun-4719de86ff"></a>

#### FUN-4719DE86FF

| 设计项 | 说明 |
|---|---|
| 函数 | `client_for_stage` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L15` |
| 签名 | `client_for_stage(stage: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `LLMClient` 类型结果 |
| 职责 | 生成`client_for_stage`结果；返回 `LLMClient` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `LLMClient`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `LLMClient` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | LLMClient |
| 复杂度 / 风险 | 分支 0；跨度 10 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-32ab5acbe0"></a>

#### FUN-32AB5ACBE0

| 设计项 | 说明 |
|---|---|
| 函数 | `llm_configured` |
| 源码位置 | [src/llm/router.py](../../../src/llm/router.py) · `L27` |
| 签名 | `llm_configured()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `bool` 类型结果 |
| 职责 | 判断`llm_configured`条件是否成立；返回 `bool` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `bool` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | bool |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="unit-31083eb5d0"></a>

### UNIT-31083EB5D0

**模块**：`src/llm/stage.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-31083EB5D0 |
| 源码 | [src/llm/stage.py](../../../src/llm/stage.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/stage.py` 的职责，通过 `stream_llm_json`、`run_llm_stage` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 6 / 1 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_json.py](../../../tests/unit/test_llm_json.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) |
| 验证状态 | selected |

#### 高风险设计评审清单

| 函数 | 职责 | 副作用 | 验证 |
|---|---|---|---|
| [run_llm_stage](#fun-f57b2fe384) | 执行`llm_stage`；可能影响共享状态；返回 `tuple[T \| None, LLMStageTrace]` 类型结果。 | 共享状态变更 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) |

#### 函数导航

[_backoff_seconds](#fun-135329b2eb) · [_parse_llm_json](#fun-4d72f972ff) · [_stream_once](#fun-7e0b5443e6) · [_add_provider_usage](#fun-4ac0fc04c1) · [stream_llm_json](#fun-46cd856473) · [run_llm_stage](#fun-f57b2fe384)

<a id="fun-135329b2eb"></a>

#### FUN-135329B2EB

| 设计项 | 说明 |
|---|---|
| 函数 | `_backoff_seconds` |
| 源码位置 | [src/llm/stage.py](../../../src/llm/stage.py) · `L30` |
| 签名 | `_backoff_seconds(attempt: int)` |
| 参数 | `attempt`（int）：由 `attempt` 表示的数值参数 |
| 返回 | 返回 `float` 类型结果 |
| 职责 | 计算`backoff_seconds`；返回 `float` 类型结果。 |
| 处理逻辑 | 直接通过表达式、字段访问或常量完成处理；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `float` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | 无直接调用依赖 |
| 复杂度 / 风险 | 分支 0；跨度 4 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-4d72f972ff"></a>

#### FUN-4D72F972FF

| 设计项 | 说明 |
|---|---|
| 函数 | `_parse_llm_json` |
| 源码位置 | [src/llm/stage.py](../../../src/llm/stage.py) · `L36` |
| 签名 | `_parse_llm_json(raw: str)` |
| 参数 | `raw`（str）：尚未标准化的原始输入 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 解析`llm_json`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `raw.strip` → `json.JSONDecodeError` → `text.find` → `text.rfind` → `attempts.append` → `re.sub` → `json.loads` → `isinstance`；包含 6 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | ValueError；json.JSONDecodeError；last_err |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | raw.strip、json.JSONDecodeError、text.find、text.rfind、attempts.append、list、re.sub、json.loads、isinstance、ValueError |
| 复杂度 / 风险 | 分支 6；跨度 27 行；低 |
| 测试 / 验证 | [tests/unit/test_llm_json.py](../../../tests/unit/test_llm_json.py) · 直接动态测试 |

<a id="fun-7e0b5443e6"></a>

#### FUN-7E0B5443E6

| 设计项 | 说明 |
|---|---|
| 函数 | `_stream_once` |
| 源码位置 | [src/llm/stage.py](../../../src/llm/stage.py) · `L65` |
| 签名 | `_stream_once(client: LLMClient, messages: list[dict[str, str]], *, stage: str, temperature: float)` |
| 参数 | `client`（LLMClient）：外部服务客户端<br>`messages`（list[dict[str, str]]）：消息序列<br>`stage`（str）：流水线或 Agent 阶段标识<br>`temperature`（float）：模型采样温度 |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stream_once`文本；可能影响共享状态；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_progress` → `prog.run_llm_stream` → `client.chat_stream`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_progress、prog.run_llm_stream、client.chat_stream |
| 复杂度 / 风险 | 分支 0；跨度 17 行；低 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) · 直接动态测试 |

<a id="fun-4ac0fc04c1"></a>

#### FUN-4AC0FC04C1

| 设计项 | 说明 |
|---|---|
| 函数 | `_add_provider_usage` |
| 源码位置 | [src/llm/stage.py](../../../src/llm/stage.py) · `L84` |
| 签名 | `_add_provider_usage(total: dict[str, int] \| None, attempt: dict[str, int] \| None)` |
| 参数 | `total`（dict[str, int] \| None）：由 `total` 表示的键值映射<br>`attempt`（dict[str, int] \| None）：由 `attempt` 表示的键值映射 |
| 返回 | 返回 `dict[str, int] \| None` 类型结果 |
| 职责 | 添加`provider_usage`；返回 `dict[str, int] \| None` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `attempt.get` → `merged.get`；包含 3 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int] \| None` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | dict、attempt.get、int、merged.get |
| 复杂度 / 风险 | 分支 3；跨度 12 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-46cd856473"></a>

#### FUN-46CD856473

| 设计项 | 说明 |
|---|---|
| 函数 | `stream_llm_json` |
| 源码位置 | [src/llm/stage.py](../../../src/llm/stage.py) · `L98` |
| 签名 | `stream_llm_json(client: LLMClient, messages: list[dict[str, str]], *, stage: str, temperature: float=0.2, max_attempts: int \| None=None)` |
| 参数 | `client`（LLMClient）：外部服务客户端<br>`messages`（list[dict[str, str]]）：消息序列<br>`stage`（str）：流水线或 Agent 阶段标识<br>`temperature`（float）：模型采样温度；默认值 `0.2`<br>`max_attempts`（int \| None）：由调用方提供的 `max_attempts` 输入对象；默认值 `None` |
| 返回 | 返回 `str` 类型结果 |
| 职责 | 生成`stream_llm_json`文本；返回 `str` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_stage_policy` → `max` → `range` → `min` → `_stream_once` → `_backoff_seconds` → `log.warning` → `time.sleep`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `str` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | last_exc |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_stage_policy、max、int、range、min、_stream_once、_backoff_seconds、log.warning、time.sleep |
| 复杂度 / 风险 | 分支 5；跨度 39 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_llm_transport.py](../../../tests/unit/test_llm_transport.py) · 直接动态测试 |

<a id="fun-f57b2fe384"></a>

#### FUN-F57B2FE384

| 设计项 | 说明 |
|---|---|
| 函数 | `run_llm_stage` |
| 源码位置 | [src/llm/stage.py](../../../src/llm/stage.py) · `L139` |
| 签名 | `run_llm_stage(*, stage: str, model: str, client: LLMClient, messages: list[dict[str, str]], parse: Callable[[dict[str, Any]], T], temperature: float=0.2)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识<br>`model`（str）：模型名称或模型对象<br>`client`（LLMClient）：外部服务客户端<br>`messages`（list[dict[str, str]]）：消息序列<br>`parse`（Callable[[dict[str, Any]], T]）：调用方提供的回调函数<br>`temperature`（float）：模型采样温度；默认值 `0.2` |
| 返回 | 返回 `tuple[T \| None, LLMStageTrace]` 类型结果 |
| 职责 | 执行`llm_stage`；可能影响共享状态；返回 `tuple[T \| None, LLMStageTrace]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `get_stage_policy` → `build_routing_strategy` → `apply_input_budget` → `log.warning` → `budget_meta.get` → `get_progress` → `routing.get` → `prog.llm_begin`；包含 11 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[T \| None, LLMStageTrace]` 类型结果；可观察变化限于共享状态 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 共享状态变更 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | get_stage_policy、build_routing_strategy、apply_input_budget、log.warning、budget_meta.get、get_progress、routing.get、prog.llm_begin、time.perf_counter、range、min、_stream_once、getattr、_add_provider_usage、_parse_llm_json、parse、int、estimate_text_size、prog.llm_end、log.info |
| 复杂度 / 风险 | 分支 11；跨度 204 行；高 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="unit-e488978a91"></a>

### UNIT-E488978A91

**模块**：`src/llm/stage_policy.py`（软件单元详细设计）

| 属性 | 内容 |
|---|---|
| 软件单元 ID | UNIT-E488978A91 |
| 源码 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) |
| 架构组件 | ARC-LLM — Optional advice wording service |
| 职责 | 实现“Optional advice wording service”组件中 `src/llm/stage_policy.py` 的职责，通过 `StagePolicy`、`get_stage_policy`、`estimate_messages_size`、`estimate_text_size`、`apply_input_budget`、`build_routing_strategy` 提供该模块的公开能力。 |
| 关联需求 | [SWR-LLM-001](../SWE.1-software-requirements.md#swr-llm-001)、[SWR-LLM-002](../SWE.1-software-requirements.md#swr-llm-002)、[SWR-CFG-001](../SWE.1-software-requirements.md#swr-cfg-001)、[SWR-NFR-001](../SWE.1-software-requirements.md#swr-nfr-001) |
| 函数 / 高风险函数 | 8 / 0 |
| 验证措施 | [VM-STATIC](../SWE.6-validation-testing.md#vm-static)、[VM-UNIT](../SWE.4-unit-testing.md#vm-unit)、[VM-REGRESSION](../SWE.6-validation-testing.md#vm-regression)、[VM-INTEGRATION-PIPELINE](../SWE.5-integration-testing.md#vm-integration-pipeline) |
| 动态测试 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py)、[tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) |
| 验证状态 | selected |

#### 函数导航

[StagePolicy.to_dict](#fun-8a092a53c7) · [_default_attempts](#fun-16718e4e98) · [_policies](#fun-500b8f3420) · [get_stage_policy](#fun-1d1021888e) · [estimate_messages_size](#fun-931519418f) · [estimate_text_size](#fun-288812bac3) · [apply_input_budget](#fun-639af5aafb) · [build_routing_strategy](#fun-e3b03c5e15)

<a id="fun-8a092a53c7"></a>

#### FUN-8A092A53C7

| 设计项 | 说明 |
|---|---|
| 函数 | `StagePolicy.to_dict` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L29` |
| 签名 | `StagePolicy.to_dict(self)` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 将当前对象转换为可序列化字典；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `asdict`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | asdict |
| 复杂度 / 风险 | 分支 0；跨度 2 行；中 |
| 测试 / 验证 | [tests/unit/test_run_config.py](../../../tests/unit/test_run_config.py) · 直接动态测试 |

<a id="fun-16718e4e98"></a>

#### FUN-16718E4E98

| 设计项 | 说明 |
|---|---|
| 函数 | `_default_attempts` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L33` |
| 签名 | `_default_attempts()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `int` 类型结果 |
| 职责 | 计算`default_attempts`；返回 `int` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `max` → `min`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `int` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | max、min、int |
| 复杂度 / 风险 | 分支 0；跨度 3 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-500b8f3420"></a>

#### FUN-500B8F3420

| 设计项 | 说明 |
|---|---|
| 函数 | `_policies` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L38` |
| 签名 | `_policies()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, StagePolicy]` 类型结果 |
| 职责 | 构建`policies`；返回 `dict[str, StagePolicy]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_default_attempts` → `StagePolicy`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, StagePolicy]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _default_attempts、int、StagePolicy |
| 复杂度 / 风险 | 分支 0；跨度 14 行；低 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-1d1021888e"></a>

#### FUN-1D1021888E

| 设计项 | 说明 |
|---|---|
| 函数 | `get_stage_policy` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L54` |
| 签名 | `get_stage_policy(stage: str)` |
| 参数 | `stage`（str）：流水线或 Agent 阶段标识 |
| 返回 | 返回 `StagePolicy` 类型结果 |
| 职责 | 获取`stage_policy`；返回 `StagePolicy` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `_policies` → `_default_attempts` → `StagePolicy`；包含 1 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `StagePolicy` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | _policies、_default_attempts、StagePolicy、int |
| 复杂度 / 风险 | 分支 1；跨度 14 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_client_timeouts.py](../../../tests/unit/test_llm_client_timeouts.py)、[tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="fun-931519418f"></a>

#### FUN-931519418F

| 设计项 | 说明 |
|---|---|
| 函数 | `estimate_messages_size` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L70` |
| 签名 | `estimate_messages_size(messages: list[dict[str, str]])` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列 |
| 返回 | 返回 `dict[str, int]` 类型结果 |
| 职责 | 估算`messages_size`；返回 `dict[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `sum` → `m.get` → `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | sum、len、str、m.get、int、round |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-288812bac3"></a>

#### FUN-288812BAC3

| 设计项 | 说明 |
|---|---|
| 函数 | `estimate_text_size` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L78` |
| 签名 | `estimate_text_size(text: str)` |
| 参数 | `text`（str）：输入文本 |
| 返回 | 返回 `dict[str, int]` 类型结果 |
| 职责 | 估算`text_size`；返回 `dict[str, int]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `round`；不包含显式控制分支。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, int]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | len、int、round |
| 复杂度 / 风险 | 分支 0；跨度 6 行；中 |
| 测试 / 验证 | — · 静态分析与组件级验证 |

<a id="fun-639af5aafb"></a>

#### FUN-639AF5AAFB

| 设计项 | 说明 |
|---|---|
| 函数 | `apply_input_budget` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L86` |
| 签名 | `apply_input_budget(messages: list[dict[str, str]], policy: StagePolicy)` |
| 参数 | `messages`（list[dict[str, str]]）：消息序列<br>`policy`（StagePolicy）：由调用方提供的 `policy` 输入对象 |
| 返回 | 返回 `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]` 类型结果 |
| 职责 | 应用`input_budget`；返回 `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `estimate_messages_size` → `enumerate` → `m.get` → `range` → `max` → `get` → `meta.update`；包含 5 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新。 |
| 前置条件 | 调用方提供满足参数类型、取值语义和默认值约定的输入；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `tuple[list[dict[str, str]], BudgetAction, dict[str, Any]]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | estimate_messages_size、dict、enumerate、m.get、list、range、len、max、str、get、meta.update |
| 复杂度 / 风险 | 分支 5；跨度 54 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |

<a id="fun-e3b03c5e15"></a>

#### FUN-E3B03C5E15

| 设计项 | 说明 |
|---|---|
| 函数 | `build_routing_strategy` |
| 源码位置 | [src/llm/stage_policy.py](../../../src/llm/stage_policy.py) · `L142` |
| 签名 | `build_routing_strategy()` |
| 参数 | 无显式输入参数 |
| 返回 | 返回 `dict[str, Any]` 类型结果 |
| 职责 | 构建`routing_strategy`；返回 `dict[str, Any]` 类型结果。 |
| 处理逻辑 | 按源码执行顺序经过 `p.to_dict` → `items` → `_policies`；不包含显式控制分支。 |
| 前置条件 | 无需调用方提供显式参数；所属软件单元已经初始化并满足关联需求约束 |
| 后置条件 | 返回 `dict[str, Any]` 类型结果；静态扫描未发现直接外部副作用 |
| 显式异常 | 未发现显式 raise |
| 副作用 | 未检测到直接副作用 |
| 并发约束 | 在调用方线程同步执行 |
| 调用依赖 | p.to_dict、items、_policies |
| 复杂度 / 风险 | 分支 0；跨度 10 行；中 |
| 测试 / 验证 | [tests/unit/test_llm_stage_policy.py](../../../tests/unit/test_llm_stage_policy.py) · 直接动态测试 |
