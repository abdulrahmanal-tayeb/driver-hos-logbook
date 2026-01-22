export function EmptyState() {
    return (
        <div className="py-20 text-center space-y-4">
            <div className="size-16 rounded-full bg-neutral-50 flex items-center justify-center mx-auto text-neutral-200">
                <span className="text-2xl font-bold">?</span>
            </div>
            <div className="space-y-1">
                <h3 className="text-sm font-bold text-neutral-900">No Logs Available</h3>
                <p className="text-[11px] text-neutral-400 font-medium max-w-[240px] mx-auto">
                    Check your trip parameters or try a different route to see HOS compliance logs.
                </p>
            </div>
        </div>
    );
}

