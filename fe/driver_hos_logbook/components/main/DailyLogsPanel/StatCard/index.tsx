import { StatProps } from "./types";

export function StatCard({ label, value }: StatProps) {
    return (
        <div className="space-y-1 bg-neutral-900 text-white rounded-xl p-2 flex justify-center items-center flex-col w-fit min-w-[160px]">
            <p className="text-[11px] font-bold">{label}</p>
            <p className="text-3xl font-bold text-white">{value}</p>
        </div>
    );
}

