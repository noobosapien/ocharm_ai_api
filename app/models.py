from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
)

from .db_connection import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    associated = Column(
        "associated", ForeignKey("user.id"), ARRAY(Integer), nullable=True
    )
    role = Column(
        Enum("primary", "secondary", name="role_enum"),
        nullable=False,
        server_default="primary",
    )

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="user_name_length_check"),
    )
