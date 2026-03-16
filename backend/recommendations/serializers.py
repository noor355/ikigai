from rest_framework import serializers
from .models import Recommendation, RecommendationHistory

class RecommendationSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = '__all__'


class RecommendationHistorySerializer(serializers.ModelSerializer):
    top_career_title = serializers.CharField(source='top_career.title', read_only=True)
    
    class Meta:
        model = RecommendationHistory
        fields = '__all__'
