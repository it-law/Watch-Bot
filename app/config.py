from __future__ import annotations

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "telegram-multichannel"
    environment: str = "development"
    database_url: str = "sqlite:///./data.db"
    redis_url: str = "redis://redis:6379/0"
    telegram_bot_token: str | None = None
    telegram_webhook_secret: str | None = None
    admin_username: str = "admin"
    admin_password: str = "admin"

    linkedin_token: str | None = None
    habr_token: str | None = None
    zen_token: str | None = None
    zakon_token: str | None = None
    blog_token: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False


class PlatformContent(BaseModel):
    platform: str
    title: str
    body: str
    hashtags: list[str] = []
    meta: dict[str, str] = {}


settings = Settings()
