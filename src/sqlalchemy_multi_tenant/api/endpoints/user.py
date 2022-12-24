from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.api import dependencies
from sqlalchemy_multi_tenant.users import adapters
from sqlalchemy_multi_tenant.users import crud_user as crud
from sqlalchemy_multi_tenant.users import models

router = APIRouter()


@router.get("", response_model=List[adapters.User])
def get_users(
    dbsession: Session = Depends(dependencies.get_db),
    page: int = 0,
    limit: int = 100,
    _: models.User = Depends(dependencies.get_current_active_superuser),
) -> List[adapters.User]:
    users = crud.user.get_all(dbsession, page=page, limit=limit)
    return users
