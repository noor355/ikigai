from django.db import models
from django.contrib.auth.models import User
from careers.models import Career

class Recommendation(models.Model):
    """Career recommendations generated for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    
    match_score = models.FloatField()  # 0-100 score
    reason = models.TextField()  # Explanation for recommendation
    
    # Breakdown of the score
    skill_match = models.FloatField()
    passion_match = models.FloatField()
    market_fit = models.FloatField()
    growth_potential = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-match_score']
        unique_together = ('user', 'career')
    
    def __str__(self):
        return f"{self.user.username} -> {self.career.title} ({self.match_score}%)"


class RecommendationHistory(models.Model):
    """Track how recommendations change over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_history')
    top_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True)
    top_score = models.FloatField()
    total_entries = models.IntegerField()  # Number of daily entries at this point
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"
