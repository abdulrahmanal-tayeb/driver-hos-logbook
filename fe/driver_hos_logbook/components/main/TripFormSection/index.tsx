"use client";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { TripFormSectionProps } from "./types";
import { useTripForm } from "./useTripForm";
import Spinner from "@/components/ui/spinner";

export function TripFormSection({ initialValues, onSubmit, isPending }: TripFormSectionProps) {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useTripForm({ initialValues, onSubmit });

    return (
        <div className="space-y-4">
            <h3 className="text-xs font-bold text-neutral-500">
                Trip planner
            </h3>
            <div className="space-y-6">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="current_location" className={errors.current_location ? "text-red-500" : ""}>Current location</Label>
                        <Input
                            id="current_location"
                            {...register("current_location")}
                            className={errors.current_location ? "border-red-200 focus:ring-red-500" : "border-neutral-200"}
                            disabled={isPending}
                        />
                        {errors.current_location && <p className="text-[11px] text-red-500 font-bold">{errors.current_location.message}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="pickup_location" className={errors.pickup_location ? "text-red-500" : ""}>Pickup location</Label>
                        <Input
                            id="pickup_location"
                            {...register("pickup_location")}
                            className={errors.pickup_location ? "border-red-200 focus:ring-red-500" : "border-neutral-200"}
                            disabled={isPending}
                        />
                        {errors.pickup_location && <p className="text-[11px] text-red-500 font-bold">{errors.pickup_location.message}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="dropoff_location" className={errors.dropoff_location ? "text-red-500" : ""}>Dropoff location</Label>
                        <Input
                            id="dropoff_location"
                            {...register("dropoff_location")}
                            className={errors.dropoff_location ? "border-red-200 focus:ring-red-500" : "border-neutral-200"}
                            disabled={isPending}
                        />
                        {errors.dropoff_location && <p className="text-[11px] text-red-500 font-bold">{errors.dropoff_location.message}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="current_cycle_used" className={errors.current_cycle_used ? "text-red-500" : ""}>Current cycle used (hrs)</Label>
                        <Input
                            id="current_cycle_used"
                            type="number"
                            step={0.25}
                            {...register("current_cycle_used")}
                            className={errors.current_cycle_used ? "border-red-200 focus:ring-red-500" : "border-neutral-200"}
                            disabled={isPending}
                        />
                        {errors.current_cycle_used && <p className="text-[11px] text-red-500 font-bold">{errors.current_cycle_used.message}</p>}
                    </div>

                    <Button type="submit" className="w-full" disabled={isPending}>
                        {isPending ? (
                            <div className="flex items-center gap-2">
                                <Spinner className="size-3" />
                                <span>Calculating...</span>
                            </div>
                        ) : "Calculate trip"}
                    </Button>
                </form>
            </div>
        </div>
    );
}

