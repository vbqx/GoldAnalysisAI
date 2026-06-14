"""Test runner engine for CLI and Streamlit dashboard."""
from __future__ import annotations

import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"

_RE_COLLECTED = re.compile(r"collected (\d+) item")
_RE_RESULT = re.compile(
    r"^(?P<name>.+?)\s+(?P<status>PASSED|FAILED|SKIPPED|ERROR)(?:\s+\[.*?\])?\s*$"
)
_RE_SUMMARY = re.compile(r"(\d+) passed")
_RE_SUMMARY_FAIL = re.compile(r"(\d+) failed")
_RE_PIPELINE_DONE = re.compile(r"pipeline done.*elapsed=([\d.]+)s")
_RE_PIPELINE_START = re.compile(r"pipeline start")


class Suite(str, Enum):
    FAST = "fast"
    UNIT = "unit"
    REGRESSION = "regression"
    INTEGRATION = "integration"
    FULL = "full"

    @property
    def label(self) -> str:
        return {
            Suite.FAST: "快速（单元 + 回归）",
            Suite.UNIT: "单元测试",
            Suite.REGRESSION: "回归测试",
            Suite.INTEGRATION: "集成测试（慢，~3min/条）",
            Suite.FULL: "完整（全部）",
        }[self]


@dataclass
class PhaseSpec:
    name: str
    args: list[str]


@dataclass
class RunState:
    status: str = "idle"  # idle | running | done | failed | stopped
    suite: str = ""
    phase: str = ""
    started_at: float = 0.0
    finished_at: float = 0.0
    collected: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    current_test: str = ""
    pipeline_elapsed: float | None = None
    exit_code: int = 0
    results: dict[str, str] = field(default_factory=dict)
    durations: dict[str, float] = field(default_factory=dict)
    logs: list[str] = field(default_factory=list)
    max_logs: int = 500

    @property
    def elapsed(self) -> float:
        end = self.finished_at or time.time()
        return max(0.0, end - self.started_at) if self.started_at else 0.0

    @property
    def progress(self) -> float:
        total = self.collected or max(len(self.results), 1)
        done = self.passed + self.failed + self.skipped
        return min(1.0, done / total) if total else 0.0

    def append_log(self, line: str) -> None:
        self.logs.append(line)
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs :]


def build_phases(suite: Suite) -> list[PhaseSpec]:
    common = ["--tb=short", "-v", "--color=no"]
    unit = PhaseSpec("unit", [str(TESTS / "unit"), *common])
    regression = PhaseSpec("regression", [str(TESTS / "regression"), *common, "-m", "regression"])
    integration = PhaseSpec("integration", [str(TESTS / "integration"), *common, "-m", "integration"])
    if suite == Suite.UNIT:
        return [unit]
    if suite == Suite.REGRESSION:
        return [regression]
    if suite == Suite.INTEGRATION:
        return [integration]
    if suite == Suite.FULL:
        return [unit, regression, integration]
    return [unit, regression]


def _pytest_cmd(args: list[str]) -> list[str]:
    return [sys.executable, "-m", "pytest", *args]


class TestRunManager:
    """Singleton background test runner (thread-safe reads)."""

    _lock = threading.Lock()
    _instance: TestRunManager | None = None

    def __init__(self) -> None:
        self.state = RunState()
        self._process: subprocess.Popen[str] | None = None
        self._thread: threading.Thread | None = None

    @classmethod
    def get(cls) -> TestRunManager:
        with cls._lock:
            if cls._instance is None:
                cls._instance = TestRunManager()
            return cls._instance

    def is_running(self) -> bool:
        return self.state.status == "running"

    def snapshot(self) -> RunState:
        with self._lock:
            return RunState(
                status=self.state.status,
                suite=self.state.suite,
                phase=self.state.phase,
                started_at=self.state.started_at,
                finished_at=self.state.finished_at,
                collected=self.state.collected,
                passed=self.state.passed,
                failed=self.state.failed,
                skipped=self.state.skipped,
                current_test=self.state.current_test,
                pipeline_elapsed=self.state.pipeline_elapsed,
                exit_code=self.state.exit_code,
                results=dict(self.state.results),
                durations=dict(self.state.durations),
                logs=list(self.state.logs),
            )

    def start(self, suite: Suite) -> bool:
        with self._lock:
            if self.state.status == "running":
                return False
            self.state = RunState(status="running", suite=suite.value, started_at=time.time())
            self._thread = threading.Thread(target=self._worker, args=(suite,), daemon=True, name="test-runner")
            self._thread.start()
            return True

    def stop(self) -> None:
        with self._lock:
            proc = self._process
            if proc and proc.poll() is None:
                proc.terminate()
            if self.state.status == "running":
                self.state.status = "stopped"
                self.state.finished_at = time.time()
                self.state.append_log("--- 用户已停止测试 ---")

    def reset(self) -> None:
        with self._lock:
            if self.state.status == "running":
                return
            self.state = RunState()

    def _worker(self, suite: Suite) -> None:
        phases = build_phases(suite)
        overall_exit = 0
        for phase in phases:
            with self._lock:
                if self.state.status != "running":
                    break
                self.state.phase = phase.name
                self.state.append_log(f"=== 阶段: {phase.name} ===")

            code = self._run_phase(phase)
            if code != 0:
                overall_exit = code
                if suite != Suite.FULL:
                    break

        with self._lock:
            if self.state.status == "running":
                self.state.exit_code = overall_exit
                self.state.status = "done" if overall_exit == 0 and self.state.failed == 0 else "failed"
                self.state.finished_at = time.time()
                self.state.current_test = ""
                summary = f"=== 完成: {self.state.passed} 通过"
                if self.state.failed:
                    summary += f", {self.state.failed} 失败"
                summary += f", 耗时 {self.state.elapsed:.1f}s ==="
                self.state.append_log(summary)

    def _run_phase(self, phase: PhaseSpec) -> int:
        cmd = _pytest_cmd(phase.args)
        env = {**dict(__import__("os").environ), "PYTHONUNBUFFERED": "1"}
        with self._lock:
            self.state.append_log("$ " + " ".join(cmd))

        proc = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        with self._lock:
            self._process = proc

        assert proc.stdout is not None
        phase_test_start = time.time()
        for raw in proc.stdout:
            line = raw.rstrip("\n\r")
            with self._lock:
                self._handle_line(line, time.time() - phase_test_start)
                phase_test_start = time.time()

        code = proc.wait()
        with self._lock:
            self._process = None
        return code

    def _handle_line(self, line: str, dt: float) -> None:
        self.state.append_log(line)

        if m := _RE_COLLECTED.search(line):
            self.state.collected += int(m.group(1))
            return

        if _RE_PIPELINE_START.search(line):
            self.state.current_test = "pipeline 运行中…"
            return

        if m := _RE_PIPELINE_DONE.search(line):
            self.state.pipeline_elapsed = float(m.group(1))
            return

        if m := _RE_RESULT.match(line.strip()):
            name = m.group("name")
            status = m.group("status")
            short = name.split("::")[-1]
            self.state.results[name] = status
            self.state.durations[name] = dt
            self.state.current_test = short
            if status == "PASSED":
                self.state.passed += 1
            elif status in ("FAILED", "ERROR"):
                self.state.failed += 1
            elif status == "SKIPPED":
                self.state.skipped += 1
            return

        if "passed" in line and "==" in line:
            if m := _RE_SUMMARY.search(line):
                pass  # final summary line; counts already tracked per test
            # pytest 有时单行汇总，确保结束时进度为 100%
            if self.state.collected == 0 and self.state.passed == 0:
                if m := _RE_SUMMARY.search(line):
                    self.state.passed = int(m.group(1))
                if m := _RE_SUMMARY_FAIL.search(line):
                    self.state.failed = int(m.group(1))


def load_catalog_summary() -> list[dict[str, str]]:
    """Lightweight catalog parse without PyYAML dependency."""
    path = TESTS / "cases" / "catalog.yaml"
    if not path.exists():
        return []
    cases: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := re.match(r"\s*- id:\s*(\S+)", line):
            if current.get("id"):
                cases.append(current)
            current = {"id": m.group(1)}
            continue
        if not current:
            continue
        for key in ("suite", "title", "priority", "layer", "automated"):
            if m := re.match(rf"\s*{key}:\s*(.+)", line):
                current[key] = m.group(1).strip().strip('"').strip("'")
    if current.get("id"):
        cases.append(current)
    return cases
