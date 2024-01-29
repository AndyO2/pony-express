from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_get_chat_messages_invalid_id():
    """Test response for `GET /chats/invalid_id/messages."""
    invalid_id = "invalid_id"

    response = client.get(f"/chats/{invalid_id}/messages")

    assert response.status_code == 404
