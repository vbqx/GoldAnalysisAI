#!/usr/bin/env bash
# GoldAnalysisAI launcher (Linux/macOS) -> cross-platform run_app.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [[ -x "$ROOT/.venv/bin/python" ]] && "$ROOT/.venv/bin/python" -c "import sys" >/dev/null 2>&1; then
  exec "$ROOT/.venv/bin/python" run_app.py "$@"
fi
exec "${PYTHON:-python3}" run_app.py "$@"
