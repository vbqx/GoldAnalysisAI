"""Application configuration from environment variables."""

from __future__ import annotations

import os

TV_SYMBOL = os.getenv("TV_SYMBOL", "XAUUSD")
TV_EXCHANGE = os.getenv("TV_EXCHANGE", "OANDA")
TV_USERNAME = os.getenv("TV_USERNAME")
TV_PASSWORD = os.getenv("TV_PASSWORD")

PROJECT_NAME = os.getenv("PROJECT_NAME", "GoldAnalysisAI")
GITHUB_REPO = os.getenv("GITHUB_REPO", "github.com/vbqx/GoldAnalysisAI")
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", PROJECT_NAME)

# Logging: DEBUG | INFO | WARNING | ERROR (default INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Optional file path, e.g. logs/goldanalysisai.log
LOG_FILE = os.getenv("LOG_FILE", "")
