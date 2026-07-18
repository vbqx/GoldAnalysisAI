"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import pytest

from tests._bootstrap import load_dotenv, setup_path

setup_path()
load_dotenv()


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "slow: integration test hitting network + LLM (~2-3 min)")
    config.addinivalue_line("markers", "integration: full pipeline or external services")
    config.addinivalue_line("markers", "external_api: live News/DXY/Social HTTP smoke tests")
    config.addinivalue_line("markers", "regression: regression checks from system test report")
    config.addinivalue_line("markers", "financial: financial review cases (FIN-*) from docs/aspice/records/reviews/financial/static-code-review.md")


def _skip_offline_external_mock(request) -> bool:
    name = request.module.__name__
    return (
        name.endswith("test_external_sources")
        or name.endswith("test_external_apis")
        or name.endswith("test_doc_pipeline_sync")
    )


@pytest.fixture(autouse=True)
def offline_external_sources(request):
    """Mock News/DXY/Social fetches in unit tests (except dedicated source tests)."""
    if _skip_offline_external_mock(request):
        yield
        return

    from unittest.mock import patch

    from src.data.sources.jin10_feed import Jin10NewsBundle

    with (
        patch(
            "src.data.sources.fundamentals.fetch_macro_quotes",
            return_value=[],
        ),
        patch(
            "src.data.sources.news.fetch_jin10_bundle",
            return_value=Jin10NewsBundle(risk_events="美盘数据/讲话 → 波动放大（占位）"),
        ),
        patch(
            "src.data.sources.social.fetch_social_sentiment",
            return_value=("—", [], {"source": "disabled"}),
        ),
    ):
        yield
