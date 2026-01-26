from __future__ import annotations

import datetime as dt
import logging

from app.config import PlatformContent
from app.db import SessionLocal
from app.models import Post, Publication
from app.pipeline.adaptation import adapt_content
from app.publishers.stubs import get_publishers
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
PLATFORMS = ["linkedin", "habr", "zen", "zakon", "blog"]


@celery_app.task
def enqueue_publications(post_id: int) -> None:
    session = SessionLocal()
    try:
        post = session.get(Post, post_id)
        if not post:
            logger.warning("Post %s not found", post_id)
            return
        for platform in PLATFORMS:
            content = adapt_content(
                {
                    "raw_text": post.raw_text,
                    "title": None,
                    "media_json": post.media_json,
                },
                platform,
            )
            publication = Publication(
                post_id=post.id,
                platform=platform,
                status="queued",
                payload={"title": content.title, "body": content.body, "meta": content.meta},
                updated_at=dt.datetime.utcnow(),
            )
            session.add(publication)
        session.commit()
    finally:
        session.close()


@celery_app.task
def publish_publication(publication_id: int) -> None:
    session = SessionLocal()
    publication: Publication | None = None
    try:
        publication = session.get(Publication, publication_id)
        if not publication:
            logger.warning("Publication %s not found", publication_id)
            return
        publication.status = "processing"
        publication.attempts += 1
        publication.updated_at = dt.datetime.utcnow()
        session.commit()

        publishers = get_publishers()
        publisher = publishers[publication.platform]
        content = publication.payload
        platform_content = PlatformContent(
            platform=publication.platform,
            title=content.get("title", ""),
            body=content.get("body", ""),
            meta=content.get("meta", {}),
        )
        result = publisher.publish(platform_content)
        publication.status = result.status
        publication.url = result.url
        publication.error = result.error
        publication.updated_at = dt.datetime.utcnow()
        session.commit()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to publish")
        if publication:
            publication.status = "failed"
            publication.error = str(exc)
            publication.updated_at = dt.datetime.utcnow()
            session.commit()
    finally:
        session.close()


@celery_app.task
def process_telegram_message(post_id: int) -> None:
    enqueue_publications(post_id)
    session = SessionLocal()
    try:
        publications = session.query(Publication).filter_by(post_id=post_id).all()
        for publication in publications:
            publish_publication.delay(publication.id)
    finally:
        session.close()
