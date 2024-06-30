from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage

from app.db_connection import SessionLocal
from app.models import Message

db = SessionLocal()


def get_messages_by_conversation_id(
    conversation_id,
) -> AIMessage | HumanMessage | SystemMessage:
    messages = (
        db.query(Message).filter(Message.conversation_id == conversation_id).all()
    )

    return [message.as_lc_message() for message in messages]


def add_message_to_conversation(conversation_id: int, role: str, content: str):
    message: Message = None

    match role:
        case "human":
            pass
        case "ai":
            pass
        case "system":
            pass
        case _:
            raise Exception(f"Undefined message_role{role}")

    message = Message(
        conversation_id=conversation_id, content=content, message_role=role, user_id=1
    )

    db.add(message)
    db.commit()
    db.refresh(message)
