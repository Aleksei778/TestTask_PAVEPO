from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    yandex_id: str
    email: EmailStr
    name: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class UserResponse(BaseModel):
    yandex_id: str
    email: EmailStr
    name: str
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True