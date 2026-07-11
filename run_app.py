#!/usr/bin/env python3
"""GoldAnalysisAI cross-platform launcher (Windows + Linux + macOS).

Loads .env, applies dev UTF-8 settings, stops stale Streamlit, starts app.py.

Usage:
    python run_app.py
    python run_app.py --port 8503

Do NOT run ``streamlit run app.py`` directly. See AGENTS.md and README.md.
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        print(f".env not found at {path} (using existing environment only).")
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        os.environ[key] = val
    print("Loaded environment from .env")


def init_dev_env() -> None:
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"


def ensure_streamlit_config() -> None:
    cfg_dir = ROOT / ".streamlit"
    cfg_dir.mkdir(exist_ok=True)
    config_path = cfg_dir / "config.toml"
    if not config_path.is_file():
        config_path.write_text(
            "[browser]\ngatherUsageStats = false\n",
            encoding="utf-8",
        )
    cred_path = cfg_dir / "credentials.toml"
    if not cred_path.is_file():
        cred_path.write_text(
            "[general]\nemail = \"\"\n",
            encoding="utf-8",
        )


def _python_is_usable(candidate: Path) -> bool:
    try:
        proc = subprocess.run(
            [str(candidate), "-c", "import sys; print(sys.executable)"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception:
        return False
    return proc.returncode == 0


def resolve_python() -> Path | str:
    for rel in (".venv/Scripts/python.exe", ".venv/bin/python"):
        candidate = ROOT / rel
        if candidate.is_file() and _python_is_usable(candidate):
            return candidate
    return sys.executable or ("python3" if sys.platform != "win32" else "python")


def _pids_listening_on_port(port: int) -> list[int]:
    pids: list[int] = []
    my_pid = os.getpid()
    if sys.platform == "win32":
        try:
            out = subprocess.check_output(
                ["netstat", "-ano"],
                text=True,
                errors="replace",
                creationflags=CREATE_NO_WINDOW,
            )
        except Exception:
            return pids
        for line in out.splitlines():
            if f":{port}" in line and "LISTENING" in line.upper():
                parts = line.split()
                if not parts:
                    continue
                try:
                    pid = int(parts[-1])
                except ValueError:
                    continue
                if pid != my_pid and pid not in pids:
                    pids.append(pid)
        return pids

    for cmd in (
        ["lsof", "-tiTCP:%d" % port, "-sTCP:LISTEN"],
        ["fuser", "%d/tcp" % port],
    ):
        try:
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
        for token in out.split():
            if token.isdigit():
                pid = int(token)
                if pid != my_pid and pid not in pids:
                    pids.append(pid)
        if pids:
            break
    return pids


def _command_line_for_pid(pid: int) -> str:
    if sys.platform == "win32":
        ps = (
            "Get-CimInstance Win32_Process -Filter "
            f"\"ProcessId={pid}\" | Select-Object -ExpandProperty CommandLine"
        )
        try:
            return subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", ps],
                text=True,
                errors="replace",
                stderr=subprocess.DEVNULL,
                creationflags=CREATE_NO_WINDOW,
            ).strip()
        except Exception:
            return ""

    try:
        return subprocess.check_output(
            ["ps", "-p", str(pid), "-o", "args="],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""


def _is_project_streamlit_pid(pid: int, root: Path) -> bool:
    cmd = _command_line_for_pid(pid).lower()
    if "streamlit" not in cmd:
        return False
    root_marker = str(root).lower()
    return "app.py" in cmd or root_marker in cmd


def _streamlit_pids(root: Path) -> list[int]:
    pids: list[int] = []
    my_pid = os.getpid()
    root_marker = str(root).lower()

    if sys.platform == "win32":
        ps = (
            "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
            "Where-Object { $_.CommandLine -match 'streamlit' -and "
            "($_.CommandLine -match 'app\\.py' -or "
            f"$_.CommandLine.ToLower().Contains('{root_marker.replace(chr(39), chr(39)*2)}')) }} | "
            "Select-Object -ExpandProperty ProcessId"
        )
        try:
            out = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", ps],
                text=True,
                errors="replace",
                stderr=subprocess.DEVNULL,
                creationflags=CREATE_NO_WINDOW,
            )
        except Exception:
            return pids
        for line in out.splitlines():
            line = line.strip()
            if line.isdigit():
                pid = int(line)
                if pid != my_pid:
                    pids.append(pid)
        return pids

    try:
        out = subprocess.check_output(
            ["pgrep", "-f", "streamlit.*app.py"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return pids
    for line in out.splitlines():
        line = line.strip()
        if line.isdigit():
            pid = int(line)
            if pid != my_pid:
                pids.append(pid)
    return pids


def _terminate_pid(pid: int) -> None:
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            check=False,
            creationflags=CREATE_NO_WINDOW,
        )
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def stop_stale_streamlit(port: int) -> None:
    targets: list[int] = []
    streamlit_pids = _streamlit_pids(ROOT)
    port_streamlit_pids = [
        pid for pid in _pids_listening_on_port(port) if _is_project_streamlit_pid(pid, ROOT)
    ]
    for pid in streamlit_pids + port_streamlit_pids:
        if pid not in targets:
            targets.append(pid)

    if not targets:
        print("No stale Streamlit processes found.")
        return

    for pid in targets:
        print(f"Stopping stale Streamlit (PID {pid})...")
        _terminate_pid(pid)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start GoldAnalysisAI Streamlit app")
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="Listen port (default: STREAMLIT_SERVER_PORT or 8501)",
    )
    return parser.parse_args()


def main() -> int:
    os.chdir(ROOT)
    args = parse_args()

    init_dev_env()
    load_dotenv(ROOT / ".env")
    ensure_streamlit_config()

    if args.port > 0:
        port = args.port
    else:
        port = int(os.environ.get("STREAMLIT_SERVER_PORT", "8501"))

    stop_stale_streamlit(port)

    python = resolve_python()
    url = f"http://localhost:{port}"
    print()
    print(f"Starting GoldAnalysisAI at {url}")
    print("Launcher: python run_app.py (do not use bare 'streamlit run app.py')")
    print()

    cmd = [str(python), "-m", "streamlit", "run", str(ROOT / "app.py"), "--server.port", str(port)]
    try:
        rc = subprocess.call(cmd)
    except KeyboardInterrupt:
        return 130
    if rc != 0:
        print(
            f"\nStreamlit exited with code {rc}. "
            "Do not run `python app.py` directly — use `python run_app.py`.\n",
            file=sys.stderr,
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
