"""Dependency injection container."""

from __future__ import annotations

from dataclasses import dataclass

from bot.config.settings import Settings
from bot.core.http_client import HttpClient


@dataclass
class Container:
    """Application dependency container.

    Attributes:
        settings: Loaded application settings.
        http_client: Shared HTTP client instance.
    """

    settings: Settings
    http_client: HttpClient

    @classmethod
    def create(cls, settings: Settings) -> "Container":
        """Create a container with default dependencies.

        Args:
            settings: Loaded application settings.

        Returns:
            Container instance.
        """

        http_client = HttpClient()
        return cls(settings=settings, http_client=http_client)
