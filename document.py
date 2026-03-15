from sqlalchemy import Column, String, Integer, Text, Boolean
from app.models.base import BaseModel

class Document(BaseModel):
    __tablename__ = "documents"
    
    filename = Column(String(255), index=True)
    file_path = Column(String(512))
    content_type = Column(String(100))
    file_size = Column(Integer)
    is_processed = Column(Boolean, default=False)
    faiss_index_id = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
