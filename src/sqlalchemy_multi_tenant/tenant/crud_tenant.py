from typing import Optional

from pydantic import EmailStr
from sqlalchemy import insert
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.crud.base import CRUDBase
from sqlalchemy_multi_tenant.users.adapters import UserCreate
from sqlalchemy_multi_tenant.users.crud_user import user as crud_user
from sqlalchemy_multi_tenant.users.models import User

from .models import Tenant
from .orm import tenant_user


class CRUDTenant(CRUDBase[Tenant, None, None]):
    def get_by_name(self, dbsession: Session, *, name: str) -> Optional[Tenant]:
        return dbsession.query(Tenant).filter(Tenant.name == name).first()

    def get_by_user_email(
        self, dbsession: Session, *, user_email: EmailStr
    ) -> Optional[Tenant]:
        return (
            dbsession.query(Tenant)
            .select_from(Tenant)
            .join(tenant_user, Tenant.id == tenant_user.c.tenant_id)
            .filter(tenant_user.c.user_email == user_email)
            .first()
        )

    def create_user_for_tenant(
        self, dbsession: Session, *, tenant_id: int, user_in: UserCreate
    ) -> User:
        user = crud_user.create(dbsession, obj_in=user_in)  # noqa: F841
        stmt = insert(tenant_user).values(tenant_id=tenant_id, user_email=user.email)
        dbsession.execute(stmt)
        dbsession.commit()
        return user


tenant = CRUDTenant(Tenant)
