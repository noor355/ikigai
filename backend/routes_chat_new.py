from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, DailyEntry
from routes_auth import get_current_active_user
from schemas_chat import ChatMessageCreate, ChatResponse
from ml_engine.recommendation_engine import create_recommendation_engine
import datetime
import random

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"]
)

# Singleton-like access to the engine (NLP models take time to load)
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        print("[CHAT] Initializing AI Engine...")
        _engine = create_recommendation_engine()
    return _engine

@router.post("/", response_model=ChatResponse)
async def chat_with_coach(
    chat_input: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the AI Career Coach using Real NLP Models.
    """
    user_message = chat_input.message.lower()
    engine = get_engine()
    
    # Get user profile information for personalization
    profile_info = ""
    interests_str = "general"
    skills_str = "unspecified"
    
    if current_user.profile:
        if current_user.profile.interests:
            interests_str = ", ".join(current_user.profile.interests)
        if current_user.profile.skills:
            skills_str = ", ".join(current_user.profile.skills)
        profile_info = f" The user is interested in {interests_str} and has skills in {skills_str}."

    # Get recent context from daily entries
    recent_entries = db.query(DailyEntry).filter(
        DailyEntry.user_id == current_user.id
    ).order_by(DailyEntry.date.desc()).limit(3).all()
    
    context_str = profile_info
    if recent_entries:
        context_str += " Recent activities include: " + "; ".join([str(e.activities) for e in recent_entries])

    # 1. First, check for high-intent keywords to trigger specialized advice
    if any(word in user_message for word in ["hello", "hi", "hey"]):
        reply = f"Hello {current_user.full_name or current_user.username}! I'm your Ikigai Career Coach. I've been analyzing your profile in {interests_str}. How can I help you discover your path today?"
    
    elif "my name is" in user_message or "i am" in user_message:
        name_part = user_message.split("is")[-1].strip() if "is" in user_message else user_message.split("am")[-1].strip()
        reply = f"It's a pleasure to meet you, {name_part.capitalize()}! I'm here to help you find your Ikigai. Since I'm learning more about you, what's a dream you've had for your career that you've never told anyone?"

    elif "ikigai" in user_message:
        reply = "Ikigai is a Japanese concept meaning 'a reason for being'. It's the intersection of: 1. What you love, 2. What you are good at, 3. What the world needs, and 4. What you can be paid for. Which of these four areas feels like your strongest foundation right now?"
        
    elif any(word in user_message for word in ["recommendation", "suggest", "find"]):
        reply = "To see your full career recommendations, head over to the Recommendations page! Based on our chat, I'm already seeing a strong alignment between your passions and future job markets. What's one skill you're proud of?"

    # 2. Use the real NLP model for general conversation
    else:
        try:
            # This uses the GPT-2 model we just added to nlp_processor.py
            nlp_reply = engine.nlp_processor.generate_coach_response(chat_input.message, context=context_str)
            reply = nlp_reply
        except Exception as e:
            print(f"[CHAT ERROR] NLP Generation failed: {e}")
            reply = "I appreciate you sharing that. Tell me more about how that fits into your ideal day-to-day life."

    # In a real implementation, we would store this in the database
    return ChatResponse(
        reply=reply,
        history=[
            {"role": "user", "content": chat_input.message, "timestamp": datetime.datetime.utcnow()},
            {"role": "assistant", "content": reply, "timestamp": datetime.datetime.utcnow()}
        ]
    )
