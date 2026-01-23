import { DailyLogsPanelProps } from "./types";
import { EmptyState } from "./EmptyState";
import { DayLog } from "./DayLog";
import { Accordion } from "@/components/ui/accordion";

export function DailyLogsPanel({ trip, isNotFound }: DailyLogsPanelProps) {
    const logs = trip?.daily_logs ?? [];

    if (isNotFound) {
        return <EmptyState />;
    }

    return (
        <Accordion type="multiple" className="w-full space-y-4" defaultValue={["day-0"]}>
            {logs.map((log, index) => (
                <DayLog key={`${log.date}-${index}`} log={log} index={index} tripId={trip?.id} />
            ))}
        </Accordion>
    );
}

