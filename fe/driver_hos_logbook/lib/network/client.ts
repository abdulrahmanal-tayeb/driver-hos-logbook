const apiBase = process.env.BACKEND_BASE_URL ?? "http://localhost:8000";
const apiPrefix = process.env.BACKEND_PREFIX ?? "/api/v1/";

type ApiOptions = Omit<RequestInit, "headers"> & {
  headers?: HeadersInit;
};

export async function apiFetch<TResponse>(
  path: string,
  options: ApiOptions = {}
): Promise<TResponse> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers ?? {}),
  };

  // Ensure apiBase doesn't end with slash, apiPrefix starts and ends with slash, and path doesn't start with slash
  const cleanBase = apiBase.endsWith('/') ? apiBase.slice(0, -1) : apiBase;
  const cleanPrefix = apiPrefix.startsWith('/') ? apiPrefix : `/${apiPrefix}`;
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;

  const fullUrl = `${cleanBase}${cleanPrefix}${cleanPath}`;

  const res = await fetch(fullUrl, {
    ...options,
    headers,
  });

  if (!res.ok) {
    let message = `Request failed with status ${res.status}`;
    try {
      const data = await res.json();
      if (data && typeof data.detail === "string") {
        message = data.detail;
      }
    } catch {
      // ignore parse errors, keep generic message
    }
    throw new Error(message);
  }

  if (res.status === 204) {
    // No content
    return undefined as TResponse;
  }

  return (await res.json()) as TResponse;
}


