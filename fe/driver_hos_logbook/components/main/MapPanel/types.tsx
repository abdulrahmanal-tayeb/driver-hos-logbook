import { TripDetail } from "@/types/common";

export type MapPanelProps = {
    trip?: TripDetail | null;
    isLoading?: boolean;
    isNotFound?: boolean;
};
