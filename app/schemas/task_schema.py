from pydantic import BaseModel, StringConstraints  # noqa
from typing import Annotated, Optional, List  # noqa
import datetime


class TaskBase(BaseModel):
    name: str
    description: str
    severity: str
    time: datetime.datetime
