"""
NLP Integration Examples for Ikigai API Routes
This module shows how to integrate NLP features into your API endpoints
"""

from ml_engine.recommendation_engine import IkigaiRecommendationEngine
from ml_engine.nlp_processor import get_nlp_processor
from typing import List, Dict


# Example: Using NLP in recommendation routes
def recommend_careers_with_nlp(
    user_profile: Dict,
    user_bio: str,
    available_careers: List[Dict]
) -> List[Dict]:
    """
    Get career recommendations using both ML and NLP
    
    Usage:
        recommendations = recommend_careers_with_nlp(
            user_profile={"skills": ["Python", "ML"], "education": "Bachelor"},
            user_bio="I love coding and solving problems. Interested in AI and data science.",
            available_careers=[
                {"id": 1, "title": "ML Engineer", "description": "..."},
                {"id": 2, "title": "Data Scientist", "description": "..."},
            ]
        )
    """
    engine = IkigaiRecommendationEngine()
    
    recommendations = []
    for career in available_careers:
        match = engine.calculate_nlp_enhanced_career_match(
            user_profile=user_profile,
            user_bio=user_bio,
            career=career
        )
        recommendations.append({
            "career": career,
            "match_score": match["overall_score"],
            "details": match,
            "matching_keywords": match.get("matching_keywords", [])
        })
    
    # Sort by score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations


# Example: Analyze daily entries for insights
def analyze_daily_entries_nlp(daily_entries: List[Dict]) -> Dict:
    """
    Analyze daily entries to extract patterns and insights
    
    Usage:
        insights = analyze_daily_entries_nlp(
            daily_entries=[
                {"id": 1, "date": "2024-01-01", "content": "Today I worked on a Python project..."},
                {"id": 2, "date": "2024-01-02", "content": "Fixed some database queries..."},
            ]
        )
    """
    nlp = get_nlp_processor()
    
    all_sentiments = []
    all_keywords = []
    all_skills = []
    
    for entry in daily_entries:
        if isinstance(entry, dict) and "content" in entry:
            # Analyze sentiment
            sentiment = nlp.analyze_sentiment(entry["content"])
            all_sentiments.append(sentiment)
            
            # Extract keywords
            keywords = nlp.extract_keywords(entry["content"])
            all_keywords.extend(keywords)
            
            # Extract skills
            entities = nlp.extract_skills_and_entities(entry["content"])
            all_skills.extend(entities.get("skills", []))
    
    # Calculate summary statistics
    positive_count = sum(1 for s in all_sentiments if s.get("sentiment_type") == "positive")
    average_sentiment = positive_count / max(len(all_sentiments), 1)
    
    return {
        "total_entries": len(daily_entries),
        "sentiment_distribution": {
            "positive": positive_count,
            "negative": len(all_sentiments) - positive_count,
            "positive_ratio": average_sentiment
        },
        "top_keywords": list(dict.fromkeys(all_keywords))[:10],
        "detected_skills": list(dict.fromkeys(all_skills)),
        "patterns": extract_patterns(all_keywords)
    }


def extract_patterns(keywords: List[str]) -> Dict:
    """Extract patterns from keywords"""
    # Simple pattern detection
    technical_keywords = ["python", "java", "javascript", "react", "sql", "api", "database"]
    soft_keywords = ["team", "communication", "problem", "solving", "leading", "mentoring"]
    
    tech_count = sum(1 for kw in keywords if any(tk in kw.lower() for tk in technical_keywords))
    soft_count = sum(1 for kw in keywords if any(sk in kw.lower() for sk in soft_keywords))
    
    return {
        "technical_focus": tech_count,
        "soft_skills_focus": soft_count,
        "focus_area": "Technical" if tech_count > soft_count else "Soft Skills"
    }


# Example: Get skill recommendations based on interests
def get_skill_recommendations(user_interests: List[str], user_skills: List[str]) -> List[str]:
    """
    Recommend skills based on user interests and current skills
    
    Usage:
        new_skills = get_skill_recommendations(
            user_interests=["AI", "data science", "machine learning"],
            user_skills=["Python", "SQL"]
        )
    """
    nlp = get_nlp_processor()
    
    # Find semantic similar areas for interests
    skill_recommendations = set()
    
    # Map common interest → recommended skills
    skill_map = {
        "AI": ["TensorFlow", "PyTorch", "Deep Learning", "Neural Networks"],
        "data": ["Pandas", "NumPy", "Tableau", "Power BI", "Statistics"],
        "machine": ["Scikit-learn", "XGBoost", "Model Evaluation", "Feature Engineering"],
        "web": ["React", "Vue", "Node.js", "Django", "FastAPI"],
        "cloud": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes"],
        "mobile": ["React Native", "Flutter", "Swift", "Kotlin"],
    }
    
    for interest in user_interests:
        for keyword, skills in skill_map.items():
            if keyword.lower() in interest.lower():
                skill_recommendations.update(skills)
    
    # Remove skills already known
    skill_recommendations -= set(user_skills)
    
    return list(skill_recommendations)


# Example: Semantic search for job descriptions matching user profile
def find_matching_jobs_nlp(
    user_profile_text: str,
    available_jobs: List[Dict]
) -> List[tuple]:
    """
    Find jobs that best match user profile using semantic similarity
    
    Usage:
        matches = find_matching_jobs_nlp(
            user_profile_text="I'm a Python developer with 5 years of experience...",
            available_jobs=[
                {"id": 1, "title": "Senior Python Developer", "description": "..."},
                {"id": 2, "title": "JavaScript Developer", "description": "..."},
            ]
        )
    """
    nlp = get_nlp_processor()
    
    job_descriptions = [f"{job['title']}: {job.get('description', '')}" for job in available_jobs]
    
    # Find most similar jobs
    matches = nlp.find_most_similar(user_profile_text, job_descriptions)
    
    # Map back to job objects with similarity scores
    results = []
    for desc, score in matches:
        for job in available_jobs:
            job_desc = f"{job['title']}: {job.get('description', '')}"
            if job_desc == desc:
                results.append(({**job, "similarity_score": score}, score))
                break
    
    return sorted(results, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    # Example usage
    print("NLP Integration Examples for Ikigai API")
    print("=" * 50)
    
    # Test data
    sample_user = {
        "skills": ["Python", "SQL", "API Design"],
        "education": "Bachelor in CS",
        "years_experience": 3
    }
    
    sample_bio = "I'm passionate about AI and machine learning. I love solving complex problems with data."
    
    sample_careers = [
        {
            "id": 1,
            "title": "Machine Learning Engineer",
            "description": "Build and deploy ML models using Python and TensorFlow. Work with data pipelines and model optimization."
        },
        {
            "id": 2,
            "title": "Data Analyst",
            "description": "Analyze data using SQL and Python. Create reports and dashboards with Tableau."
        }
    ]
    
    # Get recommendations
    recs = recommend_careers_with_nlp(sample_user, sample_bio, sample_careers)
    print("\nTop Career Recommendations:")
    for rec in recs:
        print(f"  - {rec['career']['title']}: {rec['match_score']:.1f}%")
