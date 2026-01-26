from __future__ import annotations

import abc
from dataclasses import dataclass

from app.config import PlatformContent


@dataclass
class PublishResult:
    status: str
    url: str | None = None
    error: str | None = None
    dry_run: bool = False


class Publisher(abc.ABC):
    platform: str

    @abc.abstractmethod
    def publish(self, content: PlatformContent) -> PublishResult:
        raise NotImplementedError
