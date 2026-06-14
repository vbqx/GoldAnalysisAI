"""TradingAgents-style Analyst Team — four specialists before bull/bear research."""

from __future__ import annotations

from src.agents.analysts.fundamentals import run_fundamentals_analyst
from src.agents.analysts.news import run_news_analyst
from src.agents.analysts.sentiment import run_sentiment_analyst
from src.agents.analysts.technical import run_technical_analyst
from src.core.types import AnalystTeam, MarketContext

__all__ = [
    "run_analyst_team",
    "run_fundamentals_analyst",
    "run_news_analyst",
    "run_sentiment_analyst",
    "run_technical_analyst",
]


def run_analyst_team(ctx: MarketContext) -> AnalystTeam:
    return AnalystTeam(
        technical=run_technical_analyst(ctx),
        fundamentals=run_fundamentals_analyst(ctx),
        news=run_news_analyst(ctx),
        sentiment=run_sentiment_analyst(ctx),
    )
