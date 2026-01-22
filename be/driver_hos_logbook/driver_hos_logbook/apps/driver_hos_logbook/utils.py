import requests
from datetime import timedelta
from django.utils import timezone
from .models import DutyStatus, RouteStop


def geocode_location(location_name):
    """
    Geocodes a location name using Nominatim API.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "DriverHOSLogbook/1.0 (abdulrahman.m.altayeb@gmail.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "display_name": data[0]["display_name"]
            }
    except Exception as e:
        print(f"Geocoding error for {location_name}: {e}")
    return None


def get_route_data(origin_coords, dest_coords):
    """
    Fetches route distance, duration, and geometry from OSRM.
    Coords format: (lat, lon)
    """
    # OSRM expects {lon},{lat}
    url = f"https://router.project-osrm.org/route/v1/driving/{origin_coords[1]},{origin_coords[0]};{dest_coords[1]},{dest_coords[0]}"
    params = {
        "overview": "full",
        "geometries": "geojson"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["code"] == "Ok":
            route = data["routes"][0]
            return {
                "distance_miles": route["distance"] * 0.000621371,
                "duration_hours": route["duration"] / 3600,
                "geometry": route["geometry"]
            }
    except Exception as e:
        print(f"Routing error: {e}")
    return None


def calculate_route_with_hos(
    current_location, 
    pickup_location, 
    dropoff_location, 
    current_cycle_used
):
    """
    Main orchestrator for HOS-compliant route planning using real Map APIs.
    """
    # 1. Geocode all locations
    loc_current = _get_location_coords(location_name=current_location, default_lat=34.0522, default_lon=-118.2437)
    loc_pickup = _get_location_coords(location_name=pickup_location, default_lat=33.4484, default_lon=-112.0740)
    loc_dropoff = _get_location_coords(location_name=dropoff_location, default_lat=32.7767, default_lon=-96.7970)

    # 2. Get real route data
    dist_to_pickup, dur_to_pickup, geom_to_pickup = _get_segment_route(
        start_coords=(loc_current["lat"], loc_current["lon"]), 
        end_coords=(loc_pickup["lat"], loc_pickup["lon"]), 
        fallback_dist=200.0
    )
    dist_to_dropoff, dur_to_dropoff, geom_to_dropoff = _get_segment_route(
        start_coords=(loc_pickup["lat"], loc_pickup["lon"]), 
        end_coords=(loc_dropoff["lat"], loc_dropoff["lon"]), 
        fallback_dist=1000.0
    )
    
    total_distance = dist_to_pickup + dist_to_dropoff
    
    # Always create a valid GeoJSON FeatureCollection
    route_geometry = {
        "type": "FeatureCollection",
        "features": []
    }
    if geom_to_pickup:
        route_geometry["features"].append({
            "type": "Feature", 
            "geometry": geom_to_pickup, 
            "properties": {"segment": "to_pickup"}
        })
    if geom_to_dropoff:
        route_geometry["features"].append({
            "type": "Feature", 
            "geometry": geom_to_dropoff, 
            "properties": {"segment": "to_dropoff"}
        })

    # State tracking
    start_time = timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)
    state = {
        "current_time": start_time,
        "cumulative_driving_since_last_10hr_rest": 0.0,
        "cumulative_duty_since_last_10hr_rest": 0.0,
        "cumulative_driving_since_last_30min_break": 0.0,
        "cumulative_cycle_hours": float(current_cycle_used),
        "miles_since_last_fuel": 0.0,
        "log_entries": [],
    }
    stops = []
    
    # Execution
    _add_hos_log_entry(state=state, status=DutyStatus.ON_DUTY_NOT_DRIVING, duration_hrs=0.25, location=current_location, notes="Pre-trip inspection")
    _insert_hos_breaks(state=state, needed_driving_hrs=dur_to_pickup, location="En route to Pickup", stops=stops)
    
    stops.append({
        'stop_type': RouteStop.StopType.PICKUP,
        'location': pickup_location,
        'latitude': loc_pickup["lat"],
        'longitude': loc_pickup["lon"],
        'arrival_time': state['current_time'],
        'duration_minutes': 60,
        'description': 'Loading Cargo'
    })
    _add_hos_log_entry(state=state, status=DutyStatus.ON_DUTY_NOT_DRIVING, duration_hrs=1.0, location=pickup_location, notes="Loading")
    
    _insert_hos_breaks(state=state, needed_driving_hrs=dur_to_dropoff, location="En route to Dropoff", stops=stops)
    
    stops.append({
        'stop_type': RouteStop.StopType.DROPOFF,
        'location': dropoff_location,
        'latitude': loc_dropoff["lat"],
        'longitude': loc_dropoff["lon"],
        'arrival_time': state['current_time'],
        'duration_minutes': 60,
        'description': 'Unloading Cargo'
    })
    _add_hos_log_entry(state=state, status=DutyStatus.ON_DUTY_NOT_DRIVING, duration_hrs=1.0, location=dropoff_location, notes="Unloading")
    _add_hos_log_entry(state=state, status=DutyStatus.ON_DUTY_NOT_DRIVING, duration_hrs=0.25, location=dropoff_location, notes="Post-trip inspection")

    daily_logs = generate_daily_log_sheets(state['log_entries'], total_distance)
    
    return {
        'route_summary': {
            'total_distance': total_distance,
            'total_time_hours': (state['current_time'] - start_time).total_seconds() / 3600,
            'start_time': start_time,
            'end_time': state['current_time'],
            'route_geometry': route_geometry,
            'current_coords': {"lat": loc_current["lat"], "lon": loc_current["lon"]},
            'pickup_coords': {"lat": loc_pickup["lat"], "lon": loc_pickup["lon"]},
            'dropoff_coords': {"lat": loc_dropoff["lat"], "lon": loc_dropoff["lon"]}
        },
        'stops': stops,
        'log_entries': state['log_entries'],
        'daily_logs': daily_logs
    }


def generate_daily_log_sheets(log_entries, total_dist):
    """
    Groups log entries by calendar day and prepares them for the log sheet format.
    """
    if not log_entries:
        return []
        
    split_entries = []
    for entry in log_entries:
        start = entry['start_time']
        end = entry['end_time']
        while start.date() < end.date():
            next_day = start.date() + timedelta(days=1)
            midnight = timezone.make_aware(timezone.datetime.combine(next_day, timezone.datetime.min.time()))
            split_entries.append({**entry, 'start_time': start, 'end_time': midnight})
            start = midnight
        split_entries.append({**entry, 'start_time': start, 'end_time': end})

    daily_groups = {}
    for entry in split_entries:
        d = entry['start_time'].date()
        if d not in daily_groups: daily_groups[d] = []
        daily_groups[d].append(entry)
        
    result = []
    sorted_dates = sorted(daily_groups.keys())
    total_driving_hrs = sum((e['end_time'] - e['start_time']).total_seconds() / 3600 
                           for e in split_entries if e['duty_status'] == DutyStatus.DRIVING)
    
    for i, d in enumerate(sorted_dates):
        day_entries = daily_groups[d]
        
        # Calculate daily aggregates for the 4-line grid
        total_off = sum((e['end_time'] - e['start_time']).total_seconds() / 3600 for e in day_entries if e['duty_status'] == DutyStatus.OFF_DUTY)
        total_sleeper = sum((e['end_time'] - e['start_time']).total_seconds() / 3600 for e in day_entries if e['duty_status'] == DutyStatus.SLEEPER_BERTH)
        total_driving = sum((e['end_time'] - e['start_time']).total_seconds() / 3600 for e in day_entries if e['duty_status'] == DutyStatus.DRIVING)
        total_on_duty = sum((e['end_time'] - e['start_time']).total_seconds() / 3600 for e in day_entries if e['duty_status'] == DutyStatus.ON_DUTY_NOT_DRIVING)

        day_driving_hrs = total_driving
        day_miles = (day_driving_hrs / total_driving_hrs * float(total_dist)) if total_driving_hrs > 0 else 0
        
        # Calculate Recap
        on_duty_today = total_driving + total_on_duty
        
        result.append({
            'date': d,
            'total_miles_driving': round(day_miles, 2),
            'total_mileage_today': round(day_miles, 2),
            'total_off_duty': round(total_off, 2),
            'total_sleeper': round(total_sleeper, 2),
            'total_driving': round(total_driving, 2),
            'total_on_duty': round(total_on_duty, 2),
            'log_entries': day_entries,
            'remarks': f"Day {i+1} of trip",
            'recap': {
                'on_duty_today': round(on_duty_today, 2),
                # In a real app, we'd look back at previous trips for the 70/8 rule
                'total_last_8_days': round(on_duty_today, 2), # Simplified
                'available_tomorrow': round(70.0 - on_duty_today, 2) # Simplified
            }
        })
    return result


def _get_location_coords(*, location_name, default_lat, default_lon):
    """
    Geocodes a location name with fallback coordinates.
    """
    loc = geocode_location(location_name)
    if loc:
        return loc
    return {"lat": default_lat, "lon": default_lon}


def _get_segment_route(*, start_coords, end_coords, fallback_dist):
    """
    Fetches route data with fallback if routing fails.
    """
    route = get_route_data(start_coords, end_coords)
    dist = route["distance_miles"] if route else fallback_dist
    dur = route["duration_hours"] if route else (dist / 55)
    geometry = route.get("geometry") if route else None
    return dist, dur, geometry


def _add_hos_log_entry(
    *, 
    state, 
    status, 
    duration_hrs, 
    location, 
    notes=None
):
    """
    Adds a log entry and updates HOS state.
    """
    start_time = state['current_time']
    end_time = start_time + timedelta(hours=duration_hrs)
    
    state['log_entries'].append({
        'duty_status': status,
        'start_time': start_time,
        'end_time': end_time,
        'location': location,
        'notes': notes
    })
    
    if status == DutyStatus.DRIVING:
        state['cumulative_driving_since_last_10hr_rest'] += duration_hrs
        state['cumulative_driving_since_last_30min_break'] += duration_hrs
        state['cumulative_duty_since_last_10hr_rest'] += duration_hrs
        state['cumulative_cycle_hours'] += duration_hrs
    elif status == DutyStatus.ON_DUTY_NOT_DRIVING:
        state['cumulative_duty_since_last_10hr_rest'] += duration_hrs
        state['cumulative_cycle_hours'] += duration_hrs
    
    if (status in [DutyStatus.OFF_DUTY, DutyStatus.SLEEPER_BERTH]) and duration_hrs >= 10:
        state['cumulative_driving_since_last_10hr_rest'] = 0
        state['cumulative_duty_since_last_10hr_rest'] = 0
        state['cumulative_driving_since_last_30min_break'] = 0
        if duration_hrs >= 34:
            state['cumulative_cycle_hours'] = 0
    
    if (status in [DutyStatus.OFF_DUTY, DutyStatus.SLEEPER_BERTH, DutyStatus.ON_DUTY_NOT_DRIVING]) and duration_hrs >= 0.5:
        state['cumulative_driving_since_last_30min_break'] = 0

    state['current_time'] = end_time


def _insert_hos_breaks(
    *, 
    state, 
    needed_driving_hrs, 
    location, 
    stops
):
    """
    Checks for HOS violations and inserts necessary breaks during driving.
    """
    remaining_to_drive = needed_driving_hrs
    avg_speed = 55 # Used for fuel estimation
    
    while remaining_to_drive > 0:
        # Requirement: 70hrs/8days rule
        if state['cumulative_cycle_hours'] >= 70:
            stops.append({
                'stop_type': RouteStop.StopType.REST,
                'location': location,
                'arrival_time': state['current_time'],
                'duration_minutes': 34 * 60,
                'description': '34-Hour Cycle Restart'
            })
            _add_hos_log_entry(
                state=state, 
                status=DutyStatus.OFF_DUTY, 
                duration_hrs=34, 
                location=location, 
                notes="34-Hour Restart"
            )
            continue

        avail_driving = 11.0 - state['cumulative_driving_since_last_10hr_rest']
        avail_duty = 14.0 - state['cumulative_duty_since_last_10hr_rest']
        avail_before_break = 8.0 - state['cumulative_driving_since_last_30min_break']
        
        can_drive = min(remaining_to_drive, avail_driving, avail_duty, avail_before_break)
        
        # Requirement: Fueling at least once every 1,000 miles
        miles_to_fuel = 1000 - state['miles_since_last_fuel']
        hours_to_fuel = miles_to_fuel / avg_speed
        can_drive = min(can_drive, hours_to_fuel)

        if can_drive > 0:
            _add_hos_log_entry(
                state=state, 
                status=DutyStatus.DRIVING, 
                duration_hrs=can_drive, 
                location=location
            )
            remaining_to_drive -= can_drive
            state['miles_since_last_fuel'] += (can_drive * avg_speed)
        
        if remaining_to_drive > 0:
            if state['miles_since_last_fuel'] >= 1000:
                stops.append({
                    'stop_type': RouteStop.StopType.FUEL,
                    'location': location,
                    'arrival_time': state['current_time'],
                    'duration_minutes': 15,
                    'description': 'Fueling Stop'
                })
                _add_hos_log_entry(
                    state=state, 
                    status=DutyStatus.ON_DUTY_NOT_DRIVING, 
                    duration_hrs=0.25, 
                    location=location, 
                    notes="Fueling"
                )
                state['miles_since_last_fuel'] = 0
            elif state['cumulative_driving_since_last_30min_break'] >= 8:
                stops.append({
                    'stop_type': RouteStop.StopType.BREAK,
                    'location': location,
                    'arrival_time': state['current_time'],
                    'duration_minutes': 30,
                    'description': '30-Minute Rest Break'
                })
                _add_hos_log_entry(
                    state=state, 
                    status=DutyStatus.OFF_DUTY, 
                    duration_hrs=0.5, 
                    location=location, 
                    notes="30-Min Break"
                )
            elif state['cumulative_driving_since_last_10hr_rest'] >= 11 or state['cumulative_duty_since_last_10hr_rest'] >= 14:
                stops.append({
                    'stop_type': RouteStop.StopType.REST,
                    'location': location,
                    'arrival_time': state['current_time'],
                    'duration_minutes': 10 * 60,
                    'description': '10-Hour Daily Rest'
                })
                _add_hos_log_entry(
                    state=state, 
                    status=DutyStatus.OFF_DUTY, 
                    duration_hrs=10, 
                    location=location, 
                    notes="10-Hour Rest"
                )
