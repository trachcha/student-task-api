import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/student_tasks_test",
)


@pytest.fixture(scope="session", autouse=True)
def _configure_test_database() -> None:
    """Point the application at the disposable test database for the whole run."""
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provide a TestClient backed by a clean test database.

    Entering the TestClient context runs the app's lifespan handler, which creates
    the schema via ``Base.metadata.create_all``. The ``tasks`` table is then
    truncated so each test starts from an empty database with ids reset to 1.
    """
    from sqlalchemy import text

    from app.database.database import engine
    from app.main import app

    with TestClient(app) as test_client:
        with engine.begin() as connection:
            connection.execute(text("TRUNCATE tasks RESTART IDENTITY"))
        yield test_client
