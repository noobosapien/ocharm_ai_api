from typing import List  # noqa

from langchain.schema import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class SQLMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: int

    @property
    def messages(self):
        pass

    def add_message(self, message: BaseMessage) -> None:
        pass

    def clear(self) -> None:
        pass


SQLMessageHistory.model_rebuild()
