"""
Integration layer between Django backend and ML engine
"""

from django.contrib.auth.models import User
from users.models import UserProfile, DailyEntry
from careers.models import Career
from recommendations.models import Recommendation, RecommendationHistory
from .recommendation_engine import IkigaiRecommendationEngine
import json


class RecommendationService:
    """Service to orchestrate recommendation generation"""
    
    def __init__(self):
        self.engine = IkigaiRecommendationEngine()
    
    def generate_recommendations_for_user(self, user):
        """Generate or update recommendations for a specific user"""
        
        # Get user profile
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return {'error': 'User profile not found'}
        
        # Get user's daily entries
        daily_entries = DailyEntry.objects.filter(user=user).order_by('-date')
        entries_data = [
            {
                'mood': entry.mood,
                'skills_used': entry.skills_used,
                'learnings': entry.learnings,
            }
            for entry in daily_entries
        ]
        
        # Create profile vector
        user_profile_data = {
            'passions': user_profile.passions,
            'skills': user_profile.skills,
            'values': user_profile.values,
            'years_of_experience': user_profile.years_of_experience,
            'education_level': user_profile.education_level,
        }
        
        user_vector = self.engine.calculate_user_profile_vector(user_profile_data, entries_data)
        
        # Get all careers and calculate match scores
        careers = Career.objects.all()
        recommendations_data = []
        
        for career in careers:
            career_data = {
                'passion_tags': career.passion_tags,
                'required_skills': career.required_skills,
                'job_market_demand': career.job_market_demand,
                'growth_rate': career.growth_rate,
                'sustainability': career.sustainability,
            }
            
            match_scores = self.engine.calculate_career_match(user_vector, career_data)
            reason = self.engine.generate_explanation(user.username, career.title, match_scores)
            
            recommendations_data.append({
                'career': career,
                'match_scores': match_scores,
                'reason': reason,
            })
        
        # Sort by overall score
        recommendations_data.sort(key=lambda x: x['match_scores']['overall_score'], reverse=True)
        
        # Save recommendations
        for rec_data in recommendations_data:
            Recommendation.objects.update_or_create(
                user=user,
                career=rec_data['career'],
                defaults={
                    'match_score': rec_data['match_scores']['overall_score'],
                    'skill_match': rec_data['match_scores']['skill_match'],
                    'passion_match': rec_data['match_scores']['passion_match'],
                    'market_fit': rec_data['match_scores']['market_fit'],
                    'growth_potential': rec_data['match_scores']['growth_potential'],
                    'reason': rec_data['reason'],
                }
            )
        
        # Save to history
        top_recommendation = recommendations_data[0] if recommendations_data else None
        if top_recommendation:
            RecommendationHistory.objects.create(
                user=user,
                top_career=top_recommendation['career'],
                top_score=top_recommendation['match_scores']['overall_score'],
                total_entries=daily_entries.count(),
            )
        
        return {
            'status': 'success',
            'recommendations_count': len(recommendations_data),
            'top_career': top_recommendation['career'].title if top_recommendation else None,
            'top_score': top_recommendation['match_scores']['overall_score'] if top_recommendation else 0,
        }
    
    def get_user_insights(self, user):
        """Generate insights about user's Ikigai journey"""
        try:
            user_profile = UserProfile.objects.get(user=user)
            daily_entries = DailyEntry.objects.filter(user=user)
            recommendations = Recommendation.objects.filter(user=user).order_by('-match_score')[:5]
            
            # Calculate statistics
            total_entries = daily_entries.count()
            avg_mood = self._calculate_average_mood(daily_entries)
            top_skills = self._extract_top_skills(daily_entries)
            
            return {
                'total_entries': total_entries,
                'passions': user_profile.passions,
                'skills': user_profile.skills,
                'values': user_profile.values,
                'average_mood': avg_mood,
                'top_skills_used': top_skills,
                'top_recommendations': [r.career.title for r in recommendations],
            }
        except UserProfile.DoesNotExist:
            return {'error': 'User profile not found'}
    
    def _calculate_average_mood(self, entries):
        """Calculate average mood from daily entries"""
        if not entries:
            return None
        
        mood_values = {
            'very_happy': 5,
            'happy': 4,
            'neutral': 3,
            'sad': 2,
            'very_sad': 1,
        }
        
        total = sum(mood_values.get(entry.mood, 3) for entry in entries)
        avg = total / entries.count()
        
        mood_map = {5: 'Very Happy', 4: 'Happy', 3: 'Neutral', 2: 'Sad', 1: 'Very Sad'}
        return mood_map.get(round(avg), 'Neutral')
    
    def _extract_top_skills(self, entries, limit=5):
        """Extract most frequently used skills from daily entries"""
        skill_count = {}
        
        for entry in entries:
            for skill in entry.skills_used:
                skill_count[skill] = skill_count.get(skill, 0) + 1
        
        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        return [skill for skill, count in sorted_skills[:limit]]
