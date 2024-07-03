import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import SessionLocal, get_db_session
from app.models import Task
from app.schemas.task_schema import TaskBase  # noqa

logger = logging.getLogger("app")

router = APIRouter()
db = SessionLocal()


@router.get("/", response_model=list[TaskBase], status_code=201)
def get_tasks(db: Session = Depends(get_db_session)):
    try:
        tasks = db.query(Task).all()

        return tasks
    except HTTPException as http_exc:
        logger.error(f"Error while creating message :{http_exc}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
