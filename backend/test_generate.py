"""Test the generate recommendations endpoint"""
from database import SessionLocal
from models import User
from ml_engine.recommendation_engine import create_recommendation_engine

db = SessionLocal()
try:
    # Get the test user
    user = db.query(User).filter(User.email == 'testuser456@example.com').first()
    print(f"✓ Found user: {user.email}")
    
    # Get user profile
    profile = user.profile
    print(f"✓ User profile: {profile}")
    if not profile:
        print("ERROR: User profile is None")
        exit(1)
    
    # Get daily entries
    from models import DailyEntry
    daily_entries = db.query(DailyEntry).filter(DailyEntry.user_id == user.id).all()
    print(f"✓ Daily entries count: {len(daily_entries)}")
    
    # Create engine
    print("Creating recommendation engine...")
    engine = create_recommendation_engine()
    print(f"✓ Engine created, NLP enabled: {engine.nlp_enabled}")
    print(f"✓ Careers loaded: {len(engine.careers)}")
    
    # Analyze profile
    print("\nAnalyzing user profile...")
    user_vector = engine.analyze_user_profile(profile, daily_entries)
    print(f"✓ Analysis complete")
    print(f"  - Passion: {user_vector['passion_score']}")
    print(f"  - Skills: {user_vector['skills_score']}")
    print(f"  - Values: {user_vector['values_score']}")
    print(f"  - Market: {user_vector['market_readiness']}")
    
    # Find matching careers
    print("\nFinding matching careers...")
    matched_careers = engine.find_matching_careers(user_vector, 5)
    print(f"✓ Found {len(matched_careers)} matched careers")
    for i, career in enumerate(matched_careers, 1):
        print(f"  {i}. {career['title']} (Score: {career['match_score']})")
    
    print("\n✓ ALL TESTS PASSED - generate endpoint should work!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
