export type TripDetail = {
    id: string;
    route_geometry?: unknown;
    log_entries?: Array<{
        duty_status: string;
        start_time: string;
        end_time: string;
        location: string;
        notes?: string | null;
    }>;
    stops?: Array<{
        stop_type: string;
        location: string;
        latitude?: number | string;
        longitude?: number | string;
        arrival_time: string;
        description?: string | null;
    }>;

    daily_logs?: Array<{
        date: string;
        total_miles_driving: string | number;
        total_mileage_today: string | number;
        total_off_duty: number;
        total_sleeper: number;
        total_driving: number;
        total_on_duty: number;
        log_entries?: Array<{
            duty_status: string;
            start_time: string;
            end_time: string;
            location: string;
            notes?: string | null;
        }>;
        recap?: {
            on_duty_today: number;
            total_last_8_days: number;
            available_tomorrow: number;
        };
    }>;
};