from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskRequest, TaskUpdate


def create_task(session: Session, request: TaskRequest) -> Task:
    task = Task(title=request.title, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_all_tasks(session: Session) -> list[Task]:
    return list(session.scalars(select(Task).order_by(Task.id)).all())


def find_task_by_id(session: Session, task_id: int) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task_by_id(session: Session, task_id: int, update: TaskUpdate) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = update.title
    task.completed = update.completed
    session.commit()
    session.refresh(task)
    return task


def delete_task_by_id(session: Session, task_id: int) -> dict:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
