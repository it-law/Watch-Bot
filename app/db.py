from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


def _create_engine():
    return create_engine(settings.database_url, future=True)


engine = _create_engine()
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
