"""
ML Engine for Ikigai Career Recommendations
Analyzes user profile and daily entries to recommend future-oriented careers
"""

from typing import Dict, List, Any
from .career_database import get_all_careers


class IkigaiRecommendationEngine:
    """Main recommendation engine based on Ikigai framework"""
    
    def __init__(self):
        self.careers = get_all_careers()
        self.passion_weight = 0.35
        self.skill_weight = 0.30
        self.values_weight = 0.20
        self.market_weight = 0.15
        
        # Try to initialize NLP processor
        try:
            from .nlp_processor import get_nlp_processor
            self.nlp_processor = get_nlp_processor()
            self.nlp_enabled = True
        except Exception as e:
            print(f"NLP disabled: {e}")
            self.nlp_enabled = False
            self.nlp_processor = None
    
    def analyze_user_profile(self, user_profile, daily_entries):
        """
        Comprehensive user profile analysis based on Ikigai pillars
        
        Returns: User vector with passion, skills, values, market readiness scores
        """
        passion_score = self._score_passion(user_profile, daily_entries)
        skills_score = self._score_skills(user_profile, daily_entries)
        values_score = self._score_values(user_profile, daily_entries)
        market_readiness = self._score_market_readiness(user_profile)
        
        return {
            'passion_score': passion_score,
            'skills_score': skills_score,
            'values_score': values_score,
            'market_readiness': market_readiness,
            'passion_keywords': self._extract_keywords(user_profile, 'interests'),
            'skill_keywords': self._extract_keywords(user_profile, 'skills'),
            'value_keywords': self._extract_keywords(user_profile, 'values'),
            'overall_readiness': (passion_score + skills_score + values_score + market_readiness) / 4,
        }
    
    def _score_passion(self, user_profile, daily_entries) -> float:
        """Calculate passion score 0-100"""
        score = 50
        
        if hasattr(user_profile, 'passion_areas') and user_profile.passion_areas:
            score += 20
        if hasattr(user_profile, 'interests') and user_profile.interests:
            score += 15
        
        # Analyze daily entries
        if daily_entries:
            positive_moods = sum(1 for e in daily_entries[-30:] 
                                if hasattr(e, 'mood') and e.mood in ['happy', 'very_happy', 'excited'])
            if len(daily_entries) > 0:
                score += (positive_moods / len(daily_entries[-30:])) * 15
        
        return min(100, score)
    
    def _score_skills(self, user_profile, daily_entries) -> float:
        """Calculate skills score 0-100"""
        score = 50
        
        if hasattr(user_profile, 'skills') and user_profile.skills:
            skill_count = len(user_profile.skills) if isinstance(user_profile.skills, list) else 0
            score += min(skill_count * 5, 25)
        
        if hasattr(user_profile, 'work_experience_years'):
            years = user_profile.work_experience_years
            score += min(years * 2, 20)
        
        return min(100, score)
    
    def _score_values(self, user_profile, daily_entries) -> float:
        """Calculate values alignment score 0-100"""
        score = 50
        
        if hasattr(user_profile, 'values') and user_profile.values:
            value_count = len(user_profile.values) if isinstance(user_profile.values, list) else 0
            score += min(value_count * 5, 25)
        
        return min(100, score)
    
    def _score_market_readiness(self, user_profile) -> float:
        """Calculate market readiness score 0-100"""
        score = 50
        
        education = getattr(user_profile, 'education_level', '').lower() if hasattr(user_profile, 'education_level') else ''
        
        if 'phd' in education:
            score += 20
        elif 'master' in education:
            score += 15
        elif 'bachelor' in education:
            score += 10
        
        years = getattr(user_profile, 'work_experience_years', 0)
        score += min(years * 3, 20)
        
        return min(100, score)
    
    def _extract_keywords(self, user_profile, attr_name) -> List[str]:
        """Extract keywords from user profile"""
        if hasattr(user_profile, attr_name):
            attr = getattr(user_profile, attr_name)
            if isinstance(attr, list):
                return attr[:15]
        return []
    
    def find_matching_careers(self, user_vector: Dict, top_n: int = 5) -> List[Dict]:
        """
        Find best matching careers based on user profile
        
        Returns: List of top matching careers with scores and reasoning
        """
        matches = []
        
        for career in self.careers:
            match_score = self._calculate_career_match(user_vector, career)
            reasoning = self._generate_reasoning(user_vector, career, match_score)
            skill_gaps = self._identify_skill_gaps(user_vector, career)
            
            matches.append({
                'career_id': career['id'],
                'title': career['title'],
                'description': career['description'],
                'match_score': match_score,
                'reasoning': reasoning,
                'skill_gaps': skill_gaps,
                'learning_path': career.get('learning_path', []),
                'salary_range': career.get('salary_range', (0, 0)),
                'growth_potential': career.get('growth_potential'),
                'market_demand': career.get('market_demand'),
                'future_relevance': career.get('future_relevance'),
                'required_skills': career.get('required_skills', []),
            })
        
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches[:top_n]
    
    def _calculate_career_match(self, user_vector: Dict, career: Dict) -> float:
        """Calculate match score between user and career"""
        passion_match = self._match_component(
            user_vector['passion_keywords'],
            user_vector['passion_score'],
            career.get('passion_keywords', [])
        )
        
        skill_match = self._match_component(
            user_vector['skill_keywords'],
            user_vector['skills_score'],
            career.get('skill_keywords', [])
        )
        
        values_match = self._match_component(
            user_vector['value_keywords'],
            user_vector['values_score'],
            career.get('value_keywords', [])
        )
        
        market_fit = user_vector['market_readiness']
        
        # Weighted average
        score = (
            passion_match * self.passion_weight +
            skill_match * self.skill_weight +
            values_match * self.values_weight +
            market_fit * self.market_weight
        )
        
        return round(score, 1)
    
    def _match_component(self, user_keywords: List[str], user_score: float, career_keywords: List[str]) -> float:
        """Calculate match for a single component (passion/skills/values)"""
        if not career_keywords:
            return user_score
        
        # Keyword overlap
        user_set = set([k.lower() for k in user_keywords])
        career_set = set([k.lower() for k in career_keywords])
        
        overlap = len(user_set & career_set)
        overlap_ratio = overlap / len(career_set) if career_set else 0.5
        
        # Combined score
        return user_score * 0.5 + overlap_ratio * 50
    
    def _identify_skill_gaps(self, user_vector: Dict, career: Dict) -> List[str]:
        """Identify skills user needs to develop"""
        user_skills = set([s.lower() for s in user_vector['skill_keywords']])
        required_skills = set([s.lower() for s in career.get('required_skills', [])])
        
        gaps = required_skills - user_skills
        return list(gaps)[:5]
    
    def _generate_reasoning(self, user_vector: Dict, career: Dict, score: float) -> Dict:
        """Generate explanation for career match"""
        reasoning = {
            'summary': '',
            'strengths': [],
            'growth_areas': [],
        }
        
        if score >= 80:
            reasoning['summary'] = f"Excellent match for {career['title']}!"
            reasoning['strengths'].append("Strong alignment across multiple Ikigai pillars")
        elif score >= 60:
            reasoning['summary'] = f"Good fit for {career['title']}"
            reasoning['strengths'].append("Solid foundation with growth potential")
        else:
            reasoning['summary'] = f"{career['title']} is viable with skill development"
        
        skill_gaps = self._identify_skill_gaps(user_vector, career)
        if skill_gaps:
            reasoning['growth_areas'].append(f"Learn: {', '.join(skill_gaps[:2])}")
        
        reasoning['growth_areas'].append(f"Follow the recommended learning path")
        
        return reasoning


def create_recommendation_engine():
    """Factory function to create engine instance"""
    return IkigaiRecommendationEngine()
"""
ML Engine for Ikigai Career Recommendations
This module handles all machine learning operations for career recommendations
"""

import json
from typing import Dict, List, Any
from .career_database import get_all_careers
from .nlp_processor import get_nlp_processor


class IkigaiRecommendationEngine:
    """Main recommendation engine based on Ikigai principles (Passion + Skills + Values + Market)"""
    
    def __init__(self):
        self.careers = get_all_careers()
        self.passion_weight = 0.35
        self.skill_weight = 0.30
        self.values_weight = 0.20
        self.market_weight = 0.15
        
        # Initialize NLP processor
        try:
            self.nlp_processor = get_nlp_processor()
            self.nlp_enabled = True
        except Exception as e:
            print(f"Warning: NLP processor initialization failed: {e}")
            self.nlp_enabled = False
            self.nlp_processor = None
    
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
        if user_profile.get('passions'):
            passion_score += 50
        
        # NLP-enhanced sentiment analysis on daily entries
        if daily_entries and self.nlp_enabled:
            recent_entries = daily_entries[:30]  # Last 30 days
            
            sentiment_boost = 0
            for entry in recent_entries:
                if isinstance(entry, dict) and 'content' in entry:
                    sentiment = self.nlp_processor.analyze_sentiment(entry['content'])
                    if sentiment.get('sentiment_type') == 'positive':
                        sentiment_boost += 2
                        
            passion_score += min(sentiment_boost, 30)
        
        # Fallback to mood-based scoring if NLP not available
        if daily_entries and not self.nlp_enabled:
            recent_entries = daily_entries[:30]
            happy_count = sum(1 for e in recent_entries if isinstance(e, dict) and e.get('mood') in ['happy', 'very_happy'])
            passion_score += (happy_count / max(len(recent_entries), 1)) * 50
        
        return min(100, passion_score)
    
    def _extract_skills_score(self, user_profile, daily_entries):
        """Extract skills score from user profile and daily entries"""
        skill_score = 0
        
        # Base score from profile
        if user_profile.get('skills'):
            skill_score += 50
        
        # NLP-enhanced skill extraction from daily entries
        if daily_entries and self.nlp_enabled:
            for entry in daily_entries:
                if isinstance(entry, dict) and 'content' in entry:
                    entities = self.nlp_processor.extract_skills_and_entities(entry['content'])
                    skill_score += len(entities.get('skills', [])) * 1.5
                elif isinstance(entry, dict) and entry.get('skills_used'):
                    skill_score += len(entry['skills_used']) * 2
        
        # Fallback if NLP not available
        if daily_entries and not self.nlp_enabled:
            for entry in daily_entries:
                if isinstance(entry, dict) and entry.get('skills_used'):
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
        explanation = ""
        
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
    
    # ============ NLP-ENHANCED RECOMMENDATIONS ============
    
    def analyze_user_bio_with_nlp(self, user_bio: str) -> Dict:
        """
        Analyze user's bio using NLP to extract insights
        
        Args:
            user_bio: User's biography/profile text
            
        Returns:
            dict: Comprehensive analysis including keywords, entities, sentiment
        """
        if not self.nlp_enabled or not user_bio:
            return {}
        
        return self.nlp_processor.process_user_input(user_bio)
    
    def calculate_nlp_enhanced_career_match(self, user_profile: Dict, user_bio: str, career: Dict) -> Dict:
        """
        Calculate career match using both traditional ML and NLP
        
        Args:
            user_profile: User profile dictionary
            user_bio: User's biography text
            career: Career information dictionary
            
        Returns:
            dict: Enhanced match score with NLP insights
        """
        if not self.nlp_enabled or not user_bio or not career.get('description'):
            # Fallback to traditional matching
            user_vector = self.calculate_user_profile_vector(user_profile, [])
            return self.calculate_career_match(user_vector, career)
        
        # Get traditional score
        user_vector = self.calculate_user_profile_vector(user_profile, [])
        traditional_match = self.calculate_career_match(user_vector, career)
        
        # Get NLP-enhanced similarity
        nlp_similarity = self.nlp_processor.profile_similarity_with_career(
            user_bio, 
            career.get('description', '')
        )
        
        # Combine traditional and NLP scores (70% traditional, 30% NLP)
        combined_score = (
            traditional_match['overall_score'] * 0.7 +
            nlp_similarity['combined_score'] * 100 * 0.3
        )
        
        return {
            **traditional_match,
            'overall_score': min(100, combined_score),
            'nlp_insights': nlp_similarity,
            'matching_keywords': nlp_similarity['overlapping_keywords'],
        }
    
    def get_skill_recommendations_from_daily_entries(self, daily_entries: List[Dict]) -> List[str]:
        """
        Extract skill recommendations from daily entries using NLP
        
        Args:
            daily_entries: List of user's daily entries
            
        Returns:
            list: Recommended skills to develop
        """
        if not self.nlp_enabled or not daily_entries:
            return []
        
        mentioned_skills = set()
        for entry in daily_entries:
            if isinstance(entry, dict) and 'content' in entry:
                entities = self.nlp_processor.extract_skills_and_entities(entry['content'])
                mentioned_skills.update(entities.get('skills', []))
        
        return list(mentioned_skills)
