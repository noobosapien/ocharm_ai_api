from pydantic import BaseModel, StringConstraints  # noqa
from typing import Annotated, Optional  # noqa


class InitBase(BaseModel):
    user_id: int = 1
    conversation_id: int = 0
