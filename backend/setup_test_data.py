"""Create a test user for end-to-end verification"""
from database import SessionLocal
from models import User, UserProfile, DailyEntry
from security import get_password_hash
import datetime

db = SessionLocal()
try:
    email = 'testuser456@example.com'
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print(f"Creating user {email}...")
        user = User(
            email=email,
            username='testuser456',
            hashed_password=get_password_hash('password123'),
            full_name='Test User 456',
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("✓ User created")
    else:
        print(f"✓ User {email} already exists")

    # Create profile if not exists
    if not user.profile:
        print("Creating profile...")
        profile = UserProfile(
            user_id=user.id,
            age=25,
            education_level="Bachelor's in Computer Science",
            work_experience_years=2,
            bio="Passionate about technology and problem solving.",
            interests=["coding", "reading", "gaming"],
            skills=["Python", "FastAPI", "React"],
            values=["continuous learning", "impact", "innovation"],
            passion_areas=["Artificial Intelligence", "Web Development"],
            location="San Francisco, CA"
        )
        db.add(profile)
        db.commit()
        print("✓ Profile created")
    else:
        print("✓ Profile already exists")

    # Add a daily entry if none exist
    entries_count = db.query(DailyEntry).filter(DailyEntry.user_id == user.id).count()
    if entries_count == 0:
        print("Adding a mock daily entry...")
        entry = DailyEntry(
            user_id=user.id,
            activities=["Worked on a React dashboard", "Learned about FastAPI dependency injection"],
            learnings="Deepened understanding of asynchronous Python.",
            mood="happy",
            notes="Productive day overall.",
            date=datetime.datetime.utcnow()
        )
        db.add(entry)
        db.commit()
        print("✓ Daily entry added")
    else:
        print(f"✓ {entries_count} daily entries already exist")

    print("\n✓ SUCCESS: Test data is ready for verification!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    db.rollback()
finally:
    db.close()
