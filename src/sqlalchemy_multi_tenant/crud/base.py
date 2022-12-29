from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sqlalchemy_multi_tenant.core.models import BaseDataClass

# pylint: disable=invalid-name
ModelType = TypeVar("ModelType", bound=BaseDataClass)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# pylint: enable=invalid-name


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A domain model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, dbsession: Session, obj_id: Any) -> Optional[ModelType]:
        return dbsession.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(
        self, dbsession: Session, *, page: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return dbsession.query(self.model).offset(page).limit(limit).all()

    def create(self, dbsession: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        dbsession.add(db_obj)
        dbsession.commit()
        dbsession.refresh(db_obj)
        return db_obj

    def update(
        self,
        dbsession: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        dbsession.add(db_obj)
        dbsession.commit()
        dbsession.refresh(db_obj)
        return db_obj

    def delete(self, dbsession: Session, *, obj_id: int) -> ModelType:
        obj = dbsession.query(self.model).get(obj_id)
        dbsession.delete(obj)
        dbsession.commit()
        return obj
