"use client";

import React from "react";
import { DutyStatus, DutyStatusConfig, DailyLog } from "../types";
import { LogGridProps } from "./types";

export function LogGrid({ log }: LogGridProps) {
    const hours = Array.from({ length: 25 }, (_, i) => i);
    const fifteenMinTicks = Array.from({ length: 24 * 4 }, (_, i) => i);

    const statuses: DutyStatusConfig[] = [
        { id: DutyStatus.OFF_DUTY, label: "Off Duty", y: 30 },
        { id: DutyStatus.SLEEPER_BERTH, label: "Sleeper", y: 70 },
        { id: DutyStatus.DRIVING, label: "Driving", y: 110 },
        { id: DutyStatus.ON_DUTY_NOT_DRIVING, label: "On Duty", y: 150 },
    ];

    const GRID_START_X = 120;
    const GRID_WIDTH = 840;

    // Use current log's midnight as the reference point
    const logDate = new Date(log.date);
    logDate.setHours(0, 0, 0, 0);
    const baseTime = logDate.getTime();
    const msInDay = 24 * 60 * 60 * 1000;

    const getX = (timeStr: string) => {
        const time = new Date(timeStr).getTime();
        const progress = (time - baseTime) / msInDay;
        // Clamp and map to grid
        const clampedProgress = Math.max(0, Math.min(1, progress));
        return GRID_START_X + clampedProgress * GRID_WIDTH;
    };

    const renderStatusLabels = () => {
        return statuses.map((s) => (
            <React.Fragment key={s.id}>
                <text x="10" y={s.y + 4} className="text-[11px] font-bold fill-neutral-600" textAnchor="start">
                    {s.label}
                </text>
                <line x1={GRID_START_X} y1={s.y} x2={GRID_START_X + GRID_WIDTH} y2={s.y} stroke="#f0f0f0" strokeWidth="1" />
            </React.Fragment>
        ));
    };

    const renderFifteenMinuteTicks = () => {
        return fifteenMinTicks.map((t) => {
            const x = GRID_START_X + (t / (24 * 4)) * GRID_WIDTH;
            if (t % 4 === 0) return null; // Skip full hours (handled below)
            return (
                <line key={`tick-${t}`} x1={x} y1="25" x2={x} y2="155" stroke="#f0f0f0" strokeWidth="1" />
            );
        });
    };

    const renderHourLinesAndLabels = () => {
        return hours.map((h) => {
            const x = GRID_START_X + (h / 24) * GRID_WIDTH;
            return (
                <React.Fragment key={h}>
                    <line x1={x} y1="20" x2={x} y2="160" stroke="#e5e5e5" strokeWidth={h % 6 === 0 ? "2" : "1"} />
                    <text x={x} y="180" className="text-[11px] font-medium fill-neutral-400" textAnchor="middle">
                        {h === 0 || h === 24 ? "Mid" : h === 12 ? "Noon" : h}
                    </text>
                </React.Fragment>
            );
        });
    };

    const renderLogSegments = () => {
        const segments: React.ReactNode[] = [];
        const entries = log.log_entries || [];

        for (let i = 0; i < entries.length; i++) {
            const entry = entries[i];
            const nextEntry = entries[i + 1];

            const startMs = new Date(entry.start_time).getTime();
            const endMs = new Date(entry.end_time).getTime();

            // Only draw if segment overlaps with the current day
            if (endMs <= baseTime || startMs >= baseTime + msInDay) continue;

            const xStart = getX(entry.start_time);
            const xEnd = getX(entry.end_time);
            const status = statuses.find(s => s.id === entry.duty_status);

            if (status) {
                // Horizontal line for current status
                segments.push(
                    <line
                        key={`h-${i}`}
                        x1={xStart}
                        y1={status.y}
                        x2={xEnd}
                        y2={status.y}
                        stroke="#3b82f6"
                        strokeWidth="4"
                        strokeLinecap="round"
                    />
                );

                // Vertical line to connect to next status
                if (nextEntry) {
                    const nextStatus = statuses.find(s => s.id === nextEntry.duty_status);
                    if (nextStatus) {
                        segments.push(
                            <line
                                key={`v-${i}`}
                                x1={xEnd}
                                y1={status.y}
                                x2={xEnd}
                                y2={nextStatus.y}
                                stroke="#3b82f6"
                                strokeWidth="2"
                                strokeOpacity="0.4"
                            />
                        );
                    }
                }
            }
        }

        return segments;
    };

    return (
        <div className="relative w-full overflow-x-auto">
            <div className="min-w-[850px] bg-white p-6">
                <svg viewBox="0 0 1000 200" className="w-full" preserveAspectRatio="none">
                    {/* Background Grid Labels */}
                    {renderStatusLabels()}

                    {/* 15-minute Ticks */}
                    {renderFifteenMinuteTicks()}

                    {/* Hour Vertical Lines & Labels */}
                    {renderHourLinesAndLabels()}

                    {/* The actual log line segments */}
                    {renderLogSegments()}
                </svg>
            </div>
        </div>

    );
}

