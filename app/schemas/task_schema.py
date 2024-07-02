from pydantic import BaseModel, StringConstraints  # noqa
from typing import Annotated, Optional  # noqa


class TaskBase(BaseModel):
    answer: str
    error: Optional[str]
