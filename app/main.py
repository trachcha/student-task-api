from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import initialize_db
from app.routes.auth_routes import router as auth_router
from app.routes.subject_routes import router as subject_router
from app.routes.subtask_routes import router as subtask_router
from app.routes.task_routes import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(title="Student Task API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(subject_router)
app.include_router(task_router)
app.include_router(subtask_router)


@app.get("/", tags=["health"])
def root():
    return {"message": "StudentTask API is running"}
