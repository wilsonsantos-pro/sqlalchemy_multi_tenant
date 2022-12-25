from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.auth import get_password_hash, verify_password
from sqlalchemy_multi_tenant.crud.base import CRUDBase
from sqlalchemy_multi_tenant.users.adapters import UserCreate, UserUpdate

from .models import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, dbsession: Session, *, email: str) -> Optional[User]:
        return dbsession.query(User).filter(User.email == email).first()

    def create(self, dbsession: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        dbsession.add(db_obj)
        dbsession.commit()
        dbsession.refresh(db_obj)
        return db_obj

    def update(
        self,
        dbsession: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(dbsession, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, dbsession: Session, *, email: str, password: str
    ) -> Optional[User]:
        # pylint: disable=redefined-outer-name
        user = self.get_by_email(dbsession, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user = CRUDUser(User)
