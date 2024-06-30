from typing import List  # noqa

from langchain.schema import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from app.utils.database_api import (
    get_messages_by_conversation_id,
    add_message_to_conversation,
)


class SQLMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: int

    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self, message: BaseMessage) -> None:
        return add_message_to_conversation(conversation_id=1, role="", content="")

    def clear(self) -> None:
        pass


SQLMessageHistory.model_rebuild()
