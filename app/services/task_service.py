from fastapi import HTTPException
from app.models.task import Task, TaskRequest, TaskUpdate

# temporary in-memory story
tasks: list[Task] = []
id_counter = 1


def create_task(request: TaskRequest) -> Task:
    global id_counter

    new_task = Task(
        id=id_counter,
        title=request.title
    )

    id_counter += 1

    tasks.append(new_task)

    return new_task


def get_all_tasks():
    return tasks


def find_task_by_id(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


def update_task_by_id(task_id: int, update: TaskUpdate):
    updated_task = find_task_by_id(task_id)
    updated_task.title = update.title
    updated_task.completed = update.completed

    return updated_task


def delete_task_by_id(task_id: int):
    deleted_task = find_task_by_id(task_id)
    tasks.remove(deleted_task)

    return {"message": "Task deleted successfully"}
