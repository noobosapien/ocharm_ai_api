import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import SessionLocal, get_db_session
from app.models import Message
from app.schemas.message_schema import MessageCreate, MessageReturn

logger = logging.getLogger("app")

router = APIRouter()
db = SessionLocal()


@router.post("/", response_model=MessageReturn, status_code=201)
def create_message(message_data: MessageCreate, db: Session = Depends(get_db_session)):
    try:
        new_message = Message(**message_data.model_dump())

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        # change this
        return new_message
    except HTTPException as http_exc:
        logger.error(f"Error while creating message :{http_exc}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
