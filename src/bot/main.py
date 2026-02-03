"""Application entrypoint."""

from __future__ import annotations

from telegram.ext import Application

from bot.config.settings import Settings
from bot.core.di import Container
from bot.core.logger import configure_logging, get_logger

logger = get_logger(__name__)


def build_application(settings: Settings) -> Application:
    """Build the Telegram application.

    Args:
        settings: Loaded application settings.

    Returns:
        Configured Telegram Application.
    """

    container = Container.create(settings=settings)

    async def _post_init(app: Application) -> None:
        """Initialize shared resources."""

        app.bot_data["container"] = container
        await container.http_client.start()

    async def _post_shutdown(app: Application) -> None:
        """Cleanup shared resources."""

        await container.http_client.close()

    application = (
        Application.builder()
        .token(settings.telegram_token)
        .concurrent_updates(True)
        .post_init(_post_init)
        .post_shutdown(_post_shutdown)
        .build()
    )

    return application


def main() -> None:
    """Run the bot application."""

    settings = Settings()
    configure_logging(settings.log_level)
    logger.info("Starting application")

    application = build_application(settings)
    application.run_polling()


if __name__ == "__main__":
    main()
