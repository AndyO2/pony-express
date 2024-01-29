from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_get_chats():
    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])


def test_get_chat_messages_invalid_id():
    """Test response for `GET /chats/invalid_id/messages."""
    invalid_id = "invalid_id"

    response = client.get(f"/chats/{invalid_id}/messages")

    assert response.status_code == 404


def test_get_chat_messages_valid_id():
    """Test response for `GET /chats/invalid_id/messages."""
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2/messages")
    meta = response.json()["meta"]
    messages = response.json()["messages"]

    assert len(messages) == meta["count"]
    assert response.status_code == 200


def test_get_chat_users():
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2/users")
    meta = response.json()["meta"]
    users = response.json()["users"]

    assert len(users) == meta["count"]
    assert response.status_code == 200


def test_get_chat_by_id():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    response = client.get(f"/chats/{chat_id}")
    expected_response = {
        "chat": {
            "id": "6215e6864e884132baa01f7f972400e2",
            "name": "skynet",
            "user_ids": ["sarah", "terminator"],
            'owner_id': 'sarah',
            'created_at': '2023-07-08T18:46:47'
        }
    }

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_chat_by_invalid_id():
    response = client.get("/chats/invalid_id")
    assert response.status_code == 404


def test_update_chat():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    update_params = {
        "name": "test"
    }
    expected_chat = {
        "id": "6215e6864e884132baa01f7f972400e2",
        "name": "test",
        "user_ids": ["sarah", "terminator"],
        'owner_id': 'sarah',
        'created_at': '2023-07-08T18:46:47'
    }

    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}

    # test that the update is persisted
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}


def test_delete_chat_invalid_id():
    response = client.delete("/chats/invalid_id")
    assert response.status_code == 404


def test_delete_chat():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204
    assert response.content == b""

    # test that the delete is persisted
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id,
        },
    }
