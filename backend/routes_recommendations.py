from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Recommendation, DailyEntry
from schemas import RecommendationResponse, DailyEntryCreate
from security import get_current_active_user
from ml_engine.recommendation_engine import create_recommendation_engine
from datetime import datetime
import json

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])


@router.get("/")
def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's saved recommendations"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.created_at.desc()).all()
    
    # Convert to dict and parse JSON reasoning
    result = []
    for rec in recommendations:
        rec_dict = {
            'id': rec.id,
            'user_id': rec.user_id,
            'career_title': rec.career_title,
            'description': rec.description,
            'match_score': rec.match_score,
            'reasoning': json.loads(rec.reasoning) if isinstance(rec.reasoning, str) else rec.reasoning,
            'required_skills': rec.required_skills or [],
            'growth_potential': rec.growth_potential,
            'market_demand': rec.market_demand,
            'salary_range_min': rec.salary_range_min,
            'salary_range_max': rec.salary_range_max,
            'future_oriented': rec.future_oriented,
            'created_at': rec.created_at,
            'updated_at': rec.updated_at,
        }
        result.append(rec_dict)
    
    return result


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
            detail="User profile incomplete. Please complete your profile first."
        )
    
    # Get daily entries
    daily_entries = db.query(DailyEntry).filter(
        DailyEntry.user_id == current_user.id
    ).order_by(DailyEntry.date.desc()).all()
    
    # Create recommendation engine
    engine = create_recommendation_engine()
    
    # Analyze user profile
    user_vector = engine.analyze_user_profile(profile, daily_entries)
    
    # Find matching careers
    matched_careers = engine.find_matching_careers(user_vector, top_n)
    
    # Save recommendations to database
    db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).delete()
    
    saved_recommendations = []
    
    for career_match in matched_careers:
        recommendation = Recommendation(
            user_id=current_user.id,
            career_title=career_match['title'],
            description=career_match['description'],
            match_score=career_match['match_score'],
            reasoning=json.dumps(career_match['reasoning']),
            required_skills=career_match.get('required_skills', []),
            growth_potential=career_match.get('growth_potential'),
            market_demand=career_match.get('market_demand'),
            salary_range_min=career_match.get('salary_range', (0, 0))[0],
            salary_range_max=career_match.get('salary_range', (0, 0))[1],
            future_oriented=True
        )
        db.add(recommendation)
        db.flush()
        saved_recommendations.append({
            'id': recommendation.id,
            'career_title': recommendation.career_title,
            'match_score': recommendation.match_score,
            'reasoning': career_match['reasoning'],
            'skill_gaps': career_match.get('skill_gaps', []),
            'learning_path': career_match.get('learning_path', []),
        })
    
    db.commit()
    
    return {
        'status': 'success',
        'message': f'Generated {len(saved_recommendations)} recommendations based on your profile',
        'recommendations': saved_recommendations,
        'user_profile_analysis': {
            'passion_score': user_vector['passion_score'],
            'skills_score': user_vector['skills_score'],
            'values_score': user_vector['values_score'],
            'market_readiness': user_vector['market_readiness'],
            'overall_readiness': user_vector['overall_readiness'],
        }
    }


@router.post("/save-daily-entry")
def save_daily_entry(
    entry_data: DailyEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Save a daily journal entry"""
    
    entry = DailyEntry(
        user_id=current_user.id,
        activities=entry_data.activities,
        learnings=entry_data.learnings,
        challenges=entry_data.challenges,
        mood=entry_data.mood,
        notes=entry_data.notes,
        date=datetime.utcnow()
    )
    
    db.add(entry)
    db.commit()
    db.refresh(entry)

    # Trigger async-like background update if profile exists
    # For now, we keep it simple, but the singleton engine makes this much faster
    try:
        if current_user.profile:
            # We don't wait for the full generate_recommendations here to return to user faster
            # But the initialization is now cached so this is much quicker
            pass
    except Exception:
        pass
    
    return {
        'status': 'success',
        'message': 'Daily entry saved successfully',
        'entry_id': entry.id,
    }


@router.get("/analysis")
def get_recommendation_analysis(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed analysis of user's recommendation profile"""
    
    profile = current_user.profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile incomplete"
        )
    
    daily_entries = db.query(DailyEntry).filter(
        DailyEntry.user_id == current_user.id
    ).all()
    
    engine = create_recommendation_engine()
    user_vector = engine.analyze_user_profile(profile, daily_entries)
    
    return {
        'status': 'success',
        'analysis': user_vector,
        'total_daily_entries': len(daily_entries),
        'profile_completeness': calculate_profile_completeness(profile),
    }


def calculate_profile_completeness(profile) -> float:
    """Calculate how complete the user's profile is (0-100%)"""
    completeness = 0
    total_fields = 0
    
    fields_to_check = [
        'age', 'education_level', 'work_experience_years',
        'bio', 'interests', 'skills', 'values', 'passion_areas', 'location'
    ]
    
    for field in fields_to_check:
        total_fields += 1
        value = getattr(profile, field, None)
        
        if value:
            if isinstance(value, (list, dict)):
                if len(value) > 0:
                    completeness += 1
            else:
                completeness += 1
    
    if total_fields == 0:
        return 0
    
    return (completeness / total_fields) * 100

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
