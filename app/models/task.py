from pydantic import BaseModel


class TaskRequest(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str
    completed: bool
