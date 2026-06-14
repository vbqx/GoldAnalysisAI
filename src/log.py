"""Central logging setup for GoldAnalysisAI."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import LOG_FILE, LOG_LEVEL

_CONFIGURED = False
_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(*, level: str | None = None, log_file: str | None = None) -> None:
    """Configure root logger once (console + optional rotating file)."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    level_name = (level or LOG_LEVEL or "INFO").upper()
    numeric_level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    console = logging.StreamHandler(sys.stderr)
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    console.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
    root.addHandler(console)

    file_path = log_file if log_file is not None else LOG_FILE
    if file_path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
        root.addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("websocket").setLevel(logging.WARNING)

    _CONFIGURED = True
    logging.getLogger(__name__).debug(
        "logging initialized level=%s file=%s",
        level_name,
        file_path or "(console only)",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module logger; ensures logging is configured."""
    setup_logging()
    return logging.getLogger(name)
