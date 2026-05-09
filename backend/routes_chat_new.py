from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, DailyEntry, ExpertOverride
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

    # Clean message for matching
    msg_clean = user_message.strip().lower()
    
    # Check if the message is *just* a short greeting
    is_short_greeting = msg_clean in ["hi", "hello", "hey", "greetings", "hi there", "hello there", "hey coach"]
    
    # 1. First, check for high-intent keywords to trigger specialized advice
    if is_short_greeting:
        reply = f"Hello {current_user.full_name or current_user.username}! I'm your Ikigai Career Coach. I've been analyzing your profile in {interests_str}. How can I help you discover your path today?"
    
    elif msg_clean.startswith(("my name is", "i am ")) and len(msg_clean.split()) < 6:
        name_part = msg_clean.split("is")[-1].strip() if "is" in msg_clean else msg_clean.split("am")[-1].strip()
        reply = f"It's a pleasure to meet you, {name_part.capitalize()}! I'm here to help you find your Ikigai. Since I'm learning more about you, what's a dream you've had for your career that you've never told anyone?"

    elif "ikigai" in user_message:
        reply = "Ikigai is a Japanese concept meaning 'a reason for being'. It's the intersection of: 1. What you love, 2. What you are good at, 3. What the world needs, and 4. What you can be paid for. Which of these four areas feels like your strongest foundation right now?"
        
    elif any(word in user_message for word in ["recommendation", "suggest", "find"]):
        reply = "I've just updated your personalized recommendations based on our conversation! Head over to the Recommendations page to see what's changed. What's one skill you're proud of?"
        
        # EXPERT WORKFLOW: Signal the recommendation engine by performing semantic analysis now
        try:
            # For demonstration, we'll use a simulated history or a small set of recent entries
            # In a real app, you'd pull from a chat_history table
            history = [chat_input.message] # Last message for context
            pillars = engine.nlp_processor.analyze_career_pillars(history)
            
            # Save override to DB
            override = db.query(ExpertOverride).filter(ExpertOverride.user_id == current_user.id).first()
            if not override:
                override = ExpertOverride(user_id=current_user.id, pillars=pillars)
                db.add(override)
            else:
                override.pillars = pillars
                override.analyzed_at = datetime.datetime.utcnow()
            db.commit()
            print(f"[CHAT] Expert pillars identified: {pillars}")
        except Exception as e:
            print(f"[CHAT] Expert Pillar analysis failed: {e}")

    # 2. Use the real NLP model for general conversation
    else:
        try:
            # We bypass the local keyword-based replies to let Gemini handle it with full context
            nlp_reply = engine.nlp_processor.generate_coach_response(chat_input.message, context=context_str)
            
            # If the reply is still too short or weird, use better fallback
            if len(nlp_reply) < 10:
                reply = f"I'm analyzing how '{chat_input.message}' fits with your recent journals in {current_user.profile.interests if current_user.profile else 'general interests'}. What's one specific goal you have for this month?"
            else:
                reply = nlp_reply
        except Exception as e:
            print(f"[CHAT ERROR] NLP Generation failed: {e}")
            reply = f"I'm reflecting on your interest in {chat_input.message}. How does this align with your recent journal entries?"

    # In a real implementation, we would store this in the database
    return ChatResponse(
        reply=reply,
        history=[
            {"role": "user", "content": chat_input.message, "timestamp": datetime.datetime.utcnow()},
            {"role": "assistant", "content": reply, "timestamp": datetime.datetime.utcnow()}
        ]
    )
