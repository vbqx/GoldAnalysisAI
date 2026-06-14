"""Backward-compatible shim → tests/tools/github/close_issues.py"""
from __future__ import annotations

import runpy
import warnings

warnings.warn("scripts/close_fixed_issues.py 已弃用，请使用 tests/tools/github/close_issues.py", DeprecationWarning, stacklevel=1)

runpy.run_path("tests/tools/github/close_issues.py", run_name="__main__")
