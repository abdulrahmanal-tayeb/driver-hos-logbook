"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { TripFormSection } from "../TripFormSection";
import { RecentTripsSection } from "../RecentTripsSection";
import { MapPanel } from "../MapPanel";
import { DailyLogsPanel } from "../DailyLogsPanel";
import { TripDetail } from "@/types/common";
import { requestCalculateTripAction } from "@network/requests";
import { toast } from "sonner";

export type TripDashboardProps = {
    initialTrips: any[];
    initialTripDetail: TripDetail | null;
    selectedTripId: string | undefined;
};

export function TripDashboard({ initialTrips, initialTripDetail, selectedTripId }: TripDashboardProps) {
    const router = useRouter();
    const [isPending, startTransition] = useTransition();
    const [isNotFound, setIsNotFound] = useState(false);

    const handleCalculate = async (formData: FormData) => {
        setIsNotFound(false);
        startTransition(async () => {
            const result = await requestCalculateTripAction(formData);
            console.log(result);
            if (result.success && result.id) {
                router.push(`/?selected_trip=${result.id}`);
            } else if (!result.success) {
                if (result.status === 404) {
                    setIsNotFound(true);
                } else {
                    toast.error(result.error || "Failed to calculate trip.");
                }
            }
        });
    };


    return (
        <div className="space-y-12">
            <div className="grid gap-8 lg:grid-cols-[400px_1fr] items-start">
                <div className="space-y-8">
                    <TripFormSection
                        onSubmit={handleCalculate}
                        isPending={isPending}
                    />
                    <RecentTripsSection
                        trips={initialTrips}
                        selectedTripId={selectedTripId}
                    />
                </div>

                <section className="sticky top-8 rounded-xl overflow-hidden shadow-2xl shadow-neutral-200/50 border border-neutral-100 bg-black text-white">
                    <div className="p-[12px] font-semibold">
                        <h2 className="text-xs">Route Map</h2>
                    </div>
                    <MapPanel
                        trip={initialTripDetail}
                        isLoading={isPending}
                        isNotFound={isNotFound}
                    />
                </section>
            </div>

            {(initialTripDetail && !isPending) && (
                <section className="pt-8 border-t border-neutral-100">
                    <h2 className="text-sm font-bold mb-8 text-neutral-500 text-center">Daily Log Sheets (HOS Compliance)</h2>
                    <DailyLogsPanel
                        trip={initialTripDetail}
                        isNotFound={isNotFound}
                    />
                </section>
            )}
        </div>
    );
}
