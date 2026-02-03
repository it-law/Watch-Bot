"""Tests for the dependency injection container."""

from __future__ import annotations

from bot.config.settings import Settings
from bot.core.di import Container
from bot.core.http_client import HttpClient


def test_container_create(settings: Settings) -> None:
    """Container is created with default dependencies."""

    container = Container.create(settings)
    assert container.settings is settings
    assert isinstance(container.http_client, HttpClient)
