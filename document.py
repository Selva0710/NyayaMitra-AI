from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    content_type: str
    file_size: int

class DocumentResponse(DocumentBase):
    id: int
    is_processed: bool
    summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
