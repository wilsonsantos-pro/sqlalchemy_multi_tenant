# pylint: disable=redefined-outer-name
from typing import TYPE_CHECKING, Generator

import pytest

from sqlalchemy_multi_tenant.core.db.session import dbsession_ctx
from sqlalchemy_multi_tenant.items import crud_items as crud
from sqlalchemy_multi_tenant.items.adapters import ItemCreate, ItemUpdate
from sqlalchemy_multi_tenant.items.models import Item
from sqlalchemy_multi_tenant.users.models import User

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


@pytest.fixture
def user(dbsession) -> User:
    return dbsession.query(User).first()


@pytest.fixture
def test_item(dbsession, user) -> Generator[Item, None, None]:
    item_in = ItemCreate(title="ARst", description="qwfpluyar naiers qwfon oa")
    yield crud.items.create_with_owner(
        dbsession=dbsession, obj_in=item_in, owner_id=user.id
    )


@pytest.fixture(autouse=True)
def cleanup(dbsession):
    yield
    dbsession.execute("DELETE from item")
    dbsession.commit()


def test_get_items(client: "TestClient", headers, test_item):
    response = client.get("/api/items", headers=headers)
    assert response.status_code == 200, response.json()
    result = response.json()
    assert len(result) == 1
    assert result[0]["title"] == test_item.title


def test_create_items(client: "TestClient", headers):
    item_in = ItemCreate(title="eonopqw", description="qwfpluyar naiers qwfon oa")
    response = client.post("/api/items", headers=headers, json=item_in.dict())
    assert response.status_code == 200, response.json()
    result = response.json()
    assert result["title"] == item_in.title


def test_update_items(client: "TestClient", headers, test_item):
    item_in = ItemUpdate(title="New title", description="New description")
    response = client.put(
        f"/api/items/{test_item.id}", headers=headers, json=item_in.dict()
    )
    assert response.status_code == 200, response.json()
    result = response.json()
    assert result["title"] == item_in.title
    assert result["description"] == item_in.description


def test_delete_items(client: "TestClient", headers, test_item):
    item_id = test_item.id
    response = client.delete(f"/api/items/{item_id}", headers=headers)
    assert response.status_code == 200, response.json()
