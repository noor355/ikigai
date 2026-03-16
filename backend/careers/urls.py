from django.urls import path
from .views import CareerListView, CareerDetailView

urlpatterns = [
    path('', CareerListView.as_view(), name='career-list'),
    path('<int:career_id>/', CareerDetailView.as_view(), name='career-detail'),
]
