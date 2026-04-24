import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append('backend')

from ml_engine.recommendation_engine import create_recommendation_engine

class MockProfile:
    def __init__(self, interests, skills, values, education="Bachelor in CS"):
        self.interests = interests
        self.skills = skills
        self.values = values
        self.education_level = education
        self.work_experience_years = 2

class MockEntry:
    def __init__(self, notes, mood="happy"):
        self.notes = notes
        self.mood = mood

def test_recommendation_pipeline():
    print("--- Starting End-to-End Recommendation Test ---")
    
    # 1. Initialize Engine (Singleton)
    print("Loading Engine...")
    engine = create_recommendation_engine()
    
    # 2. Mock User Data (Passion + Skills)
    profile = MockProfile(
        interests=["AI", "Python", "Automating things", "Creative coding"],
        skills=["Python", "Basic JavaScript", "Problem Solving", "Collaboration"],
        values=["Innovation", "Freedom", "Helping others"]
    )
    
    # 3. Mock Daily Entries (Sentiment Analysis)
    entries = [
        MockEntry("Today I worked on an AI project and felt incredibly energized by the possibilities."),
        MockEntry("I spent time learning about neural networks and I love how complex but logical it is."),
        MockEntry("Busy day at work, but I enjoyed helping a colleague debug their code.")
    ]
    
    print("\n--- Analyzing Profile ---")
    user_vector = engine.analyze_user_profile(profile, entries)
    print(f"Pillar Scores:")
    print(f" - Passion: {user_vector['passion_score']}/100")
    print(f" - Skills: {user_vector['skills_score']}/100")
    print(f" - Values: {user_vector['values_score']}/100")
    print(f" - Readiness: {user_vector['market_readiness']}/100")
    
    print("\n--- Finding Career Matches ---")
    matches = engine.find_matching_careers(user_vector, top_n=2)
    
    for i, match in enumerate(matches):
        print(f"\nMatch #{i+1}: {match['title']}")
        print(f"Score: {match['match_score']}%")
        print(f"Reasoning: {match['reasoning']['primary_reason']}")
        print(f"Skill Gap: {match['reasoning']['skill_alignment']}")

if __name__ == "__main__":
    try:
        test_recommendation_pipeline()
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
