import { requestListTrips, requestGetTrip } from "@network/requests";
import { TripDetail } from "@/types/common";
import { TripDashboard } from "../components/main/TripDashboard";


export default async function Home(props: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const searchParams = await props.searchParams;
  const selectedTripId = (searchParams.selected_trip as string) || undefined;

  const trips = await requestListTrips().catch(() => []);

  const tripToFetch = selectedTripId || (trips[0]?.id ?? null);
  const currentTrip = (tripToFetch
    ? await requestGetTrip(tripToFetch).catch(() => null)
    : null) as TripDetail | null;


  return (
    <TripDashboard
      initialTrips={trips}
      initialTripDetail={currentTrip}
      selectedTripId={selectedTripId}
    />
  );

}