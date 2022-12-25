from typing import Optional

from pydantic.dataclasses import dataclass

from sqlalchemy_multi_tenant.core.models import BaseDataClass


@dataclass
class Item(BaseDataClass):
    title: str
    description: Optional[str]
    owner_id: int
    id: Optional[int] = None  # pylint: disable=invalid-name
