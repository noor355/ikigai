from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Recommendation, DailyEntry
from schemas import RecommendationResponse
from security import get_current_active_user
from ml_engine import recommendation_engine
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])


@router.get("/", response_model=list[RecommendationResponse])
def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's saved recommendations"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.created_at.desc()).all()
    
    return recommendations


@router.post("/generate")
def generate_recommendations(
    top_n: int = 5,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate career recommendations based on user profile and daily entries"""
    
    # Get user's profile
    profile = current_user.profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile not complete"
        )
    
    # Get initial recommendations
    initial_recs = recommendation_engine.get_recommendations(
        user_skills=profile.skills or [],
        user_interests=profile.interests or [],
        user_values=profile.values or [],
        user_passions=profile.passion_areas or [],
        top_n=top_n
    )
    
    # Enhance with daily entries data for more accuracy
    recent_entries = db.query(DailyEntry).filter(
        DailyEntry.user_id == current_user.id
    ).order_by(DailyEntry.date.desc()).limit(7).all()
    
    combined_activities = []
    combined_learnings = ""
    combined_interests = []
    
    for entry in recent_entries:
        combined_activities.extend(entry.activities or [])
        if entry.learnings:
            combined_learnings += " " + entry.learnings
        combined_interests.extend(entry.interests_explored or [])
    
    # Update recommendations based on daily data
    if recent_entries:
        enhanced_recs = recommendation_engine.update_recommendations_with_daily_data(
            initial_recs,
            combined_activities,
            combined_learnings,
            combined_interests
        )
    else:
        enhanced_recs = initial_recs
    
    # Clear old recommendations and save new ones
    db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).delete()
    
    for rec in enhanced_recs:
        recommendation = Recommendation(
            user_id=current_user.id,
            career_title=rec["career_title"],
            description=rec["description"],
            match_score=rec["match_score"],
            reasoning=rec["reasoning"],
            required_skills=rec["required_skills"],
            growth_potential=rec["growth_potential"],
            market_demand=rec["market_demand"],
            salary_range_min=rec["salary_range_min"],
            salary_range_max=rec["salary_range_max"],
            future_oriented=rec["future_oriented"]
        )
        db.add(recommendation)
    
    db.commit()
    
    return {
        "message": "Recommendations generated successfully",
        "count": len(enhanced_recs),
        "recommendations": enhanced_recs
    }


@router.get("/{career_id}", response_model=RecommendationResponse)
def get_recommendation_details(
    career_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a recommendation"""
    recommendation = db.query(Recommendation).filter(
        (Recommendation.id == career_id) &
        (Recommendation.user_id == current_user.id)
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    return recommendation


@router.post("/refresh")
def refresh_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Refresh recommendations based on latest user data"""
    # Check how many daily entries exist
    entry_count = db.query(DailyEntry).filter(
        DailyEntry.user_id == current_user.id
    ).count()
    
    accuracy_note = ""
    if entry_count < 5:
        accuracy_note = "Add more daily entries for more accurate recommendations"
    elif entry_count < 10:
        accuracy_note = "Getting better! Continue adding daily entries"
    else:
        accuracy_note = "Excellent! High confidence recommendations"
    
    # Generate new recommendations
    result = generate_recommendations(
        top_n=10,
        current_user=current_user,
        db=db
    )
    
    result["accuracy_info"] = {
        "daily_entries": entry_count,
        "note": accuracy_note
    }
    
    return result
