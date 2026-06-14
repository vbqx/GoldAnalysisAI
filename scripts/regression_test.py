"""Backward-compatible shim → tests/run.py --fast"""
from __future__ import annotations

import subprocess
import sys
import warnings
from pathlib import Path

warnings.warn("scripts/regression_test.py 已弃用，请使用: python tests/run.py --fast", DeprecationWarning, stacklevel=1)

ROOT = Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call([sys.executable, str(ROOT / "tests" / "run.py"), "--fast"], cwd=str(ROOT)))
