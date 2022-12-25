from typing import List

from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.crud.base import CRUDBase
from sqlalchemy_multi_tenant.items.adapters import ItemCreate, ItemUpdate

from .models import Item


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, dbsession: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        db_obj = Item(
            title=obj_in.title, description=obj_in.description, owner_id=owner_id
        )
        dbsession.add(db_obj)
        dbsession.commit()
        dbsession.refresh(db_obj)
        return db_obj

    def get_all_by_owner(
        self, dbsession: Session, *, owner_id: int, page: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            dbsession.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(page)
            .limit(limit)
            .all()
        )


items = CRUDItem(Item)
