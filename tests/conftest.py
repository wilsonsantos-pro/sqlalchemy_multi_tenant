# pylint: disable=redefined-outer-name,unused-argument
from typing import Dict, Generator

import pytest
from alembic import command
from alembic import config as alembic_config
from fastapi.testclient import TestClient
from pydantic import EmailStr

from sqlalchemy_multi_tenant import config
from sqlalchemy_multi_tenant.auth import create_access_token
from sqlalchemy_multi_tenant.core.db.session import dbsession_ctx, get_engine
from sqlalchemy_multi_tenant.core.orm.mapper import start_orm_mappers
from sqlalchemy_multi_tenant.main import main
from sqlalchemy_multi_tenant.users.init_db import init_db


@pytest.fixture(scope="session")
def client(test_init_db) -> TestClient:
    app = main(start_orm_mappers=False)
    return TestClient(app)


@pytest.fixture
def user_email() -> EmailStr:
    return EmailStr("admin@admin.com")


@pytest.fixture
def headers(user_email: EmailStr) -> Dict[str, str]:
    token = create_access_token(user_email)
    return {"Authorization": f"bearer {token}"}


@pytest.fixture
def dbsession() -> Generator:
    with dbsession_ctx() as _dbsession:
        yield _dbsession


@pytest.fixture(autouse=True, scope="session")
def test_init_db() -> None:
    alembic_cfg = alembic_config.Config("alembic.ini")
    with get_engine().begin():
        command.upgrade(alembic_cfg, "head")
    start_orm_mappers()
    with dbsession_ctx() as _dbsession:
        init_db(_dbsession)


def pytest_sessionstart(
    session: pytest.Session,  # pylint: disable=unused-argument
) -> None:
    test_settings = config.Settings(_env_file=".env.test")
    setattr(config, "settings", test_settings)
    setattr(config, "settings", test_settings)
