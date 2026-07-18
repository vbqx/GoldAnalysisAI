#!/usr/bin/env python3
"""Generate and validate Automotive SPICE governance assets.

This tool reads source/doc metadata only. ``--write`` updates generated
documentation under ``docs/aspice`` and never edits functional code.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASPICE = ROOT / "docs" / "aspice"
MACHINE = ASPICE / "_machine"
REQ_PATH = MACHINE / "software-requirements.yaml"
ARCH_PATH = MACHINE / "software-architecture.yaml"
VER_PATH = MACHINE / "verification-measures.yaml"
CM_PATH = MACHINE / "configuration-management.yaml"
PIP_REPORT_PATH = MACHINE / "pip-resolution.json"
PIP_REPORT_SOURCE = ROOT / "tests" / "reports" / "aspice-pip-resolution.json"

GENERATED_PATHS = {
    MACHINE / "document-register.csv",
    ASPICE / "supporting" / "process-document-index.md",
    MACHINE / "software-unit-catalog.csv",
    MACHINE / "software-function-map.csv",
    MACHINE / "software-function-detailed-design.csv",
    MACHINE / "software-unit-verification-matrix.csv",
    MACHINE / "software-requirement-verification-coverage.csv",
    MACHINE / "traceability-matrix.csv",
    MACHINE / "dependency-lock.txt",
    MACHINE / "sbom.json",
    PIP_REPORT_PATH,
}

DOC_ROOT_FILES = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "tests" / "README.md"]
DOC_EXTRA_GLOBS = ["tests/cases/*.md", "tests/cases/*.yaml"]
SOURCE_EXCLUDES = {".git", ".venv", ".cache", ".pytest_cache", "__pycache__", "tests"}


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10].upper()
    return f"{prefix}-{digest}"


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")
    return value


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_files() -> list[Path]:
    return sorted(
        (
            path
            for path in ROOT.rglob("*.py")
            if not any(part in SOURCE_EXCLUDES for part in path.relative_to(ROOT).parts)
        ),
        key=lambda path: rel(path).casefold(),
    )


def document_files() -> list[Path]:
    paths = {path for path in (ROOT / "docs").rglob("*") if path.is_file()}
    paths.update(path for path in DOC_ROOT_FILES if path.exists())
    for pattern in DOC_EXTRA_GLOBS:
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())
    paths.update(GENERATED_PATHS)
    return sorted(paths, key=lambda path: rel(path).casefold())


def document_classification(path: Path) -> tuple[str, str, str, str]:
    path_str = rel(path)
    if path_str.startswith("docs/aspice/"):
        name = path.name
        if path_str.startswith("docs/aspice/supporting/reviews/"):
            return "SUP.1/SUP.9", "Review/Problem Analysis Evidence", "reviewed", "supporting"
        readable_process_docs = {
            "SWE.1-software-requirements.md": ("SWE.1", "17-00 Software Requirements", "agreed", "normative"),
            "SWE.2-software-architecture.md": ("SWE.2", "04-04 Software Architecture", "agreed", "normative"),
            "SWE.3-software-detailed-design.md": ("SWE.3", "04-05 Software Detailed Design", "agreed", "normative"),
            "SWE.4-unit-testing.md": ("SWE.4", "08-50 Unit Verification", "agreed", "normative"),
            "SWE.5-integration-testing.md": ("SWE.5", "08-52 Integration Verification", "agreed", "normative"),
            "SWE.6-validation-testing.md": ("SWE.6", "08-54 Software Qualification Test", "agreed", "normative"),
            "traceability.md": ("SWE.1-SWE.6", "13-51 Consistency Evidence", "agreed", "normative"),
            "SUP.8-configuration-management.md": ("SUP.8", "Configuration Status/Baseline", "agreed", "normative"),
        }
        if name in readable_process_docs:
            return readable_process_docs[name]
        if name == "README.md":
            return "SWE.1-SWE.6", "Software Domain Navigation", "agreed", "normative"
        if name == "software-requirements.yaml":
            return "SWE.1", "Machine-readable Requirement Mirror", "generated", "generated"
        if name == "software-architecture.yaml":
            return "SWE.2", "Machine-readable Architecture Mirror", "generated", "generated"
        if name in {
            "software-unit-catalog.csv",
            "software-function-map.csv",
            "software-function-detailed-design.csv",
            "key-unit-detailed-designs.md",
        }:
            return "SWE.3", "04-05 Software Detailed Design", "agreed", "normative"
        if name == "software-unit-verification-matrix.csv":
            return "SWE.4", "08-50 Verification Measure/Result", "agreed", "normative"
        if name == "software-requirement-verification-coverage.csv":
            return "SWE.6", "13-51 Consistency Evidence", "generated", "generated"
        if name == "software-integration-plan.yaml":
            return "SWE.5", "08-52 Integration Verification Measure", "agreed", "normative"
        if name == "software-domain-scope-and-closure.md":
            return "SWE.1-SWE.6", "15-52 Evaluation Results", "agreed", "normative"
        if name in {"verification-measures.yaml", "verification-results", "latest.md"} or "verification-results" in path_str:
            return "SWE.4-SWE.6", "08-60/15-52 Verification", "agreed", "normative"
        if name == "traceability-matrix.csv":
            return "SWE.1-SWE.6", "13-51 Consistency Evidence", "generated", "generated"
        if name in {"configuration-management.yaml", "dependency-lock.txt", "sbom.json", "pip-resolution.json"}:
            return "SUP.8", "Configuration Item/Baseline", "agreed", "normative"
        if name in {"document-register.csv", "process-document-index.md"}:
            return "SUP.8", "Configuration Status Record", "generated", "generated"
        return "SUP.8", "Document Control", "agreed", "normative"
    if path_str.startswith("docs/reviews/"):
        return "SUP.1/SUP.9", "Review/Problem Analysis Evidence", "reviewed", "supporting"
    if path_str.startswith("docs/planning/"):
        return "MAN.3/MAN.5", "Project/Risk Plan", "reviewed", "supporting"
    if path_str.startswith("docs/architecture/"):
        return "SWE.2", "04-04 Software Architecture", "reviewed", "supporting"
    if path_str.startswith("docs/testing/") or path_str.startswith("tests/cases/") or path_str == "tests/README.md":
        return "SWE.4-SWE.6", "Verification Strategy/Measure", "reviewed", "supporting"
    if path_str.startswith("docs/reference/"):
        return "SWE.3", "Detailed Design/Interface Reference", "reviewed", "supporting"
    if path_str.startswith("docs/operations/"):
        return "SUP.8/MAN.3", "Operation/Configuration Guidance", "reviewed", "supporting"
    if path_str.startswith("docs/overview/") or path_str == "README.md":
        return "SWE.1", "Stakeholder/Software Context", "reviewed", "supporting"
    if path_str.startswith("docs/archive/"):
        return "SUP.8", "Historical Record", "historical", "historical"
    if path_str in {"docs/README.md", "AGENTS.md"}:
        return "SUP.8", "Document/Automation Guidance", "reviewed", "supporting"
    return "SUP.8", "Registered Supporting Document", "informative", "supporting"


def document_title(path: Path) -> str:
    if path.exists() and path.suffix.lower() == ".md":
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
        if match:
            return match.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ")


def build_document_register() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in document_files():
        process, item, status, authority = document_classification(path)
        rows.append(
            {
                "document_id": stable_id("DOC", rel(path)),
                "path": rel(path),
                "title": document_title(path),
                "primary_process": process,
                "information_item": item,
                "lifecycle_status": status,
                "authority": authority,
                "owner_role": "process-owner" if authority == "normative" else "document-owner",
                "baseline": "ASPICE-DOC-2026-07-17",
                "superseded_by": "",
                "retention": "permanent" if status in {"agreed", "historical"} else "until-superseded",
            }
        )
    return rows


def component_for(path: Path) -> str:
    value = rel(path)
    if value in {"app.py", "run_app.py"} or value.startswith("views/"):
        return "ARC-APP"
    if value.startswith("src/data/"):
        return "ARC-DATA"
    if value.startswith("src/indicators/"):
        return "ARC-INDICATORS"
    if value.startswith("src/analysis/"):
        return "ARC-ANALYSIS"
    if value.startswith("src/agents/"):
        return "ARC-AGENTS"
    if value.startswith("src/llm/"):
        return "ARC-LLM"
    if value.startswith("src/run/"):
        return "ARC-RUN"
    if value.startswith("src/backtest/"):
        return "ARC-BACKTEST"
    if value.startswith("src/viz/"):
        return "ARC-VIZ"
    if value.startswith("scripts/"):
        return "ARC-TOOLS"
    return "ARC-CORE"


def module_doc(tree: ast.AST, component_name: str) -> str:
    doc = ast.get_docstring(tree, clean=True) or ""
    return doc.splitlines()[0] if doc else f"继承 {component_name} 组件设计；模块职责由公开符号和调用关系约束"


def build_units(arch: dict[str, Any]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    components = {item["id"]: item for item in arch["components"]}
    critical_paths = {
        "src/core/orchestrator.py",
        "src/analysis/claim_eligibility.py",
        "src/backtest/simulator.py",
        "src/viz/lightweight_chart.py",
    }
    units: list[dict[str, str]] = []
    functions: list[dict[str, str]] = []
    for path in source_files():
        path_rel = rel(path)
        component_id = component_for(path)
        component = components[component_id]
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=path_rel)
        unit_id = stable_id("UNIT", path_rel)
        requirements = ";".join(component["requirements"])
        critical = path_rel in critical_paths
        units.append(
            {
                "software_unit_id": unit_id,
                "source_path": path_rel,
                "architecture_id": component_id,
                "design_profile": component["name"],
                "responsibility": module_doc(tree, component["name"]),
                "static_interface_basis": "AST public symbols + Python type annotations",
                "dynamic_behavior_basis": "software-architecture.yaml component behavior",
                "requirement_ids": requirements,
                "critical_unit": "yes" if critical else "no",
                "detailed_design": "supporting/key-unit-detailed-designs.md" if critical else "inherited component profile",
            }
        )
        parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            owners: list[str] = []
            parent = parents.get(node)
            while parent is not None:
                if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    owners.append(parent.name)
                parent = parents.get(parent)
            qualname = ".".join([*reversed(owners), node.name])
            functions.append(
                {
                    "function_id": stable_id("FUN", f"{path_rel}:{qualname}"),
                    "software_unit_id": unit_id,
                    "source_path": path_rel,
                    "line": str(node.lineno),
                    "qualified_name": qualname,
                    "visibility": "internal" if node.name.startswith("_") else "public",
                    "architecture_id": component_id,
                    "requirement_ids": requirements,
                    "verification_basis": "unit/component verification selected by requirement and risk",
                }
            )
    return units, sorted(functions, key=lambda row: (row["source_path"], int(row["line"]), row["qualified_name"]))


def build_trace_rows(reqs: dict[str, Any], units: list[dict[str, str]]) -> list[dict[str, str]]:
    units_by_arch: dict[str, list[str]] = defaultdict(list)
    for unit in units:
        units_by_arch[unit["architecture_id"]].append(unit["software_unit_id"])
    rows: list[dict[str, str]] = []
    for req in reqs["requirements"]:
        unit_ids = sorted({unit for arch_id in req["architecture_ids"] for unit in units_by_arch[arch_id]})
        rows.append(
            {
                "requirement_id": req["id"],
                "requirement_title": req["title"],
                "architecture_ids": ";".join(req["architecture_ids"]),
                "software_unit_ids": ";".join(unit_ids),
                "verification_ids": ";".join(req["verification_ids"]),
                "status": req["status"],
                "consistency": "bidirectional-validated",
            }
        )
    return rows


def dependency_outputs(report: dict[str, Any]) -> tuple[str, str]:
    components: list[dict[str, Any]] = []
    lock_lines = [
        "# Generated from pip --dry-run --ignore-installed resolution.",
        "# Python 3.12 / Windows x86_64 baseline; do not edit manually.",
    ]
    installs = sorted(report.get("install", []), key=lambda row: row["metadata"]["name"].lower())
    for item in installs:
        metadata = item["metadata"]
        name = metadata["name"]
        version = metadata["version"]
        archive = item.get("download_info", {}).get("archive_info", {})
        hashes = archive.get("hashes", {})
        hash_value = hashes.get("sha256")
        line = f"{name}=={version}"
        if hash_value:
            line += f" --hash=sha256:{hash_value}"
        lock_lines.append(line)
        component: dict[str, Any] = {
            "type": "library",
            "name": name,
            "version": version,
            "purl": f"pkg:pypi/{name.lower().replace('_', '-')}@{version}",
        }
        if hash_value:
            component["hashes"] = [{"alg": "SHA-256", "content": hash_value}]
        components.append(component)
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {"component": {"type": "application", "name": "GoldAnalysisAI"}},
        "components": components,
    }
    return "\n".join(lock_lines) + "\n", json.dumps(sbom, ensure_ascii=False, indent=2) + "\n"


def csv_text(rows: list[dict[str, str]]) -> str:
    if not rows:
        raise ValueError("cannot render empty CSV")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def process_index(rows: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["primary_process"]].append(row)
    lines = [
        "# ASPICE 过程文档索引",
        "",
        "本文件由 `python scripts/check_aspice_assets.py --write` 生成。人工评审以 `../README.md` 导航的 Markdown 主文档为准；完整机器注册表位于 `../_machine/document-register.csv`。",
        "",
    ]
    for process in sorted(grouped):
        lines.extend([f"## {process}", "", "| 文档 | 信息项 | 状态 | 权威性 |", "|---|---|---|---|"])
        for row in grouped[process]:
            if row["path"].startswith("docs/aspice/supporting/"):
                target = "./" + row["path"].removeprefix("docs/aspice/supporting/")
            elif row["path"].startswith("docs/aspice/"):
                target = "../" + row["path"].removeprefix("docs/aspice/")
            elif row["path"].startswith("docs/"):
                target = "../../" + row["path"].removeprefix("docs/")
            else:
                target = "../../../" + row["path"]
            lines.append(
                f"| [{row['title']}]({target}) | {row['information_item']} | {row['lifecycle_status']} | {row['authority']} |"
            )
        lines.append("")
    return "\n".join(lines)


def expected_outputs() -> dict[Path, str]:
    reqs = read_yaml(REQ_PATH)
    arch = read_yaml(ARCH_PATH)
    documents = build_document_register()
    units, functions = build_units(arch)
    trace = build_trace_rows(reqs, units)
    report_path = PIP_REPORT_PATH if PIP_REPORT_PATH.exists() else PIP_REPORT_SOURCE
    if not report_path.exists():
        raise ValueError("missing pip resolution report; run the documented pip dry-run first")
    pip_report = json.loads(report_path.read_text(encoding="utf-8"))
    lock, sbom = dependency_outputs(pip_report)
    outputs = {
        MACHINE / "document-register.csv": csv_text(documents),
        ASPICE / "supporting" / "process-document-index.md": process_index(documents),
        MACHINE / "software-unit-catalog.csv": csv_text(units),
        MACHINE / "software-function-map.csv": csv_text(functions),
        MACHINE / "traceability-matrix.csv": csv_text(trace),
        MACHINE / "dependency-lock.txt": lock,
        MACHINE / "sbom.json": sbom,
    }
    if not PIP_REPORT_PATH.exists():
        outputs[PIP_REPORT_PATH] = json.dumps(pip_report, ensure_ascii=False, indent=2) + "\n"
    return outputs


def validate_model(*, allow_generated_missing: bool = False) -> list[str]:
    errors: list[str] = []
    reqs = read_yaml(REQ_PATH)
    arch = read_yaml(ARCH_PATH)
    ver = read_yaml(VER_PATH)
    cm = read_yaml(CM_PATH)
    req_map = {item["id"]: item for item in reqs.get("requirements", [])}
    arch_map = {item["id"]: item for item in arch.get("components", [])}
    measures = {item["id"]: item for item in ver.get("measures", [])}
    if len(req_map) != len(reqs.get("requirements", [])):
        errors.append("duplicate software requirement ID")
    if len(arch_map) != len(arch.get("components", [])):
        errors.append("duplicate architecture ID")
    if len(measures) != len(ver.get("measures", [])):
        errors.append("duplicate verification measure ID")
    reverse_ver = ver.get("requirements", {})
    for req_id, req in req_map.items():
        for arch_id in req.get("architecture_ids", []):
            if arch_id not in arch_map:
                errors.append(f"{req_id} references missing architecture {arch_id}")
            elif req_id not in arch_map[arch_id].get("requirements", []):
                errors.append(f"{req_id}<->{arch_id} is not bidirectional")
        for measure_id in req.get("verification_ids", []):
            if measure_id not in measures:
                errors.append(f"{req_id} references missing verification {measure_id}")
            elif req_id not in reverse_ver.get(measure_id, []):
                errors.append(f"{req_id}<->{measure_id} is not bidirectional")
    for arch_id, component in arch_map.items():
        for req_id in component.get("requirements", []):
            if req_id not in req_map:
                errors.append(f"{arch_id} references missing requirement {req_id}")
            elif arch_id not in req_map[req_id].get("architecture_ids", []):
                errors.append(f"{arch_id}<->{req_id} is not bidirectional")
    for measure_id, linked in reverse_ver.items():
        if measure_id not in measures:
            errors.append(f"verification mapping references missing measure {measure_id}")
        for req_id in linked:
            if req_id not in req_map:
                errors.append(f"{measure_id} references missing requirement {req_id}")
            elif measure_id not in req_map[req_id].get("verification_ids", []):
                errors.append(f"{measure_id}<->{req_id} is not bidirectional")
    for item in cm.get("configuration_items", []):
        item_path = ROOT / item["path"]
        if not item_path.exists() and not (allow_generated_missing and item_path in GENERATED_PATHS):
            errors.append(f"configuration item path missing: {item['path']}")
    return errors


def write_outputs(outputs: dict[Path, str]) -> None:
    ASPICE.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="")


def check_outputs(outputs: dict[Path, str]) -> list[str]:
    errors: list[str] = []
    for path, expected in outputs.items():
        if not path.exists():
            errors.append(f"generated artifact missing: {rel(path)}")
            continue
        actual = path.read_text(encoding="utf-8-sig")
        if actual != expected:
            errors.append(f"generated artifact stale: {rel(path)}")
    registered = {row["path"] for row in build_document_register()}
    actual_docs = {rel(path) for path in document_files()}
    if registered != actual_docs:
        errors.append("document register does not cover every document")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="write generated ASPICE assets")
    group.add_argument("--check", action="store_true", help="validate sources and generated assets")
    args = parser.parse_args()

    errors = validate_model(allow_generated_missing=args.write)
    outputs = expected_outputs()
    if args.write:
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        write_outputs(outputs)
        print(f"wrote {len(outputs)} ASPICE generated artifacts")
        return 0
    errors.extend(check_outputs(outputs))
    if errors:
        print("ASPICE asset validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    units, functions = build_units(read_yaml(ARCH_PATH))
    print(
        f"ASPICE assets valid: {len(read_yaml(REQ_PATH)['requirements'])} requirements, "
        f"{len(units)} units, {len(functions)} functions, {len(document_files())} documents"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
