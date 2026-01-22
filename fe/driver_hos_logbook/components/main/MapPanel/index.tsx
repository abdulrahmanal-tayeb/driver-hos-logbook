"use client";

import { useEffect, useRef } from "react";
import { MapPanelProps } from "./types";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix for default marker icons in Leaflet + Next.js
const fixLeafletIcons = () => {
    // @ts-ignore
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
        iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
    });
};

import { LoadingState } from "./LoadingState";
import { ErrorState } from "./ErrorState";
import { EmptyState } from "./EmptyState";

export function MapPanel({ trip, isLoading, isNotFound }: MapPanelProps) {
    const mapRef = useRef<HTMLDivElement>(null);
    const mapInstance = useRef<L.Map | null>(null);

    // ... (rest of the logic remains same, just need to update params and return)


    useEffect(() => {
        if (!mapRef.current || mapInstance.current) return;
        fixLeafletIcons();

        mapInstance.current = L.map(mapRef.current).setView([39.8283, -98.5795], 4);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(mapInstance.current);

        return () => {
            mapInstance.current?.remove();
            mapInstance.current = null;
        };
    }, []);

    useEffect(() => {
        if (!mapInstance.current || !trip) return;

        // Clear existing layers
        mapInstance.current.eachLayer((layer) => {
            if (!(layer instanceof L.TileLayer)) {
                mapInstance.current?.removeLayer(layer);
            }
        });

        const bounds = L.latLngBounds([]);

        // Render Geometry
        if (trip.route_geometry) {
            const geoJsonLayer = L.geoJSON(trip.route_geometry as any, {
                style: { color: "#3b82f6", weight: 5, opacity: 0.7 }
            }).addTo(mapInstance.current);
            bounds.extend(geoJsonLayer.getBounds());
        }

        // Render Stops
        trip.stops?.forEach((stop) => {
            const marker = L.marker([Number(stop.latitude || 0), Number(stop.longitude || 0)])
                .addTo(mapInstance.current!)
                .bindPopup(`
                    <div class="text-xs">
                        <strong class="text-primary font-bold">${stop.stop_type}</strong><br/>
                        ${stop.location}<br/>
                        <span class="text-neutral-500">${new Date(stop.arrival_time).toLocaleString()}</span>
                    </div>
                `);

            if (stop.latitude && stop.longitude) {
                bounds.extend([Number(stop.latitude), Number(stop.longitude)]);
            }
        });

        if (bounds.isValid()) {
            mapInstance.current.fitBounds(bounds, { padding: [50, 50] });
        }
    }, [trip]);

    return (
        <div className="h-[500px] w-full relative group">
            <div ref={mapRef} className="h-full w-full z-0" />

            {/* Loading Overlay */}
            {isLoading && <LoadingState />}

            {/* Not Found Overlay */}
            {!isLoading && isNotFound && <ErrorState />}

            {/* Empty State */}
            {!isLoading && !isNotFound && !trip && <EmptyState />}
        </div>
    );
}


