from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    yandex_id: str

class UserInDB(UserBase):
    id: int
    yandex_id: str
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True