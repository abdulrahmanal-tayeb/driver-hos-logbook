import { TripDetail } from "@/types/common";

export type DailyLog = Exclude<TripDetail["daily_logs"], undefined>[number];

export type DailyLogsPanelProps = {
    trip?: TripDetail | null;
    isLoading?: boolean;
    isNotFound?: boolean;
};

export enum DutyStatus {
    OFF_DUTY = "OFF_DUTY",
    SLEEPER_BERTH = "SLEEPER_BERTH",
    DRIVING = "DRIVING",
    ON_DUTY_NOT_DRIVING = "ON_DUTY_NOT_DRIVING",
}

export type DutyStatusConfig = {
    id: DutyStatus;
    label: string;
    y: number;
};
