import { RemarksProps } from "./types";

export function Remarks({ logEntries }: RemarksProps) {
    const filteredEntries = logEntries?.filter((entry, i, arr) => 
        i === 0 || entry.duty_status !== arr[i - 1].duty_status
    );

    return (
        <div className="space-y-4">
            <h4 className="text-[11px] font-bold text-neutral-600">Remarks</h4>
            <div className="space-y-1">
                {filteredEntries?.map((entry, i) => (
                    <div key={i} className="flex items-center gap-6 py-2 border-b border-neutral-300 last:border-0 text-[11px]">
                        <span className="w-16 font-bold text-neutral-500">
                            {new Date(entry.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                        <span className="flex-1 font-bold text-neutral-800">{entry.location}</span>
                        <span className="w-32 text-right font-bold text-primary text-[10px]">
                            {entry.duty_status.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}

