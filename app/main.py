from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import close_pool, initialize_db, open_pool
from app.routes.task_routes import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_pool()
    initialize_db()
    yield
    close_pool()


app = FastAPI(title="Student Task API", lifespan=lifespan)

app.include_router(task_router)


@app.get("/", tags=["health"])
def root():
    return {"message": "StudentTask API is running"}
