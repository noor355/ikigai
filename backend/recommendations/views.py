from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Recommendation, RecommendationHistory
from .serializers import RecommendationSerializer, RecommendationHistorySerializer

class RecommendationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's career recommendations"""
        recommendations = Recommendation.objects.filter(user=request.user)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)


class RecommendationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, recommendation_id):
        """Get specific recommendation details"""
        try:
            recommendation = Recommendation.objects.get(id=recommendation_id, user=request.user)
            serializer = RecommendationSerializer(recommendation)
            return Response(serializer.data)
        except Recommendation.DoesNotExist:
            return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)


class RecommendationHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get recommendation history - shows how recommendations evolved over time"""
        history = RecommendationHistory.objects.filter(user=request.user).order_by('-created_at')
        serializer = RecommendationHistorySerializer(history, many=True)
        return Response(serializer.data)


class GenerateRecommendationsView(APIView):
    """
    Generate or update recommendations for the user based on their profile and daily entries
    This will be integrated with the ML engine
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Trigger recommendation generation/refresh"""
        # This will call the ML recommendation engine
        return Response({
            'message': 'Recommendations generation started',
            'status': 'processing'
        })
