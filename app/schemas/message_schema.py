from pydantic import BaseModel, StringConstraints  # noqa
from typing import Annotated, Optional  # noqa


class MessageBase(BaseModel):
    user_id: int
    content: Annotated[str, StringConstraints(min_length=1)]
    additional: Optional[str] = ""
    conversation_id: Optional[int] = 1
    message_role: str = "human"


class MessageCreate(MessageBase):
    pass


class MessageReturn(BaseModel):
    content: Annotated[str, StringConstraints(min_length=1)]
