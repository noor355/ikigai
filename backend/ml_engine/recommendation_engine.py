"""
ML Engine for Ikigai Career Recommendations
This module handles all machine learning operations for career recommendations
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime, timedelta


class IkigaiRecommendationEngine:
    """Main recommendation engine based on Ikigai principles"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.passion_weight = 0.25
        self.skill_weight = 0.25
        self.market_weight = 0.25
        self.growth_weight = 0.25
    
    def calculate_user_profile_vector(self, user_profile, daily_entries):
        """
        Create a vector representation of user's profile based on Ikigai pillars
        
        Returns:
            dict: User profile vector with scores for passion, skills, market fit, and growth
        """
        profile_vector = {
            'passions': self._extract_passion_score(user_profile, daily_entries),
            'skills': self._extract_skills_score(user_profile, daily_entries),
            'values': self._extract_values_score(user_profile, daily_entries),
            'market_readiness': self._extract_market_readiness(user_profile),
        }
        return profile_vector
    
    def _extract_passion_score(self, user_profile, daily_entries):
        """Extract passion score from user profile and daily entries"""
        passion_score = 0
        
        # Base score from profile
        if user_profile['passions']:
            passion_score += 50
        
        # Boost from daily entries
        if daily_entries:
            recent_entries = daily_entries[:30]  # Last 30 days
            happy_count = sum(1 for e in recent_entries if e.get('mood') in ['happy', 'very_happy'])
            passion_score += (happy_count / max(len(recent_entries), 1)) * 50
        
        return min(100, passion_score)
    
    def _extract_skills_score(self, user_profile, daily_entries):
        """Extract skills score from user profile and daily entries"""
        skill_score = 0
        
        # Base score from profile
        if user_profile['skills']:
            skill_score += 50
        
        # Boost from daily entries
        if daily_entries:
            for entry in daily_entries:
                if entry.get('skills_used'):
                    skill_score += len(entry['skills_used']) * 2
        
        return min(100, skill_score)
    
    def _extract_values_score(self, user_profile, daily_entries):
        """Extract values score from user profile and learnings"""
        value_score = 0
        
        if user_profile['values']:
            value_score += 50
        
        # Check for positive learnings in daily entries
        if daily_entries:
            for entry in daily_entries:
                if entry.get('learnings'):
                    value_score += 10
        
        return min(100, value_score)
    
    def _extract_market_readiness(self, user_profile):
        """Assess market readiness based on experience and education"""
        readiness_score = 50  # Base score
        
        # Add points for experience
        years = user_profile.get('years_of_experience', 0)
        readiness_score += min(years * 5, 25)
        
        # Add points for education
        education_level = user_profile.get('education_level', '')
        if 'master' in education_level.lower():
            readiness_score += 15
        elif 'bachelor' in education_level.lower():
            readiness_score += 10
        elif 'diploma' in education_level.lower():
            readiness_score += 5
        
        return min(100, readiness_score)
    
    def calculate_career_match(self, user_vector, career):
        """
        Calculate match score between user profile vector and a career
        
        Returns:
            dict: Match score and breakdown
        """
        passion_match = self._calculate_passion_match(user_vector['passions'], career)
        skill_match = self._calculate_skill_match(user_vector['skills'], career)
        market_fit = self._calculate_market_fit(user_vector['market_readiness'], career)
        growth_potential = self._calculate_growth_potential(career)
        
        # Weighted score
        overall_score = (
            passion_match * self.passion_weight +
            skill_match * self.skill_weight +
            market_fit * self.market_weight +
            growth_potential * self.growth_weight
        )
        
        return {
            'overall_score': overall_score,
            'passion_match': passion_match,
            'skill_match': skill_match,
            'market_fit': market_fit,
            'growth_potential': growth_potential,
        }
    
    def _calculate_passion_match(self, passion_score, career):
        """Calculate how well career aligns with user's passions"""
        match = passion_score * 0.5  # Base from user passion
        
        # Boost if career belongs to passion tags
        if career.get('passion_tags'):
            match += 50
        
        return min(100, match)
    
    def _calculate_skill_match(self, skill_score, career):
        """Calculate skill alignment with career requirements"""
        match = skill_score * 0.8  # Align with user's skills
        
        # Consider required skills
        if career.get('required_skills'):
            match += 20
        
        return min(100, match)
    
    def _calculate_market_fit(self, readiness, career):
        """Calculate market fit and demand"""
        match = readiness * 0.6
        
        # Boost based on job market demand
        demand_map = {
            'very_high': 40,
            'high': 30,
            'medium': 20,
            'low': 10,
        }
        demand_score = demand_map.get(career.get('job_market_demand'), 20)
        match += demand_score
        
        return min(100, match)
    
    def _calculate_growth_potential(self, career):
        """Calculate career growth potential"""
        growth_rate = career.get('growth_rate', 2)
        
        # Normalize growth rate to 0-100 scale
        # Assuming typical growth rates are 0-20%
        potential = min(growth_rate * 5, 100)
        
        # Factor in sustainability
        sustainability_map = {
            'highly_sustainable': 100,
            'sustainable': 80,
            'emerging': 60,
            'declining': 20,
        }
        potential = potential * 0.7 + sustainability_map.get(career.get('sustainability'), 50) * 0.3
        
        return potential
    
    def generate_explanation(self, user_name, career_title, match_scores):
        """Generate a human-readable explanation for the recommendation"""
        explanation = f""
        
        if match_scores['passion_match'] > 70:
            explanation += f"This career aligns strongly with your passions. "
        elif match_scores['passion_match'] > 50:
            explanation += f"This career has good alignment with your interests. "
        
        if match_scores['skill_match'] > 70:
            explanation += f"Your skills are well-suited for this role. "
        elif match_scores['skill_match'] > 50:
            explanation += f"You have relevant skills for this career. "
        
        if match_scores['market_fit'] > 70:
            explanation += f"There's strong market demand for this career. "
        
        if match_scores['growth_potential'] > 70:
            explanation += f"This is a high-growth career with great future prospects. "
        
        return explanation
