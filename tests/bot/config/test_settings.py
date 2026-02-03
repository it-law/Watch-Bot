"""Tests for application settings."""

from __future__ import annotations

from bot.config.settings import Settings


def test_settings_loads(settings: Settings) -> None:
    """Settings loads environment values."""

    assert settings.telegram_token == "123:ABC"
    assert settings.database_url.startswith("postgresql+psycopg://")
    assert settings.openai_api_key == "test-openai"
    assert settings.news_api_key == "test-news"
    assert settings.log_level == "INFO"
