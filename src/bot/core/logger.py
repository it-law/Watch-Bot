"""Logging configuration utilities."""

from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: str) -> None:
    """Configure root logging.

    Args:
        level: Logging level name (e.g., "INFO").
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Create or retrieve a module logger.

    Args:
        name: Optional logger name.

    Returns:
        Configured logger instance.
    """

    return logging.getLogger(name if name is not None else __name__)
