from typing import Optional

from pydantic import EmailStr
from pydantic.dataclasses import dataclass

from sqlalchemy_multi_tenant.core.models import BaseDataClass


@dataclass
class User(BaseDataClass):
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = False
    id: Optional[int] = None
    full_name: Optional[str] = None
