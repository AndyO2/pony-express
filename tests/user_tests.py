from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# User Endpoint Tests
def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
