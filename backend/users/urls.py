from django.urls import path
from .views import UserProfileView, DailyEntryView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('daily-entries/', DailyEntryView.as_view(), name='daily-entries'),
]
