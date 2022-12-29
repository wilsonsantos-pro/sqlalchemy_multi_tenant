from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy_multi_tenant import auth
from sqlalchemy_multi_tenant.api import dependencies as deps
from sqlalchemy_multi_tenant.config import settings
from sqlalchemy_multi_tenant.core.db.session import dbsession_ctx_for_tenant
from sqlalchemy_multi_tenant.tenant.models import Tenant
from sqlalchemy_multi_tenant.users import crud_user as crud

router = APIRouter()


@router.post("", response_model=auth.Token)
def login(
    tenant: Tenant = Depends(deps.get_tenant_from_user_email),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> auth.Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    with dbsession_ctx_for_tenant(tenant.schema) as dbsession:
        user = crud.user.authenticate(
            dbsession, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": auth.create_access_token(
                user.email,
                tenant_name=tenant.name,
                expires_delta=access_token_expires,
            ),
            "token_type": "bearer",
        }
