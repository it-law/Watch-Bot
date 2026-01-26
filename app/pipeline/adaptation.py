from __future__ import annotations

from app.config import PlatformContent
from app.pipeline.normalization import build_slug, extract_links, generate_title, media_fallback, normalize_text


def adapt_content(post: dict, platform: str) -> PlatformContent:
    raw_text = normalize_text(post.get("raw_text") or "")
    title = post.get("title") or generate_title(raw_text)
    links = extract_links(raw_text)
    media_note = media_fallback(post.get("media_json") or {})

    if platform == "linkedin":
        hook = title if len(title) < 120 else title[:117] + "…"
        body = raw_text
        if len(body) > 1700:
            body = body[:1690].rstrip() + "…"
        hashtags = ["#law", "#legaltech", "#insights", "#telegram", "#automation"]
        content = f"{hook}\n\n{body}"
        if media_note:
            content += f"\n\nMedia: {media_note}"
        content += f"\n\n{' '.join(hashtags[:5])}"
        return PlatformContent(platform=platform, title=title, body=content, hashtags=hashtags[:5])

    if platform == "habr":
        intro = raw_text[:400] + ("…" if len(raw_text) > 400 else "")
        body = (
            f"# {title}\n\n"
            f"{intro}\n\n"
            "## Ключевые тезисы\n"
            "- Тезис 1\n"
            "- Тезис 2\n\n"
            "## Детали\n"
            f"{raw_text}\n\n"
            "## Вывод\n"
            "Нейтральный вывод без агрессивных призывов."
        )
        if links:
            body += "\n\nПолезные ссылки:\n" + "\n".join(f"- {link}" for link in links)
        if media_note:
            body += f"\n\nMedia: {media_note}"
        return PlatformContent(platform=platform, title=title, body=body)

    if platform == "zen":
        story = raw_text
        body = f"{title}\n\n{story}"
        if links:
            body += "\n\nСсылки: " + ", ".join(links)
        body += "\n\nКак вы считаете, применима ли эта практика в вашем кейсе?"
        return PlatformContent(platform=platform, title=title, body=body)

    if platform == "zakon":
        body = raw_text
        if links:
            body += "\n\nСсылки на нормы/практику:\n" + "\n".join(links)
        body = body.replace("!!!", "")
        if media_note:
            body += f"\n\nMedia: {media_note}"
        return PlatformContent(platform=platform, title=title, body=body)

    if platform == "blog":
        description = raw_text[:160] + ("…" if len(raw_text) > 160 else "")
        slug = build_slug(title)
        body = f"# {title}\n\n{raw_text}"
        if links:
            body += "\n\n## Ссылки\n" + "\n".join(f"- {link}" for link in links)
        if media_note:
            body += f"\n\nMedia: {media_note}"
        meta = {"seo_title": title, "description": description, "slug": slug}
        return PlatformContent(platform=platform, title=title, body=body, meta=meta)

    raise ValueError(f"Unsupported platform: {platform}")
