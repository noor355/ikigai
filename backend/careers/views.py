from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Career
from .serializers import CareerSerializer

class CareerListView(APIView):
    def get(self, request):
        """Get all careers with optional filtering"""
        careers = Career.objects.all()
        
        # Filter by industry if provided
        industry = request.query_params.get('industry')
        if industry:
            careers = careers.filter(industry__icontains=industry)
        
        # Filter by job market demand if provided
        demand = request.query_params.get('demand')
        if demand:
            careers = careers.filter(job_market_demand=demand)
        
        serializer = CareerSerializer(careers, many=True)
        return Response(serializer.data)


class CareerDetailView(APIView):
    def get(self, request, career_id):
        """Get specific career details"""
        try:
            career = Career.objects.get(id=career_id)
            serializer = CareerSerializer(career)
            return Response(serializer.data)
        except Career.DoesNotExist:
            return Response({'error': 'Career not found'}, status=status.HTTP_404_NOT_FOUND)
