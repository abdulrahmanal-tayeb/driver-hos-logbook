from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from .models import DailyLog, Trip

class TripViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.log = DailyLog.objects.create(log_date=timezone.now().date())
        self.trip = Trip.objects.create(
            daily_log=self.log,
            current_location="Los Angeles, CA",
            pickup_location="Phoenix, AZ",
            dropoff_location="Dallas, TX",
            current_cycle_used=10.0
        )

    def test_list_trips(self):
        """Test GET /api/v1/logbook/trips/"""
        url = reverse('trip-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['current_location'], "Los Angeles, CA")

    @patch('driver_hos_logbook.apps.driver_hos_logbook.utils.calculate_route_with_hos')
    def test_calculate_trip(self, mock_calculate):
        """Test POST /api/v1/logbook/trips/calculate/"""
        # Mocking the heavy calculation logic
        mock_calculate.return_value = {
            'route_summary': {
                'total_distance': 1200.0,
                'total_time_hours': 24.0,
                'start_time': timezone.now(),
                'end_time': timezone.now() + timezone.timedelta(days=1),
                'route_geometry': {'type': 'FeatureCollection', 'features': []},
                'current_coords': {"lat": 34.0, "lon": -118.0},
                'pickup_coords': {"lat": 33.0, "lon": -112.0},
                'dropoff_coords': {"lat": 32.0, "lon": -96.0}
            },
            'stops': [],
            'log_entries': [],
            'daily_logs': []
        }

        data = {
            "current_location": "Los Angeles, CA",
            "pickup_location": "Phoenix, AZ",
            "dropoff_location": "Dallas, TX",
            "current_cycle_used": 10.0
        }
        
        url = reverse('trip-calculate')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Trip.objects.count(), 2) # 1 from setUp, 1 from this POST
