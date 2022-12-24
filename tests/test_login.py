from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_login(client: "TestClient"):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    data = {"username": "admin@admin.com", "password": "admin@admin.com"}
    response = client.post("/api/login", headers=headers, data=data)
    assert response.status_code == 200, response.json()
    assert "access_token" in response.json()
