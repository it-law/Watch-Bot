from __future__ import annotations

import json

from app.db import SessionLocal, init_db
from app.models import Post
from app.pipeline.adaptation import adapt_content
from app.workers.tasks import enqueue_publications


def main() -> None:
    init_db()
    session = SessionLocal()
    try:
        post = Post(
            tg_message_id="demo-1",
            raw_text="Новый кейс: как автоматизация помогает юристам. Подробнее: https://example.com",
            raw_json={"demo": True},
            media_json={"urls": ["https://example.com/image.png"]},
        )
        session.add(post)
        session.commit()
        session.refresh(post)

        enqueue_publications(post.id)

        adaptations = {}
        for platform in ["linkedin", "habr", "zen", "zakon", "blog"]:
            content = adapt_content(
                {"raw_text": post.raw_text, "title": None, "media_json": post.media_json},
                platform,
            )
            adaptations[platform] = content.dict()

        print(json.dumps(adaptations, ensure_ascii=False, indent=2))
    finally:
        session.close()


if __name__ == "__main__":
    main()
