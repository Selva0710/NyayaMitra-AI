from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ChatSession(BaseModel):
    __tablename__ = "chat_sessions"
    
    title = Column(String(255), nullable=True)
    user_id = Column(String(50), nullable=True) # Optional placeholder for multi-tenant auth
    
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"
    
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String(50)) # "user", "assistant", "system"
    content = Column(Text)
    
    session = relationship("ChatSession", back_populates="messages")
