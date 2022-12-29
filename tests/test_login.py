# pylint: disable=redefined-outer-name,unused-argument
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_login_default_user(client: "TestClient"):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    data = {"username": "admin@admin.com", "password": "admin@admin.com"}
    response = client.post("/api/login", headers=headers, data=data)
    assert response.status_code == 200, response.json()
    assert "access_token" in response.json()


@pytest.mark.parametrize("multi_tenant_enabled", [True, False])
def test_login_tenant(
    client: "TestClient",
    patch_multi_tenant_enabled,
    create_tenant_user,
    tenant_username,
    tenant_password,
):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    data = {"username": tenant_username, "password": tenant_password}
    response = client.post("/api/login", headers=headers, data=data)
    assert response.status_code == 200, response.json()
    assert "access_token" in response.json()
