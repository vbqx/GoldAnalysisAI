#!/usr/bin/env python3
"""Unified test runner for GoldAnalysisAI.

Usage:
    python tests/run.py              # fast: unit + regression (no network)
    python tests/run.py --fast       # same as default
    python tests/run.py --full       # unit + regression + integration (slow)
    python tests/run.py --unit       # unit only
    python tests/run.py --regression # regression only
    python tests/run.py --integration # integration only (slow)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def _pytest(args: list[str]) -> int:
    cmd = [sys.executable, "-m", "pytest", *args]
    print("$", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="GoldAnalysisAI test runner")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fast", action="store_true", help="unit + regression (default)")
    group.add_argument("--full", action="store_true", help="all tests including slow integration")
    group.add_argument("--unit", action="store_true", help="unit tests only")
    group.add_argument("--regression", action="store_true", help="regression tests only")
    group.add_argument("--integration", action="store_true", help="integration tests only (slow)")
    group.add_argument("--financial", action="store_true", help="financial review tests (FIN-*) only")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    verbose = ["-v"] if args.verbose else ["-q"]
    common = ["--tb=short", *verbose]

    if args.unit:
        return _pytest([str(TESTS / "unit"), *common])
    if args.regression:
        return _pytest([str(TESTS / "regression"), *common, "-m", "regression"])
    if args.financial:
        return _pytest([str(TESTS / "unit" / "test_financial_review.py"), *common, "-m", "financial"])
    if args.integration:
        return _pytest([str(TESTS / "integration"), *common, "-m", "integration"])
    if args.full:
        return _pytest([str(TESTS), *common])

    # default --fast: all unit tests (incl. FIN-*) + regression
    code = _pytest([str(TESTS / "unit"), *common])
    if code != 0:
        return code
    return _pytest([str(TESTS / "regression"), *common, "-m", "regression"])


if __name__ == "__main__":
    raise SystemExit(main())
