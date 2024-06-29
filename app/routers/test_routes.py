import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import SessionLocal, get_db_session
from app.models import Conversation, User
from app.schemas.init_schema import InitBase

logger = logging.getLogger("app")

router = APIRouter()
db = SessionLocal()


@router.post("/init", response_model=InitBase, status_code=201)
def create_message(db: Session = Depends(get_db_session)):
    try:
        user = {"name": "test"}

        new_user = User(**user)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        conversation = {"user_id": 1}

        new_conversation = Conversation(**conversation)

        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)

        # change this
        return InitBase()
    except HTTPException as http_exc:
        logger.error(f"Error while creating message :{http_exc}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
