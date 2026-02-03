"""Tests for user model."""

from __future__ import annotations

from bot.models.user import Base, User


def test_user_model_metadata() -> None:
    """User model has table metadata."""

    assert User.__tablename__ == "users"
    assert hasattr(User, "__table__")
    assert Base.metadata.tables["users"].name == "users"
