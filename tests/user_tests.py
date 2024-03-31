from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# User Endpoint Tests
def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])


def test_create_user(client):
    create_params = {
        "id": "bob",
    }
    response = client.post("/users", json=create_params)
    assert response.status_code == 200

    data = response.json()
    assert "user" in data
    user = data["user"]
    for key, value in create_params.items():
        assert user[key] == value

    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    user = data["user"]
    for key, value in create_params.items():
        assert user[key] == value


def test_create_user_duplicate(client):
    create_params = {
        "id": "bishop",
    }
    response = client.post("/users", json=create_params)
    assert response.status_code == 422


def test_get_user(client):
    user_id = "bishop"
    expected_user = {
        "id": user_id,
        "created_at": "2014-04-14T10:49:07",
    }
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"user": expected_user}


def test_get_user_invalid_id():
    user_id = "invalid_id"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


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


def test_get_user_chats_invalid_id():
    invalid_user_id = "invalid_id"
    response = client.get(f"/users/{invalid_user_id}/chats")
    assert response.status_code == 404
