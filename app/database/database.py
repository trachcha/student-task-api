import os
from collections.abc import Iterator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/student_tasks"


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def _normalize_url(url: str) -> str:
    """Force the psycopg 3 driver, regardless of how the URL is written."""
    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://") :]
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://") :]
    return url


def create_db_engine():
    return create_engine(_normalize_url(get_database_url()), future=True)


engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


def initialize_db() -> None:
    """Create tables for local/dev/test convenience; production uses Alembic."""
    from app import models  # noqa: F401  ensure models are registered on Base

    Base.metadata.create_all(engine)
