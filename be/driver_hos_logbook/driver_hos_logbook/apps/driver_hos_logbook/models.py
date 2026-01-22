from django.db import models
from django.utils.translation import gettext_lazy as _
from driver_hos_logbook.base.models import BaseModel


class DutyStatus(models.TextChoices):
    OFF_DUTY = 'OFF_DUTY', _('Off Duty')
    SLEEPER_BERTH = 'SLEEPER_BERTH', _('Sleeper Berth')
    DRIVING = 'DRIVING', _('Driving')
    ON_DUTY_NOT_DRIVING = 'ON_DUTY_NOT_DRIVING', _('On Duty (Not Driving)')


class DailyLog(BaseModel):
    class LogType(models.TextChoices):
        ORIGINAL = 'ORIGINAL', _('Original')
        DUPLICATE = 'DUPLICATE', _('Duplicate')

    log_date = models.DateField()
    log_type = models.CharField(
        max_length=20, 
        choices=LogType.choices,
        default=LogType.ORIGINAL
    )
    
    # Daily From/To (different from individual trip locations)
    from_location = models.CharField(max_length=255, blank=True)
    to_location = models.CharField(max_length=255, blank=True)
    
    # Daily Mileage
    total_miles_driving_today = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_mileage_today = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Vehicle Information
    truck_tractor_number = models.CharField(max_length=100, blank=True)
    trailer_numbers = models.JSONField(default=list, help_text=_("List of trailer numbers"))
    license_plate = models.CharField(max_length=50, blank=True)
    license_state = models.CharField(max_length=2, blank=True)
    
    # Carrier Information
    carrier_name = models.CharField(max_length=255, blank=True)
    main_office_address = models.TextField(blank=True)
    home_terminal_address = models.TextField(blank=True)
    
    # Remarks
    remarks = models.TextField(blank=True)
    
    # Recap Data (can be calculated but also stored for audit purposes)
    recap_data = models.JSONField(default=dict, help_text=_("Daily recap calculations"))

    def __str__(self):
        return f"Daily Log for {self.log_date}"


class ShippingDocument(BaseModel):
    daily_log = models.ForeignKey(
        DailyLog, 
        on_delete=models.CASCADE, 
        related_name='shipping_documents'
    )
    bill_of_lading_number = models.CharField(max_length=100)
    shipper_name = models.CharField(max_length=255, blank=True)
    commodity = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"BOL {self.bill_of_lading_number} for {self.daily_log}"


class Trip(BaseModel):
    daily_log = models.ForeignKey(
        DailyLog, 
        on_delete=models.CASCADE, 
        related_name='trips',
        null=True,
        blank=True
    )
    current_location = models.CharField(max_length=255)
    current_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    pickup_location = models.CharField(max_length=255)
    pickup_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    dropoff_location = models.CharField(max_length=255)
    dropoff_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    current_cycle_used = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text=_("Hours used in the current 70-hour/8-day cycle")
    )
    total_distance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text=_("Total calculated distance in miles")
    )
    route_geometry = models.JSONField(null=True, blank=True, help_text=_("OSRM route geometry coordinates"))

    def __str__(self):
        return f"Trip from {self.current_location} to {self.dropoff_location}"


class LogEntry(BaseModel):
    trip = models.ForeignKey(
        Trip, 
        on_delete=models.CASCADE, 
        related_name='log_entries'
    )
    duty_status = models.CharField(
        max_length=20, 
        choices=DutyStatus.choices
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Log entries"
        ordering = ['start_time']

    @property
    def duration_hours(self):
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600

    def __str__(self):
        return f"{self.duty_status} ({self.start_time} - {self.end_time})"


class RouteStop(BaseModel):
    class StopType(models.TextChoices):
        PICKUP = 'PICKUP', _('Pickup')
        DROPOFF = 'DROPOFF', _('Dropoff')
        FUEL = 'FUEL', _('Fueling')
        BREAK = 'BREAK', _('30-Minute Break')
        REST = 'REST', _('10-Hour Rest')

    trip = models.ForeignKey(
        Trip, 
        on_delete=models.CASCADE, 
        related_name='stops'
    )
    stop_type = models.CharField(
        max_length=20, 
        choices=StopType.choices
    )
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    arrival_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['arrival_time']

    def __str__(self):
        return f"{self.stop_type} at {self.location}"
