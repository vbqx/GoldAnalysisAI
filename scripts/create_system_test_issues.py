"""Backward-compatible shim → tests/tools/github/create_issues.py"""
from __future__ import annotations

import runpy
import warnings

warnings.warn("scripts/create_system_test_issues.py 已弃用，请使用 tests/tools/github/create_issues.py", DeprecationWarning, stacklevel=1)

runpy.run_path("tests/tools/github/create_issues.py", run_name="__main__")
