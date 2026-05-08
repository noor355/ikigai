
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from ml_engine.career_database import get_all_careers
from ml_engine.recommendation_engine import IkigaiRecommendationEngine

def debug_recommendations():
    engine = IkigaiRecommendationEngine()
    
    # Mock user profile similar to one that should match Science Illustrator
    class Profile:
        def __init__(self):
            self.interests = ['biology', 'drawing', 'illustration', 'biotech']
            self.skills = ['visual design', 'adobe suite', 'biology']
            self.values = ['financial stability', 'impact', 'clarity']
            self.work_experience_years = 2
            self.education_level = 'Bachelor of Science'
            self.passion_areas = ['biotech', 'art']
            self.passion_keywords = ['biology', 'illustration'] # Manually added for vector check

    user_profile = Profile()
    
    # Mock daily entries
    daily_entries = []
    
    user_vector = engine.analyze_user_profile(user_profile, daily_entries)
    
    print("\n--- USER VECTOR ---")
    for k, v in user_vector.items():
        if k.endswith('keywords'):
            print(f"{k}: {v}")
        else:
            print(f"{k}: {v}")

    print("\n--- ALL CAREER MATCHES ---")
    # Get top 20 to see where everything falls
    matches = engine.find_matching_careers(user_vector, top_n=20)
    
    for i, m in enumerate(matches):
        print(f"{i+1}. {m['title']}: {m['match_score']}% (TF-IDF: {m['tfidf_similarity']:.4f})")
        if m['title'] == "Medical & Science Illustrator":
            print(f"   [FOUND] Rank: {i+1}")

if __name__ == "__main__":
    debug_recommendations()
