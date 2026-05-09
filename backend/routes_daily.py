from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, DailyEntry, ExpertOverride
from schemas import DailyEntryCreate, DailyEntryResponse
from security import get_current_active_user
from ml_engine.recommendation_engine import create_recommendation_engine
from datetime import datetime

router = APIRouter(prefix="/api/v1/daily-entries", tags=["daily-entries"])

# Singleton-like access to the engine (reuse from chat)
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_recommendation_engine()
    return _engine


@router.post("/", response_model=DailyEntryResponse)
def create_daily_entry(
    entry_data: DailyEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new daily entry and update expert pillars"""
    daily_entry = DailyEntry(
        user_id=current_user.id,
        activities=entry_data.activities,
        learnings=entry_data.learnings,
        interests_explored=entry_data.interests_explored,
        challenges=entry_data.challenges,
        mood=entry_data.mood,
        notes=entry_data.notes
    )
    
    db.add(daily_entry)
    db.commit()
    db.refresh(daily_entry)
    
    # --- TRIGGER RECOM ENGINE: Analyze context from journals ---
    try:
        engine = get_engine()
        if engine and engine.nlp_processor:
            # Fetch last 5 entries to give Gemini context
            recent_entries = db.query(DailyEntry).filter(
                DailyEntry.user_id == current_user.id
            ).order_by(DailyEntry.created_at.desc()).limit(5).all()
            
            history_text = []
            for e in recent_entries:
                text = f"Activity: {e.activities}. Learning: {e.learnings}. Note: {e.notes}"
                history_text.append(text)
                
            # Use existing analyzer to get pillars
            pillars = engine.nlp_processor.analyze_career_pillars(history_text)
            
            # Save or update ExpertOverride
            override = db.query(ExpertOverride).filter(ExpertOverride.user_id == current_user.id).first()
            if not override:
                override = ExpertOverride(user_id=current_user.id, pillars=pillars)
                db.add(override)
            else:
                override.pillars = pillars # type: ignore
                override.analyzed_at = datetime.utcnow() # type: ignore
            db.commit()
    except Exception as e:
        print(f"[RECS] Failed to update coach pillars from journal: {e}")
    
    return daily_entry


@router.get("/", response_model=list[DailyEntryResponse])
def get_daily_entries(
    days: int = 7,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's daily entries from last N days"""
    from datetime import timedelta
    
    # Use accurate filtering and include all user entries
    entries = db.query(DailyEntry).filter(
        DailyEntry.user_id == current_user.id
    ).order_by(DailyEntry.created_at.desc()).all()
    
    return entries


@router.get("/{entry_id}", response_model=DailyEntryResponse)
def get_daily_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific daily entry"""
    entry = db.query(DailyEntry).filter(
        (DailyEntry.id == entry_id) &
        (DailyEntry.user_id == current_user.id)
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily entry not found"
        )
    
    return entry


@router.put("/{entry_id}", response_model=DailyEntryResponse)
def update_daily_entry(
    entry_id: int,
    entry_data: DailyEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a daily entry"""
    entry = db.query(DailyEntry).filter(
        (DailyEntry.id == entry_id) &
        (DailyEntry.user_id == current_user.id)
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily entry not found"
        )
    
    # Update fields
    for field, value in entry_data.model_dump().items():
        setattr(entry, field, value)
    
    db.commit()
    db.refresh(entry)
    
    return entry


@router.delete("/{entry_id}")
def delete_daily_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a daily entry"""
    entry = db.query(DailyEntry).filter(
        (DailyEntry.id == entry_id) &
        (DailyEntry.user_id == current_user.id)
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily entry not found"
        )
    
    db.delete(entry)
    db.commit()
    
    return {"message": "Daily entry deleted successfully"}
