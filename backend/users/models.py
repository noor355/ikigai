from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile with Ikigai data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    years_of_experience = models.IntegerField(default=0)
    
    # Ikigai pillars - will be updated as user interacts
    passions = models.JSONField(default=list)  # Things they love
    skills = models.JSONField(default=list)    # What they're good at
    values = models.JSONField(default=list)    # What the world needs / social impact
    salary_expectation = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class DailyEntry(models.Model):
    """Track daily activities, emotions, and learnings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_entries')
    date = models.DateField(auto_now_add=True)
    
    mood = models.CharField(
        max_length=20,
        choices=[
            ('very_happy', 'Very Happy'),
            ('happy', 'Happy'),
            ('neutral', 'Neutral'),
            ('sad', 'Sad'),
            ('very_sad', 'Very Sad'),
        ]
    )
    
    activities = models.JSONField(default=list)  # List of activities done
    learnings = models.TextField()  # What they learned today
    challenges = models.TextField(blank=True)  # Challenges faced
    skills_used = models.JSONField(default=list)  # Skills applied
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
