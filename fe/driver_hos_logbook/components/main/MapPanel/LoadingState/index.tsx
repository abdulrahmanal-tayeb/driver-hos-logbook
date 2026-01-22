import Spinner from "@/components/ui/spinner";

export function LoadingState() {
    return (
        <div className="absolute inset-0 flex items-center justify-center bg-white/40 backdrop-blur-[2px] z-20 transition-all duration-300">
            <div className="flex flex-col items-center gap-3 scale-110">
                <Spinner className="size-8 text-primary" />
                <span className="text-[11px] font-bold text-neutral-500 animate-pulse">Calculating Route...</span>
            </div>
        </div>
    );
}

