"""Regression checks for ASPICE document, traceability, and baseline assets."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.regression
def test_aspice_assets_are_complete_and_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_aspice_assets.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    evidence = subprocess.run(
        [sys.executable, "scripts/generate_aspice_software_evidence.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        check=False,
    )
    assert evidence.returncode == 0, evidence.stdout + evidence.stderr

    readable = subprocess.run(
        [sys.executable, "scripts/generate_aspice_readable_docs.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        check=False,
    )
    assert readable.returncode == 0, readable.stdout + readable.stderr


@pytest.mark.regression
def test_every_function_and_document_has_an_aspice_mapping() -> None:
    with (ROOT / "docs/aspice/_machine/software-function-map.csv").open(encoding="utf-8-sig", newline="") as handle:
        functions = list(csv.DictReader(handle))
    with (ROOT / "docs/aspice/_machine/document-register.csv").open(encoding="utf-8-sig", newline="") as handle:
        documents = list(csv.DictReader(handle))

    assert functions
    assert documents
    assert all(row["software_unit_id"] and row["architecture_id"] and row["requirement_ids"] for row in functions)
    assert all(row["primary_process"] and row["information_item"] and row["lifecycle_status"] for row in documents)
    assert not any(row["information_item"] == "Registered Supporting Document" for row in documents)
    assert {row["path"] for row in documents} >= {
        "README.md",
        "AGENTS.md",
        "docs/README.md",
        "docs/aspice/_machine/software-requirements.yaml",
        "docs/aspice/_machine/software-architecture.yaml",
    }


@pytest.mark.regression
def test_software_domain_design_and_verification_are_closed() -> None:
    with (ROOT / "docs/aspice/_machine/software-function-map.csv").open(encoding="utf-8-sig", newline="") as handle:
        function_map = list(csv.DictReader(handle))
    with (ROOT / "docs/aspice/_machine/software-function-detailed-design.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        designs = list(csv.DictReader(handle))
    with (ROOT / "docs/aspice/_machine/software-unit-catalog.csv").open(encoding="utf-8-sig", newline="") as handle:
        units = list(csv.DictReader(handle))
    with (ROOT / "docs/aspice/_machine/software-unit-verification-matrix.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        verification = list(csv.DictReader(handle))
    with (ROOT / "docs/aspice/_machine/software-requirement-verification-coverage.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        requirement_coverage = list(csv.DictReader(handle))
    requirements = yaml.safe_load((ROOT / "docs/aspice/_machine/software-requirements.yaml").read_text(encoding="utf-8-sig"))

    assert {row["function_id"] for row in designs} == {row["function_id"] for row in function_map}
    assert {row["software_unit_id"] for row in verification} == {row["software_unit_id"] for row in units}
    required_design = {
        "signature",
        "parameter_contract",
        "return_contract",
        "responsibility",
        "algorithm_summary",
        "preconditions",
        "postconditions",
        "explicit_exceptions",
        "side_effects",
        "concurrency",
        "risk",
        "architecture_id",
        "requirement_ids",
        "verification_disposition",
    }
    assert all(all(row[field] for field in required_design) for row in designs)
    assert not any("As-built responsibility" in row["responsibility"] for row in designs)
    assert not any("相关业务对象或状态" in row["responsibility"] for row in designs)
    assert all(any("\u4e00" <= char <= "\u9fff" for char in row["responsibility"]) for row in designs)
    assert all(row["verification_measure_ids"] for row in verification)
    assert not [row for row in verification if row["verification_status"] == "blocking-gap"]
    assert {row["requirement_id"] for row in requirement_coverage} == {
        row["id"] for row in requirements["requirements"]
    }
    assert all(row["coverage_status"] == "closed" and row["accepted_result_ids"] for row in requirement_coverage)


@pytest.mark.regression
def test_swe5_plan_covers_every_architecture_interface() -> None:
    architecture = yaml.safe_load((ROOT / "docs/aspice/_machine/software-architecture.yaml").read_text(encoding="utf-8-sig"))
    plan = yaml.safe_load((ROOT / "docs/aspice/_machine/software-integration-plan.yaml").read_text(encoding="utf-8-sig"))
    planned_interfaces = {value for item in plan["items"] for value in item["interfaces"]}
    architecture_interfaces = {item["id"] for item in architecture["interfaces"]}

    assert architecture_interfaces <= planned_interfaces
    assert plan["integration_order"] == [item["id"] for item in plan["items"]]
    assert all(item["tests"] and item["verification_measure_ids"] and item["result"] for item in plan["items"])


@pytest.mark.regression
def test_architecture_interfaces_are_reviewable() -> None:
    architecture = yaml.safe_load((ROOT / "docs/aspice/_machine/software-architecture.yaml").read_text(encoding="utf-8-sig"))
    specifications = architecture["component_interfaces"]
    spec_names = {(item["component_id"], item["name"]) for item in specifications}
    declared_names = {
        (component["id"], name)
        for component in architecture["components"]
        for name in component["static_interfaces"]
    }
    assert spec_names == declared_names
    required = {"kind", "purpose", "parameters", "returns", "failures"}
    assert all(all(item.get(field) for field in required) for item in specifications)
    assert all(all(item.get(field) for field in required - {"kind"}) for item in architecture["interfaces"])
    readable = (ROOT / "docs/aspice/SWE.2-software-architecture.md").read_text(encoding="utf-8-sig")
    assert all(f"### {component['id']}-IF-01" in readable for component in architecture["components"])
    assert "| 输入参数 |" in readable and "| 失败 / 异常行为 |" in readable
    assert readable.count("```mermaid") == 5
    assert "## 模块分层图" in readable
    assert "## 核心依赖主干图" in readable
    assert "## 主流水线时序图" in readable
    assert "## 运行模式与回放边界图" in readable
    assert "## 跨组件接口流向图" in readable
    assert all(component["id"] in readable for component in architecture["components"])
    assert all(interface["id"] in readable for interface in architecture["interfaces"])


@pytest.mark.regression
def test_readable_aspice_navigation_covers_requirement_to_vt_chain() -> None:
    names = [
        "SWE.1-software-requirements.md",
        "SWE.2-software-architecture.md",
        "SWE.3-software-detailed-design.md",
        "SWE.4-unit-testing.md",
        "SWE.5-integration-testing.md",
        "SWE.6-validation-testing.md",
        "traceability.md",
    ]
    documents = {name: (ROOT / "docs/aspice" / name).read_text(encoding="utf-8-sig") for name in names}
    requirements = yaml.safe_load((ROOT / "docs/aspice/_machine/software-requirements.yaml").read_text(encoding="utf-8-sig"))
    architecture = yaml.safe_load((ROOT / "docs/aspice/_machine/software-architecture.yaml").read_text(encoding="utf-8-sig"))
    with (ROOT / "docs/aspice/_machine/software-function-detailed-design.csv").open(encoding="utf-8-sig", newline="") as handle:
        functions = list(csv.DictReader(handle))

    assert all(f'id="{row["id"].lower().replace(".", "-")}"' in documents[names[0]] for row in requirements["requirements"])
    assert all(f'id="{row["id"].lower()}"' in documents[names[1]] for row in architecture["components"])
    assert all(f'id="{row["function_id"].lower()}"' in documents[names[2]] for row in functions)
    assert all(f'## {row["id"]}\n' in documents[names[0]] for row in requirements["requirements"])
    assert all(f'## {row["id"]}\n' in documents[names[1]] for row in architecture["components"])
    assert all(f'#### {row["function_id"]}\n' in documents[names[2]] for row in functions)
    assert documents[names[2]].count("| 函数 | `") == len(functions)
    assert "| 设计项 | 说明 |" in documents[names[2]]
    assert "| 参数 |" in documents[names[2]] and "| 处理逻辑 |" in documents[names[2]]
    assert "[SWR-CORE-001](#swr-core-001)" in documents[names[0]]
    assert "SWE.2-software-architecture.md" in documents[names[0]]
    assert "SWE.3-software-detailed-design.md" in documents[names[1]]
    assert "SWE.3-software-detailed-design.md" in documents[names[3]]
    assert "SWE.1-software-requirements.md" in documents[names[4]]
    assert "SWE.1-software-requirements.md" in documents[names[5]]
    assert all("](./SWE." not in text for text in documents.values())
    assert "[SWR-NFR-004](SWE.1-software-requirements.md#swr-nfr-004)" in documents[names[5]]
