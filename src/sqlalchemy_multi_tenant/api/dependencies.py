from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.auth.exceptions import InvalidAccessToken
from sqlalchemy_multi_tenant.auth.models import TokenPayload
from sqlalchemy_multi_tenant.auth.token import decode_access_token
from sqlalchemy_multi_tenant.core.db import dbsession_ctx_for_tenant
from sqlalchemy_multi_tenant.tenant.crud_tenant import tenant as crud_tenant
from sqlalchemy_multi_tenant.tenant.models import Tenant
from sqlalchemy_multi_tenant.users import crud_user as crud
from sqlalchemy_multi_tenant.users.models import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login/")


def get_db_for_shared_schema() -> Generator:
    with dbsession_ctx_for_tenant("shared") as dbsession:
        yield dbsession


def get_token_payload(token: str = Depends(reusable_oauth2)) -> TokenPayload:
    try:
        return decode_access_token(token)
    except InvalidAccessToken as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc


def get_tenant_from_user_email(
    dbsession: Session = Depends(get_db_for_shared_schema),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Tenant:
    # pylint: disable=import-outside-toplevel
    from sqlalchemy_multi_tenant.config import settings

    if not settings.MULTI_TENANT_ENABLED:
        return Tenant(name="tenant_default", schema="tenant_default")

    user_email = form_data.username
    tenant = crud_tenant.get_by_user_email(dbsession, user_email=user_email)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


def get_tenant_from_token(
    dbsession: Session = Depends(get_db_for_shared_schema),
    token_data: TokenPayload = Depends(get_token_payload),
) -> Tenant:
    # pylint: disable=import-outside-toplevel
    from sqlalchemy_multi_tenant.config import settings

    if not settings.MULTI_TENANT_ENABLED:
        return Tenant(name="tenant_default", schema="tenant_default")

    tenant_name = token_data.tnt
    tenant = crud_tenant.get_by_name(dbsession, name=tenant_name)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


def get_db(tenant: Tenant = Depends(get_tenant_from_token)) -> Generator:
    with dbsession_ctx_for_tenant(tenant.schema) as dbsession:
        yield dbsession


def get_current_user(
    dbsession: Session = Depends(get_db),
    token_data: TokenPayload = Depends(get_token_payload),
) -> User:
    user = crud.user.get_by_email(dbsession, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
