from __future__ import annotations

import re
from typing import Any


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned


def extract_links(text: str) -> list[str]:
    return re.findall(r"https?://\S+", text)


def generate_title(text: str) -> str:
    if not text:
        return "Новый материал из Telegram"
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    first_line = lines[0] if lines else text
    if len(first_line) > 90:
        return first_line[:87].rstrip() + "…"
    return first_line


def build_slug(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", title)
    slug = re.sub(r"\s+", "-", slug).strip("-").lower()
    return slug or "telegram-post"


def media_fallback(media_json: dict[str, Any]) -> str | None:
    if not media_json:
        return None
    if "urls" in media_json and media_json["urls"]:
        return ", ".join(media_json["urls"])
    if "description" in media_json:
        return media_json["description"]
    return None
