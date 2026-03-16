from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, DailyEntry
from schemas import DailyEntryCreate, DailyEntryResponse
from security import get_current_active_user
from datetime import datetime

router = APIRouter(prefix="/api/v1/daily-entries", tags=["daily-entries"])


@router.post("/", response_model=DailyEntryResponse)
def create_daily_entry(
    entry_data: DailyEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new daily entry"""
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
    
    return daily_entry


@router.get("/", response_model=list[DailyEntryResponse])
def get_daily_entries(
    days: int = 7,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's daily entries from last N days"""
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    entries = db.query(DailyEntry).filter(
        (DailyEntry.user_id == current_user.id) &
        (DailyEntry.created_at >= cutoff_date)
    ).order_by(DailyEntry.date.desc()).all()
    
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
