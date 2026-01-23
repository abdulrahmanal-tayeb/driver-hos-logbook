export const API_ROUTES = {
  CALCULATE_TRIP: "logbook/trips/calculate/",
  TRIPS: "logbook/trips/",
  TRIP_DETAIL: (id: string) => `logbook/trips/${id}/`,
} as const;
