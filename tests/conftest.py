"""Pytest fixtures for the project."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from bot.config.settings import Settings


@pytest.fixture()
def settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """Provide Settings with environment variables.

    Args:
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        Settings instance with test values.
    """

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:ABC")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://user:pass@localhost:5432/test_db",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai")
    monkeypatch.setenv("NEWS_API_KEY", "test-news")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    return Settings()


def pytest_configure() -> None:
    """Ensure src/ is on the import path for tests."""

    if str(SRC_PATH) not in sys.path:
        sys.path.insert(0, str(SRC_PATH))
