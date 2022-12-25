from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.items import crud_items as crud
from sqlalchemy_multi_tenant.items.adapters import ItemCreate
from sqlalchemy_multi_tenant.items.models import Item
from sqlalchemy_multi_tenant.users.models import User

from ..dependencies import get_current_active_user, get_db

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
    dbsession: Session = Depends(get_db),
    page: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> List[Item]:
    """
    Retrieve items.
    """
    if current_user.is_superuser:
        items = crud.items.get_all(dbsession, page=page, limit=limit)
    else:
        items = crud.items.get_all_by_owner(
            dbsession=dbsession, owner_id=current_user.id, page=page, limit=limit
        )
    return items


@router.post("/", response_model=Item)
def create_item(
    *,
    dbsession: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: User = Depends(get_current_active_user),
) -> Item:
    """
    Create new item.
    """
    item = crud.items.create_with_owner(
        dbsession=dbsession, obj_in=item_in, owner_id=current_user.id
    )
    return item
