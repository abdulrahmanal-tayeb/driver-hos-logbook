export const API_ROUTES = {
  CALCULATE_TRIP: "/api/v1/logbook/trips/calculate/",
  TRIPS: "/api/v1/logbook/trips/",
  TRIP_DETAIL: (id: string) => `/api/v1/logbook/trips/${id}/`,
} as const;
