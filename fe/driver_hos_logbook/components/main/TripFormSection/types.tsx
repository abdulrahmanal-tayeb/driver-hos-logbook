export type TripFormSectionProps = {
    initialValues?: {
        current_location?: string;
        pickup_location?: string;
        dropoff_location?: string;
        current_cycle_used?: number;
    };
    onSubmit: (formData: FormData) => void;
    isPending: boolean;
};

