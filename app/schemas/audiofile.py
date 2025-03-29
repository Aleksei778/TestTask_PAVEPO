from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AudioFileCreate(BaseModel):
    user_id: int
    original_filename: str
    file_path: str
    changed_filename: Optional[str] = None

class AudioFileUpdate(BaseModel):
    changed_filename: Optional[str] = None

class AudioFileResponse(BaseModel):
    id: int
    user_id: int
    changed_filename: Optional[str] = None
    original_filename: str
    file_path: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True