"""Backward-compatible shim → tests/tools/chart_compare.py"""
from __future__ import annotations

import runpy
import warnings

warnings.warn("scripts/chart_compare_test.py 已弃用，请使用: python tests/tools/chart_compare.py", DeprecationWarning, stacklevel=1)

runpy.run_module("tests.tools.chart_compare", run_name="__main__")
