# Student Task API

A simple task-management REST API built with FastAPI and PostgreSQL, created to learn backend fundamentals and professional software engineering practices.

The project follows a layered architecture where HTTP routes delegate to a service layer, which is the single point of access to the database.

```
Routes (task_routes.py) -> Services (task_service.py) -> PostgreSQL (psycopg pool)
```

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL (raw SQL via `psycopg` 3 with a connection pool)
- Docker / Docker Compose (local database)
- Uvicorn (ASGI server)
- pytest (automated tests)

## Project Structure

```
student-task-api/
├── app/
│   ├── database/
│   │   └── database.py        # Connection pool + schema initialization
│   ├── models/
│   │   └── task.py            # Pydantic request/response models
│   ├── routes/
│   │   └── task_routes.py     # APIRouter with task endpoints
│   ├── services/
│   │   └── task_service.py    # Business logic + SQL queries
│   └── main.py                # FastAPI app: wiring and router registration
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

The API will be available at `http://127.0.0.1:8000`. The `tasks` table is created
automatically on startup if it does not already exist.

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
- [ ] Introduce SQLAlchemy ORM and migrations
- [ ] Containerization and cloud deployment

## Contributing

This project uses the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages, for example:

```
feat(tasks): add task completion filtering
fix(database): close connection on error paths
docs: document API endpoints in README
```
