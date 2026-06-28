from fastapi import FastAPI, HTTPException
from models.task import Task, TaskRequest, TaskUpdate

app = FastAPI()

# temporary in-memory story
tasks: list[Task] = []
id_counter = 1


def find_task_by_id(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/")
async def root():
    return {"message": "StudentTask API is running."}


@app.post("/tasks")
def create_task(request: TaskRequest) -> Task:
    global id_counter

    new_task = Task(
        id=id_counter,
        title=request.title
    )

    id_counter += 1

    tasks.append(new_task)

    return new_task


@app.get("/tasks")
def get_all_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int) -> Task:
    return find_task_by_id(task_id)


@app.put("/tasks/{task_id}")
def update_task_by_id(task_id: int, update: TaskUpdate):
    updated_task = find_task_by_id(task_id)
    updated_task.title = update.title
    updated_task.completed = update.completed

    return updated_task
