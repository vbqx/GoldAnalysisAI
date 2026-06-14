"""Backward-compatible shim → pytest tests/unit/test_llm_json.py"""
from __future__ import annotations

import subprocess
import sys
import warnings
from pathlib import Path

warnings.warn("scripts/test_llm_json_fix.py 已弃用，请使用: pytest tests/unit/test_llm_json.py", DeprecationWarning, stacklevel=1)

ROOT = Path(__file__).resolve().parents[1]
raise SystemExit(
    subprocess.call([sys.executable, "-m", "pytest", "tests/unit/test_llm_json.py", "-q"], cwd=str(ROOT))
)
