"""Application configuration from environment variables."""

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
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip())


_load_dotenv()
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

# Optional MT5 execution bridge. Disabled by default; the MetaTrader5 Python
# package and a running terminal are only required when MT5_ENABLED=true.
MT5_ENABLED = os.getenv("MT5_ENABLED", "false").lower() in ("1", "true", "yes")
MT5_SYMBOL = os.getenv("MT5_SYMBOL", TV_SYMBOL)
MT5_ACCOUNT = os.getenv("MT5_ACCOUNT", "")
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")
MT5_PATH = os.getenv("MT5_PATH", "")
MT5_TIMEOUT_MS = max(1000, int(os.getenv("MT5_TIMEOUT_MS", "10000")))

# Analyst Team input density (payload / evidence limits)
ANALYST_NEWS_MAX = max(3, int(os.getenv("ANALYST_NEWS_MAX", "20")))
ANALYST_CALENDAR_MAX = max(1, int(os.getenv("ANALYST_CALENDAR_MAX", "12")))
ANALYST_SOCIAL_MAX = max(1, int(os.getenv("ANALYST_SOCIAL_MAX", "15")))
ANALYST_ICT_EVENTS_MAX = max(2, int(os.getenv("ANALYST_ICT_EVENTS_MAX", "8")))
ANALYST_TEAM_ITEMS_MAX = max(4, int(os.getenv("ANALYST_TEAM_ITEMS_MAX", "16")))
PAYLOAD_EVIDENCE_MAX = max(4, int(os.getenv("PAYLOAD_EVIDENCE_MAX", "20")))
LLM_MIN_ANALYST_ITEMS = max(1, int(os.getenv("LLM_MIN_ANALYST_ITEMS", "4")))
JIN10_QUOTE_CODE = os.getenv("JIN10_QUOTE_CODE", "XAUUSD")
JIN10_QUOTE_ENABLED = os.getenv("JIN10_QUOTE_ENABLED", "true").lower() in ("1", "true", "yes")
JIN10_KLINE_CODE = os.getenv("JIN10_KLINE_CODE", JIN10_QUOTE_CODE)
JIN10_KLINE_COUNT = max(5, int(os.getenv("JIN10_KLINE_COUNT", "20")))
JIN10_KLINE_ENABLED = os.getenv("JIN10_KLINE_ENABLED", "true").lower() in ("1", "true", "yes")
# Optional integer period for get_kline (omit if empty — MCP default)
_kline_period_raw = os.getenv("JIN10_KLINE_PERIOD", "").strip()
JIN10_KLINE_PERIOD: int | None = int(_kline_period_raw) if _kline_period_raw.isdigit() else None

# External data (Jin10 MCP news/calendar, TradingView DXY/social)
JIN10_API_TOKEN = os.getenv("JIN10_API_TOKEN", "") or os.getenv("JIN10_BEARER_TOKEN", "")
JIN10_ENABLED = os.getenv("JIN10_ENABLED", "true" if JIN10_API_TOKEN else "false").lower() in (
    "1",
    "true",
    "yes",
)
JIN10_MCP_URL = os.getenv("JIN10_MCP_URL", "https://mcp.jin10.com/mcp")
JIN10_MCP_PROTOCOL = os.getenv("JIN10_MCP_PROTOCOL", "2025-11-25")
JIN10_KEYWORD = os.getenv("JIN10_KEYWORD") or os.getenv("JIN10_FLASH_KEYWORD", "黄金")
JIN10_FLASH_KEYWORD = JIN10_KEYWORD  # legacy alias
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

PROJECT_NAME = os.getenv("PROJECT_NAME", "GoldAnalysisAI")
GITHUB_REPO = os.getenv("GITHUB_REPO", "github.com/vbqx/GoldAnalysisAI")
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", PROJECT_NAME)

# Trading signal geometry (F-004)
SIGNAL_SWEEP_OFFSET = float(os.getenv("SIGNAL_SWEEP_OFFSET", "5"))
SIGNAL_SL_BELOW_SWING = float(os.getenv("SIGNAL_SL_BELOW_SWING", "9"))
RISK_REWARD_DISPLAY_CAP = float(os.getenv("RISK_REWARD_DISPLAY_CAP", "8"))

# Logging: DEBUG | INFO | WARNING | ERROR (default INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Optional file path, e.g. logs/goldanalysisai.log
LOG_FILE = os.getenv("LOG_FILE", "")

# LLM — report narrative layer (end of pipeline, independent switch)
LLM_ENABLED = os.getenv("LLM_ENABLED", "false").lower() in ("1", "true", "yes")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_MODEL_FAST = os.getenv("LLM_MODEL_FAST", LLM_MODEL)
LLM_MODEL_STRONG = os.getenv("LLM_MODEL_STRONG", LLM_MODEL)
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))
LLM_ENHANCE_CONCLUSION = os.getenv("LLM_ENHANCE_CONCLUSION", "true").lower() in ("1", "true", "yes")

# Agent pipeline mode: rule | llm | hybrid
AGENT_MODE = os.getenv("AGENT_MODE", "rule").lower()
if AGENT_MODE not in ("rule", "llm", "hybrid"):
    AGENT_MODE = "rule"

LLM_OVERRIDE_THRESHOLD = float(os.getenv("LLM_OVERRIDE_THRESHOLD", "0.65"))
_LLM_ANALYST_ONLY_RAW = os.getenv("LLM_ANALYST_ONLY", "").strip().lower()
_LLM_ANALYST_ALIASES = {
    "": "",
    "all": "",
    "technical": "technical",
    "technical_analyst": "technical",
    "fundamentals": "fundamentals",
    "fundamentals_analyst": "fundamentals",
    "news": "news",
    "news_analyst": "news",
    "sentiment": "sentiment",
    "sentiment_analyst": "sentiment",
}
LLM_ANALYST_ONLY = _LLM_ANALYST_ALIASES.get(_LLM_ANALYST_ONLY_RAW, "")


def short_model_name(model: str) -> str:
    return model.split("/")[-1] if model else "—"


def llm_sidebar_models() -> str:
    """Sidebar caption: show actual fast/strong models from .env.

    Fix #7 [Improvement] 侧边栏仅显示 STRONG 模型，与研究阶段 FAST 模型不一致
    原因：研究阶段用 LLM_MODEL_FAST、辩论/文案用 STRONG/REPORT，侧边栏需分别展示。
    """
    fast = short_model_name(LLM_MODEL_FAST)
    strong = short_model_name(LLM_MODEL_STRONG)
    report = short_model_name(LLM_MODEL)
    if fast == strong == report:
        return fast
    parts = [f"研究 {fast}", f"辩论 {strong}"]
    if report not in (fast, strong):
        parts.append(f"文案 {report}")
    return " · ".join(parts)


def _stage_flag(name: str) -> bool:
    return os.getenv(name, "false").lower() in ("1", "true", "yes")


LLM_STAGE_RESEARCH = _stage_flag("LLM_STAGE_RESEARCH")
LLM_STAGE_DEBATE = _stage_flag("LLM_STAGE_DEBATE")
LLM_STAGE_ANALYSTS = _stage_flag("LLM_STAGE_ANALYSTS")
LLM_STAGE_ICT = _stage_flag("LLM_STAGE_ICT")
LLM_STAGE_LEVELS = _stage_flag("LLM_STAGE_LEVELS")
LLM_STAGE_TRADER = _stage_flag("LLM_STAGE_TRADER")
LLM_STAGE_RISK = _stage_flag("LLM_STAGE_RISK")
LLM_STAGE_MANAGER = _stage_flag("LLM_STAGE_MANAGER")


def _stage_flag_or(name: str, default: bool) -> bool:
    if name in os.environ:
        return _stage_flag(name)
    return default


LLM_STAGE_BULLISH = _stage_flag_or("LLM_STAGE_BULLISH", LLM_STAGE_RESEARCH)
LLM_STAGE_BEARISH = _stage_flag_or("LLM_STAGE_BEARISH", LLM_STAGE_RESEARCH)

LLM_PARALLEL_ENABLED = os.getenv("LLM_PARALLEL_ENABLED", "true").lower() in ("1", "true", "yes")
LLM_PARALLEL_MAX_WORKERS = max(1, int(os.getenv("LLM_PARALLEL_MAX_WORKERS", "4")))
LLM_PARALLEL_RESEARCH = os.getenv("LLM_PARALLEL_RESEARCH", "true").lower() in ("1", "true", "yes")
# Debate output is small JSON; STRONG is default but FAST cuts wall time when models differ.
LLM_DEBATE_USE_FAST = os.getenv("LLM_DEBATE_USE_FAST", "false").lower() in ("1", "true", "yes")
