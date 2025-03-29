from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AudioFileCreate(BaseModel):
    created_name: str

class AudioFileInDB(BaseModel):
    id: int
    user_id: int
    changed_filename: Optional[str] = None
    original_filename: str
    file_path: str
    uploaded_at: datetime