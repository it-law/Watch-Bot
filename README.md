# Telegram → мультиканал контент-завод (MVP)

Production-ready MVP для автоматизации публикаций из Telegram-канала в несколько площадок.

## Архитектура

**Flow**
1. Telegram webhook принимает новый пост.
2. Нормализация текста/медиа.
3. Генерация адаптаций под платформы.
4. Запись публикаций со статусом `queued`.
5. Celery воркеры публикуют или работают в `dry-run` (если нет токена).

**Платформы**: LinkedIn, Habr, Яндекс.Дзен, Zakon.ru, сайт-блог.

## Структура репозитория
```
app/
  api/                 # FastAPI роуты
  pipeline/            # нормализация и адаптация
  publishers/          # интерфейс и stub-паблишеры
  workers/             # Celery задачи
  utils/               # логирование
scripts/
  demo_scenario.py     # сквозной пример
tests/
  test_adaptation.py   # unit-тесты
```

## Быстрый старт

1. Создайте `.env` на базе примера:
   ```bash
   cp .env.example .env
   ```
2. Запуск через Docker:
   ```bash
   docker-compose up --build
   ```
3. API доступно на `http://localhost:8000`.

## Основные эндпоинты

- `POST /telegram/webhook` — webhook для Telegram.
- `GET /admin/posts` — список постов (Basic Auth).
- `GET /admin/publications` — список публикаций (Basic Auth).
- `POST /admin/publications/{id}/retry` — повторная публикация.
- `GET /health` — проверка.

## Как работает dry-run
Если токены платформ не заданы, публикации выполняются в dry-run режиме:
- статус `published`
- ссылка вида `dry-run://platform`
- запись сохраняется в БД и логи.

## Сквозной сценарий (пример)
Запустите скрипт:
```bash
python scripts/demo_scenario.py
```
Он создаст тестовый Telegram пост, сгенерирует 5 адаптаций и запишет статусы в БД.

## Тесты
```bash
pytest
```

## Типизация и линтер
- Настройки `mypy` и `ruff` находятся в `pyproject.toml`.

## Настройка Telegram
Используйте webhook от Bot API и укажите `TELEGRAM_WEBHOOK_SECRET` для защиты.

## Поддержка медиа
- Фото/видео/документы сохраняются в `media_json`.
- Если платформа не поддерживает медиа, добавляется ссылка/описание.
