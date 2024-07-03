import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chat_routes, task_routes, test_routes

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])
app.include_router(task_routes.router, prefix="/api/tasks", tags=["Task"])
app.include_router(test_routes.router, prefix="/api/test", tags=["test"])
