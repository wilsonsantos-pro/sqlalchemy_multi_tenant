from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class User(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(User):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(User):
    password: Optional[str] = None


class UserInDBBase(User):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
