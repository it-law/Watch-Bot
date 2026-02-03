"""User repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from bot.models.user import User
from bot.repositories.base import Repository


class UserRepository(Repository[User], ABC):
    """Repository interface for user entities."""

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Fetch a user by Telegram ID."""
