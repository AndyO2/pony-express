from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# User Endpoint Tests
def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200


def test_get_user_chats():
    response = client.get("/users/bishop/chats")
    expected_response = {
        "meta": {
            "count": 1
        },
        "chats": [
            {
                "id": "734eeb9ddaec43b2ab6e289a0d472376",
                "name": "nostromo",
                "user_ids": ["bishop", "burke", "ripley"],
                "owner_id": "ripley",
                "created_at": "2023-09-18T14:18:46"
            }
        ]
    }
    assert response.status_code == 200
    assert response.json() == expected_response
