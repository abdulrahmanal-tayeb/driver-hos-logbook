import {
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";
import { LogGrid } from "../LogGrid";
import { StatCard } from "../StatCard";
import { Remarks } from "../Remarks";
import { DayLogProps } from "./types";

export function DayLog({ log, index, tripId }: DayLogProps) {
    return (
        <AccordionItem value={`day-${index}`} className="border border-neutral-100 rounded-xl overflow-hidden bg-secondary px-6">
            <AccordionTrigger className="hover:no-underline py-6">
                <div className="flex items-baseline gap-3">
                    <span className="text-xs font-bold text-neutral-500">Day {index + 1}</span>
                    <span className="text-sm font-bold text-neutral-900">{log.date}</span>
                </div>
            </AccordionTrigger>
            <AccordionContent className="pb-8 pt-2">
                <div className="space-y-8">
                    <div className="flex items-center justify-between">
                        <div className="text-[10px] font-bold text-neutral-400">
                            {tripId?.slice(0, 8)}
                        </div>
                    </div>
                    {/* THE GRID */}
                    <div className="bg-secondary rounded-xl overflow-hidden border border-neutral-100/50">
                        <LogGrid log={log} />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-[1fr,320px] gap-12">
                        {/* LEFT: Stats & Remarks */}
                        <div className="space-y-10">
                            {/* Stats */}
                            <div className="flex flex-wrap gap-4 justify-between">
                                <StatCard label="Total miles driving" value={log.total_miles_driving} />
                                <StatCard label="Total mileage today" value={log.total_mileage_today} />
                            </div>

                            {/* Remarks */}
                            <Remarks logEntries={log.log_entries} />
                        </div>

                        {/* RIGHT: Recap Table */}
                        <div className="space-y-8">
                            <h4 className="text-[11px] font-bold text-neutral-600">Recap</h4>
                            <div className="space-y-4 text-xs">
                                <div className="flex justify-between items-end border-b border-neutral-100 pb-2">
                                    <span className="text-neutral-500 font-bold text-[10px]">On duty today</span>
                                    <span className="font-bold text-neutral-900 text-sm">{log.recap?.on_duty_today ?? '0.00'}</span>
                                </div>
                                <div className="flex justify-between items-end border-b border-neutral-100 pb-2">
                                    <span className="text-neutral-500 font-bold text-[10px]">Total last 8 days</span>
                                    <span className="font-bold text-neutral-900 text-sm">{log.recap?.total_last_8_days ?? '0.00'}</span>
                                </div>
                                <div className="flex justify-between items-end">
                                    <span className="text-primary font-black text-[11px]">Available Tomorrow</span>
                                    <span className="font-black text-primary text-2xl leading-none">{log.recap?.available_tomorrow ?? '70.00'}</span>
                                </div>
                            </div>

                            <div className="pt-6 grid grid-cols-2 gap-x-4 gap-y-6 border-t border-neutral-300">
                                <div className="space-y-2">
                                    <p className="text-[10px] font-bold text-neutral-500">Off duty (total)</p>
                                    <p className="inline-flex items-center justify-center bg-neutral-900 text-white px-2 py-0.5 rounded text-[11px] font-bold min-w-[2.5rem]">
                                        {log.total_off_duty.toFixed(2)}
                                    </p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-[10px] font-bold text-neutral-500">Sleeper (total)</p>
                                    <p className="inline-flex items-center justify-center bg-neutral-900 text-white px-2 py-0.5 rounded text-[11px] font-bold min-w-[2.5rem]">
                                        {log.total_sleeper.toFixed(2)}
                                    </p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-[10px] font-bold text-neutral-500">Driving (total)</p>
                                    <p className="inline-flex items-center justify-center bg-neutral-900 text-white px-2 py-0.5 rounded text-[11px] font-bold min-w-[2.5rem]">
                                        {log.total_driving.toFixed(2)}
                                    </p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-[10px] font-bold text-neutral-500">On duty (total)</p>
                                    <p className="inline-flex items-center justify-center bg-neutral-900 text-white px-2 py-0.5 rounded text-[11px] font-bold min-w-[2.5rem]">
                                        {log.total_on_duty.toFixed(2)}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </AccordionContent>
        </AccordionItem>
    );
}

