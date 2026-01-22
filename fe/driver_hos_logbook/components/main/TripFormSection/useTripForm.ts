import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";

const locationSchema = yup.string()
    .required("Location is required")
    .min(2, "Too short")
    .test("no-short-numbers", "Must be a valid name or zip code", (value) => {
        if (!value) return false;
        // If it's purely numeric, it must be at least 5 digits (zip code style)
        if (/^\d+$/.test(value)) {
            return value.length === 5;
        }
        // Otherwise, it must contain at least one letter
        return /[a-zA-Z]/.test(value);
    });

const schema = yup.object({
    current_location: locationSchema.required("Current location is required"),
    pickup_location: locationSchema.required("Pickup location is required"),
    dropoff_location: locationSchema.required("Dropoff location is required"),

    current_cycle_used: yup.number()
        .typeError("Must be a number")
        .required("Cycle used is required")
        .min(0, "Minimum is 0")
        .max(70, "Maximum is 70"),
}).required();

export type TripFormData = yup.InferType<typeof schema>;

type UseTripFormProps = {
    initialValues?: {
        current_location?: string;
        pickup_location?: string;
        dropoff_location?: string;
        current_cycle_used?: number;
    };
    onSubmit: (formData: FormData) => void;
};

export function useTripForm({ initialValues, onSubmit }: UseTripFormProps) {
    const form = useForm<TripFormData>({
        resolver: yupResolver(schema),
        defaultValues: {
            current_location: initialValues?.current_location || "",
            pickup_location: initialValues?.pickup_location || "",
            dropoff_location: initialValues?.dropoff_location || "",
            current_cycle_used: initialValues?.current_cycle_used ?? 0,
        },
    });

    const handleSubmit = form.handleSubmit((data: TripFormData) => {
        const formData = new FormData();
        Object.entries(data).forEach(([key, value]) => {
            formData.append(key, String(value));
        });
        onSubmit(formData);
    });

    return {
        ...form,
        handleSubmit,
    };
}

