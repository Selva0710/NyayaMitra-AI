from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    role: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    title: Optional[str] = None
    user_id: Optional[str] = None

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionResponse(ChatSessionBase):
    id: int
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

class ChatQueryRequest(BaseModel):
    message: str
    session_id: Optional[int] = None
    agent_type: Optional[str] = "auto" # auto, legal, ca, doc
