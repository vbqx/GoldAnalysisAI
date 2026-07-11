#!/usr/bin/env python3
"""Deprecated wrapper - use repo-root ``python run_app.py`` instead."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
runpy.run_path(str(ROOT / "run_app.py"), run_name="__main__")
