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
        
        # NLP processor disabled for performance - can be enabled later
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
        
        education_level = getattr(user_profile, 'education_level', None) or ''
        education = education_level.lower() if education_level else ''
        
        if 'phd' in education:
            score += 20
        elif 'master' in education:
            score += 15
        elif 'bachelor' in education:
            score += 10
        
        years = getattr(user_profile, 'work_experience_years', 0) or 0
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
