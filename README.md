# Student Task API

A simple task-management REST API built with FastAPI and PostgreSQL, created to learn backend fundamentals and professional software engineering practices.

The project follows a layered architecture where HTTP routes delegate to a service layer, which is the single point of access to the database.

```
Routes (task_routes.py) -> Services (task_service.py) -> SQLAlchemy Session -> PostgreSQL
```

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.0 (typed ORM) on PostgreSQL via the `postgresql+psycopg://` (psycopg 3) dialect
- Alembic (database migrations)
- Docker / Docker Compose (local database)
- Uvicorn (ASGI server)
- pytest (automated tests)

## Project Structure

```
student-task-api/
├── app/
│   ├── database/
│   │   └── database.py        # Engine, session factory, Base, get_session
│   ├── models/
│   │   └── task.py            # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── task.py            # Pydantic request/response schemas
│   ├── routes/
│   │   └── task_routes.py     # APIRouter with task endpoints
│   ├── services/
│   │   └── task_service.py    # Business logic (ORM session operations)
│   └── main.py                # FastAPI app: wiring and router registration
├── alembic/
│   ├── env.py                 # Migration environment (reads DATABASE_URL)
│   └── versions/              # Migration scripts
├── alembic.ini                # Alembic configuration
├── db/
│   └── init/                  # SQL run on first DB container start
├── tests/
│   ├── conftest.py            # Shared fixtures (isolated test database)
│   └── test_tasks.py          # API endpoint tests
├── docker-compose.yml         # Local PostgreSQL service
├── .env.example
├── pytest.ini
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (for the local PostgreSQL database)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd student-task-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy the example environment file
cp .env.example .env
```

### Start PostgreSQL

The project ships with a Docker Compose file that runs PostgreSQL 16 and, on
first start, creates a separate database used by the test suite.

```bash
docker compose up -d
```

This exposes PostgreSQL on `localhost:5432` with two databases:

- `student_tasks` — used by the application
- `student_tasks_test` — used by the automated tests

To stop it (data is preserved in a named volume):

```bash
docker compose down
```

### Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. For local convenience the
`tasks` table is created automatically on startup if it does not already exist;
the canonical way to manage the schema is Alembic migrations (see below).

### Configuration

Configuration is read from environment variables (a local `.env` file is loaded
automatically). See [.env.example](.env.example).

| Variable            | Default                                                       | Description                                       |
|---------------------|---------------------------------------------------------------|---------------------------------------------------|
| `DATABASE_URL`      | `postgresql://postgres:postgres@localhost:5432/student_tasks` | Connection string for the application database.   |
| `TEST_DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/student_tasks_test` | Connection string used by the test suite.    |

### Interactive Documentation

FastAPI generates interactive API docs automatically:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Path               | Description            | Request Body                         | Success Response          |
|--------|--------------------|------------------------|--------------------------------------|---------------------------|
| GET    | `/`                | Health check           | -                                    | `200` status message      |
| POST   | `/tasks`           | Create a task          | `{ "title": "string" }`              | `201` created task        |
| GET    | `/tasks`           | List all tasks         | -                                    | `200` array of tasks      |
| GET    | `/tasks/{task_id}` | Get a single task      | -                                    | `200` task / `404`        |
| PUT    | `/tasks/{task_id}` | Update a task          | `{ "title": "string", "completed": bool }` | `200` updated task / `404` |
| DELETE | `/tasks/{task_id}` | Delete a task          | -                                    | `200` message / `404`     |

### Data Model

A task is represented as:

```json
{
  "id": 1,
  "title": "Study SQL",
  "completed": false
}
```

### Example Requests

```bash
# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Study SQL"}'

# List all tasks
curl http://127.0.0.1:8000/tasks

# Update a task
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Study SQL", "completed": true}'

# Delete a task
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Database Migrations

The database schema is managed with [Alembic](https://alembic.sqlalchemy.org/).
Alembic reads the same `DATABASE_URL` as the application (normalized to the
`postgresql+psycopg://` dialect) and uses the ORM models' metadata as the source
of truth for autogeneration.

```bash
# Apply all migrations to bring the database up to date
alembic upgrade head

# Autogenerate a new migration after changing the ORM models
alembic revision --autogenerate -m "describe your change"

# Inspect/roll back history
alembic current
alembic downgrade -1
```

> If a database already contains the schema (for example from an earlier phase),
> mark it as up to date without re-running DDL with `alembic stamp head`.

The test suite does not run migrations; it builds the schema directly via
`Base.metadata.create_all` for speed and isolation.

## Testing

The test suite uses `pytest` with FastAPI's `TestClient`. Tests run against the
dedicated `student_tasks_test` database and truncate the `tasks` table before each
test, so they are isolated and never touch development data.

Make sure PostgreSQL is running (`docker compose up -d`), then:

```bash
# Run the full suite
pytest

# Run with extra detail / a specific test
pytest -v
pytest tests/test_tasks.py::test_create_task
```

## Roadmap

- [x] CRUD operations with in-memory storage
- [x] Service layer architecture
- [x] SQLite-backed persistence with raw SQL
- [x] Extract routes into dedicated route modules
- [x] Automated test suite with pytest
- [x] Migrate to PostgreSQL with environment-based configuration
- [x] Introduce SQLAlchemy ORM and migrations
- [ ] Containerization and cloud deployment

## Contributing

This project uses the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages, for example:

```
feat(tasks): add task completion filtering
fix(database): close connection on error paths
docs: document API endpoints in README
```
