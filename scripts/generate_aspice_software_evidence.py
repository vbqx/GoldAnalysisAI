#!/usr/bin/env python3
"""Generate SWE.3-SWE.6 as-built design and verification evidence.

The generator reads production source and tests but writes only controlled
documents under ``docs/aspice``. It never edits product code.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASPICE = ROOT / "docs" / "aspice"
MACHINE = ASPICE / "_machine"
ARCH_PATH = MACHINE / "software-architecture.yaml"
REQ_PATH = MACHINE / "software-requirements.yaml"
RESULT_PATH = ASPICE / "verification-results" / "software-domain-2026-07-18.yaml"
FUNCTION_PATH = MACHINE / "software-function-detailed-design.csv"
UNIT_VERIFICATION_PATH = MACHINE / "software-unit-verification-matrix.csv"
REQUIREMENT_COVERAGE_PATH = MACHINE / "software-requirement-verification-coverage.csv"
SOURCE_EXCLUDES = {".git", ".venv", ".cache", ".pytest_cache", "__pycache__", "tests"}
CRITICAL_PATHS = {
    "src/core/orchestrator.py",
    "src/analysis/claim_eligibility.py",
    "src/backtest/simulator.py",
    "src/viz/lightweight_chart.py",
}


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10].upper()
    return f"{prefix}-{digest}"


def _source_files() -> list[Path]:
    return sorted(
        (
            path
            for path in ROOT.rglob("*.py")
            if not any(part in SOURCE_EXCLUDES for part in path.relative_to(ROOT).parts)
        ),
        key=lambda path: _rel(path).casefold(),
    )


def _test_corpus() -> dict[str, str]:
    return {
        _rel(path): path.read_text(encoding="utf-8-sig", errors="replace")
        for path in sorted(
            (ROOT / "tests").rglob("test_*.py"),
            key=lambda item: _rel(item).casefold(),
        )
    }


def _token_references(token: str, corpus: dict[str, str]) -> list[str]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])")
    return [path for path, text in corpus.items() if pattern.search(text)]


def _component_for(path: str) -> str:
    if path in {"app.py", "run_app.py"} or path.startswith("views/"):
        return "ARC-APP"
    for prefix, component in (
        ("src/data/", "ARC-DATA"),
        ("src/indicators/", "ARC-INDICATORS"),
        ("src/analysis/", "ARC-ANALYSIS"),
        ("src/agents/", "ARC-AGENTS"),
        ("src/llm/", "ARC-LLM"),
        ("src/run/", "ARC-RUN"),
        ("src/backtest/", "ARC-BACKTEST"),
        ("src/viz/", "ARC-VIZ"),
        ("scripts/", "ARC-TOOLS"),
    ):
        if path.startswith(prefix):
            return component
    return "ARC-CORE"


def _qualname(node: ast.FunctionDef | ast.AsyncFunctionDef, parents: dict[ast.AST, ast.AST]) -> str:
    owners: list[str] = []
    parent = parents.get(node)
    while parent is not None:
        if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            owners.append(parent.name)
        parent = parents.get(parent)
    return ".".join([*reversed(owners), node.name])


def _call_name(call: ast.Call) -> str:
    value = call.func
    parts: list[str] = []
    while isinstance(value, ast.Attribute):
        parts.append(value.attr)
        value = value.value
    if isinstance(value, ast.Name):
        parts.append(value.id)
    return ".".join(reversed(parts)) or "dynamic-call"


ARGUMENT_PURPOSES = {
    "path": "文件或目录路径", "root": "项目根目录", "config": "运行配置", "ctx": "运行上下文",
    "context": "运行上下文", "df": "输入数据表", "data": "输入数据", "payload": "结构化载荷",
    "report": "分析报告", "result": "处理结果", "results": "结果集合", "value": "待处理值",
    "values": "待处理值集合", "items": "输入项集合", "text": "输入文本", "name": "对象名称",
    "key": "索引键", "id": "对象标识", "timestamp": "时间戳", "as_of": "数据截止时间",
    "client": "外部服务客户端", "session": "会话对象", "state": "状态对象", "event": "事件对象",
    "callback": "回调函数", "timeout": "超时秒数", "port": "监听端口", "pid": "进程标识",
    "price": "当前或待评估价格", "stage": "流水线或 Agent 阶段标识", "direction": "交易方向",
    "team": "分析团队结果", "signals": "交易信号集合", "proposal": "候选交易方案",
    "analyses": "各时间框架分析结果", "label": "展示或分类标签", "row": "当前记录行", "rows": "记录行集合",
    "sig": "待评估交易信号", "messages": "消息序列", "swing_low": "摆动低点价格", "swing_high": "摆动高点价格",
    "limit": "返回或处理数量上限", "facts": "结构化事实集合", "meta": "审计或处理元数据",
    "high": "最高价序列或上界", "low": "最低价序列或下界", "analysis": "当前分析结果",
    "signal": "当前交易信号", "timeframe": "行情时间框架", "entry_high": "入场区间上界", "entry_low": "入场区间下界",
    "pipeline": "流水线对象或结果", "debate": "多角色辩论结果", "source": "数据或证据来源",
    "model": "模型名称或模型对象", "registry": "事实或证据登记映射", "atr": "平均真实波幅",
    "raw": "尚未标准化的原始输入", "analysis_5m": "5 分钟周期分析", "analysis_15m": "15 分钟周期分析",
    "agent": "Agent 实例或标识", "reviews": "风险或评审结果集合", "detail": "详细说明文本",
    "enriched": "已补充指标的行情数据", "tf": "时间框架简称", "reason": "判定或拒绝原因",
    "df_5m": "5 分钟 OHLCV 数据表", "current_price": "当前市场价格", "level": "候选价格水平",
    "kind": "类别标识", "node": "AST 或结构节点", "events": "事件集合", "error": "错误信息或异常对象",
    "trace": "Agent 或流水线追踪记录", "sentiment": "市场情绪结果", "levels": "候选价格水平集合",
    "fetched": "数据获取结果", "records": "结构化记录集合", "observation_mode": "观察模式开关或策略",
    "signal_count": "信号数量", "temperature": "模型采样温度", "bullish": "看多证据或计数",
    "bearish": "看空证据或计数", "symbol": "交易品种代码", "dxy_daily": "美元指数日线数据",
    "price_action": "价格行为分析结果", "bars": "K 线记录集合", "period": "计算周期长度", "url": "外部资源地址",
    "score": "评分值", "decision": "最终或阶段决策", "validated_plans": "已通过校验的交易计划集合",
    "latency_ms": "延迟毫秒数", "zones": "价格区域集合", "data_as_of": "数据截止时间",
    "tolerance": "数值比较容差", "output": "输出对象或输出路径", "token": "标记或认证令牌",
    "entry": "入场价格或入场记录", "stop_loss": "止损价格", "take_profits": "止盈目标集合",
    "headers": "表头或 HTTP 头字段", "steps": "执行步骤集合", "telemetry": "遥测记录",
    "item": "当前处理条目", "summary": "摘要内容", "risk_reviews": "风险评审集合",
    "mode": "运行或分析模式", "arch": "软件架构模型", "verification": "验证证据或验证配置",
}

ACTION_WORDS = {
    "ensure": "确保", "load": "加载", "read": "读取", "write": "写入", "save": "保存",
    "build": "构建", "create": "创建", "make": "构造", "get": "获取", "fetch": "获取",
    "find": "查找", "resolve": "解析并选择", "parse": "解析", "format": "格式化", "render": "渲染",
    "calculate": "计算", "compute": "计算", "validate": "验证", "check": "检查", "is": "判断",
    "has": "判断", "run": "执行", "execute": "执行", "update": "更新", "merge": "合并",
    "normalize": "标准化", "serialize": "序列化", "deserialize": "反序列化", "extract": "提取",
    "collect": "收集", "filter": "筛选", "select": "选择", "convert": "转换", "dedupe": "去重",
    "apply": "应用", "simulate": "模拟", "score": "评分", "classify": "分类", "estimate": "估算",
    "detect": "检测", "append": "追加", "add": "添加", "remove": "移除", "delete": "删除",
    "sort": "排序", "group": "分组", "init": "初始化", "reset": "重置", "close": "关闭",
    "open": "打开", "send": "发送", "emit": "发布", "publish": "发布", "archive": "归档",
    "import": "导入", "export": "导出", "aggregate": "聚合", "summarize": "汇总", "start": "启动",
    "stop": "停止", "terminate": "终止", "encode": "编码", "decode": "解码", "split": "拆分",
}

TARGET_LABELS = {
    "streamlit_runtime": "Streamlit 运行时上下文", "dotenv": ".env 环境变量", "dev_env": "开发环境变量",
    "streamlit_config": "Streamlit 配置文件", "python": "Python 解释器", "pids": "进程标识集合",
    "listening_on_port": "监听指定端口的进程", "line_for_pid": "指定进程的命令行", "project_streamlit_pid": "本项目 Streamlit 进程",
    "stale_streamlit": "遗留 Streamlit 进程", "args": "命令行参数", "document_register": "文档登记表",
    "classification": "文档过程分类", "title": "文档标题", "units": "软件单元清单", "trace_rows": "追溯记录",
    "outputs": "生成产物", "model": "ASPICE 数据模型", "files": "文件清单", "yaml": "YAML 数据",
    "json": "JSON 数据", "csv": "CSV 数据", "links": "Markdown 链接", "anchor": "Markdown 锚点",
    "report": "报告", "context": "上下文", "payload": "结构化载荷", "evidence": "证据", "evidence_items": "证据条目",
    "evidence_ids": "证据标识", "registry": "登记映射", "research_items": "研究证据条目", "confidence": "置信度",
    "signal": "交易信号", "signals": "交易信号集合", "decision": "决策", "risk": "风险结果", "facts": "事实集合",
    "data": "数据", "frame": "数据表", "frames": "多周期数据表", "state": "状态", "config": "配置",
    "result": "结果", "results": "结果集合", "text": "文本", "index": "索引", "section": "文档章节",
    "contract": "函数契约", "responsibility": "职责描述", "references": "测试引用", "nodes": "参数节点",
    "python_usable": "Python 解释器可用性", "pids_listening_on_port": "监听指定端口的进程标识集合",
    "command_line_for_pid": "指定进程的命令行", "streamlit_pids": "本项目 Streamlit 进程标识集合",
    "terminate_pid": "指定进程", "stable_id": "稳定标识", "rel": "仓库相对路径",
    "source_files": "受审源码文件清单", "document_files": "受控文档清单", "component_for": "源码所属架构组件",
    "module_doc": "模块职责说明", "dependency_outputs": "依赖锁与 SBOM 产物", "csv_text": "CSV 文本",
    "process_index": "ASPICE 过程文档索引", "expected_outputs": "预期生成产物", "write_outputs": "生成产物",
    "check_outputs": "生成产物一致性", "delta": "差值", "sanitize": "可序列化安全值",
    "trade_agent_pipeline": "交易分析 Agent 完整流水线", "lightweight_chart_html": "Lightweight Charts 交互图表 HTML",
    "claim_eligibility": "技术主张证据资格", "report_invariants": "报告不变量", "report_reliability": "报告可靠度",
    "analyst_team": "分析师团队结果", "fundamentals_analyst": "基本面分析 Agent", "news_analyst": "新闻分析 Agent",
    "sentiment_analyst": "情绪分析 Agent", "technical_analyst": "技术分析 Agent", "manager": "管理 Agent 决策",
    "run_config": "运行配置", "external": "外部数据快照", "liquidity": "流动性结构", "structure_event": "市场结构事件",
    "system_proxy": "系统代理配置", "account_info": "交易账户信息", "llm_payload": "LLM 阶段载荷",
    "signal_value": "信号数值", "nearest_pa_sr": "最近价格行为支撑阻力", "fvg": "公允价值缺口",
    "order_block": "订单块", "structure_items": "结构条目集合", "signal_geometry": "交易信号价格几何",
    "llm_io_records": "LLM 输入输出记录", "streaming_llm_record": "流式 LLM 调用记录", "fmt_price": "价格显示值",
    "multi_timeframe": "多时间框架分析", "source_label": "数据来源标签", "messages": "LLM 消息集合",
    "archive_zip": "运行归档压缩包", "key_levels": "关键价格水平", "risk_reward": "风险收益比",
    "indicator_snapshot": "指标快照", "manifest": "归档清单", "calendar_state": "经济日历状态",
    "llm_stream": "LLM 流式响应", "stage_io": "阶段输入输出遥测", "generation_id": "生成任务标识",
}

ACTION_ONLY_TARGETS = {
    "fetch": "外部或市场数据", "load": "持久化数据", "save": "当前结果", "run": "当前处理流程",
    "build": "目标结构", "create": "目标对象", "update": "当前状态", "render": "当前界面区域",
    "parse": "输入内容", "format": "输出文本", "validate": "输入和状态", "check": "约束条件",
    "close": "当前资源", "open": "目标资源", "start": "当前任务", "stop": "当前任务",
}


def _argument_nodes(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.arg]:
    return [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]


def _argument_purpose(name: str, annotation: str) -> str:
    if name in ARGUMENT_PURPOSES:
        return ARGUMENT_PURPOSES[name]
    suffix = name.split("_")[-1]
    if suffix in ARGUMENT_PURPOSES:
        return ARGUMENT_PURPOSES[suffix]
    if name.endswith("_id"):
        return "对应对象的稳定标识"
    if name.endswith(("_path", "_dir", "_directory")):
        return "文件系统路径"
    if name.endswith(("_at", "_time", "_timestamp")):
        return "事件或数据时间"
    if name.endswith("_ms"):
        return "毫秒单位的持续时间"
    if name.endswith("_pct"):
        return "百分比数值"
    if name.endswith(("_count", "_limit")):
        return "数量或处理上限"
    if "Callable" in annotation:
        return "调用方提供的回调函数"
    if annotation == "bool" or name.startswith(("is_", "has_", "allow_", "enable_")):
        return "控制对应行为是否启用的布尔值"
    if any(token in annotation for token in ("list", "set", "Sequence", "Iterable")):
        return f"由 `{name}` 表示的输入集合"
    if any(token in annotation for token in ("dict", "Mapping")):
        return f"由 `{name}` 表示的键值映射"
    if annotation in {"int", "float", "Decimal"}:
        return f"由 `{name}` 表示的数值参数"
    if annotation == "str":
        return f"由 `{name}` 表示的文本或标识"
    return f"由调用方提供的 `{name}` 输入对象"


def _parameter_contract(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    parts: list[str] = []
    positional = [*node.args.posonlyargs, *node.args.args]
    defaults: dict[str, ast.expr] = {
        arg.arg: default
        for arg, default in zip(positional[-len(node.args.defaults) :], node.args.defaults)
    } if node.args.defaults else {}
    defaults.update(
        {arg.arg: default for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults) if default is not None}
    )
    for arg in _argument_nodes(node):
        if arg.arg in {"self", "cls"}:
            continue
        annotation = ast.unparse(arg.annotation) if arg.annotation is not None else "实现约定类型"
        purpose = _argument_purpose(arg.arg, annotation)
        default_text = f"；默认值 `{ast.unparse(defaults[arg.arg])}`" if arg.arg in defaults else ""
        parts.append(f"`{arg.arg}`（{annotation}）：{purpose}{default_text}")
    if node.args.vararg:
        parts.append(f"`*{node.args.vararg.arg}`：附加位置参数")
    if node.args.kwarg:
        parts.append(f"`**{node.args.kwarg.arg}`：附加关键字参数")
    return "；".join(parts) or "无显式输入参数"


def _precondition_contract(parameter_contract: str, effects: list[str]) -> str:
    clauses = ["所属软件单元已经初始化并满足关联需求约束"]
    if parameter_contract == "无显式输入参数":
        clauses.insert(0, "无需调用方提供显式参数")
    else:
        clauses.insert(0, "调用方提供满足参数类型、取值语义和默认值约定的输入")
    if "external-io" in effects:
        clauses.append("外部客户端、凭据、网络和超时策略已按运行配置准备")
    if "filesystem" in effects:
        clauses.append("相关路径满足读取或写入权限及目录边界")
    return "；".join(clauses)


def _postcondition_contract(return_contract: str, effects: list[str]) -> str:
    clauses = [return_contract]
    effect_names = {"filesystem": "文件系统", "external-io": "外部接口", "shared-state": "共享状态", "global-state": "全局状态", "async": "异步任务"}
    if effects:
        clauses.append("可观察变化限于" + "、".join(effect_names[item] for item in effects))
    else:
        clauses.append("静态扫描未发现直接外部副作用")
    return "；".join(clauses)


def _return_contract(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    if node.returns is not None:
        annotation = ast.unparse(node.returns)
        return "无返回值（None）" if annotation == "None" else f"返回 `{annotation}` 类型结果"
    has_value = any(isinstance(item, ast.Return) and item.value is not None for item in ast.walk(node))
    return "返回实现分支产生的结果（源码未标注类型）" if has_value else "无返回值（隐式 None）"


def _target_label(tokens: list[str]) -> str:
    raw = "_".join(tokens) if tokens else "当前对象"
    return TARGET_LABELS.get(raw, f"`{raw}`")


def _inferred_purpose(node: ast.FunctionDef | ast.AsyncFunctionDef, return_contract: str, source_path: str) -> str:
    bare_name = node.name.strip("_")
    if node.name == "main":
        return f"执行 `{source_path}` 的主流程"
    if node.name in {"__init__", "__post_init__", "__new__"}:
        return "初始化当前类实例并建立字段约束"
    if node.name == "__len__":
        return "计算当前容器包含的元素数量"
    if node.name == "__iter__":
        return "创建当前容器的迭代访问序列"
    if node.name in {"__enter__", "__aenter__"}:
        return "进入资源上下文并返回可用资源"
    if node.name in {"__exit__", "__aexit__"}:
        return "退出资源上下文并执行清理"
    tokens = [token for token in re.split(r"_+", bare_name) if token]
    if tokens == ["to", "dict"]:
        return "将当前对象转换为可序列化字典"
    if "from" in tokens:
        split = tokens.index("from")
        output = _target_label(tokens[:split])
        source = _target_label(tokens[split + 1 :])
        verb = "计算" if any(word in return_contract for word in ("int", "float", "Decimal")) else "构建"
        return f"根据{source}{verb}{output}"
    action_index = next((index for index, token in enumerate(tokens) if token.lower() in ACTION_WORDS), None)
    if action_index is not None:
        action = ACTION_WORDS[tokens[action_index].lower()]
        target_tokens = [token for index, token in enumerate(tokens) if index != action_index and token not in {"for", "to", "by"}]
        target = _target_label(target_tokens) if target_tokens else ACTION_ONLY_TARGETS.get(tokens[action_index].lower(), "当前对象")
        return f"{action}{target}"
    target = _target_label(tokens)
    if "bool" in return_contract:
        return f"判断{target}条件是否成立"
    if any(word in return_contract for word in ("list", "set", "dict", "tuple", "DataFrame")):
        return f"构建{target}"
    if any(word in return_contract for word in ("int", "float", "Decimal")):
        return f"计算{target}"
    if "str" in return_contract:
        return f"生成{target}文本"
    if return_contract.startswith("无返回值"):
        return f"执行{target}处理"
    return f"生成{target}结果"


def _chinese_responsibility(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    calls: list[str],
    effects: list[str],
    return_contract: str,
    source_path: str,
) -> str:
    doc = ast.get_docstring(node, clean=True) or ""
    first_line = doc.splitlines()[0].rstrip("。.") if doc else ""
    if first_line and re.match(r"[\u4e00-\u9fff]", first_line):
        purpose = first_line
    else:
        purpose = _inferred_purpose(node, return_contract, source_path)
    details: list[str] = [purpose]
    if effects:
        effect_names = {"filesystem": "文件系统", "external-io": "外部接口", "shared-state": "共享状态", "global-state": "全局状态", "async": "异步任务"}
        details.append("可能影响" + "、".join(effect_names[item] for item in effects))
    details.append(return_contract)
    return "；".join(details) + "。"


def _algorithm_summary(calls: list[str], branches: int) -> str:
    ignored = {"str", "int", "float", "bool", "len", "list", "dict", "set", "tuple"}
    meaningful = [name for name in calls if name not in ignored]
    if meaningful:
        sequence = " → ".join(f"`{name}`" for name in meaningful[:8])
        base = f"按源码执行顺序经过 {sequence}"
    else:
        base = "直接通过表达式、字段访问或常量完成处理"
    if branches:
        base += f"；包含 {branches} 个条件、循环、异常或模式匹配分支，分支结果汇入返回或状态更新"
    else:
        base += "；不包含显式控制分支"
    return base + "。"


def _node_contract(node: ast.FunctionDef | ast.AsyncFunctionDef, source_path: str) -> dict[str, str | int]:
    signature = f"({ast.unparse(node.args)})"
    return_contract = _return_contract(node)
    call_nodes = sorted(
        (item for item in ast.walk(node) if isinstance(item, ast.Call)),
        key=lambda item: (getattr(item, "lineno", 0), getattr(item, "col_offset", 0)),
    )
    calls = list(dict.fromkeys(_call_name(item) for item in call_nodes))
    raises = sorted(
        {
            ast.unparse(item.exc.func if isinstance(item.exc, ast.Call) else item.exc)
            for item in ast.walk(node)
            if isinstance(item, ast.Raise) and item.exc is not None
        }
    )
    branches = sum(
        isinstance(item, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.Match, ast.IfExp))
        for item in ast.walk(node)
    )
    call_text = ";".join(calls).lower()
    effects: list[str] = []
    if re.search(r"(?:write_text|write_bytes|\.open|unlink|mkdir|\.rename|to_csv|to_json|json\.dump;)", call_text):
        effects.append("filesystem")
    if re.search(r"(?:requests?\.|httpx\.|urllib|urlopen|websocket|fetch_|download|client\.(?:get|post|request|call)|session\.(?:get|post))", call_text):
        effects.append("external-io")
    if re.search(r"(?:session_state|setenv|environ|cache|progress|emit|publish)", call_text):
        effects.append("shared-state")
    if any(isinstance(item, (ast.Global, ast.Nonlocal)) for item in ast.walk(node)):
        effects.append("global-state")
    if isinstance(node, ast.AsyncFunctionDef):
        effects.append("async")
    summary = _chinese_responsibility(node, calls, effects, return_contract, source_path)
    span = max(1, getattr(node, "end_lineno", node.lineno) - node.lineno + 1)
    parameter_contract = _parameter_contract(node)
    effect_names = {"filesystem": "文件系统读写", "external-io": "外部接口 I/O", "shared-state": "共享状态变更", "global-state": "全局状态变更", "async": "异步任务调度"}
    return {
        "signature": signature,
        "parameter_contract": parameter_contract,
        "return_contract": return_contract,
        "responsibility": summary,
        "algorithm_summary": _algorithm_summary(calls, branches),
        "preconditions": _precondition_contract(parameter_contract, effects),
        "postconditions": _postcondition_contract(return_contract, effects),
        "explicit_exceptions": "；".join(raises) or "未发现显式 raise",
        "side_effects": "；".join(effect_names[item] for item in sorted(set(effects))) or "未检测到直接副作用",
        "call_dependencies": ";".join(calls[:20]) or "none",
        "branch_points": branches,
        "line_span": span,
        "concurrency": "异步协程（async/await）" if isinstance(node, ast.AsyncFunctionDef) else "在调用方线程同步执行",
    }


def _risk(path: str, name: str, contract: dict[str, str | int]) -> str:
    high_name = re.search(r"(?:authoriz|execute|trade|order|simulate|pipeline|invariant|eligib|archive)", name, re.I)
    high_effect = "external-io" in str(contract["side_effects"]) or "外部接口" in str(contract["side_effects"])
    if path in CRITICAL_PATHS or int(contract["line_span"]) >= 150 or high_name or high_effect:
        return "high"
    if int(contract["line_span"]) >= 40 or int(contract["branch_points"]) >= 8 or not name.split(".")[-1].startswith("_"):
        return "medium"
    return "low"


def _csv(rows: list[dict[str, object]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def expected_outputs() -> tuple[dict[Path, str], dict[str, int]]:
    arch = yaml.safe_load(ARCH_PATH.read_text(encoding="utf-8-sig"))
    requirements = yaml.safe_load(REQ_PATH.read_text(encoding="utf-8-sig"))
    results = yaml.safe_load(RESULT_PATH.read_text(encoding="utf-8-sig"))
    components = {item["id"]: item for item in arch["components"]}
    result_map = {item["id"]: item for item in results["measures"]}
    corpus = _test_corpus()
    function_rows: list[dict[str, object]] = []
    unit_functions: dict[str, list[dict[str, object]]] = defaultdict(list)
    unit_test_refs: dict[str, set[str]] = defaultdict(set)

    for source in _source_files():
        path = _rel(source)
        unit_id = _stable_id("UNIT", path)
        component = _component_for(path)
        tree = ast.parse(source.read_text(encoding="utf-8-sig"), filename=path)
        parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        module_name = path.removesuffix(".py").replace("/", ".")
        unit_test_refs[unit_id].update(_token_references(module_name, corpus))
        unit_test_refs[unit_id].update(_token_references(path, corpus))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            name = _qualname(node, parents)
            contract = _node_contract(node, path)
            refs = _token_references(node.name, corpus)
            unit_test_refs[unit_id].update(refs)
            risk = _risk(path, name, contract)
            verification = "direct-dynamic" if refs else "static-and-component"
            row: dict[str, object] = {
                "function_id": _stable_id("FUN", f"{path}:{name}"),
                "software_unit_id": unit_id,
                "source_path": path,
                "line": node.lineno,
                "qualified_name": name,
                "visibility": "internal" if node.name.startswith("_") else "public",
                "signature": contract["signature"],
                "parameter_contract": contract["parameter_contract"],
                "return_contract": contract["return_contract"],
                "responsibility": contract["responsibility"],
                "algorithm_summary": contract["algorithm_summary"],
                "preconditions": contract["preconditions"],
                "postconditions": contract["postconditions"],
                "explicit_exceptions": contract["explicit_exceptions"],
                "side_effects": contract["side_effects"],
                "concurrency": contract["concurrency"],
                "call_dependencies": contract["call_dependencies"],
                "branch_points": contract["branch_points"],
                "line_span": contract["line_span"],
                "risk": risk,
                "architecture_id": component,
                "requirement_ids": ";".join(components[component]["requirements"]),
                "test_references": ";".join(refs),
                "verification_disposition": "直接动态测试" if refs else "静态分析与组件级验证",
                "design_status": "已按实现建立基线",
            }
            function_rows.append(row)
            unit_functions[unit_id].append(row)

    function_rows.sort(key=lambda row: (str(row["source_path"]), int(row["line"]), str(row["qualified_name"])))
    unit_rows: list[dict[str, object]] = []
    blocking_units = 0
    for source in _source_files():
        path = _rel(source)
        unit_id = _stable_id("UNIT", path)
        component = _component_for(path)
        functions = unit_functions[unit_id]
        refs = sorted(unit_test_refs[unit_id])
        high_count = sum(row["risk"] == "high" for row in functions)
        has_dynamic = bool(refs)
        blocking = high_count > 0 and not has_dynamic and not path.startswith("scripts/")
        if blocking:
            blocking_units += 1
        methods = ["VM-STATIC"]
        if has_dynamic:
            methods.append("VM-UNIT")
        if component in {"ARC-CORE", "ARC-ANALYSIS", "ARC-AGENTS", "ARC-LLM", "ARC-RUN"}:
            methods.extend(["VM-REGRESSION", "VM-INTEGRATION-PIPELINE"])
        elif component == "ARC-BACKTEST":
            methods.append("VM-BACKTEST")
        elif component == "ARC-DATA":
            methods.append("VM-INTEGRATION-EXTERNAL")
        elif component in {"ARC-APP", "ARC-VIZ"}:
            methods.append("VM-MANUAL-UI")
        unit_rows.append(
            {
                "software_unit_id": unit_id,
                "source_path": path,
                "architecture_id": component,
                "requirement_ids": ";".join(components[component]["requirements"]),
                "function_count": len(functions),
                "high_risk_function_count": high_count,
                "verification_measure_ids": ";".join(dict.fromkeys(methods)),
                "dynamic_test_references": ";".join(refs),
                "selection_rationale": (
                    "direct unit/component evidence"
                    if has_dynamic
                    else "static analysis selected for low/medium-risk unit"
                ),
                "verification_status": "blocking-gap" if blocking else "selected",
                "waiver_id": "",
            }
        )
    unit_rows.sort(key=lambda row: str(row["source_path"]))
    requirement_rows: list[dict[str, object]] = []
    blocking_requirements = 0
    accepted_outcomes = {"pass", "inherited-pass"}
    for requirement in requirements["requirements"]:
        linked_results = [result_map.get(measure_id) for measure_id in requirement["verification_ids"]]
        selected = [item["id"] for item in linked_results if item and item.get("outcome") in accepted_outcomes]
        blocking = not selected
        if blocking:
            blocking_requirements += 1
        requirement_rows.append(
            {
                "requirement_id": requirement["id"],
                "status": requirement["status"],
                "architecture_ids": ";".join(requirement["architecture_ids"]),
                "verification_measure_ids": ";".join(requirement["verification_ids"]),
                "accepted_result_ids": ";".join(selected),
                "result_outcomes": ";".join(
                    f"{item['id']}={item['outcome']}" for item in linked_results if item
                ),
                "verification_criteria": requirement["verification_criteria"],
                "coverage_status": "closed" if not blocking else "blocking-gap",
            }
        )
    summary = {
        "functions": len(function_rows),
        "units": len(unit_rows),
        "high_risk_functions": sum(row["risk"] == "high" for row in function_rows),
        "functions_with_direct_tests": sum(bool(row["test_references"]) for row in function_rows),
        "blocking_units": blocking_units,
        "requirements": len(requirement_rows),
        "blocking_requirements": blocking_requirements,
    }
    return {
        FUNCTION_PATH: _csv(function_rows),
        UNIT_VERIFICATION_PATH: _csv(unit_rows),
        REQUIREMENT_COVERAGE_PATH: _csv(requirement_rows),
    }, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, summary = expected_outputs()
    errors: list[str] = []
    for path, expected in outputs.items():
        if args.write:
            path.write_text(expected, encoding="utf-8", newline="")
        elif not path.exists():
            errors.append(f"missing generated evidence: {_rel(path)}")
        elif path.read_text(encoding="utf-8-sig") != expected:
            errors.append(f"stale generated evidence: {_rel(path)}")
    if summary["blocking_units"]:
        errors.append(f"{summary['blocking_units']} high-risk software units lack dynamic verification evidence")
    if summary["blocking_requirements"]:
        errors.append(f"{summary['blocking_requirements']} software requirements lack an accepted verification result")
    if errors:
        print("ASPICE software evidence validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        print(summary, file=sys.stderr)
        return 1
    print(f"ASPICE software evidence valid: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
