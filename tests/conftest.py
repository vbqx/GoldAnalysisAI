"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import pytest

from tests._bootstrap import load_dotenv, setup_path

setup_path()
load_dotenv()


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "slow: integration test hitting network + LLM (~2-3 min)")
    config.addinivalue_line("markers", "integration: full pipeline or external services")
    config.addinivalue_line("markers", "regression: regression checks from system test report")
    config.addinivalue_line("markers", "financial: financial review cases (FIN-*) from docs/financial-review.md")


@pytest.fixture(autouse=True)
def offline_external_sources(request):
    """Mock News/DXY/Social fetches in unit tests (except dedicated source tests)."""
    if request.module.__name__.endswith("test_external_sources"):
        yield
        return

    from unittest.mock import patch

    with (
        patch(
            "src.data.sources.fundamentals.fetch_dxy_impact",
            return_value=("偏强 → 利空黄金（占位）", {"source": "placeholder", "bias": "bearish"}),
        ),
        patch(
            "src.data.sources.news.fetch_news_bundle",
            return_value=([], "美盘数据/讲话 → 波动放大（占位）", {"source": "placeholder"}),
        ),
        patch(
            "src.data.sources.social.fetch_social_sentiment",
            return_value=("—", [], {"source": "disabled"}),
        ),
    ):
        yield
