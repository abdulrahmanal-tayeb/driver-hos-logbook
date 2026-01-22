'use server';

import { revalidatePath } from "next/cache";
import { API_ROUTES } from "./routes";
import { apiFetch } from "./client";

type TripInputPayload = {
  current_location: string;
  pickup_location: string;
  dropoff_location: string;
  current_cycle_used: number;
};

export async function requestListTrips() {
  return apiFetch<
    Array<{
      id: string;
      current_location: string;
      pickup_location: string;
      dropoff_location: string;
      current_cycle_used: string;
      created_at: string;
    }>
  >(API_ROUTES.TRIPS);
}

export async function requestGetTrip(id: string) {
  return apiFetch(API_ROUTES.TRIP_DETAIL(id));
}

export async function requestCalculateTrip(
  payload: TripInputPayload
): Promise<unknown> {
  return apiFetch(API_ROUTES.CALCULATE_TRIP, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function requestCalculateTripAction(formData: FormData) {
  try {
    const rawCycle = formData.get("current_cycle_used");

    const payload: TripInputPayload = {
      current_location: String(formData.get("current_location") ?? ""),
      pickup_location: String(formData.get("pickup_location") ?? ""),
      dropoff_location: String(formData.get("dropoff_location") ?? ""),
      current_cycle_used: Number(rawCycle ?? 0),
    };

    const result = await requestCalculateTrip(payload) as { id: string };
    revalidatePath("/");
    return { success: true, id: result.id };
  } catch (error: any) {
    console.error("Calculate Action Error:", error);
    return {
      success: false,
      error: error.message || "An unexpected error occurred",
      status: error.status || (error.message?.includes("404") ? 404 : 500)
    };
  }
}



