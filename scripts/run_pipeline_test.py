"""Backward-compatible shim → tests/run.py"""
from __future__ import annotations

import subprocess
import sys
import warnings
from pathlib import Path

warnings.warn("scripts/run_pipeline_test.py 已弃用，请使用: python tests/run.py --integration", DeprecationWarning, stacklevel=1)

ROOT = Path(__file__).resolve().parents[1]
raise SystemExit(
    subprocess.call([sys.executable, str(ROOT / "tests" / "run.py"), "--integration"], cwd=str(ROOT))
)
