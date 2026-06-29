from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.schemas.task import TaskRequest, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task_by_id,
    find_task_by_id,
    get_all_tasks,
    update_task_by_id,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create(request: TaskRequest, session: Session = Depends(get_session)) -> TaskResponse:
    return create_task(session, request)


@router.get("", response_model=list[TaskResponse])
def read_all(session: Session = Depends(get_session)) -> list[TaskResponse]:
    return get_all_tasks(session)


@router.get("/{task_id}", response_model=TaskResponse)
def read_one(task_id: int, session: Session = Depends(get_session)) -> TaskResponse:
    return find_task_by_id(session, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update(
    task_id: int, request: TaskUpdate, session: Session = Depends(get_session)
) -> TaskResponse:
    return update_task_by_id(session, task_id, request)


@router.delete("/{task_id}")
def delete(task_id: int, session: Session = Depends(get_session)) -> dict:
    return delete_task_by_id(session, task_id)
