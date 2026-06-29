from fastapi import HTTPException

from app.database.database import get_pool
from app.models.task import Task, TaskRequest, TaskUpdate


def _row_to_task(row: tuple) -> Task:
    return Task(id=row[0], title=row[1], completed=bool(row[2]))


def create_task(request: TaskRequest) -> Task:
    with get_pool().connection() as connection:
        row = connection.execute(
            "INSERT INTO tasks (title, completed) VALUES (%s, %s) "
            "RETURNING id, title, completed",
            (request.title, False),
        ).fetchone()

    return _row_to_task(row)


def get_all_tasks() -> list[Task]:
    with get_pool().connection() as connection:
        rows = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id"
        ).fetchall()

    return [_row_to_task(row) for row in rows]


def find_task_by_id(task_id: int) -> Task:
    with get_pool().connection() as connection:
        row = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = %s",
            (task_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return _row_to_task(row)


def update_task_by_id(task_id: int, update: TaskUpdate) -> Task:
    with get_pool().connection() as connection:
        row = connection.execute(
            "UPDATE tasks SET title = %s, completed = %s WHERE id = %s "
            "RETURNING id, title, completed",
            (update.title, update.completed, task_id),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return _row_to_task(row)


def delete_task_by_id(task_id: int) -> dict:
    with get_pool().connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
