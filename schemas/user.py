from pydantic import BaseModel, EmailStr
from datetime import datetime
from schemas.response import GenericResponse


class UserCreate(BaseModel):
    username: EmailStr
    password: str
    first_name: str

class UserPublic(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    full_name: str | None
    is_active: bool
    is_disabled: bool

class UserPublicResponse(GenericResponse):
    data: UserPublic

class UserUpdate(BaseModel):
    updated_at: str
    full_name: str
    username: str
    is_active: str
    is_disabled: str

class PasswordUpdate(BaseModel):
    old_password:str
    new_password:str
