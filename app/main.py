from fastapi import FastAPI

from app.database.database import initialize_db
from app.routes.task_routes import router as task_router

app = FastAPI(title="Student Task API")
initialize_db()

app.include_router(task_router)


@app.get("/", tags=["health"])
def root():
    return {"message": "StudentTask API is running"}
