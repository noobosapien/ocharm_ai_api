from app.schemas.message_schema import MessageCreate  # noqa
import pytest  # noqa
from pydantic import ValidationError  # noqa
from app.models import Message  # noqa
from fastapi import HTTPException  # noqa
from tests.factories.models_factory import get_random_message_dict


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


def test_unit_schema_message_validation():
    valid_data = {"user_id": 1, "content": "what are the tasks for today?"}
    message = MessageCreate(**valid_data)

    assert message.user_id == 1
    assert message.content == "what are the tasks for today?"
    assert message.conversation_id == 0

    invalid_data = {"user": 1}
    with pytest.raises(ValidationError):
        MessageCreate(**invalid_data)


def test_unit_create_new_message_succesfully(client, monkeypatch):
    message = get_random_message_dict()

    for key, value in message.items():
        monkeypatch.setattr(Message, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output())

    body = message.copy()
    body.pop("id")

    response = client.post("api/chat", json=body)

    assert response.status_code == 201
    assert response.json() == message


def test_unit_create_new_message_with_internal_server_error(client, monkeypatch):
    message = get_random_message_dict()

    def mock_create_message_exception(*args, **kwargs):
        raise Exception("Internal server error")

    for key, value in message.items():
        monkeypatch.setattr(Message, key, value)

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_create_message_exception)

    body = message.copy()
    body.pop("id")
    response = client.post("api/chat", json=body)

    assert response.status_code == 500
