import Link from "next/link";
import { RecentTripsSectionProps } from "./types";
import { cn } from "@/lib/utils";

export function RecentTripsSection({ trips, selectedTripId }: RecentTripsSectionProps) {
    if (!trips.length) {
        return null;
    }

    const currentSelection = selectedTripId || (trips[0]?.id ?? "");

    return (
        <div className="space-y-4">
            <h3 className="text-xs font-bold text-neutral-500">
                Recent trips
            </h3>
            <div className="space-y-3">

                <div className="space-y-2">
                    {trips.map((trip) => (
                        <Link
                            key={trip.id}
                            href={`/?selected_trip=${trip.id}`}
                            className={cn(
                                "group relative block w-full text-left transition-all pl-4",
                                currentSelection === trip.id ? "opacity-100" : "opacity-60 hover:opacity-100"
                            )}
                        >
                            <div className={cn(
                                "absolute left-0 top-0 bottom-0 w-0.5 transition-all rounded-full",
                                currentSelection === trip.id ? "bg-primary" : "bg-neutral-200 group-hover:bg-neutral-300"
                            )} />
                            <div className="space-y-1">
                                <div className="flex items-center justify-between">
                                    <p className={cn(
                                        "text-xs font-bold truncate",
                                        currentSelection === trip.id ? "text-neutral-900" : "text-neutral-700"
                                    )}>
                                        {trip.current_location}
                                    </p>
                                    <span className="text-[10px] text-neutral-300">→</span>
                                    <p className={cn(
                                        "text-xs font-bold truncate text-right",
                                        currentSelection === trip.id ? "text-neutral-900" : "text-neutral-700"
                                    )}>
                                        {trip.dropoff_location}
                                    </p>
                                </div>
                                <p className="text-[11px] font-medium text-neutral-500">
                                    {trip.pickup_location}
                                </p>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </div>

    );
}

