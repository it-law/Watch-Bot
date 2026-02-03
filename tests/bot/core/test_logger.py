"""Tests for logging utilities."""

from __future__ import annotations

import logging

from bot.core.logger import configure_logging, get_logger


def test_logger_configuration() -> None:
    """Logger configuration does not error and returns a logger."""

    configure_logging("INFO")
    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)
