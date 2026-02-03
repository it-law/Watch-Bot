"""Tests for repository interfaces."""

from __future__ import annotations

from bot.repositories.base import Repository
from bot.repositories.user_repo import UserRepository


def test_user_repo_is_repository() -> None:
    """UserRepository extends Repository interface."""

    assert issubclass(UserRepository, Repository)
