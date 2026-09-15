const PRIMARY_API_URL = process.env.NEXT_PUBLIC_API_URL ?? "/api/v1";

const FALLBACK_URLS = [
  PRIMARY_API_URL,
  "/api/v1",
  "http://127.0.0.1:8000/api/v1",
  "http://localhost:8000/api/v1",
  "http://127.0.0.1:8008/api/v1",
  "http://localhost:8008/api/v1",
];

export interface ApiRequestOptions extends RequestInit {
  params?: Record<string, any>;
}

export interface ApiClientFunction {
  <T>(path: string, options?: ApiRequestOptions): Promise<T>;
  get<T>(path: string, options?: ApiRequestOptions): Promise<T>;
  post<T>(path: string, body?: any, options?: ApiRequestOptions): Promise<T>;
  put<T>(path: string, body?: any, options?: ApiRequestOptions): Promise<T>;
  patch<T>(path: string, body?: any, options?: ApiRequestOptions): Promise<T>;
  delete<T>(path: string, options?: ApiRequestOptions): Promise<T>;
}

async function baseApi<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("uzaii_token") : null;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> ?? {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let finalPath = path;
  if (options.params) {
    const query = new URLSearchParams();
    Object.entries(options.params).forEach(([k, v]) => {
      if (v !== undefined && v !== null) {
        query.append(k, String(v));
      }
    });
    const queryString = query.toString();
    if (queryString) {
      finalPath += (finalPath.includes('?') ? '&' : '?') + queryString;
    }
  }

  // Deduplicate target URLs and ensure relative origin is tried first in browser
  const originApi = typeof window !== "undefined" ? `${window.location.origin}/api/v1` : "/api/v1";
  const candidateUrls = Array.from(new Set([originApi, PRIMARY_API_URL, ...FALLBACK_URLS]));

  let lastError: any = null;

  for (const baseUrl of candidateUrls) {
    const targetUrl = `${baseUrl.replace(/\/$/, '')}${finalPath}`;
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

export const api: ApiClientFunction = Object.assign(
  <T>(path: string, options?: ApiRequestOptions) => baseApi<T>(path, options),
  {
    get: <T>(path: string, options?: ApiRequestOptions) =>
      baseApi<T>(path, { ...options, method: 'GET' }),
    post: <T>(path: string, body?: any, options?: ApiRequestOptions) =>
      baseApi<T>(path, {
        ...options,
        method: 'POST',
        body: body !== undefined ? (typeof body === 'string' ? body : JSON.stringify(body)) : undefined,
      }),
    put: <T>(path: string, body?: any, options?: ApiRequestOptions) =>
      baseApi<T>(path, {
        ...options,
        method: 'PUT',
        body: body !== undefined ? (typeof body === 'string' ? body : JSON.stringify(body)) : undefined,
      }),
    patch: <T>(path: string, body?: any, options?: ApiRequestOptions) =>
      baseApi<T>(path, {
        ...options,
        method: 'PATCH',
        body: body !== undefined ? (typeof body === 'string' ? body : JSON.stringify(body)) : undefined,
      }),
    delete: <T>(path: string, options?: ApiRequestOptions) =>
      baseApi<T>(path, { ...options, method: 'DELETE' }),
  }
);
