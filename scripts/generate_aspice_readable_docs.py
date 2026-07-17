#!/usr/bin/env python3
"""Render the ASPICE software-domain evidence as reviewable Markdown.

Machine-oriented YAML/CSV/JSON stays under ``docs/aspice/_machine`` for
deterministic validation.  This renderer makes Markdown the normal review
surface and splits detailed design into one page per software unit.
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


def _req_links(values: list[str] | str) -> str:
    items = values.split(";") if isinstance(values, str) else values
    return "、".join(f"[{item}](./SWE.1-software-requirements.md#{_anchor(item)})" for item in items if item) or "—"


def _arch_links(values: list[str] | str) -> str:
    items = values.split(";") if isinstance(values, str) else values
    return "、".join(f"[{item}](./SWE.2-software-architecture.md#{_anchor(item)})" for item in items if item) or "—"


def _measure_links(values: list[str] | str) -> str:
    items = values.split(";") if isinstance(values, str) else values
    rendered: list[str] = []
    for item in items:
        if not item:
            continue
        target = "SWE.4-unit-testing.md" if item == "VM-UNIT" else "SWE.5-integration-testing.md" if item.startswith("VM-INTEGRATION") or item == "VM-BACKTEST" else "SWE.6-validation-testing.md"
        rendered.append(f"[{item}](./{target}#{_anchor(item)})")
    return "、".join(rendered) or "—"


def _test_links(value: list[str] | str) -> str:
    items = value.split(";") if isinstance(value, str) else value
    return "、".join(f"[{item}](../../{item})" for item in items if item) or "—"


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
            f"## {item['id']} — {item['title']}",
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


def _architecture_doc(arch: dict[str, Any], units: list[dict[str, str]]) -> str:
    by_component: dict[str, list[dict[str, str]]] = defaultdict(list)
    for unit in units:
        by_component[unit["architecture_id"]].append(unit)
    lines = _front("SWE.2 软件架构设计", "SWE.2", "评审组件职责、接口和运行模式")
    lines += ["## 架构总览", ""]
    lines += _table(
        ["组件", "名称", "软件单元", "职责"],
        [[item["id"], item["name"], len(by_component[item["id"]]), item["dynamic_behavior"]] for item in arch["components"]],
    )
    lines += ["", "## 运行模式", ""]
    lines += _table(["模式", "行为"], [[item["id"], item["behavior"]] for item in arch["modes"]])
    for item in arch["components"]:
        lines += ["", f"<a id=\"{_anchor(item['id'])}\"></a>", "", f"## {item['id']} — {item['name']}", ""]
        lines += _table(
            ["属性", "内容"],
            [
                ["源码范围", "、".join(item["source_globs"])],
                ["静态接口", "、".join(item["static_interfaces"])],
                ["动态行为", item["dynamic_behavior"]],
                ["关联需求", _req_links(item["requirements"])],
                ["详细设计", f"[查看 {len(by_component[item['id']])} 个软件单元](./SWE.3-software-detailed-design.md#{item['id'].lower()})"],
            ],
        )
    lines += ["", "## 组件接口", ""]
    lines += _table(
        ["接口", "提供者", "消费者", "契约"],
        [[item["id"], "、".join(item["providers"]), "、".join(item["consumers"]), item["contract"]] for item in arch["interfaces"]],
    )
    return "\n".join(lines) + "\n"


def _design_doc(
    arch: dict[str, Any],
    units: list[dict[str, str]],
    functions: list[dict[str, str]],
    verification: dict[str, dict[str, str]],
) -> str:
    by_component: dict[str, list[dict[str, str]]] = defaultdict(list)
    for unit in units:
        by_component[unit["architecture_id"]].append(unit)
    unit_functions: dict[str, list[dict[str, str]]] = defaultdict(list)
    for function in functions:
        unit_functions[function["software_unit_id"]].append(function)
    names = {item["id"]: item["name"] for item in arch["components"]}
    lines = _front("SWE.3 软件详细设计", "SWE.3", "在一个文档内按组件、模块和函数阅读完整详细设计")
    lines += [
        "## 阅读方式",
        "",
        "一个 Python 模块对应一个 software unit。本文件按组件、模块、函数三级组织；目录链接使用稳定 ID。",
        "",
        f"当前覆盖 **{len(units)} 个软件单元**。全部函数详细设计均在本文件内，SWE.4 汇总 UT 选择与结果。",
        "",
        "### 全部函数的共同契约",
        "",
        "- 前置条件：调用方满足函数签名、所属单元状态和关联需求约束。",
        "- 后置条件：正常返回满足返回契约；副作用不得超出函数卡片记录的类别。",
        "- 未单列运行约束时，默认值为：显式异常 `none-explicit`、副作用 `none-detected`、并发 `caller-thread`；这不代表底层依赖绝不会抛出异常。",
        "",
    ]
    for component in arch["components"]:
        component_id = component["id"]
        rows = sorted(by_component[component_id], key=lambda item: item["source_path"].casefold())
        lines += ["", f"<a id=\"{_anchor(component_id)}\"></a>", "", f"## {component_id} — {names[component_id]}", ""]
        lines += _table(
            ["模块", "函数", "高风险", "验证措施", "状态"],
            [
                [
                    f"[{unit['source_path']}](#{_anchor(unit['software_unit_id'])})",
                    verification[unit["software_unit_id"]]["function_count"],
                    verification[unit["software_unit_id"]]["high_risk_function_count"],
                    _measure_links(verification[unit["software_unit_id"]]["verification_measure_ids"]),
                    verification[unit["software_unit_id"]]["verification_status"],
                ]
                for unit in rows
            ],
        )
        for unit in rows:
            lines += _unit_section(
                unit,
                sorted(
                    unit_functions[unit["software_unit_id"]],
                    key=lambda item: (int(item["line"]), item["qualified_name"]),
                ),
                verification[unit["software_unit_id"]],
                names[component_id],
            )
    return "\n".join(lines) + "\n"


def _unit_section(
    unit: dict[str, str],
    functions: list[dict[str, str]],
    verification: dict[str, str],
    component_name: str,
) -> list[str]:
    source_link = "../../" + unit["source_path"]
    lines = [
        "",
        f"<a id=\"{_anchor(unit['software_unit_id'])}\"></a>",
        "",
        f"### {unit['source_path']} — 软件单元详细设计",
        "",
    ]
    lines += _table(
        ["属性", "内容"],
        [
            ["软件单元 ID", unit["software_unit_id"]],
            ["源码", f"[{unit['source_path']}]({source_link})"],
            ["架构组件", f"{unit['architecture_id']} — {component_name}"],
            ["职责", unit["responsibility"]],
            ["关联需求", _req_links(unit["requirement_ids"])],
            ["函数 / 高风险函数", f"{verification['function_count']} / {verification['high_risk_function_count']}"],
            ["验证措施", _measure_links(verification["verification_measure_ids"])],
            ["动态测试", _test_links(verification["dynamic_test_references"])],
            ["验证状态", verification["verification_status"]],
        ],
    )
    lines += ["", "#### 函数导航", ""]
    if functions:
        lines.append(" · ".join(f"[{item['qualified_name']}](#{_anchor(item['function_id'])})" for item in functions))
    else:
        lines.append("本模块没有函数或方法定义。")
    for item in functions:
        card = [
            "",
            f"<a id=\"{_anchor(item['function_id'])}\"></a>",
            "",
            f"#### `{item['qualified_name']}`",
            "",
            f"- **ID / 行**：`{item['function_id']}` / `L{item['line']}`（源码见本单元概览）",
            f"- **签名 / 返回**：`{item['qualified_name']}{item['signature']}` → `{item['return_contract']}`",
            f"- **职责**：{item['responsibility']}",
        ]
        if (item["explicit_exceptions"], item["side_effects"], item["concurrency"]) != (
            "none-explicit",
            "none-detected",
            "caller-thread",
        ):
            card.append(f"- **异常 / 副作用 / 并发**：{item['explicit_exceptions']} / {item['side_effects']} / {item['concurrency']}")
        if item["call_dependencies"] != "none":
            card.append(f"- **依赖**：{_list(item['call_dependencies'])}")
        card += [
            f"- **复杂度 / 风险**：分支 {item['branch_points']}；跨度 {item['line_span']} 行；{item['risk']}",
            f"- **测试 / 验证**：{_test_links(item['test_references'])} · {item['verification_disposition']}",
        ]
        lines += card
    return lines


def _unit_verification_doc(arch: dict[str, Any], rows: list[dict[str, str]]) -> str:
    names = {item["id"]: item["name"] for item in arch["components"]}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["architecture_id"]].append(row)
    blocking = sum(row["verification_status"] == "blocking-gap" for row in rows)
    high = sum(int(row["high_risk_function_count"]) for row in rows)
    lines = _front("SWE.4 单元测试（UT）", "SWE.4", "评审每个软件单元的 UT 选择、风险与结果")
    lines += ['<a id="vm-unit"></a>', ""]
    lines += ["## 结论", "", f"共 **{len(rows)} 个单元**、**{high} 个高风险函数**；阻断单元 **{blocking}** 个。", ""]
    for component_id in names:
        lines += ["", f"## {component_id} — {names[component_id]}", ""]
        lines += _table(
            ["软件单元", "函数", "高风险", "措施", "动态测试", "状态"],
            [
                [
                    f"[{row['source_path']}](./SWE.3-software-detailed-design.md#{_anchor(row['software_unit_id'])})",
                    row["function_count"], row["high_risk_function_count"], _measure_links(row["verification_measure_ids"]),
                    _test_links(row["dynamic_test_references"]), row["verification_status"],
                ]
                for row in sorted(grouped[component_id], key=lambda item: item["source_path"].casefold())
            ],
        )
    return "\n".join(lines) + "\n"


def _integration_doc(plan: dict[str, Any]) -> str:
    lines = _front("SWE.5 集成测试（IT）", "SWE.5", "评审集成顺序、接口、桩、资源和 IT 结果")
    lines += ['<a id="vm-integration-pipeline"></a>', '<a id="vm-integration-external"></a>', '<a id="vm-backtest"></a>', ""]
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
    lines += ["", "## 验证措施", ""]
    lines += [f'<a id="{_anchor(item["id"])}"></a>' for item in measures["measures"]]
    lines += [""]
    lines += _table(
        ["ID", "级别", "技术", "命令", "通过准则", "环境"],
        [[item["id"], item["level"], item["technique"], item["command"], item["pass_fail"], item["environment"]] for item in measures["measures"]],
    )
    lines += ["", "## 需求覆盖结论", "", f"共 **{len(coverage)} 条需求**；阻断覆盖缺口 **{blocking}** 条。", ""]
    lines += _table(
        ["需求", "架构", "验证措施", "接受结果", "状态"],
        [[_req_links([row["requirement_id"]]), _arch_links(row["architecture_ids"]), _measure_links(row["verification_measure_ids"]), _measure_links(row["accepted_result_ids"]), row["coverage_status"]] for row in coverage],
    )
    lines += ["", "## 最新结果", "", "详见 [软件域验证结果](./verification-results/latest.md)。"]
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
    outputs: dict[Path, str] = {
        ASPICE / "SWE.1-software-requirements.md": _requirements_doc(reqs),
        ASPICE / "SWE.2-software-architecture.md": _architecture_doc(arch, units),
        ASPICE / "SWE.3-software-detailed-design.md": _design_doc(arch, units, functions, unit_verification),
        ASPICE / "SWE.4-unit-testing.md": _unit_verification_doc(arch, unit_rows),
        ASPICE / "SWE.5-integration-testing.md": _integration_doc(integration),
        ASPICE / "SWE.6-validation-testing.md": _qualification_doc(measures, coverage),
        ASPICE / "SUP.8-configuration-management.md": _configuration_doc(cm),
        ASPICE / "traceability.md": _traceability_doc(reqs, coverage),
    }
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
