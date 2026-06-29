from fastapi import APIRouter, status

from app.models.task import Task, TaskRequest, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task_by_id,
    find_task_by_id,
    get_all_tasks,
    update_task_by_id,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create(request: TaskRequest) -> Task:
    return create_task(request)


@router.get("", response_model=list[Task])
def read_all() -> list[Task]:
    return get_all_tasks()


@router.get("/{task_id}", response_model=Task)
def read_one(task_id: int) -> Task:
    return find_task_by_id(task_id)


@router.put("/{task_id}", response_model=Task)
def update(task_id: int, request: TaskUpdate) -> Task:
    return update_task_by_id(task_id, request)


@router.delete("/{task_id}")
def delete(task_id: int) -> dict:
    return delete_task_by_id(task_id)
