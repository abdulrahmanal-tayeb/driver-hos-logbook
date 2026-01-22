from django.contrib import admin
from .models import DailyLog, ShippingDocument, Trip, LogEntry, RouteStop


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'log_date', 'log_type', 'from_location', 'to_location', 'created_at']
    list_filter = ['log_type', 'log_date']
    search_fields = ['from_location', 'to_location', 'carrier_name']
    date_hierarchy = 'log_date'


@admin.register(ShippingDocument)
class ShippingDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'bill_of_lading_number', 'daily_log', 'shipper_name', 'created_at']
    list_filter = ['daily_log']
    search_fields = ['bill_of_lading_number', 'shipper_name', 'commodity']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'current_location', 'pickup_location', 'dropoff_location', 'current_cycle_used', 'total_distance', 'created_at']
    list_filter = ['created_at']
    search_fields = ['current_location', 'pickup_location', 'dropoff_location']
    date_hierarchy = 'created_at'
    readonly_fields = ['route_geometry']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'duty_status', 'start_time', 'end_time', 'location']
    list_filter = ['duty_status', 'start_time']
    search_fields = ['location', 'notes']
    date_hierarchy = 'start_time'


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'stop_type', 'location', 'arrival_time', 'duration_minutes']
    list_filter = ['stop_type', 'arrival_time']
    search_fields = ['location', 'description']
    date_hierarchy = 'arrival_time'

