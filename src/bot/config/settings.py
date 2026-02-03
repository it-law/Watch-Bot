"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the bot.

    Attributes:
        telegram_token: Telegram bot token.
        database_url: SQLAlchemy database URL.
        openai_api_key: OpenAI or Claude API key.
        news_api_key: API key for external news sources.
        log_level: Logging level name.
    """

    telegram_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    database_url: str = Field(..., alias="DATABASE_URL")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    news_api_key: str = Field(..., alias="NEWS_API_KEY")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )
