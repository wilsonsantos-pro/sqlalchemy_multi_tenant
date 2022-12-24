from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_get_users(client: "TestClient", headers):
    response = client.get("/api/users", headers=headers)
    assert response.status_code == 200, response.json()
    result = response.json()
    assert len(result) == 1
    assert result[0]["email"] == "admin@admin.com"
