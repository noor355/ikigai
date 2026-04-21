from database import SessionLocal
from models import User
from ml_engine.recommendation_engine import create_recommendation_engine

db = SessionLocal()
user = db.query(User).filter(User.email == 'testuser456@example.com').first()

if user:
    print(f"User found: {user.email}")
    print(f"Profile: {user.profile}")
    
    if user.profile:
        print(f"Profile ID: {user.profile.id}")
        # Try the analysis
        engine = create_recommendation_engine()
        try:
            result = engine.analyze_user_profile(user.profile, [])
            print(f"Analysis result: {result}")
        except Exception as e:
            print(f"Error in analyze_user_profile: {e}")
            import traceback
            traceback.print_exc()
else:
    print("User not found")
