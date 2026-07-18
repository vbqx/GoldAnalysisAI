#!/usr/bin/env python3
"""Render the ASPICE software-domain evidence as reviewable Markdown.

Machine-oriented YAML/CSV/JSON stays under ``docs/aspice/_machine`` for
deterministic validation. This renderer makes Markdown the normal review
surface and organizes detailed design into one section per software unit.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASPICE = ROOT / "docs" / "aspice"
MACHINE = ASPICE / "_machine"


def _yaml(name: str) -> dict[str, Any]:
    value = yaml.safe_load((MACHINE / name).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain a mapping")
    return value


def _csv(name: str) -> list[dict[str, str]]:
    with (MACHINE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _cell(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        value = "、".join(str(item) for item in value)
    text = str(value).strip() or "—"
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", "<br>")


def _list(value: str) -> str:
    return "、".join(part for part in value.split(";") if part) or "—"


def _anchor(value: str) -> str:
    return value.lower().replace(".", "-").replace("_", "-")


def _req_links(values: list[str] | str, prefix: str = "") -> str:
    items = values.split(";") if isinstance(values, str) else values
    return "、".join(f"[{item}]({prefix}SWE.1-software-requirements.md#{_anchor(item)})" for item in items if item) or "—"


def _arch_links(values: list[str] | str, prefix: str = "") -> str:
    items = values.split(";") if isinstance(values, str) else values
    return "、".join(f"[{item}]({prefix}SWE.2-architecture/software-architecture.md#{_anchor(item)})" for item in items if item) or "—"


def _measure_links(values: list[str] | str, prefix: str = "") -> str:
    items = values.split(";") if isinstance(values, str) else values
    rendered: list[str] = []
    for item in items:
        if not item:
            continue
        target = "SWE.4-unit-testing.md" if item == "VM-UNIT" else "SWE.5-integration-testing.md" if item.startswith("VM-INTEGRATION") or item == "VM-BACKTEST" else "SWE.6-validation-testing.md"
        rendered.append(f"[{item}]({prefix}{target}#{_anchor(item)})")
    return "、".join(rendered) or "—"


def _test_links(value: list[str] | str, root_prefix: str = "../../") -> str:
    items = value.split(";") if isinstance(value, str) else value
    return "、".join(f"[{item}]({root_prefix}{item})" for item in items if item) or "—"


def _table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(_cell(item) for item in row) + " |" for row in rows)
    return lines


def _front(title: str, process: str, purpose: str) -> list[str]:
    return [
        f"# {title}",
        "",
        "| 属性 | 内容 |",
        "|---|---|",
        f"| ASPICE 过程 | {process} |",
        "| 状态 | 受控基线 |",
        f"| 用途 | {purpose} |",
        "",
        "> 本文是人工阅读、评审和变更讨论的正式入口。结构化校验数据位于",
        "> `_machine/`，普通评审无需直接阅读机器文件。",
        "",
    ]


def _requirements_doc(reqs: dict[str, Any]) -> str:
    items = reqs["requirements"]
    lines = _front("SWE.1 软件需求分析", "SWE.1", "理解、评审并追踪软件需求")
    lines += [
        "## 基线概览",
        "",
        f"本基线包含 **{len(items)} 条软件需求**。需求按唯一 ID 管理，并链接到架构组件、验证措施和接受准则。",
        "",
    ]
    priorities: dict[str, int] = defaultdict(int)
    for item in items:
        priorities[item["priority"]] += 1
    lines += _table(["优先级", "数量"], [[key, priorities[key]] for key in sorted(priorities)])
    lines += ["", "## 需求目录", ""]
    lines += _table(
        ["ID", "标题", "类型", "优先级", "状态"],
        [[f"[{item['id']}](#{item['id'].lower()})", item["title"], item["type"], item["priority"], item["status"]] for item in items],
    )
    for item in items:
        lines += [
            "",
            f"<a id=\"{_anchor(item['id'])}\"></a>",
            "",
            f"## {item['id']}",
            "",
            f"**标题**：{item['title']}",
            "",
            item["text"],
            "",
        ]
        lines += _table(
            ["属性", "内容"],
            [
                ["类型 / 优先级 / 状态", f"{item['type']} / {item['priority']} / {item['status']}"],
                ["来源", item["source"]],
                ["验证准则", item["verification_criteria"]],
                ["运行环境影响", item["operating_environment_impact"]],
                ["架构组件", _arch_links(item["architecture_ids"])],
                ["验证措施", _measure_links(item["verification_ids"])],
            ],
        )
    return "\n".join(lines) + "\n"


def _architecture_diagrams() -> list[str]:
    return [
        "## 模块分层图",
        "",
        "本图只表达职责分层，不绘制依赖线；组件 ID 可与后续组件章节直接对应。",
        "",
        "```mermaid",
        "flowchart TB",
        '  subgraph L1["① 交互层"]',
        "    direction LR",
        '    APP["ARC-APP｜应用入口与运行配置"]',
        '    VIZ["ARC-VIZ｜Streamlit 展示"]',
        "  end",
        '  subgraph L2["② 编排层"]',
        "    direction LR",
        '    CORE["ARC-CORE｜主编排与进度"]',
        "  end",
        '  subgraph L3["③ 领域决策层"]',
        "    direction LR",
        '    ANALYSIS["ARC-ANALYSIS｜事实、信号与门禁"]',
        '    AGENTS["ARC-AGENTS｜规则/LLM Agent"]',
        '    BACKTEST["ARC-BACKTEST｜Point-in-time 回测"]',
        "  end",
        '  subgraph L4["④ 技术服务层"]',
        "    direction LR",
        '    DATA["ARC-DATA｜行情与外部数据"]',
        '    IND["ARC-INDICATORS｜指标计算"]',
        '    LLM["ARC-LLM｜模型传输与策略"]',
        '    RUN["ARC-RUN｜运行上下文与归档"]',
        "  end",
        '  subgraph L5["⑤ 工程支撑"]',
        "    direction LR",
        '    TOOLS["ARC-TOOLS｜开发、审核与运维工具"]',
        "  end",
        "```",
        "",
        "## 核心依赖主干图",
        "",
        "仅保留最重要的正向调用和数据主干，返回值、回调及完整接口扇出由后续时序图和接口流向图表达。实线为运行依赖，虚线为工程支撑关系。",
        "",
        "```mermaid",
        "flowchart TB",
        '  APP["ARC-APP｜入口"] -->|启动分析| CORE["ARC-CORE｜主编排"]',
        '  CORE ==>|获取数据| DATA["ARC-DATA｜数据"]',
        '  DATA ==>|标准 OHLCV| IND["ARC-INDICATORS｜指标"]',
        '  IND ==>|指标快照| ANALYSIS["ARC-ANALYSIS｜分析与门禁"]',
        '  ANALYSIS ==>|事实与候选计划| AGENTS["ARC-AGENTS｜决策"]',
        '  AGENTS -->|可选模型阶段| LLM["ARC-LLM｜模型服务"]',
        '  CORE -->|保存运行快照| RUN["ARC-RUN｜归档/回放"]',
        '  ANALYSIS -->|门禁后报告| VIZ["ARC-VIZ｜展示"]',
        '  RUN -->|回放快照| VIZ',
        '  APP -->|独立入口| BACKTEST["ARC-BACKTEST｜回测"]',
        '  BACKTEST -->|回测结果| VIZ',
        '  TOOLS["ARC-TOOLS｜工具"] -.->|检查/导入导出| RUN',
        "```",
        "",
        "## 主流水线时序图",
        "",
        "```mermaid",
        "sequenceDiagram",
        "  actor User as 用户/页面",
        "  participant App as ARC-APP",
        "  participant Core as ARC-CORE",
        "  participant Data as ARC-DATA",
        "  participant Ind as ARC-INDICATORS",
        "  participant Ana as ARC-ANALYSIS",
        "  participant Agents as ARC-AGENTS",
        "  participant LLM as ARC-LLM",
        "  participant Run as ARC-RUN",
        "  participant Viz as ARC-VIZ",
        "  User->>App: 选择模式并启动分析",
        "  App->>Core: run_trade_agent_pipeline(config, progress)",
        "  Core->>Run: 建立 RunContext",
        "  Core->>Data: 获取行情与外部证据",
        "  Data-->>Core: MarketContext + 来源/时效状态",
        "  Core->>Ind: 计算多周期指标",
        "  Ind-->>Ana: enriched OHLCV + 指标快照",
        "  Core->>Ana: 构建事实、结构和候选计划",
        "  Ana->>Agents: 合格事实与候选计划",
        "  opt MODE-LLM 或 MODE-HYBRID",
        "    Agents->>LLM: 分阶段结构化载荷",
        "    LLM-->>Agents: schema 校验后的阶段结果",
        "  end",
        "  Agents-->>Ana: AgentTrace + ManagerDecision",
        "  Ana->>Ana: 执行事实资格与报告不变量门禁",
        "  Ana-->>Core: 门禁后的报告和审计结果",
        "  Core->>Run: 原子保存成功或失败归档",
        "  Core-->>App: report + enriched data + analyses",
        "  App->>Viz: 渲染同一报告快照",
        "  Viz-->>User: 报告、图表和决策审计",
        "```",
        "",
        "## 运行模式与回放边界图",
        "",
        "```mermaid",
        "flowchart TD",
        '  START["RunConfig.mode"] --> MODE{"运行模式"}',
        '  MODE -->|rule| RULE["规则 Agent + 确定性门禁"]',
        '  MODE -->|llm| LLM_MODE["LLM 分阶段决策"]',
        '  MODE -->|hybrid| HYBRID["规则基线 + 合格 LLM 覆盖"]',
        '  MODE -->|replay| REPLAY["从 ARC-RUN 加载归档"]',
        '  RULE --> LIVE_DATA["ARC-DATA 获取当前数据"]',
        '  LLM_MODE --> LIVE_DATA',
        '  HYBRID --> LIVE_DATA',
        '  LIVE_DATA --> PIPELINE["ARC-CORE 主流水线"]',
        '  PIPELINE --> GATE["ARC-ANALYSIS 报告门禁"]',
        '  GATE --> SAVE["ARC-RUN 保存不可变快照"]',
        '  REPLAY --> COMPAT{"schema/manifest 兼容校验"}',
        '  COMPAT -->|通过| SNAPSHOT["加载冻结报告和数据"]',
        '  COMPAT -->|失败| DIAG["返回明确诊断，不执行新分析"]',
        '  SNAPSHOT --> NO_IO["禁止 fetch 和新 LLM 调用"]',
        '  SAVE --> VIZ_OUT["ARC-VIZ 展示"]',
        '  NO_IO --> VIZ_OUT',
        "```",
        "",
        "## 跨组件接口流向图",
        "",
        "```mermaid",
        "flowchart LR",
        '  DATA["ARC-DATA"] -->|IF-DATA-CONTEXT| ANALYSIS["ARC-ANALYSIS"]',
        '  IND["ARC-INDICATORS"] -->|IF-DATA-CONTEXT| ANALYSIS',
        '  DATA -->|IF-DATA-CONTEXT| AGENTS["ARC-AGENTS"]',
        '  ANALYSIS -->|IF-ANALYSIS-AGENTS| AGENTS',
        '  ANALYSIS -->|IF-ANALYSIS-AGENTS| LLM["ARC-LLM"]',
        '  AGENTS -->|IF-AGENTS-REPORT| ANALYSIS',
        '  AGENTS -->|IF-AGENTS-REPORT| CORE["ARC-CORE"]',
        '  ANALYSIS -->|IF-REPORT-ARCHIVE| RUN["ARC-RUN"]',
        '  CORE -->|IF-REPORT-ARCHIVE| RUN',
        '  ANALYSIS -->|IF-REPORT-ARCHIVE| VIZ["ARC-VIZ"]',
        '  CORE -->|IF-REPORT-ARCHIVE| VIZ',
        "```",
        "",
    ]


def _architecture_doc(arch: dict[str, Any], units: list[dict[str, str]]) -> str:
    by_component: dict[str, list[dict[str, str]]] = defaultdict(list)
    interfaces_by_component: dict[str, list[dict[str, str]]] = defaultdict(list)
    interface_kind_names = {
        "command": "命令行接口", "state": "会话状态接口", "data": "数据接口", "function": "函数接口",
        "protocol": "协议接口", "service": "服务接口", "presentation": "展示接口", "document": "文档接口",
    }
    for unit in units:
        by_component[unit["architecture_id"]].append(unit)
    for interface in arch["component_interfaces"]:
        interfaces_by_component[interface["component_id"]].append(interface)
    lines = _front("SWE.2 软件架构设计", "SWE.2", "评审组件职责、接口和运行模式")
    lines += ["## 架构总览", ""]
    lines += _table(
        ["组件", "名称", "软件单元", "职责"],
        [[item["id"], item["name"], len(by_component[item["id"]]), item["dynamic_behavior"]] for item in arch["components"]],
    )
    lines += [""] + _architecture_diagrams()
    lines += ["", "## 运行模式", ""]
    lines += _table(["模式", "行为"], [[item["id"], item["behavior"]] for item in arch["modes"]])
    for item in arch["components"]:
        lines += ["", f"<a id=\"{_anchor(item['id'])}\"></a>", "", f"## {item['id']}", "", f"**名称**：{item['name']}", ""]
        interface_links = "、".join(
            f"[{spec['name']}](#{_anchor(item['id'])}-if-{index:02d})"
            for index, spec in enumerate(interfaces_by_component[item["id"]], 1)
        )
        lines += _table(
            ["属性", "内容"],
            [
                ["源码范围", "、".join(item["source_globs"])],
                ["接口规格", interface_links],
                ["动态行为", item["dynamic_behavior"]],
                ["关联需求", _req_links(item["requirements"])],
                ["详细设计", f"[查看 {len(by_component[item['id']])} 个软件单元](SWE.3-detailed-design/{item['id']}.md)"],
            ],
        )
        for index, spec in enumerate(interfaces_by_component[item["id"]], 1):
            interface_id = f"{item['id']}-IF-{index:02d}"
            lines += ["", f"<a id=\"{_anchor(interface_id)}\"></a>", "", f"### {interface_id}", "", f"**接口名称**：`{spec['name']}`", ""]
            lines += _table(
                ["属性", "说明"],
                [
                    ["接口类型", interface_kind_names.get(spec["kind"], spec["kind"])],
                    ["作用", spec["purpose"]],
                    ["输入参数", spec["parameters"]],
                    ["输出 / 返回", spec["returns"]],
                    ["失败 / 异常行为", spec["failures"]],
                ],
            )
    lines += ["", "## 组件接口", ""]
    for item in arch["interfaces"]:
        lines += ["", f"<a id=\"{_anchor(item['id'])}\"></a>", "", f"## {item['id']}", ""]
        lines += _table(
            ["属性", "说明"],
            [
                ["提供者", "、".join(item["providers"])],
                ["消费者", "、".join(item["consumers"])],
                ["作用", item["purpose"]],
                ["输入参数", item["parameters"]],
                ["输出 / 返回", item["returns"]],
                ["失败 / 异常行为", item["failures"]],
                ["数据与行为契约", item["contract"]],
            ],
        )
    return "\n".join(lines) + "\n"


def _design_outputs(
    arch: dict[str, Any],
    units: list[dict[str, str]],
    functions: list[dict[str, str]],
    verification: dict[str, dict[str, str]],
) -> dict[Path, str]:
    """Render one readable SWE.3 entry plus one bounded document per component."""
    by_component: dict[str, list[dict[str, str]]] = defaultdict(list)
    for unit in units:
        by_component[unit["architecture_id"]].append(unit)
    unit_functions: dict[str, list[dict[str, str]]] = defaultdict(list)
    for function in functions:
        unit_functions[function["software_unit_id"]].append(function)

    index = _front("SWE.3 软件详细设计", "SWE.3", "按架构组件进入模块与逐函数详细设计")
    index += [
        "## 阅读规则",
        "",
        "SWE.3 采用“一个过程入口、一个组件一份文档”。本页只负责导航，避免把全部函数塞入单个巨型文件。",
        "",
        f"当前覆盖 **{len(units)} 个软件单元**、**{len(functions)} 个函数或方法**。函数卡片由受控源码和验证映射生成，不在生成文件中手工修改。",
        "",
        "人工维护的关键单元补充设计见 [关键单元设计](./critical-units.md)，接口与 schema 参考见 [详细设计参考](./reference/design-reference.md)。",
        "",
        "## 组件导航",
        "",
    ]
    component_rows: list[list[object]] = []
    outputs: dict[Path, str] = {}
    for component in arch["components"]:
        component_id = component["id"]
        component_units = sorted(by_component[component_id], key=lambda item: item["source_path"].casefold())
        function_count = sum(len(unit_functions[unit["software_unit_id"]]) for unit in component_units)
        component_rows.append(
            [
                f"[{component_id} — {component['name']}](./{component_id}.md)",
                len(component_units),
                function_count,
                _req_links(component["requirements"], "../"),
            ]
        )

        lines = _front(
            f"{component_id} — {component['name']}",
            "SWE.3",
            "阅读该架构组件的软件单元、函数职责、契约、风险与验证引用",
        )
        lines += [
            f"[返回 SWE.3 组件导航](./software-detailed-design.md) · [返回 SWE.2 架构组件](../SWE.2-architecture/software-architecture.md#{_anchor(component_id)})",
            "",
            "## 组件概览",
            "",
        ]
        lines += _table(
            ["模块", "函数", "高风险", "验证措施", "状态"],
            [
                [
                    f"[{unit['source_path']}](#{_anchor(unit['software_unit_id'])})",
                    verification[unit["software_unit_id"]]["function_count"],
                    verification[unit["software_unit_id"]]["high_risk_function_count"],
                    _measure_links(verification[unit["software_unit_id"]]["verification_measure_ids"], "../"),
                    verification[unit["software_unit_id"]]["verification_status"],
                ]
                for unit in component_units
            ],
        )
        for unit in component_units:
            lines += _unit_section(
                unit,
                sorted(
                    unit_functions[unit["software_unit_id"]],
                    key=lambda item: (int(item["line"]), item["qualified_name"]),
                ),
                verification[unit["software_unit_id"]],
                component["name"],
                root_prefix="../../../",
                aspice_prefix="../",
            )
        outputs[ASPICE / "SWE.3-detailed-design" / f"{component_id}.md"] = "\n".join(lines) + "\n"

    index += _table(["架构组件", "软件单元", "函数", "关联需求"], component_rows)
    index += [
        "",
        "## 共同契约",
        "",
        "- 前置条件：调用方满足函数签名、所属单元状态和关联需求约束。",
        "- 后置条件：正常返回满足返回契约；副作用不得超出函数卡片记录的类别。",
        "- 静态扫描未发现显式异常或副作用，不代表底层依赖绝不会产生间接行为。",
    ]
    outputs[ASPICE / "SWE.3-detailed-design" / "software-detailed-design.md"] = "\n".join(index) + "\n"
    return outputs


def _unit_section(
    unit: dict[str, str],
    functions: list[dict[str, str]],
    verification: dict[str, str],
    component_name: str,
    *,
    root_prefix: str = "../../",
    aspice_prefix: str = "",
) -> list[str]:
    source_link = root_prefix + unit["source_path"]
    lines = [
        "",
        f"<a id=\"{_anchor(unit['software_unit_id'])}\"></a>",
        "",
        f"### {unit['software_unit_id']}",
        "",
        f"**模块**：`{unit['source_path']}`（软件单元详细设计）",
        "",
    ]
    lines += _table(
        ["属性", "内容"],
        [
            ["软件单元 ID", unit["software_unit_id"]],
            ["源码", f"[{unit['source_path']}]({source_link})"],
            ["架构组件", f"{unit['architecture_id']} — {component_name}"],
            ["职责", unit["responsibility"]],
            ["关联需求", _req_links(unit["requirement_ids"], aspice_prefix)],
            ["函数 / 高风险函数", f"{verification['function_count']} / {verification['high_risk_function_count']}"],
            ["验证措施", _measure_links(verification["verification_measure_ids"], aspice_prefix)],
            ["动态测试", _test_links(verification["dynamic_test_references"], root_prefix)],
            ["验证状态", verification["verification_status"]],
        ],
    )
    high_risk_functions = [item for item in functions if item["risk"] == "high"]
    if high_risk_functions:
        lines += ["", "#### 高风险设计评审清单", ""]
        lines += _table(
            ["函数", "职责", "副作用", "验证"],
            [
                [
                    f"[{item['qualified_name']}](#{_anchor(item['function_id'])})",
                    item["responsibility"],
                    item["side_effects"],
                    _test_links(item["test_references"], root_prefix),
                ]
                for item in high_risk_functions
            ],
        )
    lines += ["", "#### 函数导航", ""]
    if functions:
        lines.append(" · ".join(f"[{item['qualified_name']}](#{_anchor(item['function_id'])})" for item in functions))
    else:
        lines.append("本模块没有函数或方法定义。")
    for item in functions:
        risk_name = {"high": "高", "medium": "中", "low": "低"}.get(item["risk"], item["risk"])
        parameter_text = item["parameter_contract"].replace("；`", "<br>`")
        dependency_text = _list(item["call_dependencies"]) if item["call_dependencies"] != "none" else "无直接调用依赖"
        lines += [
            "",
            f"<a id=\"{_anchor(item['function_id'])}\"></a>",
            "",
            f"#### {item['function_id']}",
            "",
        ]
        lines += _table(
            ["设计项", "说明"],
            [
                ["函数", f"`{item['qualified_name']}`"],
                ["源码位置", f"[{item['source_path']}]({root_prefix}{item['source_path']}) · `L{item['line']}`"],
                ["签名", f"`{item['qualified_name']}{item['signature']}`"],
                ["参数", parameter_text],
                ["返回", item["return_contract"]],
                ["职责", item["responsibility"]],
                ["处理逻辑", item["algorithm_summary"]],
                ["前置条件", item["preconditions"]],
                ["后置条件", item["postconditions"]],
                ["显式异常", item["explicit_exceptions"]],
                ["副作用", item["side_effects"]],
                ["并发约束", item["concurrency"]],
                ["调用依赖", dependency_text],
                ["复杂度 / 风险", f"分支 {item['branch_points']}；跨度 {item['line_span']} 行；{risk_name}"],
                ["测试 / 验证", f"{_test_links(item['test_references'], root_prefix)} · {item['verification_disposition']}"],
            ],
        )
    return lines


def _unit_verification_doc(arch: dict[str, Any], rows: list[dict[str, str]]) -> str:
    names = {item["id"]: item["name"] for item in arch["components"]}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["architecture_id"]].append(row)
    blocking = sum(row["verification_status"] == "blocking-gap" for row in rows)
    high = sum(int(row["high_risk_function_count"]) for row in rows)
    lines = _front("SWE.4 单元测试（UT）", "SWE.4", "评审每个软件单元的 UT 选择、风险与结果")
    lines += ['<a id="vm-unit"></a>', "", "## VM-UNIT", ""]
    lines += ["### 结论", "", f"共 **{len(rows)} 个单元**、**{high} 个高风险函数**；阻断单元 **{blocking}** 个。", ""]
    for component_id in names:
        lines += ["", f"## {component_id} — {names[component_id]}", ""]
        lines += _table(
            ["软件单元", "函数", "高风险", "措施", "动态测试", "状态"],
            [
                [
                    f"[{row['source_path']}](SWE.3-detailed-design/{row['architecture_id']}.md#{_anchor(row['software_unit_id'])})",
                    row["function_count"], row["high_risk_function_count"], _measure_links(row["verification_measure_ids"]),
                    _test_links(row["dynamic_test_references"]), row["verification_status"],
                ]
                for row in sorted(grouped[component_id], key=lambda item: item["source_path"].casefold())
            ],
        )
    return "\n".join(lines) + "\n"


def _integration_doc(plan: dict[str, Any], measures: dict[str, Any]) -> str:
    lines = _front("SWE.5 集成测试（IT）", "SWE.5", "评审集成顺序、接口、桩、资源和 IT 结果")
    measure_items: dict[str, list[str]] = defaultdict(list)
    for item in plan["items"]:
        for measure_id in item["verification_measure_ids"]:
            measure_items[measure_id].append(item["id"])
    for measure in measures["measures"]:
        if measure["level"] == "SWE.5":
            measure_items.setdefault(measure["id"], [])
    for measure_id, item_ids in measure_items.items():
        links = "、".join(f"[{item_id}](#{_anchor(item_id)})" for item_id in item_ids)
        association = f"关联集成项：{links}" if links else "关联集成项：独立回测验证措施，不绑定跨组件集成步骤。"
        lines += [f'<a id="{_anchor(measure_id)}"></a>', "", f"## {measure_id}", "", association, ""]
    lines += ["## 准入与退出", "", "### 准入条件", ""]
    lines += [f"- {item}" for item in plan["entry_criteria"]]
    lines += ["", "### 退出条件", ""] + [f"- {item}" for item in plan["exit_criteria"]]
    lines += ["", "## 集成顺序", ""] + [f"{idx}. `{item}`" for idx, item in enumerate(plan["integration_order"], 1)]
    for item in plan["items"]:
        lines += ["", f"<a id=\"{_anchor(item['id'])}\"></a>", "", f"## {item['id']}", ""]
        lines += _table(
            ["属性", "内容"],
            [
                ["提供者 → 消费者", f"{'、'.join(item['providers'])} → {'、'.join(item['consumers'])}"],
                ["接口", "、".join(item["interfaces"])],
                ["需求", _req_links(item["requirement_ids"])],
                ["前置条件", item["prerequisites"]],
                ["桩 / 隔离", item["stubs"]],
                ["超时 / 资源", f"{item['timeout_seconds']} 秒；{item['resource_target']}"],
                ["测试", _test_links(item["tests"])],
                ["验证措施", _measure_links(item["verification_measure_ids"])],
                ["结果", item["result"]],
            ],
        )
    return "\n".join(lines) + "\n"


def _qualification_doc(measures: dict[str, Any], coverage: list[dict[str, str]]) -> str:
    blocking = sum(row["coverage_status"] == "blocking-gap" for row in coverage)
    lines = _front("SWE.6 验证测试（VT）", "SWE.6", "评审验证措施、需求覆盖和发布接受结果")
    policy = measures["selection_policy"]
    lines += ["## 选择策略", ""]
    lines += _table(["规则", "内容"], [[key, value] for key, value in policy.items()])
    lines += ["", "## 验证措施目录", ""]
    lines += _table(
        ["ID", "级别", "技术"],
        [[f"[{item['id']}](#{_anchor(item['id'])})", item["level"], item["technique"]] for item in measures["measures"]],
    )
    for item in measures["measures"]:
        lines += ["", f'<a id="{_anchor(item["id"])}"></a>', "", f"## {item['id']}", ""]
        lines += _table(
            ["属性", "内容"],
            [["级别", item["level"]], ["技术", item["technique"]], ["命令", item["command"]], ["通过准则", item["pass_fail"]], ["环境", item["environment"]]],
        )
    lines += ["", "## 需求覆盖结论", "", f"共 **{len(coverage)} 条需求**；阻断覆盖缺口 **{blocking}** 条。", ""]
    lines += _table(
        ["需求", "架构", "验证措施", "接受结果", "状态"],
        [[_req_links([row["requirement_id"]]), _arch_links(row["architecture_ids"]), _measure_links(row["verification_measure_ids"]), _measure_links(row["accepted_result_ids"]), row["coverage_status"]] for row in coverage],
    )
    lines += ["", "## 最新结果", "", "详见 [软件域验证结果](./records/verification/latest.md)。"]
    return "\n".join(lines) + "\n"


def _configuration_doc(cm: dict[str, Any]) -> str:
    sbom = json.loads((MACHINE / "sbom.json").read_text(encoding="utf-8"))
    components = sbom.get("components", [])
    lines = _front("SUP.8 软件配置管理", "SUP.8", "评审配置项、变更控制、依赖和基线")
    lines += ["## 基线", ""]
    lines += _table(
        ["属性", "内容"],
        [["基线 ID", cm["baseline_id"]], ["状态", cm["status"]], ["发布引用", cm["baseline_ref"]], ["负责人角色", cm["owner_role"]]],
    )
    lines += ["", "## 变更控制", ""]
    lines += _table(["控制项", "规则"], [[key, value] for key, value in cm["change_control"].items()])
    lines += ["", "## 配置项", ""]
    lines += _table(["ID", "路径", "过程"], [[item["id"], item["path"], item["process"]] for item in cm["configuration_items"]])
    lines += ["", "## 依赖基线", "", f"锁定 **{len(components)} 个依赖组件**。机器可校验的哈希、SBOM 和 pip 解析结果保存在 `_machine/`。", ""]
    lines += _table(["包", "版本"], [[item.get("name"), item.get("version")] for item in components])
    return "\n".join(lines) + "\n"


def _traceability_doc(reqs: dict[str, Any], coverage: list[dict[str, str]]) -> str:
    titles = {item["id"]: item["title"] for item in reqs["requirements"]}
    lines = _front("软件双向追溯", "SWE.1–SWE.6", "从需求导航到架构、验证措施和接受结果")
    lines += _table(
        ["需求", "标题", "架构组件", "验证措施", "接受结果", "覆盖"],
        [[_req_links([row["requirement_id"]]), titles[row["requirement_id"]], _arch_links(row["architecture_ids"]), _measure_links(row["verification_measure_ids"]), _measure_links(row["accepted_result_ids"]), row["coverage_status"]] for row in coverage],
    )
    return "\n".join(lines) + "\n"


def expected_outputs() -> dict[Path, str]:
    reqs = _yaml("software-requirements.yaml")
    arch = _yaml("software-architecture.yaml")
    measures = _yaml("verification-measures.yaml")
    integration = _yaml("software-integration-plan.yaml")
    cm = _yaml("configuration-management.yaml")
    units = _csv("software-unit-catalog.csv")
    functions = _csv("software-function-detailed-design.csv")
    unit_rows = _csv("software-unit-verification-matrix.csv")
    coverage = _csv("software-requirement-verification-coverage.csv")
    unit_verification = {row["software_unit_id"]: row for row in unit_rows}
    outputs = _design_outputs(arch, units, functions, unit_verification)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = expected_outputs()
    errors: list[str] = []
    for path, expected in outputs.items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8", newline="")
        elif not path.exists():
            errors.append(f"missing readable document: {path.relative_to(ROOT).as_posix()}")
        elif path.read_text(encoding="utf-8-sig") != expected:
            errors.append(f"stale readable document: {path.relative_to(ROOT).as_posix()}")
    if errors:
        print("ASPICE readable documentation validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"ASPICE readable documentation valid: {len(outputs)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
