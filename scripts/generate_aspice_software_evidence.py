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
ARCH_PATH = ASPICE / "software-architecture.yaml"
REQ_PATH = ASPICE / "software-requirements.yaml"
RESULT_PATH = ASPICE / "verification-results" / "software-domain-2026-07-18.yaml"
FUNCTION_PATH = ASPICE / "software-function-detailed-design.csv"
UNIT_VERIFICATION_PATH = ASPICE / "software-unit-verification-matrix.csv"
REQUIREMENT_COVERAGE_PATH = ASPICE / "software-requirement-verification-coverage.csv"
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
        path
        for path in ROOT.rglob("*.py")
        if not any(part in SOURCE_EXCLUDES for part in path.relative_to(ROOT).parts)
    )


def _test_corpus() -> dict[str, str]:
    return {
        _rel(path): path.read_text(encoding="utf-8-sig", errors="replace")
        for path in sorted((ROOT / "tests").rglob("test_*.py"))
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


def _node_contract(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, str | int]:
    signature = f"({ast.unparse(node.args)})"
    return_contract = ast.unparse(node.returns) if node.returns is not None else "runtime/inferred"
    doc = ast.get_docstring(node, clean=True) or ""
    summary = doc.splitlines()[0] if doc else f"As-built responsibility derived from `{node.name}` and its owning unit."
    calls = sorted({_call_name(item) for item in ast.walk(node) if isinstance(item, ast.Call)})
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
    if re.search(r"(?:write_text|write_bytes|\.open|unlink|mkdir|replace|rename|to_csv|to_json|json\.dump;)", call_text):
        effects.append("filesystem")
    if re.search(r"(?:requests?\.|httpx\.|urllib|urlopen|websocket|fetch_|download|client\.(?:get|post|request|call)|session\.(?:get|post))", call_text):
        effects.append("external-io")
    if re.search(r"(?:session_state|setenv|environ|cache|progress|emit|publish)", call_text):
        effects.append("shared-state")
    if any(isinstance(item, (ast.Global, ast.Nonlocal)) for item in ast.walk(node)):
        effects.append("global-state")
    if isinstance(node, ast.AsyncFunctionDef):
        effects.append("async")
    span = max(1, getattr(node, "end_lineno", node.lineno) - node.lineno + 1)
    return {
        "signature": signature,
        "return_contract": return_contract,
        "responsibility": summary,
        "explicit_exceptions": ";".join(raises) or "none-explicit",
        "side_effects": ";".join(sorted(set(effects))) or "none-detected",
        "call_dependencies": ";".join(calls[:20]) or "none",
        "branch_points": branches,
        "line_span": span,
        "concurrency": "async-await" if isinstance(node, ast.AsyncFunctionDef) else "caller-thread",
    }


def _risk(path: str, name: str, contract: dict[str, str | int]) -> str:
    high_name = re.search(r"(?:authoriz|execute|trade|order|simulate|pipeline|invariant|eligib|archive)", name, re.I)
    high_effect = "external-io" in str(contract["side_effects"])
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
            contract = _node_contract(node)
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
                "return_contract": contract["return_contract"],
                "responsibility": contract["responsibility"],
                "preconditions": "caller satisfies signature, owning-unit state, and linked requirement constraints",
                "postconditions": "normal return follows return contract; detected side effects are limited to recorded categories",
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
                "verification_disposition": verification,
                "design_status": "baselined-as-built",
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
        component_dynamic = component in {
            "ARC-APP",
            "ARC-CORE",
            "ARC-ANALYSIS",
            "ARC-AGENTS",
            "ARC-LLM",
            "ARC-RUN",
            "ARC-BACKTEST",
            "ARC-VIZ",
        }
        blocking = high_count > 0 and not has_dynamic and not component_dynamic and not path.startswith("scripts/")
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
                    else "static plus controlled component/integration evidence"
                    if component_dynamic
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
