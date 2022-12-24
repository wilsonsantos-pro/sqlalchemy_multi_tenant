from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.auth.exceptions import InvalidAccessToken
from sqlalchemy_multi_tenant.auth.token import decode_access_token
from sqlalchemy_multi_tenant.core.db import dbsession_ctx
from sqlalchemy_multi_tenant.users import crud_user as crud
from sqlalchemy_multi_tenant.users import models

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login/")


def get_db() -> Generator:
    with dbsession_ctx() as dbsession:
        yield dbsession


def get_current_user(
    dbsession: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        token_data = decode_access_token(token)
    except InvalidAccessToken as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc
    user = crud.user.get_by_email(dbsession, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
