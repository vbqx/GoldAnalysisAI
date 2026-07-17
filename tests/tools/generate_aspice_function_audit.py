#!/usr/bin/env python3
"""Generate the function-level evidence inventory used by the ASPICE audit."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "docs" / "reviews" / "aspice"
CSV_PATH = OUT_DIR / "software-function-audit-2026-07-17.csv"
SUMMARY_PATH = OUT_DIR / "software-function-audit-summary-2026-07-17.json"
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    ".cache",
    ".pytest_cache",
    "__pycache__",
    "tests",
}


def _source_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.py")
        if not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    )


def _text_index(base: Path, pattern: str) -> dict[Path, str]:
    return {
        path: path.read_text(encoding="utf-8-sig", errors="replace")
        for path in base.rglob(pattern)
        if path.is_file()
    }


def _references(name: str, corpus: dict[Path, str], *, limit: int = 4) -> list[str]:
    token = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])")
    refs = [str(path.relative_to(ROOT)).replace("\\", "/") for path, text in corpus.items() if token.search(text)]
    return refs[:limit]


def _function_rows() -> list[dict[str, object]]:
    docs = _text_index(ROOT / "docs", "*.md")
    tests = _text_index(ROOT / "tests", "test_*.py")
    rows: list[dict[str, object]] = []

    for path in _source_files():
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=rel)
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
            args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
            typed_args = sum(arg.annotation is not None for arg in args)
            fully_typed = typed_args == len(args) and node.args.vararg is None and node.args.kwarg is None
            if node.args.vararg is not None:
                fully_typed = fully_typed and node.args.vararg.annotation is not None
            if node.args.kwarg is not None:
                fully_typed = fully_typed and node.args.kwarg.annotation is not None

            docstring = ast.get_docstring(node, clean=True) or ""
            doc_refs = _references(node.name, docs)
            test_refs = _references(node.name, tests)
            public = not node.name.startswith("_")
            interface_state = "完整注解" if fully_typed and node.returns is not None else "部分注解"
            design_state = "有函数说明" if docstring else "缺函数级详细设计"
            trace_state = "存在符号级文档引用" if doc_refs else "无需求/架构追溯记录"
            verify_state = "存在同名测试引用" if test_refs else "无同名测试追溯证据"
            if docstring and doc_refs and test_refs and interface_state == "完整注解":
                verdict = "P-部分满足"
            elif docstring or doc_refs or test_refs:
                verdict = "P-证据不足"
            else:
                verdict = "N-未满足"

            findings: list[str] = []
            if not doc_refs:
                findings.append("ASPICE-SWE-TRACE")
            if not docstring:
                findings.append("ASPICE-SWE3-DD")
            if not test_refs:
                findings.append("ASPICE-SWE4-UV")
            if interface_state != "完整注解":
                findings.append("ASPICE-SWE3-IF")

            stable = hashlib.sha1(f"{rel}:{qualname}".encode()).hexdigest()[:10].upper()
            rows.append(
                {
                    "software_unit_id": f"SWU-{stable}",
                    "file": rel,
                    "line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                    "qualified_function": qualname,
                    "visibility": "public" if public else "internal",
                    "function_summary": docstring.splitlines()[0] if docstring else "未在函数级文档中说明；需从实现推断",
                    "detailed_design_evidence": design_state,
                    "interface_evidence": interface_state,
                    "requirements_architecture_trace": trace_state,
                    "document_references": ";".join(doc_refs),
                    "unit_verification_trace": verify_state,
                    "test_references": ";".join(test_refs),
                    "aspice_document_verdict": verdict,
                    "linked_findings": ";".join(findings),
                }
            )
    return sorted(rows, key=lambda row: (str(row["file"]), int(row["line"]), str(row["qualified_function"])))


def main() -> int:
    rows = _function_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    verdicts = Counter(str(row["aspice_document_verdict"]) for row in rows)
    findings = Counter(
        finding
        for row in rows
        for finding in str(row["linked_findings"]).split(";")
        if finding
    )
    summary = {
        "snapshot_head": "6da1e0c2e1ea0f4b43bba85a19db0576a88a37fa",
        "scope": "All non-test Python functions, excluding auditor/test tooling and virtual environments",
        "source_files": len(_source_files()),
        "functions": len(rows),
        "functions_with_docstrings": sum(row["detailed_design_evidence"] == "有函数说明" for row in rows),
        "functions_with_complete_annotations": sum(row["interface_evidence"] == "完整注解" for row in rows),
        "functions_with_document_symbol_references": sum(bool(row["document_references"]) for row in rows),
        "functions_with_same_name_test_references": sum(bool(row["test_references"]) for row in rows),
        "verdicts": dict(verdicts),
        "linked_findings": dict(findings),
        "method_limitations": [
            "Document and test links are conservative lexical symbol matches, not proof of semantic coverage.",
            "Indirect tests may exist even when no same-name test reference is found.",
            "A docstring or type annotation is supporting evidence, not a replacement for an agreed detailed design.",
        ],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
