# pylint: disable=redefined-outer-name,unused-argument,import-outside-toplevel
from typing import Generator

import pytest

from sqlalchemy_multi_tenant.core.db.session import dbsession_ctx_for_tenant
from sqlalchemy_multi_tenant.tenant.crud_tenant import tenant as crud_tenant
from sqlalchemy_multi_tenant.tenant.tenant import tenant_create
from sqlalchemy_multi_tenant.users.adapters import UserCreate
from sqlalchemy_multi_tenant.users.crud_user import user as crud_user


@pytest.fixture
def patch_multi_tenant_enabled(settings, multi_tenant_enabled: bool) -> Generator:
    before = settings.MULTI_TENANT_ENABLED
    settings.MULTI_TENANT_ENABLED = multi_tenant_enabled
    yield
    settings.MULTI_TENANT_ENABLED = before


@pytest.fixture
def tenant_schema() -> str:
    return "tenant_evil_inc"


@pytest.fixture
def with_tenant(settings, tenant_schema):
    if not settings.MULTI_TENANT_ENABLED:
        return None
    return tenant_create("Evil Inc", tenant_schema)


@pytest.fixture
def tenant_username() -> str:
    return "firstuser@evil.com"


@pytest.fixture
def tenant_password() -> str:
    return "firstuser@evil.com"


@pytest.fixture
def create_tenant_user(with_tenant, tenant_schema, tenant_username, tenant_password):
    user_in = UserCreate(
        email=tenant_username,
        password=tenant_password,
        is_superuser=False,
    )
    tenant_id = with_tenant
    if tenant_id is None:
        with dbsession_ctx_for_tenant() as dbsession:
            user_id = crud_user.create(dbsession, obj_in=user_in).id
    else:
        with dbsession_ctx_for_tenant(tenant_schema=tenant_schema) as dbsession:
            user_id = crud_tenant.create_user_for_tenant(
                dbsession, tenant_id=tenant_id, user_in=user_in
            ).id

    yield

    tenant_schema = "tenant_default" if not tenant_id else tenant_schema
    with dbsession_ctx_for_tenant(tenant_schema=tenant_schema) as dbsession:
        crud_user.delete(dbsession, obj_id=user_id)
