"""Repository interface definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract repository interface."""

    @abstractmethod
    async def add(self, entity: T) -> None:
        """Add an entity to the repository."""

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None:
        """Fetch an entity by its primary key."""

    @abstractmethod
    async def list_all(self) -> Iterable[T]:
        """List all entities in the repository."""
