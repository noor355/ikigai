from django.urls import path
from .views import (
    RecommendationListView,
    RecommendationDetailView,
    RecommendationHistoryView,
    GenerateRecommendationsView
)

urlpatterns = [
    path('', RecommendationListView.as_view(), name='recommendation-list'),
    path('<int:recommendation_id>/', RecommendationDetailView.as_view(), name='recommendation-detail'),
    path('history/', RecommendationHistoryView.as_view(), name='recommendation-history'),
    path('generate/', GenerateRecommendationsView.as_view(), name='generate-recommendations'),
]
