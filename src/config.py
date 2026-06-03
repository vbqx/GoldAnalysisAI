"""Application configuration from environment variables."""

from __future__ import annotations

import os

TV_SYMBOL = os.getenv("TV_SYMBOL", "XAUUSD")
TV_EXCHANGE = os.getenv("TV_EXCHANGE", "OANDA")
TV_USERNAME = os.getenv("TV_USERNAME")
TV_PASSWORD = os.getenv("TV_PASSWORD")
