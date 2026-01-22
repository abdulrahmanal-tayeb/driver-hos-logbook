export function ErrorState() {
    return (
        <div className="absolute inset-0 flex items-center justify-center bg-neutral-50/90 backdrop-blur-[4px] z-10 transition-all duration-300">
            <div className="text-center space-y-2 max-w-xs px-6">
                <div className="size-10 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
                    <span className="text-red-400 font-bold text-lg">!</span>
                </div>
                <h4 className="text-sm font-bold text-neutral-900">Route Not Found</h4>
                <p className="text-[11px] text-neutral-500 leading-relaxed font-medium">
                    We couldn't calculate a route for these locations. Please check the addresses and try again.
                </p>
            </div>
        </div>
    );
}

