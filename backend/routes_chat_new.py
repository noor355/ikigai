from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User
from routes_auth import get_current_active_user
from schemas_chat import ChatMessageCreate, ChatResponse
import datetime

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"]
)

@router.post("/", response_model=ChatResponse)
async def chat_with_coach(
    chat_input: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the AI Career Coach.
    This is a mock implementation that will later be connected to a real LLM.
    """
    user_message = chat_input.message.lower()
    
    # Simple rule-based mock response logic
    if "hello" in user_message or "hi" in user_message:
        reply = f"Hello {current_user.full_name or current_user.username}! I'm your Ikigai Career Coach. How can I help you discover your path today?"
    elif "ikigai" in user_message:
        reply = "Ikigai is a Japanese concept meaning 'a reason for being'. it's the intersection of what you love, what you are good at, what the world needs, and what you can be paid for."
    elif "career" in user_message or "job" in user_message:
        reply = "I can definitely help with career guidance! Have you completed your profile and logged some daily journals? That helps me give better recommendations."
    elif "recommendation" in user_message:
        reply = "To see your career recommendations, you can head over to the Recommendations page. I analyze your skills and interests to find the best fit!"
    else:
        reply = "That's interesting! Tell me more about your passions and what you enjoy doing in your daily life."

    # In a real implementation, we would store this in the database and use an LLM
    return ChatResponse(
        reply=reply,
        history=[
            {"role": "user", "content": chat_input.message, "timestamp": datetime.datetime.utcnow()},
            {"role": "assistant", "content": reply, "timestamp": datetime.datetime.utcnow()}
        ]
    )
