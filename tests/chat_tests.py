from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_get_chat_messages_invalid_id():
    """Test response for `GET /chats/invalid_id/messages."""
    invalid_id = "invalid_id"

    response = client.get(f"/chats/{invalid_id}/messages")

    assert response.status_code == 404


def test_get_chat_messages_valid_id():
    """Test response for `GET /chats/invalid_id/messages."""
    response = client.get(f"/chats/6215e6864e884132baa01f7f972400e2/messages")

    assert response.status_code == 200


def test_get_chat_users():
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2/users")
    assert response.status_code == 200
