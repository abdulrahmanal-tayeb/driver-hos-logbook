import { NavProps } from "./types";

export function Nav({ }: NavProps) {
    return (
        <header className="border-b border-neutral-200 bg-white">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
                <h1 className="text-sm font-bold text-neutral-800">
                    Driver HOS Logbook
                </h1>
            </div>
        </header>

    );
}
