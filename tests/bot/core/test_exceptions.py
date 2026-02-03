"""Tests for custom exceptions."""

from __future__ import annotations

from bot.core.exceptions import BaseError, ExternalAPIError, ValidationError


def test_exceptions_instantiate() -> None:
    """Custom exceptions can be created."""

    assert isinstance(BaseError("base"), Exception)
    assert isinstance(ValidationError("validation"), BaseError)
    assert isinstance(ExternalAPIError("api"), BaseError)
