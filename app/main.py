import logging
import logging.config

from fastapi import FastAPI

from app.routers import chat_routes, test_routes

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])
app.include_router(test_routes.router, prefix="/api/test", tags=["test"])
