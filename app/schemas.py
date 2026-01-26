from __future__ import annotations

import datetime as dt
from typing import Any

from pydantic import BaseModel


class PostCreate(BaseModel):
    tg_message_id: str
    raw_text: str | None
    raw_json: dict[str, Any]
    media_json: dict[str, Any]


class PostRead(BaseModel):
    id: int
    tg_message_id: str
    created_at: dt.datetime
    raw_text: str | None
    media_json: dict[str, Any]

    class Config:
        from_attributes = True


class PublicationRead(BaseModel):
    id: int
    post_id: int
    platform: str
    status: str
    url: str | None
    error: str | None
    attempts: int
    updated_at: dt.datetime

    class Config:
        from_attributes = True
