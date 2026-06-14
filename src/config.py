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

# External data (News / DXY / Social)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
TE_CALENDAR_ENABLED = os.getenv("TE_CALENDAR_ENABLED", "true").lower() in ("1", "true", "yes")
TE_CALENDAR_COUNTRY = os.getenv("TE_CALENDAR_COUNTRY", "united states")
TE_CALENDAR_DAYS = max(1, int(os.getenv("TE_CALENDAR_DAYS", "2")))
TE_CALENDAR_MIN_IMPORTANCE = max(1, min(3, int(os.getenv("TE_CALENDAR_MIN_IMPORTANCE", "2"))))
NEWS_RSS_ENABLED = os.getenv("NEWS_RSS_ENABLED", "true").lower() in ("1", "true", "yes")
TV_SOCIAL_ENABLED = os.getenv("TV_SOCIAL_ENABLED", "true").lower() in ("1", "true", "yes")
TV_SOCIAL_SYMBOL = os.getenv("TV_SOCIAL_SYMBOL", TV_SYMBOL)
TV_SOCIAL_IDEAS_LIMIT = max(5, int(os.getenv("TV_SOCIAL_IDEAS_LIMIT", "25")))
TV_SOCIAL_MINDS_LIMIT = max(5, int(os.getenv("TV_SOCIAL_MINDS_LIMIT", "15")))
EXTERNAL_HTTP_TIMEOUT = int(os.getenv("EXTERNAL_HTTP_TIMEOUT", "15"))
EXTERNAL_HTTP_RETRIES = max(0, int(os.getenv("EXTERNAL_HTTP_RETRIES", "2")))

PROJECT_NAME = os.getenv("PROJECT_NAME", "GoldAnalysisAI")
GITHUB_REPO = os.getenv("GITHUB_REPO", "github.com/vbqx/GoldAnalysisAI")
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", PROJECT_NAME)

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
LLM_STAGE_TRADER = _stage_flag("LLM_STAGE_TRADER")
LLM_STAGE_RISK = _stage_flag("LLM_STAGE_RISK")
LLM_STAGE_MANAGER = _stage_flag("LLM_STAGE_MANAGER")
