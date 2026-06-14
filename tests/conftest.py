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
