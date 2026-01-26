from __future__ import annotations

from fastapi import FastAPI

from app.api import admin, telegram
from app.db import init_db
from app.utils.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    init_db()
    app = FastAPI(title="Telegram Multichannel Pipeline")
    app.include_router(admin.router)
    app.include_router(telegram.router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
