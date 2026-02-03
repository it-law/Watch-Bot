"""Tests for main application wiring."""

from __future__ import annotations

from telegram.ext import Application

from bot.config.settings import Settings
from bot.main import build_application


def test_build_application(settings: Settings) -> None:
    """Application builder returns a Telegram Application."""

    app = build_application(settings)
    assert isinstance(app, Application)
