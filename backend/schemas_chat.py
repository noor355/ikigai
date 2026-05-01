from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(BaseModel):
    role: str # 'user' or 'assistant'
    content: str
    timestamp: datetime

class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessageResponse] = []
