from __future__ import annotations

from app.pipeline.adaptation import adapt_content


def base_post():
    return {
        "raw_text": "Заголовок\n\nОсновной текст с ссылкой https://example.com и выводами.",
        "title": None,
        "media_json": {"urls": ["https://example.com/image.png"]},
    }


def test_linkedin_hashtags_and_hook():
    content = adapt_content(base_post(), "linkedin")
    assert content.body.splitlines()[0]
    assert "#" in content.body
    assert len(content.body) <= 2000


def test_habr_has_markdown_structure():
    content = adapt_content(base_post(), "habr")
    assert content.body.startswith("# ")
    assert "## Вывод" in content.body


def test_zen_is_story_like():
    content = adapt_content(base_post(), "zen")
    assert "Как вы считаете" in content.body


def test_zakon_keeps_links():
    content = adapt_content(base_post(), "zakon")
    assert "https://example.com" in content.body


def test_blog_has_meta():
    content = adapt_content(base_post(), "blog")
    assert content.meta["slug"]
    assert content.meta["description"]
