const PRIMARY_API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api/v1";

const FALLBACK_URLS = [
  PRIMARY_API_URL,
  "http://127.0.0.1:8000/api/v1",
  "http://localhost:8000/api/v1",
  "http://127.0.0.1:8008/api/v1",
  "http://localhost:8008/api/v1",
];

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("uzaii_token") : null;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> ?? {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Deduplicate target URLs
  const candidateUrls = Array.from(new Set([PRIMARY_API_URL, ...FALLBACK_URLS]));

  let lastError: any = null;

  for (const baseUrl of candidateUrls) {
    const targetUrl = `${baseUrl.replace(/\/$/, '')}${path}`;
    try {
      const response = await fetch(targetUrl, {
        ...options,
        headers,
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const errorMsg = data?.error?.message ?? `API request failed with status ${response.status}`;
        const error = new Error(errorMsg);
        (error as any).status = response.status;
        (error as any).code = data?.error?.code ?? `HTTP_${response.status}`;
        throw error;
      }

      return data as T;
    } catch (err: any) {
      lastError = err;
      // If it's an HTTP error returned by server (e.g. 400, 401, 403, 404, 500), don't retry on other ports
      if (err?.status && err?.status >= 400) {
        throw err;
      }
      // Continue to next candidate URL on network connection failure
    }
  }

  // Network connection failed across all candidates
  const fallbackError = new Error(
    lastError?.message && lastError?.message !== "Failed to fetch"
      ? lastError.message
      : "Unable to connect to the backend server. Please ensure the backend server is running on localhost."
  );
  (fallbackError as any).status = 503;
  (fallbackError as any).code = "NETWORK_ERROR";
  throw fallbackError;
}
