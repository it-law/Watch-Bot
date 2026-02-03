"""Custom exception hierarchy for the application."""

from __future__ import annotations


class BaseError(Exception):
    """Base class for application-specific errors."""


class ValidationError(BaseError):
    """Raised when input validation fails."""


class ExternalAPIError(BaseError):
    """Raised when an external API call fails."""
