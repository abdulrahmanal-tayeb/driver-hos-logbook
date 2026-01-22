export type TripSummary = {
    id: string;
    current_location: string;
    pickup_location: string;
    dropoff_location: string;
    current_cycle_used: string;
    created_at: string;
};

export type RecentTripsSectionProps = {
    trips: TripSummary[];
    selectedTripId?: string;
};

