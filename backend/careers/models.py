from django.db import models

class Career(models.Model):
    """Career opportunities aligned with Ikigai"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    average_salary = models.DecimalField(max_digits=12, decimal_places=2)
    job_market_demand = models.CharField(
        max_length=20,
        choices=[
            ('very_high', 'Very High'),
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ]
    )
    growth_rate = models.FloatField()  # Annual growth percentage
    education_required = models.CharField(max_length=100)
    future_oriented = models.BooleanField(default=True)  # Is this a future-oriented career?
    industry = models.CharField(max_length=100)
    
    # Ikigai alignment factors
    passion_tags = models.JSONField(default=list)  # What passions align with this
    social_impact = models.TextField()  # Social value/world needs
    sustainability = models.CharField(max_length=20, choices=[
        ('highly_sustainable', 'Highly Sustainable'),
        ('sustainable', 'Sustainable'),
        ('emerging', 'Emerging'),
        ('declining', 'Declining'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-growth_rate']
    
    def __str__(self):
        return self.title
