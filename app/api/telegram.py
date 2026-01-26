from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.config import settings
from app.models import Post
from app.pipeline.normalization import normalize_text
from app.workers.tasks import process_telegram_message

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


def verify_webhook(secret_token: str | None = Header(default=None, alias="X-Telegram-Bot-Api-Secret-Token")) -> None:
    if settings.telegram_webhook_secret and secret_token != settings.telegram_webhook_secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid webhook token")


def extract_media(message: dict[str, Any]) -> dict[str, Any]:
    media: dict[str, Any] = {}
    if "photo" in message:
        media["photos"] = message["photo"]
    if "video" in message:
        media["video"] = message["video"]
    if "document" in message:
        media["document"] = message["document"]
    if "media_group_id" in message:
        media["album_id"] = message["media_group_id"]
    return media


@router.post("/webhook")
def telegram_webhook(
    update: dict[str, Any],
    db: Session = Depends(get_db),
    _auth: None = Depends(verify_webhook),
) -> dict[str, str]:
    message = update.get("channel_post") or update.get("message")
    if not message:
        return {"status": "ignored"}

    raw_text = normalize_text(message.get("text") or message.get("caption") or "")
    post = Post(
        tg_message_id=str(message.get("message_id")),
        raw_text=raw_text,
        raw_json=update,
        media_json=extract_media(message),
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    logger.info("Received telegram message %s", post.id)
    process_telegram_message.delay(post.id)
    return {"status": "accepted"}
