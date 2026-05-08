"""
ML Engine for Ikigai Career Recommendations
Analyzes user profile and daily entries to recommend future-oriented careers
"""

from typing import Dict, List, Any
from .career_database import get_all_careers
from .nlp_processor import NLPProcessor
from .trainer import ModelTrainer

class IkigaiRecommendationEngine:
    """Main recommendation engine based on Ikigai framework"""
    
    def __init__(self):
        self.careers = get_all_careers()
        self.passion_weight = 0.35
        self.skill_weight = 0.30
        self.values_weight = 0.20
        self.market_weight = 0.15
        
        # Initialize NLP processor on startup
        print("[ENGINE] Initializing NLP processor...")
        self.nlp_enabled = True
        try:
            self.nlp_processor = NLPProcessor()
            # Initialize Trainer for TF-IDF Similarity
            print("[ENGINE] Initializing model trainer...")
            self.trainer = ModelTrainer()
            # ALWAYS refresh model from database to ensure new careers are indexed
            print("[ENGINE] Refreshing TF-IDF model from career database...")
            self.trainer.train_from_career_database(self.careers)
            self.trainer.save_model()
            print("[ENGINE] Model trainer initialized and model updated")
        except Exception as e:
            print(f"[ENGINE] Failed to initialize NLP Processor: {e}")
            self.nlp_enabled = False
            self.nlp_processor = None
            self.trainer = None
    
    def analyze_user_profile(self, user_profile, daily_entries):
        """
        Comprehensive user profile analysis based on Ikigai pillars
        
        Tailored for Teens: Focuses on Passion, Skills, and Values.
        Market Readiness (Education/Work Exp) is hidden/removed as it's less relevant for teenagers.
        
        Returns: User vector with scores
        """
        passion_score = self._score_passion(user_profile, daily_entries)
        skills_score = self._score_skills(user_profile, daily_entries)
        values_score = self._score_values(user_profile, daily_entries)
        
        # Teen mode: We keep this at 0 internally but ignore it for the overall average
        market_readiness = 0.0 
        
        return {
            'passion_score': passion_score,
            'skills_score': skills_score,
            'values_score': values_score,
            'market_readiness': market_readiness,
            'passion_keywords': self._extract_dynamic_keywords(user_profile, daily_entries, 'interests'),
            'skill_keywords': self._extract_dynamic_keywords(user_profile, daily_entries, 'skills'),
            'value_keywords': self._extract_dynamic_keywords(user_profile, daily_entries, 'values'),
            'overall_readiness': (passion_score + skills_score + values_score) / 3,
        }
    
    def _extract_dynamic_keywords(self, user_profile, daily_entries, profile_attr) -> List[str]:
        """Extract keywords from both profile and daily entries for a specific pillar"""
        keywords = set()
        
        # 1. Start with profile keywords
        profile_data = getattr(user_profile, profile_attr, [])
        if isinstance(profile_data, list):
            for item in profile_data:
                keywords.add(item.lower())
        elif isinstance(profile_data, str) and profile_data:
            keywords.add(profile_data.lower())
            
        # 2. Add keywords from daily entries if NLP is enabled
        if self.nlp_enabled and self.nlp_processor and daily_entries:
            # Look at last 10 entries for fresh context
            recent_texts = [e.notes for e in daily_entries[-10:] if hasattr(e, 'notes') and e.notes]
            if recent_texts:
                combined_text = " ".join(recent_texts)
                extracted = self.nlp_processor.extract_keywords(combined_text, top_k=15)
                for word in extracted:
                    keywords.add(word.lower())
                    
        return list(keywords)

    def _score_passion(self, user_profile, daily_entries) -> float:
        """Calculate passion score 0-100"""
        score = 0
        
        has_data = False
        if hasattr(user_profile, 'passion_areas') and user_profile.passion_areas:
            score += 40
            has_data = True
        if hasattr(user_profile, 'interests') and user_profile.interests:
            score += 30
            has_data = True
        
        # Analyze daily entries using NLP if enabled
        if daily_entries:
            has_data = True
            # BASELINE for activity
            score = max(score, 50)
            if self.nlp_enabled and self.nlp_processor:
                # Combine last 5 entries for a sentiment snapshot
                recent_texts = [e.notes for e in daily_entries[-5:] if hasattr(e, 'notes') and e.notes]
                if recent_texts:
                    sentiments = [self.nlp_processor.analyze_sentiment(text) for text in recent_texts]
                    positive_count = sum(1 for s in sentiments if s.get('sentiment_type') == 'positive')
                    # Increase impact of positive engagement
                    score += (positive_count / len(recent_texts)) * 50
            else:
                # Fallback to categorical mood field
                positive_moods = sum(1 for e in daily_entries[-30:] 
                                    if hasattr(e, 'mood') and e.mood in ['happy', 'very_happy', 'excited'])
                if len(daily_entries) > 0:
                    score += (positive_moods / len(daily_entries[-30:])) * 50
        
        return min(100, score) if has_data else 0.0

    def _score_skills(self, user_profile, daily_entries) -> float:
        """Calculate skills score 0-100"""
        score = 0
        has_data = False
        
        if hasattr(user_profile, 'skills') and user_profile.skills:
            skill_count = len(user_profile.skills) if isinstance(user_profile.skills, list) else 0
            if skill_count > 0:
                score += min(skill_count * 15, 60)
                has_data = True
        
        if hasattr(user_profile, 'work_experience_years') and user_profile.work_experience_years:
            years = user_profile.work_experience_years
            if years > 0:
                score += min(years * 10, 40)
                has_data = True
        
        # Check if skills mentioned in daily entries
        if daily_entries and not has_data:
            score = 30
            has_data = True

        return min(100, score) if has_data else 0.0

    def _score_values(self, user_profile, daily_entries) -> float:
        """Calculate values alignment score 0-100"""
        score = 0
        has_data = False
        
        if hasattr(user_profile, 'values') and user_profile.values:
            value_count = len(user_profile.values) if isinstance(user_profile.values, list) else 0
            if value_count > 0:
                score += min(value_count * 20, 100)
                has_data = True
        
        if daily_entries and not has_data:
            score = 40
            has_data = True
        
        return min(100, score) if has_data else 0.0

    def _score_market_readiness(self, user_profile) -> float:
        """Calculate market readiness score 0-100"""
        score = 0
        has_data = False
        
        education_level = getattr(user_profile, 'education_level', None) or ''
        education = education_level.lower() if education_level else ''
        
        if education:
            has_data = True
            if 'phd' in education:
                score += 60
            elif 'master' in education:
                score += 40
            elif 'bachelor' in education:
                score += 20
        
        years = getattr(user_profile, 'work_experience_years', 0) or 0
        if years > 0:
            has_data = True
            score += min(years * 10, 40)
        
        return min(100, score) if has_data else 0.0
    
    def _extract_keywords(self, user_profile, attr_name) -> List[str]:
        """Extract keywords from user profile"""
        if hasattr(user_profile, attr_name):
            attr = getattr(user_profile, attr_name)
            if isinstance(attr, list):
                return attr[:15]
        return []
    
    def find_matching_careers(self, user_vector: Dict, top_n: int = 5, context_boost: Dict = None) -> List[Dict]:
        """
        Find best matching careers based on user profile and optional context boost from Coach
        
        Args:
            user_vector: Analyzed user profile
            top_n: Number of results
            context_boost: Dict with 'passions', 'skills', 'values' from expert analysis
            
        Returns: List of top matching careers with scores and reasoning
        """
        matches = []
        
        # New: Get TF-IDF similarities from Trainer (from notebook approach)
        tfidf_scores = {}
        if self.nlp_enabled and self.trainer:
            # Combine standard keywords with context boost keywords if provided
            boost_keywords = []
            if context_boost:
                boost_keywords = [
                    *context_boost.get('passions', []),
                    *context_boost.get('skills', []),
                    *context_boost.get('values', [])
                ]

            combined_queries = " ".join([
                *user_vector.get('passion_keywords', []),
                *user_vector.get('skill_keywords', []),
                *user_vector.get('value_keywords', []),
                *boost_keywords
            ])
            recs = self.trainer.get_recommendations(combined_queries, top_n=50)
            tfidf_scores = {r['career']: r['score'] for r in recs}
        
        for career in self.careers:
            match_score = self._calculate_career_match(user_vector, career)
            attribution_reasons = []
            
            # Boost score based on TF-IDF similarity (up to +40 points)
            tfidf_sim = tfidf_scores.get(career['title'], 0)
            if tfidf_sim > 0.1: # Significant match
                match_score += (tfidf_sim * 40)
                # Find which keyword matched best for attribution
                career_terms = set([k.lower() for k in career.get('passion_keywords', []) + career.get('skill_keywords', [])])
                user_terms = [k.lower() for k in user_vector.get('passion_keywords', [])]
                overlap = [t for t in user_terms if t in career_terms]
                if overlap:
                    attribution_reasons.append(f"matched your interest in {overlap[0]}")
            
            # Apply direct boost for 'Expert Override' pillars (Coach Signal)
            if context_boost:
                boost_weight = 5.0 # points per matching keyword
                boost_found = False
                for k in context_boost.get('passions', []):
                    if k.lower() in [pk.lower() for pk in career.get('passion_keywords', [])]:
                        match_score += boost_weight
                        boost_found = True
                for k in context_boost.get('skills', []):
                    if k.lower() in [sk.lower() for sk in career.get('skill_keywords', [])]:
                        match_score += boost_weight
                        boost_found = True
                
                if boost_found:
                    attribution_reasons.append("aligned with your recent conversation with Coach")

            # Construct attribution string
            attribution = ""
            if attribution_reasons:
                attribution = "Expert Tip: Boosted because this " + " and ".join(attribution_reasons) + "."
            elif tfidf_sim > 0.2:
                attribution = "Expert Tip: High semantic match with your recent journal entries."

            reasoning = self._generate_reasoning(user_vector, career, match_score)
            skill_gaps = self._identify_skill_gaps(user_vector, career)
            
            matches.append({
                'career_id': career['id'],
                'title': career['title'],
                'description': career['description'],
                'match_score': min(100, round(match_score, 1)),
                'reasoning': reasoning,
                'attribution': attribution,
                'skill_gaps': skill_gaps,
                'learning_path': career.get('learning_path', []),
                'salary_range': career.get('salary_range', (0, 0)),
                'growth_potential': career.get('growth_potential'),
                'market_demand': career.get('market_demand'),
                'future_relevance': career.get('future_relevance'),
                'required_skills': career.get('required_skills', []),
                'tfidf_similarity': tfidf_scores.get(career['title'], 0)
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
        # Base score from profile levels
        # Increase visibility: Use a higher baseline if there is activity
        base_score = user_score * 0.5
        
        if not career_keywords:
            return base_score + 20
        
        # Keyword overlap with semantic awareness (case insensitive)
        user_set = set([k.lower() for k in user_keywords])
        career_set = set([k.lower() for k in career_keywords])
        
        if not user_set:
            return base_score
            
        overlap = len(user_set & career_set)
        
        # Expert Tuning: If user keywords overlap with career keywords, give a MUCH larger boost
        if overlap > 0:
            # Overlap score captures how many career keywords we hit
            overlap_score = (overlap / len(career_set)) * 80 if career_set else 40
            # Matching bonus based on total overlap to reward specificity
            bonus = min(overlap * 15, 40)
            return min(100, base_score + overlap_score + bonus)
        
        return base_score
    
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


# Singleton instance
_engine_instance = None

def create_recommendation_engine():
    """Factory function to get or create engine instance (Singleton)"""
    global _engine_instance
    if _engine_instance is None:
        print("Initializing Global Recommendation Engine (This may take a minute first time)...")
        _engine_instance = IkigaiRecommendationEngine()
    return _engine_instance

