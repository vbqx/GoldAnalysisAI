"""External data sources — Jin10 MCP, DXY, TV social, market bars."""

from src.data.sources.fundamentals import FundamentalsDataSource
from src.data.sources.market import MarketDataSource
from src.data.sources.news import NewsDataSource
from src.data.sources.social import SocialDataSource

__all__ = [
    "FundamentalsDataSource",
    "MarketDataSource",
    "NewsDataSource",
    "SocialDataSource",
]
