"""Run full pipeline test with .env loaded."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
# Fix #5 [Improvement] run_pipeline_test.py 直接运行报 ModuleNotFoundError
# 原因：脚本未将项目根目录加入 sys.path，直接运行找不到 src 包。
sys.path.insert(0, str(ROOT))

for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    os.environ[k.strip()] = v.strip()

from src.config import AGENT_MODE, LLM_ENABLED, LLM_MODEL, LLM_MODEL_FAST, LLM_MODEL_STRONG
from src.core.progress import ProgressReporter, set_progress, reset_progress
from src.pipeline import run_analysis

print("AGENT_MODE:", AGENT_MODE)
print("LLM_ENABLED:", LLM_ENABLED)
print("FAST:", LLM_MODEL_FAST)
print("STRONG:", LLM_MODEL_STRONG)
print("REPORT:", LLM_MODEL)
print("---")

reporter = ProgressReporter()
token = set_progress(reporter)
t0 = time.perf_counter()
try:
    report, data, analyses = run_analysis()
finally:
    reset_progress(token)

elapsed = time.perf_counter() - t0
meta = report.get("meta", {})
print(f"OK price={report['metrics']['current_price']:.2f} elapsed={elapsed:.1f}s")
print("agent_mode:", meta.get("agent_mode"))
print("stage_sources:", json.dumps(meta.get("stage_sources", {}), ensure_ascii=False, indent=2))
print("generation_steps:")
for s in meta.get("generation_steps", []):
    print(f"  - {s['label']}: {s['status']} {s.get('detail','')}")
llm = report.get("llm_analysis") or {}
print("llm_analysis enabled:", llm.get("enabled"), "error:", llm.get("error"))
print("llm_io calls:", len(meta.get("llm_io", [])))
for io in meta.get("llm_io", []):
    print(f"  - {io.get('label')}: {io.get('model')} ({io.get('latency_ms')}ms)")
