from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trip
from .serializers import (
    TripInputSerializer, 
    TripListSerializer, 
    TripDetailSerializer
)


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Trip-related operations, including HOS calculations and history.
    """
    queryset = Trip.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TripListSerializer
        if self.action == 'retrieve':
            return TripDetailSerializer
        return TripListSerializer

    @action(
        detail=False,
        url_path='calculate',
        url_name='calculate',
        methods=['post'],
        serializer_class=TripInputSerializer
    )
    def calculate(self, request):
        """
        Calculates an HOS-compliant route, persists it, and returns the saved trip.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
     
        trip = serializer.save()
            
        response_serializer = TripDetailSerializer(trip)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)