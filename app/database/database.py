import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/student_tasks"

_pool: ConnectionPool | None = None


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def open_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool(conninfo=get_database_url(), open=True)
    return _pool


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def get_pool() -> ConnectionPool:
    if _pool is None:
        return open_pool()
    return _pool


def initialize_db() -> None:
    with get_pool().connection() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id SERIAL PRIMARY KEY,"
            "title TEXT NOT NULL,"
            "completed BOOLEAN NOT NULL DEFAULT FALSE)"
        )
