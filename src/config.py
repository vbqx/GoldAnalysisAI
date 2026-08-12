"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

# Market data
TV_SYMBOL = os.getenv("TV_SYMBOL", "XAUUSD")
TV_EXCHANGE = os.getenv("TV_EXCHANGE", "OANDA")
TV_USERNAME = os.getenv("TV_USERNAME")
TV_PASSWORD = os.getenv("TV_PASSWORD")
TV_FETCH_RETRIES = max(0, int(os.getenv("TV_FETCH_RETRIES", "3")))
TV_FETCH_RETRY_BASE_S = float(os.getenv("TV_FETCH_RETRY_BASE_S", "2.0"))
TV_FETCH_ROUND_RETRIES = max(0, int(os.getenv("TV_FETCH_ROUND_RETRIES", "1")))
TV_DXY_EXCHANGE = os.getenv("TV_DXY_EXCHANGE", "TVC")
TV_DXY_SYMBOL = os.getenv("TV_DXY_SYMBOL", "DXY")
TV_US10Y_EXCHANGE = os.getenv("TV_US10Y_EXCHANGE", "TVC")
TV_US10Y_SYMBOL = os.getenv("TV_US10Y_SYMBOL", "US10Y")

# Optional MT5 connection self-check. Advice V2 never sends orders.
MT5_ENABLED = os.getenv("MT5_ENABLED", "false").lower() in ("1", "true", "yes")
MT5_SYMBOL = os.getenv("MT5_SYMBOL", TV_SYMBOL)
MT5_ACCOUNT = os.getenv("MT5_ACCOUNT", "")
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")
MT5_PATH = os.getenv("MT5_PATH", "")
MT5_TIMEOUT_MS = max(1000, int(os.getenv("MT5_TIMEOUT_MS", "10000")))

# External context payload caps
ANALYST_NEWS_MAX = max(3, int(os.getenv("ANALYST_NEWS_MAX", "20")))
ANALYST_CALENDAR_MAX = max(1, int(os.getenv("ANALYST_CALENDAR_MAX", "12")))
ANALYST_SOCIAL_MAX = max(1, int(os.getenv("ANALYST_SOCIAL_MAX", "15")))
JIN10_QUOTE_CODE = os.getenv("JIN10_QUOTE_CODE", "XAUUSD")
JIN10_QUOTE_ENABLED = os.getenv("JIN10_QUOTE_ENABLED", "true").lower() in ("1", "true", "yes")
JIN10_KLINE_CODE = os.getenv("JIN10_KLINE_CODE", JIN10_QUOTE_CODE)
JIN10_KLINE_COUNT = max(5, int(os.getenv("JIN10_KLINE_COUNT", "20")))
JIN10_KLINE_ENABLED = os.getenv("JIN10_KLINE_ENABLED", "true").lower() in ("1", "true", "yes")
_kline_period_raw = os.getenv("JIN10_KLINE_PERIOD", "").strip()
JIN10_KLINE_PERIOD: int | None = int(_kline_period_raw) if _kline_period_raw.isdigit() else None

JIN10_API_TOKEN = os.getenv("JIN10_API_TOKEN", "") or os.getenv("JIN10_BEARER_TOKEN", "")
JIN10_ENABLED = os.getenv("JIN10_ENABLED", "true" if JIN10_API_TOKEN else "false").lower() in (
    "1",
    "true",
    "yes",
)
JIN10_MCP_URL = os.getenv("JIN10_MCP_URL", "https://mcp.jin10.com/mcp")
JIN10_MCP_PROTOCOL = os.getenv("JIN10_MCP_PROTOCOL", "2025-11-25")
JIN10_KEYWORD = os.getenv("JIN10_KEYWORD") or os.getenv("JIN10_FLASH_KEYWORD", "黄金")
JIN10_FLASH_KEYWORD = JIN10_KEYWORD
JIN10_NEWS_LIMIT = max(3, int(os.getenv("JIN10_NEWS_LIMIT", "12")))
JIN10_FLASH_LIMIT = max(1, int(os.getenv("JIN10_FLASH_LIMIT", "8")))
JIN10_ARTICLE_LIMIT = max(1, int(os.getenv("JIN10_ARTICLE_LIMIT", "6")))
JIN10_CACHE_TTL = max(0, int(os.getenv("JIN10_CACHE_TTL", "600")))
JIN10_MCP_TIMEOUT = max(30, int(os.getenv("JIN10_MCP_TIMEOUT", "60")))
TV_SOCIAL_ENABLED = os.getenv("TV_SOCIAL_ENABLED", "true").lower() in ("1", "true", "yes")
TV_SOCIAL_SYMBOL = os.getenv("TV_SOCIAL_SYMBOL", TV_SYMBOL)
TV_SOCIAL_IDEAS_LIMIT = max(5, int(os.getenv("TV_SOCIAL_IDEAS_LIMIT", "25")))
TV_SOCIAL_MINDS_LIMIT = max(5, int(os.getenv("TV_SOCIAL_MINDS_LIMIT", "15")))
EXTERNAL_HTTP_TIMEOUT = int(os.getenv("EXTERNAL_HTTP_TIMEOUT", "15"))
EXTERNAL_HTTP_RETRIES = max(0, int(os.getenv("EXTERNAL_HTTP_RETRIES", "2")))

# Application and logging
PROJECT_NAME = os.getenv("PROJECT_NAME", "GoldAnalysisAI")
GITHUB_REPO = os.getenv("GITHUB_REPO", "github.com/vbqx/GoldAnalysisAI")
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", PROJECT_NAME)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "")

# Optional Advice V2 prose enhancement
LLM_ENABLED = os.getenv("LLM_ENABLED", "false").lower() in ("1", "true", "yes")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-v4-flash")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))
LLM_CONNECT_TIMEOUT = float(os.getenv("LLM_CONNECT_TIMEOUT", str(min(30, LLM_TIMEOUT))))
LLM_READ_TIMEOUT = float(os.getenv("LLM_READ_TIMEOUT", str(LLM_TIMEOUT)))
LLM_MAX_RETRIES = max(0, min(5, int(os.getenv("LLM_MAX_RETRIES", "2"))))
LLM_RETRY_BACKOFF_BASE_S = max(0.1, float(os.getenv("LLM_RETRY_BACKOFF_BASE_S", "1.0")))
LLM_STREAM_INCLUDE_USAGE = os.getenv("LLM_STREAM_INCLUDE_USAGE", "true").lower() in (
    "1",
    "true",
    "yes",
)
LLM_STAGE_WARN_MS = max(30_000, int(os.getenv("LLM_STAGE_WARN_MS", "120000")))


def short_model_name(model: str) -> str:
    return model.split("/")[-1] if model else "—"


def llm_provider_extra_payload(*, model: str | None = None) -> dict[str, object]:
    """Provider-specific chat/completions fields (e.g. DeepSeek V4 thinking mode)."""
    model_id = (model or LLM_MODEL).lower()
    mode = os.getenv("LLM_THINKING", "").strip().lower()
    if mode in ("enabled", "on", "true", "1", "yes"):
        return {"thinking": {"type": "enabled"}}
    if mode in ("disabled", "off", "false", "0", "no"):
        return {"thinking": {"type": "disabled"}}
    # V4 Flash defaults to thinking on; advice wording uses fast non-thinking mode.
    if "deepseek-v4" in model_id:
        return {"thinking": {"type": "disabled"}}
    return {}


# Run archive retention (0 means unlimited)
RUN_ARCHIVE_MAX_COUNT = max(0, int(os.getenv("RUN_ARCHIVE_MAX_COUNT", "200")))
RUN_ARCHIVE_MAX_MB = max(0, int(os.getenv("RUN_ARCHIVE_MAX_MB", "2048")))
