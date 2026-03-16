import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


class CareerRecommendationEngine:
    """
    AI-powered career recommendation engine using the Ikigai framework.
    Recommends future-oriented careers based on:
    1. Abilities (skills and experience)
    2. Interests (passions and areas of focus)
    3. Values (what matters to the user)
    4. Passion areas (what they love doing)
    """
    
    # Career database with future-oriented careers
    CAREERS_DATABASE = [
        {
            "title": "AI/ML Engineer",
            "description": "Develops artificial intelligence and machine learning models for various applications",
            "skills": ["Python", "TensorFlow", "Machine Learning", "Data Analysis"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 80000,
            "salary_max": 150000,
            "related_ikigai": ["coding", "problem solving", "innovation", "technology"]
        },
        {
            "title": "Data Scientist",
            "description": "Analyzes complex datasets to drive business decisions and insights",
            "skills": ["Python", "SQL", "Statistics", "Data Visualization"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 85000,
            "salary_max": 160000,
            "related_ikigai": ["analysis", "patterns", "data", "insights"]
        },
        {
            "title": "Cloud Architect",
            "description": "Designs and manages scalable cloud infrastructure solutions",
            "skills": ["AWS", "Azure", "DevOps", "System Design"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 100000,
            "salary_max": 180000,
            "related_ikigai": ["architecture", "infrastructure", "scalability", "technology"]
        },
        {
            "title": "Data Engineer",
            "description": "Builds and maintains data pipelines and infrastructure",
            "skills": ["SQL", "Python", "Apache Spark", "ETL"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 90000,
            "salary_max": 170000,
            "related_ikigai": ["data", "infrastructure", "optimization", "technology"]
        },
        {
            "title": "UX/UI Designer",
            "description": "Creates user-centered design solutions for digital products",
            "skills": ["Figma", "User Research", "Prototyping", "Design Thinking"],
            "growth_potential": "Medium",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 60000,
            "salary_max": 120000,
            "related_ikigai": ["design", "creativity", "user experience", "innovation"]
        },
        {
            "title": "Product Manager",
            "description": "Guides product development from concept to market launch",
            "skills": ["Strategy", "Analytics", "Leadership", "Communication"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 85000,
            "salary_max": 160000,
            "related_ikigai": ["leadership", "strategy", "building products", "innovation"]
        },
        {
            "title": "Cybersecurity Specialist",
            "description": "Protects organizational data and systems from cyber threats",
            "skills": ["Network Security", "Cryptography", "Penetration Testing", "Python"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 90000,
            "salary_max": 170000,
            "related_ikigai": ["security", "protection", "problem solving", "technology"]
        },
        {
            "title": "Blockchain Developer",
            "description": "Develops decentralized applications and smart contracts",
            "skills": ["Solidity", "Web3", "Cryptography", "JavaScript"],
            "growth_potential": "High",
            "market_demand": "Medium",
            "future_oriented": True,
            "salary_min": 100000,
            "salary_max": 200000,
            "related_ikigai": ["innovation", "decentralization", "coding", "future"]
        },
        {
            "title": "Renewable Energy Engineer",
            "description": "Develops solutions for sustainable energy production",
            "skills": ["Engineering", "Solar/Wind Technology", "Systems Design", "Analysis"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 70000,
            "salary_max": 140000,
            "related_ikigai": ["sustainability", "environment", "innovation", "energy"]
        },
        {
            "title": "Biotechnology Specialist",
            "description": "Works on genetic engineering and life science innovations",
            "skills": ["Biology", "Genetic Engineering", "Lab Techniques", "Research"],
            "growth_potential": "High",
            "market_demand": "High",
            "future_oriented": True,
            "salary_min": 75000,
            "salary_max": 150000,
            "related_ikigai": ["science", "innovation", "helping people", "research"]
        }
    ]
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
    
    def calculate_match_score(
        self,
        user_skills: List[str],
        user_interests: List[str],
        user_values: List[str],
        user_passions: List[str],
        career: Dict
    ) -> Tuple[float, Dict]:
        """
        Calculate how well a career matches the user's profile
        Returns: (match_score, reasoning)
        """
        reasoning = {
            "skill_match": 0,
            "interest_match": 0,
            "values_match": 0,
            "passion_match": 0
        }
        
        # Skill matching
        if user_skills and career['skills']:
            skill_overlap = len(
                set(user_skills) & set(career['skills'])
            ) / len(career['skills'])
            reasoning["skill_match"] = skill_overlap * 100
        
        # Interest matching using cosine similarity
        if user_interests:
            user_interests_text = " ".join(user_interests).lower()
            career_interests_text = " ".join(
                career.get('related_ikigai', [])
            ).lower()
            
            if user_interests_text and career_interests_text:
                vectors = self.vectorizer.fit_transform(
                    [user_interests_text, career_interests_text]
                )
                similarity = cosine_similarity(vectors)[0][1]
                reasoning["interest_match"] = similarity * 100
        
        # Passion matching
        if user_passions:
            passion_overlap = len(
                set(user_passions) & set(career.get('related_ikigai', []))
            ) / max(len(career.get('related_ikigai', [])), 1)
            reasoning["passion_match"] = passion_overlap * 100
        
        # Calculate weighted average score
        weights = {
            "skill_match": 0.25,
            "interest_match": 0.25,
            "values_match": 0.25,
            "passion_match": 0.25
        }
        
        match_score = sum(
            reasoning[key] * weights[key]
            for key in reasoning.keys()
        )
        
        # Add bonus for future-oriented careers
        if career.get('future_oriented'):
            match_score = match_score * 1.1  # 10% bonus
        
        # Cap score at 100
        match_score = min(match_score, 100)
        
        return match_score, reasoning
    
    def get_recommendations(
        self,
        user_skills: List[str],
        user_interests: List[str],
        user_values: List[str],
        user_passions: List[str],
        top_n: int = 5
    ) -> List[Dict]:
        """
        Get top N career recommendations for a user
        """
        recommendations = []
        
        for career in self.CAREERS_DATABASE:
            score, reasoning = self.calculate_match_score(
                user_skills,
                user_interests,
                user_values,
                user_passions,
                career
            )
            
            recommendations.append({
                "career_title": career["title"],
                "description": career["description"],
                "match_score": round(score, 2),
                "reasoning": reasoning,
                "required_skills": career["skills"],
                "growth_potential": career["growth_potential"],
                "market_demand": career["market_demand"],
                "salary_range_min": career["salary_min"],
                "salary_range_max": career["salary_max"],
                "future_oriented": career["future_oriented"]
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations[:top_n]
    
    def update_recommendations_with_daily_data(
        self,
        current_recommendations: List[Dict],
        daily_activities: List[str],
        daily_learnings: str,
        interests_explored: List[str]
    ) -> List[Dict]:
        """
        Update recommendations based on daily entry data
        The more interactions, the more accurate the results
        """
        # Boost careers that match daily activities and learnings
        for rec in current_recommendations:
            boost = 0
            
            # Check if daily interests align with career
            for interest in interests_explored:
                if interest.lower() in rec["career_title"].lower():
                    boost += 5
            
            # Boost based on learning relevance
            if daily_learnings:
                career_keywords = set(rec["career_title"].lower().split())
                learning_keywords = set(daily_learnings.lower().split())
                overlap = len(career_keywords & learning_keywords)
                boost += overlap * 2
            
            rec["match_score"] = min(rec["match_score"] + boost, 100)
        
        # Resort by updated score
        current_recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return current_recommendations


# Singleton instance
recommendation_engine = CareerRecommendationEngine()
