from itertools import count

id_counter = count(start=1)


class Message:
    def __init__(
        self,
        id_: int,
        user_id: int,
        content: str,
        additional: str,
        conversation_id: int,
    ):
        self.id = id_
        self.user_id = user_id
        self.content = content
        self.additional = additional
        self.conversation_id = conversation_id


def get_random_message_dict(id_: int = None):
    id_counter = count(1)
    id_ = next(id_counter)

    return {
        "id": id_,
        "user_id": 1,
        "content": "What are the tasks for today?",
        "additional": "",
        "conversation_id": 1,
    }
