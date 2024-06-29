from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP

from .db_connection import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    # associated = Column(
    #     "associated", ForeignKey("user.id"), ARRAY(Integer), nullable=True
    # )
    role = Column(
        Enum("primary", "secondary", name="role_enum"),
        nullable=False,
        server_default="primary",
    )

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="user_name_length_check"),
    )


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)
    additional = Column(Text, nullable=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(content) > 0", name="message_content_length_check"),
    )


class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    time = Column(TIMESTAMP, nullable=False)
    severity = Column(
        Enum("low", "medium", "high", name="severity_enum"),
        nullable=False,
        server_default="low",
    )
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="task_name_length_check"),
    )
