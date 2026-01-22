from rest_framework import serializers
from django.db import transaction
from .models import Trip, LogEntry, RouteStop
from . import utils


class TripInputSerializer(serializers.Serializer):
    current_location = serializers.CharField(max_length=255)
    pickup_location = serializers.CharField(max_length=255)
    dropoff_location = serializers.CharField(max_length=255)
    current_cycle_used = serializers.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        min_value=0, 
        max_value=70
    )

    def create(self, validated_data):
        # 1. Perform HOS calculation
        result = utils.calculate_route_with_hos(
            current_location=validated_data['current_location'],
            pickup_location=validated_data['pickup_location'],
            dropoff_location=validated_data['dropoff_location'],
            current_cycle_used=validated_data['current_cycle_used']
        )
        
        # 2. Persist the results in a transaction
        with transaction.atomic():
            # Create the Trip
            trip = Trip.objects.create(
                current_location=validated_data['current_location'],
                current_lat=result['route_summary']['current_coords']['lat'],
                current_lon=result['route_summary']['current_coords']['lon'],
                pickup_location=validated_data['pickup_location'],
                pickup_lat=result['route_summary']['pickup_coords']['lat'],
                pickup_lon=result['route_summary']['pickup_coords']['lon'],
                dropoff_location=validated_data['dropoff_location'],
                dropoff_lat=result['route_summary']['dropoff_coords']['lat'],
                dropoff_lon=result['route_summary']['dropoff_coords']['lon'],
                current_cycle_used=validated_data['current_cycle_used'],
                total_distance=result['route_summary']['total_distance'],
                route_geometry=result['route_summary']['route_geometry']
            )
            
            # Create Log Entries
            log_entries = [
                LogEntry(
                    trip=trip,
                    duty_status=entry['duty_status'],
                    start_time=entry['start_time'],
                    end_time=entry['end_time'],
                    location=entry['location'],
                    notes=entry.get('notes')
                )
                for entry in result['log_entries']
            ]
            LogEntry.objects.bulk_create(log_entries)
            
            # Create Route Stops
            route_stops = [
                RouteStop(
                    trip=trip,
                    stop_type=stop['stop_type'],
                    location=stop['location'],
                    latitude=stop.get('latitude'),
                    longitude=stop.get('longitude'),
                    arrival_time=stop['arrival_time'],
                    duration_minutes=stop['duration_minutes'],
                    description=stop.get('description')
                )
                for stop in result['stops']
            ]
            RouteStop.objects.bulk_create(route_stops)
            
        return trip


class LogEntrySerializer(serializers.ModelSerializer):
    duration_hours = serializers.ReadOnlyField()

    class Meta:
        model = LogEntry
        fields = [
            'duty_status', 
            'start_time', 
            'end_time', 
            'location', 
            'duration_hours', 
            'notes'
        ]


class RouteStopSerializer(serializers.ModelSerializer):
    stop_type_display = serializers.CharField(source='get_stop_type_display', read_only=True)

    class Meta:
        model = RouteStop
        fields = [
            'stop_type', 
            'stop_type_display', 
            'location', 
            'latitude',
            'longitude',
            'arrival_time', 
            'duration_minutes', 
            'description'
        ]


class DailyLogSheetSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_miles_driving = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_mileage_today = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    # Grid totals (exactly 24 hours total)
    total_off_duty = serializers.FloatField(default=0.0)
    total_sleeper = serializers.FloatField(default=0.0)
    total_driving = serializers.FloatField(default=0.0)
    total_on_duty = serializers.FloatField(default=0.0)
    
    log_entries = LogEntrySerializer(many=True)
    remarks = serializers.CharField(required=False, allow_blank=True)
    recap = serializers.DictField(required=False, help_text="HOS Recap data")


class TripListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            'id', 
            'current_location', 
            'pickup_location', 
            'dropoff_location', 
            'current_cycle_used', 
            'created_at'
        ]


class TripDetailSerializer(serializers.ModelSerializer):
    log_entries = LogEntrySerializer(many=True, read_only=True)
    stops = RouteStopSerializer(many=True, read_only=True)
    daily_logs = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'id', 
            'current_location',
            'current_lat',
            'current_lon',
            'pickup_location',
            'pickup_lat',
            'pickup_lon',
            'dropoff_location',
            'dropoff_lat',
            'dropoff_lon',
            'current_cycle_used', 
            'log_entries', 
            'stops', 
            'daily_logs',
            'route_geometry',
            'created_at'
        ]

    def get_daily_logs(self, obj):
        from .utils import generate_daily_log_sheets
        import dateutil.parser
        
        # We need to re-hydrate the log entries for the utility
        # In a real app, we might store the daily logs or compute them more efficiently
        log_entries_data = LogEntrySerializer(obj.log_entries.all(), many=True).data
        for entry in log_entries_data:
            entry['start_time'] = dateutil.parser.parse(entry['start_time'])
            entry['end_time'] = dateutil.parser.parse(entry['end_time'])
            
        return DailyLogSheetSerializer(
            generate_daily_log_sheets(log_entries_data, obj.total_distance),
            many=True
        ).data
