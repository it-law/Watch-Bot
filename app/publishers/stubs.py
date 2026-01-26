from __future__ import annotations

import logging

from app.config import PlatformContent, settings
from app.publishers.base import PublishResult, Publisher

logger = logging.getLogger(__name__)


class StubPublisher(Publisher):
    token_name: str

    def __init__(self, platform: str, token_name: str):
        self.platform = platform
        self.token_name = token_name

    def publish(self, content: PlatformContent) -> PublishResult:
        token_value = getattr(settings, self.token_name)
        if not token_value:
            logger.info("Dry-run publish for %s", self.platform)
            return PublishResult(status="published", url="dry-run://" + self.platform, dry_run=True)
        logger.info("Publishing to %s with token %s", self.platform, self.token_name)
        return PublishResult(status="published", url=f"https://{self.platform}.example.com/post/123")


def get_publishers() -> dict[str, Publisher]:
    return {
        "linkedin": StubPublisher("linkedin", "linkedin_token"),
        "habr": StubPublisher("habr", "habr_token"),
        "zen": StubPublisher("zen", "zen_token"),
        "zakon": StubPublisher("zakon", "zakon_token"),
        "blog": StubPublisher("blog", "blog_token"),
    }
