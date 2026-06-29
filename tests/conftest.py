from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch) -> Iterator[TestClient]:
    """Provide a TestClient backed by an isolated, empty SQLite database.

    Each test gets its own temporary database file via ``tmp_path``. The
    ``DATABASE_NAME`` env var is read per-connection in the data layer, and the
    schema is created by the app's lifespan handler when the TestClient context
    is entered.
    """
    db_path = tmp_path / "test_tasks.db"
    monkeypatch.setenv("DATABASE_NAME", str(db_path))

    with TestClient(app) as test_client:
        yield test_client
